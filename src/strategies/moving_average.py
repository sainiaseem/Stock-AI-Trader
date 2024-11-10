from .base_strategy import BaseStrategy

class MovingAverageStrategy(BaseStrategy):
    def __init__(self, data, capital, short_window=50, long_window=200):
        super().__init__(data, capital)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        """Calculate moving averages and generate buy/sell signals."""
        self.data['Short_MA'] = self.data['Close'].rolling(self.short_window).mean()
        self.data['Long_MA'] = self.data['Close'].rolling(self.long_window).mean()

        self.data['Signal'] = 0
        self.data.loc[self.data['Short_MA'] > self.data['Long_MA'], 'Signal'] = 1  # Buy
        self.data.loc[self.data['Short_MA'] < self.data['Long_MA'], 'Signal'] = -1  # Sell

        return self.data['Signal']
