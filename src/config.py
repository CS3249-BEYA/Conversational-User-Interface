from typing import Dict
import os
import json

# -------------------------------
# Model and API configuration
# -------------------------------
MODEL_PROVIDER = "openai"
MODEL_NAME = "gpt-4o-mini"
MODEL_ENDPOINT = "https://api.openai.com/v1"
TEMPERATURE = 0.0
TOP_P = 1.0
MAX_TOKENS = 500
TIMEOUT_SECONDS = 60
RANDOM_SEED = 42

# -------------------------------
# Logging configuration
# -------------------------------
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
OUTPUTS_FILE = os.path.join(TESTS_DIR, "outputs.jsonl")
SCHEMA_FILE = os.path.join(TESTS_DIR, "expected_schema.json")
PROFILE_FILE = os.path.join(BASE_DIR, "app", "data", "profiles.json")

# -------------------------------
# Conversation context
# -------------------------------
CONTEXT_WINDOW_SIZE = 5  # Only last 5 messages remembered

# -------------------------------
# Safety
# -------------------------------
SAFETY_MODE = "permissive"

# -------------------------------
# Custom config for chatbot behavior
# -------------------------------
CUSTOM_CONFIG = {
    "empathy_level": "high",
    "clarification_threshold": 0.7,
    "referral_sensitivity": "moderate",
    "response_style": "supportive",
}

# -------------------------------
# User profile loading
# -------------------------------


def _load_user_profile(file_path: str) -> Dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("default_user", {})
    except (FileNotFoundError, json.JSONDecodeError):
        print(
            f"Warning: Could not load user profile from {file_path}. Using empty profile.")
        return {}


def _format_user_profile_for_prompt(profile_data: Dict) -> str:
    """Formats user profile section for the system prompt."""
    if not profile_data:
        return ""

    profile_str = "\n## Current User Profile\n"
    profile_str += f"- User Name: {profile_data.get('name', 'Unknown')}\n"
    profile_str += f"- Learning Level: **{profile_data.get('level', 'not specified')}**\n"

    goal = profile_data.get("goal", [])
    if isinstance(goal, list):
        goal_str = ", ".join(goal) if goal else "to improve Chinese skills"
    else:
        goal_str = str(goal)
    profile_str += f"- Goal: **{goal_str}**\n"

    profile_str += "\n**Tailor your responses specifically to this user's background and needs.**\n"
    return profile_str


# Load and format profile section at import
user_profile_data = _load_user_profile(PROFILE_FILE)
formatted_profile_section = _format_user_profile_for_prompt(user_profile_data)

# -------------------------------
# System prompt
# -------------------------------
SYSTEM_PROMPT = f"""
You are a friendly and patient Chinese language practice partner (AI). Your goal is to help users improve their Mandarin in a supportive, engaging, and encouraging way. Keep responses concise (under 100 words) and adapt your explanations to the user's skill level.

## User details
{formatted_profile_section}

## Role
- Focus exclusively on Chinese language practice; avoid unrelated advice.
- Be positive, encouraging, and supportive, even when the user makes mistakes.
- Provide gentle corrections and explain grammar, vocabulary, or pronunciation if needed.

## Interaction
- Always encourage practice in Chinese characters, Hanyu Pinyin, and English translation.
- Include optional Singapore cultural references, slang, idioms, or etiquette where relevant.
- Contextually adapt examples and sentences for everyday life or common scenarios.

## Reply Format
For every response, provide each sentence or phrase in this structure:
- Whether the user responded to the situation/scenario correctly (text and visual cues)
- Chinese: [Characters]
- Pinyin: [Hanyu Pinyin]
- English: [Translation]

- Keep responses clear, concise, and easy to follow.
- Do not bold text or add unnecessary formatting.
- Always remain friendly and encouraging.
"""


# -------------------------------
# Utility functions
# -------------------------------


def get_model_config() -> Dict:
    return {
        "model": MODEL_NAME,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "seed": RANDOM_SEED,
    }


def validate_config():
    assert 0 <= TEMPERATURE <= 1, f"Invalid TEMPERATURE: {TEMPERATURE}"


validate_config()
