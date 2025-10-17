# October 10 Data Collection Plan

## Data Sources

### 1. On-Chain Data (Hyperliquid)
**What we need:**
- Liquidation events (timestamp, address, asset, amount, price)
- Insurance fund balance changes
- ADL events (who got deleveraged, when, at what price)

**Source:** Hyperliquid blockchain explorer / API
- Explorer: https://app.hyperliquid.xyz/explorer
- API docs: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api

**Collection method:**
- Query liquidation events for October 10, 2025 (20:00-22:00 UTC)
- Export to CSV: timestamp, wallet, position_size, liquidation_price, asset
- Track insurance fund balance every minute during cascade

### 2. Price Data (Multiple Exchanges)
**What we need:**
- USDe, wBETH, BNSOL prices across exchanges
- 1-minute granularity for October 10, 20:00-22:00 UTC
- Orderbook depth snapshots

**Sources:**
- **Hyperliquid:** Internal orderbook prices (primary manipulation venue)
- **Binance:** Spot + futures prices (baseline for "real" market)
- **Bybit:** Perpetual prices
- **OKX:** Perpetual prices

**Collection method:**
- Use exchange APIs to pull historical OHLCV data
- Binance API: https://api.binance.com/api/v3/klines
- Compare Hyperliquid prices vs. CEX consensus

### 3. Dune Analytics
**What we need:**
- Cross-chain liquidation data
- DeFi protocol oracle price feeds
- Volume analysis across DEXs

**Queries to build:**
1. Hyperliquid liquidations on October 10
2. USDe price across Curve, Uniswap, Balancer
3. wBETH price across Lido, Rocket Pool integrations
4. Volume spikes on specific pairs

**Dune SQL example:**
```sql
SELECT 
  block_time,
  liquidated_user,
  collateral_asset,
  liquidation_amount,
  liquidation_price
FROM hyperliquid.liquidations
WHERE block_time BETWEEN '2025-10-10 20:00:00' AND '2025-10-10 22:00:00'
ORDER BY block_time ASC
```

### 4. Market Maker Activity
**What we need:**
- Top market maker wallet addresses
- Liquidity provision/withdrawal events
- Timing of position changes

**Source:**
- Hyperliquid on-chain data
- Track top 10 liquidity providers by volume
- Monitor their position changes during 20:00-21:35 UTC window

---

## Data Schema

### liquidations.csv
```
timestamp, exchange, wallet_address, asset, position_size, liquidation_price, liquidation_type (orderbook/insurance/ADL)
```

### prices.csv
```
timestamp, exchange, asset, price, volume, bid_depth, ask_depth
```

### insurance_fund.csv
```
timestamp, exchange, balance, change_amount, utilization_rate
```

### market_makers.csv
```
timestamp, wallet_address, action (add/remove), liquidity_amount, asset
```

---

## Analysis Plan

### Step 1: Price Deviation Analysis
- Calculate cross-exchange price deviation for USDe, wBETH, BNSOL
- Identify when Hyperliquid prices diverged >5% from CEX consensus
- Visualize: Timeline chart showing price spread

### Step 2: Liquidation Cascade Timeline
- Map liquidation events to price movements
- Identify cascade trigger point (when insurance fund depleted)
- Visualize: Waterfall chart of liquidations over time

### Step 3: Market Maker Withdrawal Pattern
- Track top MM liquidity changes
- Identify coordination (did they all withdraw at similar times?)
- Visualize: Heatmap of MM activity

### Step 4: Counterfactual Analysis
**Lighter scenario:**
- If prices were ZK-proven, would manipulation have been detectable?
- How would cryptographic verification have flagged the deviation?

**Variational scenario:**
- If OLP internalized liquidity, would cascade have been prevented?
- Model: OLP absorbs losses vs. insurance fund depletion

**FRY scenario:**
- How many liquidated traders would have stayed with FRY retention?
- Model: 82% attrition → 30% with FRY (70% retention)

---

## Deliverables

1. **Interactive Dune Dashboard**
   - Live October 10 data
   - Price deviation charts
   - Liquidation cascade visualization
   - MM withdrawal heatmap

2. **Data Export for Mirror Post**
   - CSV files for all datasets
   - Charts exported as PNG for article
   - Statistical summary (median deviation, cascade velocity, etc.)

3. **Counterfactual Analysis Document**
   - "How Lighter Would Have Prevented October 10"
   - "How Variational Would Have Mitigated the Cascade"
   - "Why FRY Is Still Needed"

---

## Next Steps

1. Set up Dune Analytics account
2. Write SQL queries for Hyperliquid liquidation data
3. Pull historical price data from Binance/Bybit/OKX APIs
4. Build data pipeline to combine all sources
5. Start analysis and visualization

Ready to start with Dune queries?
