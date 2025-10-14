# Chinese Language Learning Chatbot - Installation Guide

This guide explains how to install and run the **Chinese Language Learning Chatbot** locally using **Python** and the **OpenAI API**.

---

## 🧩 Prerequisites

* Python **3.11+**
* 8GB RAM (minimum)
* 10GB free disk space
* Internet connection
* macOS or Windows

---

## ⚙️ Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/chinese-chatbot.git
cd chinese-chatbot
```

---

### Step 2: Create a Python Virtual Environment

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure your `requirements.txt` includes the following:

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

### Step 4: Create a `.env` File

In the project root, create a file named `.env`:

```bash
touch .env
```

Add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ Keep this file **private** and **never commit it** to GitHub.

---

### Step 5: Verify the OpenAI Setup

You can test your configuration with a quick script:

```python
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "你好！"}]
)

print(response.choices[0].message.content)
```

If you see a response, everything’s working ✅

---

### Step 6: Start the Chatbot

Run the app:

```bash
python -m app.app
```

Then open your browser to:

```
http://127.0.0.1:5000/
```

You can now chat with your **Chinese Language Learning Bot** powered by OpenAI!

---

## 🧠 Troubleshooting

### 🔹 Missing Packages

If you get `ModuleNotFoundError` for any module, reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

### 🔹 Missing OpenAI Key

Make sure:

* `.env` file exists in your project root
* It contains a valid `OPENAI_API_KEY`
* You’ve activated your virtual environment before running the app

---

### 🔹 Updating Dependencies

To update all installed packages to their latest compatible versions:

```bash
pip install -U -r requirements.txt
```

---

## ✅ Notes

* The chatbot uses **OpenAI GPT models** for generating Chinese learning conversations.
* All secrets (API keys, etc.) should be stored securely in the `.env` file.
* The web interface runs locally on **Flask**.

---

Would you like me to add a short **“Docker setup” section** too (so users can run it with one command, e.g., `docker compose up`)?
