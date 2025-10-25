# Chainlink Oracle Integration for USD_FRY

## Overview
Integrate Chainlink oracles to provide decentralized, tamper-proof data feeds for wreckage processing and prediction markets.

---

## Use Cases

### 1. Price Feeds for Wreckage Processing
Use Chainlink Price Feeds to get real-time, verified crypto prices for accurate wreckage calculation.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract WreckageProcessorWithOracle {
    AggregatorV3Interface internal btcPriceFeed;
    AggregatorV3Interface internal ethPriceFeed;
    AggregatorV3Interface internal solPriceFeed;
    
    // Arbitrum Mainnet Price Feeds
    constructor() {
        btcPriceFeed = AggregatorV3Interface(0x6ce185860a4963106506C203335A2910413708e9); // BTC/USD
        ethPriceFeed = AggregatorV3Interface(0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612); // ETH/USD
        // Add more as needed
    }
    
    /**
     * Get latest BTC price from Chainlink
     */
    function getLatestBTCPrice() public view returns (int) {
        (
            /* uint80 roundID */,
            int price,
            /* uint startedAt */,
            /* uint timeStamp */,
            /* uint80 answeredInRound */
        ) = btcPriceFeed.latestRoundData();
        return price; // Returns price with 8 decimals
    }
    
    /**
     * Calculate wreckage value in USD using Chainlink price
     */
    function calculateWreckageValue(
        string memory asset,
        uint256 amount
    ) public view returns (uint256) {
        int price;
        
        if (keccak256(bytes(asset)) == keccak256(bytes("BTC"))) {
            price = getLatestBTCPrice();
        } else if (keccak256(bytes(asset)) == keccak256(bytes("ETH"))) {
            (, price, , , ) = ethPriceFeed.latestRoundData();
        }
        // Add more assets
        
        require(price > 0, "Invalid price");
        
        // Calculate USD value
        uint256 usdValue = (amount * uint256(price)) / 1e8; // Adjust for decimals
        return usdValue;
    }
    
    /**
     * Process wreckage with verified price data
     */
    function processWreckageWithOracle(
        string memory asset,
        uint256 amount
    ) external returns (uint256 fryMinted) {
        // Get verified price from Chainlink
        uint256 usdValue = calculateWreckageValue(asset, amount);
        
        // Mint FRY at 2.26x rate
        fryMinted = usdValue * 226 / 100;
        
        // Mint FRY tokens
        _mintFRY(msg.sender, fryMinted);
        
        emit WreckageProcessed(msg.sender, asset, amount, usdValue, fryMinted);
        
        return fryMinted;
    }
}
```

### 2. Prediction Market Resolution with Chainlink
Use Chainlink to automatically resolve prediction markets based on real-world data.

```solidity
contract FRYPredictionMarketWithOracle {
    AggregatorV3Interface internal priceFeed;
    
    struct Market {
        uint256 id;
        string question;
        uint256 targetPrice;
        uint256 resolutionTime;
        bool resolved;
        bool outcome; // true = YES, false = NO
    }
    
    mapping(uint256 => Market) public markets;
    
    /**
     * Create price-based prediction market
     * Example: "Will BTC hit $100k by Dec 31?"
     */
    function createPriceMarket(
        string memory question,
        uint256 targetPrice,
        uint256 resolutionTime
    ) external returns (uint256 marketId) {
        marketId = markets.length;
        
        markets[marketId] = Market({
            id: marketId,
            question: question,
            targetPrice: targetPrice,
            resolutionTime: resolutionTime,
            resolved: false,
            outcome: false
        });
        
        return marketId;
    }
    
    /**
     * Resolve market using Chainlink price feed
     */
    function resolveMarket(uint256 marketId) external {
        Market storage market = markets[marketId];
        
        require(!market.resolved, "Already resolved");
        require(block.timestamp >= market.resolutionTime, "Too early");
        
        // Get price from Chainlink
        (, int price, , , ) = priceFeed.latestRoundData();
        
        // Determine outcome
        market.outcome = uint256(price) >= market.targetPrice;
        market.resolved = true;
        
        // Process wreckage for losers
        _processMarketLosses(marketId);
        
        emit MarketResolved(marketId, market.outcome, uint256(price));
    }
    
    /**
     * Process losses and mint FRY to losers
     */
    function _processMarketLosses(uint256 marketId) internal {
        Market storage market = markets[marketId];
        
        // Get all losing bets
        Bet[] memory losingBets = getLosingBets(marketId, !market.outcome);
        
        // Process each loss
        for (uint i = 0; i < losingBets.length; i++) {
            uint256 loss = losingBets[i].amount;
            uint256 fryAmount = loss * 226 / 100; // 2.26x rate
            
            // Mint FRY to loser
            _mintFRY(losingBets[i].bettor, fryAmount);
            
            emit WreckageProcessed(
                losingBets[i].bettor,
                "PREDICTION_MARKET",
                loss,
                fryAmount
            );
        }
    }
}
```

### 3. Chainlink Automation for Demo Updates
Use Chainlink Keepers (now Automation) to automatically update demo data.

```solidity
import "@chainlink/contracts/src/v0.8/AutomationCompatible.sol";

