# Public Retention Metrics Dashboard - Demo Spec

## Overview
Live, interactive dashboard that proves the FRY retention oracle is working by displaying real-time retention metrics from tracked wallets.

---

## Core Purpose
**Build credibility** by transparently showing:
- Which wallets are being tracked (anonymized)
- Days since liquidation
- Return activity (yes/no with timestamps)
- Current retention rate vs 18% baseline

---

## Technical Architecture

### Data Sources
1. **Liquidation Events Database** (`fry_retention.db`)
   - Tracked wallets with liquidation timestamps
   - Liquidation sizes and assets
   - 30-day tracking windows

2. **Activity Monitoring**
   - Post-liquidation trading activity
   - Return timestamps
   - Volume metrics

3. **Behavioral Patterns** (`behavioral_liquidity.db`)
   - Behavioral fingerprints
   - Alpha potential scores
   - Pattern classifications

### Tech Stack
```
Frontend: HTML5 + CSS3 + Vanilla JavaScript
Visualization: Chart.js for real-time graphs
Data Layer: SQLite → JSON API
Update Frequency: Real-time (WebSocket) or 5-minute polling
Hosting: GitHub Pages (static) or Vercel (dynamic)
```

---

## UI/UX Design Spec

### Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    FRY RETENTION ORACLE                     │
│                   Live Retention Dashboard                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  42% vs 0%  │  │  22 Wallets │  │  7.2 Days   │        │
│  │  Retention  │  │   Tracked   │  │ Avg Return  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │          Retention Rate Over Time (Line Chart)       │ │
│  │                                                       │ │
│  │  50% ┤                                               │ │
│  │      │          ╱────────                            │ │
│  │  25% ┤      ╱──╱                                     │ │
│  │      │  ╱──╱                                         │ │
│  │   0% ┴────────────────────────────────────────────  │ │
│  │      Oct 11   Oct 18   Oct 25   Nov 01   Nov 08    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │               Tracked Wallets Table                  │ │
│  ├─────────┬───────────┬──────────┬──────────┬──────────┤ │
│  │ Wallet  │  Days     │ Returned │ Activity │ Pattern  │ │
│  │ ID      │ Since Liq │          │          │          │ │
│  ├─────────┼───────────┼──────────┼──────────┼──────────┤ │
│  │ 0x4a3.. │    8d     │    ✅    │  High    │  Alpha   │ │
│  │ 0x7b2.. │   12d     │    ✅    │  Medium  │ Retention│ │
│  │ 0x9c1.. │   15d     │    ❌    │  None    │  Churned │ │
│  │ 0x2d8.. │   20d     │    ✅    │  High    │  Alpha   │ │
│  └─────────┴───────────┴──────────┴──────────┴──────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │          Behavioral Pattern Distribution             │ │
│  │                (Pie/Donut Chart)                     │ │
│  │                                                       │ │
│  │         Alpha Traders: 27%                           │ │
│  │         Retention: 41%                               │ │
│  │         Arbitrageurs: 14%                            │ │
│  │         Churned: 18%                                 │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Metrics Display

### Hero Metrics (Top Cards)
1. **Retention Rate**
   - Large percentage: "42% vs 0%"
   - Subtitle: "Control group retention"
   - Color: Green if > 30%, Yellow if 20-30%, Red if < 20%

2. **Wallets Tracked**
   - Number: "22 Wallets"
   - Subtitle: "Since Oct 11, 2025"
   - Live counter animation

3. **Average Return Time**
   - Number: "7.2 Days"
   - Subtitle: "Median: 5 days"
   - Lower is better indicator

### Retention Rate Over Time (Line Chart)
- **X-axis:** Date (Oct 11 → Present)
- **Y-axis:** Retention percentage (0-100%)
- **Lines:**
  - FRY Retention (green, bold)
  - Control Group (red, dashed)
  - Industry Baseline 18% (gray, dotted reference line)
- **Interactive:** Hover for exact values
- **Update:** Real-time or every 5 minutes

### Tracked Wallets Table
**Columns:**
1. **Wallet ID** - First 6 chars (anonymized)
2. **Days Since Liquidation** - Live counter
3. **Returned** - ✅/❌ with timestamp on hover
4. **Activity Level** - High/Medium/Low/None
5. **Pattern** - Alpha/Retention/Arbitrage/Churned

**Features:**
- Sortable by any column
- Searchable by wallet ID
- Color-coded rows (green = returned, red = churned)
- Click row to see detailed behavioral fingerprint

### Behavioral Pattern Distribution
**Visualization:** Donut chart with legend
**Segments:**
- Alpha Traders (purple)
- Retention Candidates (green)
- Arbitrageurs (blue)
- Sentiment Leaders (yellow)
- Churned (red)

**Interactive:** Click segment to filter table

---

## Data Update Strategy

### Real-Time Updates
```javascript
// WebSocket connection for live updates
const ws = new WebSocket('wss://fry-api.com/retention/live');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateDashboard(data);
};
```

### Polling Fallback
```javascript
// Poll every 5 minutes if WebSocket fails
setInterval(async () => {
  const response = await fetch('/api/retention/current');
  const data = await response.json();
  updateDashboard(data);
}, 300000);
```

---

## Privacy & Anonymization

### Wallet Anonymization
- Display only first 6 characters: `0x4a3c2f...`
- Hash middle portion: `0x4a3...7f2e`
- Never show full addresses publicly

### Data Aggregation
- All metrics aggregated before display
- Individual wallet details hidden behind click
- No personally identifiable information

### Transparency Note
> "All wallet addresses are anonymized. Data is aggregated from on-chain activity and public exchange APIs. No private information is displayed."

---

## Interactive Features

