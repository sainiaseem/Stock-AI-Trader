from datetime import datetime, timezone

class Backtester:
    def __init__(self, data, strategy, capital, start_date, end_date, management_style):
        # Get the timezone from the data's index, if any
        tz = data.index.tz

        # Convert start_date and end_date to timezone-aware if tz is not None
        if tz is not None:
            self.start_date = datetime.combine(start_date, datetime.min.time()).astimezone(tz)
            self.end_date = datetime.combine(end_date, datetime.min.time()).astimezone(tz)
        else:
            self.start_date = datetime.combine(start_date, datetime.min.time())
            self.end_date = datetime.combine(end_date, datetime.min.time())
        
        # Filter data once using the timezone-aware start and end dates
        self.data = data[(data.index >= self.start_date) & (data.index <= self.end_date)]
        
        # Initialize other attributes
        self.strategy = strategy(self.data, capital)
        self.capital = capital
        self.holdings = 0
        self.cash = capital
        self.positions = []
        self.management_style = management_style

    def run_backtest(self):
        """Run backtest using the selected strategy and track positions."""
        signals = self.strategy.generate_signals()

        for date, signal in signals.items():
            if signal == 1:  # Buy
                shares = self.cash // self.data.loc[date, 'Close']
                self.holdings += shares
                self.cash -= shares * self.data.loc[date, 'Close']
                self.positions.append((date, 'Buy', shares, self.data.loc[date, 'Close']))
            elif signal == -1 and self.holdings > 0:  # Sell
                self.cash += self.holdings * self.data.loc[date, 'Close']
                self.positions.append((date, 'Sell', self.holdings, self.data.loc[date, 'Close']))
                self.holdings = 0

    def get_results(self):
        """Calculate and return the final portfolio and HODL values."""
        portfolio_value = self.cash + (self.holdings * self.data.iloc[-1]['Close'])
        hodl_value = (self.capital / self.data.iloc[0]['Close']) * self.data.iloc[-1]['Close']
        
        return portfolio_value, hodl_value, self.positions
