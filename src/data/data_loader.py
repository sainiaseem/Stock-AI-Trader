# import pandas as pd

# def load_data(file_path):
#     """Load and preprocess stock data from a CSV file."""
#     data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
#     data = data.dropna()  # Remove missing values
#     return data
import pandas as pd
import yfinance as yf
import os

# Function to load and preprocess stock data from a CSV file
def load_data(file_path=None, symbols=None, country=None):
    """Load and preprocess stock data either from a CSV file or Yahoo Finance."""
    
    # Load CSV if file path is provided
    if file_path:
        data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
        data = data.dropna()  # Remove missing values
        return data
    
    # If symbols and country are provided, fetch stock data from Yahoo Finance
    if symbols and country:
        # Directory to store the CSV files
        output_dir = f'data/{country.lower()}_stock_data'
        os.makedirs(output_dir, exist_ok=True)
        
        all_data = pd.DataFrame()

        # Fetch data for each symbol
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                historical_data = stock.history(period="10y")
                historical_data['Symbol'] = symbol  # Add symbol as a column to identify stock
                
                # Fetch stock details (additional attributes)
                stock_info = stock.info
                for key in ['marketCap', 'priceToBook', 'pegRatio', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow']:
                    if key in stock_info:
                        historical_data[key] = stock_info[key]

                all_data = pd.concat([all_data, historical_data], axis=0)
                
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")

        # Save combined data to a CSV file
        file_name = os.path.join(output_dir, f"combined_data_{country}.csv")
        all_data.to_csv(file_name)
        return all_data

    # Return empty DataFrame if no valid input
    return pd.DataFrame()
