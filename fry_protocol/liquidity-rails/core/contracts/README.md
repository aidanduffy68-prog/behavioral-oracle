# USD_FRY Protocol Smart Contracts

Production-ready smart contracts for the USD_FRY liquidity rails system.

## Contracts

### Core Contracts

1. **USDFRYToken.sol** - Wreckage-backed stablecoin
   - Multi-tier minting rates (base, rails, P2P)
   - Native stablecoin bonuses (USDH, USDF)
   - Wreckage event tracking
   - Supply limit: 1B USD_FRY
   - USD-denominated, wreckage-backed

2. **LiquidityRailsRouter.sol** - On-chain routing for wreckage
   - Multi-hop routing (up to 3 hops)
   - Venue management (Hyperliquid, Aster)
   - Optimal path finding
   - USD_FRY minting with efficiency bonuses

3. **WreckageMatchingPool.sol** - P2P matching for funding swaps
   - Cash-settled position matching
   - Cross-DEX offsetting
   - Highest USD_FRY rate (1.4x)
   - Automatic matching engine

### Privacy Contracts

4. **AgentBVerifier.sol** - zkML proof verification
   - EZKL-generated proof verification
   - Client reputation tracking
   - On-chain accuracy verification

5. **ConfidentialPositionVerifier.sol** - Pedersen commitments
   - Confidential position tracking
   - Range proofs (0 ≤ v ≤ Vmax)
   - Homomorphic aggregation

## Setup

### Install Dependencies

```bash
npm install
```

### Configure Environment

```bash
cp .env.example .env
# Edit .env with your keys
```

Required environment variables:
- `PRIVATE_KEY` - Deployment wallet private key
- `ARBITRUM_SEPOLIA_RPC` - Arbitrum Sepolia RPC URL
- `ARBITRUM_RPC` - Arbitrum mainnet RPC URL
- `ARBISCAN_API_KEY` - Arbiscan API key for verification

## Deployment

### Local Testing

```bash
npm run deploy:local
```

### Arbitrum Sepolia (Testnet)

```bash
npm run deploy:testnet
```

### Arbitrum One (Mainnet)

```bash
npm run deploy:mainnet
```

## Verification

After deployment, verify contracts on Arbiscan:

```bash
npm run verify:testnet  # For testnet
npm run verify:mainnet  # For mainnet
```

Or manually:

```bash
npx hardhat verify --network arbitrumSepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

## Contract Addresses

### Arbitrum Sepolia (Testnet)
- USDFRYToken: TBD
- LiquidityRailsRouter: TBD
- WreckageMatchingPool: TBD
- AgentBVerifier: TBD
- ConfidentialPositionVerifier: TBD

### Arbitrum One (Mainnet)
- USDFRYToken: TBD
- LiquidityRailsRouter: TBD
- WreckageMatchingPool: TBD
- AgentBVerifier: TBD
- ConfidentialPositionVerifier: TBD

## Usage

### Minting USD_FRY from Wreckage

```solidity
// Route wreckage through liquidity rails
uint256 usdFryMinted = router.routeWreckage(
    100000 * 10**18,  // $100k wreckage
    2                  // Max 2 hops
);
```

### P2P Matching

```solidity
// Submit position for matching
bytes32 positionId = matchingPool.submitPosition(
    PositionType.LONG,
    "Hyperliquid",
    "BTC",
    50000 * 10**18,   // $50k position
    100                // 1% funding rate
);
```

### Check Statistics

```solidity
// Get system stats
(uint256 wreckage, uint256 usdFry, uint256 rate,,) = usdFryToken.getSystemStats();
```

## Testing

Run the test suite:

```bash
npm test
```

## Security

- All contracts use OpenZeppelin libraries
- ReentrancyGuard on all state-changing functions
- AccessControl for role-based permissions
- Ready for audit (Certik/Trail of Bits)

## Gas Costs (Arbitrum L2)

| Operation | Gas | Cost (0.1 gwei) |
|-----------|-----|-----------------|
| Route wreckage | ~150k | $0.015 |
| Submit position | ~100k | $0.010 |
| Mint USD_FRY | ~80k | $0.008 |
| Verify zkML proof | ~250k | $0.025 |

## License

MIT
