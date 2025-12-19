# Multi-Agent AI Trading System

A production-ready algorithmic trading system using LangGraph, LangChain, Alpaca, and Lumibot.

## Architecture

- **Multi-Agent System**: Logic distributed across specialized agents (Technical, Sentiment, Macro, Strategist, Risk, Executor).
- **LangGraph**: Orchestrates the workflow and state management.
- **Gemini 2.0 Flash**: Synthesizes signals and makes high-level decisions.
- **Alpaca**: Used for market data and trade execution (Paper Trading by default).
- **Redis**: Persistent state checkpointer.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
   Required keys: `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `GOOGLE_API_KEY`.

3. **Run using Docker**
   ```bash
   docker-compose up --build
   ```

4. **Run Locally**
   Start Redis first, then:
   ```bash
   python -m trading_system.main
   ```

## Folder Structure
- `agents/`: Individual agent logic.
- `utils/`: Helpers for data, backtesting, and safety.
- `graph.py`: The LangGraph workflow definition.
- `state.py`: Global state schema.

## Safety
- **Circuit Breaker**: Halts trading on high vol or massive losses.
- **Risk Agent**: Validates every trade before execution.
- **Paper Trading**: Enabled by default.
