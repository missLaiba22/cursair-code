# ⚡ CodeSpark AI

> Your AI pair programmer — generate, optimize, debug, and understand code in seconds.

[![Open the app](https://img.shields.io/badge/Open%20the%20app-7C3AED?style=for-the-badge&logo=streamlit&logoColor=white)](https://cursair-code.streamlit.app)
[![API](https://img.shields.io/badge/API-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://codesparkai.onrender.com)

CodeSpark AI pairs a polished Streamlit interface with a FastAPI + Google Gemini backend to make everyday coding faster and easier.

## ✨ What it can do

- **Generate** code from plain-English prompts
- **Optimize** code for clarity and performance
- **Explain** unfamiliar code in simple language
- **Debug** issues and suggest fixes
- **Create** unit tests for your functions

## 🖥️ Live demo

Try it here: **[cursair-code.streamlit.app](https://cursair-code.streamlit.app)**  
Backend API: **[codesparkai.onrender.com](https://codesparkai.onrender.com)**

## 🚀 Run locally

```bash
pip install -r requirements.txt
pip install -r frontend/requirements.txt
```

Create a `.env` file, then start the app:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

```bash
python main.py
```

Open `http://localhost:8501` in your browser.
