# Chinese Language Learning Chatbot

A friendly and interactive **Chinese language learning chatbot** that helps users practice Mandarin, improve vocabulary, understand grammar, and learn cultural context. The bot provides Chinese characters, **Hanyu Pinyin**, and English translations for every response.

---

## Features

- Conversational practice in Mandarin Chinese  
- Chinese characters + Hanyu Pinyin + English meaning  
- Vocabulary and grammar support  
- Sentence correction and suggestions  
- Cultural insights (idioms, holidays, customs)  
- Friendly and encouraging tutor-style responses  

---

## Technology Stack

- **Python 3.11+**  
- **Flask** for web interface  
- **Ollama** local AI models (Phi-3 Medium recommended)  
- **Tailwind CSS** for frontend styling  

---

## Installation

See the detailed instructions in [INSTALL.md](INSTALL.md).  
Supports **macOS** and **Windows**.

Quick steps:

1. Install Python 3.11+  
2. Install Ollama (`brew install ollama` on macOS, download installer on Windows)  
3. Start Ollama service: `ollama serve`  
4. Pull the Phi-3 Medium model: `ollama pull phi3:medium`  
5. Set up Python virtual environment and install dependencies:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
````

6. Start the chatbot: `python -m app.app`
7. Open `http://127.0.0.1:5000/` in your browser

---

## Usage

* Type in English or Chinese phrases to practice conversation
* The chatbot will respond with:

  * Chinese characters
  * Hanyu Pinyin
  * English meaning
* Receive gentle corrections and suggestions for improving sentences

---

## Recommended Model

* **Phi-3 Medium** (`ollama pull phi3:medium`)
* Balance of performance and system resource usage (14B parameters)

---

## Troubleshooting

* Ensure Ollama service is running (`ollama serve`)
* Verify model is installed (`ollama list`)
* If connection fails, check port `11434` is free
* Re-pull model if necessary (`ollama rm phi3:medium && ollama pull phi3:medium`)

---

## Contributing

Contributions are welcome! You can help by:

* Improving the frontend UI
* Adding more examples or cultural notes
* Optimizing chatbot prompts for better learning

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, open an issue or contact the maintainer.
