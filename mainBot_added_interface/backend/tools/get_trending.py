import yfinance as yf

def get_trending_stocks(_: str = ""):
    symbols = [
        # Banking & Financials
        'HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'AXISBANK.NS', 'KOTAKBANK.NS',
        'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'IDFCFIRSTB.NS', 'PNB.NS', 'BANKBARODA.NS',

        # IT & Technology
        'TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HCLTECH.NS', 'TECHM.NS',
        'LTIM.NS', 'PERSISTENT.NS', 'COFORGE.NS',

        # Energy & Power
        'RELIANCE.NS', 'ONGC.NS', 'NTPC.NS', 'POWERGRID.NS', 'TATAPOWER.NS',
        'ADANIGREEN.NS', 'ADANITRANS.NS', 'IOC.NS', 'BPCL.NS',

        # Auto
        'TATAMOTORS.NS', 'MARUTI.NS', 'EICHERMOT.NS', 'M&M.NS',
        'BAJAJ-AUTO.NS', 'TVSMOTOR.NS', 'ASHOKLEY.NS',

        # Pharma
        'SUNPHARMA.NS', 'DRREDDY.NS', 'CIPLA.NS', 'DIVISLAB.NS',
        'AUROPHARMA.NS', 'LUPIN.NS', 'TORNTPHARM.NS',

        # FMCG
        'HINDUNILVR.NS', 'ITC.NS', 'NESTLEIND.NS', 'BRITANNIA.NS',
        'DABUR.NS', 'MARICO.NS', 'COLPAL.NS',

        # Metals & Mining
        'TATASTEEL.NS', 'JSWSTEEL.NS', 'HINDALCO.NS', 'COALINDIA.NS',
        'NMDC.NS', 'VEDL.NS',

        # Infra, Cement & Construction
        'ULTRACEMCO.NS', 'SHREECEM.NS', 'AMBUJACEM.NS', 'ACC.NS',
        'LT.NS', 'GRASIM.NS',

        # Telecom, Consumer, Services
        'BHARTIARTL.NS', 'IDEA.NS', 'ZOMATO.NS', 'PAYTM.NS',
        'NYKAA.NS', 'DMART.NS', 'IRCTC.NS'
        
         # 🌍 U.S. Global Stocks
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META',
        'TSLA', 'NVDA', 'NFLX', 'ADBE', 'INTC',
        'AMD', 'CRM', 'PYPL', 'UBER', 'SHOP',
        'SNOW', 'PLTR', 'BABA', 'JNJ', 'PFE',
        'DIS'
    ]

    result = []
    for sym in symbols:
        stock = yf.Ticker(sym)
        info = stock.info
        name = info.get("shortName", sym)
        price = info.get("regularMarketPrice", None)
        change = info.get("regularMarketChangePercent", None)

        if price is not None and change is not None:
            result.append({
                "symbol": sym,
                "name": name,
                "price": price,
                "change": change
            })

    # Sort by % change descending
    sorted_result = sorted(result, key=lambda x: x["change"], reverse=True)

    # Display top 5
    top_5 = sorted_result[:5]
    output = []
    for stock in top_5:
        output.append(f"{stock['name']} - ₹{stock['price']} ({round(stock['change'], 2)}%)")

    return "\n".join(output)

if __name__ == "__main__":
    print(get_trending_stocks())
