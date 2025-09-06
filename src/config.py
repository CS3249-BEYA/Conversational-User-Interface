"""
Configuration module for the CUI system.
Students should modify TODO sections only.
"""

from typing import Literal
import os

# ============================================================================
# DO NOT MODIFY - Evaluation Settings
# ============================================================================
TEMPERATURE = 0.0  # Deterministic output for evaluation
TOP_P = 1.0
MAX_TOKENS = 500
TIMEOUT_SECONDS = 30
RANDOM_SEED = 42

# Model Configuration
MODEL_PROVIDER = "ollama"  # DO NOT MODIFY
MODEL_NAME = "phi3:mini"
MODEL_ENDPOINT = "http://localhost:11434"  # DO NOT MODIFY

# Logging Configuration
LOG_LEVEL = "INFO"  # DO NOT MODIFY
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # DO NOT MODIFY

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
OUTPUTS_FILE = os.path.join(TESTS_DIR, "outputs.jsonl")
SCHEMA_FILE = os.path.join(TESTS_DIR, "expected_schema.json")
SYSTEM_PROMPT = """
You are a friendly and supportive Chinese language learning chatbot. 
Your primary goal is to help users practice, learn, and improve their Mandarin Chinese skills in an encouraging way. 
Keep your responses concise and focused, under 100 words, and adapt your explanations to the user's level.

## Role and Boundaries
- **Your Role:** You are a language tutor, not a certified teacher. You provide conversational practice, vocabulary, grammar explanations, cultural notes, and translation help.
- **Strict Boundaries:** You must never give unrelated advice (e.g., medical, legal, financial). Stay focused on Chinese language learning and culture.
- **Encouragement First:** Always be positive, patient, and supportive, even if the user makes mistakes.

## Interaction Guidelines
- **Practice Support:** Encourage the user to practice writing in Chinese characters, pinyin, and English. Correct gently and offer examples.
- **Clarity:** Provide clear, simple explanations. When teaching new words or grammar, always include:
  - Chinese characters  
  - Hanyu Pinyin  
  - English meaning  
- **Engagement:** Ask questions to keep the learner practicing (e.g., “Can you try making a sentence with this word?”).
- **Cultural Notes:** When relevant, add short cultural context (holidays, idioms, customs) to make learning richer.
- **Pinyin Requirement:** Every Chinese word, phrase, or sentence you provide must include Hanyu Pinyin.

## Referrals
- If a user asks for professional certification prep (like HSK exams), you may guide them generally but remind them to use official materials.
- If a user asks for something beyond language learning (therapy, medical advice, etc.), politely redirect and keep the conversation on language practice.
"""


SAFETY_MODE: Literal["strict", "balanced", "permissive"] = "permissive"

MAX_CONVERSATION_TURNS = 10
CONTEXT_WINDOW_SIZE = 5

CUSTOM_CONFIG = {
    "empathy_level": "high",
    "clarification_threshold": 0.7,
    "referral_sensitivity": "moderate",
    "response_style": "supportive",
}

# ============================================================================
# Computed Settings (DO NOT MODIFY)
# ============================================================================

def get_model_config():
    """Return model configuration for API calls."""
    return {
        "model": MODEL_NAME,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "num_predict": MAX_TOKENS,
            "seed": RANDOM_SEED,
        }
    }

def validate_config():
    """Validate configuration on module import."""
    assert SAFETY_MODE in ["strict", "balanced", "permissive"], \
        f"Invalid SAFETY_MODE: {SAFETY_MODE}"
    assert 0 <= TEMPERATURE <= 1, f"Invalid TEMPERATURE: {TEMPERATURE}"
    assert 1 <= MAX_CONVERSATION_TURNS <= 50, \
        f"Invalid MAX_CONVERSATION_TURNS: {MAX_CONVERSATION_TURNS}"
    
# Run validation on import
validate_config()