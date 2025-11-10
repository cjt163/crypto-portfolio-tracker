from brownie import PortfolioTracker, accounts
import os

def main():
    """Deploy PortfolioTracker contract and save address to file"""
    try:
        # Get deployer account (first account from local development network)
        deployer = accounts[0]
        print(f"Deploying from account: {deployer.address}")

        # Deploy the PortfolioTracker contract
        print("Deploying PortfolioTracker contract...")
        portfolio_tracker = PortfolioTracker.deploy({'from': deployer})

        # Get the deployed contract address
        contract_address = portfolio_tracker.address
        print(f"[OK] PortfolioTracker deployed successfully at: {contract_address}")

        # Save contract address to data/contract_address.txt
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)  # Create data directory if it doesn't exist

        with open(os.path.join(data_dir, "contract_address.txt"), "w") as f:
            f.write(contract_address)

        print(f"[OK] Contract address saved to {data_dir}/contract_address.txt")

    except Exception as e:
        print(f"[ERROR] Deployment failed: {str(e)}")
        raise
