"""
Notification MCP Client
Sends alerts via Slack and Discord
"""
import os
import aiohttp
from typing import Optional, List, Dict, Any
from enum import Enum

class AlertLevel(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    CRITICAL = "critical"

class NotificationMCPClient:
    """Multi-channel notification client"""
    
    def __init__(self):
        self.slack_token = os.getenv("SLACK_BOT_TOKEN")
        self.slack_channel = os.getenv("SLACK_CHANNEL", "#trading-alerts")
        self.discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
    
    async def send_trade_alert(
        self,
        symbol: str,
        action: str,
        quantity: int,
        price: float,
        reason: str,
        confidence: float
    ) -> None:
        """Send trade execution alert"""
        emoji = "🟢" if action == "BUY" else "🔴"
        message = f"{emoji} **TRADE EXECUTED**\n**{action}** {quantity} {symbol} @ ${price:.2f}\n*Why:* {reason} ({confidence*100:.1f}%)"
        await self._send_to_all(message, AlertLevel.SUCCESS if action == "BUY" else AlertLevel.WARNING)
    
    async def send_risk_alert(
        self,
        alert_type: str,
        details: Dict[str, Any],
        level: AlertLevel = AlertLevel.WARNING
    ) -> None:
        """Send risk management alert"""
        message = f"⚠️ **RISK ALERT TRIPPED**\nType: {alert_type}\nDetails: {details}"
        await self._send_to_all(message, level)
    
    async def send_circuit_breaker_alert(
        self,
        reason: str,
        triggered_at: str
    ) -> None:
        """Send circuit breaker trip alert - CRITICAL"""
        message = f"🚨 **CIRCUIT BREAKER TRIGGERED** 🚨\nReason: {reason}\nSystem Halted until reset."
        await self._send_to_all(message, AlertLevel.CRITICAL)
    
    async def _send_to_all(self, message: str, level: AlertLevel) -> None:
        """Send to all enabled channels"""
        print(f"NOTIFICATION [{level.value}]: {message}") # Console Fallback

        if self.discord_webhook:
            try:
                async with aiohttp.ClientSession() as session:
                    # Simple color coding for embeds could be added, but sending plain content first
                    payload = {"content": message}
                    async with session.post(self.discord_webhook, json=payload) as response:
                        if response.status >= 300:
                            print(f"❌ Discord API Error: {response.status}")
                            print(await response.text())
                        else:
                            print(f"✅ Discord Sent: {response.status}")
            except Exception as e:
                print(f"Failed to send Discord alert: {e}")
        
        if self.slack_token:
            try:
                from slack_sdk import WebClient
                client = WebClient(token=self.slack_token)
                client.chat_postMessage(channel=self.slack_channel, text=message)
            except Exception as e:
                print(f"Failed to send Slack alert: {e}")

notification_client = NotificationMCPClient()
