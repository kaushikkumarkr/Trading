import asyncio
from dotenv import load_dotenv
import os

# Load env FIRST
load_dotenv(dotenv_path="trading_system/.env")

from trading_system.utils.llm_client import llm_client

async def test_brain():
    print("🧠 Testing Multi-LLM Brain...\n")
    
    providers = ["gemini", "groq"]
    # openrouter check if key exists
    if os.getenv("OPENROUTER_API_KEY"):
        providers.append("openrouter")
        
    for provider in providers:
        print(f"--- Testing {provider.upper()} ---")
        try:
            llm = llm_client.get_model(provider=provider)
            response = llm.invoke("Say 'Hello Trader' and nothing else.")
            print(f"✅ Response: {response.content}")
        except Exception as e:
            print(f"❌ Failed: {e}")
        print("")

if __name__ == "__main__":
    asyncio.run(test_brain())
