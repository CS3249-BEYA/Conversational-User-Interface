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
# Start Ollama in background (keep terminal open)
ollama serve

# Verify available models (in a new terminal)
ollama list
```

---

### Step 4: Pull the Phi-3 Medium Model

```bash
# Pull Phi-3 Medium (~14B parameters)
ollama pull phi3:medium
```

---

### Step 5: Test the Model

```bash
# Simple test prompt
ollama run phi3:medium "Hello, how are you?"

# Exit with /bye
```

---

### Step 6: Set Up Python Virtual Environment

```bash
# Create and activate virtual environment
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

---

## Windows Installation

### Step 1: Install Python

1. Download Python 3.11+ from [https://python.org](https://python.org)
2. Check **Add Python to PATH** during installation
3. Verify:

```powershell
python --version
```

---

### Step 2: Install Ollama

1. Download the installer from [https://ollama.com/download/windows](https://ollama.com/download/windows)
2. Run the installer (OllamaSetup.exe)
3. Ollama starts automatically and appears in the system tray

---

### Step 3: Pull the Phi-3 Medium Model

Open PowerShell:

```powershell
ollama pull phi3:medium

# Test the model
ollama run phi3:medium "Hello"
# Exit with /bye
```

---

### Step 4: Set Up Python Environment

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Step 5: Start the Chatbot

```powershell
python -m app.app
```

Visit:

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