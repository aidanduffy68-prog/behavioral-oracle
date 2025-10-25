# 🍟 Agent B Federated Learning System

**Train Agent B (Fryboy) across distributed trading venues using privacy-preserving federated learning**

## 📋 Quick Summary

This system uses [Flower](https://flower.dev/) to train Agent B across multiple trading instances without sharing raw trading data. Each Agent B learns from its local market conditions while contributing to a global model weighted by **FRY-specific alpha scores**.

> **Note**: "Fryboy" and "Agent B" refer to the same entity - the embedded FRY market maker.

### Key Innovation: FRY Alpha Weighting

Unlike traditional federated learning that uses simple data size weighting, we aggregate models based on:

1. **Hedge Prediction Accuracy** (inverse RMSE) - Core weight
2. **Slippage Harvest Efficiency** - Up to 50% bonus
3. **Funding Arbitrage ROI** - Up to 30% bonus  
4. **FRY Minting Rate** - Up to 20% bonus
5. **Circuit Breaker Penalty** - 40% reduction if active
6. **Regime Confidence** - Weights high-confidence predictions

This ensures the best-performing Agent B instances have more influence on the global model.

## 🗂️ File Structure

```
core/
├── fryboy_federated_server.py      # Flower server with FRY alpha aggregation
├── fryboy_federated_client.py      # Client wrapper for Agent B instances
├── fryboy_federated_demo.py        # Single-process demo for testing
├── fryboy_federated_requirements.txt  # Python dependencies
├── FRYBOY_FEDERATED_SETUP.md       # Detailed setup guide
└── README_FRYBOY_FEDERATED.md      # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r fryboy_federated_requirements.txt
```

### 2. Run Demo (Single Machine)

```bash
python fryboy_federated_demo.py
```

This launches:
- 1 server (aggregator)
- 3 clients (Binance, OKX, Bybit)
- 10 training rounds
- Performance report

### 3. Production Deployment

**Server:**
```bash
python fryboy_federated_server.py
```

**Clients (on separate machines):**
```bash
# Binance instance
python fryboy_federated_client.py binance_agent server_ip:8080 binance

# OKX instance  
python fryboy_federated_client.py okx_agent server_ip:8080 okx

# Bybit instance
python fryboy_federated_client.py bybit_agent server_ip:8080 bybit
```

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Agent B Server (Hub)                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  AgentBAdaptiveStrategy                               │  │
│  │  • FRY Alpha Weighting                                │  │
│  │  • Regime-Specific Model Storage                      │  │
│  │  • Performance Tracking                               │  │
│  │  • Model Versioning (Last 10)                         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Client 1   │      │   Client 2   │      │   Client 3   │
│   (Binance)  │      │    (OKX)     │      │   (Bybit)    │
├──────────────┤      ├──────────────┤      ├──────────────┤
│  Agent B     │      │  Agent B     │      │  Agent B     │
│  Instance    │      │  Instance    │      │  Instance    │
│              │      │              │      │              │
│  Local Data: │      │  Local Data: │      │  Local Data: │
│  • Trades    │      │  • Trades    │      │  • Trades    │
│  • Hedges    │      │  • Hedges    │      │  • Hedges    │
│  • Slippage  │      │  • Slippage  │      │  • Slippage  │
│  • Regimes   │      │  • Regimes   │      │  • Regimes   │
└──────────────┘      └──────────────┘      └──────────────┘
     (Private)             (Private)             (Private)
```

## 🧠 What Gets Trained

### Model: Hedge Ratio Predictor

A neural network that predicts optimal hedge ratios based on:

**Inputs (15 features):**
- LPI score
- Market volatility
- Volume ratio
- Price change %
- Bid-ask spread
- Order flow imbalance
- RSI (normalized)
- Bollinger band position
- Position size (normalized)
- Regime indicators (one-hot: crisis, volatile, trending_bull, trending_bear)
- Regime confidence
- LPI score

**Output:**
- Optimal hedge ratio [0, 1]

**Architecture:**
- Input → 64 hidden → 64 hidden → 32 hidden → 1 output
- ReLU activations, Dropout (0.2), Sigmoid output
- MSE loss, Adam optimizer

## 📊 Performance Metrics

### Server Tracks:
- Total FRY minted across all clients
- Total slippage harvested (USD)
- Total arbitrage profit (USD)
- Average hedge accuracy
- Circuit breaker activations
- Regime distribution

### Client Reports:
- Hedge prediction RMSE
- Slippage harvest efficiency
- Arbitrage ROI %
- FRY mint rate
- Current market regime
- Regime confidence

### Example Output:

```
Round 5 Aggregation Complete
Clients: 3 | Avg FRY Weight: 2.3456
Regime Distribution: {'trending_bull': 1, 'volatile': 2}
Total FRY Minted: 12,345.67

Client binance_agent | Regime: volatile | 
FRY Weight: 2.8901 | Hedge RMSE: 0.0234 | Slippage Eff: 85.00%

Client okx_agent | Regime: trending_bull | 
FRY Weight: 1.9876 | Hedge RMSE: 0.0456 | Slippage Eff: 82.00%

Client bybit_agent | Regime: volatile | 
FRY Weight: 2.1234 | Hedge RMSE: 0.0389 | Slippage Eff: 83.50%
```

## 🔒 Privacy & Security

### What's Shared:
✅ Model weights (neural network parameters)  
✅ Aggregate performance metrics  
✅ Regime classifications  

### What's NOT Shared:
❌ Raw trade data  
❌ Position sizes  
❌ Venue-specific strategies  
❌ Individual trader information  

### Additional Security:
- Optional differential privacy via Flower DP
- Secure aggregation (server can't see individual updates)
- TLS/SSL for production deployments
- Client authentication

## 🎓 Training Process

### Each Round:

1. **Server** sends global model to selected clients
2. **Clients** train locally on their data for 5 epochs
3. **Clients** calculate FRY alpha metrics
4. **Clients** send updated weights + metrics to server
5. **Server** aggregates using FRY alpha weighting
6. **Server** updates regime-specific models
7. **Server** versions the model
8. Repeat for N rounds

### Adaptive Features:

- **Learning rate decay**: 0.01 × 0.95^round
- **Client sampling**: Configurable fraction per round
- **Regime-aware**: Best models stored per regime
- **Early stopping**: Can halt if convergence detected

## 🔧 Customization

### Adjust Aggregation Weights

Edit `_calculate_fry_alpha_weight()` in `fryboy_federated_server.py`:

```python
# Increase slippage bonus from 50% to 100%
slippage_bonus = slippage_efficiency * 1.0  # Was 0.5

# Add custom metric
custom_metric = metrics.get("my_metric", 0.0)
custom_bonus = custom_metric * 0.2
```

### Change Model Architecture

Edit `HedgeRatioPredictor` in `fryboy_federated_client.py`:

```python
# Deeper network
self.network = nn.Sequential(
    nn.Linear(input_dim, 128),  # Larger hidden layer
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(128, 128),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 1),
    nn.Sigmoid()
)
```

### Add New Metrics

In client's `_get_metrics()`:

```python
metrics = {
    # ... existing metrics ...
    'my_custom_metric': self._calculate_custom_metric(),
}
```

Then use in server's weighting function.

## 📈 Expected Results

Based on the ML-enhanced hedging system (from memories):

- **Hedge ratio improvement**: +11.0% over traditional methods
- **Regime-specific gains**: 
  - Crisis: +15.7%
  - Trending Bear: +11.7%
  - Sideways: +10.3%
- **Volatility reduction**: 61.5% in funding rates
- **Capital efficiency**: 7.4x advantage

Federated learning should amplify these gains by:
- Learning from diverse market conditions across venues
- Adapting to regime-specific patterns
- Leveraging collective intelligence of all Agent B instances

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Check server is running, firewall allows port 8080 |
| Insufficient data | Increase collection period or reduce batch size |
| Model divergence | Reduce learning rate or increase min_clients |
| High RMSE | Collect more diverse data or adjust architecture |
| Import errors | Run `pip install -r fryboy_federated_requirements.txt` |

## 📚 Resources

- **Flower Documentation**: https://flower.dev/docs/
- **Federated Learning**: https://en.wikipedia.org/wiki/Federated_learning
- **Setup Guide**: `FRYBOY_FEDERATED_SETUP.md`
- **Agent B Core**: `agent_b_core.py`
- **ML Hedging**: `ml_adaptive_hedging.py`

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Run demo locally
3. ⬜ Test with real market data
4. ⬜ Deploy to staging environment
5. ⬜ Monitor for 24-48 hours
6. ⬜ Scale to production venues
7. ⬜ Iterate based on FRY alpha metrics

## 💡 Key Insights

From the FRY ecosystem memories:

1. **Native Token Denomination**: Losses denominated in native tokens create positive feedback loops
2. **Wreckage Absorption**: Converting losses into FRY minting strengthens the ecosystem
3. **Regime-Aware Learning**: Different market conditions require different strategies
4. **Ensemble Intelligence**: Combining multiple Agent B instances improves overall performance

---

**Built for the FRY Ecosystem** 🍟  
*Training the Phil Ivey of DeFi across the multiverse*
