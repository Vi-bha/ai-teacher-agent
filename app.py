"""
app.py
Streamlit front-end for the EngiTutor agent.

Run with:
    streamlit run app.py

Requires a free Groq API key from https://console.groq.com/keys
"""

import streamlit as st
from agent import ask_agent, DEFAULT_MODEL
from ppt_generator import build_pptx

st.set_page_config(page_title="EngiTutor - AI Engineering Teacher", page_icon="🎓", layout="centered")

st.title("🎓 EngiTutor — AI Engineering Teacher")
st.caption("A free, local AI agent that explains engineering concepts, builds PPTs, and quizzes you.")

# Sidebar settings
with st.sidebar:
    st.header("Settings")

    # Try to get key from Streamlit secrets first (used when deployed online)
    default_key = st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else ""
    api_key = st.text_input(
        "Groq API Key",
        value=default_key,
        type="password",
        help="Get a free key at https://console.groq.com/keys",
    )
    model_name = st.text_input("Model name", value=DEFAULT_MODEL)
    st.markdown(
        "**Setup checklist:**\n"
        "1. Get a free Groq API key: console.groq.com/keys\n"
        "2. Paste it above (or set it in Streamlit Cloud secrets as `GROQ_API_KEY`)\n"
    )
    if st.button("Clear conversation"):
        st.session_state.chat_history = []
        st.session_state.display_history = []
        st.rerun()

# Session state init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # plain role/content for the LLM
if "display_history" not in st.session_state:
    st.session_state.display_history = []  # for rendering in the UI (includes ppt buffers etc.)

# Render past conversation
for item in st.session_state.display_history:
    with st.chat_message(item["role"]):
        st.markdown(item["text"])
        if item.get("ppt_buffer") is not None:
            st.download_button(
                label="📥 Download PPT",
                data=item["ppt_buffer"],
                file_name=f"{item['topic'].replace(' ', '_')}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key=item["ppt_key"],
            )

# Chat input
user_input = st.chat_input("Ask EngiTutor anything... e.g. 'Explain Bernoulli's principle' or 'Make a PPT on Op-Amps'")

if user_input:
    # Show user message immediately
    st.session_state.display_history.append({"role": "user", "text": user_input, "ppt_buffer": None})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                parsed = ask_agent(user_input, st.session_state.chat_history, api_key=api_key, model=model_name)
            except RuntimeError as e:
                st.error(str(e))
                st.stop()

        # Update raw chat history (for context in future turns)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": parsed.raw})

        ppt_buffer = None
        ppt_key = None

        if parsed.mode == "PPT":
            st.markdown(f"**Topic:** {parsed.topic}")
            st.markdown("Here's your slide outline:")
            st.text(parsed.content)
            ppt_buffer = build_pptx(parsed.topic, parsed.content)
            ppt_key = f"ppt_{len(st.session_state.display_history)}"
            st.download_button(
                label="📥 Download PPT",
                data=ppt_buffer,
                file_name=f"{parsed.topic.replace(' ', '_')}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key=ppt_key,
            )
            display_text = f"**Topic:** {parsed.topic}\n\nHere's your slide outline:\n\n```\n{parsed.content}\n```"
        else:
            st.markdown(f"**Mode:** {parsed.mode} | **Topic:** {parsed.topic}")
            st.markdown(parsed.content)
            display_text = f"**Mode:** {parsed.mode} | **Topic:** {parsed.topic}\n\n{parsed.content}"

        st.session_state.display_history.append({
            "role": "assistant",
            "text": display_text,
            "ppt_buffer": ppt_buffer,
            "topic": parsed.topic,
            "ppt_key": ppt_key,
        })
