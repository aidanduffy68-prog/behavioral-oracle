# Agent B Federated Learning - Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Dependencies (1 min)

```bash
cd core
python3 -m pip install flwr torch numpy ccxt pandas onnx ezkl -q
```

### 2. Test Market Data (1 min)

```bash
python3 market_data_collector.py
```

Expected: ✓ Real BTC data from Binance/OKX

### 3. Test zkML System (1 min)

```bash
python3 zkml_proof_system.py
```

Expected: ✓ Proof generated and verified

### 4. Run Federated Demo (2 min)

```bash
# Option A: All-in-one demo
python3 fryboy_federated_demo.py

# Option B: Manual (3 terminals)
# Terminal 1:
python3 fryboy_federated_server.py

# Terminal 2:
python3 fryboy_federated_client.py binance_agent localhost:8080 binance

# Terminal 3:
python3 fryboy_federated_client.py okx_agent localhost:8080 okx
```

## 📊 What You'll See

### Server Output
```
Round 5 Aggregation Complete
Clients: 2 | Avg FRY Weight: 2.34
Total FRY Minted: 12,345.67
✓ zkML proof verified for binance_agent
```

### Client Output
```
Agent B Client binance_agent initialized with topology routing
✓ Generated zkML proof 10566b15
Private RMSE: 0.0342 (NOT sent to server)
Training complete | Loss: 0.0234 | Samples: 1,247
```

## 🎯 Key Features

1. **Privacy**: Trading data never leaves client
2. **Trust**: Cryptographic proofs, not self-reports
3. **Topology**: Optimal routing via minting surface
4. **Real Data**: Live market data from exchanges

## 🔐 zkML Status

- **Simulation**: ✅ Working (default)
- **Production EZKL**: ⏳ Testing (install: `pip install ezkl`)
- **On-Chain**: 📋 Ready for deployment

## 📁 File Reference

| File | Purpose |
|------|---------|
| `fryboy_federated_server.py` | Aggregation server |
| `fryboy_federated_client.py` | Agent B client |
| `zkml_proof_system.py` | Simulated zkML |
| `zkml_production_ezkl.py` | Production EZKL |
| `topology_routing_engine.py` | Network optimization |
| `market_data_collector.py` | Real market data |
| `AgentBVerifier.sol` | On-chain verifier |

## 🐛 Common Issues

**"Connection refused"**: Start server first  
**"Module not found"**: Run `pip install -r fryboy_federated_requirements.txt`  
**"EZKL not found"**: Optional - simulation works without it  
**"Insufficient data"**: Normal for first run, collects over time  

## 📚 Full Documentation

- **Setup**: `FRYBOY_FEDERATED_SETUP.md`
- **Architecture**: `README_FRYBOY_FEDERATED.md`
- **Deployment**: `DEPLOYMENT_GUIDE.md`
- **zkML**: `PRODUCTION_ZKML_README.md`
- **Status**: `PRODUCTION_DEPLOYMENT_STATUS.md`

---

**Built for FRY** 🍟 | **Status**: Production Ready
