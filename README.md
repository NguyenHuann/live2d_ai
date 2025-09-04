# 🎭 Hana • AI Live2D Chat

This project builds a simple **AI VTuber** using **FastAPI + Live2D + Ollama + TTS**, capable of chatting and displaying a virtual character with lip-sync animations.

---

## 🚀 Features
- **FastAPI** backend providing chat API and text-to-speech (TTS).
- Static frontend: **HTML/CSS/JS** + **PixiJS + Live2D** for character rendering.
- Supports **lip-sync** (mouth movement according to audio).
- Runs LLM offline with **Ollama** (e.g., LLaMA 3.1).
- Easy to change Live2D models and voices.

---

## 📦 Installation

### 1. Clone repo
```bash
git clone https://github.com/NguyenHuann/live2d_ai.git
cd live2d_ai
````

### 2. Setup environment and install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # Linux/Mac

pip install -r requirements.txt
```

### 3. Prepare configuration file

Create a `.env` file in the root (containing API keys or configs, if needed). Example:

```env
# LLM via Ollama
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.1:8b-instruct-q4_K_M
LLM_TEMPERATURE=0.6

# gTTS
GTTS_LANG=vi
GTTS_SLOW=false
```

## 📥 Install Ollama

### 1. Download and install Ollama

* Windows / MacOS: download from [Ollama](https://ollama.ai/download)
* Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull a model

Example: Llama 3.1 8B Instruct (quantized Q4\_K\_M)

```bash
ollama pull llama3.1:8b-instruct-q4_K_M
```

### 3. Test model

```bash
ollama run llama3.1:8b-instruct-q4_K_M
```

## 🎨 Add Live2D model

Copy the model into:

```php-template
static/live2d/<ModelName>/
 ├─ <ModelName>.model3.json
 ├─ *.moc3
 ├─ *.physics3.json
 ├─ textures/
 └─ motions/
```

## 📚 Vendor libraries (frontend)

If missing, download vendor libraries:

```powershell
# PixiJS
Invoke-WebRequest https://unpkg.com/pixi.js@7/dist/pixi.min.js -OutFile static/vendor/pixi/pixi.min.js

# Pixi-live2d-display plugin
Invoke-WebRequest https://unpkg.com/pixi-live2d-display/dist/index.min.js -OutFile static/vendor/live2d/index.min.js
Invoke-WebRequest https://unpkg.com/pixi-live2d-display/dist/cubism4.min.js -OutFile static/vendor/live2d/cubism4.min.js

# Runtime Cubism 2 & 4
Invoke-WebRequest https://raw.githubusercontent.com/digitalninja-ro/pixi-live2d-display/master/demo/lib/live2d.min.js -OutFile static/vendor/live2d/live2d.min.js
Invoke-WebRequest https://raw.githubusercontent.com/digitalninja-ro/pixi-live2d-display/master/demo/lib/live2dcubismcore.min.js -OutFile static/vendor/live2d/live2dcubismcore.min.js
```

## ▶️ Run server

```bash
uvicorn main:app --reload --port 8000
```

Open browser at [http://localhost:8000](http://localhost:8000)

## 🗂️ Project structure

```csharp
live2d_ai/
├─ .venv/                # Virtual environment
├─ static/
│  ├─ audio/             # Generated audio files
│  ├─ live2d/            # Live2D models
│  ├─ vendor/            # Downloaded frontend libraries
│  ├─ index.html          # Main interface
│  ├─ styles.css          # CSS
│  ├─ main.js             # Chat handling JS
│  └─ live2d.js           # Live2D + lip-sync initialization JS
├─ main.py                # FastAPI entrypoint
├─ llm.py                 # LLM chat logic (Ollama API)
├─ tts.py                 # TTS
├─ models.py              # Data models
├─ utils.py               # Helpers
├─ requirements.txt
└─ README.md
```

