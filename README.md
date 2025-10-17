# 🍟 Greenhouse & Company

**Retention Infrastructure for Crypto Exchanges**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FRY Protocol](https://img.shields.io/badge/FRY-Live%20on%20Arbitrum-green.svg)](https://arbiscan.io/address/0x492397d5912C016F49768fBc942d894687c5fe33)
[![Research](https://img.shields.io/badge/Research-Mirror-blue.svg)](https://mirror.xyz/0xf551aF8d5373B042DBB9F0933C59213B534174e4)

🌐 **[FRY Demo](https://aidanduffy68-prog.github.io/USD_FRY/)** | 📊 **[Contracts](https://arbiscan.io/address/0x492397d5912C016F49768fBc942d894687c5fe33)** | 📝 **[Research](https://mirror.xyz/0xf551aF8d5373B042DBB9F0933C59213B534174e4)**

---

## Core Thesis

**Every exchange is fighting over the same 18% of traders who stay after liquidation.**

**We're building infrastructure to capture the 82% who quit.**

---

## 🚀 Live on Arbitrum Mainnet

**Deployed October 11, 2025**

```
USD_FRY Token:               0x492397d5912C016F49768fBc942d894687c5fe33
WreckageProcessorWithOracle: 0xf97E890aDf8968256225060e8744a797954C33CF
FRYPredictionMarket:         0xdF0B798E51d5149fE97D57fbBc8D6A8A0756204e
```

**Chainlink Oracles:**
- BTC/USD: `0x6ce185860a4963106506C203335A2910413708e9`
- ETH/USD: `0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612`

[View on Arbiscan →](https://arbiscan.io/address/0x492397d5912C016F49768fBc942d894687c5fe33)

---

## 📘 [Read the Technical Whitepaper](liquidity-rails/docs/FRY_TECHNICAL_WHITEPAPER.md)

**Start here** - Complete technical specification covering system architecture, routing algorithms, privacy layer, economic model, and deployment guide.

---

## Quick Links

- **[Technical Whitepaper](liquidity-rails/docs/FRY_TECHNICAL_WHITEPAPER.md)** - THE BIBLE
- **[Quick Start](liquidity-rails/docs/QUICK_START.md)** - Get running in 5 minutes
- **[System Summary](liquidity-rails/docs/SYSTEM_SUMMARY.md)** - High-level overview
- **[Deployment Guide](liquidity-rails/docs/DEPLOYMENT_GUIDE.md)** - Production deployment

---

## What We Do

### 1. Research (Competitive Intelligence)

We analyze DeFi infrastructure across three layers:

**Layer 1: Oracle & Price Discovery**
- Lighter (ZK-proven matching), Stork (pull oracles), Pyth, Chainlink

**Layer 2: Liquidity & Risk Management**
- Variational (OLP), Vertex, Hyperliquid, dYdX v4

**Layer 3: Retention Infrastructure**
- **FRY Protocol (our solution)** - Nobody else is building here

📖 **[Read our October 10 analysis](https://mirror.xyz/0xf551aF8d5373B042DBB9F0933C59213B534174e4/i8FZxbZRcqG8IVG6AWyMC3TvMmSYFeG1Q3QDrfGZUp0)** - Oracle failure, market maker withdrawal, and why retention infrastructure matters.

### 2. Build (FRY Protocol)

**The Problem:**
- 82% of liquidated traders quit forever
- Exchanges lose their most active users
- Death spiral: liquidations → attrition → less liquidity → more liquidations

**The Solution:**
- Mint FRY tokens at 2.26× liquidation value
- 6-month vesting (prevents dump, creates re-engagement)
- Tradeable, stakeable, fee discounts
- Psychological shift: "I lost money" → "I got something back"

**The Result:**
- **70% retention vs 18% baseline**
- **3.9× improvement**
- Growth spiral instead of death spiral

### October 10, 2025: The Validation Event

- **$19.3B destroyed** in liquidation cascade
- **1.6M traders** liquidated
- **82% quit forever** (industry baseline)
- **FRY thesis validated**: Retention infrastructure is the missing layer

**Tech Stack:**
- Smart Contracts: Solidity 0.8.19, OpenZeppelin, Hardhat
- Oracles: Chainlink Price Feeds (BTC/USD, ETH/USD)
- Network: Arbitrum Mainnet
- Research: Mirror, Dune Analytics

---

## Project Structure

```
liquidity-rails/
├── core/
│   ├── engines/        # Routing, matching, ML, visualization
│   ├── privacy/        # zkML & confidential positions
│   ├── federated/      # Distributed learning
│   ├── api/            # REST API server
│   ├── contracts/      # Smart contracts
│   └── tests/          # Test suite
├── docs/               # Documentation
├── scripts/            # Deployment scripts
└── examples/           # Usage examples
```

---

## Quick Start

### Use the Protocol
1. Visit [Live Demo](https://aidanduffy68-prog.github.io/USD_FRY/)
2. Connect wallet (Arbitrum mainnet)
3. Process wreckage or bet on prediction markets

### Deploy Contracts
```bash
cd liquidity-rails/core/contracts
npm install
npm run deploy:mainnet
```

---

## Architecture

### Core Components

1. **WreckageProcessorWithOracle** - Processes losses with Chainlink-verified prices
2. **FRYPredictionMarket** - Auto-resolving prediction markets
3. **USD_FRY Token** - ERC20 token minted from processed wreckage

### How It Works

```
Trading Loss → Chainlink Price Verification → FRY Minting (2.26x) → Tradeable Token
```

### Prediction Markets
- Create markets about crypto prices, events, etc.
- Bet with USDC
- Auto-resolve using Chainlink oracles
- Losers receive FRY tokens (2.26x their loss)
- Winners receive 70% of losing pool

---

## Why This Matters

### The Unsolved Problem

**Even with perfect infrastructure:**
- Perfect oracles (Lighter) prevent manipulation ✓
- Perfect liquidity (Variational) prevent cascades ✓
- **But traders still get liquidated on legitimate moves**
- **And 82% still quit**

**FRY is the only solution addressing post-liquidation retention.**

### Competitive Positioning

**We Are NOT:**
- Another oracle provider (Lighter/Stork/Pyth do this)
- Another liquidity solution (Variational/Vertex do this)
- Another DEX (we integrate with all of them)

**We ARE:**
- The retention layer that makes all DEXs better
- Competitive intelligence firm for DeFi infrastructure
- The only team building Layer 3 (retention)

### Use Cases

**For Exchanges:**
- Integrate FRY to reduce 82% attrition to 30%
- 3.9× more retained users = 3.9× more trading volume
- Non-competitive: works with any oracle/liquidity solution

**For Traders:**
- Get 2.26× FRY tokens after liquidation
- Vesting schedule creates reason to stay engaged
- Fee discounts + staking rewards on future trades

**For Researchers:**
- Access our competitive intelligence on DeFi infrastructure
- Collaborate on oracle/liquidity/retention research
- Cite our published analysis

---

## Research & Publications

**Published:**
- [October 10 Analysis: Oracle Failure, MM Withdrawal, ADL Cascades](https://mirror.xyz/0xf551aF8d5373B042DBB9F0933C59213B534174e4/i8FZxbZRcqG8IVG6AWyMC3TvMmSYFeG1Q3QDrfGZUp0)
- [Positioning Document](docs/greenhouse-positioning.md) - Complete strategy and roadmap
- [Counterfactual Analysis](docs/lighter-variational-fry-analysis.md) - How Lighter + Variational + FRY prevent October 10

**In Progress:**
- Oracle Manipulation Detection (Part 2)
- Exchange Architecture Analysis
- Retention Economics Deep Dive

---

## Status

**FRY Protocol**: Live on Arbitrum Mainnet  
**Launched**: October 11, 2025  
**Contracts**: [View on Arbiscan](https://arbiscan.io/address/0x492397d5912C016F49768fBc942d894687c5fe33)  
**Demo**: [Live](https://aidanduffy68-prog.github.io/USD_FRY/)

**Research**: Active  
**Partnerships**: In discussion (Stork Labs, Lighter, Variational)

### Roadmap

**Q4 2025:**
- ✅ Publish October 10 analysis
- ✅ Deploy FRY Protocol on Arbitrum
- 🔄 Secure first exchange integration
- 🔄 Publish oracle manipulation research series

**Q1 2026:**
- Integrate with 3-5 exchanges
- Launch retention analytics dashboard
- Expand research to cover all major DEXs

---

## Contact

**Partnerships**: Open an issue or reach out via [LinkedIn](https://www.linkedin.com/company/greenhouseandco/)  
**Research Collaboration**: We're open to joint research projects  
**Integration**: Contact us to integrate FRY as your retention layer

Built for the 82% who quit. Because retention infrastructure matters. 🍟
