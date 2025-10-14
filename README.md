# Chinese Language Practise Chatbot

A friendly and interactive **Chinese Language Practise Chatbot** that helps users practice Mandarin, improve vocabulary, understand grammar, and explore cultural context.
Each response includes **Chinese characters**, **Hanyu Pinyin**, and **English translations** to enhance comprehension.

---

## 🌟 Features

* 🗣️ Conversational Mandarin practice
* 🀄 Chinese characters + Hanyu Pinyin + English translation
* 📘 Vocabulary, grammar, and sentence correction support
* 💬 Cultural insights (idioms, holidays, customs)
* 🤖 Friendly, encouraging tutor-style responses

---

## 🧠 Technology Stack

* **Python 3.11+**
* **Flask** — web application framework
* **OpenAI API** — language model backend
* **Tailwind CSS** — frontend styling
* **gTTS** — text-to-speech for pronunciation
* **dotenv** — environment variable management

---

## ⚙️ Installation

See the full installation guide in [INSTALL.md](INSTALL.md).
Supports **macOS** and **Windows**.

### Quick Setup

1. **Install Python 3.11+**

2. **Clone the repository**

   ```bash
   git clone https://github.com/CS3249-BEYA/Conversational-User-Interface.git
   cd Conversational-User-Interface
   ```

3. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file** and add your OpenAI API key:

   ```bash
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

6. **Start the chatbot**

   ```bash
   python -m app.app
   ```

7. Open your browser and go to:

   ```
   http://127.0.0.1:5000/
   ```

---

## 💡 Usage

* Type **English** or **Chinese** phrases to start a conversation.
* The chatbot replies with:

  * 🇨🇳 **Chinese characters**
  * 🈶 **Hanyu Pinyin**
  * 🇬🇧 **English meaning**
* Receive helpful **corrections** and **cultural context** to deepen understanding.

---

## 🔐 Environment Variables

The app uses a `.env` file to store configuration:

| Variable         | Description         |
| ---------------- | ------------------- |
| `OPENAI_API_KEY` | Your OpenAI API key |

---

## 🧩 Requirements

Make sure your `requirements.txt` includes:

```txt
requests==2.31.0
pydantic==2.5.0
jsonschema==4.20.0
python-dateutil==2.8.2
typing-extensions==4.9.0
colorama==0.4.6
tqdm==4.66.1
Flask==2.3.2
gTTs==2.5.4
openai==1.51.0
python-dotenv==1.0.1
```

---

## 🧰 Troubleshooting

### Missing API Key

* Ensure your `.env` file exists and contains a valid `OPENAI_API_KEY`
* Make sure your virtual environment is activated before running

### Dependencies Not Found

Reinstall all dependencies:

```bash
pip install -r requirements.txt
```

### Port Already in Use

If Flask fails to start:

```bash
lsof -i :5000    # macOS/Linux
netstat -ano | findstr :5000   # Windows
```

Then stop the process using that port, or change the app’s port in code.
