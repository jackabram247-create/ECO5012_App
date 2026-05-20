# 1_Advanced_Dashboard.py

import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 Advanced Stock Dashboard")

# Sidebar inputs
tickers = st.sidebar.multiselect(
    "Choose one or more stock tickers",
    ["AAPL", "TSLA", "MSFT", "AMZN", "NVDA"],
    default=["AAPL"]
)

start = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end   = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetch data
if tickers:
    data = yf.download(tickers, start=start, end=end)

    st.subheader("Closing Price Chart")
    st.line_chart(data["Close"])

    st.subheader("Returns")
    returns = data["Close"].pct_change()
    st.line_chart(returns)

    st.subheader("Summary Statistics")
    st.write(data.describe())
else:
    st.warning("Please select at least one ticker.")
