# USD_FRY Deployment - Part 1: Environment Setup

## What You Need

1. **MetaMask wallet** with Arbitrum Sepolia network added
2. **Private key** from MetaMask
3. **5 minutes**

---

## Step 1: Add Arbitrum Sepolia to MetaMask

1. Open MetaMask
2. Click network dropdown → "Add Network"
3. Add these details:
   - Network Name: `Arbitrum Sepolia`
   - RPC URL: `https://sepolia-rollup.arbitrum.io/rpc`
   - Chain ID: `421614`
   - Currency Symbol: `ETH`
   - Block Explorer: `https://sepolia.arbiscan.io`

---

## Step 2: Get Your Private Key

⚠️ **NEVER share this or commit it to git**

1. Open MetaMask
2. Click three dots → Account Details
3. Click "Show Private Key"
4. Enter password
5. Copy the key

---

## Step 3: Create .env File

```bash
cd liquidity-rails/core/contracts
```

Open `.env` file (already created) and replace:
```
PRIVATE_KEY=your_private_key_here
```

With your actual private key from MetaMask.

---

## Step 4: Install Dependencies

```bash
npm install
```

This installs:
- Hardhat (Ethereum dev environment)
- OpenZeppelin contracts (security)
- Ethers.js (blockchain interaction)

Takes ~2 minutes.

---

## ✅ Part 1 Complete!

You now have:
- ✅ Arbitrum Sepolia network in MetaMask
- ✅ Private key in .env file
- ✅ Dependencies installed

**Next:** Part 2 - Compile contracts (5 min)

---

**Stop here if you need a break. Everything is saved.**
