import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Set up Groq API client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.title("💬 Groq Chatbot with LLaMA 3")

# Store chat messages in session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display chat messages
for msg in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_prompt = st.chat_input("Say something...")

if user_prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Get model response
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=st.session_state.messages,
    )
    reply = response.choices[0].message.content

    # Add bot message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
