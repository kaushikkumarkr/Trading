"""
Supabase MCP Client
Handles trade logging, portfolio history, and state persistence
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
from supabase import create_client, Client

class SupabaseMCPClient:
    """
    Real-world Database Client using Supabase Cloud (Free Tier).
    """
    
    def __init__(self, project_ref: str = None):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = None
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
            except Exception as e:
                print(f"Supabase Init Error: {e}")

    async def log_trade(self, trade: Dict[str, Any]) -> str:
        """
        Log a trade to Supabase 'trades' table
        """
        if not self.client:
            print(f"DB FALLBACK (No Creds): {trade}")
            return "no_db"

        try:
            # Supabase-py is sync by default, but fast enough for this agent loop.
            # Ideally wrap in executor, but direct call is acceptable for low frequency.
            data = self.client.table("trades").insert(trade).execute()
            print(f"✅ DB LOG: Saved to Supabase - {trade.get('symbol')}")
            return "logged"
        except Exception as e:
            print(f"❌ Supabase Error: {e}")
            return "error"
    
    async def get_trade_history(self) -> List[Dict]:
        """Get historical trades"""
        if not self.client: return []
        try:
            response = self.client.table("trades").select("*").order("timestamp", desc=True).limit(50).execute()
            return response.data
        except Exception:
            return []

    # Stubs
    async def save_portfolio_snapshot(self, snapshot: Dict[str, Any]) -> None: pass
    async def get_performance_metrics(self, period: str = "30d") -> Dict[str, Any]: return {}
    async def save_agent_state(self, agent_name: str, state: Dict[str, Any]) -> None: pass
    async def load_agent_state(self, agent_name: str) -> Optional[Dict]: return None
