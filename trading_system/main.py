import asyncio
from dotenv import load_dotenv
import os
from trading_system.config import config
from trading_system.graph import build_graph
from trading_system.utils.data_pipeline import data_pipeline
from trading_system.utils.circuit_breaker import circuit_breaker
from datetime import datetime

# Load env
load_dotenv()

async def main():
    print("🚀 Starting Multi-Agent Trading System...")
    print(f"Tickers: {config.TRADING_TICKERS}")
    
    # 1. Initialize Graph
    graph = build_graph()
    
    # 2. Start Data Pipeline (Background)
    # asyncio.create_task(data_pipeline.start_stream())
    
    # 3. Trading Loop
    # In a real event-driven system, we'd react to data_pipeline events.
    # Here, we'll simulate a loop for demonstration.
    
    print("\n--- Starting Trading Cycle ---\n")
    
    # Initial State
    initial_state = {
        "ticker": "AAPL",
        "current_price": 150.0, # Mock start
        "timestamp": datetime.now(),
        "account_value": 100000.0,
        "daily_pnl": 0.0
    }
    
    # Run the Graph
    # We use .stream() or .invoke(). .invoke() runs until END.
    
    config_run = {"recursion_limit": 50, "configurable": {"thread_id": "1"}}
    
    try:
        if circuit_breaker.check(initial_state):
            print("Circuit breaker active. Halting.")
            return

        final_state = await graph.ainvoke(initial_state, config_run)
        
        print("\n--- Cycle Complete ---")
        print(f"Action: {final_state.get('final_action')}")
        print(f"Confidence: {final_state.get('confidence_score')}")
        print(f"Reasoning: {final_state.get('reasoning')}")
        print(f"Execution: {final_state.get('execution_status')}")
        
    except Exception as e:
        print(f"System Error: {e}")

from trading_system.agents.quant_researcher import quant_researcher

async def run_loop():
    # Phase 2: Run Initial Optimization (The "Nightly" Build)
    try:
        print("\n🧬 Running Initial Strategy Optimization (VectorBT)...")
        # Optimize safely for Top Tickers
        await quant_researcher.run_optimization(config.TRADING_TICKERS)
        print("✅ Strategy parameters updated based on recent market conditions.")
    except Exception as e:
        print(f"⚠️ Optimization Warning: {e}")

    while True:
        try:
            print("\n" + "="*50)
            print(f"🕒 Cycle Start: {datetime.now()}")
            print("="*50 + "\n")
            
            await main()
            
            print("\n💤 Sleeping for 15 minutes...")
            await asyncio.sleep(900) # 15 minutes
            
        except KeyboardInterrupt:
            print("\n🛑 Stopping System (User Interrupt)")
            break
        except Exception as e:
            print(f"\n❌ Critical Error in Loop: {e}")
            print("Restarting in 60 seconds...")
            await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(run_loop())
    except KeyboardInterrupt:
        pass
