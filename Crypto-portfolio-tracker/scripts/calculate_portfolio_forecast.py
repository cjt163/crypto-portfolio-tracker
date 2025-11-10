import json
import csv
import os

def main():
    data_dir = "data"
    # Load wallet balances (use first wallet)
    with open(os.path.join(data_dir, "wallet_balances.json"), 'r') as f:
        first_wallet = list(json.load(f).values())[0]
    holdings = {
        "BTC": first_wallet.get("btc", 0.0),
        "ETH": first_wallet.get("eth", 0.0),
        "SOL": first_wallet.get("sol", 0.0),
        "XRP": first_wallet.get("xrp", 0.0)
    }
    # Load forecast data for each coin
    coins = ["BTC", "ETH", "SOL", "XRP"]
    forecasts = {}
    for coin in coins:
        with open(os.path.join(data_dir, f"{coin}_forecast.csv"), 'r') as f:
            forecasts[coin] = {int(row['day']): float(row['predicted_price'])
                              for row in csv.DictReader(f)}
    # Calculate portfolio value for each day (1-7)
    portfolio_forecast = []
    for day in range(1, 8):
        total_value = sum(holdings[coin] * forecasts[coin][day] for coin in coins)
        portfolio_forecast.append({"day": day, "total_value": total_value})
    # Save to CSV
    output_file = os.path.join(data_dir, "portfolio_forecast.csv")
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["day", "total_value"])
        writer.writeheader()
        writer.writerows(portfolio_forecast)
    print("[OK] Portfolio forecast calculated for 7 days")

if __name__ == "__main__":
    main()
