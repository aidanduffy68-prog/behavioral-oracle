# Bigger Items - Save for Later

## High Priority (Post-Launch)

### 1. Implement Public Retention Metrics Dashboard
**What:** Live dashboard showing real retention data
**Why:** Proves the oracle is working, builds credibility
**Effort:** Medium (2-3 days)
**Deliverable:**
- Public page showing tracked wallets (anonymized)
- Days since liquidation
- Return activity (yes/no)
- Current retention rate vs baseline

### 2. Reach Out to Drift/Vertex for Pilot Partnership
**What:** Close one small exchange integration
**Why:** Need proof-of-concept partnership for credibility
**Effort:** Low (outreach) + High (integration if accepted)
**Pitch template:** Already created in reality-check doc
**Target:** Drift (Solana) or Vertex (Arbitrum)

### 3. Run Allium Oct 10 Analysis
**What:** Validate retention predictions on real liquidation data
**Why:** Needed for Part 3 article and Hyperliquid pitch
**Effort:** Medium (depends on Allium data access)
**Deliverable:** Part 3 article with real validation results

## Medium Priority

### 4. Update Monday Launch Copy
**What:** Adjust LinkedIn/X posts to be more honest about current state
**Why:** Avoid overpromising, build trust
**Effort:** Low (30 minutes)
**Changes:**
- "Could reduce churn 82% → 50%" becomes "Early data shows promise, full results November 10"
- Add transparency about MVP vs full vision

### 5. Publish Daily Retention Metrics (Starting November)
**What:** Weekly updates showing retention data
**Why:** Transparency, engagement, proof of work
**Effort:** Low (once dashboard is built)
**Format:** GitHub README updates + LinkedIn posts

## Low Priority

### 6. Separate Prediction Markets Documentation
**What:** Create separate docs for prediction markets feature
**Why:** Avoid confusing retention oracle narrative
**Effort:** Low (1 hour)
**Deliverable:** `docs/prediction-markets.md`

### 7. Design Bonding Curve AMM Contracts
**What:** Implement full AMM mechanics from article
**Why:** Close gap between vision and code
**Effort:** High (1-2 weeks)
**Deliverable:** Solidity contracts for bonding curve + LP pools

---

## Sequencing

**This week (pre-launch):**
- ✅ README transparency updates (done)
- Update Monday launch copy (30 min)

**Week of Oct 21 (post-launch):**
- Reach out to Drift/Vertex (1 day)
- Start Allium Oct 10 analysis (ongoing)

**Week of Oct 28:**
- Build public retention metrics dashboard (2-3 days)
- Publish first retention data update

**November:**
- Weekly retention metrics updates
- Close pilot partnership (if Drift/Vertex responds)
- Publish Part 3 with Allium validation

---

## Decision Points

**If David Knott responds positively:**
- Prioritize Hyperliquid pilot over Drift/Vertex
- Focus on community validation (Discord post)

**If no partnerships by mid-November:**
- Pivot to public data validation
- Use Oct 10 analysis as standalone proof
- Target smaller protocols (GMX, Gains Network)

**If retention data is weak (<30% at 30 days):**
- Be honest about it
- Analyze why (sample size? incentive structure?)
- Iterate on FRY mechanics before scaling
