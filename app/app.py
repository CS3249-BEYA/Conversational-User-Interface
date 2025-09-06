from src.chat_engine import get_engine
import json
from flask import Flask, render_template_string, request, jsonify
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
    <title>Psychological Pre-consultation Chatbot</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }
        .chat-container {
            max-width: 800px;
            height: 85vh;
            display: flex;
            flex-direction: column;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            background-color: #ffffff;
            overflow: hidden;
        }
        .message-box {
            padding: 1rem;
            border-radius: 0.75rem;
            margin-bottom: 0.5rem;
            max-width: 75%;
        }
        .user-message {
            background-color: #d1e7dd; /* Normal user message color */
            align-self: flex-end;
            border-bottom-right-radius: 0;
        }
        .assistant-message {
            background-color: #e2e8f0; /* Normal assistant message color */
            align-self: flex-start;
            border-bottom-left-radius: 0;
        }
        .disclaimer-message {
            background-color: #fff3cd; /* Warning/Disclaimer color */
            color: #664d03;
            border: 1px solid #ffecb5;
            align-self: center;
            max-width: 90%;
            text-align: center;
        }
        .blocked-message {
            background-color: #f8d7da; /* Blocked message color */
            color: #58151c;
            border: 1px solid #f5c2c7;
        }
        .safe-fallback-message {
            background-color: #cff4fc; /* Safe fallback color */
            color: #055160;
            border: 1px solid #b6effb;
        }
        .loading-dots {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            padding: 1rem;
        }
        .loading-dot {
            width: 8px;
            height: 8px;
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
<body class="flex items-center justify-center h-screen p-4">
    <div class="chat-container">
        <!-- Chat Display Area -->
        <div id="chat-messages" class="flex-1 p-4 overflow-y-auto space-y-4">
            <!-- Disclaimer will be inserted here by JavaScript -->
        </div>

        <!-- Input Area -->
        <div class="p-4 bg-gray-50 border-t border-gray-200 flex items-center">
            <input id="user-input" type="text" placeholder="Type your message..."
                    class="flex-1 p-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200">
            <button id="send-button"
                    class="ml-4 p-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors duration-200 shadow-md">
                Send
            </button>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chat-messages');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');

        // Function to create and append a message bubble
        function appendMessage(text, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message-box ${type}`;
            messageDiv.innerHTML = `<p class="whitespace-pre-wrap">${text}</p>`;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to bottom
        }

        // Function to show a loading indicator
        function showLoading() {
            const loadingDiv = document.createElement('div');
            loadingDiv.id = 'loading-indicator';
            loadingDiv.className = 'loading-dots assistant-message';
            loadingDiv.innerHTML = `
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            `;
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Function to remove the loading indicator
        function hideLoading() {
            const loadingIndicator = document.getElementById('loading-indicator');
            if (loadingIndicator) {
                loadingIndicator.remove();
            }
        }

        // Main function to send a message
        async function sendMessage() {
            const prompt = userInput.value.trim();
            if (prompt === '') return;

            // Display user message immediately
            appendMessage(prompt, 'user-message');
            userInput.value = '';

            // Show loading indicator
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

                // Determine message type based on safety_action
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

        // Event listeners for sending message
        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Initial Disclaimer fetch
        async function fetchDisclaimer() {
            try {
                const response = await fetch('/disclaimer');
                if (!response.ok) {
                    throw new Error('Could not fetch disclaimer.');
                }
                const data = await response.json();
                if (data.disclaimer) {
                    appendMessage(data.disclaimer, 'disclaimer-message');
                }
            } catch (error) {
                console.error("Error fetching disclaimer:", error);
            }
        }

        // Fetch disclaimer on page load
        document.addEventListener('DOMContentLoaded', fetchDisclaimer);

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
        # Log the error for debugging
        print(f"Error processing chat message: {e}")
        return jsonify({"response": "An error occurred. Please try again later.", "safety_action": "block"}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
