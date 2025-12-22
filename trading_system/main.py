import asyncio
from dotenv import load_dotenv
import os

# Load env immediately before other imports
load_dotenv()

from trading_system.config import config
from trading_system.graph import build_graph
from trading_system.utils.data_pipeline import data_pipeline
from trading_system.utils.circuit_breaker import circuit_breaker
from datetime import datetime

async def main():
    print("🚀 Starting Multi-Agent Trading System...")
    print(f"Tickers: {config.TRADING_TICKERS}")
    
    # 1. Initialize Checkpointer (Persistence)
    checkpointer = None
    db_url = os.getenv("DATABASE_URL")
    
    # We need to hold the pool reference to keep it alive if using Postgres
    pool = None 
    
    if db_url:
        try:
            from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
            from psycopg_pool import AsyncConnectionPool
            
            print(f"🔌 Connecting to Database for Persistence...")
            # Create pool with autocommit for setup() compatibility
            pool = AsyncConnectionPool(conninfo=db_url, min_size=1, max_size=5, kwargs={"autocommit": True})
            await pool.open() # Ensure it's ready
            
            checkpointer = AsyncPostgresSaver(pool)
            await checkpointer.setup()
            print("✅ Persistence Layer (Postgres) Ready.")
            
        except Exception as e:
            print(f"❌ Persistence Error (Falling back to Memory): {e}")
            if pool: await pool.close()
            pool = None
            checkpointer = None

    # 2. Build Graph
    graph = build_graph(checkpointer=checkpointer)
    
    # 3. Start Data Pipeline (Background)
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
