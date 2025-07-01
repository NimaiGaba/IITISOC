from langchain.agents import Tool, initialize_agent
from llm_config import llm
from tools.get_company_profile import get_company_profile
from tools.get_trending import get_trending  # Import earlier
from tools.get_sentiment import get_sentiment
from tools.get_news_summary import get_news_summary
from tools.should_i_buy import should_i_buy
from tools.get_top_by_metric import get_top_by_metric
from tools.get_returns import get_top_returners
from tools.get_comparison import get_comparison
from tools.get_market_news_summary import get_market_news
from tools.get_low_risk_stocks import get_low_risk_stock

import requests
from bs4 import BeautifulSoup




# ✅ Define all tools first
tools = [
    Tool(
        name="get_company_profile",
        func=get_company_profile,
        description="Use this tool to get a short business description of a company. Example: 'Tell me about Infosys'."
    ),
    Tool(
        name="get_trending",
        func=get_trending,
        description="Use this tool to get top trending Indian stocks (NSE gainers). Example: 'Show trending stocks today'."
    ),
    Tool(
        name="get_sentiment",
        func=get_sentiment,
        description="Use this to get stock sentiment based on recent headlines. Example: 'What is the sentiment for Adani?'"
    ),
     Tool(
        name="get_news_summary",
        func=get_news_summary,
        description="Use this to summarize recent news about a stock. Example: 'Why is Reliance falling today?'"
    ),
    Tool(
        name="get_top_by_metric",
        func=get_top_by_metric,
        description="Use this to show top N stocks by metric. Example: 'Top 5 undervalued largecaps', 'Midcaps with high ROE'"
    ),
    Tool(
        name="get_market_news",
        func=get_market_news,
        description="Use this to get the latest Indian stock market headlines. Ex: 'Give me today’s market news'"
    ),
    Tool(
        name="get_comparison",
        func=get_comparison,
        description="Use this to compare two stocks across key metrics like PE, ROE, revenue, etc."
    ),
     Tool(
        name="get_low_risk_stock",
        func=get_low_risk_stock,
        description="Use this to get safe, low-volatility stocks with good ROE and EPS."
    )
]



agent = initialize_agent(
    tools,
    llm,
    agent_type="openai-tools",
    verbose=True,
    handle_parsing_errors=True
)

if __name__ == "__main__":
    while True:
        user_input = input("Ask your question: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        try:
            response = agent.invoke({"input": user_input})
            print("🤖", response)
        except Exception as e:
            print("⚠️ Error:", e)
