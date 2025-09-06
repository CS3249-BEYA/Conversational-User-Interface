from src.chat_engine import get_engine
import json
from flask import Flask, request, jsonify
import sys
import os

# Add the parent directory to the Python path to import chat_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
chat_engine = get_engine()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Language Learning Assistant</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f9fafb;
            transition: background-color 0.3s ease;
        }
        .chat-container {
            max-width: 800px;
            height: 95vh;
            display: flex;
            flex-direction: column;
            border-radius: 1rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            background-color: #ffffff;
            overflow: hidden;
        }
        .chat-header {
            background-color: #2563eb;
            padding: 1.5rem;
            border-bottom: 1px solid #1e40af;
            text-align: center;
            color: white;
        }
        .chat-messages {
            flex-grow: 1;
            padding: 1.5rem;
            overflow-y: auto;
            scroll-behavior: smooth;
            display: flex;
            flex-direction: column;
        }
        .message-row {
            display: flex;
            margin-bottom: 1rem;
        }
        .user-row {
            justify-content: flex-end;
        }
        .assistant-row {
            justify-content: flex-start;
        }
        .message-box {
            padding: 0.75rem 1.25rem;
            border-radius: 1.5rem;
            max-width: 75%;
            word-wrap: break-word;
            white-space: pre-wrap;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        }
        .user-message {
            background-color: #dbeafe;
            color: #1e40af;
            border-bottom-right-radius: 0.5rem;
        }
        .assistant-message {
            background-color: #f1f5f9;
            color: #334155;
            border-bottom-left-radius: 0.5rem;
        }
        .disclaimer-message, .blocked-message, .safe-fallback-message {
            margin: 1rem auto;
            max-width: 90%;
            text-align: center;
            border-radius: 0.75rem;
            padding: 1rem;
            border: 1px solid;
            box-shadow: none;
        }
        .disclaimer-message {
            background-color: #fff3cd;
            color: #664d03;
            border-color: #ffecb5;
        }
        .blocked-message {
            background-color: #fee2e2;
            color: #991b1b;
            border-color: #fecaca;
        }
        .safe-fallback-message {
            background-color: #cffafe;
            color: #155e75;
            border-color: #a5f3fc;
        }
        .input-area {
            padding: 1.5rem;
            background-color: #ffffff;
            border-top: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
        }
        #user-input {
            flex-grow: 1;
            padding: 0.75rem 1.5rem;
            border-radius: 9999px;
            border: 1px solid #cbd5e1;
            font-size: 1rem;
            outline: none;
        }
        #user-input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
        }
        #send-button {
            margin-left: 1rem;
            padding: 0.75rem 1.5rem;
            background-color: #2563eb;
            color: white;
            border-radius: 9999px;
            font-weight: 600;
            cursor: pointer;
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
            width: 10px;
            height: 10px;
            background-color: #94a3b8;
            border-radius: 50%;
            margin: 0 4px;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .loading-dot:nth-child(1) { animation-delay: -0.32s; }
        .loading-dot:nth-child(2) { animation-delay: -0.16s; }
        .loading-dot:nth-child(3) { animation-delay: 0s; }
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1.0); }
        }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="chat-container">
        <div class="chat-header">
            <h1 class="text-2xl font-bold">Language Learning Bot 🌍</h1>
            <p class="text-sm mt-1">Practice, learn, and improve your language skills with AI</p>
        </div>

        <div id="chat-messages" class="chat-messages"></div>

        <div class="input-area">
            <input id="user-input" type="text" placeholder="Ask me to translate, practice conversation, or explain grammar..." autocomplete="off">
            <button id="send-button">Send</button>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chat-messages');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');

        function appendMessage(text, type) {
            const rowDiv = document.createElement('div');
            rowDiv.className = `message-row ${type === 'user-message' ? 'user-row' : 'assistant-row'}`;
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message-box ${type}`;
            messageDiv.innerHTML = `<p>${text}</p>`;

            rowDiv.appendChild(messageDiv);
            chatMessages.appendChild(rowDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
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
                </div>
            `;
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function hideLoading() {
            const loadingIndicator = document.getElementById('loading-indicator');
            if (loadingIndicator) {
                loadingIndicator.remove();
            }
        }

        async function sendMessage() {
            const prompt = userInput.value.trim();
            if (prompt === '') return;

            appendMessage(prompt, 'user-message');
            userInput.value = '';
            showLoading();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: prompt })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                hideLoading();
                
                let messageType = 'assistant-message';
                if (data.safety_action === 'block') {
                    messageType = 'blocked-message';
                } else if (data.safety_action === 'safe_fallback') {
                    messageType = 'safe-fallback-message';
                }
                
                appendMessage(data.response, messageType);

            } catch (error) {
                hideLoading();
                appendMessage("An error occurred. Please try again later.", 'blocked-message');
                console.error("Error:", error);
            }
        }

        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    """Renders the single-page application."""
    return HTML_TEMPLATE


@app.route("/disclaimer")
def disclaimer():
    """Returns the initial disclaimer text."""
    try:
        disclaimer_text = chat_engine.moderator.get_disclaimer()
        return jsonify({"disclaimer": disclaimer_text})
    except Exception as e:
        print(f"Error getting disclaimer: {e}")
        return jsonify({"disclaimer": "An error occurred fetching the disclaimer."}), 500


@app.route("/chat", methods=["POST"])
def chat():
    """Handles the chat message processing."""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"response": "Invalid request. Please provide a prompt.", "safety_action": "allow"}), 400

        user_prompt = data.get("prompt", "")
        if not user_prompt.strip():
            return jsonify({"response": "Please enter a message.", "safety_action": "allow"}), 400

        response_data = chat_engine.process_message(user_prompt)
        return jsonify(response_data)
    except Exception as e:
        print(f"Error processing chat message: {e}")
        return jsonify({"response": "An error occurred. Please try again later.", "safety_action": "block"}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
