# Chinese Language Learning Chatbot - Installation Guide

This guide explains how to install and run the Chinese Language Learning Chatbot locally using Python and Ollama with the **Phi-3 Medium** model.

---

## Prerequisites

- Python 3.11+
- 8GB RAM (minimum)
- 10GB free disk space
- Internet connection for initial setup
- macOS or Windows

---

## macOS Installation

### Step 1: Install Python (if needed)

```bash
# Check Python version
python3 --version

# If Python 3.11+ not installed, use Homebrew:
brew install python@3.11
````

---

### Step 2: Install Ollama

```bash
# Install via Homebrew
brew install ollama

# Or download from official website:
# https://ollama.com/download/mac
```

Verify installation:

```bash
ollama --version
```

---

### Step 3: Start Ollama Service

```bash
# Start Ollama service (keep this terminal tab open!)
ollama serve
```

> ⚠️ **Important:** Keep this terminal tab open while using the chatbot.
> You will need to open a **new terminal tab/window** for subsequent steps.

---

### Step 4: Pull the Phi-3 Medium Model

In a **new terminal tab/window**, run:

```bash
# Pull Phi-3 Medium (~14B parameters)
ollama pull phi3:medium
```

---

### Step 5: Test the Model

```bash
# In the same new tab
ollama run phi3:medium "Hello, how are you?"

# Exit with /bye
```

---

### Step 6: Set Up Python Virtual Environment

```bash
# In another terminal tab/window
python3 -m venv venv
source venv/bin/activate
```

---

### Step 7: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 8: Start the Chatbot

```bash
python -m app.app
```

Open your browser and navigate to:

```
http://127.0.0.1:5000/
```

> Now you can chat with your Chinese Language Learning Bot!

---

## Windows Installation

### Step 1: Install Python

1. Download Python 3.11+ from [https://python.org](https://python.org)
2. Check **Add Python to PATH** during installation
3. Verify installation:

```powershell
python --version
```

---

### Step 2: Install Ollama

1. Download installer from [https://ollama.com/download/windows](https://ollama.com/download/windows)
2. Run the installer (OllamaSetup.exe)
3. Ollama will start automatically and appear in the system tray

---

### Step 3: Start Ollama Service

Open PowerShell:

```powershell
# Start Ollama service (keep this window open!)
ollama serve
```

> Keep this window open. Open a **new PowerShell tab/window** for pulling models and running Python commands.

---

### Step 4: Pull the Phi-3 Medium Model

In the new terminal tab/window:

```powershell
ollama pull phi3:medium

# Test the model
ollama run phi3:medium "Hello"
# Exit with /bye
```

---

### Step 5: Set Up Python Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Step 6: Start the Chatbot

```powershell
python -m app.app
```

Visit in your browser:

```
http://127.0.0.1:5000/
```

---

## Troubleshooting

### Ollama Connection Errors

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
# macOS:
brew services restart ollama
# Windows:
# Right-click system tray icon → Quit, then restart

# Check port isn't blocked
lsof -i :11434  # macOS
netstat -an | findstr :11434  # Windows
```

### Model Download Issues

```bash
# Remove model and retry
ollama rm phi3:medium
ollama pull phi3:medium

# Use --insecure if there are certificate issues
ollama pull phi3:medium --insecure
```

---

### Notes

* Always keep the **Ollama service tab running** while using the chatbot.
* Use separate terminal tabs for Python environment setup, dependency installation, and running the chatbot.
