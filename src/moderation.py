"""
Content moderation module for safety enforcement.
Students must complete TODO sections according to POLICY.md.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

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
    # Response to use if action != ALLOW
    fallback_response: Optional[str] = None


class Moderator:
    """Handles content moderation according to safety policy."""

    def __init__(self):
        """Initialize the moderator with safety rules."""
        self.safety_mode = SAFETY_MODE
        self._initialize_rules()

    def _initialize_rules(self):
        """Initialize moderation rules based on POLICY.md."""

        # Define racial bias / racism detection keywords
        self.racial_bias_keywords = [
            "chink", "ah tiong", "bangla", "keling", "malay pig", "go back china",
            "dirty indian", "smelly foreigner", "yellow monkey", "blackie",
            "inferior race", "your race is", "better race than",
            "hate chinese", "hate malay", "hate indian"
        ]

        # Racial bias regex patterns
        self.racial_bias_patterns = [
            r"\b(chinese|malay|indian|foreigner|expat)\s+(are|is)\s+(lazy|dirty|stupid|smelly|inferior)\b",
            r"\b(go back to|send them back to)\s+(china|india|bangladesh|malaysia)\b",
            r"\b(i hate|we hate)\s+(chinese|malays|indians|foreigners)\b",
            r"\b(too many|flooded with)\s+(foreigners|prc|workers)\b"
        ]

        # Define general bias keywords (other than racial)
        self.bias_keywords = [
            "women are weak", "men are better", "useless women", "toxic men",
            "old people are useless", "youngsters are stupid",
            "muslims are", "christians are", "hindus are", "buddhists are",
            "filipinos are lazy", "thais are stupid", "japanese are weird"
        ]

        # Bias regex patterns
        self.bias_patterns = [
            r"\b(all|most)\s+(women|men)\s+(are|are so)\s+(weak|dumb|emotional|useless)\b",
            r"\b(old|young)\s+(people|folks)\s+(are|are so)\s+(stupid|slow|useless)\b",
            r"\b(all|most)\s+(muslims|christians|buddhists|hindus)\s+(are|are so)\b",
            r"\b(i hate|we hate)\s+(women|men|old people|religion)\b"
        ]

        # Confidence thresholds
        self.confidence_thresholds = {
            "strict": {
                "racial_bias": 0.3,
                "bias": 0.4,
            },
            "balanced": {
                "racial_bias": 0.6,
                "bias": 0.7,
            },
            "permissive": {
                "racial_bias": 0.9,
                "bias": 0.95,
            }
        }

        # Fallback response templates
        self.fallback_templates = {
            "racial_bias": """
I need to pause here 🚫. The message contains racially biased or discriminatory language.  
This chatbot is designed to support inclusive and respectful learning of Mandarin, so racism or derogatory terms won’t be part of our conversations.  

👉 Let’s keep the practice positive and constructive.  
Would you like me to suggest respectful vocabulary for describing people of different backgrounds instead?
            """,

            "bias": """
I noticed your message may include biased or discriminatory language about gender, religion, or age.  
This chatbot’s purpose is to **help everyone learn Chinese respectfully**, without reinforcing stereotypes or unfair judgments.  

👉 Let’s shift focus to language practice!  
For example, instead of stereotypes, we can learn neutral and polite phrases for describing people. Want to try?
            """,

            "disclaimer": """Welcome to your Chinese Language Practice Partner! 🌟

NOTE:
- This AI helps you practice and improve Mandarin.  
- It is not a certified teacher.  
- Conversations are for learning purposes only and are not monitored by a human.  
- Do not share personal information.

What I Offer:
- Conversational practice with Chinese characters, Hanyu Pinyin, and English meaning  
- Vocabulary and grammar support  
- Sentence corrections and cultural tips  

Focus on improving your Chinese, what would you like to practice today?""",
        }

    def moderate(
        self,
        user_prompt: str,
        model_response: Optional[str] = None,
        context: Optional[List[Dict]] = None,
    ) -> ModerationResult:
        """Perform moderation on user input and/or model output."""

        # Step 1: Check for racial bias
        racial_bias_check = self._check_racial_bias(user_prompt)
        if racial_bias_check.action != ModerationAction.ALLOW:
            logger.warning(f"Racial bias detected: {racial_bias_check.reason}")
            return racial_bias_check

        # Step 2: Check for general bias
        bias_check = self._check_bias(user_prompt)
        if bias_check.action != ModerationAction.ALLOW:
            logger.warning(f"Bias detected: {bias_check.reason}")
            return bias_check

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

    def _check_racial_bias(self, text: str) -> ModerationResult:
        """Check for racial bias indicators."""
        text_lower = text.lower()
        confidence = 0.0
        detected_tags = []

        # Keywords
        for keyword in self.racial_bias_keywords:
            if keyword in text_lower:
                confidence = max(confidence, 0.7)
                detected_tags.append(f"racial_bias_keyword:{keyword}")

        # Regex patterns
        for pattern in self.racial_bias_patterns:
            if re.search(pattern, text_lower):
                confidence = max(confidence, 0.9)
                detected_tags.append(f"racial_bias_pattern:{pattern}")

        threshold = self.confidence_thresholds[self.safety_mode]["racial_bias"]

        if confidence >= threshold:
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=detected_tags,
                reason="Racial bias indicator detected.",
                confidence=confidence,
                fallback_response=self.fallback_templates["racial_bias"]
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No racial bias detected",
            confidence=confidence,
        )

    def _check_bias(self, text: str) -> ModerationResult:
        """Check for general bias indicators."""
        text_lower = text.lower()
        confidence = 0.0
        detected_tags = []

        # Keywords
        for keyword in self.bias_keywords:
            if keyword in text_lower:
                confidence = max(confidence, 0.7)
                detected_tags.append(f"bias_keyword:{keyword}")

        # Regex patterns
        for pattern in self.bias_patterns:
            if re.search(pattern, text_lower):
                confidence = max(confidence, 0.85)
                detected_tags.append(f"bias_pattern:{pattern}")

        threshold = self.confidence_thresholds[self.safety_mode]["bias"]

        if confidence >= threshold:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=detected_tags,
                reason="Bias detected.",
                confidence=confidence,
                fallback_response=self.fallback_templates["bias"]
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No bias detected",
            confidence=confidence,
        )

    def _check_model_output(self, response: str) -> ModerationResult:
        """Check model output for bias-like statements."""
        response_lower = response.lower()

        # Check for general bias in model's output
        for keyword in self.bias_keywords + self.racial_bias_keywords:
            if keyword in response_lower:
                return ModerationResult(
                    action=ModerationAction.SAFE_FALLBACK,
                    tags=["model_output_bias_violation"],
                    reason="Model's output contains bias keywords.",
                    confidence=0.9,
                    fallback_response=self.fallback_templates["bias"]
                )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Model output is appropriate",
            confidence=1.0,
        )

    def _check_context_patterns(self, context: List[Dict]) -> ModerationResult:
        """Check conversation history for repeated racial bias patterns."""
        racial_bias_count = 0
        for turn in context:
            if turn.get("role") == "user":
                content = turn.get("content", "").lower()
                for keyword in self.racial_bias_keywords:
                    if keyword in content:
                        racial_bias_count += 1

        if racial_bias_count >= 3:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=["pattern_escalation", "repeated_racial_bias"],
                reason="Escalating racial bias pattern detected",
                confidence=0.8,
                fallback_response=self.fallback_templates["racial_bias"],
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
