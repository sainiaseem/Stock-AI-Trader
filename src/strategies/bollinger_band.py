import pandas as pd
from .base_strategy import BaseStrategy

class BollingerBandStrategy(BaseStrategy):
    def __init__(self, data, capital, window=20, num_std_dev=2):
        super().__init__(data, capital)
        self.window = window
        self.num_std_dev = num_std_dev

    def generate_signals(self):
        """Calculate Bollinger Bands and generate buy/sell signals."""
        self.data['MA'] = self.data['Close'].rolling(self.window).mean()
        self.data['Upper'] = self.data['MA'] + self.num_std_dev * self.data['Close'].rolling(self.window).std()
        self.data['Lower'] = self.data['MA'] - self.num_std_dev * self.data['Close'].rolling(self.window).std()

        self.data['Signal'] = 0  # Neutral by default
        self.data.loc[self.data['Close'] < self.data['Lower'], 'Signal'] = 1  # Buy
        self.data.loc[self.data['Close'] > self.data['Upper'], 'Signal'] = -1  # Sell

        return self.data['Signal']
