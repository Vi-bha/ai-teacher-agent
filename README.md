# EngiTutor — AI Engineering Teacher Agent

A free, local AI agent built with Streamlit + Ollama (open-source LLM) that:
- Explains engineering concepts
- Generates real downloadable PPT files
- Creates quizzes with answers
- Answers student doubts

100% free — no API keys, no internet required once set up (runs fully on your machine).

## How it works

```
You (browser) → Streamlit app (app.py) → agent.py → Ollama (local LLM)
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

## Setup

### 1. Install Ollama
Download from https://ollama.com/download and install it (Windows/Mac/Linux all supported).

### 2. Pull a model
Open a terminal and run:
```bash
ollama pull llama3.1
```
(Smaller/faster alternative: `ollama pull qwen2.5:7b` — if you do this, change
`DEFAULT_MODEL` in `agent.py` or just type the model name in the app sidebar.)

Ollama runs a local server automatically at `http://localhost:11434`.

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```
This opens the app in your browser at `http://localhost:8501`.

## Example things to try
- "Explain the working of a transformer"
- "Make a PPT on Newton's laws of motion"
- "Quiz me on data structures - arrays and linked lists"
- "What is the difference between AC and DC current?"

## Project structure
```
ai-teacher-agent/
├── app.py            # Streamlit UI (run this)
├── agent.py          # Talks to Ollama, parses structured responses
├── ppt_generator.py  # Converts slide text into real .pptx files
├── prompts.py         # System prompt that defines the agent's behavior
├── requirements.txt
└── README.md
```

## Notes for your project report
- This demonstrates an **agentic AI** pattern: the agent autonomously decides
  *what kind of help is needed* (explanation vs. PPT vs. quiz) based on the
  user's natural language request, then takes the appropriate *action*
  (generating a file, formatting a quiz, etc.) without the user specifying
  the mode explicitly.
- Using a **local LLM via Ollama** keeps the project free and runnable offline,
  which is ideal for a student project (no API costs, no rate limits).
- The strict `MODE/TOPIC/CONTENT` output format is a simple but effective way
  to get reliable structured behavior out of smaller open-source models that
  don't support native "function calling" like larger commercial APIs do.

## Possible extensions (good for "future scope" section)
- Track student quiz scores over time and adapt difficulty
- Add voice input/output
- Support diagram generation (e.g., circuit diagrams) using a diagram library
- Multi-subject memory: remember what topics a student has already covered
