# FRY Protocol Testnet Deployment Guide

## Prerequisites

### 1. Get Arbitrum Sepolia ETH
- Faucet: https://faucet.quicknode.com/arbitrum/sepolia
- Or: https://www.alchemy.com/faucets/arbitrum-sepolia
- Need: ~0.5 ETH for deployment

### 2. Create .env File
```bash
cd liquidity-rails/core/contracts
```

Create `.env`:
```bash
# Your wallet private key (DO NOT COMMIT)
PRIVATE_KEY=your_private_key_here

# RPC endpoints (optional, has defaults)
ARBITRUM_SEPOLIA_RPC=https://sepolia-rollup.arbitrum.io/rpc

# Arbiscan API key for verification (optional)
ARBISCAN_API_KEY=your_arbiscan_key
```

### 3. Install Dependencies
```bash
npm install
```

---

## Deployment Steps

### Step 1: Compile Contracts
```bash
npm run compile
```

Expected output:
```
Compiled 5 Solidity files successfully
```

### Step 2: Deploy to Testnet
```bash
npm run deploy:testnet
```

This deploys:
- ✅ USDFRYToken (ERC20)
- ✅ AgentBVerifier (zkML)
- ✅ ConfidentialPositionVerifier (Privacy)
- ✅ LiquidityRailsRouter (Routing)
- ✅ WreckageMatchingPool (P2P)

Saves addresses to `deployment.json`

### Step 3: Verify on Arbiscan (Optional)
```bash
npm run verify:testnet
```

---

## Connect Agent B to Testnet

### Step 1: Update Agent B Config
```bash
cd ../../engines/agent_b
```

Create `testnet_config.json`:
```json
{
  "network": "arbitrum-sepolia",
  "contracts": {
    "usdFryToken": "ADDRESS_FROM_DEPLOYMENT_JSON",
    "router": "ADDRESS_FROM_DEPLOYMENT_JSON",
    "matchingPool": "ADDRESS_FROM_DEPLOYMENT_JSON"
  },
  "dexes": {
    "hyperliquid": {
      "testnet": true,
      "api_url": "https://api.hyperliquid-testnet.xyz",
      "ws_url": "wss://api.hyperliquid-testnet.xyz/ws"
    }
  },
  "capital": {
    "initial_usdc": 10000,
    "max_position_size": 5000,
    "rails_allocation": 0.7,
    "agent_b_reserve": 0.3
  }
}
```

### Step 2: Run Agent B on Testnet
```bash
python3 agent_b_testnet.py --config testnet_config.json
```

---

## Monitor Performance

### Real-Time Dashboard
```bash
cd ../../../
python3 -m http.server 8000
```

Open: http://localhost:8000/docs/dashboard.html

### Check Contract State
```bash
# Get FRY total supply
npx hardhat console --network arbitrumSepolia
> const token = await ethers.getContractAt("USDFRYToken", "ADDRESS")
> await token.totalSupply()

# Check minting events
> const filter = token.filters.WreckageMinted()
> const events = await token.queryFilter(filter)
> console.log(events)
```

---

## Hyperliquid Testnet Integration

### Get Testnet Access
1. Go to: https://app.hyperliquid-testnet.xyz
2. Connect wallet
3. Get testnet USDC from faucet
4. Note your API credentials

### Connect to Hyperliquid API
```python
# hyperliquid_testnet_client.py
import requests

class HyperliquidTestnet:
    def __init__(self):
        self.base_url = "https://api.hyperliquid-testnet.xyz"
    
    def get_funding_rates(self):
        """Get current funding rates"""
        response = requests.get(f"{self.base_url}/info", json={
            "type": "metaAndAssetCtxs"
        })
        return response.json()
    
    def get_liquidations(self, lookback_hours=24):
        """Get recent liquidations"""
        response = requests.get(f"{self.base_url}/info", json={
            "type": "liquidations",
            "lookback": lookback_hours
        })
        return response.json()
    
    def submit_order(self, asset, size, price, is_buy):
        """Submit test order"""
        # Implement with your API key
        pass

# Test connection
client = HyperliquidTestnet()
funding = client.get_funding_rates()
print(f"Connected! Found {len(funding)} markets")
```

