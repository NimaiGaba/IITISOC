## Not working

import requests
from bs4 import BeautifulSoup

def get_trending(_input: str = ""):
    url = "https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the table with gainers
        table = soup.find("table", {"class": "tbldata14"})
        rows = table.find_all("tr")[1:6]  # Top 5 stocks

        trending_stocks = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 1:
                name = cols[0].text.strip()
                price = cols[1].text.strip()
                change = cols[4].text.strip()
                trending_stocks.append(f"{name} – ₹{price} ({change})")

        return "📈 Top Trending NSE Gainers:\n" + "\n".join([f"• {stock}" for stock in trending_stocks])

    except Exception as e:
        return f"⚠️ Failed to fetch trending stocks: {e}"


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# def get_trending(_input=None):
#     driver = None
#     try:
#         options = Options()
#         options.add_argument("--headless=new")  # NEW Headless mode for Chrome 109+
#         options.add_argument("--disable-gpu")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         options.add_argument("--window-size=1920,1080")

#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)

#         driver.get("https://www.nseindia.com/market-data/top-gainers")

#         # Wait until the table rows are loaded
#         WebDriverWait(driver, 15).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
#         )

#         rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
#         trending_stocks = []

#         for row in rows[:5]:
#             cols = row.find_elements(By.TAG_NAME, "td")
#             if len(cols) >= 5:
#                 name = cols[0].text.strip()
#                 price = cols[1].text.strip()
#                 change = cols[4].text.strip()
#                 trending_stocks.append(f"{name} – ₹{price} ({change}%)")

#         if not trending_stocks:
#             raise ValueError("⚠️ Table found, but no data extracted. Check site layout.")

#         return "📈 Top Trending NSE Gainers:\n" + "\n".join(f"• {s}" for s in trending_stocks)

#     except Exception as e:
#         return f"⚠️ Failed to fetch trending stocks: {str(e)}"

#     finally:
#         if driver:
#             driver.quit()
