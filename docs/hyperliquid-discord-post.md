# Hyperliquid Discord Post - Reverse Oracles

## Community Research Section Post

**Title:** Reverse Oracles for Trader Retention - Looking for Feedback

---

**Post:**

Hey Hyperliquid community,

Been researching October 10 and built something I'd love feedback on: **reverse oracles**.

**The concept:**
Traditional oracles measure asset prices (BTC/USD, ETH/USD). Reverse oracles measure trader behavior (retention, churn, LTV).

**The problem:**
82% of liquidated traders quit forever. That's massive LTV loss for exchanges and a death spiral for liquidity.

**The solution:**
Reverse oracle + Retention AMM that:
- Measures which traders return post-liquidation
- Predicts 30-day return rates
- Automates retention incentives (FRY token allocation)
- Could reduce churn from 82% → 50%

**October 10 counterfactual:**
- 1.6M traders liquidated
- Without intervention: 1.3M quit forever
- With FRY allocation: 800K retained
- 2.7× improvement in retention

**Full spec:** DM me for the article link (Discord blocks external URLs)

**Questions for the community:**
1. Would you want retention incentives after getting liquidated?
2. Does 6-month vesting make sense? (prevents dump, creates re-engagement)
3. What metrics matter most? (30-day return rate, LTV, activity?)
4. Any concerns about fairness/bias toward certain trader types?

Running analysis on actual Oct 10 data via Allium to validate predictions. Happy to share results.

Built for the 82% who quit. 🍟

---

## Alternative: Shorter Version

**Title:** Reverse Oracles - Feedback Wanted

Hey everyone,

Built a reverse oracle that measures trader retention instead of asset prices. Could reduce post-liquidation churn from 82% → 50%.

Full spec: DM me for the article link (Discord blocks external URLs)

**Quick question:** Would you want retention incentives (FRY tokens) after getting liquidated? Or would you rather just move on?

Trying to validate if this is actually useful for the community.

Thanks 🍟

---

## Alternative: Technical Version

**Title:** [Research] Reverse Oracle Architecture for Trader Retention

**Abstract:**
Proposing a new oracle category that measures on-chain user behavior instead of external market prices. Specifically designed to predict and automate trader retention post-liquidation.

**Architecture:**
- Retention oracle tracks 30-day return rates, LTV, churn signals
- Bonding curve prices retention incentives (cheap early, expensive late)
- AMM automates FRY token allocation based on predicted retention probability
- Self-regulating feedback loop adjusts pricing based on actual outcomes

**October 10 Analysis:**
- Baseline: 82% churn (1.3M of 1.6M liquidated traders quit)
- With FRY: 50% churn (800K retained)
- 2.7× improvement in retention
- $15.8B LTV saved

**Implementation:**
- Oracle: Python + SQLite (tracks wallet activity)
- AMM: Solidity contracts (bonding curve + LP pools)
- Integration: Works with any exchange oracle/liquidity layer

**Full technical spec:** [Mirror link]
**Code:** https://github.com/aidanduffy68-prog/USD_FRY

**Looking for feedback on:**
- Oracle design patterns
- AMM mechanics (bonding curve parameters)
- Fairness/bias concerns
- Integration with HLP vaults

---

## Recommended: First Version

The first version is best for Discord. It's:
- Clear and accessible (not too technical)
- Asks specific questions (drives engagement)
- Shows you've done the work (Oct 10 analysis)
- Casual tone (fits Discord culture)

The technical version is better for a forum post or GitHub discussion.
