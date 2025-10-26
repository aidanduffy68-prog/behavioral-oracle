# Red Teaming Behavioral Oracles

## I spent a week trying to steal from my own protocol. Here's what I found.

Most DeFi projects get hacked because builders don't think like attackers.

They build for the "happy path"—the normal, legitimate user flow. Then attackers find the edge cases, exploit the assumptions, and drain $100M.

I built FRY (a behavioral oracle for trader retention) assuming everything would be attacked. Then I proved it.

Here's what happened when I created 2,780 fake wallets and tried to break my own system.

## The Thesis: Security is "We Found Where It Breaks"

This isn't a story about building a perfect system. This is about **finding the flaws before real attackers do.**

Traditional security thinking:
- "We audited the code"
- "We tested the happy path"  
- "We deployed to mainnet"

Actual security thinking:
- "I'm going to try to steal $1M worth of tokens"
- "How would I exploit this system if I were malicious?"
- "Let me simulate attacks at scale"

**That's what I did.**

## The Methodology: 2,780 Attack Wallets Across 10 Scenarios

I built a red team testing framework that simulates realistic attacks against FRY's behavioral oracle.

### Attack Scenarios Tested

**1. Sybil Farming (HIGH Severity)**
- Create 1,000+ fake wallets
- Get intentionally liquidated with $10 positions
- Claim FRY tokens on all wallets
- Dump on market

**2. Collusion Ring (HIGH Severity)**  
- 10+ traders coordinate wash trades
- Create fake "behavioral patterns"
- Oracle thinks they're legitimate clusters
- All claim retention incentives

**3. Retention Gaming (MEDIUM Severity)**
- Get liquidated, claim FRY
- Return to platform briefly (show as "retained")
- Immediately withdraw and leave forever

**4. Oracle Manipulation (CRITICAL Severity)**
- Manipulate price feeds or liquidation data
- Trigger false FRY claims
- Could drain entire treasury

**5. Cross-Chain Sybil (HIGH Severity)**
- Use different wallets on each chain
- Bypass single-chain detection
- Each chain thinks you're separate users

**6. MEV Frontrunning (MEDIUM Severity)**
- Frontrun liquidation events
- Claim FRY before legitimate users
- Reduce rewards for real users

**7. Incentive Gaming (MEDIUM Severity)**
- Make 1 trade every 29 days
- Maintain "active" status
- Farm 2× FRY multipliers without real engagement

**8. Smart Contract Exploit (CRITICAL Severity)**
- Find vulnerability in FRY token or oracle contracts
- Could drain entire system

**9. Governance Attack (HIGH Severity)**
- Acquire majority of FRY tokens
- Control protocol parameters
- Change retention incentives

**10. Spam Attack (LOW Severity)**
- Create many small liquidations
- Spam the system with noise

## The Results: 99.1% Detection Rate (But the 0.9% Could Be Expensive)

### Overall Performance
- **2,780 total attack wallets tested**
- **2,756 detected (99.1%)**
- **24 undetected (0.9%)**

### Detection Rate by Attack Type

✅ **Sybil Farming (HIGH)**: 100% detection
- Input validation caught all obvious fake wallets
- Wallet age < 30 days = automatic rejection
- Liquidation size < $1,000 = filtered out

✅ **Collusion Ring (HIGH)**: 100% detection
- Echo coherence detection identified coordinated patterns
- Pattern repetition > 80% flagged as suspicious
- Temporal correlation analysis caught coordinated timing

✅ **Retention Gaming (MEDIUM)**: 100% detection
- Vesting schedules prevent immediate dumps
- LTV tracking measures depth of re-engagement
- Volume requirements ($10K+ monthly) filter gaming

✅ **Cross-Chain Sybil (HIGH)**: 100% detection
- Cross-chain behavioral fingerprinting identified patterns
- Universal behavioral patterns detected across chains
- Multi-chain correlation analysis caught coordinated behavior

✅ **MEV Frontrunning (MEDIUM)**: 100% detection
- Time-based validation prevents race conditions
- MEV-resistant claim mechanisms in place
- Transaction sequencing protected

✅ **Incentive Gaming (MEDIUM)**: 100% detection
- Volume requirements ($10K+ monthly) prevent low-value gaming
- Depth of engagement measured beyond just frequency
- Behavioral consistency validated

✅ **Smart Contract Exploit (CRITICAL)**: 100% detection
- Audited contracts with multi-sig governance
- Continuous security monitoring in place
- Formal verification for critical functions

✅ **Governance Attack (HIGH)**: 100% detection
- Decentralized governance prevents single-entity control
- Token distribution prevents whale accumulation
- Anti-whale mechanisms in place

✅ **Spam Attack (LOW)**: 100% detection
- Minimum liquidation size ($1K+) filters spam
- Activity thresholds prevent noise

⚠️ **Oracle Manipulation (CRITICAL)**: 76% detection
- **24 wallets undetected out of 100 tested**
- **This is the critical vulnerability**

## The Critical Vulnerability: Oracle Manipulation

### Why 76% Isn't Good Enough

When you're handling liquidation events that trigger token claims, 24 undetected oracle manipulation attempts could be expensive.

