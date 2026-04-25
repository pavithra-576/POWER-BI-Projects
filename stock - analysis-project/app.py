import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import predict_stock
import numpy as np

st.set_page_config(page_title="Stock Dashboard", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("selenium_stock_data.csv")

# Clean data
df["% Change"] = pd.to_numeric(df["% Change"].astype(str).str.replace('%', ''), errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

df.dropna(inplace=True)

# -----------------------------
# SIDEBAR MENU
# -----------------------------
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Analysis", "Prediction"])

st.sidebar.header("Filters")

search = st.sidebar.text_input("Search Company")
min_change = st.sidebar.slider(
    "Minimum % Change",
    float(df["% Change"].min()),
    float(df["% Change"].max()),
    0.0
)

# Apply filters
filtered_df = df[df["% Change"] >= min_change]

if search:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(search, case=False)]

# -----------------------------
# KPI CARDS
# -----------------------------
st.title("📊 Advanced Stock Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Stocks", len(df))
col2.metric("Highest Gain", f"{df['% Change'].max():.2f}%")
col3.metric("Lowest Loss", f"{df['% Change'].min():.2f}%")

# -----------------------------
# MENU LOGIC
# -----------------------------

# ===== DASHBOARD =====
if menu == "Dashboard":

    st.subheader("📋 Filtered Data")
    st.dataframe(filtered_df)

    # Multi-stock comparison
    st.subheader("📊 Compare Stocks")

    stocks = st.multiselect("Select Stocks", df["Symbol"])

    if stocks:
        compare_df = df[df["Symbol"].isin(stocks)]
        st.dataframe(compare_df)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇️ Download Data",
        data=csv,
        file_name="stock_data.csv",
        mime="text/csv"
    )

# ===== ANALYSIS =====
elif menu == "Analysis":

    option = st.radio("Select View", ["Top Gainers", "Top Losers"])

    if option == "Top Gainers":
        data = df.sort_values("% Change", ascending=False).head(5)
    else:
        data = df.sort_values("% Change").head(5)

    st.dataframe(data)

    # Plot
    plt.figure()
    plt.bar(data["Name"], data["% Change"])
    plt.xticks(rotation=45)
    plt.ylabel("% Change")

    st.pyplot(plt)

    # Recommendation
    st.subheader("🤖 Buy/Sell Recommendation")

    def recommendation(change):
        if change > 3:
            return "Buy 📈"
        elif change < -3:
            return "Sell 📉"
        else:
            return "Hold 🤝"

    df["Recommendation"] = df["% Change"].apply(recommendation)

    st.dataframe(df[["Name", "% Change", "Recommendation"]])

    # Risk Analysis
    st.subheader("⚠️ High Risk Stocks")

    df["Risk"] = df["% Change"].abs()
    high_risk = df.sort_values("Risk", ascending=False).head(5)

    st.dataframe(high_risk)

# ===== PREDICTION =====
elif menu == "Prediction":

    st.subheader("📈 Stock Prediction (ML)")

    ticker = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")

    if st.button("Predict"):
        result = predict_stock(ticker)

        if result:
            data, predictions = result

            st.write("Predicted Prices:", predictions)

            plt.figure()
            plt.plot(data["Close"], label="Actual Price")
            plt.plot(range(len(data), len(data)+len(predictions)), predictions, label="Predicted")
            plt.legend()

            st.pyplot(plt)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("🚀 Built with Streamlit | Stock Analysis Project")
st.subheader("📊 Live Stock Chart")

live_ticker = st.text_input("Enter ticker for live chart", "AAPL")

st.write("Live Chart Preview:")
from newsapi import NewsApiClient
from textblob import TextBlob

st.subheader("📰 Stock News & Sentiment")

api_key = "YOUR_API_KEY"   # get from newsapi.org
newsapi = NewsApiClient(api_key=api_key)

company = st.text_input("Enter company for news", "Apple")

if st.button("Get News"):
    articles = newsapi.get_everything(q=company, language='en', page_size=5)

    for article in articles["articles"]:
        title = article["title"]
        sentiment = TextBlob(title).sentiment.polarity

        if sentiment > 0:
            result = "Positive 😊"
        elif sentiment < 0:
            result = "Negative 😟"
        else:
            result = "Neutral 😐"

        st.write(f"📰 {title}")
        st.write(f"Sentiment: {result}")
        st.write("---")
