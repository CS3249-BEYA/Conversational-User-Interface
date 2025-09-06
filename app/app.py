from src.chat_engine import get_engine
import json
from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
chat_engine = get_engine()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chinese Language Learning Bot</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #f0f4ff 0%, #e0f7ff 100%);
    margin: 0;
}
.chat-container {
    max-width: 700px;
    margin: 2rem auto;
    display: flex;
    flex-direction: column;
    height: 85vh;
    background-color: #ffffff;
    border-radius: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    overflow: hidden;
}
.chat-header {
    background-color: #2563eb;
    color: white;
    padding: 1.5rem;
    text-align: center;
    font-weight: 600;
}
.chat-messages {
    flex-grow: 1;
    padding: 1rem 1.5rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.message-row {
    display: flex;
    align-items: flex-start;
}
.user-row {
    justify-content: flex-end;
}
.assistant-row {
    justify-content: flex-start;
}
.message-box {
    max-width: 70%;
    padding: 0.75rem 1rem;
    border-radius: 1rem;
    word-wrap: break-word;
    white-space: pre-wrap;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.user-message {
    background-color: #dbeafe;
    color: #1e40af;
    border-bottom-right-radius: 0.3rem;
}
.assistant-message {
    background-color: #f1f5f9;
    color: #334155;
    border-bottom-left-radius: 0.3rem;
}
.avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    flex-shrink: 0;
}
.input-area {
    display: flex;
    padding: 1rem 1.5rem;
    border-top: 1px solid #e2e8f0;
    background-color: #f9fafb;
}
#user-input {
    flex-grow: 1;
    padding: 0.75rem 1rem;
    border-radius: 9999px;
    border: 1px solid #cbd5e1;
    outline: none;
    font-size: 1rem;
}
#user-input:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}
#send-button {
    margin-left: 0.75rem;
    padding: 0.6rem 1.5rem;
    background-color: #2563eb;
    color: white;
    font-weight: 600;
    border-radius: 9999px;
    cursor: pointer;
    transition: all 0.2s ease;
}
#send-button:hover {
    background-color: #1e40af;
}
.loading-dots {
    display: flex;
    align-items: center;
    justify-content: center;
}
.loading-dot {
    width: 8px;
    height: 8px;
    background-color: #94a3b8;
    border-radius: 50%;
    margin: 0 3px;
    animation: bounce 1.2s infinite ease-in-out both;
}
.loading-dot:nth-child(1) { animation-delay: -0.3s; }
.loading-dot:nth-child(2) { animation-delay: -0.15s; }
@keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}
</style>
</head>
<body>
<div class="chat-container">
    <div class="chat-header">
        Chinese Language Learning Bot 🌏
        <p class="text-sm mt-1 font-normal">Practice Mandarin with pinyin, translation, and grammar tips</p>
    </div>
    <div id="chat-messages" class="chat-messages"></div>
    <div class="input-area">
        <input id="user-input" type="text" placeholder="Type a sentence, ask for translation, or grammar tips..." autocomplete="off"/>
        <button id="send-button">Send</button>
    </div>
</div>

<script>
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

function appendMessage(text, type) {
    const row = document.createElement('div');
    row.className = 'message-row ' + (type === 'user-message' ? 'user-row' : 'assistant-row');
    const box = document.createElement('div');
    box.className = 'message-box ' + type;
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.style.backgroundImage = type==='user-message' ? 'url(https://i.imgur.com/8Km9tLL.png)' : 'url(https://i.imgur.com/1X9kzqK.png)';
    avatar.style.backgroundSize = 'cover';
    box.appendChild(avatar);
    const textNode = document.createElement('div');
    textNode.innerHTML = text;
    box.appendChild(textNode);
    row.appendChild(box);
    chatMessages.appendChild(row);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading-indicator';
    loadingDiv.className = 'message-row assistant-row';
    loadingDiv.innerHTML = `
        <div class="message-box assistant-message loading-dots">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>`;
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideLoading() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) loadingIndicator.remove();
}

async function sendMessage() {
    const prompt = userInput.value.trim();
    if(!prompt) return;
    appendMessage(prompt, 'user-message');
    userInput.value = '';
    showLoading();
    try {
        const res = await fetch('/chat', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({prompt}) });
        const data = await res.json();
        hideLoading();
        let type = 'assistant-message';
        if(data.safety_action==='block') type='blocked-message';
        else if(data.safety_action==='safe_fallback') type='safe-fallback-message';
        appendMessage(data.response, type);
    } catch(e) {
        hideLoading();
        appendMessage('An error occurred. Please try again later.', 'blocked-message');
        console.error(e);
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', e => { if(e.key==='Enter') sendMessage(); });
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return HTML_TEMPLATE


@app.route("/disclaimer")
def disclaimer():
    try:
        text = chat_engine.moderator.get_disclaimer()
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
        response_data = chat_engine.process_message(user_prompt)
        return jsonify(response_data)
    except Exception as e:
        print(f"Error processing chat: {e}")
        return jsonify({"response": "Error occurred.", "safety_action": "block"}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
