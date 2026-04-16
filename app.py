from typing import List, Dict

import streamlit as st

from backend.storage import (
    list_chats,
    load_chat,
    create_chat,
    save_chat,
    delete_chat,
)
from backend.ollama_client import generate_stream
from automata.intent_dfa import classify_intent, Intent
from automata.cfg_prompt import build_prompt
from automata.output_filter import check_output_safe
from automata.response_bank import canned_response_for_intent
from automata.math_module import try_solve_math


st.set_page_config(
    page_title="Automata-Guided Local Chatbot",
    page_icon="🤖",
    layout="wide",
)


def init_session_state():
    if "chat_id" not in st.session_state:
        st.session_state.chat_id = None
    if "messages" not in st.session_state:
        st.session_state.messages: List[Dict[str, str]] = []
    if "automata_mode" not in st.session_state:
        st.session_state.automata_mode = True
    if "show_debug" not in st.session_state:
        st.session_state.show_debug = False


def load_chat_into_session(chat_id: str):
    chat = load_chat(chat_id)
    st.session_state.chat_id = chat_id
    st.session_state.messages = chat["messages"]


def start_new_chat():
    chat = create_chat()
    st.session_state.chat_id = chat["id"]
    st.session_state.messages = []


def sidebar():
    st.sidebar.title("Sessions")

    if st.sidebar.button("➕ New chat", use_container_width=True):
        start_new_chat()

    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Existing chats")

    chats = list_chats()
    if not chats:
        st.sidebar.caption("No chats yet.")
    else:
        for chat in chats:
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                if st.button(
                    chat["title"],
                    key=f"load_{chat['id']}",
                    use_container_width=True,
                ):
                    load_chat_into_session(chat["id"])
            with col2:
                if st.button("🗑️", key=f"delete_{chat['id']}"):
                    delete_chat(chat["id"])
                    if st.session_state.chat_id == chat["id"]:
                        st.session_state.chat_id = None
                        st.session_state.messages = []
                    st.experimental_rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Settings")

    st.session_state.automata_mode = st.sidebar.checkbox(
        "Use automata-guided pipeline",
        value=st.session_state.automata_mode,
    )

    st.session_state.show_debug = st.sidebar.checkbox(
        "Show debug info",
        value=st.session_state.show_debug,
    )

    temperature = st.sidebar.slider(
        "Model temperature",
        min_value=0.0,
        max_value=1.5,
        value=0.7,
        step=0.1,
    )

    return temperature


def render_header():
    st.markdown(
        """
        <h3 style="margin-bottom:0;">Automata-Guided Local Chatbot</h1>
        <p style="color:gray; margin-top:0;">
        Runs entirely on your machine using Ollama + Mistral. Input and output are wrapped by DFA & CFG logic.
        </p>
        """, unsafe_allow_html=True,
    )
    if st.session_state.automata_mode:
        st.success("Automata-guided mode is ON (DFA intents + CFG prompts + safety filter).")
    else:
        st.info("Automata-guided mode is OFF (direct LLM chat).")


def render_messages():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def automata_pipeline(user_text: str, temperature: float):
    intent = classify_intent(user_text)
    debug_info = {"intent": intent.value}

    if intent in {Intent.GREETING, Intent.GOODBYE, Intent.THANKS}:
        reply = canned_response_for_intent(intent)
        if st.session_state.show_debug:
            debug_info["source"] = "response_bank"
            with st.expander("Debug (automata)", expanded=False):
                st.json(debug_info)
        yield reply, True
        return

    if intent == Intent.MATH:
        math_result = try_solve_math(user_text)
        if math_result is not None:
            if st.session_state.show_debug:
                debug_info["source"] = "math_module"
                with st.expander("Debug (automata)", expanded=False):
                    st.json(debug_info)
            yield math_result, True
            return

    full_prompt = build_prompt(intent, st.session_state.messages, user_text)
    if st.session_state.show_debug:
        debug_info["source"] = "llm"
        debug_info["prompt"] = full_prompt
        with st.expander("Debug (automata)", expanded=False):
            st.json(debug_info)

    response_chunks = []
    for chunk in generate_stream(full_prompt, temperature=temperature):
        response_chunks.append(chunk)
        yield "".join(response_chunks), False

    full_response = "".join(response_chunks)
    is_safe, reason = check_output_safe(full_response)
    if not is_safe:
        full_response = (
            "⚠️ The generated answer was blocked by the safety filter.\n\n"
            f"Reason: {reason}"
        )
    yield full_response, True


def direct_llm_pipeline(user_text: str, temperature: float):
    history_lines = []
    for msg in st.session_state.messages:
        role = msg["role"].title()
        history_lines.append(f"{role}: {msg['content']}")
    history_block = "\n".join(history_lines)
    base_prompt = (
        "You are a helpful local assistant.\n\n"
        f"{history_block}\n\nUser: {user_text}\nAssistant:"
    )
    response_chunks = []
    for chunk in generate_stream(base_prompt, temperature=temperature):
        response_chunks.append(chunk)
        yield "".join(response_chunks), False
    yield "".join(response_chunks), True


def main():
    init_session_state()
    temperature = sidebar()
    render_header()
    st.markdown("---")

    render_messages()

    if prompt := st.chat_input("Ask something (automata, theory, math, code, etc.)..."):

        # 1) Show the user message bubble immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2) Save user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 3) Generate assistant response (same as before)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            streamed_text = ""
            is_final = False

            if st.session_state.automata_mode:
                pipeline = automata_pipeline(prompt, temperature)
            else:
                pipeline = direct_llm_pipeline(prompt, temperature)

            for partial_text, is_final in pipeline:
                streamed_text = partial_text
                message_placeholder.markdown(
                    streamed_text + ("▌" if not is_final else "")
                )

            message_placeholder.markdown(streamed_text)

        # 4) Save assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": streamed_text})

        if st.session_state.chat_id is None:
            chat = create_chat()
            st.session_state.chat_id = chat["id"]
        save_chat(
            st.session_state.chat_id,
            st.session_state.messages,
        )


if __name__ == "__main__":
    main()