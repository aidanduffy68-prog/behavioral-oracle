# Agent B Federated Learning Deployment Guide

## 🚀 Complete System Overview

This deployment guide covers the full Agent B federated learning system with:
- **Flower FL Framework**: Distributed training across venues
- **zkML Proofs**: Privacy-preserving accuracy verification
- **Topology Routing**: Network-aware cross-DEX optimization
- **FRY Alpha Weighting**: Performance-based model aggregation

## 📦 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent B Federated System                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Server (Hub)                    Clients (Venues)                │
│  ┌──────────────────┐           ┌──────────────────┐            │
│  │ FryboyStrategy   │◄──────────┤ Agent B Instance │            │
│  │ • FRY Alpha      │           │ • Binance        │            │
│  │ • zkML Verify    │           │ • Local Training │            │
│  │ • Topology Agg   │           │ • zkML Proofs    │            │
│  │ • On-Chain       │           │ • Topology Route │            │
│  └──────────────────┘           └──────────────────┘            │
│         │                               │                        │
│         │                        ┌──────────────────┐           │
│         │◄───────────────────────┤ Agent B Instance │           │
│         │                        │ • OKX            │           │
│         │                        │ • Local Training │           │
│         │                        │ • zkML Proofs    │           │
│         │                        │ • Topology Route │           │
│         │                        └──────────────────┘           │
│         │                               │                        │
│         │                        ┌──────────────────┐           │
│         └────────────────────────┤ Agent B Instance │           │
│                                  │ • Bybit          │           │
│                                  │ • Local Training │           │
│                                  │ • zkML Proofs    │           │
│                                  │ • Topology Route │           │
│                                  └──────────────────┘           │
│                                                                   │
│  Blockchain Layer                                                │
│  ┌──────────────────────────────────────────────────┐           │
│  │ OnChainVerifier (Smart Contract)                 │           │
│  │ • Verify zkML proofs                             │           │
│  │ • Update client reputation                       │           │
│  │ • Emit ProofVerified events                      │           │
│  └──────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Installation

### 1. Install Dependencies

```bash
cd core
pip install -r fryboy_federated_requirements.txt
```

**Core Dependencies:**
- `flwr==1.6.0` - Federated learning framework
- `torch>=2.6.0` - Neural network training
- `numpy>=1.24.3` - Numerical computing

### 2. Verify Installation

```bash
python3 -c "import flwr; import torch; print('✓ Dependencies installed')"
```

## 🎯 Quick Start

### Option 1: Local Testing (Single Machine)

**Terminal 1 - Server:**
```bash
cd core
python3 fryboy_federated_server.py
```

**Terminal 2 - Client 1 (Binance):**
```bash
cd core
python3 fryboy_federated_client.py binance_agent localhost:8080 binance
```

**Terminal 3 - Client 2 (OKX):**
```bash
cd core
python3 fryboy_federated_client.py okx_agent localhost:8080 okx
```

### Option 2: Production Deployment (Distributed)

**Central Server:**
```bash
# On your aggregation server
python3 fryboy_federated_server.py
```

**Trading Instances:**
```bash
# On Binance trading server
python3 fryboy_federated_client.py binance_agent SERVER_IP:8080 binance

# On OKX trading server
python3 fryboy_federated_client.py okx_agent SERVER_IP:8080 okx

# On Bybit trading server
python3 fryboy_federated_client.py bybit_agent SERVER_IP:8080 bybit
```

## 🔐 zkML Proof System

### How It Works

1. **Client Side**: Generate zero-knowledge proof
```python
# Client proves "RMSE < 0.05" without revealing data
zkml_proof = zkml_generator.generate_accuracy_proof(
    model_predictions=predictions,
    actual_values=actuals,
    validation_features=features,
    threshold=0.05,
    model_hash="global_model_v1"
)
# Send only proof, NOT raw data
```

2. **Server Side**: Verify proof cryptographically
```python
# Server verifies without accessing private data
verification = zkml_verifier.verify_accuracy_proof(proof)
if verification['verified']:
    # Apply 30% weight bonus
    zkml_bonus = 1.3
    # Submit to blockchain
    on_chain_verifier.submit_proof_to_chain(proof)
```

