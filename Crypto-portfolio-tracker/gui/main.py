import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv
import os

class CryptoPortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Portfolio Tracker")
        self.root.geometry("900x700")
        self.data_dir = "data"
        self.wallets = {}
        self.current_prices = {}
        self.load_wallets()
        self.load_prices()
        self.create_widgets()

    def load_wallets(self):
        try:
            with open(os.path.join(self.data_dir, "wallet_balances.json"), 'r') as f:
                self.wallets = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load wallets: {e}")

    def load_prices(self):
        for coin in ["BTC", "ETH", "SOL", "XRP"]:
            try:
                with open(os.path.join(self.data_dir, f"{coin}_history.csv"), 'r') as f:
                    rows = list(csv.DictReader(f))
                    self.current_prices[coin] = float(rows[-1]['price']) if rows else 0.0
            except:
                self.current_prices[coin] = 0.0

    def create_widgets(self):
        # Top section - Wallet Selection
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        tk.Label(top_frame, text="Select Wallet:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.wallet_combo = ttk.Combobox(top_frame, values=list(self.wallets.keys()), width=50)
        self.wallet_combo.pack(side=tk.LEFT, padx=5)
        if self.wallets:
            self.wallet_combo.current(0)
        tk.Button(top_frame, text="Load Portfolio", command=self.load_portfolio).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Refresh Data", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        # Middle section - Three panels
        middle_frame = tk.Frame(self.root, padx=10, pady=10)
        middle_frame.pack(fill=tk.BOTH, expand=True)
        # Create three panels with labels
        panels = [("Holdings", "0.0000"), ("Live Prices", "${:,.2f}"), ("Total Value", "$0.00")]
        self.holdings_labels, self.price_labels, self.value_labels = {}, {}, {}
        label_dicts = [self.holdings_labels, self.price_labels, self.value_labels]
        for col, (title, fmt) in enumerate(panels):
            frame = tk.LabelFrame(middle_frame, text=title, font=("Arial", 12, "bold"), padx=10, pady=10)
            frame.grid(row=0, column=col, sticky="nsew", padx=5)
            middle_frame.columnconfigure(col, weight=1)
            for coin in ["BTC", "ETH", "SOL", "XRP"]:
                if col == 1:  # Live Prices
                    text = f"{coin}: ${self.current_prices.get(coin, 0.0):,.2f}"
                else:
                    text = f"{coin}: {fmt}" if col == 0 else f"{coin}: $0.00"
                lbl = tk.Label(frame, text=text, font=("Arial", 10))
                lbl.pack(anchor="w", pady=5)
                label_dicts[col][coin] = lbl
            if col == 2:  # Add total label to Value panel
                self.total_label = tk.Label(frame, text="Total: $0.00", font=("Arial", 12, "bold"), fg="green")
                self.total_label.pack(anchor="w", pady=10)
        # Bottom section - Forecasts (two columns)
        bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        bottom_frame.pack(fill=tk.BOTH, expand=True)

        # BTC Price Forecast
        forecast_frame = tk.LabelFrame(bottom_frame, text="BTC Price Forecast (Next 7 Days)",
                                       font=("Arial", 12, "bold"), padx=10, pady=10)
        forecast_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        self.forecast_text = tk.Text(forecast_frame, height=10, font=("Arial", 10))
        self.forecast_text.pack(fill=tk.BOTH, expand=True)
        self.load_forecast()

        # Portfolio Value Forecast
        portfolio_forecast_frame = tk.LabelFrame(bottom_frame, text="Portfolio Value Forecast (Next 7 Days)",
                                                 font=("Arial", 12, "bold"), padx=10, pady=10)
        portfolio_forecast_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        self.portfolio_forecast_text = tk.Text(portfolio_forecast_frame, height=10, font=("Arial", 10))
        self.portfolio_forecast_text.pack(fill=tk.BOTH, expand=True)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)

    def load_portfolio(self):
        selected = self.wallet_combo.get()
        if not selected or selected not in self.wallets:
            messagebox.showwarning("Warning", "Please select a valid wallet")
            return
        holdings = self.wallets[selected]
        total_value = 0.0
        for coin in ["BTC", "ETH", "SOL", "XRP"]:
            amount = holdings.get(coin.lower(), 0.0)
            price = self.current_prices.get(coin, 0.0)
            value = amount * price
            total_value += value
            self.holdings_labels[coin].config(text=f"{coin}: {amount:.4f}")
            self.value_labels[coin].config(text=f"{coin}: ${value:,.2f}")
        self.total_label.config(text=f"Total: ${total_value:,.2f}")
        self.load_portfolio_forecast()

    def refresh_data(self):
        self.load_wallets()
        self.load_prices()
        self.load_forecast()
        self.load_portfolio_forecast()
        for coin in ["BTC", "ETH", "SOL", "XRP"]:
            self.price_labels[coin].config(text=f"{coin}: ${self.current_prices.get(coin, 0.0):,.2f}")
        messagebox.showinfo("Success", "Data refreshed successfully!")

    def load_forecast(self):
        try:
            with open(os.path.join(self.data_dir, "forecast_output.csv"), 'r') as f:
                self.forecast_text.delete(1.0, tk.END)
                for row in csv.DictReader(f):
                    self.forecast_text.insert(tk.END, f"Day {row['day']}: ${float(row['predicted_price']):,.2f}\n")
        except Exception as e:
            self.forecast_text.delete(1.0, tk.END)
            self.forecast_text.insert(tk.END, f"Forecast not available: {e}")

    def load_portfolio_forecast(self):
        try:
            # Get currently selected wallet
            selected = self.wallet_combo.get()
            if not selected or selected not in self.wallets:
                self.portfolio_forecast_text.delete(1.0, tk.END)
                self.portfolio_forecast_text.insert(tk.END, "Please select a wallet first")
                return

            # Get holdings for selected wallet
            holdings = self.wallets[selected]
            holdings_dict = {
                "BTC": holdings.get("btc", 0.0),
                "ETH": holdings.get("eth", 0.0),
                "SOL": holdings.get("sol", 0.0),
                "XRP": holdings.get("xrp", 0.0)
            }

            # Load forecast data for each coin
            coins = ["BTC", "ETH", "SOL", "XRP"]
            forecasts = {}
            for coin in coins:
                forecast_file = os.path.join(self.data_dir, f"{coin}_forecast.csv")
                with open(forecast_file, 'r') as f:
                    forecasts[coin] = {int(row['day']): float(row['predicted_price'])
                                      for row in csv.DictReader(f)}

            # Calculate portfolio value for each day (1-7)
            portfolio_values = []
            for day in range(1, 8):
                total_value = sum(holdings_dict[coin] * forecasts[coin][day] for coin in coins)
                portfolio_values.append((day, total_value))

            # Display results
            self.portfolio_forecast_text.delete(1.0, tk.END)
            if portfolio_values:
                day1_value = portfolio_values[0][1]
                day7_value = portfolio_values[-1][1]
                percent_change = ((day7_value - day1_value) / day1_value) * 100

                # Display each day's forecast
                for day, value in portfolio_values:
                    self.portfolio_forecast_text.insert(tk.END, f"Day {day}: ${value:,.2f}\n")

                # Display percent change with color coding
                change_text = f"\nChange: {percent_change:+.2f}% over 7 days"
                change_color = "green" if percent_change >= 0 else "red"

                # Configure tag for colored text
                self.portfolio_forecast_text.tag_config("change_color", foreground=change_color, font=("Arial", 10, "bold"))

                # Insert colored change text
                self.portfolio_forecast_text.insert(tk.END, change_text, "change_color")
        except Exception as e:
            self.portfolio_forecast_text.delete(1.0, tk.END)
            self.portfolio_forecast_text.insert(tk.END, f"Portfolio forecast not available: {e}")

def main():
    root = tk.Tk()
    app = CryptoPortfolioApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
