# Agent B Federated Learning Setup Guide

## 🚀 Overview

This federated learning system trains Agent B (aka "Fryboy") across distributed trading instances using Flower FL framework. Each Agent B instance learns from its local market data while contributing to a global model without sharing raw trading data.

> **Terminology**: "Fryboy" and "Agent B" refer to the same entity - the embedded FRY market maker. Agent B is the official name used throughout the codebase.

## 🎯 Key Features

### Server-Side (`fryboy_federated_server.py`)
- **FRY Alpha Weighting**: Aggregates models weighted by hedge accuracy, slippage efficiency, and arbitrage ROI
- **Regime-Aware Learning**: Maintains separate models for different market regimes (crisis, trending, volatile, etc.)
- **Performance Tracking**: Monitors global FRY minting, slippage harvesting, and arbitrage profits
- **Model Versioning**: Keeps last 10 model versions for rollback capability
- **Adaptive Learning Rates**: Automatically adjusts learning rate based on training round

### Client-Side (`fryboy_federated_client.py`)
- **Privacy-Preserving**: Only shares model weights, never raw trading data
- **Local Training**: Trains hedge ratio predictor on venue-specific data
- **Real-Time Metrics**: Reports FRY-specific performance to server
- **Automatic Data Collection**: Integrates with existing Agent B infrastructure
- **Fault Tolerance**: Handles disconnections and reconnections gracefully

## 📦 Installation

### 1. Install Dependencies

```bash
cd core
pip install -r fryboy_federated_requirements.txt
```

### 2. Verify Installation

```bash
python -c "import flwr; import torch; print('Flower:', flwr.__version__); print('PyTorch:', torch.__version__)"
```

Expected output:
```
Flower: 1.6.0
PyTorch: 2.1.0
```

## 🏃 Quick Start

### Option 1: Single Machine (Testing)

**Terminal 1 - Start Server:**
```bash
python fryboy_federated_server.py
```

**Terminal 2 - Start Client 1:**
```bash
python fryboy_federated_client.py fryboy_client_1 localhost:8080 binance
```

**Terminal 3 - Start Client 2:**
```bash
python fryboy_federated_client.py fryboy_client_2 localhost:8080 okx
```

### Option 2: Distributed Setup (Production)

**Server (Central Hub):**
```bash
# On your central server
python fryboy_federated_server.py
```

**Client 1 (Binance Trading Instance):**
```bash
# On Binance trading server
python fryboy_federated_client.py binance_agent server_ip:8080 binance
```

**Client 2 (OKX Trading Instance):**
```bash
# On OKX trading server
python fryboy_federated_client.py okx_agent server_ip:8080 okx
```

**Client 3 (Bybit Trading Instance):**
```bash
# On Bybit trading server
python fryboy_federated_client.py bybit_agent server_ip:8080 bybit
```

## ⚙️ Configuration

### Server Configuration

Edit `fryboy_federated_server.py`:

```python
start_fryboy_server(
    server_address="[::]:8080",      # Server address
    num_rounds=50,                    # Training rounds
    min_clients=2,                    # Minimum clients required
    fraction_fit=0.5,                 # Fraction of clients per round
)
```

### Client Configuration

Edit `fryboy_federated_client.py`:

```python
start_fryboy_client(
    server_address="localhost:8080",  # Server address
    client_id="fryboy_client_1",      # Unique client ID
    venue="binance",                   # Trading venue
    initial_capital=1000000,           # Starting capital
)
```

## 📊 Monitoring Performance

### Server Metrics

The server logs comprehensive metrics after each round:

```
Round 5 Aggregation Complete
Clients: 3 | Avg FRY Weight: 2.3456
Regime Distribution: {'trending_bull': 1, 'volatile': 2}
Total FRY Minted: 12,345.67
```

### Client Metrics

Each client reports:
- **Hedge RMSE**: Prediction accuracy (lower is better)
- **Slippage Efficiency**: Harvest efficiency percentage
- **Arbitrage ROI**: Return on arbitrage trades
- **FRY Mint Rate**: FRY tokens minted per round
- **Market Regime**: Current detected regime

### Final Report

After training completes, the server generates a comprehensive report:

```
FRYBOY FEDERATED LEARNING PERFORMANCE REPORT
======================================================================
Global Metrics:
  Training Rounds: 50
  Total FRY Minted: 125,432.18
  Total Slippage Harvested: $456,789.23
  Total Arbitrage Profit: $89,234.56
  Avg Hedge Accuracy: 0.8234
  Circuit Breaker Activations: 3

Regime-Specific Models:
  TRENDING_BULL: Score=3.4567, Round=45, Clients=2
  VOLATILE: Score=2.8901, Round=38, Clients=3
  CRISIS: Score=4.1234, Round=12, Clients=2
```

