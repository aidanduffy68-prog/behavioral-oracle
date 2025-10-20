# FAQ - Token Economics, Competitive Analysis, Implementation

## Token Economics

**Q: What's the FRY supply schedule? Inflation mechanics? How does this avoid becoming another incentive-farming dust token?**

**Supply Schedule:**
- FRY is minted on-demand at 2.26× liquidation value
- No pre-mine, no team allocation, no VC rounds
- Supply grows with liquidation volume (elastic supply)

**Inflation Control:**
- 6-month vesting prevents immediate dump
- Unvested FRY burns if trader churns (deflationary pressure)
- Only ~18% of minted FRY fully vests (based on baseline retention)
- Net inflation = liquidation volume × 2.26 × 0.18 = ~40% of liquidation value

**Anti-Farming Mechanisms:**
1. **Vesting cliff** - No immediate liquidity
2. **Activity multiplier** - Must trade to unlock full value (2.26× boost requires ongoing activity)
3. **Churn burn** - Leave and you lose unvested tokens
4. **Cross-exchange tracking** - Can't farm multiple exchanges (oracle tracks wallet, not venue)

**Why it's not dust:**
- FRY has utility: fee discounts, staking rewards, governance
- Backed by real retention value (not arbitrary emissions)
- Deflationary if retention improves (less churn = more burn)

---

## Competitive Analysis

**Q: What stops every exchange from just building their own retention token? Why is this cross-exchange AMM structure necessary?**

**Nothing stops them. They should.**

But here's why cross-exchange matters:

**Single-Exchange Token Problems:**
1. **Siloed liquidity** - FRY only valuable on one venue
2. **Farming risk** - Traders farm token, dump, move to next exchange
3. **No network effects** - Can't measure cross-exchange retention

**Cross-Exchange AMM Advantages:**
1. **Portable retention** - FRY earned on Hyperliquid works on dYdX
2. **Better data** - Oracle tracks trader across all venues
3. **Anti-farming** - Can't game the system by hopping exchanges
4. **Network effects** - More exchanges = more valuable FRY = better retention

**Competitive Moat:**
- First-mover advantage (we're defining the category)
- Oracle infrastructure (hard to replicate)
- Cross-exchange data (requires partnerships)
- Brand ("reverse oracles" is our term)

**Realistic outcome:**
- Large exchanges (Binance, Coinbase) build internal retention systems
- Mid-tier exchanges (Hyperliquid, dYdX, Vertex) use FRY as shared infrastructure
- We become the "Chainlink for retention" - neutral third party

---

## Implementation Roadmap

**Q: Pilot details matter. Which exchange? What success metrics? Timeline?**

**Phase 1: Data Validation (Current)**
- Run October 10 analysis via Allium
- Validate retention predictions on real liquidation data
- Publish results (Part 3 of research series)
- **Timeline:** 2-4 weeks
- **Success metric:** Prediction accuracy >70%

**Phase 2: Single-Exchange Pilot (Q1 2026)**
- **Target exchange:** Hyperliquid (most receptive, best data access)
- **Pilot structure:**
  - 1,000 liquidated traders receive FRY
  - 6-month vesting, 2.26× multiplier
  - Track 30-day return rate vs. control group
- **Success metrics:**
  - 30-day return rate: >30% (vs. 18% baseline)
  - 90-day LTV: 2× control group
  - FRY token liquidity: >$100k daily volume
- **Timeline:** 3-6 months

**Phase 3: Cross-Exchange Expansion (Q2-Q3 2026)**
- Integrate with 2-3 additional exchanges (dYdX, Vertex, Drift)
- Launch cross-exchange oracle (track wallets across venues)
- Expand AMM to support multi-venue liquidity
- **Success metrics:**
  - 3+ exchanges live
  - 10,000+ traders using FRY
  - Cross-exchange retention data validated
- **Timeline:** 6-9 months

**Phase 4: Decentralization (Q4 2026)**
- Transition oracle to decentralized network
- Launch governance token (separate from FRY)
- Open-source AMM contracts
- **Success metrics:**
  - 10+ exchanges integrated
  - $10M+ TVL in retention AMM
  - Self-sustaining economics
- **Timeline:** 12+ months

**Immediate Next Steps (Post-Launch):**
1. Secure Allium data access (in progress)
2. Run Oct 10 validation analysis
3. Present results to Hyperliquid (David Knott conversation)
4. Negotiate pilot terms
5. Deploy pilot contracts on testnet

---

## Risk Mitigation

**What could go wrong:**

1. **Exchanges don't adopt** - Mitigation: Start with one willing partner (Hyperliquid), prove ROI
2. **Token becomes dust** - Mitigation: Utility (fee discounts), vesting, burn mechanics
3. **Farmers exploit system** - Mitigation: Cross-exchange tracking, activity multipliers
4. **Regulatory issues** - Mitigation: FRY as utility token, not security; no pre-mine
5. **Oracle manipulation** - Mitigation: Decentralized validation, multiple data sources

**Why this is worth the risk:**
- 82% churn is an existential problem for exchanges
- No one else is solving this
- First-mover advantage in new oracle category
- Worst case: We validate the concept, someone else executes (still a win for the space)

---

## Open Questions

**Still figuring out:**
1. Optimal vesting schedule (6 months vs. 12 months?)
2. Activity multiplier mechanics (linear vs. exponential?)
3. Cross-exchange oracle design (centralized vs. decentralized?)
4. Governance structure (who controls retention parameters?)
5. Fee model (how do we capture value as infrastructure provider?)

**Community feedback needed on:**
- Token utility beyond fee discounts
- Fair launch vs. strategic allocation
- Oracle decentralization timeline
- AMM fee structure
