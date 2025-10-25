# FRY Degen Subnet + Losers Casino Integration

## Overview

This integration merges the **Bittensor-inspired Degen Subnet** with your existing **Losers Casino backend** from the `git-checkout--b-add-losers-casino` branch. The result is a complete ecosystem where:

1. **Miners** scan Hyperliquid for degen trades and submit predictions
2. **Validators** verify outcomes and score miner accuracy
3. **FRY Casino** mints/burns FRY tokens based on validated losses/profits
4. **DEGEN tokens** reward accurate predictions (subnet-specific token)
5. **Dual token economy** creates synergies between prediction accuracy and loss quantification

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRY Degen Subnet                          │
│                                                               │
│  ┌──────────┐         ┌──────────┐        ┌──────────┐     │
│  │  Miners  │────────▶│  Subnet  │◀───────│Validators│     │
│  │          │ predict │   Core   │ verify │          │     │
│  └──────────┘         └─────┬────┘        └──────────┘     │
│                              │                               │
│                              ▼                               │
│                      ┌───────────────┐                       │
│                      │ DEGEN Rewards │                       │
│                      └───────────────┘                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  FRY Casino Backend                          │
│                  (from losers-casino branch)                 │
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │ Hyperliquid  │────────▶│ FRY Balance  │                  │
│  │  WebSocket   │  prices │   Database   │                  │
│  └──────────────┘         └──────────────┘                  │
│                                  │                            │
│                                  ▼                            │
│                          ┌───────────────┐                   │
│                          │ Mint/Burn FRY │                   │
│                          │ 10 FRY per $1 │                   │
│                          └───────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### From Losers Casino Branch
- **`fry_fastapi_backend.py`** - Core casino backend with FRY minting/burning
- **`proof-of-loss-consensus.js`** - Original PoL consensus (Node.js)
- **`ProofOfLossToken.sol`** - Smart contract for FRY tokens

### New Degen Subnet Components
- **`degen_subnet_core.py`** - Core subnet runtime (Python)
- **`degen_miner.py`** - Miner implementation
- **`degen_validator.py`** - Validator implementation
- **`degen_subnet_integration.py`** - Integration API layer

## How It Works

### 1. Miner Workflow

```python
# Miner scans Hyperliquid for degen positions
miner = DegenMiner(miner_id="miner_001", wallet_address="0x...")
await miner.register(stake=1000)  # Stake 1000 FRY

# Monitor your wallet
miner.add_monitored_address("0xf551aF8d5373B042DBB9F0933C59213B534174e4")

# Scan every 30 seconds
await miner.mine_loop(interval=30)
```

**Degen Score Calculation:**
- Leverage: 100x = 30 points
- Position Size: $50k+ = 25 points
- Volatility: 10%+ = 20 points
- Unrealized Loss: $1k+ = 15 points
- Funding Rate: High = 10 points
- **Total: 0-100 scale**

### 2. Validator Workflow

```python
# Validator verifies outcomes
validator = DegenValidator(validator_id="val_001", wallet_address="0x...")
await validator.register(stake=10000)  # 10x miner stake

# Validate every 30 seconds
await validator.validation_loop(interval=30)
```

**Outcome Detection:**
- **REKT**: Position liquidated → Mint FRY
- **MOON**: Position profitable → Burn FRY
- **SURVIVED**: Position closed neutral → No FRY change

### 3. FRY Casino Integration

When a validator confirms a REKT outcome:

```python
# Validator submits outcome
outcome = TradeOutcomeData(
    trade_id="0xf551...XRP_1234567890",
    outcome=TradeOutcome.REKT,
    loss_amount=5000,  # $5k loss
    liquidation_time=1234567890,
    final_pnl=-5000
)

# Subnet processes outcome
subnet.submit_outcome(outcome)

# Automatically calls FRY Casino API
POST http://localhost:8000/mirror
{
    "pnl": -5000,
    "symbol": "SUBNET",
    "trade_type": "subnet_validated"
}

# FRY Casino mints tokens
# Loss: $5000 × 10 FRY per $1 = 50,000 FRY minted ✅
```

