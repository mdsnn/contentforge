# ✦ ContentForge — Django + Groq AI Content Generator

A fast, beautiful Django app that generates stories, blog posts, poems, tweet threads, and scripts using Groq's ultra-fast LLM inference.

---

## 🚀 Setup (5 minutes)

### 1. Install dependencies
```bash
pip install django groq
```

### 2. Run the server
```bash
python manage.py runserver
```

### 3. Open in browser
```
http://127.0.0.1:8000
```

### 4. Enter your Groq API Key
Get it from: https://console.groq.com/keys

---

## ✨ Features

- **5 content types**: Short Story, Blog Post, Poem, Tweet Thread, Micro Script
- **8 tones**: Inspiring, Humorous, Dark & Gritty, Whimsical, Suspenseful, Romantic, Satirical, Nostalgic
- **3 Groq models**: Llama 3.3 70B, Llama 3.1 8B, Gemma 2 9B
- **Copy & Download** generated content
- **Ctrl+Enter** to generate quickly
- Your API key stays in your browser — never stored on server

---

## 📁 Project Structure

```
groq_content_app/
├── config/
│   ├── settings.py
│   └── urls.py
├── forge/
│   ├── views.py          ← Groq API logic here
│   ├── urls.py
│   └── templates/
│       └── forge/
│           └── index.html
└── manage.py
```

---

## 🛠 Customizing

To add a new content type, add an entry to `CONTENT_TYPES` in `forge/views.py`:

```python
'my_type': {
    'label': 'My Type',
    'emoji': '🔥',
    'system': 'You are a ...',
    'prompt_template': 'Write a ... about: {topic}. Tone: {tone}.',
},
```
