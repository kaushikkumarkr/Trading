# Force a trade immediately to prove the system works
import asyncio
from trading_system.agents.executor import executor
from trading_system.state import TradingState
from trading_system.mcp.alpaca_client import AlpacaMCPClient

async def force_trade():
    print("🚀 Forcing a Test Trade (Bypassing Strategy)...")
    
    # Check Price
    client = AlpacaMCPClient()
    bars = await client.get_bars("AAPL", limit=1)
    price = bars[0]['c']
    print(f"Current AAPL Price: {price}")
    
    # Construct Forced State
    forced_state = {
        "ticker": "AAPL",
        "current_price": price,
        "risk_approved": True,
        "final_action": "BUY",
        "position_size": 1,
        "confidence_score": 1.0, # MAX CONFIDENCE
        "reasoning": "FORCED TEST TRADE BY USER"
    }
    
    # Execute
    print(f"Executing: BUY 1 AAPL @ {price} (Extended Hours)")
    result = await executor.run(forced_state)
    
    print("\n✅ Execution Result:")
    print(result)

if __name__ == "__main__":
    asyncio.run(force_trade())
