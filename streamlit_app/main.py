import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.table import Table
from src.data.data_loader import load_data
from src.strategies.bollinger_band import BollingerBandStrategy
from src.strategies.macd import MACDStrategy
from src.strategies.rsi import RSIStrategy
from src.strategies.simple_moving_average import SMAStrategy
from src.strategies.vwap import VWAPStrategy
from src.backtest.backtester import Backtester
from src.utils.visualizations import plot_stock_data, plot_stock_with_signals

# App Title and Description
st.title("Stock Backtesting Engine")
st.markdown("""
This application allows you to backtest stock strategies using historical data. 
You can choose from different strategies and investment styles to simulate your portfolio's performance over a given period.
""")

# Country Selection
st.sidebar.subheader("1. Select Country & Stock Data")
country = st.sidebar.selectbox("Select Country", ["India", "USA", "Japan"])

# Initialize symbols based on country selection
symbols = []

# Handle country-based stock symbols
if country == "India":
    # Stock Exchange Selection
    exchange = st.sidebar.selectbox("Select Stock Exchange", ["NSE", "BSE"])
    if exchange == "NSE":
        symbols = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'HDFC.NS', 'LT.NS', 'KOTAKBANK.NS', 'BAJFINANCE.NS']
    elif exchange == "BSE":
        symbols = ['RELIANCE.BO', 'TCS.BO', 'INFY.BO', 'HDFCBANK.BO', 'ICICIBANK.BO', 'SBIN.BO', 'HDFC.BO', 'LT.BO', 'KOTAKBANK.BO', 'BAJFINANCE.BO']
        
elif country == "USA":
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK-B', 'JNJ', 'V']

elif country == "Japan":
    symbols = ['7203.T', '6758.T', '9432.T', '9984.T', '8306.T', '8058.T', '6861.T', '6971.T', '8035.T', '7267.T']

# Stock Selection
selected_symbol = st.sidebar.selectbox("Select Stocks", symbols,index=0)

# File Upload Option (CSV)
st.sidebar.subheader("2. Upload Data (Optional)")
file_path = st.sidebar.file_uploader("Or upload a CSV file with stock data", type=["csv"])

# Load Data (either from CSV or selected symbols)
data = None
if file_path:
    data = load_data(file_path=file_path)
    st.write("**Uploaded Stock Data:**", data)

elif selected_symbol:
    data = load_data(symbols=[selected_symbol], country=country)
    st.write(f"**Stock Data for {country} - {selected_symbol}:**", data)

# Check if data is available before displaying strategy options
if data is not None and not data.empty:
    # Configuration Inputs
    st.sidebar.subheader("3. Backtest Configuration")
    start_date = st.sidebar.date_input("Start Date", value=data.index.min())
    end_date = st.sidebar.date_input("End Date", value=data.index.max())
    initial_capital = st.sidebar.number_input("Initial Capital", min_value=1000, step=1000)
    management_style = st.sidebar.selectbox("Investment Style", ["Aggressive", "Moderate", "Passive"])
    
    strategy = st.sidebar.selectbox("Select Strategy", ["Bollinger Band","Simple Moving Avg","MACD", "RSI", "VWAP"])
    # strategy = st.sidebar.selectbox("Select Strategy", ["Bollinger Band","Simple Moving Avg"])

    # Run Backtest on Button Click
    if st.sidebar.button("Run Backtest"):
        with st.spinner("Running backtest..."):
            if strategy == "Bollinger Band":
                backtester = Backtester(data, BollingerBandStrategy, initial_capital, start_date, end_date, management_style)
            elif strategy == "MACD":
                backtester = Backtester(data, MACDStrategy, initial_capital, start_date, end_date, management_style)
            elif strategy == "RSI":
                backtester = Backtester(data, RSIStrategy, initial_capital, start_date, end_date, management_style)
            elif strategy == "Simple Moving Avg":
                backtester = Backtester(data, SMAStrategy, initial_capital, start_date, end_date, management_style)
            elif strategy == "VWAP":
                backtester = Backtester(data, VWAPStrategy, initial_capital, start_date, end_date, management_style)

            backtester.run_backtest()

            # Results
            final_value, hodl_value, positions = backtester.get_results()

            # Display Final Portfolio Value with a green color for success
            if final_value > hodl_value:
                st.success(f"**Final Portfolio Value**: {final_value:.2f} (✅ Profit)")
            else:
                st.error(f"**Final Portfolio Value**: {final_value:.2f} (❌ Loss)")

            # Display HODL value (Buy & Hold Strategy) with neutral color
            st.info(f"**HODL Value (Buy & Hold Strategy)**: {hodl_value:.2f}")

            # Display Positions Taken with a table
            if positions:
                st.write("**Positions Taken**:")
                positions_df = pd.DataFrame(positions, columns=["Date", "Action", "Shares", "Price"])
                st.dataframe(positions_df)
            else:
                st.warning("No positions taken during the backtest.")

            # Visualizations
            st.subheader("Visualizations")
            st.write("### Initial Stock Data")
            st.plotly_chart(plot_stock_data(data), use_container_width=True)

            st.write("### Backtest Results with Buy/Sell Signals")
            st.plotly_chart(plot_stock_with_signals(data, positions), use_container_width=True)

            # st.write("### Profit/Loss on Each Trade")
            # profit_loss = [(date, action, shares * price) for date, action, shares, price in positions]
            # st.write(profit_loss)
            profit_loss = []
            cumulative_profit = 0
            for i, (date, action, shares, price) in enumerate(positions):
                # Buy action: no profit/loss yet, just store the cost
                if action == 'Buy':
                    profit_loss.append((date, action, shares, price, 0))  # No P/L for buy
                else:
                    # Sell action: Calculate profit/loss
                    previous_buy = positions[i - 1]  # The previous Buy action
                    buy_price = previous_buy[3]  # Price from the previous Buy action
                    pl = (price - buy_price) * shares  # Profit or Loss
                    cumulative_profit += pl
                    profit_loss.append((date, action, shares, price, pl))

            # Convert profit_loss list into a DataFrame for better display
            profit_loss_df = pd.DataFrame(profit_loss, columns=["Date", "Action", "Shares", "Price", "Profit/Loss"])

            # Plotting the Profit/Loss Cumulative Over Time
            dates = [entry[0] for entry in profit_loss]
            cumulative_pl_values = [sum([entry[4] for entry in profit_loss[:i + 1]]) for i in range(len(profit_loss))]

            # Plot the cumulative profit/loss over time
            plt.figure(figsize=(12, 6))
            plt.plot(dates, cumulative_pl_values, marker='o', color='g' if cumulative_pl_values[-1] >= 0 else 'r')
            plt.title('Cumulative Profit/Loss Over Time', fontsize=14)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Cumulative Profit/Loss ($)', fontsize=12)
            plt.grid(True)

            # Display the plot in Streamlit
            st.pyplot(plt)

            # Display the Profit/Loss table below the chart
            st.write("### Profit/Loss on Each Trade")
            st.dataframe(profit_loss_df)

else:
    st.warning("Please upload a file or select stock symbols to proceed with the backtest.")
