import streamlit as st
from main import chat_with_bot

st.set_page_config(page_title="LangGraph AI Chatbot", page_icon="🤖", layout="centered")

# Session State
if "history" not in st.session_state:
    st.session_state.history = []

# Input Box
user_query = st.text_input("Your question: ", key="input")

if st.button("Ask"):
    if user_query:
        with st.spinner("Thinking..."):
            response = chat_with_bot(user_query)
        st.session_state.history.append((user_query, response))
        st.experimental_rerun()

# Display History
for user_msg, bot_msg in reversed(st.session_state.history):
    with st.chat_message("user"):
        st.write(user_msg)
    with st.chat_message("assistant"):
        st.write(bot_msg)