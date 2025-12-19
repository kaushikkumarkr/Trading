import unittest
from trading_system.agents.technical_analyst import technical_analyst
from trading_system.agents.macro_analyst import macro_analyst
from trading_system.state import TradingState

class TestAgents(unittest.TestCase):
    def test_technical_analyst_structure(self):
        state = TradingState(ticker="AAPL")
        # Mocking run not easily possible without internet/mocking yfinance
        # Just checking class exists and has run method
        self.assertTrue(hasattr(technical_analyst, 'run'))

    def test_macro_analyst_structure(self):
        self.assertTrue(hasattr(macro_analyst, 'run'))
        
if __name__ == '__main__':
    unittest.main()