contract LiveDemoUpdater is AutomationCompatibleInterface {
    uint256 public lastUpdate;
    uint256 public updateInterval = 300; // 5 minutes
    
    struct TrendingCoin {
        string symbol;
        uint256 liquidations;
        int256 priceChange;
        string roast;
    }
    
    TrendingCoin[] public trendingCoins;
    
    /**
     * Chainlink Automation checks if update needed
     */
    function checkUpkeep(bytes calldata /* checkData */)
        external
        view
        override
        returns (bool upkeepNeeded, bytes memory /* performData */)
    {
        upkeepNeeded = (block.timestamp - lastUpdate) > updateInterval;
    }
    
    /**
     * Chainlink Automation performs update
     */
    function performUpkeep(bytes calldata /* performData */) external override {
        if ((block.timestamp - lastUpdate) > updateInterval) {
            lastUpdate = block.timestamp;
            
            // Update trending coins data
            _updateTrendingCoins();
            
            emit DemoDataUpdated(block.timestamp);
        }
    }
    
    /**
     * Update trending coins with latest data
     */
    function _updateTrendingCoins() internal {
        // Fetch data from Chainlink oracles
        // Update trending coins array
        // Generate new roasts based on data
    }
}
```

### 4. Any API Integration with Chainlink Functions
Use Chainlink Functions to fetch data from ANY API (Coinglass, Twitter, news APIs).

```solidity
import {FunctionsClient} from "@chainlink/contracts/src/v0.8/functions/dev/v1_0_0/FunctionsClient.sol";
import {FunctionsRequest} from "@chainlink/contracts/src/v0.8/functions/dev/v1_0_0/libraries/FunctionsRequest.sol";

contract FRYWithChainlinkFunctions is FunctionsClient {
    using FunctionsRequest for FunctionsRequest.Request;
    
    bytes32 public lastRequestId;
    bytes public lastResponse;
    bytes public lastError;
    
    // Chainlink Functions JavaScript code
    string public source = 
        "const apiKey = secrets.coinglassKey;"
        "const url = `https://open-api.coinglass.com/public/v2/liquidation?time_type=1h&symbol=all`;"
        "const response = await Functions.makeHttpRequest({"
        "  url: url,"
        "  headers: { 'coinglassSecret': apiKey }"
        "});"
        "const data = response.data.data;"
        "const topLiquidations = data"
        "  .sort((a, b) => b.longLiquidationUsd - a.longLiquidationUsd)"
        "  .slice(0, 5);"
        "return Functions.encodeString(JSON.stringify(topLiquidations));";
    
    /**
     * Fetch liquidation data from Coinglass API
     */
    function fetchLiquidationData() external returns (bytes32 requestId) {
        FunctionsRequest.Request memory req;
        req.initializeRequestForInlineJavaScript(source);
        
        // Add encrypted secrets (API keys)
        req.addSecretsReference(encryptedSecretsUrls);
        
        // Send request
        lastRequestId = _sendRequest(
            req.encodeCBOR(),
            subscriptionId,
            gasLimit,
            donID
        );
        
        return lastRequestId;
    }
    
    /**
     * Callback from Chainlink Functions
     */
    function fulfillRequest(
        bytes32 requestId,
        bytes memory response,
        bytes memory err
    ) internal override {
        lastResponse = response;
        lastError = err;
        
        // Decode response
        string memory liquidationData = string(response);
        
        // Update trending coins
        _updateTrendingCoins(liquidationData);
        
        emit LiquidationDataUpdated(liquidationData);
    }
}
```

---

## Architecture

### Demo Integration
```
Interactive Demo (Frontend)
    ↓
Live Market Service (Backend)
    ↓
Chainlink Oracles (On-chain)
    ↓
External APIs (Coinglass, Twitter, etc.)
```

### Smart Contract Flow
```
User submits wreckage
    ↓
Contract queries Chainlink Price Feed
    ↓
Verified price returned
    ↓
Calculate USD value
    ↓
Mint FRY at 2.26x rate
    ↓
