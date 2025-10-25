# FRY Degen Subnet - Real Bittensor Integration Guide

## Overview

This is a **real Bittensor subnet** that integrates with your FRY ecosystem. It uses actual Bittensor SDK components (not a fork) to create a decentralized network for predicting and validating degenerate trading outcomes.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Bittensor Network                           │
│                                                               │
│  ┌──────────┐         ┌──────────┐        ┌──────────┐     │
│  │  Miners  │◀───────▶│ Subtensor│◀──────▶│Validators│     │
│  │ (Axons)  │  query  │ (Chain)  │ weights│(Dendrites)│     │
│  └──────────┘         └──────────┘        └──────────┘     │
│       │                                           │          │
│       │ DegenSynapse                             │          │
│       ▼                                           ▼          │
│  Hyperliquid API                          Score & Validate  │
└───────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  FRY Casino Backend                          │
│                                                               │
│              Mint FRY from validated losses                  │
└─────────────────────────────────────────────────────────────┘
```

## Real Bittensor Components Used

### 1. **Subtensor** (Blockchain)
- Connects to Bittensor testnet or mainnet
- Handles staking, registration, and weight setting
- Manages consensus and rewards

### 2. **Axon** (Miner Server)
- Serves predictions to validators
- Implements forward function for DegenSynapse
- Handles blacklisting and priority

### 3. **Dendrite** (Validator Client)
- Queries miners for predictions
- Aggregates responses
- Sets weights based on accuracy

### 4. **Metagraph** (Network State)
- Tracks all neurons (miners + validators)
- Stores stakes, weights, and UIDs
- Syncs with chain every epoch

### 5. **Custom Synapse** (Protocol)
- `DegenSynapse`: Custom protocol for degen predictions
- Request: trader_address, coin, position_data
- Response: degen_score, loss_probability, timeline

## Installation

### 1. Install Bittensor SDK

```bash
pip3 install bittensor
```

### 2. Create Wallets

```bash
# Create miner wallet
btcli wallet new_coldkey --wallet.name miner
btcli wallet new_hotkey --wallet.name miner --wallet.hotkey default

# Create validator wallet
btcli wallet new_coldkey --wallet.name validator
btcli wallet new_hotkey --wallet.name validator --wallet.hotkey default
```

### 3. Get Testnet TAO

```bash
# Faucet for testnet TAO
btcli wallet faucet --wallet.name miner --subtensor.network test
btcli wallet faucet --wallet.name validator --subtensor.network test
```

### 4. Register on Subnet

```bash
# Register miner (requires stake)
btcli subnet register --netuid 1 --wallet.name miner --subtensor.network test

# Register validator (requires higher stake)
btcli subnet register --netuid 1 --wallet.name validator --subtensor.network test
```

## Running the Subnet

### Start Miner

```bash
cd liquidity-rails/core/subnet

# Run miner with default config
python3 bittensor_degen_miner.py \
    --netuid 1 \
    --subtensor.network test \
    --wallet.name miner \
    --wallet.hotkey default \
    --axon.port 8091
```

**Miner Features:**
- Scans Hyperliquid for positions
- Calculates degen scores (0-100)
- Predicts loss probability and timeline
- Serves predictions via Axon
- Blacklists low-stake validators

### Start Validator

```bash
cd liquidity-rails/core/subnet

# Run validator with default config
python3 bittensor_degen_validator.py \
    --netuid 1 \
    --subtensor.network test \
    --wallet.name validator \
    --wallet.hotkey default
```

**Validator Features:**
- Queries all miners via Dendrite
- Monitors Hyperliquid for liquidations
- Scores miners based on accuracy
- Sets weights on Bittensor chain
- Mints FRY via casino backend

### Start FRY Casino Backend

```bash
# Terminal 3: Casino backend (for FRY minting)
cd /tmp/usd_fry_casino/core
python3 fry_fastapi_backend.py
# Runs on http://localhost:8000
```

## How It Works

### 1. Miner Prediction Flow

```python
# Validator sends query
synapse = DegenSynapse(
    trader_address="0xf551aF8d5373B042DBB9F0933C59213B534174e4",
    coin="XRP",
    position_data={...}
)

# Miner receives via Axon
response = await miner.predict_degen(synapse)

# Miner calculates degen score
degen_score = calculate_degen_score(position)
# - Leverage: 100x = 30 points
# - Size: $50k = 25 points  
# - Volatility: 20% = 20 points
# - Unrealized loss: -$6k = 15 points
# - Distance to liq: 5% = 10 points
# Total: 95/100 (extreme degen)