### 4. Reward Distribution

**DEGEN Token Emissions:**
- 1 DEGEN per block (12 second blocks)
- 41% to miners (based on accuracy scores)
- 41% to validators (based on consensus)
- 18% to subnet owner

**Miner Scoring:**
```python
accuracy_score = (
    loss_probability_accuracy * 0.5 +
    timeline_accuracy * 0.3 +
    degen_score_accuracy * 0.2
)

# Bonuses
extreme_degen_bonus = 1.0 if loss > $10k else 0.0
consistency_bonus = 0.2 if avg_accuracy > 80% else 0.0
speed_bonus = 0.15 if predicted >1hr early else 0.0

final_score = accuracy * (1 + bonuses)  # Max 10x
```

## API Endpoints

### Subnet API (Port 8001)

**Register Miner:**
```bash
POST http://localhost:8001/subnet/miner/register
{
    "miner_id": "miner_001",
    "wallet_address": "0xf551aF8d5373B042DBB9F0933C59213B534174e4",
    "stake": 1000
}
```

**Submit Prediction:**
```bash
POST http://localhost:8001/subnet/prediction/submit
{
    "trade_id": "0xf551...XRP_1234567890",
    "miner_id": "miner_001",
    "degen_score": 95,
    "predicted_loss_probability": 0.85,
    "predicted_rekt_timeline": 3600,
    "leverage": 100,
    "position_size": 10000,
    "volatility": 15.5,
    "liquidity_score": 30,
    "fomo_factor": 0.95
}
```

**Submit Outcome:**
```bash
POST http://localhost:8001/subnet/outcome/submit
{
    "trade_id": "0xf551...XRP_1234567890",
    "outcome": "rekt",
    "loss_amount": 5000,
    "liquidation_time": 1234567890,
    "final_pnl": -5000
}
```

**Get Leaderboard:**
```bash
GET http://localhost:8001/subnet/leaderboard?limit=10
```

**Get Stats:**
```bash
GET http://localhost:8001/subnet/stats
```

### Casino API (Port 8000)

**Mirror PnL (used by subnet):**
```bash
POST http://localhost:8000/mirror
{
    "pnl": -5000,
    "symbol": "SUBNET",
    "trade_type": "subnet_validated"
}
```

**Get Balance:**
```bash
GET http://localhost:8000/balance
```

**Get Events:**
```bash
GET http://localhost:8000/balance/events
```

## Running the System

### Step 1: Start FRY Casino Backend

```bash
cd /tmp/usd_fry_casino/core
python3 fry_fastapi_backend.py
# Runs on http://localhost:8000
```

### Step 2: Start Degen Subnet API

```bash
cd liquidity-rails/core/subnet
python3 degen_subnet_integration.py
# Runs on http://localhost:8001
```

### Step 3: Start Miners

```bash
# Terminal 1
python3 degen_miner.py
```

### Step 4: Start Validators

```bash
# Terminal 2
python3 degen_validator.py
```

## Integration Flow Example

### Real-World Scenario: Your XRP Position

**Current Status:**
- Position: LONG XRP $3,340
- PnL: -196.4% (-$6,560)
- Leverage: ~50x
- Status: Deep underwater

**Subnet Prediction:**

1. **Miner scans your position:**
   ```python
   degen_score = 95  # Extremely degen
   # - Leverage 50x = 30 points
   # - Size $3,340 = 15 points
   # - Loss -$6,560 = 15 points
   # - Volatility 20% = 20 points
   # - Funding rate = 10 points
   # - FOMO factor = 5 points
   ```

2. **Miner predicts:**
   ```python
   predicted_loss_probability = 0.85  # 85% chance of rekt
   predicted_rekt_timeline = 7200  # 2 hours until liquidation
   ```