**What's happening:**
- Established wallets (90-180 days old)
- High trading volume ($50K-$200K lifetime)
- Many trades (50-150 total)
- Large liquidation values ($5K-$20K)
- Multi-chain presence (4-5 chains)

These look legitimate at first glance. But they're designed to manipulate price feeds or liquidation data to trigger false claims.

**Current defenses:**
- Multi-party validation (Hyperliquid + dYdX + Chainlink)
- Price consistency checks
- Liquidation event verification

**What's failing:**
- Some sophisticated manipulation attempts bypass validation
- High-credibility scores mask manipulation intent
- Cross-chain coordination not fully detected

### How Attackers Could Exploit This

1. **Price Feed Manipulation**
   - Manipulate price feeds on one exchange
   - Trigger false liquidation events
   - Claim FRY tokens for non-existent liquidations

2. **Cross-Chain Coordination**
   - Liquidate on one chain
   - Claim on another chain
   - Oracle sees two separate events instead of one

3. **Timing Attacks**
   - Coordinate multiple price updates across oracles
   - Create brief windows where different oracles disagree
   - Exploit these windows for false claims

### Planned Improvements

**Phase 1: Enhanced Multi-Party Validation** (This week)
- Add 2+ additional oracle data sources
- Implement stricter consensus requirements (4/5 instead of 2/3)
- Increase price deviation thresholds
- Add temporal consistency checks

**Phase 2: Cross-Chain Correlation** (Next week)
- Track liquidation events across all chains
- Detect cross-chain duplicate claims
- Implement universal event ID tracking
- Add behavioral fingerprint correlation

**Phase 3: Machine Learning Detection** (This month)
- Train models on historical oracle manipulation attempts
- Real-time anomaly detection for price feed inconsistencies
- Pattern recognition for coordinated attacks
- Automated fraud detection

**Timeline for Fix:** Oracle manipulation detection should improve from 76% to >95% within 2 weeks.

## The Analysis: How We Detect Each Attack

### For Each Attack Type, How Does It Work?

**Sybil Farming:**
- Create thousands of fake wallets
- Get intentionally liquidated with tiny positions
- Claim FRY tokens on all wallets
- Dump tokens to profit from airdrops/incentives

**Why it's profitable:**
- Minimal cost (gas fees + small liquidations)
- High reward (hundreds or thousands of FRY tokens)
- Scale makes it profitable even with low per-wallet rewards

**How we detect it:**
- Input validation catches wallet age < 30 days
- Minimum liquidation size ($1,000+) filters tiny positions
- Historical activity requirements (10+ trades) prevent new account farming
- Bot pattern detection identifies automated behavior

**Current defense effectiveness:** ✅ 100% - Well defended

**What needs improvement:** None - This attack vector is fully mitigated

---

**Collusion Ring:**
- 10+ traders coordinate wash trades
- Create fake "behavioral patterns" (echo clusters)
- Oracle thinks they're legitimate behavioral clusters
- All claim retention incentives without real engagement

**Why it's profitable:**
- Claims retention incentives without actual retention
- Coordinates fake "return after liquidation" patterns
- Profits from protocol incentives without generating real value

**How we detect it:**
- Echo coherence detection identifies >80% identical patterns
- Temporal correlation analysis catches coordinated timing
- Pattern repetition scoring flags suspicious similarity
- Cross-reference with known bot trading rings

**Current defense effectiveness:** ✅ 100% - Well defended

**What needs improvement:** None - Collusion detection is working

---

**Retention Gaming:**
- Get liquidated, claim FRY tokens
- Return to platform briefly (make 1-2 trades)
- Show as "retained" in metrics
- Immediately withdraw and leave forever

**Why it's profitable:**
- Collect retention incentives without real retention
- Appears as legitimate retention in metrics
- Minimal effort for high reward

**How we detect it:**
- Vesting schedules prevent immediate dumps (90-180 day locks)
- LTV tracking measures depth of re-engagement (not just presence)
- Volume requirements ($10K+ monthly) prevent low-value gaming
- Behavioral consistency validation measures real engagement

**Current defense effectiveness:** ✅ 100% - Well defended

**What needs improvement:** None - Vesting and LTV tracking working

---

**Oracle Manipulation:**
- Manipulate price feeds or liquidation data
- Trigger false FRY claims
- Could drain entire treasury if successful

**Why it's profitable:**
- Maximum reward potential (could drain $100M+ treasury)
- High value justifies sophisticated attacks
- Protocol-critical if successful

**How we detect it:**
- Multi-party validation (Hyperliquid + dYdX + Chainlink consensus)
- Price consistency checks across oracles
- Liquidation event verification
- Cross-chain event correlation

**Current defense effectiveness:** ⚠️ 76% - **Needs improvement**

**What needs improvement:**
- Add more oracle data sources (currently 3, need 5+)
- Implement stricter consensus requirements
- Better cross-chain correlation detection
- Enhanced timing attack prevention

---

**Cross-Chain Sybil:**
- Use different wallet addresses on each chain (Ethereum, Arbitrum, Polygon, Base, Solana)
- Bypass single-chain detection
- Oracle thinks each chain has separate legitimate users

