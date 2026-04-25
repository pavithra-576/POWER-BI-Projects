import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("selenium_stock_data.csv")

print("Original Data:")
print(df.head())

# -----------------------------
# CLEANING (SAFE)
# -----------------------------

# Convert Price
df["Price"] = pd.to_numeric(
    df["Price"].astype(str).str.replace(",", ""),
    errors="coerce"
)

# Convert Change
df["Change"] = pd.to_numeric(
    df["Change"].astype(str).str.replace(",", ""),
    errors="coerce"
)

# Convert % Change
df["% Change"] = pd.to_numeric(
    df["% Change"].astype(str).str.replace("%", "", regex=False),
    errors="coerce"
)

# Convert Volume
def convert_volume(v):
    v = str(v)

    try:
        if "M" in v:
            return float(v.replace("M", "").replace(",", "")) * 1e6
        elif "B" in v:
            return float(v.replace("B", "").replace(",", "")) * 1e9
        elif "K" in v:
            return float(v.replace("K", "").replace(",", "")) * 1e3
        else:
            return float(v.replace(",", ""))
    except:
        return None

df["Volume"] = df["Volume"].apply(convert_volume)

# Drop only important missing values
df = df.dropna(subset=["Price", "% Change", "Volume"])

print("\nCleaned Data:")
print(df.head())
print("Total rows after cleaning:", len(df))

# Stop if empty
if df.empty:
    print("❌ No valid data available after cleaning")
    exit()

# -----------------------------
# ANALYSIS
# -----------------------------

# Top Gainers
top_gainers = df.sort_values("% Change", ascending=False).head(5)

# Top Losers
top_losers = df.sort_values("% Change").head(5)

# Volatility
df["Volatility"] = df["% Change"].abs()
volatile = df.sort_values("Volatility", ascending=False).head(5)

# Most Active
active = df.sort_values("Volume", ascending=False).head(5)

# -----------------------------
# VISUALIZATION
# -----------------------------

# Top Gainers
top_gainers.plot(x="Name", y="% Change", kind="bar", title="Top Gainers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Top Losers
top_losers.plot(x="Name", y="% Change", kind="bar", title="Top Losers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Volatility
volatile.plot(x="Name", y="Volatility", kind="bar", title="Most Volatile Stocks")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Most Active
active.plot(x="Name", y="Volume", kind="bar", title="Most Active Stocks")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n✅ Analysis Completed Successfully 🎉")
