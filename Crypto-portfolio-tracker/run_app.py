"""
Crypto Portfolio Tracker - Main Application
"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

def run_step(name, command):
    """Run a pipeline step"""
    print(f"\n{'='*60}")
    print(f"{name}")
    print('='*60)
    
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"⚠ {name} failed but continuing...")
    else:
        print(f"✓ {name} completed")
    
    return result.returncode == 0

def main():
    print("="*60)
    print("CRYPTO PORTFOLIO TRACKER")
    print("="*60)
    
    steps = [
        ("1. Generate Mock Wallets", f"{sys.executable} scripts/generate_mock_wallets.py"),
        ("2. Fetch Crypto Prices", f"{sys.executable} api/fetch_prices.py"),
        ("3. Run Julia ML Pipeline", f"{sys.executable} scripts/run_julia_ml.py"),
        ("4. Launch GUI", f"{sys.executable} gui/main.py"),
    ]
    
    for name, command in steps:
        success = run_step(name, command)
        if not success and "GUI" not in name:
            response = input("\nContinue anyway? (y/n): ")
            if response.lower() != 'y':
                print("Pipeline stopped.")
                return
    
    print("\n" + "="*60)
    print("✓ APPLICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()