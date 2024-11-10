from datetime import datetime

class Backtester:
    def __init__(self, data, strategy_class, capital, start_date, end_date, management_style):
        tz = data.index.tz
        if tz is not None:
            self.start_date = datetime.combine(start_date, datetime.min.time()).astimezone(tz)
            self.end_date = datetime.combine(end_date, datetime.min.time()).astimezone(tz)
        else:
            self.start_date = datetime.combine(start_date, datetime.min.time())
            self.end_date = datetime.combine(end_date, datetime.min.time())

        self.data = data[(data.index >= self.start_date) & (data.index <= self.end_date)]
        self.strategy = strategy_class(self.data, capital, investment_style=management_style)  # Corrected to pass the class, not instance
        self.capital = capital
        self.holdings = 0
        self.cash = capital
        self.positions = []
        self.management_style = management_style

    def run_backtest(self):
        """Run backtest using the selected strategy and management style."""
        signals = self.strategy.generate_signals()

        # Define style-specific parameters
        if self.management_style == 'aggressive':
            trade_fraction = 1.0  # Use all available cash per trade
            min_signal_strength = 0  # Accept any signal
        elif self.management_style == 'moderate':
            trade_fraction = 0.5  # Use half of available cash per trade
            min_signal_strength = 0.5  # Accept moderate to strong signals
        else:  # Passive
            trade_fraction = 0.25  # Use a quarter of available cash per trade
            min_signal_strength = 1.0  # Only accept the strongest signals
        print(self.management_style)
        for date, signal in signals.items():
            stock_price = self.data.loc[date, 'Close']

            # Buy signal logic based on the management style and signal strength
            if signal >= min_signal_strength:
                if signal == 1 and self.cash > 0:  # Buy if we have enough cash
                    # Calculate shares based on the available cash
                    shares = int((self.cash * trade_fraction) // stock_price)
                    
                    if shares > 0:
                        self.holdings += shares
                        self.cash -= shares * stock_price
                        self.positions.append((date, 'Buy', shares, stock_price))
            elif signal == -1 and self.holdings > 0:  # Sell signal for all styles
                # Sell all holdings
                self.cash += self.holdings * stock_price
                self.positions.append((date, 'Sell', self.holdings, stock_price))
                self.holdings = 0

    def get_results(self):
        """Calculate and return the final portfolio and HODL values."""
        portfolio_value = self.cash + (self.holdings * self.data.iloc[-1]['Close'])
        hodl_value = (self.capital / self.data.iloc[0]['Close']) * self.data.iloc[-1]['Close']
        
        return portfolio_value, hodl_value, self.positions
    