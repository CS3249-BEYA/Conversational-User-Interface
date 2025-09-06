# Safety and Moderation Policy

## Overview

This document defines the safety boundaries and moderation policies for the psychological pre-consultation CUI system. The system prioritizes user safety while providing supportive dialogue within appropriate boundaries.

## Policy Framework

### 1. Safety Categories

#### 1.1 Crisis Situations

**Definition**: Immediate risk of harm to self or others

**Implementation Requirements**: 
- Add more crisis keywords
- Create more regex patterns for complex expressions
- Use highest sensitivity in all safety modes

```python
# Student Implementation Required:
# Minimum 20 keywords covering various crisis expressions
CRISIS_KEYWORDS = [
    # Direct suicide mentions:
    "suicide", "end my life", "kill myself", "take my life", "can't go on", "better off dead", "ready to die",
    # Self-harm expressions:
    "hurt myself", "self-harm", "cut myself", "injure myself", "harming myself", "punish myself",
    # Imminent danger indicators:
    "goodbye forever", "final message", "last time", "won't be here", "leaving soon", "over it all",
    # Emotional crisis expressions:
    "hopeless", "worthless", "can't take it", "don't see the point", "at my wit's end", "giving up"
]


# Minimum 8 regex patterns for complex expressions
CRISIS_PATTERNS = [
    r"\b(want|going|plan|ready) to (die|kill|hurt|end)\b",
    r"\b(thinking|thought) about (suicide|dying|ending it)\b",
    r"\b(no|don't have) a (reason|point) to (live|go on|continue)\b",
    r"\b(tonight|tomorrow|this weekend) (i will|i'm going to)\b",
    r"\b(wish|wishing) i was (dead|gone)\b",
    r"\b(can't take|can't stand) this (anymore|any longer)\b",
    r"\b(what's|what is) the point of living\b",
    r"\b(going to|gonna) (hurt myself|self-harm|end it)\b"
]
```

**Action**: `BLOCK` + Crisis referral

**Example Response Template (Complete this with 150-200 words)**: 

```text
I'm deeply concerned about what you're sharing. Your safety is my top priority, and I want you to know that help is available right now.

Please reach out to trained crisis counselors immediately:  
- Singapore Association for Mental Health (SAMH) 24-hour helpline: 1800 283 7019  
- Samaritans of Singapore (SOS) Crisis Helpline: 1800 221 4444  
- Institute of Mental Health (IMH) Hotline: 6389 2222  

It sounds like you are going through an extremely difficult time, and feeling overwhelmed is understandable. You are not alone in this, and reaching out to trained professionals can help you navigate these intense emotions safely. Even if it feels hard to take the first step, talking to someone who is trained to listen and provide support can make a real difference.  

Remember, seeking help is a sign of strength, and connecting with professional support can help you find safety and stability. Please consider contacting one of the hotlines above immediately. Your life matters, and support is just a call or text away.

```

#### 1.2 Medical Requests

**Definition**: Requests for diagnosis, treatment, or medication advice

**Implementation Requirements**:
- Define more medical keywords
- Create more regex patterns
- Use SAFE_FALLBACK action

```python
# Student Implementation Required:
# Minimum 20 keywords
MEDICAL_INDICATORS = [
    # Diagnosis requests:
    "diagnose", "what condition", "do I have", "am I sick", "is this a disorder", "what's wrong with me",
    # Medication/treatment:
    "medication", "what pills", "drugs for", "cure for", "what treatment", "prescribe me", "side effects", "what should I take",
    # Mental health specific:
    "am i depressed", "bipolar", "schizophrenic", "anorexia", "adhd", "ocd", "anxiety disorder", "what's my diagnosis",
    # Other:
    "psychiatrist recommendation", "doctor's advice", "medical advice"
]

# Minimum 8 regex patterns for complex expressions
MEDICAL_PATTERNS = [
    r"\b(prescribe|recommend|suggest) (medication|pills|drugs)\b",
    r"\bwhat (medication|medicine|pills) should i take\b",
    r"\bdo i have (depression|anxiety|bipolar|ocd)\b",
    r"\bcan you diagnose me\b",
    r"\bwhat is the best treatment for\b",
    r"\bshould i take (a drug|a pill) for\b",
    r"\bwhat are the side effects of\b",
    r"\bwhere can i find a psychiatrist\b"
]

```

