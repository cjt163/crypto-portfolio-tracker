// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Track cryptocurrency holdings for multiple wallet addresses
contract PortfolioTracker {
    // Struct to store holdings for each cryptocurrency
    struct Holdings {
        uint256 btc;  // Bitcoin
        uint256 eth;  // Ethereum
        uint256 sol;  // Solana
        uint256 xrp;  // Ripple
    }

    // Mapping from wallet address to their holdings
    mapping(address => Holdings) private portfolios;
    // Array to keep track of all wallet addresses
    address[] private walletAddresses;
    // Check if an address is already tracked
    mapping(address => bool) private isTracked;

    // Set holdings for the caller's wallet (BTC, ETH, SOL, XRP)
    function setHoldings(uint256 _btc, uint256 _eth, uint256 _sol, uint256 _xrp) external {
        // Add to wallet list if not already tracked
        if (!isTracked[msg.sender]) {
            walletAddresses.push(msg.sender);
            isTracked[msg.sender] = true;
        }
        // Update holdings
        portfolios[msg.sender] = Holdings(_btc, _eth, _sol, _xrp);
    }

    // Get holdings for a specific wallet, returns (btc, eth, sol, xrp)
    function getHoldings(address _wallet) external view returns (uint256, uint256, uint256, uint256) {
        Holdings memory h = portfolios[_wallet];
        return (h.btc, h.eth, h.sol, h.xrp);
    }

    // Get all tracked wallet addresses
    function getAllWallets() external view returns (address[] memory) {
        return walletAddresses;
    }
}