3. **Blockchain**: Update reputation
```python
# Smart contract verifies and updates reputation
tx_result = submit_proof_to_chain(proof)
# Gas cost: ~250k gas
# Reputation score updated on-chain
```

### Privacy Guarantees

✅ **What's Shared:**
- zkML proof (~200 bytes)
- Commitment hash
- Threshold (public)
- Number of samples (public)

❌ **What's NOT Shared:**
- Raw validation data
- Actual RMSE value
- Trading positions
- Hedge ratios
- Feature vectors

## 🌐 Topology Routing

### Network Configuration

The system uses the FRY v3 topology from your visualization:

```python
dex_network = {
    'dYdX': {
        'efficiency': 0.16,  # 16%
        'notional_capacity': 50000,
        'connections': ['Aster', 'Hyperliquid']
    },
    'Aster': {
        'efficiency': 0.12,  # 12%
        'notional_capacity': 30000,
        'connections': ['dYdX', 'Hyperliquid']
    },
    'Hyperliquid': {
        'efficiency': 0.25,  # 25% (hub)
        'notional_capacity': 80000,
        'connections': ['dYdX', 'Aster', 'GMX']
    },
    'GMX': {
        'efficiency': 0.40,  # 40% (highest)
        'notional_capacity': 40000,
        'connections': ['Hyperliquid']
    }
}
```

### Minting Surface Optimization

The system calculates optimal routes using:
- **dy/dx gradients**: Minting surface derivatives
- **Number theory**: GCD and prime factorization bonuses
- **Path efficiency**: Multi-hop route optimization

Example route:
```
dYdX → Hyperliquid → GMX
Gradient: 2.34
FRY Minted: 1,245.67
Efficiency: 92.3%
```

## 📊 Monitoring & Metrics

### Server Metrics

```
Round 10 Aggregation Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Clients: 3 | Avg FRY Weight: 2.8456
Regime Distribution: {'trending_bull': 1, 'volatile': 2}
Total FRY Minted: 45,678.23
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

zkML Proofs Verified:
✓ binance_agent: Proof 10566b15 verified (30% bonus applied)
✓ okx_agent: Proof 2a7f8c3d verified (30% bonus applied)
✓ bybit_agent: Proof 9e4d1a2b verified (30% bonus applied)

Topology Metrics:
  Avg Minting Gradient: 2.14
  Routes via GMX: 67%
  Number Theory Bonus: 1.23x avg
```

### Client Metrics

```
Agent B Client binance_agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Training Round: 10
Samples: 1,247
Private RMSE: 0.0342 (NOT sent to server)
zkML Proof: 10566b15 (VERIFIED)
Topology Routes: 15
Avg Gradient: 2.34
FRY Bonus: 1,245.67
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🎛️ Configuration

### Server Configuration

Edit `fryboy_federated_server.py`:

```python
start_fryboy_server(
    server_address="[::]:8080",
    num_rounds=50,           # Training rounds
    min_clients=2,           # Minimum clients
    fraction_fit=0.5,        # Fraction per round
)

# zkML settings
strategy.zkml_enabled = True
strategy.zkml_threshold = 0.05  # 5% RMSE threshold

# Topology settings
topology_router = TopologyRouter()
topology_router.minting_surface.gradient_threshold = 1.5
```

### Client Configuration

Edit `fryboy_federated_client.py`:

```python
start_fryboy_client(
    server_address="localhost:8080",
    client_id="binance_agent",
    venue="binance",
    initial_capital=1000000,
)

# Model architecture
model = HedgeRatioPredictor(
    input_dim=25,   # 15 base + 10 topology features
    hidden_dim=64
)

# zkML configuration
zkml_generator = ZKMLProofGenerator(client_id)
```

## 🔒 Security Best Practices

### 1. Network Security

```bash
# Use TLS/SSL for production
python3 fryboy_federated_server.py --use-ssl --cert-path /path/to/cert

