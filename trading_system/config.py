import os
from dataclasses import dataclass, field
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

@dataclass
class MCPConfig:
    """MCP Server configurations"""
    
    # Alpaca Trading
    alpaca_mcp_url: str = "https://mcp.alpaca.markets/sse"
    alpaca_paper: bool = True
    
    # Yahoo Finance (local)
    yahoo_finance_enabled: bool = True
    
    # Brave Search
    brave_api_key: str = field(default_factory=lambda: os.getenv("BRAVE_API_KEY", ""))
    brave_enabled: bool = True
    
    # Tavily Research
    tavily_api_key: str = field(default_factory=lambda: os.getenv("TAVILY_API_KEY", ""))
    tavily_enabled: bool = True
    
    # Supabase
    supabase_project_ref: str = field(default_factory=lambda: os.getenv("SUPABASE_PROJECT_REF", ""))
    supabase_mcp_url: str = field(init=False)
    
    # Slack
    slack_bot_token: str = field(default_factory=lambda: os.getenv("SLACK_BOT_TOKEN", ""))
    slack_channel: str = field(default_factory=lambda: os.getenv("SLACK_CHANNEL", "#trading-alerts"))
    slack_enabled: bool = True
    
    # Discord
    discord_webhook_url: str = field(default_factory=lambda: os.getenv("DISCORD_WEBHOOK_URL", ""))
    discord_enabled: bool = True
    
    # GitHub
    github_token: str = field(default_factory=lambda: os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", ""))
    github_enabled: bool = False
    
    def __post_init__(self):
        self.supabase_mcp_url = f"https://mcp.supabase.com/mcp?project_ref={self.supabase_project_ref}"

@dataclass
class TradingConfig:
    """Trading parameters"""
    
    # Tickers
    TRADING_TICKERS: List[str] = field(default_factory=lambda: ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"])
    
    # Risk Management
    MAX_POSITION_PCT: float = 0.10
    MAX_RISK_PER_TRADE: float = 0.02
    MAX_DAILY_LOSS: float = 0.05
    MAX_DRAWDOWN: float = 0.10
    MIN_CONFIDENCE: float = 0.6
    MAX_DAILY_TRADES: int = 20
    
    # Technical Analysis
    RSI_PERIOD: int = 14
    MACD_FAST: int = 12
    MACD_SLOW: int = 26
    MACD_SIGNAL: int = 9
    BB_PERIOD: int = 20
    BB_STD: int = 2
    
    # Circuit Breaker
    CONSECUTIVE_LOSS_LIMIT: int = 3
    VIX_THRESHOLD: float = 40.0
    SLIPPAGE_THRESHOLD: float = 0.02
    
    # Keys (Legacy Support until full migration)
    ALPACA_API_KEY: str = os.getenv("ALPACA_API_KEY", "")
    ALPACA_SECRET_KEY: str = os.getenv("ALPACA_SECRET_KEY", "")
    PAPER_TRADING: bool = True

@dataclass
class Config:
    """Main configuration"""
    mcp: MCPConfig = field(default_factory=MCPConfig)
    trading: TradingConfig = field(default_factory=TradingConfig)
    
    # LLM
    GOOGLE_API_KEY: str = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""))
    ANTHROPIC_API_KEY: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    
    # Redis
    REDIS_URL: str = field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379"))
    
    # Backward compatibility for direct access
    @property
    def ALPACA_API_KEY(self): return self.trading.ALPACA_API_KEY
    @property
    def ALPACA_SECRET_KEY(self): return self.trading.ALPACA_SECRET_KEY
    @property
    def PAPER_TRADING(self): return self.trading.PAPER_TRADING
    @property
    def TRADING_TICKERS(self): return self.trading.TRADING_TICKERS
    @property
    def MAX_DAILY_LOSS(self): return self.trading.MAX_DAILY_LOSS
    @property
    def MAX_RISK_PER_TRADE(self): return self.trading.MAX_RISK_PER_TRADE
    @property
    def MIN_CONFIDENCE(self): return self.trading.MIN_CONFIDENCE
    @property
    def MAX_POSITION_PCT(self): return self.trading.MAX_POSITION_PCT

config = Config()