3. **Validator monitors position:**
   - Checks every 30 seconds
   - Detects liquidation via Hyperliquid API
   - Confirms REKT outcome

4. **FRY Casino mints tokens:**
   ```python
   loss_amount = 6560  # $6,560 loss
   fry_minted = 6560 * 10 = 65,600 FRY
   # Your balance: 4.96M → 5.03M FRY
   ```

5. **Miner earns DEGEN rewards:**
   ```python
   accuracy_score = 0.9  # Predicted correctly
   extreme_degen_bonus = 1.0  # $6k+ loss
   final_score = 0.9 * 2.0 = 1.8
   
   # Next block reward: 1.8x share of miner pool
   ```

## Dual Token Economy

### FRY Token (Loss Proof)
- **Minted**: When losses are verified
- **Burned**: When profits are verified
- **Rate**: 10 FRY per $1 lost, 5 FRY per $1 profit
- **Purpose**: Quantifiable proof of trading losses
- **Supply**: Unlimited (inflationary from losses)

### DEGEN Token (Prediction Rewards)
- **Minted**: Block emissions (1 DEGEN per 12s)
- **Earned**: Accurate predictions by miners/validators
- **Rate**: Based on accuracy scores
- **Purpose**: Incentivize accurate degen detection
- **Supply**: 21M total (deflationary)

### Synergies

**Burn DEGEN to boost FRY multipliers:**
```python
def burn_degen_for_multiplier(degen_amount):
    base_multiplier = 1.0
    bonus = (degen_amount / 1000) * 0.1  # 0.1x per 1000 DEGEN
    return min(base_multiplier + bonus, 10.0)

# Example: Burn 5000 DEGEN
multiplier = burn_degen_for_multiplier(5000)  # 1.5x
# Next loss: $1000 × 10 FRY × 1.5x = 15,000 FRY instead of 10,000
```

**Stake FRY to mine DEGEN:**
- Miners stake FRY to participate
- Higher FRY stake = higher weight in rewards
- Creates demand for FRY tokens

## Deployment Checklist

- [ ] FRY Casino backend running (port 8000)
- [ ] Degen Subnet API running (port 8001)
- [ ] At least 1 miner registered and scanning
- [ ] At least 1 validator registered and validating
- [ ] Hyperliquid API access configured
- [ ] Database initialized (fry_trading.db)
- [ ] WebSocket connections active

## Monitoring

**Check Integration Status:**
```bash
curl http://localhost:8001/subnet/integration/status
```

**Expected Response:**
```json
{
    "subnet_active": true,
    "casino_connected": true,
    "casino_balance": 4960000,
    "casino_api_url": "http://localhost:8000",
    "total_miners": 1,
    "total_validators": 1,
    "total_predictions": 5,
    "total_outcomes": 2
}
```

## Next Steps

1. **Deploy to Production:**
   - Move from localhost to production servers
   - Add authentication/authorization
   - Implement proper key management

2. **Scale Subnet:**
   - Add more miners for broader coverage
   - Add more validators for consensus
   - Monitor multiple exchanges (Binance, dYdX, GMX)

3. **Smart Contract Integration:**
   - Deploy DEGEN token contract
   - Integrate with ProofOfLossToken.sol
   - Enable on-chain reward distribution

4. **Frontend Dashboard:**
   - Real-time prediction feed
   - Miner/validator leaderboards
   - Live FRY minting visualization
   - Degen score heatmaps

## Conclusion

This integration creates a **complete Proof of Loss ecosystem** where:

- **Miners** earn DEGEN by accurately predicting degenerate trades
- **Validators** earn DEGEN by verifying outcomes
- **Traders** earn FRY from their verified losses
- **The Network** quantifies financial degeneracy at scale

The synergy between the Bittensor-style subnet and the FRY Casino creates a self-sustaining economy where trading failures become both **predictable** (DEGEN rewards) and **valuable** (FRY tokens).

**The Meta Innovation:** We've decentralized the identification, verification, and monetization of financial stupidity. 🍟📉
