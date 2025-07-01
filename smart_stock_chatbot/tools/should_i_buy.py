'''
“Should I buy Microsoft?”

“Is Reliance a good investment?”

“Is Infosys a buy right now?”

“What should I do about Apple?”
'''

import os
import yfinance as yf
from llm_config import llm
from dotenv import load_dotenv

load_dotenv()

def get_ticker_from_name(name: str) -> str:
    """
    Try to resolve user input to a valid ticker symbol using yfinance.
    """
    # First, try direct (user typed 'MSFT' or 'AAPL')
    try:
        test = yf.Ticker(name)
        if test.info.get("shortName"):
            return name
    except:
        pass

    # Manual mapping fallback for common Indian stocks
    fallback = {
        "Reliance": "RELIANCE.NS",
        "Infosys": "INFY.NS",
        "TCS": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Adani Enterprises": "ADANIENT.NS",
        "Microsoft": "MSFT",
        "Apple": "AAPL",
        "Google": "GOOGL"
    }

    return fallback.get(name.strip().title(), None)

def should_i_buy(stock: str) -> str:
    stock = stock.strip()
    ticker = get_ticker_from_name(stock)

    if not ticker:
        return f"❌ I couldn't find a valid ticker for '{stock}'. Try another company."

    try:
        data = yf.Ticker(ticker)
        info = data.info

        pe_ratio = info.get("trailingPE", "N/A")
        sector = info.get("sector", "N/A")
        price_history = data.history(period="10d")["Close"]

        if len(price_history) < 2:
            return f"⚠️ Not enough price data for {stock}."

        # Determine trend
        if price_history[-1] > price_history[0]:
            trend = "uptrend"
        elif price_history[-1] < price_history[0]:
            trend = "downtrend"
        else:
            trend = "sideways"

        # Build prompt for LLM
        prompt = f"""
You're a financial analyst. A user is asking whether to buy the stock '{stock}' (ticker: {ticker}).
Here is the data:

• Sector: {sector}
• P/E Ratio: {pe_ratio}
• 10-Day Price Trend: {trend}

Give a short 2–3 line investment advice: (Buy / Hold / Avoid) with reasoning.
"""

        result = llm.invoke(prompt)
        return f"📊 Recommendation for {stock}:\n{result.content.strip()}"

    except Exception as e:
        return f"❌ Error fetching data for {stock}: {str(e)}"


# Optional: manual test
if __name__ == "__main__":
    stock_name = input("Enter company name: ")
    print(should_i_buy(stock_name))
