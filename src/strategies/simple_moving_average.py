import pandas as pd
from .base_strategy import BaseStrategy

class SMAStrategy(BaseStrategy):
    def __init__(self, data, capital, investment_style="Moderate"):
        super().__init__(data, capital)
        self.investment_style = investment_style
        self.short_window, self.long_window = self.get_style_parameters()

    def get_style_parameters(self):
        """Determine parameters based on investment style."""
        if self.investment_style == "Aggressive":
            # Shorter windows for aggressive trading
            return 20, 50
        elif self.investment_style == "Moderate":
            # Medium windows for moderate trading
            return 50, 200
        elif self.investment_style == "Passive":
            # Longer windows for passive trading
            return 100, 300
        else:
            raise ValueError("Invalid investment style. Choose from 'Aggressive', 'Moderate', or 'Passive'.")

    def generate_signals(self):
        """Generate buy/sell signals based on SMA crossover strategy."""
        # Calculate the short-term and long-term moving averages
        self.data['SMA_Short'] = self.data['Close'].rolling(window=self.short_window).mean()
        self.data['SMA_Long'] = self.data['Close'].rolling(window=self.long_window).mean()

        # Generate signals: 1 for buy, -1 for sell, 0 for hold
        self.data['Signal'] = 0  # Default hold signal
        self.data.loc[self.data['SMA_Short'] > self.data['SMA_Long'], 'Signal'] = 1  # Buy signal
        self.data.loc[self.data['SMA_Short'] < self.data['SMA_Long'], 'Signal'] = -1  # Sell signal

        # Fill NaN values with hold (0)
        self.data['Signal'].fillna(0, inplace=True)

        return self.data['Signal']
