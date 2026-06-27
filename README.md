# EngiTutor — AI Engineering Teacher Agent

A free AI agent built with Streamlit + Groq (free hosted LLM API) that:
- Explains engineering concepts
- Generates real downloadable PPT files
- Creates quizzes with answers
- Answers student doubts

Runs both locally and **online for free** via Streamlit Community Cloud, since
it uses Groq's hosted API instead of a local model.

## How it works

```
You (browser) → Streamlit app (app.py) → agent.py → Groq API (hosted LLM)
                                              ↓
                                       ppt_generator.py → real .pptx file
```

The system prompt (in `prompts.py`) forces the LLM to always reply in a strict
format:

```
MODE: EXPLAIN | PPT | QUIZ | ANSWER
TOPIC: <topic>
CONTENT:
<actual content>
```

`agent.py` parses this with regex into a clean object. If `MODE` is `PPT`,
`ppt_generator.py` converts the slide text into an actual `.pptx` file you can
download.

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

1. Push this project to a GitHub repo (already done if you're reading this on GitHub).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app**, select this repo, branch `main`, file `app.py`.
4. Before deploying, click **Advanced settings → Secrets** and add:
   ```toml
   GROQ_API_KEY = "your_actual_groq_key_here"
   ```
5. Click **Deploy**. You'll get a public link like:
   `https://your-app-name.streamlit.app`

The app automatically reads `GROQ_API_KEY` from Streamlit secrets when deployed,
so users don't need to paste a key themselves.

## Example things to try
- "Explain the working of a transformer"
- "Make a PPT on Newton's laws of motion"
- "Quiz me on data structures - arrays and linked lists"
- "What is the difference between AC and DC current?"

## Project structure
```
ai-teacher-agent/
├── app.py            # Streamlit UI (run this)
├── agent.py          # Talks to Groq API, parses structured responses
├── ppt_generator.py  # Converts slide text into real .pptx files
├── prompts.py         # System prompt that defines the agent's behavior
├── requirements.txt
├── .gitignore
└── README.md
```

## Notes for your project report
- This demonstrates an **agentic AI** pattern: the agent autonomously decides
  *what kind of help is needed* (explanation vs. PPT vs. quiz) based on the
  user's natural language request, then takes the appropriate *action*
  (generating a file, formatting a quiz, etc.) without the user specifying
  the mode explicitly.
- Using **Groq's free hosted API** keeps the project free, fast, and
  deployable online (unlike a local-only model, this works as a shareable
  web app).
- The strict `MODE/TOPIC/CONTENT` output format is a simple but effective way
  to get reliable structured behavior out of LLMs without needing native
  "function calling" support.

## Possible extensions (good for "future scope" section)
- Track student quiz scores over time and adapt difficulty
- Add voice input/output
- Support diagram generation (e.g., circuit diagrams) using a diagram library
- Multi-subject memory: remember what topics a student has already covered
