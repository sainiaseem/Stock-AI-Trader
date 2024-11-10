class Backtester:
    def __init__(self, data, strategy, capital):
        self.data = data
        self.strategy = strategy(data, capital)
        self.capital = capital
        self.holdings = 0
        self.cash = capital
        self.positions = []

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
        """Calculate and return the final portfolio value."""
        print("Data:", self.data)  # Print data for debugging
        print("Columns:", self.data.columns)  # Print column names for debugging

        if len(self.data) == 0:
            raise ValueError("Data is empty. Please check the data loading process.")
        
        # Ensure the 'Close' column exists
        if 'Close' not in self.data.columns:
            raise ValueError("The 'Close' column is missing in the data. Please ensure the dataset includes 'Close' prices.")

        # Calculate portfolio value
        portfolio_value = self.cash + (self.holdings * self.data.iloc[-1]['Close'])
        return portfolio_value, self.positions
