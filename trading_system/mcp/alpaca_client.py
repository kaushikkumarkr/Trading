"""
Alpaca MCP Client Wrapper
Provides trading operations via Alpaca's Official SDK (Embedded Mode)
"""
from typing import Optional, Dict, Any, List
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderStatus
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from ..config import config
from datetime import datetime, timedelta

class AlpacaMCPClient:
    """Wrapper for Alpaca operations using the official SDK using local keys"""
    
    def __init__(self, mcp_url: str = None):
        # We ignore mcp_url in this embedded mode and use config keys
        self.trading_client = TradingClient(
            api_key=config.ALPACA_API_KEY,
            secret_key=config.ALPACA_SECRET_KEY,
            paper=config.PAPER_TRADING
        )
        self.data_client = StockHistoricalDataClient(
            api_key=config.ALPACA_API_KEY,
            secret_key=config.ALPACA_SECRET_KEY
        )
    
    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get latest bar as 'quote' approximation"""
        # Data client is synchronous usually, but we wrap result or use standard calls
        # Note: alpaca-py historical methods usually sync? 
        # Actually StockHistoricalDataClient is sync. 
        # We can implement async wrapper if needed or just block for simplicity in this 'embedded mcp'
        
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Minute,
            start=datetime.now() - timedelta(days=1),
            limit=1
        )
        bars = self.data_client.get_stock_bars(request_params)
        if bars.df.empty:
            return {"symbol": symbol, "price": 0.0}
        
        price = bars[symbol][0].close
        return {"symbol": symbol, "price": price}
    
    async def get_bars(self, symbol: str, timeframe: str = "1Day", limit: int = 100) -> List[Dict]:
        """Get historical bars"""
        tf = TimeFrame.Day
        if timeframe == "1Min": tf = TimeFrame.Minute
        
        start = datetime.now() - timedelta(days=limit * 2) # Buffer
        
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=tf,
            start=start,
            limit=limit
        )
        
        bars = self.data_client.get_stock_bars(request_params)
        data = []
        for bar in bars[symbol]:
            data.append({
                "t": bar.timestamp,
                "o": bar.open,
                "h": bar.high,
                "l": bar.low,
                "c": bar.close,
                "v": bar.volume
            })
        return data
    
    async def get_account(self) -> Dict[str, Any]:
        """Get account information"""
        acc = self.trading_client.get_account()
        return {
            "buying_power": float(acc.buying_power),
            "cash": float(acc.cash),
            "portfolio_value": float(acc.portfolio_value),
            "status": acc.status
        }
    
    async def get_positions(self) -> List[Dict]:
        """Get current positions"""
        positions = self.trading_client.get_all_positions()
        return [{"symbol": p.symbol, "qty": float(p.qty), "market_value": float(p.market_value)} for p in positions]
    
    async def submit_order(
        self, 
        symbol: str, 
        qty: int, 
        side: str, 
        type: str = "market", 
        time_in_force: str = "day", 
        extended_hours: bool = False,
        limit_price: float = None
    ) -> Dict[str, Any]:
        """Submits an order"""
        if qty <= 0: return {}
        try:
            req_params = {
                "symbol": symbol,
                "qty": qty,
                "side": OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
                "time_in_force": TimeInForce.DAY if time_in_force.lower() == "day" else TimeInForce.GTC,
                "extended_hours": extended_hours
            }
            
            if type.lower() == "limit":
                req = LimitOrderRequest(
                    **req_params,
                    limit_price=limit_price
                )
            else:
                req = MarketOrderRequest(**req_params)

            order = self.trading_client.submit_order(req)
            return {
                "id": str(order.id),
                "status": str(order.status),
                "filled_avg_price": float(order.filled_avg_price) if order.filled_avg_price else None
            }
        except Exception as e:
            print(f"Alpaca Order Error: {e}")
            return {}
