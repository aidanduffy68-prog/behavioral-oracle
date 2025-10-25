# Chainlink Oracle Integration

## Contracts

### 1. WreckageProcessorWithOracle.sol
Process trading wreckage with Chainlink-verified prices.

**Features:**
- Chainlink Price Feeds for BTC, ETH (SOL, XRP on mainnet)
- Automatic USD valuation
- FRY minting at 2.26x rate
- Tamper-proof price verification

**Functions:**
```solidity
// Process wreckage with asset amount
processWreckage(string asset, uint256 amount, uint256 decimals)

// Process wreckage with USD amount (for demo)
processWreckageUSD(string asset, uint256 usdAmount)

// Get latest Chainlink price
getLatestPrice(string asset) returns (int256)

// Check if price feed is healthy
isPriceFeedHealthy(string asset) returns (bool)
```

### 2. FRYPredictionMarket.sol
Prediction markets with Chainlink auto-resolution.

**Features:**
- Price-based prediction markets
- Chainlink oracle auto-resolution
- Losers receive FRY at 2.26x rate
- Winners receive 70% of losing pool

**Functions:**
```solidity
// Create market (OPERATOR_ROLE only)
createMarket(
    string question,
    string asset,
    uint256 targetPrice,
    uint256 resolutionTime,
    address priceFeed
)

// Place bet
placeBet(uint256 marketId, bool prediction, uint256 amount)

// Resolve market using Chainlink
resolveMarket(uint256 marketId)

// Claim winnings
claimWinnings(uint256 marketId)
```

## Deployment

### Install Dependencies
```bash
cd liquidity-rails/core/contracts
npm install
```

This will install:
- `@openzeppelin/contracts`
- `@chainlink/contracts`

### Configure Environment
Create `.env` file:
```bash
PRIVATE_KEY=your_private_key
ARBISCAN_API_KEY=your_arbiscan_key
```

### Deploy to Arbitrum Sepolia
```bash
npm run deploy:testnet
```

Or manually:
```bash
npx hardhat run scripts/deploy-oracle-contracts.js --network arbitrumSepolia
```

## Chainlink Price Feeds

### Arbitrum Sepolia (Testnet)
- **BTC/USD**: `0x56a43EB56Da12C0dc1D972ACb089c06a5dEF8e69`
- **ETH/USD**: `0xd30e2101a97dcbAeBCBC04F14C3f624E67A35165`

### Arbitrum Mainnet
- **BTC/USD**: `0x6ce185860a4963106506C203335A2910413708e9`
- **ETH/USD**: `0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612`
- **LINK/USD**: `0x86E53CF1B870786351Da77A57575e79CB55812CB`
- **SOL/USD**: Available (check Chainlink docs)
- **XRP/USD**: Available (check Chainlink docs)

## Usage Examples

### Process Wreckage with Oracle
```javascript
const wreckageProcessor = await ethers.getContractAt(
    "WreckageProcessorWithOracle",
    "0x..." // deployed address
);

// Process 0.1 BTC wreckage
const tx = await wreckageProcessor.processWreckage(
    "BTC",
    ethers.utils.parseUnits("0.1", 8), // 0.1 BTC with 8 decimals
    8 // BTC decimals
);

await tx.wait();
console.log("Wreckage processed with Chainlink-verified price");
```

### Create Prediction Market
```javascript
const predictionMarket = await ethers.getContractAt(
    "FRYPredictionMarket",
    "0x..." // deployed address
);

// Create market: "Will BTC hit $100k by Dec 31?"
const tx = await predictionMarket.createMarket(
    "Will BTC hit $100k by Dec 31?",
    "BTC",
    100000 * 1e8, // $100k with 8 decimals
    Math.floor(new Date('2025-12-31').getTime() / 1000), // Resolution time
    "0x56a43EB56Da12C0dc1D972ACb089c06a5dEF8e69" // BTC/USD feed
);

await tx.wait();
```

### Place Bet
```javascript
// Approve USDC
const usdc = await ethers.getContractAt("IERC20", usdcAddress);
await usdc.approve(predictionMarket.address, ethers.utils.parseUnits("100", 6));

// Place $100 bet on YES
const tx = await predictionMarket.placeBet(
    0, // marketId
    true, // YES
    ethers.utils.parseUnits("100", 6) // $100 USDC
);

await tx.wait();
```

### Resolve Market
```javascript
// Anyone can call this after resolution time
const tx = await predictionMarket.resolveMarket(0);
await tx.wait();

// Chainlink price is checked automatically
// Losers receive FRY tokens
// Winners can claim payouts
```

## Integration with Demo

### Update interactive-demo.html
```javascript
// Connect to WreckageProcessor
const wreckageProcessor = new ethers.Contract(
    '0x...', // deployed address
    wreckageProcessorABI,
    signer
);

// Process wreckage with Chainlink price
async function processWreckageWithOracle(asset, usdAmount) {
    const tx = await wreckageProcessor.processWreckageUSD(asset, usdAmount);
    await tx.wait();
    
    addTerminalLine('> ✓ Wreckage processed with Chainlink-verified price');
    addTerminalLine('> Price feed: Decentralized oracle network');
}

// Show live Chainlink price
async function showLivePrice(asset) {
    const price = await wreckageProcessor.getLatestPrice(asset);
    const priceUSD = price / 1e8; // Convert from 8 decimals
    
    document.getElementById('price-ticker').innerHTML = 
        `${asset}: $${priceUSD.toLocaleString()} (via Chainlink ✓)`;
}
```

## Benefits

### Decentralization
- No single point of failure
- Multiple node operators
- Tamper-proof data

### Accuracy
- Real-time price feeds
- Sub-second updates
- Median aggregation

### Automation
- Auto-resolve prediction markets
- No manual intervention
- Trustless execution

## Cost Estimates

### Price Feed Reads
- **Free to read** on-chain
- ~50k gas per query
- ~$0.01 per read at 0.1 gwei

### Market Resolution
- ~200k gas
- ~$0.04 at 0.1 gwei
- Includes FRY minting to all losers

## Testing

### Local Testing
```bash
npx hardhat test
```

### Testnet Testing
1. Get Arbitrum Sepolia ETH from faucet
2. Deploy contracts
3. Process test wreckage
4. Create test market
5. Resolve market after time

## Verification

### Verify on Arbiscan
```bash
npm run verify:testnet
```

Or manually:
```bash
npx hardhat verify --network arbitrumSepolia DEPLOYED_ADDRESS "CONSTRUCTOR_ARGS"
```

## Next Steps

1. ✅ Deploy contracts to Arbitrum Sepolia
2. ✅ Verify on Arbiscan
3. Update demo with contract addresses
4. Add Chainlink price ticker to demo
5. Create sample prediction markets
6. Test full flow: bet → resolve → claim
7. Deploy to mainnet

## Resources

- [Chainlink Price Feeds](https://docs.chain.link/data-feeds/price-feeds/addresses?network=arbitrum)
- [Chainlink Functions](https://docs.chain.link/chainlink-functions)
- [Chainlink Automation](https://docs.chain.link/chainlink-automation)
- [Arbitrum Sepolia Faucet](https://faucet.quicknode.com/arbitrum/sepolia)
