#3_Sentiment_Analysis.py

import streamlit as st
import yfinance as yf
import pandas as pd
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

st.title("📰 Sentiment Analysis (News + NLP)")

ticker = st.text_input("Enter stock ticker", "AAPL")

# Scrape news headlines
st.subheader("Latest News Headlines")

url = f"https://finance.yahoo.com/quote/{ticker}"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

headlines = soup.find_all("h3")

news_items = []
for h in headlines[:10]:
    text = h.get_text()
    sentiment = TextBlob(text).sentiment.polarity
    news_items.append({"headline": text, "sentiment": sentiment})

df = pd.DataFrame(news_items)

st.write(df)

avg_sent = df["sentiment"].mean()
st.success(f"Average Sentiment: {avg_sent:.2f}")
