# USD_FRY: Turning Trading Losses Into Productive Assets

**TL;DR**: We built infrastructure that converts DEX trading losses into a stablecoin with 7.4x better capital efficiency than traditional approaches.

---

## The Problem: $50M+ in Daily Wreckage

Every day, decentralized exchanges generate massive losses from:
- Liquidations (longs/shorts getting rekt)
- Slippage (price moves against you mid-trade)
- Funding rate payments (perps bleeding money)
- Getting picked off by informed traders

Traditional solution? Socialize the losses across all LPs. Everyone loses.

## The FRY Solution: Liquidity Rails

We built a three-tier system that routes losses through optimal paths:

### Tier 1: P2P Matching (1.4 FRY per $1)
If you're paying funding and someone else is receiving it, we match you directly. Cash-settled swap, no token transfers. Both sides mint enhanced FRY.

### Tier 2: Liquidity Rails (1.2-2.2 FRY per $1)
Smart routing across 5+ DEXes (Hyperliquid, Aster, dYdX, GMX, Vertex). Multi-hop paths, liquidity aggregation, efficiency bonuses.

### Tier 3: Agent B AI (0.8-1.0 FRY per $1)
ML-enhanced market maker as fallback. Slippage harvesting, adaptive hedging, reinforcement learning. +11% better than traditional hedging.

**Result**: 2.26 FRY per $1 average (vs 0.5 base rate)

---

## Why This Works: Native Token Magic

Here's the key insight: **denominate losses in the DEX's native token, not USD**.

When you measure losses in $HYPE or $USDF instead of USDC:
- Higher token price → More valuable loss pool
- More FRY minted per dollar of losses
- Creates positive feedback loop

**Proof**: 61.5% reduction in funding rate volatility, 7.4x capital efficiency advantage.

---

## Privacy Layer: zkML + Pedersen Commitments

**Problem**: Market makers don't want to reveal their positions/strategies.

**Solution**:
- **zkML proofs** (EZKL): Prove your model works without showing validation data
- **Pedersen commitments**: Hide collateral amounts while proving you're not overleveraged
- **Federated learning**: Train AI across venues without sharing raw data

Bonus: 30% higher FRY minting rate if you provide zkML proofs.

---

## The Numbers

**Test Results** (20 wreckage events):
- $2.33M wreckage processed
- 3.74M FRY minted
- 221% improvement vs base rate
- 57% average liquidity utilization

**ML Performance**:
- +11% hedge ratio optimization
- +15.7% in crisis scenarios
- 85%+ regime detection accuracy

**Capital Efficiency**:
- 7.4x vs traditional stablecoins
- 61.5% funding rate volatility reduction
- 70% liquidity rails / 30% AI reserve allocation

---

## Who This Is For

**DEXes**: Reduce LP losses, stabilize funding rates, attract liquidity

**Market Makers**: Convert losses to FRY, access optimal routes, ML-enhanced hedging

**Liquidity Providers**: Earn FRY from provision, reduced IL, confidential positions

---

## The Tech Stack

- **Routing**: Dynamic programming for optimal paths (up to 3 hops)
- **Matching**: Cash-settled funding swaps (no token transfers)
- **AI**: Reinforcement learning + regime detection
- **Privacy**: EZKL zkML + Pedersen commitments
- **Contracts**: Solidity on Arbitrum (ready for audit)

All production-ready. All open source.

---

## What Makes This Different

**Traditional stablecoins**: Backed by fiat or crypto reserves
**Native stablecoins** (USDF/USDH): Backed by DEX native tokens
**USD_FRY**: Backed by *wreckage* (trading losses)

We're not competing with USDC. We're infrastructure for native stablecoin DEXes to recycle losses productively.

---

## Roadmap

**Q1 2026**:
- 10+ DEX integrations
- $50M+ TVL
- 500+ Agent B instances

**Q2 2026**:
- Cross-chain (Solana, Base)
- Advanced ML (transformers)
- Options market

---

## Try It

**Website**: https://aidanduffy68-prog.github.io/USD_FRY/
**GitHub**: https://github.com/aidanduffy68-prog/USD_FRY
**Docs**: Full technical whitepaper available

Built by liquidity engineers. Powered by Greenhouse & Company.

---

*The first wreckage-backed stablecoin. Because losses shouldn't be wasted.* 🍟
