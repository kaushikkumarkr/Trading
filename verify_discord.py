import asyncio
import os
from dotenv import load_dotenv

# Load env vars FIRST
load_dotenv(dotenv_path="trading_system/.env")

from trading_system.mcp.notification_client import notification_client, AlertLevel

async def test_discord():
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    print(f"Testing Discord Webhook: {webhook[:20]}... (masked)")
    
    if not webhook:
        print("❌ Error: DISCORD_WEBHOOK_URL is missing in .env")
        return

    print("Sending test alert...")
    
    # Test Trade Alert
    await notification_client.send_trade_alert(
        symbol="TEST-COIN",
        action="BUY",
        quantity=100,
        price=420.69,
        reason="Manual System Verification",
        confidence=0.99
    )
    
    # Test Critical Alert
    await notification_client.send_circuit_breaker_alert(
        reason="Manual Test Trigger",
        triggered_at="Now"
    )
    
    print("✅ Alerts sent. Check your Discord channel!")

if __name__ == "__main__":
    asyncio.run(test_discord())
