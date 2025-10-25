# USD_FRY Demo Video Script
**Duration: 2-3 minutes**

---

## Opening (0:00-0:15)
**[Screen: Website homepage]**

"Hi, I'm showing you USD_FRY - DeFi infrastructure I built for wreckage absorption on native stablecoin DEXes."

**[Scroll to stats]**

"It achieves 7.4x capital efficiency and 2.26 FRY per dollar of trading losses processed."

---

## Live Deployment (0:15-0:45)
**[Click "Live Contracts" button]**

"These are live smart contracts deployed on Arbitrum Sepolia testnet."

**[Show contract addresses section]**

"Five contracts total: the FRY token, Agent B verifier for zkML proofs, confidential position verifier for privacy, the liquidity rails router, and the wreckage matching pool."

**[Click "View on Arbiscan"]**

"All verified on-chain. You can see the deployment, transactions, and source code."

**[Show Arbiscan page briefly]**

---

## Architecture (0:45-1:30)
**[Back to website, scroll to "How It Works"]**

"The system has three tiers."

**[Point to each tier]**

"Tier 1: P2P matching for funding rate swaps. Highest minting rate at 1.4x.

Tier 2: Liquidity rails with multi-hop routing. This is where most wreckage goes. 1.2 to 2.2x minting rate.

Tier 3: Agent B, an ML-enhanced market maker as fallback. 0.8 to 1.0x."

**[Scroll to metrics]**

"The system averages 2.26 FRY per dollar, which is 221% better than the base rate."

---

## Code Structure (1:30-2:00)
**[Open GitHub repo]**

"Let me show you the code structure."

**[Navigate to liquidity-rails/core/]**

"Core directory has the routing engine, Agent B market maker, and smart contracts."

**[Open contracts folder]**

"Five Solidity contracts using OpenZeppelin. USDFRYToken is the main ERC20, LiquidityRailsRouter handles routing, WreckageMatchingPool does P2P matching."

**[Open engines/agent_b/]**

"Agent B uses PyTorch for ML-enhanced hedging. It monitors Hyperliquid funding rates in real-time."

**[Open privacy/]**

"Privacy layer uses EZKL for zkML proofs and Pedersen commitments for confidential positions."

---

## Technical Highlights (2:00-2:30)
**[Back to README or whitepaper]**

"Key technical achievements:

One - Native token denomination for 7.4x capital efficiency. By measuring losses in HYPE or USDF instead of USDC, we create a positive feedback loop.

Two - zkML privacy layer. Market makers can prove their models work without revealing validation data.

Three - Multi-hop routing with dynamic programming for optimal paths across five DEXes.

Four - ML-enhanced hedging with 11% improvement over traditional approaches."

---

## Use Case (2:30-2:50)
**[Show partnership pitch or website]**

"This is built for native stablecoin DEXes like Hyperliquid with USDH and Aster with USDF.

For DEXes, it reduces LP losses and stabilizes funding rates.

For market makers, it converts losses into FRY tokens and provides optimal routing.

For LPs, it offers better risk-adjusted returns with confidential position tracking."

---

## Closing (2:50-3:00)
**[Back to website homepage]**

"Everything's open source on GitHub. Live demo at the link below. Thanks for watching."

**[Show final frame with:]**
- Website: https://aidanduffy68-prog.github.io/USD_FRY/
- GitHub: https://github.com/aidanduffy68-prog/USD_FRY
- Contracts: Arbitrum Sepolia

---

## Recording Tips

**Tools:**
- QuickTime (Mac screen recording)
- Or: Loom (loom.com)
- Or: OBS Studio (free)

**Settings:**
- 1080p resolution
- Show cursor
- Clear audio (use AirPods/headphones mic)

**Preparation:**
- Have all tabs open beforehand
- Practice once without recording
- Keep it under 3 minutes
- Speak clearly and at moderate pace

**What to Show:**
1. Website (30 sec)
2. Deployed contracts on Arbiscan (30 sec)
3. Code structure on GitHub (45 sec)
4. Technical highlights (30 sec)
5. Use case (20 sec)
6. Closing (15 sec)

**Upload to:**
- YouTube (unlisted)
- Add link to README
- Share in job applications

---

## Alternative: Shorter Version (1 minute)

**0:00-0:20** - Website + deployed contracts  
**0:20-0:40** - Architecture diagram  
**0:40-0:55** - Code structure  
**0:55-1:00** - Closing  

Use this for quick demos or Twitter/LinkedIn posts.
