def calculate_roi(initial_capital, final_capital):
    """Calculate Return on Investment (ROI)."""
    return (final_capital - initial_capital) / initial_capital

def calculate_sharpe_ratio(returns, risk_free_rate=0):
    """Calculate the Sharpe ratio given returns and a risk-free rate."""
    excess_returns = returns - risk_free_rate
    return excess_returns.mean() / excess_returns.std()
