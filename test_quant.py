# Test Optimization Logic Explicitly
import asyncio
from trading_system.agents.quant_researcher import quant_researcher
from trading_system.config import config
import json

async def test_quant():
    print("🧪 Testing Quant Optimization...")
    
    # Run for just one ticker to be fast
    tickers = ["AAPL"] 
    print(f"Optimizing for: {tickers}")
    
    await quant_researcher.run_optimization(tickers)
    
    # Check Result
    with open("trading_system/strategy_config.json", "r") as f:
        data = json.load(f)
        
    print("\n✅ Config Updated:")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    asyncio.run(test_quant())
