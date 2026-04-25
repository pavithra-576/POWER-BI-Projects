from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()

driver.get("https://finance.yahoo.com/markets/stocks/most-active/")
time.sleep(5)

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

data = []

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    row_data = [col.text for col in cols]

    print(row_data)  # debug

    if len(row_data) >= 7:
        symbol = row_data[0]
        name = row_data[1]
        price = row_data[3]      # ✅ FIXED
        change = row_data[4]
        percent = row_data[5]
        volume = row_data[6]

        # ✅ NOW THIS WILL WORK
        if price != "" and "%" in percent:
            data.append([symbol, name, price, change, percent, volume])

driver.quit()

df = pd.DataFrame(data, columns=["Symbol", "Name", "Price", "Change", "% Change", "Volume"])

print("\n✅ FINAL DATA:")
print(df.head())
print("Total rows scraped:", len(df))

df.to_csv("selenium_stock_data.csv", index=False)
