from typing import TypedDict, List, Optional, Literal, Annotated
import operator
from datetime import datetime

class TradingState(TypedDict, total=False):
    # Market Data
    ticker: str
    current_price: float
    price_history: List[float]
    volume_history: List[float]
    timestamp: datetime
    
    # Technical Analysis
    technical_signals: dict  # RSI, MACD, BB, ATR, SMA20, SMA50
    technical_score: float   # -1 to 1
    
    # Sentiment Analysis
    news_headlines: Annotated[List[str], operator.add]
    sentiment_scores: List[float]
    aggregated_sentiment: float  # -1 to 1
    sentiment_source: str
    
    # Macro Context
    vix_level: Optional[float]
    vix_regime: str  # "low", "normal", "elevated", "crisis"
    sector_momentum: Optional[float]
    
    # Position & Portfolio
    current_position: dict
    account_value: float
    buying_power: float
    daily_pnl: float
    daily_trades: int
    max_drawdown_today: float
    
    # Decision
    final_action: Literal["BUY", "SELL", "HOLD"]
    confidence_score: float  # 0 to 1
    position_size: int
    stop_loss_price: Optional[float]
    take_profit_price: Optional[float]
    reasoning: str
    
    # Execution
    order_id: Optional[str]
    execution_status: str
    slippage: Optional[float]
    
    # Routing
    next: str
    agent_messages: Annotated[List[dict], operator.add]
    error: Optional[str]
    risk_approved: bool
