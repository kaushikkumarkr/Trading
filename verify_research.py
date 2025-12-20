import asyncio
from dotenv import load_dotenv
# Load env variables (API keys)
load_dotenv(dotenv_path="trading_system/.env")

from trading_system.agents.news_researcher import news_researcher
from trading_system.state import TradingState

async def test_research():
    print("🕵️‍♂️ Testing Deep Research Agent (DuckDuckGo + Gemini)...\n")
    
    # Mock State
    state: TradingState = {
        "ticker": "TSLA"
    }
    
    print(f"Goal: Research why {state['ticker']} is moving today.")
    
    result = await news_researcher.run(state)
    
    print("\n--- Research Report ---")
    print(result.get("research_report"))
    print("-----------------------\n")
    
    if "Error" in str(result.get("research_report")):
        print("❌ Test Failed")
    else:
        print("✅ Test Passed")

if __name__ == "__main__":
    asyncio.run(test_research())
