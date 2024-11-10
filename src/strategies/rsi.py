import pandas as pd
from .base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    def __init__(self, data, capital, investment_style="Moderate"):
        super().__init__(data, capital)
        self.investment_style = investment_style
        self.rsi_window = self.get_rsi_window()

    def get_rsi_window(self):
        """Determine RSI window based on investment style."""
        if self.investment_style == "Aggressive":
            return 7
        elif self.investment_style == "Moderate":
            return 14
        elif self.investment_style == "Passive":
            return 21
        else:
            raise ValueError("Invalid investment style. Choose from 'Aggressive', 'Moderate', or 'Passive'.")

    def calculate_rsi(self):
        """Calculate the Relative Strength Index (RSI)."""
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_window).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signals(self):
        """Generate buy/sell signals based on RSI strategy."""
        self.data['RSI'] = self.calculate_rsi()

        self.data['Signal'] = 0
        self.data.loc[self.data['RSI'] < 30, 'Signal'] = 1  # Buy signal (Oversold)
        self.data.loc[self.data['RSI'] > 70, 'Signal'] = -1  # Sell signal (Overbought)

        self.data['Signal'].fillna(0, inplace=True)

        return self.data['Signal']
