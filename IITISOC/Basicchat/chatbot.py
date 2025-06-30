import streamlit as st
import requests
import os
from dotenv import load_dotenv


load_dotenv()
GROQ_API_KEY = os.getenv("llama3_api_key")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

PROMPT = """
You are a friendly onboarding assistant named Stock Screener Assistant.

Your job is:
- Greet users politely when they say "hello"
- Explain your basic features like "finding top trending stocks", "most profitable companies", etc.
- If the user asks for results (like "which company is most profitable?"), respond:
  "That’s a premium feature. Please sign up on our website. But feel free to ask any technical questions!"

Never give real stock data. Stay friendly and act like a first-level chatbot.
"""

st.title("💬 Stock Screener Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": PROMPT}
    ]

user_input = st.chat_input("Ask me anything...")

if user_input:
    user_text = user_input.lower().strip()
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Greeting logic
    if user_text in ["hello", "hi", "hey", "hii", "helo"]:
        reply = "👋 Hello! I am Stock Screener Assistant. How can I help you today?"

    elif any(phrase in user_text for phrase in [
        "what can you do", "how can you help", "what you can do", 
        "what do you do", "your features", "your capabilities", 
        "what are your features", "how you can help"
    ]):
       reply = (
                "💼 I'm glad you asked! Here's what I can help you with:\n\n"
                "• 📈 Find trending stocks using technical indicators\n\n"
                "• 📊 Explain financial terms and ratios\n\n"
                "• 💡 Guide you in using stock screeners effectively\n\n"
                "Let me know what you'd like to explore!"
            )



    elif any(phrase in user_text for phrase in [
        "which stock", "which company", "should i buy", "most profitable", "top stock", "best stock"
    ]):
        reply = (
            "🔒 That’s a premium feature. Please sign up on our website to access real-time stock picks. "
            "But feel free to ask me any technical questions! 🧠"
        )

    else:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": st.session_state.chat_history,
                "temperature": 0.7
            }
        )
        reply = response.json()["choices"][0]["message"]["content"]

    st.session_state.chat_history.append({"role": "assistant", "content": reply})


for msg in st.session_state.chat_history[1:]:  # Skip system prompt
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
