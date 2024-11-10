import pandas as pd
from .base_strategy import BaseStrategy

class BollingerBandStrategy(BaseStrategy):
    def __init__(self, data, capital, investment_style="Moderate"):
        super().__init__(data, capital)
        self.investment_style = investment_style
        self.window, self.num_std_dev = self.get_style_parameters()

    def get_style_parameters(self):
        """Determine parameters based on investment style."""
        if self.investment_style == "Aggressive":
            # Shorter window, smaller threshold for aggressive trading
            return 14, 1.5
        elif self.investment_style == "Moderate":
            # Standard settings for moderate trading
            return 20, 2
        elif self.investment_style == "Passive":
            # Longer window, wider threshold for infrequent trading
            return 30, 2.5
        else:
            raise ValueError("Invalid investment style. Choose from 'Aggressive', 'Moderate', or 'Passive'.")

    def generate_signals(self):
        """Calculate Bollinger Bands and generate buy/sell signals based on investment style."""
        # Calculate the rolling mean and standard deviation for Bollinger Bands
        self.data['MA'] = self.data['Close'].rolling(window=self.window).mean()
        self.data['STD'] = self.data['Close'].rolling(window=self.window).std()
        self.data['Upper'] = self.data['MA'] + (self.num_std_dev * self.data['STD'])
        self.data['Lower'] = self.data['MA'] - (self.num_std_dev * self.data['STD'])

        # Generate signals: 1 for buy, -1 for sell, 0 for hold
        self.data['Signal'] = 0  # Default hold signal
        self.data.loc[self.data['Close'] < self.data['Lower'], 'Signal'] = 1  # Buy signal
        self.data.loc[self.data['Close'] > self.data['Upper'], 'Signal'] = -1  # Sell signal

        # Fill NaN values with hold (0)
        self.data['Signal'].fillna(0, inplace=True)

        return self.data['Signal']

    