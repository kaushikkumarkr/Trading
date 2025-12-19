import unittest
import asyncio
from trading_system.mcp.alpaca_client import AlpacaMCPClient
from trading_system.mcp.news_client import NewsMCPClient

class TestMCPClients(unittest.TestCase):
    def test_alpaca_init(self):
        client = AlpacaMCPClient(mcp_url="http://mock")
        self.assertIsNotNone(client)
        
    def test_news_init(self):
        client = NewsMCPClient()
        self.assertIsNotNone(client)

if __name__ == '__main__':
    unittest.main()
