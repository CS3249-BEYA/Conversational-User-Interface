"""
Content moderation module for safety enforcement.
Students must complete TODO sections according to POLICY.md.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from .config import SAFETY_MODE

logger = logging.getLogger(__name__)


class ModerationAction(Enum):
    """Possible moderation actions."""
    ALLOW = "allow"
    BLOCK = "block"
    SAFE_FALLBACK = "safe_fallback"


@dataclass
class ModerationResult:
    """Result of moderation check."""
    action: ModerationAction
    tags: List[str]  # Policy tags that were triggered
    reason: str  # Human-readable explanation
    confidence: float  # Confidence level (0-1)
    fallback_response: Optional[str] = None  # Response to use if action != ALLOW


class Moderator:
    """Handles content moderation according to safety policy."""
    
    def __init__(self):
        """Initialize the moderator with safety rules."""
        self.safety_mode = SAFETY_MODE
        self._initialize_rules()
    
    def _initialize_rules(self):
        """
        Initialize moderation rules based on POLICY.md.
        TODO: Students must define these based on their POLICY.md
        
        IMPLEMENTATION GUIDE:
        1. Copy all keywords and patterns from your completed POLICY.md
        2. Ensure Python formatting (lists, strings, regex compilation)
        3. Templates should be multi-line strings with proper formatting
        """
        
        # TODO: Define crisis keywords and patterns
        # These should detect immediate risk of harm
        self.crisis_keywords = [
            # Direct suicide mentions:
            "suicide", "end my life", "kill myself", "take my life", "can't go on", "better off dead", "ready to die",
            # Self-harm expressions:
            "hurt myself", "self-harm", "cut myself", "injure myself", "harming myself", "punish myself",
            # Imminent danger indicators:
            "goodbye forever", "final message", "last time", "won't be here", "leaving soon", "over it all",
            # Emotional crisis expressions:
            "hopeless", "worthless", "can't take it", "don't see the point", "at my wit's end", "giving up"
        ]
        
        # TODO: Crisis patterns - regex for complex expressions
        self.crisis_patterns = [
            r"\b(want|going|plan|ready) to (die|kill|hurt|end)\b",
            r"\b(thinking|thought) about (suicide|dying|ending it)\b",
            r"\b(no|don't have) a (reason|point) to (live|go on|continue)\b",
            r"\b(tonight|tomorrow|this weekend) (i will|i'm going to)\b",
            r"\b(wish|wishing) i was (dead|gone)\b",
            r"\b(can't take|can't stand) this (anymore|any longer)\b",
            r"\b(what's|what is) the point of living\b",
            r"\b(going to|gonna) (hurt myself|self-harm|end it)\b"
        ]
        
        # TODO: Define medical request patterns
        self.medical_keywords = [
            # Diagnosis requests:
            "diagnose", "what condition", "do I have", "am I sick", "is this a disorder", "what's wrong with me",
            # Medication/treatment:
            "medication", "what pills", "drugs for", "cure for", "what treatment", "prescribe me", "side effects", "what should I take",
            # Mental health specific:
            "am i depressed", "bipolar", "schizophrenic", "anorexia", "adhd", "ocd", "anxiety disorder", "what's my diagnosis",
            # Other:
            "psychiatrist recommendation", "doctor's advice", "medical advice"
        ]
        
        # TODO: Medical patterns - regex for complex expressions
        self.medical_patterns = [
            r"\b(prescribe|recommend|suggest) (medication|pills|drugs)\b",
            r"\bwhat (medication|medicine|pills) should i take\b",
            r"\bdo i have (depression|anxiety|bipolar|ocd)\b",
            r"\bcan you diagnose me\b",
            r"\bwhat is the best treatment for\b",
            r"\bshould i take (a drug|a pill) for\b",
            r"\bwhat are the side effects of\b",
            r"\bwhere can i find a psychiatrist\b"
        ]
        
        # TODO: Define harmful content patterns
        self.harmful_content = {
            "violence": [
                "attack", "revenge", "hurt someone", "beat up", "murder", "kill a person", "assault", "threaten"
            ],
            "illegal": [
                "buy drugs", "sell drugs", "illegal activities", "stolen goods", "fraud", "hacking", "piracy", "smuggling"
            ],
            "harassment": [
                "hate speech", "discriminate", "harass", "bully", "stalk", "doxxing", "threaten to expose", "insult"
            ]
        }
        
        # TODO: Define confidence thresholds based on safety mode
        self.confidence_thresholds = {
            "strict": {
                "crisis": 0.3,
                "medical": 0.4,
                "harmful": 0.5,
            },
            "balanced": {
                "crisis": 0.6,
                "medical": 0.7,
                "harmful": 0.8,
            },
            "permissive": {
                "crisis": 0.9,
                "medical": 0.95,
                "harmful": 0.95,
            }
        }
        
        # TODO: Define safety fallback templates
        # Copy complete templates from POLICY.md
        self.fallback_templates = {
            "crisis": """