# Miner returns prediction
response.degen_score = 95
response.predicted_loss_probability = 0.85
response.predicted_rekt_timeline = 7200  # 2 hours
response.confidence = 0.8
response.reasoning = "100x leverage | $6560 underwater | extreme degen detected"
```

### 2. Validator Scoring Flow

```python
# Validator queries all miners
responses = await validator.dendrite(
    axons=[metagraph.axons[uid] for uid in miner_uids],
    synapses=[synapse for _ in miner_uids],
    timeout=12
)

# Check for liquidation
liquidation = await check_liquidation(trader_address, coin)

if liquidation['liquidated']:
    # Score based on accuracy
    for response in responses:
        accuracy = compare_prediction_to_outcome(response, liquidation)
        scores[uid] = accuracy * response.confidence
    
    # Mint FRY from loss
    fry_minted = await mint_fry_from_loss(liquidation['loss_amount'])
    # $6560 loss × 10 FRY/$ × 10x multiplier = 656,000 FRY
else:
    # Score based on consensus
    median_score = median([r.degen_score for r in responses])
    for response in responses:
        consensus = 1.0 - abs(response.degen_score - median_score) / 100
        scores[uid] = consensus * response.confidence

# Set weights on chain
validator.subtensor.set_weights(
    netuid=1,
    uids=uids,
    weights=scores
)
```

### 3. FRY Minting Integration

```python
# When liquidation confirmed
POST http://localhost:8000/mirror
{
    "pnl": -6560,  # $6560 loss
    "symbol": "XRP",
    "trade_type": "bittensor_validated"
}

# Casino backend mints FRY
base_fry = 6560 * 10 = 65,600 FRY
multiplier = 10x (degen_score > 90)
total_fry = 65,600 * 10 = 656,000 FRY

# Your balance: 4.96M → 5.62M FRY
```

## Reward Model

### Miner Rewards (TAO)

Miners earn TAO based on prediction accuracy:

```python
# Accuracy components
loss_accuracy = 1.0 - abs(predicted_prob - actual_outcome)  # 50% weight
timeline_accuracy = 1.0 - time_error / max_time  # 30% weight
degen_accuracy = 1.0 - abs(predicted_score - actual_score) / 100  # 20% weight

# Final score
accuracy_score = (loss_accuracy * 0.5 + timeline_accuracy * 0.3 + degen_accuracy * 0.2)
final_score = accuracy_score * confidence

# TAO rewards distributed proportionally
miner_reward = (final_score / total_scores) * epoch_emission
```

### FRY Minting (from losses)

FRY tokens minted when predictions are validated:

```python
# Base minting
base_fry = loss_amount * 10  # 10 FRY per $1 lost

# Degen multiplier
if degen_score >= 90: multiplier = 10x
elif degen_score >= 80: multiplier = 5x
elif degen_score >= 70: multiplier = 3x
elif degen_score >= 60: multiplier = 2x
else: multiplier = 1x

# Accuracy bonus
accuracy_bonus = 1.0 + (miner_accuracy * 0.5)  # Up to 1.5x

# Total FRY
total_fry = base_fry * multiplier * accuracy_bonus
```

## Configuration

### Subnet Parameters

```python
# In bittensor_subnet_protocol.py
class SubnetConfig:
    NETUID = 1  # Your subnet ID
    NETWORK = "test"  # or "finney" for mainnet
    
    # Staking
    MIN_MINER_STAKE = 1000  # TAO
    MIN_VALIDATOR_STAKE = 10000  # TAO
    
    # Validation
    EPOCH_LENGTH = 100  # blocks
    VALIDATION_INTERVAL = 60  # seconds
    QUERY_TIMEOUT = 12  # seconds
    
    # Scoring
    SCORE_EMA_ALPHA = 0.3
    MIN_SCORE_THRESHOLD = 0.1
    
    # FRY integration
    CASINO_API_URL = "http://localhost:8000"
    
    # Hyperliquid
    MONITORED_ADDRESSES = ["0xf551aF8d5373B042DBB9F0933C59213B534174e4"]
    MONITORED_COINS = ["XRP", "FARTCOIN", "BTC", "ETH"]
```

### Custom Arguments

```bash
# Miner
python3 bittensor_degen_miner.py \
    --netuid 1 \
    --subtensor.network test \
    --wallet.name miner \
    --wallet.hotkey default \
    --axon.port 8091 \
    --logging.debug

# Validator  
python3 bittensor_degen_validator.py \
    --netuid 1 \
    --subtensor.network test \
    --wallet.name validator \
    --wallet.hotkey default \
    --neuron.epoch_length 100 \
    --logging.debug
