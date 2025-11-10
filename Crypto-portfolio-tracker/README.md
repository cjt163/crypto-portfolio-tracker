# Crypto Portfolio Tracker

A comprehensive cryptocurrency portfolio tracking and forecasting application integrating Python GUI, Blockchain (Solidity/Brownie), and Julia Machine Learning.

## Overview

Track your crypto holdings across multiple wallets, fetch real-time price data, generate ML-based forecasts, and visualize portfolio performance with an interactive GUI.

### Features

- **Smart Contract**: Solidity contract for on-chain portfolio storage (PortfolioTracker.sol)
- **Multi-Wallet Support**: Track 5+ wallets with BTC, ETH, SOL, and XRP holdings
- **Price Data**: Fetch 180-day historical prices from CoinGecko API
- **ML Forecasting**: Linear regression models trained on lagged price features (Julia)
- **Portfolio Projections**: 7-day portfolio value forecasts with % change
- **Interactive GUI**: Tkinter-based interface with real-time updates

## Prerequisites

### Required Software

1. **Python 3.9+** (Anaconda recommended)
   - Download: https://www.anaconda.com/download

2. **Julia 1.11+**
   - Download: https://julialang.org/downloads/

3. **Brownie** (Ethereum development framework)
   - Installed via pip

### Environment Setup

**Option 1: Conda (Recommended)**
```bash
conda create -n python-julia python=3.9
conda activate python-julia
```

**Option 2: venv**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- `requests` - API calls
- `pandas` - Data processing
- `brownie` - Ethereum framework
- `tkinter` - GUI (included with Python)

### Julia Packages

Open Julia REPL and run:

```julia
using Pkg
Pkg.add("CSV")
Pkg.add("DataFrames")
Pkg.add("MLJ")
Pkg.add("MLJLinearModels")
Pkg.add("Statistics")
```

**Verify installation:**
```julia
using CSV, DataFrames, MLJ, MLJLinearModels, Statistics
```

## Installation

1. **Clone or download the repository**
   ```bash
   cd Crypto-portfolio-tracker
   ```

2. **Activate environment** (if using conda)
   ```bash
   conda activate python-julia
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Julia packages** (see Prerequisites section)

5. **Initialize Brownie** (first time only)
   ```bash
   brownie init
   ```

6. **Test environment**
   ```bash
   python test_environment.py
   ```

## Quick Start

### Full Application (Automated)

```bash
python run_app.py
```

This runs all stages automatically and launches the GUI.

### Manual Workflow (Step-by-Step)

**1. Generate Mock Wallets**
```bash
python scripts/generate_mock_wallets.py
```
Creates 5 wallets with random holdings in `data/wallet_balances.json`.

**2. Fetch Price Data**
```bash
cd api
python fetch_prices.py
cd ..
```
Fetches 180 days of historical prices for BTC, ETH, SOL, XRP.
**Note**: Includes 2-second delays between API requests.

**3. Run ML Pipeline**
```bash
python scripts/run_julia_ml.py
```
Executes:
- Preprocessing (creates lagged features)
- Forecasting (trains models, generates 7-day predictions)
- Portfolio forecast (calculates portfolio value projections)

**4. Launch GUI**
```bash
python gui/main.py
```

## Project Structure

```
Crypto-portfolio-tracker/
├── contracts/              # Solidity smart contracts
│   └── PortfolioTracker.sol
├── scripts/                # Utility scripts
│   ├── deploy.py           # Contract deployment
│   ├── generate_mock_wallets.py
│   ├── calculate_portfolio_forecast.py
│   └── run_julia_ml.py     # ML pipeline orchestrator
├── api/                    # Price data fetching
│   ├── config.py           # CoinGecko API config
│   └── fetch_prices.py     # Fetch historical prices
├── ml/                     # Julia ML scripts
│   ├── preprocess.jl       # Feature engineering (lag features)
│   └── forecast.jl         # Price prediction models
├── gui/                    # Tkinter GUI application
│   └── main.py
├── data/                   # Generated data (created automatically)
│   ├── wallet_balances.json
│   ├── *_history.csv       # Historical price data
│   ├── *_preprocessed.csv  # Preprocessed with lag features
│   ├── *_forecast.csv      # 7-day price predictions
│   └── portfolio_forecast.csv
├── JuliaExecutor.py        # Python-Julia bridge
├── run_app.py              # Main entry point
├── test_environment.py     # Environment verification
├── requirements.txt        # Python dependencies
└── README.md
```

## Usage Guide

### GUI Features

**Wallet Selection**
- Select wallet from dropdown menu
- Click "Load Portfolio" to view holdings and forecasts
- Switch between wallets to compare portfolios

**Display Panels**
- **Holdings**: Crypto amounts for each coin (BTC, ETH, SOL, XRP)
- **Live Prices**: Latest prices from historical data
- **Total Value**: Current portfolio valuation in USD

**Forecasts**
- **BTC Price Forecast**: 7-day BTC price predictions
- **Portfolio Value Forecast**: Total portfolio value over 7 days
  - Shows daily projections
  - Displays % change (green = gain, red = loss)

**Data Management**
- Click "Refresh Data" to reload all CSV files
- Updates prices and recalculates forecasts

### Smart Contract Deployment (Optional)

Deploy PortfolioTracker contract to local blockchain:

```bash
brownie run scripts/deploy.py
```

Saves contract address to `data/contract_address.txt`.

**Note**: Requires Ganache or local blockchain running.

## Data Flow

```
1. Price Fetching
   api/fetch_prices.py → data/{COIN}_history.csv

