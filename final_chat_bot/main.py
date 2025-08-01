from langchain.agents import Tool, initialize_agent
from llm_config import llm
from tools.get_company_profile import get_company_profile
from tools.get_trending import get_trending_stocks 
from tools.get_sentiment import get_sentiment
from tools.should_i_buy import should_i_buy
from tools.get_top_by_metric import get_top_by_metric_wrapper
from tools.get_comparison import get_comparison
from tools.get_market_news_summary import get_market_news_summary
from tools.get_low_risk_stocks import get_low_risk_stock
from tools.get_recommendation import get_recommendation

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
        func=get_trending_stocks,
        description="Use this tool to get top trending Indian stocks (NSE gainers). Example: 'Show trending stocks today'."
    ),
    
    Tool(
        name="get_sentiment",
        func=get_sentiment,
        description="Use this to get news sentiment for a given company name (only U.S. stocks like Microsoft, Google, Apple are supported).",
        return_direct=True  # ✅ Add this
  
    ),
    
 Tool(
    name="get_top_by_metric",
    func=get_top_by_metric_wrapper,
    description=(
        "Use this tool to get top stocks by financial metric.\n"
        "Understands phrases like 'most profitable company', 'top eps stocks', 'lowest pe ratio'.\n"
        "Supported metrics: return, roe, eps, pe_ratio,\n"
        "Input example: 'metric=roe, top_n=3' or 'metric=return, period_days=30'"
    )
)
    ,
    
    Tool(
        name="get_market_news",
        func=get_market_news_summary,
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
        description="Use this to get safe, low-volatility stocks with good ROE and EPS, low risk. Input: number of stocks to return (e.g., 5)"
        
    ),
     
     Tool(
    name="should_i_buy",
    func=should_i_buy,
    description="Use this to determine if a user should buy a stock. Input: company name like 'Microsoft'"

    )
     ,
     Tool(
    name="get_recommendation",
    func=get_recommendation,
    description="Use this to get 2–3 stock recommendations for today. Example: 'Which stock should I buy today?'"
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
