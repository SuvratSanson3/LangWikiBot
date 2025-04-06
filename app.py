import streamlit as st
from main import chat_with_bot

# Page configuration
st.set_page_config(page_title="LangGraph AI Chatbot", page_icon="🤖", layout="centered")

# Title and description
st.title("🤖 LangGraph AI Chatbot")
st.markdown("""
Welcome to the LangGraph-powered AI assistant!  
Ask me anything related to research, Wikipedia, or general topics — I'm here to help!  
""")

# Session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_query = st.text_input("💬 Type your question here...", placeholder="e.g., What is LangGraph?")
    submitted = st.form_submit_button("Send")

    if submitted and user_query:
        with st.spinner("Thinking..."):
            try:
                response = chat_with_bot(user_query)
            except Exception as e:
                response = f"❌ Error: {str(e)}"
        st.session_state.history.append((user_query, response))

# Chat history display
if st.session_state.history:
    for user_msg, bot_msg in reversed(st.session_state.history):
        with st.chat_message("user"):
            st.markdown(f"**You:** {user_msg}")
        with st.chat_message("assistant"):
            st.markdown(f"**Bot:** {bot_msg}")
else:
    st.markdown("🧠 Ask your first question to get started!")

# Optional: Add footer or credits
st.markdown("---")
st.caption("🚀 Built using [LangGraph](https://python.langgraph.dev/), LLMs, and Streamlit")