**Why it's profitable:**
- Scale: 5 chains × 1,000 wallets = 5,000 potential claims
- Harder to detect than single-chain Sybil
- Individual chains don't see the full picture

**How we detect it:**
- Cross-chain behavioral fingerprinting
- Universal behavioral patterns independent of wallet address
- Multi-chain correlation analysis
- Cross-referencing behavioral patterns across chains

**Current defense effectiveness:** ✅ 100% - Well defended

**What needs improvement:** None - Cross-chain detection working

---

**MEV Frontrunning:**
- Frontrun liquidation events
- Claim FRY before legitimate users
- Reduce rewards for real users, increase for attackers

**Why it's profitable:**
- Claim rewards before others
- Reduce time to claim (higher first-mover advantage)
- Potential for automated profitable strategies

**How we detect it:**
- Time-based validation prevents race conditions
- MEV-resistant claim mechanisms
- Transaction sequencing protection
- Temporal analysis detects frontrunning patterns

**Current defense effectiveness:** ✅ 100% - Well defended

**What needs improvement:** None - MEV resistance working

---

**Incentive Gaming:**
- Make 1 trade every 29 days
- Maintain "active" status to farm 2× FRY multipliers
- No real engagement, just maintaining minimum activity

**Why it's profitable:**
- 2× multiplier doubles FRY rewards
- Minimal effort (1 trade every 29 days)
- High reward-to-effort ratio

**How we detect it:**
- Volume requirements ($10K+ monthly) prevent low-value gaming
- Depth of engagement metrics beyond just frequency
- Behavioral consistency validation
- Trading pattern analysis

**Current defense effectiveness:** ✅ 100% - Well defended

**What needs improvement:** None - Volume requirements working

---

**Smart Contract Exploit:**
- Find vulnerability in FRY token or oracle contracts
- Could drain entire system if successful

**Why it's profitable:**
- Maximum potential impact (entire protocol)
- High value justifies sophisticated research
- Protocol-critical if successful

**How we detect it:**
- Audited contracts with multi-sig governance
- Continuous security monitoring
- Formal verification for critical functions
- Bug bounty program

**Current defense effectiveness:** ✅ 100% - Well defended

**What needs improvement:** None - Audited contracts working

---

**Governance Attack:**
- Acquire majority of FRY tokens
- Control protocol parameters
- Change retention incentives to benefit attackers

**Why it's profitable:**
- Control over protocol parameters
- Can change incentives to benefit token holders
- Long-term profit potential

**How we detect it:**
- Decentralized governance prevents single-entity control
- Token distribution prevents whale accumulation
- Anti-whale mechanisms
- Proposal delay mechanisms

**Current defense effectiveness:** ✅ 100% - Well defended

**What needs improvement:** None - Decentralized governance working

---

**Spam Attack:**
- Create many small liquidations
- Spam the system with noise
- Overwhelm system resources

**Why it's profitable:**
- Low effort attack
- Could slow system down
- Reduces quality of legitimate data

**How we detect it:**
- Minimum liquidation size ($1K+) filters spam
- Activity thresholds prevent noise
- Rate limiting on API endpoints

**Current defense effectiveness:** ✅ 100% - Well defended

**What needs improvement:** None - Spam filtering working

## The Conclusion: Security is Ongoing Discovery

**Security isn't "we're safe."**

Security is **"we tried to break it 2,780 times and found where it breaks."**

Then we fix it.

Then we test again.

The fact that 24 attack wallets got through isn't a failure. It's a **discovery.** A vulnerability we found before real attackers did.

### What This Means for FRY

- **99.1% detection rate** is solid for a first implementation
- **Critical vulnerability identified** before production deployment
- **Comprehensive testing** validates the five-layer framework works
- **Continuous improvement** is built into the process

### What This Means for DeFi

Most projects don't do this. They:
- Test the happy path
- Deploy to mainnet
- Hope attackers don't find vulnerabilities

We:
- Test attack vectors at scale
- Find vulnerabilities proactively
- Fix before deployment
- Continue testing regularly

### The Invitation: Find More Attacks

This is open source. The red team testing framework is publicly available.

**I invite you to try to break it.**

- Review the threat model
- Run the attack simulations
- Find new attack vectors we missed
- Submit issues on GitHub

**The more attacks we find in testing, the fewer exploit real users.**

### What's Next

- **This week**: Fix oracle manipulation detection (76% → >95%)
- **This month**: Deploy improvements to mainnet
- **Ongoing**: Continue red team testing and improve defenses

**Security is never done. It's continuously discovering vulnerabilities and fixing them before they're exploited.**

## Join the Red Team

**If you're interested in:**
- Adversarial security testing
- Behavioral oracle research
- DeFi protocol security
- Threat modeling

**Get involved:**
- Review the code: https://github.com/aidanduffy68-prog/behavioral-oracle
- Read the research: https://mirror.xyz/0xf551aF8d5373B042DBB9F0933C59213B534174e4
- Run the attack simulations
- Submit new attack vectors

**Let's find the vulnerabilities before attackers do.**

---

*Built for the 82% who quit. 🍟*
