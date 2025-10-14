from typing import Literal
import os
import json

TEMPERATURE = 0.0
TOP_P = 1.0
MAX_TOKENS = 500
TIMEOUT_SECONDS = 60
RANDOM_SEED = 42

MODEL_PROVIDER = "openai"
MODEL_NAME = "gpt-4o-mini"
MODEL_ENDPOINT = "https://api.openai.com/v1"

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
OUTPUTS_FILE = os.path.join(TESTS_DIR, "outputs.jsonl")
SCHEMA_FILE = os.path.join(TESTS_DIR, "expected_schema.json")

PROFILE_FILE = os.path.join(BASE_DIR, "app", "data", "profiles.json")


def _load_user_profile(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("default_user", {})
    except FileNotFoundError:
        print(
            f"Warning: Profile file not found at {file_path}. Using empty profile.")
        return {}
    except json.JSONDecodeError:
        print(
            f"Warning: Error decoding JSON from {file_path}. Using empty profile.")
        return {}


def _format_user_profile_for_prompt(profile_data):
    """Formats the user profile for system prompt."""
    if not profile_data:
        return ""

    profile_str = "\n## Current User Profile\n"
    profile_str += f"- User Name: {profile_data.get('name', 'Unknown')}\n"
    profile_str += f"- Learning Level: **{profile_data.get('level', 'not specified')}**\n"

    # goal can now be a list from multi-select
    goal = profile_data.get('goal', [])
    if isinstance(goal, list):
        goal_str = ", ".join(goal) if goal else "to improve Chinese skills"
    else:
        goal_str = str(goal)
    profile_str += f"- Goal: **{goal_str}**\n"

    profile_str += "\n**Tailor your responses specifically to this user's background and needs.**\n"
    return profile_str


# Load and format the profile data when module imports
user_profile_data = _load_user_profile(PROFILE_FILE)
formatted_profile_section = _format_user_profile_for_prompt(user_profile_data)

SYSTEM_PROMPT = f"""
You are a friendly Chinese language practise chatbot. Your goal is to help users practice and improve Mandarin in an encouraging way. Keep responses concise (under 100 words) and adapt to the user's level.

## User details
{formatted_profile_section}

## Role
- Stay focused on Chinese language practice; do not give unrelated advice.
- Be positive, patient, and supportive, even if the user makes mistakes.

## Interaction
- Encourage practice in Chinese characters, Hanyu Pinyin, and English.
- Implement optional Singapore cultural insights (slang, idioms, etiquette)
- All Chinese text must include Hanyu Pinyin.

## Reply
"For every response, you MUST provide the Simplified Chinese characters, Hanyu Pinyin, and an English translation."
"Use the following format for each sentence or phrase:"
"Chinese: [Characters]\nPinyin: [Pinyin]\nEnglish: [Translation]\n\n"
"Don't bold your replies"
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
    return {
        "model": MODEL_NAME,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "seed": RANDOM_SEED,
    }


def validate_config():
    assert SAFETY_MODE in ["strict", "balanced",
                           "permissive"], f"Invalid SAFETY_MODE: {SAFETY_MODE}"
    assert 0 <= TEMPERATURE <= 1, f"Invalid TEMPERATURE: {TEMPERATURE}"
    assert 1 <= MAX_CONVERSATION_TURNS <= 50, f"Invalid MAX_CONVERSATION_TURNS: {MAX_CONVERSATION_TURNS}"


validate_config()
