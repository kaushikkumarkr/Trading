import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load env from parent directory if needed, or assume running in docker with env vars
load_dotenv()

# Config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

st.set_page_config(page_title="🤖 AI Trading Bot Dashboard", layout="wide", page_icon="📈")

# Sidebar
st.sidebar.title("Configuration")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 5, 300, 30)

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing SUPABASE_URL or SUPABASE_KEY environment variables.")
    st.stop()

@st.cache_resource
def init_db():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_db()

st.title("🤖 Adaptive AI Trading System")
st.markdown("### Real-Time Performance & Signals")

# --- Kpi Metric Row ---
col1, col2, col3, col4 = st.columns(4)

# Fetch data function
def fetch_data():
    # 1. Fetch latest Snapshot
    try:
        snap_res = supabase.table("portfolio_snapshots").select("*").order("snapshot_date", desc=True).limit(1).execute()
        snapshot = snap_res.data[0] if snap_res.data else {}
    except Exception as e:
        snapshot = {}
        st.sidebar.error(f"Snapshot Error: {e}")

    # 2. Fetch Recent Trades
    try:
        trades_res = supabase.table("trades").select("*").order("execution_time", desc=True).limit(50).execute()
        trades = trades_res.data if trades_res.data else []
    except Exception as e:
        trades = []
        st.sidebar.error(f"Trades Error: {e}")

    return snapshot, trades

snapshot, trades = fetch_data()

# KPIS
total_val = float(snapshot.get("total_value", 0))
cash_val = float(snapshot.get("cash", 0))
daily_pnl = float(snapshot.get("daily_pnl", 0))
daily_pnl_pct = float(snapshot.get("daily_pnl_pct", 0)) * 100

col1.metric("💰 Total Account Value", f"${total_val:,.2f}", f"${daily_pnl:,.2f}")
col2.metric("💵 Cash Balance", f"${cash_val:,.2f}")
col3.metric("📉 Daily PnL %", f"{daily_pnl_pct:.2f}%", delta_color="normal")
col4.metric("📊 Total Trades (History)", len(trades))

# --- Divider ---
st.markdown("---")

# --- Charts and Tables ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Recent Trades")
    if trades:
        df_trades = pd.DataFrame(trades)
        # Format columns
        display_cols = ["execution_time", "symbol", "side", "quantity", "price", "profit_loss", "strategy_reasoning"]
        # Handle columns that might not ensure existence (e.g. profit_loss not in schema yet? Check schema)
        # Schema has: symbol, side, k quantity, price, total_value... 
        # Wait, 'profit_loss' is not in the schema I reviewed earlier. Let's stick to what's there.
        # Schema: symbol, side, quantity, price, execution_time, strategy_reasoning, confidence
        
        # Cleaner DF
        df_display = df_trades[["execution_time", "symbol", "side", "quantity", "price", "confidence", "strategy_reasoning", "status"]]
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No trades recorded yet.")

with c2:
    st.subheader("Portfolio Composition")
    # Parse positions json from snapshot
    positions_json = snapshot.get("positions", {})
    if positions_json:
        # Example json: {"AAPL": {"qty": 10, "value": 1500}}
        # Need to parse this based on how we save it. 
        # Assuming simple dict for now or empty.
        # If it's a list or dict, prepare for pie chart.
        # For now, let's just make a mock pie chart if empty, or real if data.
        if isinstance(positions_json, dict) and len(positions_json) > 0:
            df_pos = pd.DataFrame([{"Symbol": k, "Value": v.get("market_value", 0)} for k, v in positions_json.items() if isinstance(v, dict)])
            if not df_pos.empty:
                fig = px.pie(df_pos, values="Value", names="Symbol", hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No active positions.")
        else:
            st.write("No active positions.")
    else:
        # Show Cash vs Equity if nothing else
        pass
        
# --- Footer ---
if st.button("Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")
