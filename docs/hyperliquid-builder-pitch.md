# Hyperliquid Builder Pitch - Reverse Oracle for HLP

## Quick LinkedIn Note (Friend of Friend)

Hey [Name],

[Mutual friend] mentioned you're building on HLP.

Quick thought: built a reverse oracle that measures trader retention instead of prices. Could help HLP vaults predict which LPs are sticky vs. mercenary.

Spec here: [Mirror link]

Curious if this maps to anything you're working on.

Best,
Aidan

---

## Why This Works for HLP Builders

**The problem:**
- HLP (Hyperliquid Liquidity Provider) vaults need to differentiate
- Everyone competes on APY, but retention is the real metric
- No way to measure which LPs will stay vs. farm-and-exit

**The pitch:**
- Reverse oracle measures LP behavior (deposits, withdrawals, duration)
- Predicts which LPs are sticky vs. mercenary
- Vaults can optimize incentives for high-LTV providers

**The hook:**
- Hyperliquid's on-chain oracle is great for prices
- But you still need behavioral data for retention
- That's what reverse oracles solve

---

## Alternative Angle: Trader Retention for HLP Profitability

**HLP makes money when:**
- Traders lose (HLP is the house)
- Traders keep trading (volume = fees)

**HLP loses money when:**
- Traders quit after liquidation (no more volume)
- One-time users don't return

**Reverse oracle value prop:**
- Predict which traders will return post-liquidation
- Allocate retention incentives (FRY, fee rebates) to high-LTV traders
- Maximize HLP long-term profitability

---

## Call to Action

"If you're building on HLP and retention matters, let's chat. Built the first reverse oracle for trader behavior—might be useful for vault optimization."