## 🔧 Advanced Usage

### Custom Aggregation Weights

Modify `_calculate_fry_alpha_weight()` in `fryboy_federated_server.py`:

```python
def _calculate_fry_alpha_weight(self, metrics: Dict) -> float:
    # Customize weighting formula
    hedge_rmse = metrics.get("hedge_rmse", 1.0)
    base_weight = 1.0 / max(hedge_rmse, 0.01)
    
    # Add your custom bonuses
    custom_bonus = metrics.get("your_metric", 0.0) * 0.3
    
    return base_weight * (1 + custom_bonus)
```

### Regime-Specific Training

Enable regime-specific model selection:

```python
# In client configuration
config = {
    "enable_regime_detection": True,
    "regime_specific_training": True,
    "target_regime": "crisis",  # Focus on crisis scenarios
}
```

### Model Rollback

Access previous model versions:

```python
# In server
strategy = FryboyAdaptiveStrategy(...)

# Get model from 5 rounds ago
previous_model = strategy.model_versions[-5]
```

## 🎓 Training Best Practices

### 1. Client Selection
- **Minimum 2 clients** for meaningful aggregation
- **Diverse venues** for better generalization
- **Similar capital sizes** for balanced learning

### 2. Training Rounds
- **Start with 20-30 rounds** for initial testing
- **50-100 rounds** for production deployment
- **Monitor convergence** and stop early if needed

### 3. Learning Rate Schedule
- **Default**: 0.01 with 0.95 decay per round
- **Aggressive**: 0.05 for faster convergence
- **Conservative**: 0.001 for stable training

### 4. Data Quality
- **Minimum 1000 samples** per client per round
- **80/20 train/validation split**
- **Shuffle data** between epochs

## 🔒 Security & Privacy

### Data Privacy
- ✅ Only model weights are shared (not raw trades)
- ✅ Differential privacy can be added via Flower DP
- ✅ Secure aggregation prevents server from seeing individual updates

### Network Security
- Use **TLS/SSL** for production deployments
- Implement **client authentication**
- Set up **firewall rules** for server access

### Production Deployment
```bash
# Use secure connection
python fryboy_federated_server.py --use-ssl --cert-path /path/to/cert
```

## 🐛 Troubleshooting

### Issue: "Connection refused"
**Solution**: Ensure server is running and firewall allows port 8080

### Issue: "Insufficient training data"
**Solution**: Increase data collection period or reduce batch size

### Issue: "Model divergence"
**Solution**: Reduce learning rate or increase min_clients

### Issue: "High RMSE"
**Solution**: Collect more diverse training data or adjust model architecture

## 📈 Performance Optimization

### 1. Batch Size Tuning
```python
# Larger batches = faster training, more memory
config["batch_size"] = 64  # Default: 32
```

### 2. Local Epochs
```python
# More epochs = better local fit, slower rounds
config["local_epochs"] = 10  # Default: 5
```

### 3. Client Sampling
```python
# Sample more clients per round for stability
strategy = FryboyAdaptiveStrategy(
    fraction_fit=0.8,  # Use 80% of available clients
)
```

## 🔗 Integration with Existing Systems

### Agent B Integration

The federated client automatically integrates with your existing Agent B instance:

```python
# Your existing Agent B
agent_b = AgentB(initial_capital=1000000)

# Wrap with federated client
client = FryboyClient(
    client_id="my_agent",
    agent_b=agent_b,  # Use existing instance
    model=HedgeRatioPredictor(),
    venue="binance",
)
```

### Real-Time Data Integration

Replace synthetic data generation with real market data:

```python
def _collect_training_data(self):
    # Replace this with your real data source
    market_data = self.agent_b.get_recent_market_data()
    
    for data_point in market_data:
        features = self._extract_features(data_point)
        label = self._calculate_optimal_hedge(data_point)
        self.training_buffer.append((features, label))
```

## 📚 Next Steps

1. **Test locally** with 2-3 clients on same machine
2. **Deploy to staging** with real market data
3. **Monitor performance** for 24-48 hours
4. **Scale to production** with multiple venues
5. **Iterate and improve** based on FRY alpha metrics

## 🤝 Support

For issues or questions:
- Check logs in `fryboy_federated_server.log`
- Review client logs for connection issues
- Verify network connectivity between server and clients

---

**Built for the FRY Ecosystem** 🍟
*Training Fryboy to clip edges across the multiverse*
