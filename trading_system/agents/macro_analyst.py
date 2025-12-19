import yfinance as yf
from ..state import TradingState

class MacroAnalyst:
    def __init__(self):
        self.sector_map = {
            "AAPL": "XLK", "MSFT": "XLK", "NVDA": "XLK", 
            "GOOGL": "XLC", "META": "XLC",
            "JPM": "XLF", "BAC": "XLF",
            "TSLA": "XLY", "AMZN": "XLY"
        }

    def run(self, state: TradingState) -> dict:
        ticker = state["ticker"]
        
        # 1. VIX Analysis
        try:
            vix = yf.Ticker("^VIX")
            vix_hist = vix.history(period="5d")
            if not vix_hist.empty:
                current_vix = vix_hist["Close"].iloc[-1]
                if hasattr(current_vix, "item"): current_vix = current_vix.item()
            else:
                current_vix = 20.0 # Fallback
        except Exception as e:
            print(f"VIX Error: {e}")
            current_vix = 20.0

        if current_vix < 15:
            regime = "low"
        elif current_vix < 25:
            regime = "normal"
        elif current_vix < 35:
            regime = "elevated"
        else:
            regime = "crisis"

        # 2. Sector Momentum
        sector_ticker = self.sector_map.get(ticker, "SPY") # Default to market if unknown
        try:
            sector_data = yf.download(sector_ticker, period="1mo", progress=False)
            spy_data = yf.download("SPY", period="1mo", progress=False)
            
            if not sector_data.empty and not spy_data.empty:
                # Handle potential MultiIndex or Series
                sector_close = sector_data["Close"]
                if hasattr(sector_close, "iloc"):
                    c_start = sector_close.iloc[0]
                    c_end = sector_close.iloc[-1]
                else:
                    c_start = sector_close[0]
                    c_end = sector_close[-1]
                
                # Convert to float (handle if they are Series/Arrays of size 1)
                if hasattr(c_start, "item"): c_start = c_start.item()
                if hasattr(c_end, "item"): c_end = c_end.item()

                spy_close = spy_data["Close"]
                if hasattr(spy_close, "iloc"):
                    s_start = spy_close.iloc[0]
                    s_end = spy_close.iloc[-1]
                else:
                    s_start = spy_close[0]
                    s_end = spy_close[-1]

                if hasattr(s_start, "item"): s_start = s_start.item()
                if hasattr(s_end, "item"): s_end = s_end.item()

                sector_perf = (float(c_end) / float(c_start)) - 1
                spy_perf = (float(s_end) / float(s_start)) - 1
                momentum = sector_perf - spy_perf
            else:
                momentum = 0.0
        except Exception as e:
            print(f"Macro Analyst Error: {e}")
            momentum = 0.0

        return {
            "vix_level": float(current_vix),
            "vix_regime": regime,
            "sector_momentum": float(momentum)
        }

macro_analyst = MacroAnalyst()
