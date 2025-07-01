import yfinance as yf
from datetime import datetime, timedelta
import time
import pandas as pd

# List of NSE/US stock tickers you want to track
stock_list = [
    "RELIANCE.NS", "INFY.NS", "TCS.NS", "ITC.NS", "HDFCBANK.NS", "SBIN.NS",
    "ADANIENT.NS", "NTPC.NS", "COALINDIA.NS", "POWERGRID.NS", "AAPL", "MSFT", "GOOGL"
]

def get_top_returners(period: str = "1 month", top_n: int = 5) -> str:
    period = period.lower()
    # Map human periods to days
    period_days = {
        "1 week": 7,
        "1 month": 30,
        "3 months": 90,
        "6 months": 180,
        "1 year": 365
    }

    days = period_days.get(period, 30)
    start_date = datetime.today() - timedelta(days=days)
    end_date = datetime.today()

    result_data = []

    for ticker in stock_list:
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if data.empty:
                continue

            start_price = data["Close"].iloc[0]
            end_price = data["Close"].iloc[-1]
            pct_return = ((end_price - start_price) / start_price) * 100

            result_data.append({
                "ticker": ticker,
                "return": round(pct_return, 2)
            })

            time.sleep(1)  # avoid rate-limiting
        except Exception as e:
            continue

    if not result_data:
        return "⚠️ Could not fetch any return data."

    # Convert to DataFrame and sort
    df = pd.DataFrame(result_data)
    df = df.sort_values(by="return", ascending=False)

    # Prepare output
    response = f"📈 Top {top_n} returners over {period}:\n"
    for i, row in df.head(top_n).iterrows():
        response += f"{row['ticker']} — Return: {row['return']}%\n"

    return response
