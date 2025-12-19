"""
Notification MCP Client
Sends alerts via Slack and Discord
"""
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
        self.slack_enabled = True
        self.discord_enabled = True
    
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
        message = f"TRADE: {action} {quantity} {symbol} @ {price}"
        await self._send_to_all(message, AlertLevel.SUCCESS if action == "BUY" else AlertLevel.WARNING)
    
    async def send_risk_alert(
        self,
        alert_type: str,
        details: Dict[str, Any],
        level: AlertLevel = AlertLevel.WARNING
    ) -> None:
        """Send risk management alert"""
        pass
    
    async def send_circuit_breaker_alert(
        self,
        reason: str,
        triggered_at: str
    ) -> None:
        """Send circuit breaker trip alert - CRITICAL"""
        message = f"🚨 CIRCUIT BREAKER TRIGGERED: {reason}"
        await self._send_to_all(message, AlertLevel.CRITICAL)
    
    async def _send_to_all(self, message: str, level: AlertLevel) -> None:
        """Send to all enabled channels"""
        print(f"NOTIFICATION [{level.value}]: {message}")
