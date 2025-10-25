# Live Market Service

Backend service that aggregates real-time crypto events, liquidations, and news for wreckage processing.

## Features

- **Real-time liquidation data** from Coinglass API
- **Trending wreckage coins** (top 5 by liquidations)
- **Auto-generated prediction markets** based on market events
- **WebSocket support** for live updates
- **Snarky roasts** based on actual market data

## Installation

```bash
cd liquidity-rails/core/api
npm install
```

## Configuration

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your API keys (Coinglass key already included).

**Note:** If the Coinglass API key is expired or unavailable, the service automatically falls back to realistic mock data. The demo will still work perfectly!

## Running

```bash
# Production
npm start

# Development (auto-reload)
npm run dev
```

Server runs on `http://localhost:3001`

## API Endpoints

### GET /api/live-data
Returns all live data (coins, liquidations, markets)

```json
{
  "trendingWreckage": [...],
  "recentLiquidations": [...],
  "activePredictionMarkets": [...],
  "lastUpdate": "2025-01-10T15:30:00.000Z"
}
```

### GET /api/trending-wreckage
Returns top 5 coins by liquidations with snarky roasts

```json
{
  "coins": [
    {
      "symbol": "BTC",
      "liquidations": 500000000,
      "longLiq": 400000000,
      "shortLiq": 100000000,
      "priceChange": -5.2,
      "roast": "BTC just liquidated $500M... you too?",
      "emoji": "₿"
    }
  ],
  "lastUpdate": "2025-01-10T15:30:00.000Z"
}
```

### GET /api/recent-liquidations
Returns terminal messages about recent liquidations

```json
{
  "messages": [
    "> 🚨 $500.0M liquidated in the last hour",
    "> 15 coins experiencing wreckage",
    "> You're in good company (misery loves company)"
  ],
  "lastUpdate": "2025-01-10T15:30:00.000Z"
}
```

### GET /api/prediction-markets
Returns auto-generated prediction markets

```json
{
  "markets": [
    {
      "id": "market_BTC_1234567890",
      "question": "Will BTC recover within 24h?",
      "outcomes": ["YES", "NO"],
      "context": "$500M liquidated in last hour",
      "roast": "Buying the dip? Bold strategy.",
      "expires": 1234567890000,
      "trending": true
    }
  ],
  "lastUpdate": "2025-01-10T15:30:00.000Z"
}
```

### GET /health
Health check endpoint

## WebSocket

Connect to `ws://localhost:3001` for real-time updates every 30 seconds.

```javascript
const ws = new WebSocket('ws://localhost:3001');

ws.onmessage = (event) => {
  const { type, data } = JSON.parse(event.data);
  
  if (type === 'initial') {
    // Initial data load
    console.log('Connected:', data);
  } else if (type === 'update') {
    // Live updates
    console.log('Update:', data);
  }
};
```

## Scheduled Jobs

- **Every 5 minutes**: Update all live data from Coinglass
- **Every hour**: Clean up expired prediction markets

## Integration with Demo

Update `interactive-demo.html`:

```javascript
// Fetch live data
async function loadLiveData() {
  const response = await fetch('http://localhost:3001/api/live-data');
  const data = await response.json();
  
  // Update coin selector
  updateCoinSelector(data.trendingWreckage);
  
  // Show liquidation messages
  data.recentLiquidations.forEach(msg => addTerminalLine(msg));
  
  // Display prediction markets
  renderPredictionMarkets(data.activePredictionMarkets);
}

// Refresh every 30 seconds
setInterval(loadLiveData, 30000);
```

## Example Roasts

Based on real market data:

- **High liquidations**: "BTC just liquidated $500M... you too?"
- **Price dump**: "SOL down -20.5%... classic"
- **Long squeeze**: "ETH longs getting absolutely rekt"
- **Short squeeze**: "XRP shorts getting squeezed... ouch"
- **Default**: "DOGE wreckage detected... let me guess, you longed the top?"

## Notes

- Uses your existing Coinglass API key
- Fallback data if API fails
- CORS enabled for demo integration
- WebSocket for real-time updates
- Auto-generates prediction markets from trending events