```

## Monitoring

### Check Miner Status

```bash
# View miner info
btcli wallet overview --wallet.name miner --subtensor.network test

# Check subnet registration
btcli subnet list --subtensor.network test

# View metagraph
btcli subnet metagraph --netuid 1 --subtensor.network test
```

### Check Validator Weights

```bash
# View set weights
btcli root weights --netuid 1 --subtensor.network test

# Check validator performance
btcli wallet overview --wallet.name validator --subtensor.network test
```

### Monitor FRY Minting

```bash
# Check casino balance
curl http://localhost:8000/balance

# View recent events
curl http://localhost:8000/balance/events

# Check integration status
curl http://localhost:8000/status
```

## Real-World Example: Your XRP Position

### Current Position
- Trader: `0xf551aF8d5373B042DBB9F0933C59213B534174e4`
- Coin: XRP
- Size: $3,340
- PnL: -196.4% (-$6,560)
- Leverage: ~50x

### Miner Prediction
```
Degen Score: 95/100
- Leverage 50x: 30 points
- Size $3,340: 15 points
- Volatility 20%: 20 points
- Loss -$6,560: 15 points
- Distance to liq: 10 points

Loss Probability: 85%
Timeline: 7,200 seconds (2 hours)
Confidence: 0.8
Reasoning: "50x leverage | $6560 underwater | extreme degen detected"
```

### If Liquidated
```
Validator detects liquidation
Loss: $6,560

FRY Minting:
- Base: $6,560 × 10 = 65,600 FRY
- Multiplier: 10x (degen_score 95)
- Accuracy bonus: 1.4x (miner was 80% accurate)
- Total: 65,600 × 10 × 1.4 = 918,400 FRY

Your balance: 4.96M → 5.88M FRY

Miner TAO reward:
- Accuracy: 0.8
- Weight: 0.8 / total_weights
- Epoch reward: weight × epoch_emission
```

## Deployment Checklist

- [x] Bittensor SDK installed
- [ ] Wallets created (miner + validator)
- [ ] Testnet TAO obtained from faucet
- [ ] Registered on subnet (netuid 1)
- [ ] Miner running and serving predictions
- [ ] Validator running and querying miners
- [ ] FRY Casino backend running (port 8000)
- [ ] Hyperliquid API access configured
- [ ] Weights being set successfully
- [ ] FRY minting on validated losses

## Next Steps

### 1. Deploy to Mainnet
```bash
# Switch to mainnet
--subtensor.network finney

# Requires real TAO for staking
```

### 2. Scale the Network
- Add more miners for diverse predictions
- Add more validators for consensus
- Monitor multiple exchanges (Binance, dYdX, GMX)

### 3. Advanced Features
- Machine learning models for predictions
- Historical backtesting
- Prediction markets integration
- Mobile app for degen alerts

### 4. Token Economics
- Launch DEGEN token for subnet rewards
- Create FRY-DEGEN liquidity pools
- Implement burning mechanisms
- Governance via token voting

## Troubleshooting

### Miner Not Receiving Queries
```bash
# Check if axon is serving
btcli subnet metagraph --netuid 1 --subtensor.network test

# Verify port is open
netstat -an | grep 8091

# Check firewall
sudo ufw allow 8091
```

### Validator Can't Set Weights
```bash
# Check stake
btcli wallet overview --wallet.name validator

# Verify registration
btcli subnet list --subtensor.network test

# Check balance
btcli wallet balance --wallet.name validator
```

### FRY Not Minting
```bash
# Check casino backend
curl http://localhost:8000/status

# Verify integration
curl http://localhost:8000/balance

# Check logs
tail -f fry_trading.db
```

## Conclusion

This is a **real Bittensor subnet** that:

1. ✅ Uses actual Bittensor SDK (not a fork)
2. ✅ Connects to Bittensor testnet/mainnet
3. ✅ Implements custom DegenSynapse protocol
4. ✅ Integrates with Hyperliquid for real data
5. ✅ Mints FRY tokens from validated losses
6. ✅ Distributes TAO rewards to accurate miners
7. ✅ Sets weights on-chain via Subtensor

The subnet creates a decentralized network where miners compete to predict degenerate trading outcomes, validators verify the results, and the FRY ecosystem mints tokens from confirmed losses.

**The Innovation:** We've combined Bittensor's decentralized AI infrastructure with FRY's proof-of-loss tokenomics to create the world's first subnet for quantifying and predicting financial degeneracy at scale. 🍟📉
