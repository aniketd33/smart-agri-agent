import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.language import render_language_sidebar
from modules.chat_agent import get_chat_response

st.set_page_config(page_title="AI Farm Assistant", page_icon="🤖", layout="wide")

T, lang_key = render_language_sidebar()

st.title(T["ai_title"])
st.markdown(T["ai_subtitle"])
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader(T["ai_quick"])
col1, col2, col3, col4 = st.columns(4)

quick_questions = {
    col1: T["ai_q1"],
    col2: T["ai_q2"],
    col3: T["ai_q3"],
    col4: T["ai_q4"],
}

for col, question in quick_questions.items():
    with col:
        if st.button(question, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner(T["ai_thinking"]):
                response, error = get_chat_response(st.session_state.messages)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input(T["ai_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner(T["ai_thinking"]):
            response, error = get_chat_response(st.session_state.messages)
        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error(f"{T['ai_error']}: {error}")

if st.session_state.messages:
    if st.button(T["ai_clear"]):
        st.session_state.messages = []
        st.rerun()