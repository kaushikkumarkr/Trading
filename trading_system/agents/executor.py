from ..config import config
from ..state import TradingState
from ..mcp.alpaca_client import AlpacaMCPClient
from ..mcp.database_client import SupabaseMCPClient
from ..mcp.notification_client import NotificationMCPClient, AlertLevel
import asyncio

class Executor:
    def __init__(self):
        self.alpaca = AlpacaMCPClient()
        self.db = SupabaseMCPClient()
        self.notify = NotificationMCPClient()

    async def run(self, state: TradingState) -> dict: # Async
        if not state.get("risk_approved", False):
            return {
                "execution_status": "rejected",
                "error": "Risk assessment failed"
            }

        action = state["final_action"]
        ticker = state["ticker"]
        qty = state["position_size"]
        
        if action == "HOLD" or qty <= 0:
            return {
                "execution_status": "skipped",
                "reasoning": "Action is HOLD or Quantity is 0"
            }

        try:
            # 1. Place Order via MCP
            # Extended Hours requires LIMIT orders.
            order_type = "limit"
            limit_price = state["current_price"] # For buy, we might want slightly higher to fill? But let's use current.
            
            order_data = await self.alpaca.submit_order(
                symbol=ticker,
                qty=qty,
                side="buy" if action == "BUY" else "sell",
                type=order_type,
                time_in_force="day",
                extended_hours=True,
                limit_price=limit_price
            )
            
            # 2. Extract Data
            order_id = order_data.get("id")
            filled_price = order_data.get("filled_avg_price")
            expected_price = state["current_price"]
            
            if filled_price is not None:
                slippage = (filled_price - expected_price) / expected_price if expected_price else 0.0
            else:
                slippage = 0.0 # Pending order

            # 3. Log to Database via MCP
            trade_log = {
                "symbol": ticker,
                "side": action.lower(),
                "quantity": qty,
                "price": filled_price,
                "order_id": order_id
            }
            await self.db.log_trade(trade_log)

            # 4. Notify via MCP
            await self.notify.send_trade_alert(
                symbol=ticker, 
                action=action, 
                quantity=qty, 
                price=filled_price,
                reason=state.get("reasoning", ""),
                confidence=state.get("confidence_score", 0.0)
            )

            return {
                "order_id": order_id,
                "execution_status": "filled",
                "slippage": slippage
            }

        except Exception as e:
            print(f"Execution Error: {e}")
            await self.notify.send_risk_alert("execution_error", {"error": str(e)})
            return {
                "execution_status": "error",
                "error": str(e)
            }

executor = Executor()
