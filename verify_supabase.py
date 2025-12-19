import asyncio
from trading_system.mcp.database_client import SupabaseMCPClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv("trading_system/.env")

async def verify_supabase():
    print("🧪 Verifying Supabase Connection...")
    
    client = SupabaseMCPClient()
    
    if not client.client:
        print("❌ Connect Failed: Could not initialize Supabase client (Check env vars).")
        return

    test_trade = {
        "symbol": "TEST-DB",
        "side": "buy",
        "quantity": 1,
        "price": 100.00,
        "order_id": "test-uuid-verification",
        "status": "filled"
    }
    
    print(f"Attempting to log trade: {test_trade}")
    result = await client.log_trade(test_trade)
    
    if result == "logged":
        print("✅ SUCCESS: Trade logged to Supabase.")
        
        # Optional: Verify read
        print("Verifying read...")
        history = await client.get_trade_history()
        if history and history[0].get('symbol') == 'TEST-DB':
             print("✅ SUCCESS: Verified read back from DB.")
        else:
             print("⚠️ WARNING: Write succeeded but read verification failed (or delayed).")
             
    else:
        print(f"❌ FAIL: Logging failed. Result: {result}")

if __name__ == "__main__":
    asyncio.run(verify_supabase())
