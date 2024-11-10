import pandas as pd

def load_data(file_path):
    """Load and preprocess stock data from a CSV file."""
    data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    data = data.dropna()  # Remove missing values
    return data
