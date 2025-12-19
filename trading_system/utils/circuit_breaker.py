from ..state import TradingState
from ..config import config

class CircuitBreaker:
    def __init__(self):
        self.consecutive_losses = 0
        self.is_tripped = False
        self.trip_reason = ""

    def check(self, state: TradingState) -> bool:
        if self.is_tripped:
            return True # Still tripped

        # Trip on: 3 consecutive losses
        # This requires tracking history which might be in state or DB. 
        # Here we assume state has 'daily_trades' or we track it externally.
        # For this simulation, we'll check 'daily_pnl' against threshold
        
        # 1. Daily Loss Limit
        if state.get("daily_pnl", 0) < -(config.MAX_DAILY_LOSS * 100000): # Assuming 100k base
             self.trip("Daily Loss Limit Hit")
             return True

        # 2. VIX Check
        vix = state.get("vix_level", 0)
        if vix > 40:
             self.trip(f"VIX is {vix} (> 40)")
             return True
             
        # 3. Slippage Check (from last trade)
        slippage = state.get("slippage", 0)
        if slippage and slippage > 0.02:
             self.trip(f"Slippage {slippage:.2%} too high")
             return True

        return False

    def trip(self, reason: str):
        self.is_tripped = True
        self.trip_reason = reason
        print(f"CIRCUIT BREAKER TRIPPED: {reason}")
    
    def reset(self):
        self.is_tripped = False
        self.trip_reason = ""
        self.consecutive_losses = 0

circuit_breaker = CircuitBreaker()
