import yfinance as yf
from tabulate import tabulate

# Optional mapping if user enters plain names
TICKER_MAP = {
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC": "HDFCBANK.NS",
    "ICICI": "ICICIBANK.NS",
    "Apple": "AAPL",
    "Microsoft": "MSFT"
}

def get_comparison(stock1: str, stock2: str) -> str:
    stock1 = stock1.strip().title()
    stock2 = stock2.strip().title()

    ticker1 = TICKER_MAP.get(stock1, stock1)
    ticker2 = TICKER_MAP.get(stock2, stock2)

    try:
        data1 = yf.Ticker(ticker1).info
        data2 = yf.Ticker(ticker2).info

        rows = [
            ["Company", stock1, stock2],
            ["Market Cap", f"{data1.get('marketCap', 'N/A'):,}", f"{data2.get('marketCap', 'N/A'):,}"],
            ["P/E Ratio", data1.get("trailingPE", "N/A"), data2.get("trailingPE", "N/A")],
            ["ROE", data1.get("returnOnEquity", "N/A"), data2.get("returnOnEquity", "N/A")],
            ["Profit Margin", data1.get("profitMargins", "N/A"), data2.get("profitMargins", "N/A")],
            ["Revenue (TTM)", f"{data1.get('totalRevenue', 'N/A'):,}", f"{data2.get('totalRevenue', 'N/A'):,}"],
            ["Dividend Yield", data1.get("dividendYield", "N/A"), data2.get("dividendYield", "N/A")],
        ]

        table = tabulate(rows, headers="firstrow", tablefmt="github")
        return f"📊 **Comparison of {stock1} vs {stock2}:**\n\n```\n{table}\n```"

    except Exception as e:
        return f"❌ Error fetching data: {str(e)}"