I'm deeply concerned about what you're sharing. Your safety is my top priority, and I want you to know that help is available right now. Your life has value, and there are people who want to support you through this. Please reach out to trained crisis counselors immediately:
- Singapore Association for Mental Health (SAMH) 24-hour helpline: 1800 283 7019
- Samaritans of Singapore (SOS) Crisis Helpline: 1800 221 4444
- Institute of Mental Health (IMH) Hotline: 6389 2222
It sounds like you are going through an extremely difficult time, and feeling overwhelmed is understandable. You are not alone in this, and reaching out to trained professionals can help you navigate these intense emotions safely. Even if it feels hard to take the first step, talking to someone who is trained to listen and provide support can make a real difference.
Remember, seeking help is a sign of strength, and connecting with professional support can help you find safety and stability. Please consider contacting one of the hotlines above immediately. Your life matters, and support is just a call or text away.
            """,

            "medical": """
I understand you're looking for medical guidance, and I appreciate you reaching out. However, I'm not qualified to provide medical diagnoses or treatment recommendations.
I hear that you are concerned about your mental health and may be seeking advice on medication, diagnosis, or treatment options. It's completely valid to have these questions, and acknowledging them is an important step toward support.
For your health and safety, please consult with:
- A licensed psychiatrist for medication questions
- A licensed psychologist or counselor for therapy and mental health evaluation
- Your primary care doctor for any general medical concerns
While I cannot provide medical advice, I can offer empathetic listening and help you reflect on your thoughts and emotions. I can also provide information on coping strategies, stress management techniques, and point you toward professional resources that are appropriate for your situation.
Remember, seeking professional help is a sign of strength. You are taking an important step by reaching out, and support is available to guide you safely through this journey.
            """,

            "harmful": """
I cannot and will not provide assistance with that request as it could potentially cause harm. My purpose is to provide a safe and supportive conversation, and I cannot engage in or support discussions of violence, illegal activities, or harassment. This is a strict boundary of our conversation. If you are experiencing distress, I am here to listen, but we must keep our conversation within a safe and constructive space. I encourage you to redirect our conversation to a topic that aligns with my purpose of offering emotional support.
            """,

            "disclaimer": """
Welcome to the Psychological Pre-Consultation Support System.

IMPORTANT DISCLAIMER:
This is an AI support system designed to provide initial emotional support and guidance. Please note:
- This system is not a substitute for professional medical advice, diagnosis, or treatment.
- It does not offer emergency services.
- The conversation is not monitored by a human professional.
- Your privacy is important, but please do not share personally identifiable information.
- Any information shared is for support purposes only and should not be considered a clinical record.

When to Seek Immediate Help:
If you are in immediate danger or a crisis situation, please contact emergency services or a crisis hotline. Examples include thoughts of self-harm, harm to others, or any other immediate safety risk.

