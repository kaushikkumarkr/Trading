import vectorbt as vbt
import yfinance as yf
from ..config import config

class Backtester:
    def __init__(self):
        pass

    def run_backtest(self, ticker: str, start_date: str, end_date: str):
        print(f"Running backtest for {ticker}...")
        
        # 1. Fetch Data
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # 2. Define Strategy (Simple MA Crossover for demo)
        # In a real system, we'd try to invoke the Agent logic, but vectorbt is best for vectorized logic
        # So we approximate the logic or just run a standard check
        
        close = data['Close']
        fast_ma = vbt.MA.run(close, 20)
        slow_ma = vbt.MA.run(close, 50)
        
        entries = fast_ma.ma_crossed_above(slow_ma)
        exits = fast_ma.ma_crossed_below(slow_ma)
        
        # 3. Run Portfolio
        portfolio = vbt.Portfolio.from_signals(
            close, entries, exits, 
            init_cash=100000,
            fees=0.001,
            slippage=0.001
        )
        
        # 4. Stats
        print(portfolio.stats())
        # portfolio.plot().show() 

backtester = Backtester()