### 1. Wallet Detail Modal
**Trigger:** Click wallet row
**Content:**
- Behavioral fingerprint visualization
- Risk tolerance score
- Recovery speed score
- Platform loyalty score
- Trading consistency score
- Activity timeline

### 2. Date Range Filter
**Options:**
- Last 7 days
- Last 14 days
- Last 30 days
- All time
- Custom range

### 3. Pattern Filter
**Options:**
- Show all patterns
- Alpha traders only
- Retention candidates only
- Arbitrageurs only
- Sentiment leaders only
- Churned wallets only

### 4. Export Data
**Formats:**
- CSV export
- JSON export
- PNG image of charts
- PDF report

---

## API Endpoints

### GET `/api/retention/current`
Returns current retention metrics
```json
{
  "retention_rate": 0.42,
  "control_group_rate": 0.0,
  "total_tracked": 22,
  "returned_count": 9,
  "avg_return_days": 7.2,
  "median_return_days": 5,
  "last_updated": "2025-10-21T14:30:00Z"
}
```

### GET `/api/retention/wallets`
Returns tracked wallet summary
```json
{
  "wallets": [
    {
      "id": "0x4a3c2f",
      "days_since_liquidation": 8,
      "returned": true,
      "return_timestamp": "2025-10-19T10:45:00Z",
      "activity_level": "high",
      "pattern": "alpha_trader"
    }
  ]
}
```

### GET `/api/retention/patterns`
Returns behavioral pattern distribution
```json
{
  "patterns": {
    "alpha_traders": 6,
    "retention_candidates": 9,
    "arbitrageurs": 3,
    "sentiment_leaders": 2,
    "churned": 2
  }
}
```

### GET `/api/retention/history`
Returns time-series data
```json
{
  "history": [
    {
      "date": "2025-10-11",
      "retention_rate": 0.0,
      "control_rate": 0.0,
      "tracked_count": 10
    },
    {
      "date": "2025-10-18",
      "retention_rate": 0.3,
      "control_rate": 0.0,
      "tracked_count": 15
    }
  ]
}
```

---

## Mobile Responsive Design

### Breakpoints
- **Desktop:** > 1024px (full layout)
- **Tablet:** 768px - 1023px (stacked cards)
- **Mobile:** < 767px (single column)

### Mobile Optimizations
- Stack hero metrics vertically
- Simplify table to card view
- Touch-friendly tap targets
- Swipe for chart navigation

---

## Performance Requirements

### Load Time
- Initial page load: < 2 seconds
- Data updates: < 500ms
- Chart rendering: < 1 second

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## Accessibility (A11y)

### WCAG 2.1 AA Compliance
- Keyboard navigation
- Screen reader support
- Color contrast ratios > 4.5:1
- ARIA labels on interactive elements

### Features
- Skip to main content link
- Focus indicators on all interactive elements
- Alt text for charts (data tables as fallback)
- Reduced motion support

---

## Implementation Phases

### Phase 1: MVP (2-3 days)
- Basic dashboard layout
- Hero metrics display
- Simple table view
- Static data (hardcoded)

### Phase 2: Live Data (1-2 days)
- API integration
- Real-time updates
- Database connection
- Polling mechanism

### Phase 3: Visualization (1-2 days)
- Line chart for retention over time
- Donut chart for patterns
- Interactive filters
- Date range selector

### Phase 4: Advanced Features (2-3 days)
- Wallet detail modal
- Behavioral fingerprint viz
- Export functionality
- Mobile optimization

---

## Success Metrics

### Credibility Indicators
- Dashboard uptime: > 99%
- Data freshness: < 5 minutes old
- Transparency score: Fully anonymized + verifiable

### User Engagement
- Page views: Track daily visitors
- Time on page: > 2 minutes average
- Interaction rate: > 30% click through to details
- Share rate: Track social media shares

### Technical Performance
- Load time: < 2 seconds
- API response: < 500ms
- Chart render: < 1 second
- Mobile performance: Lighthouse score > 90

---

## Launch Checklist

### Pre-Launch
- [ ] Database populated with 20+ tracked wallets
- [ ] All API endpoints tested
- [ ] Charts rendering correctly
- [ ] Mobile responsive tested
- [ ] Privacy compliance verified
- [ ] Analytics integrated

### Launch
- [ ] Deploy to GitHub Pages / Vercel
- [ ] Update README with dashboard link
- [ ] Post on Twitter / LinkedIn
- [ ] Share in Discord / Telegram
- [ ] Monitor for issues

### Post-Launch
- [ ] Daily monitoring of metrics
- [ ] Weekly updates to tracked wallets
- [ ] Monthly blog post with insights
- [ ] Continuous improvement based on feedback

---

## Marketing Copy

### Dashboard Headline
"FRY Retention Oracle: Live Proof of 42% vs 0% Retention"

### Subtitle
"Transparent, real-time tracking of liquidated trader behavior. See the oracle at work."

### CTA
"View Live Dashboard →"

### Social Media Teaser
"We said we'd track liquidated traders. Here's the proof: 42% retention vs 0% control group. Live dashboard showing all 22 wallets (anonymized). Real data, real time. 🍟"

---

## Files to Create

1. `/docs/retention-dashboard-enhanced.html` - Full dashboard implementation
2. `/docs/assets/dashboard.css` - Styling
3. `/docs/assets/dashboard.js` - Interactive logic
4. `/api/retention.py` - API backend (Python/Flask)
5. `/docs/dashboard-demo-spec.md` - This spec document

---

## Next Steps

1. Build Phase 1 MVP with static data
2. Integrate with existing `fry_retention.db`
3. Add real-time updates
4. Deploy to GitHub Pages
5. Launch with Twitter/LinkedIn post

**Estimated Total Time:** 5-7 days
**Priority:** High (builds credibility)
**Impact:** High (proves oracle works)

