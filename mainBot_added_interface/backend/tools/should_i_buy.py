import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Add parent dir

from llm_config import llm
from tools.get_sentiment import get_sentiment
from tools.get_company_profile import get_company_profile
from tools.get_comparison import resolve_company_name, TICKER_MAP

def should_i_buy(stock_name: str) -> str:
    """
    Takes a U.S. stock name and returns a buy/hold/sell recommendation using LLM.
    Skips Indian stocks (.NS) with a warning.
    """
    try:
        resolved = resolve_company_name(stock_name)
        symbol = TICKER_MAP.get(resolved, resolved.upper())

        # ❌ Block Indian stocks
        if symbol.endswith(".NS"):
            return f"❌ Sorry, this tool currently supports only U.S. stocks. '{stock_name}' is an Indian stock."

        # ✅ Proceed for U.S. stocks
        sentiment = get_sentiment(stock_name)
        profile = get_company_profile(stock_name)

        prompt = f"""
        Stock Name: {stock_name}

        📊 Company Profile:
        {profile}

        📰 Market Sentiment (last 24 hours):
        {sentiment}

        Based on the company profile and current market sentiment, should I buy, hold, or avoid this stock?
        Provide a recommendation and 2-3 bullet points as justification.
        Answer in this format:
        Recommendation: <Buy / Hold / Avoid>
        Reasons:
        - Reason 1
        - Reason 2
        """

        response = llm.invoke(prompt)
        return response.content.strip()

    except Exception as e:
        return f"❌ Error while evaluating stock: {e}"

# ✅ CLI usage
if __name__ == "__main__":
    stock_input = input("Enter company name (e.g., Microsoft, Apple): ")
    result = should_i_buy(stock_input)
    print("\n" + result)
