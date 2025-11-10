import random
import json
import os

def generate_wallet_address():
    """Generate random wallet address (0x + 40 hex characters)"""
    hex_chars = '0123456789abcdef'
    return '0x' + ''.join(random.choice(hex_chars) for _ in range(40))

def generate_random_holdings():
    """Generate random crypto holdings within specified ranges"""
    return {
        "btc": round(random.uniform(0.1, 5.0), 4),
        "eth": round(random.uniform(1.0, 50.0), 4),
        "sol": round(random.uniform(10.0, 500.0), 4),
        "xrp": round(random.uniform(1000.0, 50000.0), 4)
    }

def main():
    """Generate mock wallets with random holdings and save to JSON"""
    num_wallets = 5
    wallets = {}
    # Generate 5 mock wallets
    for i in range(num_wallets):
        wallets[generate_wallet_address()] = generate_random_holdings()
    # Save to data/wallet_balances.json
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    output_file = os.path.join(data_dir, "wallet_balances.json")
    with open(output_file, "w") as f:
        json.dump(wallets, f, indent=2)
    print(f"[OK] Successfully created {num_wallets} mock wallets")
    print(f"[OK] Wallet balances saved to {output_file}")

if __name__ == "__main__":
    main()