What I Can Offer:
- A non-judgmental and empathetic listening space
- Techniques for stress and anxiety management
- Support in navigating common life challenges
- Guidance on finding professional mental health resources

Your wellbeing is important. How can I support you today?
            """,
        }

    
    def moderate(
        self,
        user_prompt: str,
        model_response: Optional[str] = None,
        context: Optional[List[Dict]] = None,
    ) -> ModerationResult:
        """
        Perform moderation on user input and/or model output.
        
        Args:
            user_prompt: The user's input text
            
        Returns:
            ModerationResult with action and explanation
            
        IMPLEMENTATION ORDER:
        1. Check crisis (highest priority - must not miss)
        2. Check medical (prevent harmful advice)
        3. Check harmful content (filter inappropriate)
        """
        
        # Step 1: Check for crisis indicators (highest priority)
        crisis_check = self._check_crisis(user_prompt)
        if crisis_check.action != ModerationAction.ALLOW:
            logger.warning(f"Crisis detected: {crisis_check.reason}")
            return crisis_check

        # Step 2: Check for medical requests
        medical_check = self._check_medical(user_prompt)
        if medical_check.action != ModerationAction.ALLOW:
            logger.warning(f"Medical request detected: {medical_check.reason}")
            return medical_check

        # Step 3: Check for harmful content
        harmful_check = self._check_harmful(user_prompt)
        if harmful_check.action != ModerationAction.ALLOW:
            logger.warning(f"Harmful content detected: {harmful_check.reason}")
            return harmful_check

        # If model response provided, check it
        if model_response:
            output_check = self._check_model_output(model_response)
            if output_check.action != ModerationAction.ALLOW:
                logger.warning(f"Output violation: {output_check.reason}")
                return output_check

        # Check context for concerning patterns
        if context:
            context_check = self._check_context_patterns(context)
            if context_check.action != ModerationAction.ALLOW:
                logger.info(f"Context concern: {context_check.reason}")
                return context_check

        # Default: Allow
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Content passes all safety checks",
            confidence=1.0,
        )
    
    def _check_crisis(self, text: str) -> ModerationResult:
        """
        Check for crisis indicators.
        
        TODO: Implement crisis detection
        
        ALGORITHM:
        1. Convert text to lowercase
        2. Check against crisis_keywords:
           - If found, set confidence = 0.7
           - Track which keywords were found
        3. Check against crisis_patterns:
           - If matched, set confidence = 0.8-0.9
           - Use re.search() for each pattern
        4. If multiple matches, use MAXIMUM confidence
        5. Get threshold for current safety_mode
        6. If confidence >= threshold:
           - Return BLOCK action
           - Include crisis fallback_response
           - Add descriptive tags
        7. Otherwise return ALLOW
        """

        text_lower = text.lower()
        confidence = 0.0
        detected_tags = []

        # Check keywords
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                confidence = max(confidence, 0.7)
                detected_tags.append(f"crisis_keyword:{keyword}")

        # Check regex patterns
        for pattern in self.crisis_patterns:
            if re.search(pattern, text_lower):
                confidence = max(confidence, 0.9)
                detected_tags.append(f"crisis_pattern:{pattern}")

        crisis_threshold = self.confidence_thresholds[self.safety_mode.value]["crisis"]

        if confidence >= crisis_threshold:
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=detected_tags,
                reason="Crisis indicator detected.",
                confidence=confidence,
                fallback_response=self.fallback_templates["crisis"]
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No crisis indicators detected",
            confidence=confidence,
        )
    
    def _check_medical(self, text: str) -> ModerationResult:
        """
        Check for medical requests.
        
        TODO: Implement medical request detection
        
        ALGORITHM:
        1. Convert text to lowercase
        2. Check against medical_keywords (confidence = 0.7)
        3. Check against medical_patterns (confidence = 0.85)
        4. Use maximum confidence if multiple matches
        5. Compare against threshold for safety_mode
        6. Return SAFE_FALLBACK if threshold exceeded
        
        Note: Use SAFE_FALLBACK, not BLOCK, for medical requests
        """
        text_lower = text.lower()
        confidence = 0.0
        detected_tags = []

        # Check keywords
        for keyword in self.medical_keywords:
            if keyword in text_lower:
                confidence = max(confidence, 0.7)
                detected_tags.append(f"medical_keyword:{keyword}")

        # Check regex patterns
        for pattern in self.medical_patterns:
            if re.search(pattern, text_lower):
                confidence = max(confidence, 0.85)
                detected_tags.append(f"medical_pattern:{pattern}")

        medical_threshold = self.confidence_thresholds[self.safety_mode.value]["medical"]

        if confidence >= medical_threshold:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=detected_tags,
                reason="Medical request detected.",
                confidence=confidence,
                fallback_response=self.fallback_templates["medical"]
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No medical requests detected",
            confidence=confidence,
        )
    
    def _check_harmful(self, text: str) -> ModerationResult:
        """
        Check for harmful content.
        
        TODO: Implement harmful content detection
        
        ALGORITHM:
        1. Convert text to lowercase
        2. For each category in harmful_content:
           - Check if any keywords present
           - Track which categories triggered
        3. Set confidence = 0.75 for any match
        4. Compare against threshold
        5. Return BLOCK if threshold exceeded
        
        Include triggered categories in tags for debugging
        """

        text_lower = text.lower()
        confidence = 0.0
        detected_tags = []

        for category, keywords in self.harmful_content.items():
            for keyword in keywords:
                if keyword in text_lower:
                    confidence = max(confidence, 0.75)
                    detected_tags.append(
                        f"harmful:{category}_keyword:{keyword}")

        harmful_threshold = self.confidence_thresholds[self.safety_mode.value]["harmful"]

        if confidence >= harmful_threshold:
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=detected_tags,
                reason="Harmful content detected.",
                confidence=confidence,
                fallback_response=self.fallback_templates["harmful"]
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No harmful content detected",
            confidence=confidence,
        )
    
    def _check_model_output(self, response: str) -> ModerationResult:
        """
        Check model output for policy violations.
        
        TODO: Ensure model didn't provide medical advice or break boundaries
        
        ALGORITHM:
        1. Check for medical_keywords that shouldn't appear
        2. Look for diagnosis-like statements
        3. Check for treatment recommendations
        4. Return SAFE_FALLBACK if violations found

        """

        response_lower = response.lower()

        # Look for medical keywords in the model's response
        for keyword in self.medical_keywords:
            if keyword in response_lower:
                return ModerationResult(
                    action=ModerationAction.SAFE_FALLBACK,
                    tags=["model_output_medical_violation"],
                    reason="Model's output contains medical advice keywords.",
                    confidence=0.9,
                    fallback_response=self.fallback_templates["medical"]
                )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Model output is appropriate",
            confidence=1.0,
        )
    
    def _check_context_patterns(self, context: List[Dict]) -> ModerationResult:
        
        # Check for escalation
        crisis_count = 0
        for turn in context:
            if turn.get("role") == "user":
                content = turn.get("content", "").lower()
                for keyword in self.crisis_keywords:
                    if keyword in content:
                        crisis_count += 1
        
        if crisis_count >= 3:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=["pattern_escalation", "repeated_crisis"],
                reason="Escalating crisis pattern detected",
                confidence=0.8,
                fallback_response=self.fallback_templates["crisis"],
            )
        
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Conversation pattern is safe",
            confidence=1.0,
        )
    
    def get_disclaimer(self) -> str:
        """Get initial disclaimer."""
        return self.fallback_templates.get("disclaimer", "")

# Singleton instance
_moderator_instance = None

def get_moderator() -> Moderator:
    """Get singleton moderator instance."""
    global _moderator_instance
    if _moderator_instance is None:
        _moderator_instance = Moderator()
    return _moderator_instance