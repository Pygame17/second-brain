# 🧠 Second Brain — Personal RAG Knowledge System

A lightweight, command-line **Retrieval-Augmented Generation (RAG)** system that turns a folder of Markdown notes into a queryable personal knowledge base, powered by Google's Gemini API.

Built to capture thoughts in seconds and retrieve them intelligently — without the overhead of heavy frameworks.

---

## 🎯 Problem

Personal notes pile up but become impossible to search meaningfully. Keyword search misses context; full-text dumps into an LLM are expensive and slow. This project solves that with **selective context loading**: only the relevant notes are sent to the model, keeping queries fast and token-efficient.

---

## 🏗️ Architecture

```
┌──────────────┐     writes      ┌─────────────────────┐
│  Capture.py  │ ──────────────▶ │   Markdown Vault     │
│  (CLI input) │                 │  (5 fields / Diario) │
└──────────────┘                 └─────────────────────┘
                                           │ reads + filters
                                           ▼
┌──────────────┐    context      ┌─────────────────────┐
│  Gemini API  │ ◀────────────── │      Brain.py        │
│ (2.5 Flash)  │ ──────────────▶ │  (RAG query engine)  │
└──────────────┘    response     └─────────────────────┘
```

The vault is organized into **5 life domains**, each containing topic notes:

| Folder | Domain |
|--------|--------|
| `01_Cuerpo` | Body & performance |
| `02_Mente` | Mind & growth |
| `03_Carrera` | Career & income |
| `04_Negocios` | Business & projects |
| `05_Relaciones` | Relationships |
| `Diario` | Daily timestamped captures |

---

## ⚙️ Tech Stack

- **Python 3.11+**
- **Google Gemini API** (`gemini-2.5-flash`)
- **python-dotenv** for secure config
- Standard library: `argparse`, `pathlib`, `re`

---

## 🚀 Usage

### Capture a quick note
```bash
python Capture.py "call the physiotherapist" -a salud
```
Appends a timestamped line to today's daily note, creating it if needed.

### Query your knowledge base
```bash
# Ask across the whole vault
python Brain.py "what are my pending tasks?"

# Filter by domain folder
python Brain.py --folder 01_Cuerpo "how is my training going?"

# Filter by tag
python Brain.py --tag urgent "what is urgent this week?"

# Only load notes relevant to the question
python Brain.py --relevant "summarize my finances"

# Interactive mode
python Brain.py
```

---

## 🔑 Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your values:
   ```
   GEMINI_API_KEY=your_key_here
   VAULT_DIR=C:\path\to\your\vault
   ```
3. Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com).

---

## 🧩 Key Engineering Decisions

- **Selective context loading** — filter by folder, tag, or keyword relevance before hitting the API, reducing token cost.
- **Config via environment** — no secrets in code; both scripts read from `.env`.
- **Zero-friction capture** — the cost of writing a thought down must be near zero, or you won't do it.
- **Plain Markdown storage** — human-readable, future-proof, and editable in any tool (Obsidian, VSCode, etc.).

---

## 🛣️ Roadmap

- [ ] Semantic search with embeddings (replace keyword filtering)
- [ ] Migrate to Claude API with model routing (light vs heavy tasks)
- [ ] WhatsApp interface via agent layer
- [ ] Scheduled daily briefings (cron)
- [ ] Vector database for long-term memory

---

## 📄 License

MIT
