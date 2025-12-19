import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

# Load env from the project root (where .env is)
load_dotenv(dotenv_path="trading_system/.env") # Explicit path since script run from root
# Or if run from root and .env is in trading_system/.env, explicitly pointing or moving .env
# The user said ".env.example" in file system, and "trading_system/.env" in previous turns.
# Actually config.py loads it. Let's just use load_dotenv which searches.
# Wait, user added keys to `/Users/krkaushikkumar/Desktop/K01/trading_system/.env`.
# If I run from root `K01`, standard load_dotenv might not find it if it's in subdirectory `trading_system`.
# I will specify path.

load_dotenv("trading_system/.env")

api_key = os.getenv("ALPACA_API_KEY")
# secret_key = os.getenv("ALPACA_SECRET_KEY") # Sometimes printed as None if not stripped?
# Best to trust the lib load or os.getenv

print(f"Checking Alpaca Keys...")
print(f"API Key found: {'Yes' if api_key else 'No'}")

try:
    # Re-read to ensure we get them
    ak = os.getenv("ALPACA_API_KEY")
    sk = os.getenv("ALPACA_SECRET_KEY")
    
    if not ak or not sk:
        print("❌ Error: Valid keys not found in environment.")
        exit(1)

    client = TradingClient(ak, sk, paper=True)
    account = client.get_account()
    
    print("\n✅ Authentication Successful!")
    print(f"Account Status: {account.status}")
    print(f"Buying Power: ${account.buying_power}")
    print(f"Cash: ${account.cash}")
    print(f"Currency: {account.currency}")

except Exception as e:
    print(f"\n❌ Connection Failed: {e}")
