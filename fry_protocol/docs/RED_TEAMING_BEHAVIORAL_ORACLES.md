# Red Teaming Behavioral Oracles

## I spent a week trying to steal from my own protocol. Here's what I found.

Most crypto projects get hacked because builders don't think like attackers.

They build for the "happy path"—the normal, legitimate user flow. Then attackers find the edge cases, exploit the assumptions, and drain $100M.

I built FRY (a behavioral oracle for trader retention) assuming everything would be attacked. Then I proved it.

Here's what happened when I created 2,780 fake accounts and tried to break my own system.

## The Thesis: Security is "We Found Where It Breaks"

This isn't a story about building a perfect system. This is about **finding the flaws before real attackers do.**

**Traditional security thinking:**
- "We audited the code"
- "We tested the normal use cases"  
- "We deployed to mainnet"

**Actual security thinking:**
- "I'm going to try to steal tokens"
- "How would I exploit this if I were trying to profit from it?"
- "Let me test attacks at scale"

**That's what I did.**

## The Methodology: 2,780 Fake Accounts Testing 10 Attack Scenarios

I built a testing system that simulates realistic attacks against FRY.

### What Each Attack Tries To Do

**1. Fake Account Farming (HIGH Severity)**
- Create 1,000+ fake accounts
- Make tiny losing trades ($10)
- Claim rewards on all accounts
- Sell immediately for profit

**2. Coordination Ring (HIGH Severity)**  
- Get 10+ people to work together
- Create fake "user patterns"
- System thinks they're legitimate users
- All claim rewards

**3. Fake Retention (MEDIUM Severity)**
- Lose money, claim rewards
- Come back for 1 day to look "retained"
- Leave forever
- Still got paid

**4. Data Manipulation (CRITICAL Severity)**
- Trick the system into thinking fake events happened
- Trigger false reward claims
- Could drain the entire treasury

**5. Cross-Chain Gaming (HIGH Severity)**
- Use different accounts on different blockchains
- System thinks you're multiple people
- Claim rewards as each "person"

**6. Speed Gaming (MEDIUM Severity)**
- Rush to claim rewards before real users
- Take their share
- Profit from timing advantage

**7. Minimal Activity Gaming (MEDIUM Severity)**
- Do just enough to stay "active"
- Get 2× multiplier without real use
- Maximize rewards with minimal effort

**8. Code Exploit (CRITICAL Severity)**
- Find bug in smart contract
- Drain the system
- Most dangerous attack

**9. Control Attack (HIGH Severity)**
- Buy majority of tokens
- Control the system
- Change rules in your favor

**10. Spam Attack (LOW Severity)**
- Create tons of tiny transactions
- Overwhelm the system
- Reduce service quality

## The Results: 99.1% Detection Rate (But the 0.9% Could Be Expensive)

### Overall Performance
- **2,780 fake accounts tested**
- **2,756 caught (99.1%)**
- **24 slipped through (0.9%)**

### How We Caught Each Attack

✅ **Fake Account Farming (HIGH)**: 100% caught
- All obviously fake accounts rejected
- Accounts less than 30 days old = automatic rejection
- Trade size less than $1,000 = filtered out

✅ **Coordination Ring (HIGH)**: 100% caught
- System detected coordinated patterns
- Too similar to be real = flagged
- Timing matched perfectly = suspicious

✅ **Fake Retention (MEDIUM)**: 100% caught
- Rewards can't be sold immediately (90-180 day lock)
- System measures depth of return, not just presence
- Must trade $10K+ monthly to count

✅ **Cross-Chain Gaming (HIGH)**: 100% caught
- System tracks behavior across all chains
- Detects matching patterns across accounts
- One person can't hide as multiple users

✅ **Speed Gaming (MEDIUM)**: 100% caught
- Timing protections prevent rush attacks
- Sequence of claims is protected
- Can't game the timing

✅ **Minimal Activity Gaming (MEDIUM)**: 100% caught
- Must trade $10K+ monthly to count
- System measures real engagement, not just login
- One trade every 29 days doesn't count

