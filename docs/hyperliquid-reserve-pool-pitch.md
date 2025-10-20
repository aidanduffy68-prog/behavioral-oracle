# Hyperliquid Reserve Pool Pitch

## The Flywheel (Aster + USDF Model)

**Core concept:**
Reserve pool sits directly in the DEX stack, powering:
1. Hidden orders (dark pool functionality)
2. Internalized flow (reduce external MEV)
3. Fee rebates for terminal users

**For Hyperliquid:**
Replace Aster → HYPE token
Replace USDF → USDC (or native stablecoin)

---

## Pitch to David Knott

### The Problem
Hyperliquid has great infrastructure but leaves value on the table:
- No dark pool for large orders
- Flow goes external (MEV leakage)
- Terminal users pay full fees

### The Solution: HYPE Reserve Pool

**Mechanism:**
1. **Reserve Pool** - HYPE + USDC staked by LPs
2. **Hidden Orders** - Large traders use reserve pool for dark execution
3. **Internalized Flow** - Trades settle against pool, not external venues
4. **Fee Rebates** - Terminal users get rebates funded by pool revenue

**Revenue Sources:**
- Spread capture from internalized flow
- MEV capture (kept in-house vs. leaked to external)
- LP fees from reserve pool usage

**Flywheel:**
- More reserve pool liquidity → Better hidden order execution
- Better execution → More terminal users
- More users → More flow to internalize
- More internalized flow → Higher LP returns
- Higher returns → More reserve pool liquidity

---

## Why This Works for Hyperliquid

**Competitive Advantage:**
- Hyperliquid already has best on-chain perps
- Adding dark pool + internalized flow = institutional-grade
- Fee rebates = stickier users (retention!)

**Synergy with Reverse Oracle:**
- Reserve pool measures *flow* (external data)
- Reverse oracle measures *retention* (internal data)
- Combined = complete picture of user value

**Implementation:**
- HYPE token as reserve asset (creates demand)
- LPs stake HYPE + USDC
- Terminal users get rebates (retention incentive)
- Dark pool for whales (institutional adoption)

---

## Pitch Message

Hey David,

One more thought: we built a reserve pool flywheel for Aster (USDF stablecoin) that could map well to Hyperliquid.

Core idea: reserve pool sits in the DEX stack, powers hidden orders, internalizes flow, and funds fee rebates for terminal users.

For Hyperliquid:
- HYPE + USDC reserve pool
- Dark pool for large orders
- Internalized flow (capture MEV in-house)
- Fee rebates for terminal users (retention!)

Creates a flywheel: more liquidity → better execution → more users → more flow → higher LP returns → more liquidity.

Synergizes with reverse oracle (flow data + retention data = complete user value picture).

Spec here: [link to detailed doc]

Curious if this maps to anything on your roadmap.

Best,
Aidan

Hyperliquid

---

## Technical Spec (If He Asks)

**Reserve Pool Mechanics:**
- LPs deposit HYPE + USDC (50/50 or custom ratio)
- Pool provides liquidity for hidden orders
- Spread captured: 0.02-0.05% per trade
- MEV captured: ~0.1% of internalized flow
- Fee rebates: 0.01% to terminal users

**Hidden Order Flow:**
- Large trader submits hidden order
- Order matched against reserve pool (not public book)
- Execution price = mid-market ± small spread
- No slippage, no front-running

**Internalized Flow:**
- Trades settle against pool instead of external venues
- Reduces MEV leakage to external arbitrageurs
- Pool captures spread + MEV value

**LP Returns:**
- Base APY: 8-12% (from spread + MEV)
- Boosted by HYPE emissions (if applicable)
- Risk: impermanent loss (mitigated by balanced flow)

**Fee Rebates:**
- Terminal users get 0.01% rebate on all trades
- Funded by pool revenue
- Creates retention incentive (cheaper to stay than leave)

---

## Why Now

**Timing:**
- Hyperliquid is dominant on-chain perps
- Next competitive moat = institutional features (dark pool)
- Reserve pool + reverse oracle = complete retention stack

**Precedent:**
- Aster does this with USDF
- Hyperliquid could do it better (more volume, better tech)

**Outcome:**
- Stickier users (fee rebates)
- Institutional adoption (dark pool)
- Higher HYPE token utility (reserve asset)
- Captured MEV (vs. leaked to external)