**Action**: `SAFE_FALLBACK`

**Response Template (Complete with structured format)**: 

```text
I understand you're looking for medical guidance, and I appreciate you reaching out. However, I'm not qualified to provide medical diagnoses or treatment recommendations.  

I hear that you are concerned about your mental health and may be seeking advice on medication, diagnosis, or treatment options. It's completely valid to have these questions, and acknowledging them is an important step toward support.  

For your health and safety, please consult with:  
- A licensed psychiatrist for medication questions  
- A licensed psychologist or counselor for therapy and mental health evaluation  
- Your primary care doctor for any general medical concerns  

While I cannot provide medical advice, I can offer empathetic listening and help you reflect on your thoughts and emotions. I can also provide information on coping strategies, stress management techniques, and point you toward professional resources that are appropriate for your situation.  

Remember, seeking professional help is a sign of strength. You are taking an important step by reaching out, and support is available to guide you safely through this journey.

```

#### 1.3 Harmful Content

**Definition**: Violence, illegal activities, harassment

**Implementation Requirements**:
- Minimum 20 keywords
- Consider both direct and indirect expressions

```python
# Student Implementation Required:
HARMFUL_CATEGORIES = {
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

```

**Action**: `BLOCK`

**Example Response Template (Complete this with 150-200 words)**: 

```text
I cannot and will not provide assistance with that request as it could potentially cause harm. My purpose is to provide a safe and supportive conversation, and I cannot engage in or support discussions of violence, illegal activities, or harassment. This is a strict boundary of our conversation. If you are experiencing distress, I am here to listen, but we must keep our conversation within a safe and constructive space. I encourage you to redirect our conversation to a topic that aligns with my purpose of offering emotional support.
```

#### 1.4 Supportive Dialogue

**Definition**: General emotional support, stress discussion, life challenges

**Acceptable Topics** (define at least 10):
```python
SUPPORTIVE_TOPICS = [
    "stress management",
    "relationship challenges",
    "work-life balance",
    "anxiety coping",
    "grief and loss",
    "self-esteem issues",
    "social difficulties",
    "academic pressure",
    "career uncertainty",
    "coping with change"
]
```

**Action**: `ALLOW`

### 2. Action Definitions

- **ALLOW**: Proceed with normal dialogue
- **BLOCK**: Refuse interaction with safety message and resources
- **SAFE_FALLBACK**: Redirect to appropriate resources while maintaining support

### 3. Confidence and Ambiguity

**Confidence Score Guidelines**:
- Keyword match: 0.7 confidence
- Pattern match: 0.8-0.9 confidence
- Multiple matches: Use maximum confidence

**Implementation Requirements**:
- Complete confidence thresholds by safety mode

**Confidence Thresholds by Safety Mode**:

```python
CONFIDENCE_THRESHOLDS = {
    "strict": {
        # Maximum sensitivity - err on side of caution
        "crisis": 0.3,   # Very low threshold for crisis detection
        "medical": 0.4,  # Low threshold for medical boundaries
        "harmful": 0.5   # Moderate threshold for harmful content
    },
    "balanced": {
        # Balanced approach for production use
        "crisis": 0.6,
        "medical": 0.7,
        "harmful": 0.8
    },
    "permissive": {
        # Minimum filtering - only clear violations
        "crisis": 0.9,
        "medical": 0.95,
        "harmful": 0.95
    }
}
```

### 5. Response Templates

**Implementation Requirements**:
- Copy the complete crisis template from your completed 1.1 Crisis Situations above.
- Copy the complete medical template from your completed 1.2 Medical Requests above.
- Copy the complete harmful template from your completed 1.3 Harmful Content above.
- Complete disclaimer template.

```python
RESPONSE_TEMPLATES = {
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
    """
}
```
