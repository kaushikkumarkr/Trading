import asyncio
import os
from dotenv import load_dotenv
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

# Load Env
load_dotenv(dotenv_path="trading_system/.env")

async def verify_persistence():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ Error: DATABASE_URL not found in .env")
        return

    print(f"🔌 Connecting to Database: {db_url.split('@')[-1]}...") # Mask password
    
    try:
        # Test Connection logic similar to AsyncPostgresSaver
        # note: setup() often runs CREATE INDEX CONCURRENTLY which needs autocommit
        async with AsyncConnectionPool(conninfo=db_url, kwargs={"autocommit": True}) as pool:
            # Checkpointer uses the pool to setup
            checkpointer = AsyncPostgresSaver(pool)
            
            # Need to initialize the tables (AsyncPostgresSaver.setup())
            await checkpointer.setup()
            
            print("✅ Connection Successful!")
            print("✅ Checkpoint Tables Verified/Created.")
            
            # Simple write/read test could go here but setup() proves connectivity + permissions
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_persistence())