✅ **Code Exploit (CRITICAL)**: 100% caught
- Code is audited before deployment
- Multiple security reviews
- Continuous monitoring for bugs

✅ **Control Attack (HIGH)**: 100% caught
- No single person can control the system
- Tokens are distributed widely
- Governance is decentralized

✅ **Spam Attack (LOW)**: 100% caught
- Minimum trade size ($1K+) filters spam
- Activity requirements prevent noise

⚠️ **Data Manipulation (CRITICAL)**: 76% caught
- **24 accounts slipped through out of 100 tested**
- **This is the critical weakness**

## The Critical Vulnerability: Data Manipulation

### Why 76% Isn't Good Enough

When you're handling events that trigger reward claims, 24 undetected manipulation attempts could be very expensive.

**What's happening:**
- Accounts look legitimate (90-180 days old)
- High trading volume ($50K-$200K lifetime)
- Many trades (50-150 total)
- Large losses ($5K-$20K)
- Active on multiple chains (4-5 chains)

These look real at first glance. But they're designed to trick the system into thinking fake events happened to trigger false claims.

**Current protections:**
- Check multiple data sources
- Verify prices are consistent
- Validate event data

**What's failing:**
- Some sophisticated manipulation gets through
- High-activity accounts are trusted too much
- Cross-chain coordination not fully caught

### How Attackers Could Exploit This

1. **Fake Price Movements**
   - Manipulate prices on one exchange
   - Trigger false loss events
   - Claim rewards for events that didn't really happen

2. **Cross-Chain Gaming**
   - Lose money on one chain
   - Claim on another chain
   - System sees two separate events instead of one

3. **Timing Tricks**
   - Coordinate price updates across data sources
   - Create brief windows where sources disagree
   - Exploit these windows for false claims

### How We'll Fix This

**This Week:**
- Add 2+ more data sources
- Require 4 out of 5 sources to agree (instead of 2 out of 3)
- Stricter price difference limits
- Better timing checks

**Next Week:**
- Track events across all chains
- Detect duplicate claims across chains
- Create universal event IDs
- Better behavior pattern matching

**This Month:**
- Train AI to detect manipulation patterns
- Real-time anomaly detection
- Automatic fraud detection

**Timeline:** Should improve from 76% to >95% within 2 weeks.

## The Conclusion: Security is Never Done

**Security isn't "we're safe."**

Security is **"we tried to break it 2,780 times and found where it breaks."**

Then we fix it.

Then we test again.

The fact that 24 fake accounts got through isn't a failure. It's a **discovery.** A vulnerability we found before real attackers did.

### What This Means for FRY

- **99.1% catch rate** is solid for a first try
- **Critical weakness identified** before going live
- **Comprehensive testing** validates the system works
- **Continuous improvement** is built into the process

### What This Means for DeFi

Most projects don't do this. They:
- Test the normal use cases
- Deploy to mainnet
- Hope attackers don't find bugs

We:
- Test attack scenarios at scale
- Find weaknesses before going live
- Fix before deployment
- Keep testing regularly

### The Invitation: Try To Break It

This is open source. The testing system is publicly available.

**I invite you to try to break it.**

- Review the security model
- Run the attack tests
- Find new attack methods we missed
- Submit issues on GitHub

**The more attacks we find in testing, the fewer hurt real users.**

### What's Next

- **This week:** Fix data manipulation detection (76% → >95%)
- **This month:** Deploy improvements to production
- **Ongoing:** Keep testing and improving

**Security is never done. It's constantly finding weaknesses and fixing them before they're exploited.**

## Join the Security Team

**If you're interested in:**
- Finding security weaknesses
- Testing crypto systems
- DeFi security research
- Threat modeling

**Get involved:**
- Review the code: https://github.com/aidanduffy68-prog/behavioral-oracle
- Read the research: https://mirror.xyz/0xf551aF8d5373B042DBB9F0933C59213B534174e4
- Run the attack tests
- Submit new attack methods

**Let's find the weaknesses before attackers do.**

---

*Built for the 82% who quit. 🍟*