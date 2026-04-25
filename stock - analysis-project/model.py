import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_stock(ticker="AAPL", days=5):
    # Fetch real stock data
    data = yf.download(ticker, period="6mo")

    if data.empty:
        print("❌ No data found")
        return None

    data = data.reset_index()

    # Use closing price
    data["Day"] = np.arange(len(data))

    X = data[["Day"]]
    y = data["Close"]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future days
    future_days = np.arange(len(data), len(data) + days).reshape(-1, 1)
    predictions = model.predict(future_days)

    return data, predictions
