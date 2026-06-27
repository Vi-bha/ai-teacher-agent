"""
agent.py
Core agent logic: sends messages to Groq's free hosted LLM API and parses
the structured MODE/TOPIC/CONTENT response format defined in prompts.py
"""

import re
import requests
from prompts import SYSTEM_PROMPT

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.1-8b-instant"  # fast + free on Groq


class ParsedResponse:
    """Holds the parsed agent output in a clean structure."""

    def __init__(self, mode: str, topic: str, content: str, raw: str):
        self.mode = mode
        self.topic = topic
        self.content = content
        self.raw = raw


def call_groq(messages: list, api_key: str, model: str = DEFAULT_MODEL) -> str:
    """
    Sends the conversation to Groq's hosted API and returns the raw text reply.

    messages: list of {"role": "user"/"assistant"/"system", "content": str}
    api_key: Groq API key (free, from console.groq.com)
    """
    if not api_key:
        raise RuntimeError(
            "No Groq API key found. Add it in Streamlit secrets or paste it "
            "in the sidebar. Get a free key at https://console.groq.com/keys"
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.4,
    }
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Groq API error: {e} - {response.text}")
    except Exception as e:
        raise RuntimeError(f"Error talking to Groq: {e}")


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


def ask_agent(user_message: str, chat_history: list, api_key: str, model: str = DEFAULT_MODEL) -> ParsedResponse:
    """
    Main entry point: builds the full message list (system prompt + history +
    new message), calls the Groq API, and returns a parsed response.

    chat_history: list of {"role": "user"/"assistant", "content": str}
                  (plain conversation history, without the system prompt)
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    raw_reply = call_groq(messages, api_key=api_key, model=model)
    return parse_response(raw_reply)
