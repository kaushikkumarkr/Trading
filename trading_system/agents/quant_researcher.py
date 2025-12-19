# Quant Researcher Agent
# Optimizes strategy parameters using VectorBT backtesting
import json
import os
from datetime import datetime
import pandas as pd
import numpy as np
import vectorbt as vbt
from typing import Dict, Any, List
from ..mcp.alpaca_client import AlpacaMCPClient
from ..config import config

class QuantResearcher:
    def __init__(self):
        self.alpaca = AlpacaMCPClient()
        self.config_path = "trading_system/strategy_config.json"
        
    async def load_config(self) -> Dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    async def save_config(self, new_config: Dict):
        new_config["updated_at"] = datetime.now().isoformat()
        with open(self.config_path, "w") as f:
            json.dump(new_config, f, indent=4)

    async def run_optimization(self, tickers: List[str]):
        print(f"🧪 QuantResearcher: Optimizing parameters for {len(tickers)} tickers...")
        
        current_config = await self.load_config()
        
        # 1. Fetch Data (90 Days, Hourly for granularity or Daily)
        # Using daily for stability in this MVP
        try:
            # We need a proper Dataframe for VectorBT
            # Fetching one by one or bulk? AlpacaMCPClient does one by one currently.
            # For efficiency in "best" system, we'd batch, but let's iterate.
            
            for ticker in tickers:
                print(f"    Running backtests for {ticker}...")
                
                # Fetch 200 days history
                bars = await self.alpaca.get_bars(ticker, timeframe="1Day", limit=365)
                if not bars:
                    continue
                    
                df = pd.DataFrame(bars)
                # vbt expects index to be datetime (if not already?)
                # Alpaca 't' is datetime
                # vbt usually wants 'Close'
                close_price = df['c']
                
                # --- RSI Optimization ---
                # Test Windows: 10 to 30, Step 2
                windows = np.arange(10, 31, 2)
                # Ensure freq is passed if index has no freq
                rsi = vbt.RSI.run(close_price, window=windows, short_name='rsi') 
                # Note: vbt functions often don't strictly need freq unless computing returns/stats that depend on time
                # The error likely comes from Portfolio.from_signals calculating stats
                
                # Test Strategy: Buy < 30, Sell > 70
                entries = rsi.rsi_below(30)
                exits = rsi.rsi_above(70)
                
                portfolio = vbt.Portfolio.from_signals(close_price, entries, exits, init_cash=10000, fees=0.001, freq='D')
                
                # Find best performing window (Sharpe Ratio)
                sharpe = portfolio.sharpe_ratio()
                best_idx = sharpe.idxmax()
                if pd.isna(best_idx):
                    best_window = 14
                else:
                    best_window = int(best_idx)
                
                # --- SMA Optimization ---
                # --- SMA Optimization (Manual Loop for Stability) ---
                fast_windows = [10, 20, 30]
                slow_windows = [50, 100, 200]
                
                best_sma_return = -float('inf')
                best_fast, best_slow = 20, 50

                for f in fast_windows:
                    for s in slow_windows:
                        if f >= s: continue # Fast must be < Slow
                        
                        # Calculate MAs
                        fast_ma = vbt.MA.run(close_price, window=f)
                        slow_ma = vbt.MA.run(close_price, window=s)
                        
                        entries = fast_ma.ma_crossed_above(slow_ma)
                        exits = fast_ma.ma_crossed_below(slow_ma)
                        
                        # Fast simulation
                        pf = vbt.Portfolio.from_signals(close_price, entries, exits, init_cash=10000, freq='D')
                        total_return = float(pf.total_return()) 
                        
                        if total_return > best_sma_return:
                            best_sma_return = total_return
                            best_fast, best_slow = f, s
                
                print(f"    ✅ Best {ticker}: RSI Window={best_window} | SMA Fast={best_fast}, Slow={best_slow}")

                # Update Config
                if "tickers" not in current_config:
                    current_config["tickers"] = {}
                
                current_config["tickers"][ticker] = {
                    "rsi": {
                        "window": best_window,
                        "buy_threshold": 30,
                        "sell_threshold": 70
                    },
                    "sma": {
                        "fast_window": int(best_fast),
                        "slow_window": int(best_slow)
                    },
                    "last_optimized": datetime.now().isoformat()
                }

            await self.save_config(current_config)
            return {"status": "optimized", "updated_tickers": tickers}

        except Exception as e:
            print(f"QuantResearcher Error: {e}")
            return {"error": str(e)}

quant_researcher = QuantResearcher()
