# 🎓 EngiTutor — AI Engineering Teacher Agent

A free AI teaching agent built with **Streamlit + Groq** (free hosted LLM API)
that actually *teaches* — not just answers — engineering students.

**🔗 Live app:** https://engitutor-vibha.streamlit.app/
*(no installation or API key needed — just open the link)*

## What it does

- **Explains concepts like a professor** — every explanation follows a real
  teaching structure: hook/intuition → core concept → worked example → check-in
  question, instead of a flat dictionary-style definition.
- **Proactively suggests what to learn next** — if you confirm you understood
  something, EngiTutor suggests a logical next topic on its own, without being
  asked (agentic behavior).
- **Generates real downloadable PPT files** — ask for a presentation and it
  builds an actual `.pptx` you can download and use.
- **Creates quizzes with answers** on any topic.
- **Adapts to your subject and experience level** — set your subject area
  (Mechanical, CS, Electrical, etc.) and level (beginner/intermediate/advanced)
  in the sidebar; the agent calibrates depth and analogies accordingly.

## How it works

```
You (browser) → Streamlit app (app.py) → agent.py → Groq API (hosted LLM)
                                              ↓
                                       ppt_generator.py → real .pptx file
```

The system prompt (`prompts.py`) instructs the LLM to:
1. Decide autonomously which mode fits the request: `EXPLAIN`, `PPT`, `QUIZ`, or `ANSWER`
2. Follow a strict output format so the response can be reliably parsed:
   ```
   MODE: EXPLAIN | PPT | QUIZ | ANSWER
   TOPIC: <topic>
   CONTENT:
   <actual content, following a teaching structure if EXPLAIN/ANSWER>
   ```
3. Teach using a hook → concept → example → check-in structure (not just define)
4. Proactively suggest a next topic when the student confirms understanding

`agent.py` parses this structured output with regex into a clean object.
If `MODE` is `PPT`, `ppt_generator.py` converts the slide text into a real,
downloadable `.pptx` file using `python-pptx`.

## Setup — Run Locally

### 1. Get a free Groq API key
Go to https://console.groq.com/keys, sign up (free), and create a key.

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```
Paste your Groq API key into the sidebar when the app opens in your browser.

## Setup — Deploy Online for Free (shareable link)

1. Push this project to a GitHub repo.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app**, select this repo, branch `main`, file `app.py`.
4. Click **Advanced settings → Secrets**, and add:
   ```toml
   GROQ_API_KEY = "your_actual_groq_key_here"
   ```
5. Click **Deploy**.

When deployed this way, the API key is loaded securely from Streamlit secrets
and is never shown or exposed to visitors — they just see a confirmation that
the AI engine is connected, and can start using the app immediately.

## Example things to try

- "Explain Bayesian networks" → then reply "yes, makes sense" and watch it
  proactively suggest the next logical topic
- "Make a PPT on transformers"
- "Quiz me on data structures - arrays and linked lists"
- "What is the difference between AC and DC current?"

## Project structure

```
ai-teacher-agent/
├── app.py            # Streamlit UI — student profile, chat, file downloads
├── agent.py          # Talks to Groq API, parses structured responses
├── ppt_generator.py  # Converts slide text into real .pptx files
├── prompts.py        # System prompt: teaching style + agentic behaviors
├── requirements.txt
├── .gitignore
└── README.md
```

## Notes for project report

- **Agentic behavior**: the agent doesn't just respond to instructions — it
  autonomously decides *what kind of help is needed* (explain vs. quiz vs. PPT)
  from natural language, takes the matching action (e.g. generating a real
  file), and proactively initiates the next teaching step (suggesting a
  follow-up topic) without explicit prompting each time.
- **Free, hosted, and shareable**: using Groq's free API instead of a local
  model means this runs as an actual deployed web app anyone can open via a
  link, rather than being limited to one machine.
- **Structured output without function-calling**: the strict
  `MODE/TOPIC/CONTENT` format is a lightweight way to get reliable, parseable
  behavior out of an LLM without needing native tool/function-calling support.
- **Secure key handling**: the API key is stored in Streamlit Cloud secrets
  and never rendered in the UI when present, so the public link is safe to
  share without exposing credentials.

## Future scope

- Persistent memory of student progress across sessions (what's been covered,
  quiz performance) — currently the agent has no memory between visits
- Multi-day study plan agent: give it a learning goal, it plans and teaches
  across multiple sessions automatically
- Adaptive quiz difficulty based on tracked performance over time
- Voice input/output
- Diagram generation (e.g. circuit diagrams) for visual learners
