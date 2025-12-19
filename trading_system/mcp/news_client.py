"""
News MCP Client - Aggregates Brave Search + Tavily
Provides real-time news and research capabilities
"""
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS

class NewsMCPClient:
    """
    Real-world News Client using DuckDuckGo (FOSS).
    No API Keys required.
    """
    
    def __init__(self):
        self.ddgs = DDGS()
    
    async def search_news(
        self,
        query: str,
        symbols: Optional[List[str]] = None,
        freshness: str = "day", # DDG uses 'd', 'w', 'm'
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for financial news using DuckDuckGo.
        """
        print(f"📰 Searching News for: {query}")
        try:
            # DDGS is synchronous, but fast. In a high-perf asyncio app we might wrap in thread executor,
            # but for this scale direct call is fine or we can use the async wrapper if available (v6 has async? sticking to sync for stability unless verified).
            # v4+ usually sync. Let's wrap in simple sync call for now.
            
            # Map freshness
            timelimit = 'd' if freshness == '24h' else 'w'
            
            results = self.ddgs.news(keywords=query, region="us-en", safesearch="off", timelimit=timelimit, max_results=count)
            
            # Normalize format
            normalized = []
            for r in results:
                normalized.append({
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "source": r.get("source"),
                    "published": r.get("date")
                })
            
            return normalized

        except Exception as e:
            print(f"News Search Error: {e}")
            return []
    
    async def deep_research(self, topic: str) -> Dict[str, Any]:
        """Simple Deep Search simulation using standard search"""
        results = self.ddgs.text(keywords=topic, max_results=5)
        return {
            "summary": f"Research on {topic}",
            "sources": results
        }

