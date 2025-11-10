import requests
import time
import csv
import os
from datetime import datetime
from config import COINS, BASE_URL, DAYS

def fetch_coin_history(coin_id, days):
    """Fetch historical price data for a coin from CoinGecko API"""
    endpoint = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # Raise exception for bad status codes
    return response.json()

def save_to_csv(coin_symbol, prices_data):
    """Save price data to CSV file"""
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    filename = os.path.join(data_dir, f"{coin_symbol}_history.csv")

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "price"])

        # Each item in prices is [timestamp_ms, price]
        for timestamp_ms, price in prices_data:
            # Convert timestamp from milliseconds to datetime
            date = datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([date, price])

    return len(prices_data)

def main():
    """Fetch and save historical price data for all coins"""
    for coin_symbol, coin_id in COINS.items():
        try:
            print(f"Fetching {coin_symbol}...")

            # Fetch data from CoinGecko
            data = fetch_coin_history(coin_id, DAYS)
            prices = data.get("prices", [])

            # Save to CSV
            num_records = save_to_csv(coin_symbol, prices)
            print(f"[OK] Saved {num_records} records to {coin_symbol}_history.csv")

            # Delay to respect rate limits (2 seconds between requests)
            time.sleep(2)

        except Exception as e:
            print(f"[ERROR] Error fetching {coin_symbol}: {str(e)}")

if __name__ == "__main__":
    main()
