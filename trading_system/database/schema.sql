-- database/schema.sql

-- Trades table
CREATE TABLE IF NOT EXISTS trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(10) NOT NULL,
    side VARCHAR(4) NOT NULL CHECK (side IN ('buy', 'sell')),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    total_value DECIMAL(12, 2) GENERATED ALWAYS AS (quantity * price) STORED,
    order_id VARCHAR(50),
    fill_price DECIMAL(10, 2),
    slippage DECIMAL(5, 4),
    
    -- Strategy data
    technical_score DECIMAL(4, 3),
    sentiment_score DECIMAL(4, 3),
    confidence DECIMAL(4, 3),
    strategy_reasoning TEXT,
    
    -- Risk data
    stop_loss DECIMAL(10, 2),
    take_profit DECIMAL(10, 2),
    position_size_method VARCHAR(20),
    
    -- Timestamps
    signal_time TIMESTAMPTZ,
    execution_time TIMESTAMPTZ DEFAULT NOW(),
    
    -- Status
    status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Portfolio snapshots
CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_date DATE NOT NULL,
    total_value DECIMAL(14, 2) NOT NULL,
    cash DECIMAL(14, 2) NOT NULL,
    positions_value DECIMAL(14, 2) NOT NULL,
    daily_pnl DECIMAL(12, 2),
    daily_pnl_pct DECIMAL(6, 4),
    cumulative_pnl DECIMAL(14, 2),
    max_drawdown DECIMAL(6, 4),
    positions JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(snapshot_date)
);

-- Circuit breaker events
CREATE TABLE IF NOT EXISTS circuit_breaker_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    triggered_at TIMESTAMPTZ DEFAULT NOW(),
    reason VARCHAR(100) NOT NULL,
    details JSONB,
    reset_at TIMESTAMPTZ,
    reset_by VARCHAR(50)
);

-- Performance metrics (daily)
CREATE TABLE IF NOT EXISTS performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_date DATE NOT NULL,
    total_trades INTEGER,
    winning_trades INTEGER,
    losing_trades INTEGER,
    win_rate DECIMAL(5, 4),
    gross_profit DECIMAL(12, 2),
    gross_loss DECIMAL(12, 2),
    net_profit DECIMAL(12, 2),
    avg_win DECIMAL(10, 2),
    avg_loss DECIMAL(10, 2),
    profit_factor DECIMAL(6, 3),
    sharpe_ratio DECIMAL(6, 3),
    sortino_ratio DECIMAL(6, 3),
    max_drawdown DECIMAL(6, 4),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(metric_date)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol);
CREATE INDEX IF NOT EXISTS idx_trades_execution_time ON trades(execution_time);
CREATE INDEX IF NOT EXISTS idx_trades_status ON trades(status);
CREATE INDEX IF NOT EXISTS idx_snapshots_date ON portfolio_snapshots(snapshot_date);