2. Preprocessing
   ml/preprocess.jl → data/{COIN}_preprocessed.csv

3. ML Forecasting
   ml/forecast.jl → data/{COIN}_forecast.csv

4. Portfolio Calculation
   scripts/calculate_portfolio_forecast.py → data/portfolio_forecast.csv

5. Visualization
   gui/main.py (reads all CSV files)
```

## Technical Details

### Machine Learning Model

- **Algorithm**: Linear Regression (MLJLinearModels)
- **Features**: lag1, lag2, lag3 (previous 3 prices)
- **Target**: Current price
- **Train/Test Split**: 80/20
- **Evaluation Metric**: MAE (Mean Absolute Error)
- **Forecast Method**: Rolling predictions (7 days)

### Supported Cryptocurrencies

| Coin | Symbol | CoinGecko ID |
|------|--------|--------------|
| Bitcoin | BTC | bitcoin |
| Ethereum | ETH | ethereum |
| Solana | SOL | solana |
| Ripple | XRP | ripple |

### API Configuration

- **Data Source**: CoinGecko API (https://www.coingecko.com/)
- **Historical Range**: 180 days
- **Rate Limit**: 10-50 calls/minute (free tier)
- **Delay**: 2 seconds between requests

## Troubleshooting

### Julia not found
```bash
# Verify Julia installation
julia --version

# Add Julia to PATH (Windows)
# Add C:\Users\<YourName>\AppData\Local\Programs\Julia-1.11.x\bin to PATH
```

### Python package errors
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Unicode encoding errors (Windows)
- All Unicode checkmarks replaced with `[OK]` for compatibility
- Should work without issues on Windows now

### CoinGecko API rate limits
- Free tier: 10-50 calls per minute
- Script includes 2-second delays
- If blocked, wait 5-10 minutes before retrying

### Missing CSV files
```bash
# Run in order:
python scripts/generate_mock_wallets.py
cd api && python fetch_prices.py && cd ..
python scripts/run_julia_ml.py
```

### Julia package load errors
```julia
# In Julia REPL, rebuild packages:
using Pkg
Pkg.update()
Pkg.build()
```

## Performance Notes

- **Price fetching**: ~45 seconds (4 coins × 2s delay)
- **ML preprocessing**: ~5-10 seconds (4 coins)
- **ML forecasting**: ~30-60 seconds (model training × 4)
- **GUI load time**: < 1 second

## Development Status

- [x] Smart contract (PortfolioTracker.sol)
- [x] Mock wallet generation
- [x] Price API integration (CoinGecko)
- [x] Julia ML preprocessing
- [x] Julia ML forecasting (all 4 coins)
- [x] Portfolio forecast calculation
- [x] GUI implementation
- [x] Full integration
- [x] Multi-wallet support

## Future Enhancements

- Real-time price updates (WebSocket)
- More cryptocurrencies (top 20)
- Advanced ML models (LSTM, Prophet)
- Web-based dashboard (Flask/Django)
- On-chain portfolio sync with smart contract
- Price alerts and notifications
- Historical performance tracking
- Export reports (PDF, Excel)

## Contributing

This is a class project. Feel free to fork and extend for your own learning.

## License

MIT

## Disclaimer

**This tool is for educational and informational purposes only.**

Cryptocurrency investments carry significant risk. Past performance does not guarantee future results. The forecasts generated by this application are based on historical data and simple linear models - they should not be used as financial advice.

Always do your own research (DYOR) before making investment decisions.
