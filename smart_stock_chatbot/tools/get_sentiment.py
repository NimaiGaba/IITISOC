##📰 Latest sentiment for Reliance: Mostly positive due to recent project launches and strong earnings.


import requests
from bs4 import BeautifulSoup
from llm_config import llm
import sys
import os

# Add parent path to import llm_config if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def get_sentiment(stock: str) -> str:
    query = f"{stock} stock news site:moneycontrol.com"
    url = f"https://www.google.com/search?q={query}&hl=en"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = []

        for result in soup.select("div.BNeawe.vvjwJb.AP7Wnd")[:5]:
            headline = result.get_text()
            if headline:
                headlines.append(headline)

        if not headlines:
            return f"⚠️ Could not fetch news for {stock}."

        headline_str = "\n".join(headlines)
        prompt = f"Based on the following recent headlines, what is the overall sentiment (positive, neutral, or negative) for {stock}?\n\n{headline_str}"
        sentiment = llm.invoke(prompt)
        return f"📰 Latest sentiment for **{stock}**: {sentiment.content}"

    except Exception as e:
        return f"❌ Error fetching sentiment: {e}"
