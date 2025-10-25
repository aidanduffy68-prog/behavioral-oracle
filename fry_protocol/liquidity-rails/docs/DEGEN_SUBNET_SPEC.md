# FRY Degen Subnet Technical Specification

## Overview
A Bittensor-inspired subnet where miners compete to identify the highest-risk trading opportunities and validators score them on actual rekt outcomes. The subnet creates a permissionless network for quantifying and predicting financial degeneracy.

## Core Mechanism

### **Miners: Degen Signal Detection**
Miners scan markets for maximum risk opportunities and submit "degen scores" for trades:

```python
class DegenMiner:
    def scan_markets(self):
        """Find the most degenerate trading opportunities"""
        signals = {
            'leverage': self.detect_max_leverage(),      # 100x+ positions
            'fomo': self.detect_fomo_signals(),          # Parabolic price action
            'liquidity': self.detect_thin_markets(),     # Low liquidity = high slippage
            'volatility': self.detect_vol_spikes(),      # VIX equivalents
            'sentiment': self.detect_euphoria(),         # Social sentiment extremes
        }
        return self.calculate_degen_score(signals)
    
    def submit_prediction(self, trade_id, degen_score):
        """Submit prediction to validators"""
        return {
            'trade_id': trade_id,
            'degen_score': degen_score,  # 0-100 scale
            'predicted_loss': self.estimate_loss_probability(),
            'rekt_timeline': self.estimate_liquidation_time(),
            'miner_id': self.wallet_address
        }
```

### **Validators: Outcome Verification**
Validators track actual outcomes and score miners on prediction accuracy:

```python
class DegenValidator:
    def score_miner(self, prediction, actual_outcome):
        """Score miner based on actual rekt outcome"""
        accuracy_score = self.compare_prediction_to_reality(
            predicted_loss=prediction['predicted_loss'],
            actual_loss=actual_outcome['loss_amount'],
            predicted_timeline=prediction['rekt_timeline'],
            actual_timeline=actual_outcome['liquidation_time']
        )
        
        # Bonus for identifying extreme degens
        if actual_outcome['loss_amount'] > 10000:  # $10k+ loss
            accuracy_score *= 2.0
        
        return accuracy_score
```

## Subnet Architecture

### **1. Registration Requirements**
- **Miners:** Stake 1000 FRY tokens + proof of personal trading losses
- **Validators:** Stake 10000 FRY tokens + $1000+ verified loss history
- **Subnet Creation:** 100k FRY stake + community vote

### **2. Emission Schedule**
```python
EMISSION_SCHEDULE = {
    'total_supply': 21_000_000,  # 21M DEGEN tokens
    'block_time': 12,  # 12 seconds (Bittensor standard)
    'emission_per_block': 1.0,  # 1 DEGEN per block
    'miner_share': 0.41,  # 41% to miners
    'validator_share': 0.41,  # 41% to validators
    'subnet_owner': 0.18,  # 18% to subnet owner
}
```

### **3. Scoring Mechanism**

**Miner Score Formula:**
```python
def calculate_miner_reward(predictions, outcomes):
    """Calculate miner rewards based on prediction accuracy"""
    
    # Base accuracy score
    accuracy = sum([
        compare_prediction(pred, outcome) 
        for pred, outcome in zip(predictions, outcomes)
    ]) / len(predictions)
    
    # Multipliers
    extreme_degen_bonus = count_extreme_predictions(predictions) * 0.1
    consistency_bonus = calculate_consistency(predictions) * 0.2
    speed_bonus = calculate_early_detection(predictions) * 0.15
    
    final_score = accuracy * (1 + extreme_degen_bonus + consistency_bonus + speed_bonus)
    return min(final_score, 10.0)  # Cap at 10x
```

**Validator Score Formula:**
```python
def calculate_validator_reward(miner_scores):
    """Validators earn based on consensus with other validators"""
    
    # Validators who score miners similarly get higher rewards
    consensus_score = calculate_consensus_similarity(miner_scores)
    
    # Bonus for validators who catch miner manipulation
    fraud_detection_bonus = detect_miner_fraud() * 0.3
    
    return consensus_score * (1 + fraud_detection_bonus)
```

