## News summary for Infosys:
##Infosys is under pressure today following weaker-than-expected quarterly guidance and concerns over demand in the US market. Analysts are revising short-term outlook.

import os
import requests
from llm_config import llm
from dotenv import load_dotenv

load_dotenv()

def get_news_summary(stock: str) -> str:
    api_key = os.getenv("BING_NEWS_API_KEY")
    endpoint = "https://api.bing.microsoft.com/v7.0/news/search"

    params = {
        "q": f"{stock} stock",
        "count": 5,
        "freshness": "Day",
        "mkt": "en-IN"
    }

    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    try:
        res = requests.get(endpoint, headers=headers, params=params)
        data = res.json()

        if "value" not in data or len(data["value"]) == 0:
            return f"⚠️ No recent news found for {stock}."

        headlines = [article["name"] for article in data["value"][:5]]
        headline_text = "\n".join(headlines)

        prompt = f"""Give a short 3–4 line summary of why the stock '{stock}' might be rising or falling today based on the following news headlines:\n\n{headline_text}"""
        result = llm.invoke(prompt)

        return f"📉 News summary for {stock}:\n{result.content.strip()}"

    except Exception as e:
        return f"❌ Error fetching news summary: {str(e)}"


# ✅ Optional: test manually
if __name__ == "__main__":
    stock_name = input("Enter stock name: ")
    print(get_news_summary(stock_name))
