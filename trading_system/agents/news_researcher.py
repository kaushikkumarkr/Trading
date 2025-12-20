from typing import Dict, Any
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ..utils.llm_client import llm_client
from ..state import TradingState

class NewsResearcherAgent:
    """
    Active Research Agent.
    Uses DuckDuckGo to answer specific market questions.
    """
    
    def __init__(self):
        self.search = DuckDuckGoSearchRun()
        self.llm = llm_client.get_model(provider="gemini", temperature=0) # Smart model for synthesis
        
        self.prompt = PromptTemplate(
            template="""You are a deep-dive financial researcher.
            
            Task: Research the following ticker and current market situation.
            
            Ticker: {ticker}
            Search Results:
            {search_results}
            
            Question: Wht is driving the price action today? Are there any major catalytic events (Earnings, FDA approvals, Lawsuits, Macro news)?
            
            Output: A concise research report (bullet points) summarizing the key drivers. If no news is found, state "No significant news found."
            """,
            input_variables=["ticker", "search_results"]
        )

    async def run(self, state: TradingState) -> Dict[str, Any]:
        ticker = state.get("ticker", "SPY")
        print(f"🕵️‍♂️ NewsResearcher: Searching for info on {ticker}...")
        
        try:
            # 1. Search Query
            query = f"{ticker} stock news reason for price move today"
            results = self.search.invoke(query)
            
            # 2. Synthesize with LLM
            chain = self.prompt | self.llm | StrOutputParser()
            report = await chain.ainvoke({"ticker": ticker, "search_results": results})
            
            return {
                "research_report": report
            }
            
        except Exception as e:
            print(f"NewsResearcher Error: {e}")
            return {
                "research_report": f"Error fetching news: {e}"
            }

news_researcher = NewsResearcherAgent()
