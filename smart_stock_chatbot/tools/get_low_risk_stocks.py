import yfinance as yf
import pandas as pd
import time

# Track Indian + US stocks for demo
STOCK_LIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "ITC.NS", "HDFCBANK.NS",
    "SBIN.NS", "ADANIENT.NS", "NTPC.NS", "COALINDIA.NS", "POWERGRID.NS",
    "AAPL", "MSFT", "GOOGL", "JNJ", "PG"
]

def get_low_risk_stock(top_n: int = 5) -> str:
    result = []

    for ticker in STOCK_LIST:
        try:
            info = yf.Ticker(ticker).info
            beta = info.get("beta", None)
            roe = info.get("returnOnEquity", None)
            eps = info.get("trailingEps", None)
            div = info.get("dividendYield", 0)

            if beta is not None and beta < 1 and eps and eps > 0 and roe and roe > 0.1:
                result.append({
                    "Ticker": ticker,
                    "Beta": round(beta, 2),
                    "ROE": round(roe * 100, 2),
                    "EPS": round(eps, 2),
                    "Div Yield": f"{round(div * 100, 2)}%" if div else "—"
                })
            time.sleep(1)
        except:
            continue

    if not result:
        return "⚠️ Could not find any low-risk stocks based on criteria."

    df = pd.DataFrame(result)
    df = df.sort_values(by="Beta")

    response = "🛡️ **Low-Risk Stocks (Beta < 1, ROE > 10%, EPS > 0):**\n\n"
    for _, row in df.head(top_n).iterrows():
        response += f"🔹 {row['Ticker']} → Beta: {row['Beta']} | ROE: {row['ROE']}% | EPS: {row['EPS']} | Div: {row['Div Yield']}\n"

    return response
