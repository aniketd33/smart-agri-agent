import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.chat_agent import get_chat_response

st.set_page_config(page_title="AI Farm Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Farm Assistant")
st.markdown("Ask me anything about farming, crops, diseases, or market prices!")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader("💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)

quick_questions = {
    col1: "Best crops for Black soil in Kharif season?",
    col2: "How to treat tomato late blight?",
    col3: "What is PM-KISAN scheme?",
    col4: "How much water does wheat need?",
}

for col, question in quick_questions.items():
    with col:
        if st.button(question, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner("Thinking..."):
                response, error = get_chat_response(st.session_state.messages)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask your farming question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response, error = get_chat_response(st.session_state.messages)
        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error(f"Error: {error}")

if st.session_state.messages:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()