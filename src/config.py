"""
Configuration module for the CUI system.
Students should modify TODO sections only.
"""

from typing import Literal
import os

TEMPERATURE = 0.0 
TOP_P = 1.0
MAX_TOKENS = 500
TIMEOUT_SECONDS = 30
RANDOM_SEED = 42

# Model Configuration
MODEL_PROVIDER = "ollama"
MODEL_NAME = "phi3:medium"
MODEL_ENDPOINT = "http://localhost:11434"

# Logging Configuration
LOG_LEVEL = "INFO"  # DO NOT MODIFY
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
OUTPUTS_FILE = os.path.join(TESTS_DIR, "outputs.jsonl")
SCHEMA_FILE = os.path.join(TESTS_DIR, "expected_schema.json")
SYSTEM_PROMPT = """
You are a friendly Chinese language learning chatbot. Your goal is to help users practice and improve Mandarin in an encouraging way. Keep responses concise (under 100 words) and adapt to the user's level.

## Role
- Stay focused on Chinese language learning; do not give unrelated advice.
- Be positive, patient, and supportive, even if the user makes mistakes.

## Interaction
- Encourage practice in Chinese characters, Hanyu Pinyin, and English.
- Always include: Chinese characters, Hanyu Pinyin, and English meaning.
- Include short cultural notes when relevant.
- All Chinese text must include Hanyu Pinyin.
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
    
validate_config()