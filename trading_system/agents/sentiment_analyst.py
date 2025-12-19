from typing import List, Dict
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from ..config import config
from ..state import TradingState
from ..mcp.news_client import NewsMCPClient
import asyncio

class SentimentAnalyst:
    def __init__(self):
        # FinBERT (kept as is for analysis, but fetching changes to MCP)
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
            self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
            self.nlp = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)
        except Exception as e:
            print(f"Warning: Could not load FinBERT. {e}")
            self.nlp = None

        self.news_client = NewsMCPClient()

    async def run(self, state: TradingState) -> dict: # Async
        ticker = state["ticker"]
        
        # Fetch news via MCP
        news_items = await self.news_client.search_news(
            query=f"{ticker} stock news",
            symbols=[ticker],
            freshness="24h",
            count=10
        )
        
        headlines = [item.get("title", "") for item in news_items]
        
        if not headlines or not self.nlp:
            return {
                "news_headlines": [],
                "sentiment_scores": [],
                "aggregated_sentiment": 0.0,
                "sentiment_source": "None"
            }
            
        sentiment_scores = []
        total_score = 0.0
        
        for headline in headlines:
            result = self.nlp(headline)[0]
            label = result['label']
            score = result['score']
            
            final_score = 0.0
            if label == 'positive': final_score = score
            elif label == 'negative': final_score = -score
            
            sentiment_scores.append(final_score)
            total_score += final_score

        avg_score = total_score / len(sentiment_scores) if sentiment_scores else 0.0
        avg_score = max(min(avg_score, 1.0), -1.0)

        return {
            "news_headlines": headlines,
            "sentiment_scores": sentiment_scores,
            "aggregated_sentiment": avg_score,
            "sentiment_source": "FinBERT + BraveMCP"
        }

sentiment_analyst = SentimentAnalyst()
