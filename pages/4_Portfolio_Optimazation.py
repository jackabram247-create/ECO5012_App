##4_Portfolio_Optimization.py

import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Portfolio Optimization — Markowitz Efficient Frontier")

tickers = st.multiselect(
    "Select tickers",
    ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"],
    default=["AAPL", "MSFT", "TSLA"]
)

start = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end   = st.date_input("End Date")

if len(tickers) < 2:
    st.warning("Please select at least two assets.")
else:
    prices = yf.download(tickers, start=start, end=end)["Close"]
    returns = prices.pct_change().dropna()

    # Random portfolios
    n_portfolios = 3000
    results = np.zeros((3, n_portfolios))

    for i in range(n_portfolios):
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)

        portfolio_return = np.sum(weights * returns.mean() * 252)
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*252, weights)))

        results[0, i] = portfolio_vol
        results[1, i] = portfolio_return
        results[2, i] = portfolio_return / portfolio_vol

    fig, ax = plt.subplots()
    scatter = ax.scatter(results[0, :], results[1, :], c=results[2, :])
    ax.set_title("Efficient Frontier")
    ax.set_xlabel("Risk (Volatility)")
    ax.set_ylabel("Expected Return")
    st.pyplot(fig)
