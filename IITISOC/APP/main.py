from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GROQ_API_KEY = os.getenv("llama3_api_key")
# print("🔑 GROQ_API_KEY =", GROQ_API_KEY)

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

# Memory for simplicity (can be upgraded later)
chat_history = [{"role": "system", "content": PROMPT}]

class Query(BaseModel):
    message: str

@app.post("/chat")
def chat_response(query: Query):
    user_text = query.message.strip().lower()
    chat_history.append({"role": "user", "content": query.message})

    try:
        # Match static rules
        if user_text in ["hello", "hi", "hey", "hii", "helo"]:
            reply = "👋 Hello! I am Stock Screener Assistant. How can I help you today?"

        elif any(phrase in user_text for phrase in [
            "what can you do", "how can you help", "what you can do",
            "what do you do", "your features", "your capabilities"
        ]):
            reply = (
                "💼 I'm glad you asked! Here's what I can help you with:\n"
                "• 📈 Find trending stocks using technical indicators\n"
                "• 📊 Explain financial terms and ratios\n"
                "• 💡 Guide you in using stock screeners effectively"
            )

        elif any(phrase in user_text for phrase in [
            "which stock", "which company", "should i buy", "most profitable"
        ]):
            reply = (
                "🔒 That’s a premium feature. Please sign up to access real-time stock picks. "
                "But feel free to ask any technical questions!"
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
                    "messages": chat_history,
                    "temperature": 0.7
                }
            )
            # print("✅ Groq raw response:", response.text)  # Log whole response for debug
            # response.raise_for_status()  # Raise error if not 2xx
            reply = response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ Error in Groq API call:", e)
        reply = "❌ Sorry, I'm having trouble processing that."

    chat_history.append({"role": "assistant", "content": reply})
    return {"reply": reply}