## Data Sources & Integration

### **Market Data Feeds**
```python
class DegenDataAggregator:
    def __init__(self):
        self.sources = {
            'hyperliquid': HyperliquidAPI(),
            'binance': BinanceAPI(),
            'coinglass': CoinglassAPI(),
            'dexscreener': DexScreenerAPI(),
            'twitter': TwitterSentimentAPI(),
        }
    
    def aggregate_degen_signals(self):
        """Combine multiple data sources for degen detection"""
        return {
            'leverage_data': self.sources['coinglass'].get_leverage_ratio(),
            'liquidations': self.sources['coinglass'].get_liquidation_data(),
            'new_listings': self.sources['dexscreener'].get_new_tokens(),
            'fomo_score': self.sources['twitter'].get_sentiment_extremes(),
            'funding_rates': self.sources['hyperliquid'].get_funding_rates(),
        }
```

### **Integration with Existing FRY Systems**

**Hyperliquid Loss Mining:**
```python
# When subnet identifies a degen trade that gets rekt
# Automatically mint FRY tokens for the loss
class SubnetFRYIntegration:
    def on_rekt_confirmed(self, trade_outcome):
        """Mint FRY when subnet predictions are confirmed"""
        if trade_outcome['loss_amount'] > 0:
            fry_amount = trade_outcome['loss_amount'] * 10  # 10 FRY per $1 lost
            multiplier = self.calculate_loss_multiplier(trade_outcome)
            
            self.mint_fry(
                amount=fry_amount * multiplier,
                trader=trade_outcome['trader_address'],
                proof=trade_outcome['subnet_prediction_id']
            )
```

**Proof of Loss Consensus:**
```python
# Subnet predictions feed into PoL consensus
class PoLSubnetBridge:
    def submit_to_pol_chain(self, subnet_prediction):
        """Submit subnet predictions to main PoL chain"""
        return {
            'loss_proof': subnet_prediction['actual_outcome'],
            'validator_consensus': subnet_prediction['validator_scores'],
            'degen_score': subnet_prediction['degen_score'],
            'subnet_id': 'degen-subnet-1',
        }
```

## Subnet-Specific Features

### **1. Degen Leaderboard**
```python
class DegenLeaderboard:
    def get_top_degens(self):
        """Track the most accurate degen predictors"""
        return {
            'top_miners': self.get_highest_scoring_miners(),
            'biggest_predictions': self.get_largest_rekt_predictions(),
            'fastest_detections': self.get_earliest_predictions(),
            'consistency_kings': self.get_most_consistent_miners(),
        }
```

### **2. Degen Score Calculation**
```python
def calculate_degen_score(trade_data):
    """0-100 scale of how degen a trade is"""
    
    factors = {
        'leverage': min(trade_data['leverage'] / 100, 1.0) * 30,  # Max 30 points
        'position_size': min(trade_data['size'] / trade_data['account_value'], 1.0) * 25,
        'volatility': min(trade_data['iv'] / 200, 1.0) * 20,
        'liquidity': (1 - min(trade_data['liquidity'] / 1000000, 1.0)) * 15,
        'fomo_factor': trade_data['price_change_24h'] / 100 * 10,
    }
    
    return min(sum(factors.values()), 100)
```

### **3. Rekt Prediction Market**
```python
class RektPredictionMarket:
    def create_market(self, trade_id, degen_score):
        """Create prediction market for rekt outcome"""
        return {
            'market_id': f"rekt_{trade_id}",
            'question': f"Will this {degen_score}/100 degen trade get liquidated?",
            'outcomes': ['REKT', 'SURVIVED', 'MOON'],
            'resolution_time': self.estimate_resolution_time(trade_id),
            'liquidity': self.calculate_market_liquidity(degen_score),
        }
```

## Economic Model

### **Token Utility: DEGEN Token**

**Staking:**
- Miners stake DEGEN to participate
- Validators stake DEGEN to score miners
- Higher stake = higher weight in consensus

