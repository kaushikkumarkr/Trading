from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed
from ..config import config
import threading
import asyncio

class DataPipeline:
    def __init__(self):
        self.stream = StockDataStream(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY)
        self.latest_bars = {}

    async def start_stream(self):
        # Subscribe to bars
        # Note: 'iex' is usually strictly for paid/pro, 'sip' for pro, 'av'/'iex' might work on free tier depending on plan
        # Using 'iex' as default often works for ensuring some data or modify based on subscription
        try:
             # Basic handler
            async def bar_handler(bar):
                symbol = bar.symbol
                self.latest_bars[symbol] = bar
                print(f"Update: {symbol} @ {bar.close}")

            self.stream.subscribe_bars(bar_handler, *config.TRADING_TICKERS)
            await self.stream._run_forever()
        except Exception as e:
            print(f"Data Stream Error: {e}")

    def get_latest_price(self, ticker: str) -> float:
        bar = self.latest_bars.get(ticker)
        if bar:
            return bar.close
        return 0.0

data_pipeline = DataPipeline()
