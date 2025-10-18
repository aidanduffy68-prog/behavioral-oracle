# Hyperliquid API Access Guide

**Goal:** Get liquidation data from Hyperliquid to populate FRY retention oracle.

---

## API Documentation

**Base URL:** `https://api.hyperliquid.xyz/info`

**Docs:** https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api

---

## Key Endpoints for FRY Oracle

### 1. User Fills (Trading History)
```python
payload = {
    "type": "userFills",
    "user": "0x..." # wallet address
}
```
Returns all trades for a user, including liquidations.

### 2. Liquidation Events
Liquidations appear in `userFills` with specific flags. Need to filter for:
- `liquidation: true` flag
- Or parse from fill type

### 3. User State (Current Positions)
```python
payload = {
    "type": "clearinghouseState",
    "user": "0x..."
}
```
Returns current positions, margin, etc.

---

## Data We Need

### For Oracle Population:
1. **Liquidation events (October 10):**
   - Wallet address
   - Timestamp
   - Liquidation size (USD)
   - Asset liquidated

2. **Post-liquidation activity (30 days):**
   - Did wallet trade again?
   - Volume generated
   - Deposits/withdrawals

---

## Implementation Steps

### Step 1: Get October 10 Liquidations
```python
# Pseudo-code
oct10_start = datetime(2025, 10, 10, 0, 0, 0).timestamp()
oct10_end = datetime(2025, 10, 11, 0, 0, 0).timestamp()

# Option A: Query known liquidated wallets
for wallet in known_liquidated_wallets:
    fills = fetch_user_fills(wallet)
    liquidations = filter_liquidations(fills, oct10_start, oct10_end)
    
# Option B: Query global liquidation feed (if available)
liquidations = fetch_all_liquidations(oct10_start, oct10_end)
```

### Step 2: Track Wallets for 30 Days
```python
for liq in liquidations:
    oracle.track_liquidation(
        wallet_address=liq["wallet"],
        liquidation_timestamp=liq["timestamp"],
        liquidation_size=liq["size"],
        asset=liq["asset"]
    )
```

### Step 3: Check Return Rates
```python
# Run daily
oracle.update_retention_metrics()
```

---

## Challenges

### 1. No Global Liquidation Feed
Hyperliquid API may not have a "get all liquidations" endpoint. May need to:
- Query known liquidated wallets individually
- Use on-chain events if available
- Partner with Hyperliquid for data access

### 2. Rate Limits
Need to respect API rate limits when querying thousands of wallets.

### 3. Historical Data Availability
October 10 was in the past - need to verify historical data is available via API.

---

## Alternative Data Sources

### 1. On-Chain Data
If Hyperliquid is on-chain (L1 or L2), can query:
- Liquidation events from smart contracts
- Trading activity from transaction logs

### 2. Dune Analytics
Create Dune queries to extract:
- October 10 liquidations
- Post-liquidation activity
- Already have SQL queries written

### 3. Direct Partnership
Reach out to Hyperliquid team:
- Request data export for research
- Propose FRY integration
- Get API access or data dump

---

## Next Actions

1. **Test Hyperliquid API:**
   - Make sample calls to understand response structure
   - Verify historical data availability
   - Check rate limits

2. **Parse Liquidation Events:**
   - Update `collect_oct10_liquidations.py` with real API calls
   - Filter for liquidation-specific fills

3. **Populate Oracle:**
   - Run collection script
   - Verify data in SQLite database

4. **Wait 30 Days (or use historical data):**
   - If October 10 was >30 days ago, can measure immediately
   - Otherwise, set up daily cron job to check retention

5. **Generate Report:**
   - Run `oracle.get_retention_report()`
   - Use data for bonding curve design
   - Write Part 3 Mirror article

---

## Code to Test API

```python
import requests

def test_hyperliquid_api():
    base_url = "https://api.hyperliquid.xyz/info"
    
    # Test 1: Get metadata
    payload = {"type": "meta"}
    response = requests.post(base_url, json=payload)
    print("Meta:", response.json())
    
    # Test 2: Get user fills (replace with real wallet)
    payload = {
        "type": "userFills",
        "user": "0x0000000000000000000000000000000000000000"
    }
    response = requests.post(base_url, json=payload)
    print("User fills:", response.json())

test_hyperliquid_api()
```

---

## Timeline

- **Now:** Test API, understand data structure
- **Week 1:** Collect October 10 liquidations
- **Week 2-5:** Track wallets, measure 30-day return
- **Week 6:** Generate retention report, design bonding curve
- **Week 7:** Write Part 3 Mirror article with real data

---

**Status:** Ready to test API and collect data.