**Rewards Distribution:**
```python
class RewardDistribution:
    def distribute_block_rewards(self, block_number):
        """Distribute 1 DEGEN per block"""
        
        total_reward = 1.0
        
        # Miner rewards (41%)
        miner_rewards = self.calculate_miner_rewards(
            total=total_reward * 0.41,
            scores=self.get_miner_scores()
        )
        
        # Validator rewards (41%)
        validator_rewards = self.calculate_validator_rewards(
            total=total_reward * 0.41,
            consensus_scores=self.get_validator_consensus()
        )
        
        # Subnet owner (18%)
        owner_reward = total_reward * 0.18
        
        return {
            'miners': miner_rewards,
            'validators': validator_rewards,
            'owner': owner_reward
        }
```

### **Dual Token System**
- **FRY:** Minted from actual losses (existing system)
- **DEGEN:** Earned from accurate predictions (subnet token)
- **Conversion:** DEGEN can be burned to boost FRY mining multipliers

```python
def burn_degen_for_multiplier(degen_amount):
    """Burn DEGEN tokens to increase FRY mining multiplier"""
    base_multiplier = 1.0
    bonus_multiplier = (degen_amount / 1000) * 0.1  # 0.1x per 1000 DEGEN
    return min(base_multiplier + bonus_multiplier, 10.0)  # Cap at 10x
```

## Anti-Gaming Mechanisms

### **1. Sybil Resistance**
```python
class SybilDetection:
    def detect_coordinated_miners(self, predictions):
        """Detect miners submitting identical predictions"""
        similarity_threshold = 0.95
        
        for miner_a, miner_b in combinations(predictions, 2):
            if self.calculate_similarity(miner_a, miner_b) > similarity_threshold:
                self.flag_potential_sybil(miner_a, miner_b)
```

### **2. Prediction Manipulation Prevention**
```python
class ManipulationPrevention:
    def prevent_self_rekt(self, prediction, trader):
        """Prevent miners from making trades to match their predictions"""
        
        # Check if miner wallet matches trader wallet
        if prediction['miner_id'] == trader['wallet']:
            return False  # Reject prediction
        
        # Check for related wallets
        if self.detect_wallet_relationship(prediction['miner_id'], trader['wallet']):
            return False
        
        return True
```

### **3. Validator Collusion Detection**
```python
class CollusionDetection:
    def detect_validator_collusion(self, validator_scores):
        """Detect validators always scoring the same miners highly"""
        
        for validator in validator_scores:
            favoritism_score = self.calculate_favoritism(validator)
            if favoritism_score > 0.8:  # 80% threshold
                self.penalize_validator(validator)
```

## Technical Stack

### **Blockchain Layer**
- Fork Bittensor's Subtensor blockchain
- Custom consensus: Proof of Loss + Yuma Consensus
- Block time: 12 seconds
- Finality: 100 blocks (~20 minutes)

### **Subnet Runtime**
```python
# Python-based subnet runtime
SUBNET_CONFIG = {
    'subnet_id': 1,  # First FRY subnet
    'name': 'Degen Detection Network',
    'tempo': 360,  # Validator set updates every 360 blocks (~1.2 hours)
    'immunity_period': 7200,  # New miners immune for 7200 blocks (~1 day)
    'min_stake': 1000,  # 1000 FRY minimum stake
    'max_validators': 64,
    'max_miners': 4096,
}
```

### **API Endpoints**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/subnet/degen/predictions")
async def get_active_predictions():
    """Get all active degen predictions"""
    return subnet.get_active_predictions()

@app.get("/subnet/degen/leaderboard")
async def get_leaderboard():
    """Get top miners and validators"""
    return subnet.get_leaderboard()

@app.post("/subnet/degen/submit")
async def submit_prediction(prediction: DegenPrediction):
    """Miners submit predictions"""
    return subnet.submit_prediction(prediction)

@app.post("/subnet/degen/validate")
async def validate_outcome(outcome: TradeOutcome):
    """Validators submit outcome verification"""
    return subnet.validate_outcome(outcome)