# Firewall rules
sudo ufw allow 8080/tcp
sudo ufw enable
```

### 2. zkML Security

- **Trusted Setup**: Use production zkML framework (EZKL, Risc0)
- **Proof Verification**: Always verify proofs before aggregation
- **Reputation System**: Track client history on-chain
- **Penalty System**: 50% weight reduction for failed proofs

### 3. Data Privacy

- ✅ Only share model weights and zkML proofs
- ✅ Never log private validation data
- ✅ Use secure enclaves for key material
- ✅ Implement differential privacy if needed

## 📈 Performance Optimization

### 1. Batch Size Tuning

```python
# Larger batches = faster training, more memory
config["batch_size"] = 64  # Default: 32
```

### 2. Learning Rate Schedule

```python
# Adaptive learning rate
base_lr = 0.01
lr_decay = 0.95
learning_rate = base_lr * (lr_decay ** (server_round - 1))
```

### 3. Client Sampling

```python
# Sample more clients for stability
strategy = FryboyAdaptiveStrategy(
    fraction_fit=0.8,  # Use 80% of clients
    min_fit_clients=3,
)
```

### 4. Topology Caching

```python
# Cache topology routes
topology_router.route_cache = {}
# Reuse routes for similar trade sizes
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'v2_circuit_breaker'"

**Solution:**
```bash
cp archive/v2_old/v2_circuit_breaker.py core/
cp archive/v2_old/v2_slippage_engine.py core/
```

### Issue: "zkML proof verification failed"

**Solution:**
- Check proof structure is valid JSON
- Verify commitment hash length (64 chars)
- Ensure timestamp is recent (< 1 hour)
- Check public inputs are valid

### Issue: "Connection refused to server"

**Solution:**
- Verify server is running: `ps aux | grep fryboy_federated_server`
- Check firewall: `sudo ufw status`
- Test connection: `telnet SERVER_IP 8080`

### Issue: "Topology routing failed"

**Solution:**
- Verify DEX network connectivity
- Check trade size is within capacity
- Ensure preferred_dexes are valid
- Review minting surface parameters

## 🔄 Upgrade Path

### From Traditional FL to zkML

1. **Enable zkML on server:**
```python
strategy.zkml_enabled = True
```

2. **Update clients to generate proofs:**
```python
# Already integrated in evaluate()
```

3. **Monitor verification rates:**
```python
summary = zkml_verifier.get_verification_summary()
print(f"Verified: {summary['total_verified']}")
```

### From Basic to Topology-Aware

1. **Add topology features:**
```python
# Already integrated in _extract_features()
```

2. **Configure DEX network:**
```python
topology_router.dex_network['NewDEX'] = {
    'efficiency': 0.35,
    'notional_capacity': 60000,
    'connections': ['Hyperliquid']
}
```

## 📚 Production Checklist

- [ ] Install all dependencies
- [ ] Configure server address and ports
- [ ] Set up TLS/SSL certificates
- [ ] Configure firewall rules
- [ ] Test zkML proof generation
- [ ] Verify topology routing
- [ ] Set up monitoring/logging
- [ ] Configure on-chain verifier
- [ ] Test with 2+ clients
- [ ] Run 10+ training rounds
- [ ] Verify model convergence
- [ ] Check zkML verification rates
- [ ] Monitor FRY minting metrics
- [ ] Set up alerting
- [ ] Document custom configurations

## 🎓 Advanced Features

### Custom Aggregation Weights

```python
def _calculate_fry_alpha_weight(self, metrics: Dict) -> float:
    # Add custom metrics
    custom_metric = metrics.get("your_metric", 0.0)
    custom_bonus = custom_metric * 0.2
    
    return base_weight * (1 + custom_bonus)
```

### Regime-Specific Models

```python
# Store best model per regime
if regime == 'crisis':
    self.regime_models['crisis'] = {
        'parameters': parameters,
        'score': regime_score,
        'round': server_round
    }
```

### Model Rollback

```python
# Rollback to previous version
previous_model = strategy.model_versions[-5]
self.set_parameters(previous_model['parameters'])
```

## 📞 Support

For issues or questions:
- Check logs: `tail -f fryboy_federated_server.log`
- Review metrics in server output
- Verify client connectivity
- Test zkML proofs independently

---

**Built for the FRY Ecosystem** 🍟  
*Privacy-preserving federated learning with topology-aware routing and zkML verification*