---

## Test Scenarios

### Scenario 1: Process Liquidation
```python
from liquidity_rails_engine import LiquidityRailsEngine

engine = LiquidityRailsEngine(testnet=True)

# Simulate liquidation wreckage
wreckage = {
    "type": "long_liq",
    "asset": "BTC",
    "amount_usd": 5000,
    "dex": "Hyperliquid",
    "stablecoin": "USDH"
}

route = engine.route_wreckage(wreckage)
print(f"FRY Minted: {route['fry_minted']}")
print(f"Route: {route['path']}")
print(f"Cost: {route['cost_bps']} bps")
```

### Scenario 2: P2P Matching
```python
from wreckage_matching_engine import WreckageMatchingEngine

matcher = WreckageMatchingEngine(testnet=True)

# Two offsetting positions
long_funding = {"dex": "Hyperliquid", "asset": "ETH", "funding_rate": 0.01, "notional": 10000}
short_funding = {"dex": "dYdX", "asset": "ETH", "funding_rate": -0.008, "notional": 10000}

match = matcher.match_funding_swaps([long_funding, short_funding])
print(f"Match found: {match['matched']}")
print(f"FRY minted: {match['fry_total']}")
```

### Scenario 3: Agent B Market Making
```python
from agent_b_core import AgentB

agent = AgentB(testnet=True, venue="hyperliquid")

# Run for 1 hour
agent.start_market_making(
    asset="BTC",
    capital_usd=5000,
    duration_hours=1
)

# Check results
stats = agent.get_stats()
print(f"Slippage harvested: ${stats['slippage_usd']}")
print(f"FRY minted: {stats['fry_minted']}")
print(f"Hedge performance: {stats['hedge_accuracy']}%")
```

---

## Success Metrics

Track these for your pilot:

### Volume Metrics
- [ ] Wreckage processed: $X
- [ ] FRY minted: Y tokens
- [ ] Effective minting rate: Z FRY/$1

### Efficiency Metrics
- [ ] P2P match rate: X%
- [ ] Average routing cost: Y bps
- [ ] Capital utilization: Z%

### Performance Metrics
- [ ] Agent B hedge accuracy: X%
- [ ] Slippage harvested: $Y
- [ ] ML improvement: +Z%

### Goal: Prove 2x+ improvement over base rate

---

## Troubleshooting

### Contract Deployment Fails
```bash
# Check balance
npx hardhat run scripts/check-balance.js --network arbitrumSepolia

# Increase gas
# Edit hardhat.config.js: gasPrice: 2000000000 (2 gwei)
```

### Hyperliquid Connection Issues
```bash
# Test API
curl https://api.hyperliquid-testnet.xyz/info

# Check rate limits
# Hyperliquid: 100 req/min
```

### Agent B Not Minting FRY
```bash
# Check contract permissions
npx hardhat console --network arbitrumSepolia
> const token = await ethers.getContractAt("USDFRYToken", "ADDRESS")
> await token.hasRole(await token.MINTER_ROLE(), "ROUTER_ADDRESS")
# Should return: true
```

---

## Next Steps After Testnet

1. **Collect 2 weeks of data**
   - Wreckage processed
   - FRY minted
   - Capital efficiency
   - System uptime

2. **Create metrics dashboard**
   - Real-time stats
   - Historical charts
   - Comparison to base rate

3. **Prepare pitch**
   - "We processed $X wreckage"
   - "Minted Y FRY at Z rate"
   - "Improved efficiency by W%"

4. **Approach Hyperliquid**
   - Show testnet results
   - Propose mainnet pilot
   - Negotiate revenue share

---

## Resources

- Arbitrum Sepolia Explorer: https://sepolia.arbiscan.io
- Hyperliquid Testnet: https://app.hyperliquid-testnet.xyz
- Hyperliquid Docs: https://hyperliquid.gitbook.io
- FRY Discord: [Coming soon]

---

**Ready to deploy? Start with Step 1: Get testnet ETH** 🍟
