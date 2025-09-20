from src.chat_engine import get_engine
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
import sys
import os

# Add parent directory to path for src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__, template_folder='templates') # Specify templates folder

# Global chat engine instance
chat_engine = None

# Path for storing profiles
PROFILE_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'profiles.json')

def load_user_profiles():
    """Loads all user profiles from profiles.json."""
    if not os.path.exists(PROFILE_DATA_PATH):
        return {}
    with open(PROFILE_DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_user_profile(user_id, profile_data):
    """Saves a single user profile to profiles.json."""
    profiles = load_user_profiles()
    profiles[user_id] = profile_data
    os.makedirs(os.path.dirname(PROFILE_DATA_PATH), exist_ok=True)
    with open(PROFILE_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=4, ensure_ascii=False)


@app.before_request
def ensure_chat_engine():
    """Initializes chat_engine if it hasn't been already."""
    global chat_engine
    if chat_engine is None:
        chat_engine = get_engine()
        user_profiles = load_user_profiles()
        if 'default_user' in user_profiles: # Check for a default profile
            chat_engine.set_user_profile(user_profiles['default_user'])
            print("Loaded default user profile into chat engine.")
        else:
            print("No default user profile found. Chat engine running without profile data.")


@app.route("/")
def index():
    """Determines whether to show the quiz or the chat."""
    # For a simple demo, check if a 'default_user' profile exists
    profiles = load_user_profiles()
    if 'default_user' in profiles:
        return redirect(url_for('chat_interface'))
    else:
        return redirect(url_for('profile_quiz'))

@app.route("/profile_quiz")
def profile_quiz():
    """Serves the profiling quiz HTML page."""
    return render_template('profile_quiz.html')

@app.route("/submit_profile", methods=["POST"])
def submit_profile():
    """Receives and saves the user's profile data."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid profile data."}), 400

        # For this demo, we'll save it as a 'default_user'
        user_id = 'default_user'
        save_user_profile(user_id, data)

        # Update the chat engine with the new profile immediately
        global chat_engine
        if chat_engine:
            chat_engine.set_user_profile(data)
        else:
            # If chat_engine wasn't initialized yet (unlikely with @before_request but good for robustness)
            chat_engine = get_engine()
            chat_engine.set_user_profile(data)


        print(f"Profile saved for {user_id}: {data}")
        return jsonify({"message": "Profile saved successfully!"}), 200
    except Exception as e:
        print(f"Error submitting profile: {e}")
        return jsonify({"message": "Error saving profile."}), 500

@app.route("/chat_interface")
def chat_interface():
    """Serves the main chat interface HTML page."""
    return render_template('chat.html')


@app.route("/disclaimer")
def disclaimer():
    try:
        # Assuming chat_engine has a moderator with get_disclaimer()
        # For this example, we'll just return a static disclaimer
        text = "This chatbot is for educational purposes only and may not always provide perfectly accurate or complete information. Always verify critical language or cultural details with reliable sources."
        return jsonify({"disclaimer": text})
    except Exception as e:
        print(f"Error getting disclaimer: {e}")
        return jsonify({"disclaimer": "Error fetching disclaimer."}), 500


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"response": "Invalid request.", "safety_action": "allow"}), 400
        user_prompt = data.get("prompt", "").strip()
        if not user_prompt:
            return jsonify({"response": "Please enter a message.", "safety_action": "allow"}), 400

        global chat_engine
        if chat_engine is None:
            # Re-initialize if for some reason it's gone (shouldn't happen with @before_request)
            chat_engine = get_engine()

        response_data = chat_engine.process_message(user_prompt)
        return jsonify(response_data)
    except Exception as e:
        print(f"Error processing chat: {e}")
        return jsonify({"response": [{"chinese": "抱歉，服务器发生错误。", "pinyin": "Bàoqiàn, fúwùqì fāshēng cuòwù.", "english": "Sorry, a server error occurred."}], "safety_action": "block"}), 500


if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5001)