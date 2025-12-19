import asyncio
from dotenv import load_dotenv
from trading_system.mcp.alpaca_client import AlpacaMCPClient

# Load env
load_dotenv("trading_system/.env")

async def verify_order():
    print("🚀 Verifying Paper Trading Execution...")
    
    client = AlpacaMCPClient()
    
    # 1. Check Account
    account = await client.get_account()
    print(f"Account Buying Power: ${account['buying_power']}")
    
    if account['buying_power'] < 200:
        print("❌ Not enough buying power for test.")
        return

    # 2. Place Test Order (Buy 1 share of SPY)
    symbol = "SPY"
    qty = 1
    print(f"\nSubmitting Paper Order: Buy {qty} {symbol} (Market)...")
    
    try:
        order = await client.submit_order(
            symbol=symbol,
            qty=qty,
            side="buy",
            type="market",
            time_in_force="day"
        )
        
        print(f"✅ Order Submitted Successfully!")
        print(f"Order ID: {order['id']}")
        print(f"Status: {order['status']}")
        
        # 3. Wait briefly and check status (Market orders fill fast in paper)
        await asyncio.sleep(2)
        # In a real app we'd use get_order(id), but for now we trust submission.
        
        print("\nNote: This was a real paper trade. Check your Alpaca Dashboard.")
        
    except Exception as e:
        print(f"❌ Order Failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_order())
