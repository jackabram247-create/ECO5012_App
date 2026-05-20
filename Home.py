import streamlit as st



st.set_page_config(page_title="Module App", initial_sidebar_state="expanded")

st.title("ECO5012B")
st.subheader("Interactive Module Dashboards")

st.markdown("""
Welcome to the interactive support tool for **ECO5012B**. 
Use the sidebar on the left to navigate through the different financial applications.

### Available Tools:
1. **Advanced Dashboard**: Real-time stock data visualization and summary statistics.
2. **Behavioral Finance**: Exploration of Prospect Theory and the Loss Aversion utility curve ($λ$).
3. **Sentiment Analysis**: Scrapes live news headlines and calculates sentiment scores.
4. **Portfolio Optimization**: Visualizes the Markowitz Efficient Frontier using Monte Carlo simulation.

---
**Instructions:**
* Select a tool from the sidebar.
* Adjust parameters (tickers, dates, or coefficients) to see real-time updates.
* For the Sentiment Analysis tool, ensure you have an active internet connection.
""")

st.info("ECO5012B")
