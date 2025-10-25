# Live Market Data Integration for Wreckage Processing

## Core Concept
Use real-time news, social sentiment, and market events to dynamically generate wreckage scenarios and prediction markets.

---

## 1. Crypto Demo - Live Market Data

### Current State
- Static coin selection (BTC, SOL, XRP, FARTCOIN)
- Simulated wreckage processing
- Fixed roast messages

### With Live Data Integration

#### Data Sources
```javascript
// CoinGecko API (Free)
- Real-time prices
- 24h price changes
- Market cap rankings
- Trending coins

// Twitter/X API
- Trending crypto topics
- Sentiment analysis
- Viral tweets about losses

// CryptoCompare API
- Historical price data
- Volatility metrics
- Liquidation data

// Coinglass API (You already have this!)
- Liquidation heatmaps
- Long/short ratios
- Funding rates
- Open interest
```

#### Dynamic Coin Selection
```javascript
// Instead of static coins, fetch trending disasters
async function getTrendingWreckage() {
    const coins = await fetch('https://api.coinglass.com/api/futures/liquidation/chart');
    
    // Find coins with highest liquidations in last 24h
    const topWrecks = coins
        .sort((a, b) => b.liquidations - a.liquidations)
        .slice(0, 5);
    
    return topWrecks.map(coin => ({
        symbol: coin.symbol,
        liquidations: coin.liquidations,
        roast: generateRoast(coin)
    }));
}

// Dynamic roasts based on real data
function generateRoast(coin) {
    if (coin.liquidations > 100000000) {
        return `${coin.symbol} just liquidated $${coin.liquidations/1e6}M... you too?`;
    }
    if (coin.priceChange < -20) {
        return `${coin.symbol} down ${coin.priceChange}%... classic`;
    }
    if (coin.fundingRate > 0.1) {
        return `${coin.symbol} funding rate at ${coin.fundingRate}%... longs getting rekt`;
    }
}
```

#### Real-Time Price Updates
```javascript
// WebSocket connection for live prices
const ws = new WebSocket('wss://stream.coinglass.com');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // Update demo with real-time data
    updateCoinPrices(data);
    
    // Trigger wreckage events on big moves
    if (data.priceChange < -10) {
        showFlashCrash(data.symbol);
        addTerminalLine(`> 🚨 ${data.symbol} flash crash detected!`);
        addTerminalLine(`> Wreckage incoming...`);
    }
};
```

#### Dynamic Terminal Messages
```javascript
// Fetch recent liquidations
async function getRecentLiquidations() {
    const liquidations = await coinglass.getLiquidations();
    
    return [
        `> Someone just lost $${liquidations[0].amount} on ${liquidations[0].symbol}`,
        `> ${liquidations.length} liquidations in the last hour`,
        `> Total wreckage: $${liquidations.reduce((a, b) => a + b.amount, 0)}`,
        `> You're in good company`
    ];
}
```

---

## 2. Prediction Markets - Live Event Integration

### News API Integration

#### Data Sources
```javascript
// NewsAPI.org
- Breaking crypto news
- Sentiment analysis
- Event detection

// Twitter/X API
- Trending topics
- Viral predictions
- Community sentiment

// Google Trends
- Search volume for crypto terms
- Regional interest
- Related queries

// Reddit API
- r/CryptoCurrency sentiment
- Popular predictions
- Loss stories
```

#### Auto-Generated Markets

##### Example: Zelensky Suit Ordeal
```javascript
// Detect trending event
const event = detectTrendingEvent();
// "Zelensky suit controversy trending"

// Auto-generate prediction market
const market = {
    question: "Will the Zelensky suit ordeal affect crypto donations?",
    outcomes: ["YES", "NO"],
    context: "Trending on Twitter with 50k mentions",
    expiresIn: "24 hours",
    roast: "Betting on geopolitics? Bold move."
};

// Create market automatically
createMarket(market);
```

##### Real-Time Market Generation
```javascript
async function generateMarketsFromNews() {
    const news = await fetchCryptoNews();
    
    const markets = news
        .filter(article => article.sentiment === 'controversial')
        .map(article => ({
            question: generateQuestion(article),
            context: article.headline,
            trending: article.mentions,
            expires: Date.now() + 86400000 // 24h
        }));
    
    return markets;
}

// Example outputs:
// "Will SEC approve Bitcoin ETF this week?"
// "Will FTX customers get their money back?"
// "Will Do Kwon be extradited?"
// "Will Binance survive this lawsuit?"
```

#### Social Sentiment Markets
```javascript
// Track Twitter sentiment
async function createSentimentMarket() {
    const sentiment = await analyzeTweets('#Bitcoin');
    
    return {
        question: `Will Bitcoin sentiment stay bullish? (Currently ${sentiment.score}/100)`,
        outcomes: ["YES", "NO"],
        context: `Based on ${sentiment.tweetCount} tweets`,
        roast: sentiment.score < 30 
            ? "Bearish tweets everywhere... you're not alone"
            : "Everyone's bullish... time to short?"
    };
}
```

---

## 3. Implementation Architecture

### Backend Service
```javascript
// market-generator-service.js
const express = require('express');
const app = express();

// Fetch live data every 5 minutes
setInterval(async () => {
    // Get trending crypto events
    const cryptoNews = await fetchCryptoNews();
    const liquidations = await fetchLiquidations();
    const sentiment = await analyzeSocialSentiment();
    
    // Generate markets
    const markets = generateMarkets({
        news: cryptoNews,
        liquidations,
        sentiment
    });
    
    // Update demo
    updateDemo(markets);
}, 300000);

