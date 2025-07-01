import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

# List of stocks (NSE codes)
stock_list = ["RELIANCE", "TCS", "INFY", "ITC", "HDFCBANK", "SBIN", "ADANIENT", "POWERGRID", "NTPC", "BAJFINANCE"]

def scrape_metrics(stock_code):
    url = f"https://www.screener.in/company/{stock_code}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    metrics = {"stock": stock_code}

    try:
        ratios = soup.select("li.flex.flex-space-between")

        for r in ratios:
            k = r.select_one("span").text.strip()
            v = r.select("span")[-1].text.strip()

            if "P/E" in k: metrics["pe"] = v
            if "ROE" in k: metrics["roe"] = v
            if "Dividend" in k: metrics["div_yield"] = v
            if "Market Cap" in k: metrics["market_cap"] = v

        return metrics
    except:
        return None

def get_top_by_metric(query: str) -> str:
    query = query.lower()
    metric_key = None

    # Detect metric
    if "pe" in query or "undervalued" in query:
        metric_key = "pe"
        ascending = True
    elif "roe" in query:
        metric_key = "roe"
        ascending = False
    elif "dividend" in query:
        metric_key = "div_yield"
        ascending = False
    elif "market cap" in query:
        metric_key = "market_cap"
        ascending = False
    else:
        return "❌ Could not detect which metric to sort by (e.g. PE, ROE, Dividend)."

    # Scrape data live
    all_data = []
    for code in stock_list:
        m = scrape_metrics(code)
        if m:
            all_data.append(m)
        time.sleep(1.5)  # respect website rate limits

    if not all_data:
        return "⚠️ Could not fetch any data."

    # Clean + sort
    df = pd.DataFrame(all_data)
    df[metric_key] = df[metric_key].str.replace(",", "").str.replace("%", "").astype(float)
    df = df.sort_values(by=metric_key, ascending=ascending).dropna()

    # Get top 5
    top_n = 5
    result = f"📊 Top {top_n} stocks by {metric_key.upper()}:\n"
    for i, row in df.head(top_n).iterrows():
        result += f"{row['stock']} — {metric_key.upper()}: {round(row[metric_key], 2)}\n"

    return result
