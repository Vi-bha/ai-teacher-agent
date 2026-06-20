"""
agent.py
Core agent logic: sends messages to a local Ollama model and parses
the structured MODE/TOPIC/CONTENT response format defined in prompts.py
"""

import re
import requests
from prompts import SYSTEM_PROMPT

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3.1"  # change to "qwen2.5" if you pulled that instead


class ParsedResponse:
    """Holds the parsed agent output in a clean structure."""

    def __init__(self, mode: str, topic: str, content: str, raw: str):
        self.mode = mode
        self.topic = topic
        self.content = content
        self.raw = raw


def call_ollama(messages: list, model: str = DEFAULT_MODEL) -> str:
    """
    Sends the conversation to the local Ollama server and returns the
    raw text reply.

    messages: list of {"role": "user"/"assistant"/"system", "content": str}
    """
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is installed and "
            "running (it should start automatically after installation, or "
            "run 'ollama serve' in a terminal)."
        )
    except Exception as e:
        raise RuntimeError(f"Error talking to Ollama: {e}")


def parse_response(raw_text: str) -> ParsedResponse:
    """
    Parses the model's raw text into MODE / TOPIC / CONTENT.
    Falls back gracefully if the model didn't follow the format exactly.
    """
    mode_match = re.search(r"MODE:\s*(\w+)", raw_text)
    topic_match = re.search(r"TOPIC:\s*(.+)", raw_text)
    content_match = re.search(r"CONTENT:\s*(.*?)(?:\n---|\Z)", raw_text, re.DOTALL)

    mode = mode_match.group(1).strip().upper() if mode_match else "ANSWER"
    topic = topic_match.group(1).strip() if topic_match else "General"
    content = content_match.group(1).strip() if content_match else raw_text.strip()

    return ParsedResponse(mode=mode, topic=topic, content=content, raw=raw_text)


def ask_agent(user_message: str, chat_history: list, model: str = DEFAULT_MODEL) -> ParsedResponse:
    """
    Main entry point: builds the full message list (system prompt + history +
    new message), calls the local LLM, and returns a parsed response.

    chat_history: list of {"role": "user"/"assistant", "content": str}
                  (plain conversation history, without the system prompt)
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    raw_reply = call_ollama(messages, model=model)
    return parse_response(raw_reply)
