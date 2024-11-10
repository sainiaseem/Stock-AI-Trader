import pandas as pd
from .base_strategy import BaseStrategy

class VWAPStrategy(BaseStrategy):
    def __init__(self, data, capital, investment_style="Moderate"):
        super().__init__(data, capital)
        self.investment_style = investment_style
        self.vwap_window = self.get_vwap_window()

    def get_vwap_window(self):
        """Determine VWAP window based on investment style."""
        if self.investment_style == "Aggressive":
            return 30
        elif self.investment_style == "Moderate":
            return 50
        elif self.investment_style == "Passive":
            return 100
        else:
            raise ValueError("Invalid investment style. Choose from 'Aggressive', 'Moderate', or 'Passive'.")

    def generate_signals(self):
        """Generate buy/sell signals based on VWAP strategy."""
        self.data['VWAP'] = (self.data['Close'] * self.data['Volume']).rolling(window=self.vwap_window).sum() / self.data['Volume'].rolling(window=self.vwap_window).sum()

        self.data['Signal'] = 0
        self.data.loc[self.data['Close'] > self.data['VWAP'], 'Signal'] = 1  # Buy signal
        self.data.loc[self.data['Close'] < self.data['VWAP'], 'Signal'] = -1  # Sell signal

        self.data['Signal'].fillna(0, inplace=True)

        return self.data['Signal']
