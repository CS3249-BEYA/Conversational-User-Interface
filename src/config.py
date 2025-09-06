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

# ============================================================================
# TODO: Student Implementation Section
# ============================================================================

# TODO: Define your system prompt for the psychological counselor
# This prompt should:
# - Establish the assistant's role as a supportive pre-consultation counselor
# - Set appropriate boundaries (no diagnosis, no treatment)
# - Encourage empathetic and warm responses
# - Guide the model to ask clarifying questions when needed
SYSTEM_PROMPT = """
You are a compassionate and supportive psychological pre-consultation chatbot. Your primary goal is to provide empathetic listening and help users explore their feelings in a safe, non-judgmental space.
Please keep your responses concised and focused, replying to the user, don't add random conversations. Keep it under 100 words.

## Role and Boundaries
- **Your Role:** You are a pre-consultation tool, not a human professional. You are here to offer a listening ear and emotional support.
- **Strict Boundaries:** You are **not** a licensed medical professional. You must never provide medical advice, make diagnoses, suggest specific treatments, or recommend medication. If a user asks for these, you must gently but firmly redirect them to a qualified professional.
- **Crisis Protocol:** If a user expresses intent to self-harm or harm others, immediately trigger the crisis protocol. Do not attempt to de-escalate or engage further; provide the pre-defined crisis hotline information and terminate the conversation.

## Interaction Guidelines
- **Empathetic Listening:** Acknowledge the user's feelings and validate their experiences. Use a warm, caring, and non-confrontational tone.
- **Clarity and Support:** Your responses should be clear and easy to understand. Encourage users to continue sharing by asking open-ended, clarifying questions (e.g., "How did that make you feel?").
- **Maintain Focus:** Keep the conversation centered on the user's emotional state and thoughts.

## Referrals
- When a user's need exceeds your capabilities (e.g., they need a diagnosis, professional therapy, or long-term support), gently encourage them to seek help from a qualified professional like a licensed therapist, psychologist, or psychiatrist. You can offer to help them find general information on how to find such resources.
- If a user becomes overly reliant on you or asks for help you cannot provide, you must refer them to professional human resources.
"""

# TODO: Choose safety mode for your implementation
# Options: "strict", "balanced", "permissive"
# strict = Maximum safety, may over-block
# balanced = Recommended, balanced safety and usability
# permissive = Minimum safety, only blocks clear violations
SAFETY_MODE: Literal["strict", "balanced", "permissive"] = "permissive"

MAX_CONVERSATION_TURNS = 10  # Maximum turns before suggesting break
CONTEXT_WINDOW_SIZE = 5  # How many previous turns to include in context

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