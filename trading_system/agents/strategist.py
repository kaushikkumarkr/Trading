# from langchain_google_genai import ChatGoogleGenerativeAI # Replaced by LLMClient
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from ..config import config
from ..state import TradingState
import json

class TradeDecision(BaseModel):
    action: Literal["BUY", "SELL", "HOLD"] = Field(description="The trading action to take")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    reasoning: str = Field(description="Detailed reasoning for the decision")

from ..utils.llm_client import llm_client

class Strategist:
    def __init__(self):
        # Default to Gemini (Smartest) if not specified
        # In a real evolution, this could be passed via config
        self.llm = llm_client.get_model(provider="gemini", temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=TradeDecision)
        
        self.prompt = PromptTemplate(
            template="""You are a Senior Hedge Fund Portfolio Manager. Analyze the following market data and make a trading decision.

Context:
- Ticker: {ticker}
- Price: {price}
- VIX Regime: {vix_regime} (Level: {vix_level})
- Sector Momentum: {sector_momentum:.4f}

Technical Analysis (Score: {technical_score}):
{technical_signals}

Sentiment Analysis (Score: {sentiment_score}):
Top Headlines: {headlines}

News Research Report:
{research_report}

Decision Rules:
- STRONG_BUY: Technical > 0.5, Sentiment > 0.3, VIX < 25
- BUY: Technical > 0.2, Sentiment > 0, Favorable Sector
- SELL: Technical < -0.2, Sentiment < 0
- STRONG_SELL: Technical < -0.5, Sentiment < -0.3, VIX > 30
- HOLD: Conflicting signals or low confidence

Provide a JSON decision with action, confidence (0-1), and reasoning.
{format_instructions}
""",
            input_variables=["ticker", "price", "vix_regime", "vix_level", "sector_momentum", 
                           "technical_score", "technical_signals", "sentiment_score", "headlines", "research_report"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def run(self, state: TradingState) -> dict:
        try:
            # Prepare Input
            input_data = {
                "ticker": state["ticker"],
                "price": state.get("current_price", 0.0),
                "vix_regime": state.get("vix_regime", "normal"),
                "vix_level": state.get("vix_level", 20.0),
                "sector_momentum": state.get("sector_momentum", 0.0),
                "technical_score": state.get("technical_score", 0.0),
                "technical_signals": str(state.get("technical_signals", {})),
                "sentiment_score": state.get("aggregated_sentiment", 0.0),
                "headlines": str(state.get("news_headlines", [])[:3]),
                "research_report": state.get("research_report", "No special research requested.")
            }
            
            # Generate Decision
            chain = self.prompt | self.llm | self.parser
            decision = chain.invoke(input_data)
            
            return {
                "final_action": decision.action,
                "confidence_score": decision.confidence,
                "reasoning": decision.reasoning
            }
        except Exception as e:
            print(f"Strategist Error: {e}")
            return {
                "final_action": "HOLD",
                "confidence_score": 0.0,
                "reasoning": f"Error in strategy generation: {e}"
            }

strategist = Strategist()
