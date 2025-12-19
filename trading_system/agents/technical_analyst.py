import pandas as pd
import ta
import json
import os
from ..state import TradingState
from ..mcp.alpaca_client import AlpacaMCPClient
import asyncio

class TechnicalAnalyst:
    def __init__(self):
        self.alpaca = AlpacaMCPClient()
        self.config_path = "trading_system/strategy_config.json"

    def get_ticker_config(self, ticker: str) -> dict:
        # Load config
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                data = json.load(f)
                # Return specific or default
                return data.get("tickers", {}).get(ticker, data.get("default", {}))
        
        # Fallback hardcoded defaults if file missing
        return {
            "rsi": {"window": 14, "buy_threshold": 30, "sell_threshold": 70},
            "sma": {"fast_window": 20, "slow_window": 50}
        }

    async def run(self, state: TradingState) -> dict: # Async for MCP
        ticker = state["ticker"]
        
        # 1. Fetch Data via MCP
        # Using 6 months of daily data
        bars = await self.alpaca.get_bars(ticker, timeframe="1Day", limit=200)
        
        if not bars:
            return {
                "technical_signals": {},
                "technical_score": 0.0,
                "error": "No data found via MCP"
            }

        # Convert to DataFrame
        df = pd.DataFrame(bars)
        # Ensure correct types
        close = df["c"]
        high = df["h"]
        low = df["l"]

        # 2. Calculate Indicators using 'ta' library

        # Get Params
        params = self.get_ticker_config(ticker)
        rsi_window = params.get("rsi", {}).get("window", 14)
        rsi_buy = params.get("rsi", {}).get("buy_threshold", 30)
        rsi_sell = params.get("rsi", {}).get("sell_threshold", 70)
        
        sma_fast = params.get("sma", {}).get("fast_window", 20)
        sma_slow = params.get("sma", {}).get("slow_window", 50)
        
        # RSI
        try:
            rsi_indicator = ta.momentum.RSIIndicator(close=close, window=rsi_window)
            df["RSI"] = rsi_indicator.rsi()
        except Exception:
            df["RSI"] = 50.0 # Default fallback

        # MACD (Keeping defaults for now or add to config later)
        try:
            macd = ta.trend.MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
            df["MACD"] = macd.macd()
            df["MACD_Signal"] = macd.macd_signal()
            df["MACD_Hist"] = macd.macd_diff()
        except Exception:
            df["MACD_Hist"] = 0.0

        # Bollinger Bands
        try:
            bb = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
            df["BBL_20_2.0"] = bb.bollinger_lband()
            df["BBU_20_2.0"] = bb.bollinger_hband()
        except Exception:
            pass
            
        # ATR
        try:
            atr = ta.volatility.AverageTrueRange(high=high, low=low, close=close, window=14)
            df["ATR"] = atr.average_true_range()
        except Exception:
            df["ATR"] = 0.0
        
        # SMAs
        try:
            sma20_ind = ta.trend.SMAIndicator(close=close, window=sma_fast)
            df["SMA_FAST"] = sma20_ind.sma_indicator()
            sma50_ind = ta.trend.SMAIndicator(close=close, window=sma_slow)
            df["SMA_SLOW"] = sma50_ind.sma_indicator()
        except Exception:
            pass

        # Get latest
        if len(df) > 0:
            latest = df.iloc[-1]
        else:
            return {"technical_score": 0, "technical_signals": {}}
        
        # Scoring Logic
        score = 0.0
        signals = {}
        
        # RSI Score
        rsi = float(latest.get("RSI", 50))
        signals["RSI"] = rsi
        if rsi < rsi_buy: score += 0.25
        elif rsi > rsi_sell: score -= 0.25
            
        # MACD Score
        hist = float(latest.get("MACD_Hist", 0))
        signals["MACD_Hist"] = hist
        if hist > 0: score += 0.25
        else: score -= 0.25
            
        # Trend Score
        price = float(latest["c"])
        ma_fast_val = float(latest.get("SMA_FAST", price))
        ma_slow_val = float(latest.get("SMA_SLOW", price))
        
        if price > ma_fast_val > ma_slow_val: score += 0.25
        elif price < ma_fast_val < ma_slow_val: score -= 0.25
            
        # BB Score
        bb_lower = float(latest.get("BBL_20_2.0", 0))
        bb_upper = float(latest.get("BBU_20_2.0", float('inf')))
        
        if price < bb_lower: score += 0.25
        elif price > bb_upper: score -= 0.25

        return {
            "technical_signals": signals,
            "technical_score": float(score)
        }

technical_analyst = TechnicalAnalyst()
