import time
import yfinance as yf
import pandas as pd
import ta
import requests

# 🔧 Config
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def check_di(symbol="BTC-USD", interval="5m"):
    df = yf.download(symbol, period="2d", interval=interval)
    df["+DI"] = ta.trend.adx_pos(df["High"], df["Low"], df["Close"], window=14)
    df["-DI"] = ta.trend.adx_neg(df["High"], df["Low"], df["Close"], window=14)

    latest = df.iloc[-2:]
    prev, curr = latest.iloc[0], latest.iloc[1]

    if prev["+DI"] < prev["-DI"] and curr["+DI"] > curr["-DI"]:
        send_alert(f"🔔 {symbol}: +DI crossed above -DI")
    elif prev["+DI"] > prev["-DI"] and curr["+DI"] < curr["-DI"]:
        send_alert(f"🔔 {symbol}: -DI crossed above +DI")

if __name__ == "__main__":
    while True:
        try:
            check_di("BTC-USD", "5m")  # change symbol if needed
        except Exception as e:
            print("Error:", e)
        time.sleep(300)  # every 5 min
