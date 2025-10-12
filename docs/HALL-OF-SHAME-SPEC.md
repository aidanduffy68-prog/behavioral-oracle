# Hall of Shame - Combined Feature Spec

## What It Is

One feature that combines:
1. **Leaderboard** - See other people's losses
2. **Community** - Connect with others who got rekt
3. **Shareable receipts** - Turn your loss into a story

## The Flow

### 1. Process Your Loss
- Enter amount + coin
- Process through FRY
- Get FRY tokens

### 2. Enter the Hall of Shame
- Your loss gets added to the leaderboard
- Anonymous by default, optional username
- Shows: Amount, Coin, Date, Rank

### 3. See You're Not Alone
```
HALL OF SHAME - Oct 10, 2025

#1  Anonymous Whale    $847,392  BTC   "longed at $122k"
#2  paper_hands_pete   $523,100  SOL   "but the ecosystem"
#3  XRP_believer       $401,293  XRP   "SEC case incoming"
...
#47 You               $5,000    BTC   "first time?"
...
#1,642,891 total losers | $19.2B processed
```

### 4. Share Your Receipt
Click "Share" → Generates image:

```
┌─────────────────────────────────┐
│  FRY PROTOCOL - LOSS RECEIPT    │
├─────────────────────────────────┤
│  Date: Oct 10, 2025             │
│  Asset: BTC                     │
│  Loss: $5,000                   │
│  FRY Minted: 11,300             │
│  Rank: #47 / 1.6M               │
├─────────────────────────────────┤
│  "We catch you when you fall"   │
│  aidanduffy68-prog.github.io    │
└─────────────────────────────────┘
```

Post to Twitter/LinkedIn with one click.

## Why This Works

**Leaderboard = Validation**
"I'm not the only one who got rekt"

**Community = Connection**
"Other people lost on BTC at $122k too"

**Shareable = Story**
"I survived the $19B crash and got this receipt"

## Technical Implementation

### Data Storage
- Local storage for personal stats
- Optional: Backend API for global leaderboard
- No wallet connection required (lower friction)

### Privacy
- Anonymous by default
- Optional username (no real names)
- Only shows: amount, coin, date, rank
- No wallet addresses, no personal info

### Shareables
- Generate image with Canvas API
- Pre-filled Twitter/LinkedIn text
- One-click share buttons
- Includes link back to FRY

## UI/UX

### Leaderboard View
```
┌────────────────────────────────────────┐
│  🏆 HALL OF SHAME - Oct 10, 2025      │
├────────────────────────────────────────┤
│  Filter: [All] [BTC] [SOL] [XRP]      │
│  Sort: [Biggest] [Recent] [My Rank]   │
├────────────────────────────────────────┤
│  #1  👑 $847K  BTC  "longed at $122k" │
│  #2  💎 $523K  SOL  "but ecosystem"   │
│  #3  🤡 $401K  XRP  "SEC case soon"   │
│  ...                                   │
│  #47 🫵 $5K    BTC  "first time?"     │
│  ...                                   │
├────────────────────────────────────────┤
│  Total: 1.6M losers | $19.2B rekt    │
│  [Share Your Loss] [View My Rank]     │
└────────────────────────────────────────┘
```

### Share Modal
```
┌────────────────────────────────────────┐
│  Share Your Loss Receipt              │
├────────────────────────────────────────┤
│  [Receipt Preview Image]              │
├────────────────────────────────────────┤
│  Caption:                             │
│  "I processed $5K in losses on        │
│   @FRY_Protocol. Rank #47/1.6M.       │
│   We catch you when you fall. 🍟"     │
├────────────────────────────────────────┤
│  [📱 Twitter] [💼 LinkedIn] [📋 Copy] │
└────────────────────────────────────────┘
```

## Copy/Messaging

**Leaderboard Header:**
"You're not alone. 1.6M traders got liquidated on Oct 10."

**Empty State:**
"Be the first to admit your losses. (Someone has to start)"

**After Processing:**
"Your loss has been recorded in the Hall of Shame. You're #47 out of 1.6M."

**Share Button:**
"Turn your L into a story"

## Viral Mechanics

1. **Competitive suffering** - "My loss was bigger than yours"
2. **Solidarity** - "We all got rekt together"
3. **Dark humor** - "At least I'm honest about it"
4. **FOMO** - "Everyone's sharing their receipts"

## Success Metrics

- % of users who view leaderboard after processing
- % of users who share their receipt
- Click-through rate from shared receipts
- Retention: Do people come back to check their rank?

## Phase 1 (MVP)

- Local leaderboard (just your browser)
- Basic receipt generation
- Share to Twitter/LinkedIn
- No backend required

## Phase 2 (If It Works)

- Global leaderboard (backend API)
- Real-time updates
- Filter by coin/date
- User profiles (optional)
- Comments/reactions

---

**The goal:** Make people feel less alone when they lose money.

The leaderboard isn't about competition. It's about **community in shared suffering.**