Emit event with verified data
```

---

## Benefits

### 1. Decentralization
- No single point of failure
- Tamper-proof data
- Trustless verification

### 2. Accuracy
- Real-time price feeds
- Multiple data sources
- Median aggregation

### 3. Automation
- Auto-resolve prediction markets
- Scheduled demo updates
- No manual intervention needed

### 4. Flexibility
- Any API via Chainlink Functions
- Custom data sources
- Encrypted API keys

---

## Implementation Plan

### Phase 1: Price Feeds
1. Integrate Chainlink Price Feeds for BTC, ETH, SOL, XRP
2. Update WreckageProcessor contract to use oracle prices
3. Deploy to Arbitrum testnet
4. Test with demo

### Phase 2: Prediction Markets
1. Create FRYPredictionMarket contract with oracle resolution
2. Auto-resolve markets based on Chainlink data
3. Process losses and mint FRY to losers
4. Add to demo

### Phase 3: Chainlink Functions
1. Set up Chainlink Functions subscription
2. Create JavaScript code to fetch Coinglass data
3. Store encrypted API keys
4. Update demo with real-time data

### Phase 4: Automation
1. Set up Chainlink Automation (Keepers)
2. Auto-update demo every 5 minutes
3. Auto-resolve expired markets
4. Monitor upkeep performance

---

## Code Examples

### Get Latest Price
```javascript
// Frontend: Query Chainlink price feed
const priceFeed = new ethers.Contract(
    '0x6ce185860a4963106506C203335A2910413708e9', // BTC/USD on Arbitrum
    priceFeedABI,
    provider
);

const latestPrice = await priceFeed.latestRoundData();
console.log('BTC Price:', latestPrice.answer.toString() / 1e8);
```

### Process Wreckage with Oracle
```javascript
// Process wreckage with verified price
const tx = await wreckageProcessor.processWreckageWithOracle(
    'BTC',
    ethers.utils.parseEther('0.1') // 0.1 BTC
);

await tx.wait();
console.log('Wreckage processed with Chainlink-verified price');
```

### Create Prediction Market
```javascript
// Create market: "Will BTC hit $100k by Dec 31?"
const tx = await predictionMarket.createPriceMarket(
    "Will BTC hit $100k by Dec 31?",
    100000 * 1e8, // $100k with 8 decimals
    Math.floor(new Date('2025-12-31').getTime() / 1000)
);

await tx.wait();
console.log('Market created with Chainlink auto-resolution');
```

---

## Chainlink Networks

### Arbitrum Mainnet Price Feeds
- BTC/USD: `0x6ce185860a4963106506C203335A2910413708e9`
- ETH/USD: `0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612`
- LINK/USD: `0x86E53CF1B870786351Da77A57575e79CB55812CB`

### Arbitrum Sepolia (Testnet)
- BTC/USD: `0x56a43EB56Da12C0dc1D972ACb089c06a5dEF8e69`
- ETH/USD: `0xd30e2101a97dcbAeBCBC04F14C3f624E67A35165`

### Chainlink Functions
- Arbitrum Mainnet: Available
- Arbitrum Sepolia: Available for testing

---

## Cost Considerations

### Price Feeds
- **Free to read** on-chain
- Gas cost only for transactions
- ~50k gas per price query

### Chainlink Functions
- ~0.2 LINK per request
- Depends on computation complexity
- Can batch requests to save costs

### Chainlink Automation
- ~0.1 LINK per upkeep
- Configurable frequency
- Pay only when executed

---

## Demo Enhancement Ideas

### 1. Live Price Ticker
Show real-time prices from Chainlink in demo header:
```
BTC: $67,234 | ETH: $3,456 | SOL: $123
(Powered by Chainlink)
```

### 2. Verified Wreckage Processing
Add badge to demo:
```
✓ Prices verified by Chainlink Oracle Network
✓ Tamper-proof data feeds
✓ Decentralized verification
```

### 3. Auto-Resolving Markets
Show countdown to resolution:
```
Market: "Will BTC hit $100k by Dec 31?"
Resolves in: 45 days
Current Price: $67,234 (via Chainlink)
Auto-resolution enabled ✓
```

### 4. Oracle Status Indicator
```
🟢 Chainlink Oracle: Online
📊 Last Update: 2 seconds ago
🔒 Data Verified: Yes
```

---

## Next Steps

1. **Set up Chainlink subscription** on Arbitrum Sepolia
2. **Integrate price feeds** into WreckageProcessor contract
3. **Test oracle queries** with demo
4. **Add Chainlink Functions** for Coinglass data
5. **Deploy Automation** for scheduled updates
6. **Update demo UI** with oracle indicators

This gives USD_FRY enterprise-grade data reliability while maintaining decentralization. 🍟⛓️
