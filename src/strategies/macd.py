import pandas as pd
from .base_strategy import BaseStrategy

class MACDStrategy(BaseStrategy):
    def __init__(self, data, capital, investment_style="Moderate"):
        super().__init__(data, capital)
        self.investment_style = investment_style
        self.short_window, self.long_window, self.signal_window = self.get_macd_parameters()

    def get_macd_parameters(self):
        """Determine MACD parameters based on investment style."""
        if self.investment_style == "Aggressive":
            return 12, 26, 9
        elif self.investment_style == "Moderate":
            return 12, 26, 9
        elif self.investment_style == "Passive":
            return 24, 52, 18
        else:
            raise ValueError("Invalid investment style. Choose from 'Aggressive', 'Moderate', or 'Passive'.")

    def calculate_macd(self):
        """Calculate the MACD line and the signal line."""
        self.data['EMA_Short'] = self.data['Close'].ewm(span=self.short_window, adjust=False).mean()
        self.data['EMA_Long'] = self.data['Close'].ewm(span=self.long_window, adjust=False).mean()

        self.data['MACD'] = self.data['EMA_Short'] - self.data['EMA_Long']
        self.data['Signal_Line'] = self.data['MACD'].ewm(span=self.signal_window, adjust=False).mean()

    def generate_signals(self):
        """Generate buy/sell signals based on MACD strategy."""
        self.calculate_macd()

        self.data['Signal'] = 0
        self.data.loc[self.data['MACD'] > self.data['Signal_Line'], 'Signal'] = 1  # Buy signal
        self.data.loc[self.data['MACD'] < self.data['Signal_Line'], 'Signal'] = -1  # Sell signal

        self.data['Signal'].fillna(0, inplace=True)

        return self.data['Signal']
