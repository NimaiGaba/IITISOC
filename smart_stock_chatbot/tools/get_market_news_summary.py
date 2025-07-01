import requests
from bs4 import BeautifulSoup


def get_market_news():
    url = "https://www.moneycontrol.com/news/business/markets/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return "⚠️ Could not fetch market news right now."

        soup = BeautifulSoup(res.text, "html.parser")
        headlines = soup.select("ul.li_listing li a")

        news_items = []
        for headline in headlines:
            title = headline.text.strip()
            link = headline['href'].strip()
            if title and link and "video" not in link:
                news_items.append(f"🔹 {title}\n{link}")
            if len(news_items) >= 8:
                break

        if not news_items:
            return "⚠️ No headlines found right now."

        return "📰 **Today's Market News:**\n\n" + "\n\n".join(news_items)

    except Exception as e:
        return f"❌ Error fetching news: {str(e)}"


def get_market_news():
    url = "https://www.moneycontrol.com/news/business/markets/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return "⚠️ Could not fetch market news right now."

        soup = BeautifulSoup(res.text, "html.parser")
        headlines = soup.select("ul.li_listing li a")

        news_items = []
        for headline in headlines:
            title = headline.text.strip()
            link = headline['href'].strip()
            if title and link and "video" not in link:
                news_items.append(f"🔹 {title}\n{link}")
            if len(news_items) >= 8:
                break

        if not news_items:
            return "⚠️ No headlines found right now."

        return "📰 **Today's Market News:**\n\n" + "\n\n".join(news_items)

    except Exception as e:
        return f"❌ Error fetching news: {str(e)}"
