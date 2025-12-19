import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load env
load_dotenv("trading_system/.env")

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Checking Google API Key...")
print(f"API Key found: {'Yes' if api_key else 'No (Check .env)'}")

if not api_key:
    exit(1)

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key,
        temperature=0
    )
    
    print("\nSending test message to Gemini 2.0 Flash...")
    response = llm.invoke([HumanMessage(content="Say 'Hello Trader' and nothing else.")])
    
    print(f"\n✅ Success! Response: {response.content}")

except Exception as e:
    print(f"\n❌ Failed: {e}")