// API endpoint for demo
app.get('/api/trending-wreckage', async (req, res) => {
    const data = {
        coins: await getTrendingWreckage(),
        markets: await getActiveMarkets(),
        recentLosses: await getRecentLiquidations()
    };
    res.json(data);
});
```

### Demo Integration
```javascript
// interactive-demo.html
async function loadLiveData() {
    const data = await fetch('/api/trending-wreckage');
    
    // Update coin selector with trending disasters
    updateCoinSelector(data.coins);
    
    // Show recent liquidations in terminal
    data.recentLosses.forEach(loss => {
        addTerminalLine(`> ${loss.message}`);
    });
    
    // Display active prediction markets
    renderPredictionMarkets(data.markets);
}

// Refresh every 30 seconds
setInterval(loadLiveData, 30000);
```

---

## 4. Specific Use Cases

### Zelensky Suit Example
```javascript
// Detected event
{
    event: "Zelensky suit controversy",
    source: "Twitter trending",
    mentions: 50000,
    sentiment: -0.3, // Negative
    relatedTopics: ["crypto donations", "Ukraine", "politics"]
}

// Generated markets
[
    {
        question: "Will crypto donations to Ukraine drop this week?",
        roast: "Betting on geopolitics? That's a new low."
    },
    {
        question: "Will Zelensky address the suit controversy?",
        roast: "More important things to worry about tbh."
    },
    {
        question: "Will this affect crypto adoption in Ukraine?",
        roast: "Probably not, but you'll lose money anyway."
    }
]
```

### Crypto Flash Crash Example
```javascript
// Detected event
{
    event: "BTC flash crash",
    priceChange: -15%,
    liquidations: $500M,
    timeframe: "5 minutes"
}

// Generated markets
[
    {
        question: "Will BTC recover to $65k within 24h?",
        roast: "Buying the dip? Classic."
    },
    {
        question: "Will more liquidations follow?",
        roast: "Spoiler: yes."
    }
]

// Demo updates
addTerminalLine('> 🚨 FLASH CRASH DETECTED');
addTerminalLine('> $500M liquidated in 5 minutes');
addTerminalLine('> Processing wreckage...');
showFlashCrashAnimation();
```

### Exchange Drama Example
```javascript
// Detected event
{
    event: "Binance lawsuit",
    source: "Reuters",
    sentiment: -0.7,
    impact: "high"
}

// Generated markets
[
    {
        question: "Will BNB drop below $200?",
        roast: "CZ can't save you now."
    },
    {
        question: "Will users withdraw from Binance?",
        roast: "Bank run speedrun any%"
    }
]
```

---

## 5. Data Sources & APIs

### Free APIs
```javascript
// CoinGecko (Free)
https://api.coingecko.com/api/v3/coins/markets

// CryptoCompare (Free tier)
https://min-api.cryptocompare.com/data/price

// NewsAPI (Free tier)
https://newsapi.org/v2/everything?q=cryptocurrency

// Reddit API (Free)
https://www.reddit.com/r/CryptoCurrency.json
```

### Paid APIs (You Have)
```javascript
// Coinglass (You already have this!)
- Liquidation data
- Funding rates
- Long/short ratios
- Open interest

// Twitter API (Paid)
- Real-time trending topics
- Sentiment analysis
- Viral tweets
```

---

## 6. Implementation Phases

### Phase 1: Crypto Demo Live Data
1. Integrate Coinglass API for liquidations
2. Add real-time price updates
3. Dynamic coin selection based on trending disasters
4. Live terminal messages from recent liquidations

### Phase 2: Prediction Markets
1. Set up news aggregation service
2. Auto-generate markets from trending events
3. Social sentiment analysis
4. Market expiration and resolution

### Phase 3: Full Integration
1. WebSocket connections for real-time updates
2. Push notifications for major events
3. Community market creation
4. Historical data analysis

---

## 7. Snarky Copy for Live Events

### Flash Crash
- "🚨 Flash crash detected! Time to panic sell?"
- "$500M liquidated... you're not alone"
- "This is fine. Everything is fine."

### Exchange Drama
- "Another exchange in trouble... classic"
- "Not your keys, not your coins (told you)"
- "Time to move to cold storage?"

### Regulatory News
- "SEC strikes again... shocking"
- "Regulatory clarity (lol)"
- "At least you can lose money legally now"

### Viral Predictions
- "Everyone's calling the top... time to buy?"
- "Twitter analysts at it again"
- "This aged well (it didn't)"

---

## 8. Technical Requirements

### Backend
```bash
npm install express axios ws node-cron
npm install sentiment twitter-api-v2 newsapi
```

### Environment Variables
```bash
COINGLASS_API_KEY=your_key
TWITTER_API_KEY=your_key
NEWSAPI_KEY=your_key
```

### Cron Jobs
```javascript
// Update markets every 5 minutes
cron.schedule('*/5 * * * *', updateMarkets);

// Check for trending events every 15 minutes
cron.schedule('*/15 * * * *', checkTrendingEvents);

// Resolve expired markets every hour
cron.schedule('0 * * * *', resolveMarkets);
```

---

**Next Steps:**
1. Set up news aggregation service
2. Integrate Coinglass API for live liquidations
3. Add WebSocket for real-time price updates
4. Auto-generate markets from trending events
5. Test with Zelensky suit example
6. Deploy to production

This keeps the wreckage processing current and relevant to what's actually happening in crypto. 🍟💀
