# Adaptive AI Trading System (FOSS Edition)

A professional-grade, self-optimizing multi-agent trading system built with **Python**, **Docker**, **Supabase**, and **DuckDuckGo**. Designed for 24/7 continuous operation with zero ongoing API costs (excluding trading commissions).

## 🚀 Features

- **Multi-Agent Architecture**:
  - **Strategist**: Makes high-level decisions based on aggregated data.
  - **Quant Researcher**: Self-optimizes technical parameters (RSI, SMA, MACD) using `vectorbt` backtesting.
  - **Sentiment Analyst**: Analyzes news sentiment using `DuckDuckGo` and `FinBERT`.
  - **Risk Manager**: Enforces stop-losses, position sizing, and circuit breakers.
  - **Executor**: Smart order execution via Alpaca (Limit orders in extended hours).

- **FOSS Stack (Free & Open Source)**:
  - **News**: DuckDuckGo (No API Keys).
  - **Database**: Supabase Free Tier (PostgreSQL in Cloud).
  - **Deployment**: Docker Containerized.

- **Advanced capabilities**:
  - **Extended Hours Trading**: Automatic limit order switching.
  - **Continuous Loop**: Runs 24/7 with sleep cycles and error recovery.
  - **Persistence**: Logs every trade to Supabase Cloud.

## 🛠️ Architecture

```mermaid
graph TD
    Market[Market Data] --> Quant[Quant Researcher]
    News[DuckDuckGo] --> Sentiment[Sentiment Analyst]
    DB[(Supabase)] <--> Executor
    Quant --> Strategist
    Sentiment --> Strategist
    Strategist --> Risk[Risk Manager]
    Risk --> Executor[Executor Agent]
    Executor --> Alpaca[Alpaca API]
```

## 📦 Installation

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Supabase Account (Free)
- Alpaca Paper Trading Account

### 1. Clone & Setup
```bash
git clone https://github.com/kaushikkumarkr/Trading.git
cd Trading
cp trading_system/.env.example trading_system/.env
```

### 2. Configure Environment
Edit `trading_system/.env` with your keys:
```bash
# Alpaca (Trading)
ALPACA_API_KEY=...
ALPACA_SECRET_KEY=...

# Google (LLM Brain)
GOOGLE_API_KEY=...

# Supabase (Database)
SUPABASE_URL=...
SUPABASE_KEY=...
```

### 3. Initialize Database
Copy the SQL from `trading_system/database/schema.sql` and run it in your Supabase SQL Editor.

## 🏃‍♂️ Usage

### Docker (Recommended)
```bash
docker-compose up --build
```

### Local (Dev)
```bash
python -m venv venv
source venv/bin/activate
pip install -r trading_system/requirements.txt
python -m trading_system.main
```

## 🧪 Verification
The system includes verification scripts to test all components:
- `verify_alpaca.py`: Test broker connection.
- `verify_google.py`: Test LLM connection.
- `verify_supabase.py`: Test database write/read.

## 📝 License
MIT
