import streamlit as st
from src.data.data_loader import load_data
from src.strategies.bollinger_band import BollingerBandStrategy
from src.backtest.backtester import Backtester
from src.utils.visualizations import plot_stock_data, plot_stock_with_signals

st.title("Backtest Engine")

# Load and display data
file_path = st.file_uploader("Upload NSE Stock Data CSV", type=["csv"])
if file_path is not None:
    data = load_data(file_path)
    st.write("Stock Data", data)

    # User inputs for strategy configuration
    start_date = st.date_input("Start Date", value=data.index.min())
    end_date = st.date_input("End Date", value=data.index.max())
    initial_capital = st.number_input("Initial Capital", min_value=1000, step=1000)
    management_style = st.selectbox("Investment Style", ["Aggressive", "Moderate", "Passive"])
    strategy = st.selectbox("Select Strategy", ["Bollinger Band", "Moving Average"])

    # Run backtest
    if st.button("Run Backtest"):
        if strategy == "Bollinger Band":
            backtester = Backtester(data, BollingerBandStrategy, initial_capital, start_date, end_date, management_style)
        
        backtester.run_backtest()
        final_value, hodl_value, positions = backtester.get_results()

        st.write(f"Final Portfolio Value: {final_value}")
        st.write(f"HODL Value: {hodl_value}")
        st.write("Positions", positions)

        # Visualize results
        st.subheader("Initial Stock Data")
        st.plotly_chart(plot_stock_data(data))
        
        st.subheader("Backtest Results with Buy/Sell Signals")
        st.plotly_chart(plot_stock_with_signals(data, positions))

        st.subheader("Profit/Loss on Each Trade")
        profit_loss = [(date, action, shares * price) for date, action, shares, price in positions]
        st.write(profit_loss)
