from ..config import config
from ..state import TradingState

class RiskAgent:
    def __init__(self):
        pass

    def run(self, state: TradingState) -> dict:
        action = state.get("final_action", "HOLD")
        confidence = state.get("confidence_score", 0.0)
        current_price = state.get("current_price", 100.0) # avoid div/0
        account_value = state.get("account_value", 100000.0)
        
        if action == "HOLD":
            return {
                "position_size": 0,
                "stop_loss_price": None,
                "take_profit_price": None,
                "risk_approved": True 
            }
            
        # 1. Risk Checks
        if confidence < config.MIN_CONFIDENCE:
            return {
                "position_size": 0,
                "risk_approved": False,
                "reasoning": f"Low confidence: {confidence} < {config.MIN_CONFIDENCE}"
            }
            
        if state.get("daily_pnl", 0) < -(account_value * config.MAX_DAILY_LOSS):
             return {
                "position_size": 0,
                "risk_approved": False,
                "reasoning": "Max daily loss exceeded"
            }

        # 2. Position Sizing
        # Method A: Fixed % Risk (e.g. 2% of equity)
        risk_amount = account_value * config.MAX_RISK_PER_TRADE
        
        # Calculate volatility based stop distance (ATR)
        # Assuming ATR is available from technicals, otherwise default to 2%
        atr = state.get("technical_signals", {}).get("ATR", current_price * 0.02)
        stop_distance = atr * 2
        
        if stop_distance == 0: stop_distance = current_price * 0.01

        # Shares based on risk: Risk Amount / Risk Per Share
        size_risk_based = risk_amount / stop_distance
        
        # Method B: Max position percentage (e.g. 10% of portfolio)
        max_position_value = account_value * config.MAX_POSITION_PCT
        size_max_pos = max_position_value / current_price
        
        # Take minimum
        position_size = int(min(size_risk_based, size_max_pos))
        
        # Scale by confidence? (Optional, maybe reducing size if confidence is barely above threshold)
        if confidence < 0.8:
            position_size = int(position_size * 0.8)
            
        # 3. Stop Loss & Take Profit
        if action == "BUY":
            stop_loss = current_price - stop_distance
            take_profit = current_price + (stop_distance * 2) # 2:1 Reward ratio
        else: # SELL
            stop_loss = current_price + stop_distance
            take_profit = current_price - (stop_distance * 2)

        return {
            "position_size": position_size,
            "stop_loss_price": stop_loss,
            "take_profit_price": take_profit,
            "risk_approved": True
        }

risk_agent = RiskAgent()
