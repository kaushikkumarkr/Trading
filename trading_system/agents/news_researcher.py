"""
News Research Agent
Uses Brave Search + Tavily MCP for deep market research
"""
from typing import Dict, Any, List
from ..mcp.news_client import NewsMCPClient
from ..state import TradingState

class NewsResearcherAgent:
    """
    Deep research agent using MCP servers
    """
    
    def __init__(self):
        self.news_client = NewsMCPClient()
    
    async def run(self, state: TradingState) -> Dict[str, Any]:
        """
        Runs research. 
        Note: The state object might not have fields for deep research yet, 
        so we might just append to news_headlines or use a new key.
        For now, we place it in 'news_headlines' or we'd need to extend State.
        """
        ticker = state.get("ticker", "SPY")
        
        # 1. Deep Research if event detected
        # Mock event detection logic
        # deep_res = await self.news_client.deep_research(f"{ticker} future outlook")
        
        # 2. Simple News Search (augmenting Sentiment Analyst)
        news = await self.news_client.search_news(f"{ticker} stock analysis")
        
        headlines = [n["title"] for n in news]
        
        # Return allows merging into state
        # We can append these headlines to existing
        current_headlines = state.get("news_headlines", [])
        combined = list(set(current_headlines + headlines))
        
        return {
            "news_headlines": combined
        }

news_researcher = NewsResearcherAgent()
