import matplotlib.pyplot as plt

def plot_stock_data(data):
    """Plot stock data with indicators."""
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price')
    if 'MA' in data.columns:
        plt.plot(data['MA'], label='Moving Average')
    if 'Upper' in data.columns and 'Lower' in data.columns:
        plt.plot(data['Upper'], linestyle='--', color='gray', label='Upper Band')
        plt.plot(data['Lower'], linestyle='--', color='gray', label='Lower Band')
    plt.legend()
    plt.show()