```

## Deployment Roadmap

### **Phase 1: Testnet (Month 1-2)**
- Deploy subnet on FRY Chain testnet
- Recruit 10 validators, 100 miners
- Test scoring mechanisms
- Integrate with Hyperliquid testnet

### **Phase 2: Mainnet Launch (Month 3)**
- Deploy on Bittensor mainnet as Subnet #1
- Launch DEGEN token with fair distribution
- Integrate with production Hyperliquid API
- Enable FRY-DEGEN token bridge

### **Phase 3: Expansion (Month 4-6)**
- Add more data sources (Binance, dYdX, GMX)
- Launch prediction market UI
- Mobile app for degen alerts
- Integration with existing FRY Casino

## Revenue Model

### **Subnet Economics**
```python
REVENUE_STREAMS = {
    'subnet_fees': {
        'miner_registration': 100,  # 100 FRY per miner
        'validator_registration': 1000,  # 1000 FRY per validator
        'prediction_fee': 1,  # 1 FRY per prediction
    },
    'prediction_market': {
        'trading_fee': 0.003,  # 0.3% on prediction market trades
        'settlement_fee': 0.001,  # 0.1% on market settlement
    },
    'data_api': {
        'basic_tier': 0,  # Free tier
        'pro_tier': 100,  # 100 DEGEN/month
        'enterprise_tier': 1000,  # 1000 DEGEN/month
    }
}
```

### **Value Accrual**
- Subnet owner earns 18% of block emissions
- Fees collected in FRY are burned (deflationary)
- DEGEN staking rewards from fee revenue
- API access requires DEGEN token holding

## Integration Examples

### **Example 1: Hyperliquid Degen Detection**
```python
# Miner scans Hyperliquid for degen trades
miner = DegenMiner()
degen_trades = miner.scan_hyperliquid()

for trade in degen_trades:
    if trade['leverage'] > 50 and trade['size'] > 10000:
        prediction = miner.submit_prediction(
            trade_id=trade['id'],
            degen_score=95,  # Extremely degen
            predicted_loss=0.8,  # 80% chance of loss
            rekt_timeline=3600  # 1 hour until liquidation
        )
        
        # Earn DEGEN tokens if prediction is accurate
        await subnet.submit(prediction)
```

### **Example 2: Validator Scoring**
```python
# Validator checks actual outcome
validator = DegenValidator()
outcome = validator.fetch_trade_outcome(trade_id)

if outcome['liquidated']:
    # Score all miners who predicted this trade
    for prediction in subnet.get_predictions(trade_id):
        score = validator.score_miner(prediction, outcome)
        
        # Submit score to subnet
        await subnet.submit_score(
            miner_id=prediction['miner_id'],
            score=score,
            validator_signature=validator.sign(score)
        )
```

### **Example 3: FRY Minting Integration**
```python
# When subnet confirms a rekt outcome, mint FRY
class SubnetFRYBridge:
    async def on_rekt_confirmed(self, outcome):
        """Mint FRY when degen prediction confirmed"""
        
        # Calculate FRY amount
        fry_amount = outcome['loss_amount'] * 10
        
        # Apply subnet multiplier
        subnet_multiplier = self.get_subnet_multiplier(outcome['degen_score'])
        total_fry = fry_amount * subnet_multiplier
        
        # Mint FRY tokens
        await fry_minter.mint(
            trader=outcome['trader_address'],
            amount=total_fry,
            proof={
                'subnet_id': 'degen-subnet-1',
                'prediction_id': outcome['prediction_id'],
                'validator_consensus': outcome['validator_scores']
            }
        )
```

## Conclusion

The Degen Subnet creates a permissionless network for:
1. **Identifying** the most degenerate trading opportunities
2. **Predicting** which trades will get rekt
3. **Verifying** actual outcomes with validator consensus
4. **Rewarding** accurate predictions with DEGEN tokens
5. **Minting** FRY tokens from confirmed losses

This subnet transforms degen trading from individual gambling into a collaborative prediction network, where the wisdom of the crowd quantifies and forecasts financial degeneracy at scale.

**The Meta Innovation:** Just as Bittensor decentralizes AI intelligence, the Degen Subnet decentralizes the identification and quantification of financial stupidity.
