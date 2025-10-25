# Liquidity Rails System - Deployment Guide

## System Components

1. **Liquidity Rails Engine** - Optimal wreckage routing across venues
2. **Agent B Market Maker** - Slippage harvesting + adaptive hedging
3. **Wreckage Matching** - P2P funding rate swaps
4. **Topology Router** - Minting surface optimization
5. **zkML Proofs** - Privacy-preserving accuracy verification
6. **Confidential Positions** - Pedersen commitments for private collateral

## Quick Deploy

### Prerequisites
```bash
python3 -m pip install -r fryboy_federated_requirements.txt
```

### Start System
```bash
# 1. Start liquidity rails
python3 liquidity_rails_engine.py

# 2. Start wreckage matching
python3 fry_wreckage_matching_engine.py

# 3. Start integrated system
python3 liquidity_rails_integration.py
```

## Production Deployment

### Environment Setup
```bash
export FRY_ENV=production
export FRY_CAPITAL=10000000
export FRY_VENUES="dYdX,Hyperliquid,Aster,GMX,Vertex"
```

### Deploy to Cloud
```bash
# Docker deployment
docker build -t fry-liquidity-rails .
docker run -d -p 8080:8080 fry-liquidity-rails

# Kubernetes
kubectl apply -f k8s/liquidity-rails-deployment.yaml
```

## Monitoring

- Liquidity utilization: Track via `get_liquidity_summary()`
- FRY minting rate: Monitor `effective_rate`
- P2P match rate: Check `matched_pairs`
- Capital allocation: Review `capital_allocations`

## Built for FRY 🍟
