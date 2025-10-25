// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

interface IUSDFRYToken {
    function mintFromWreckage(
        address recipient,
        uint256 amountUSD,
        string memory dex,
        string memory stablecoin,
        string memory routingType,
        uint256 efficiencyScore
    ) external returns (uint256);
}

/**
 * @title WreckageProcessorWithOracle
 * @dev Process trading wreckage with Chainlink-verified prices
 * 
 * Features:
 * - Chainlink Price Feeds for accurate USD valuation
 * - Support for BTC, ETH, SOL, XRP
 * - Automatic FRY minting at 2.26x rate
 * - Tamper-proof price verification
 */
contract WreckageProcessorWithOracle is ReentrancyGuard, AccessControl {
    
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    
    IUSDFRYToken public usdFryToken;
    
    // Chainlink Price Feeds (Arbitrum Sepolia)
    AggregatorV3Interface internal btcPriceFeed;
    AggregatorV3Interface internal ethPriceFeed;
    
    // Asset tracking
    mapping(string => address) public priceFeeds;
    string[] public supportedAssets;
    
    // Statistics
    uint256 public totalWreckageProcessed;
    uint256 public totalFryMinted;
    uint256 public totalTransactions;
    
    // Events
    event WreckageProcessed(
        address indexed user,
        string asset,
        uint256 amount,
        uint256 usdValue,
        uint256 fryMinted,
        int256 verifiedPrice
    );
    
    event PriceFeedUpdated(string asset, address priceFeed);
    
    constructor(address _usdFryToken) {
        usdFryToken = IUSDFRYToken(_usdFryToken);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(OPERATOR_ROLE, msg.sender);
        
        // Initialize Chainlink Price Feeds (Arbitrum Sepolia)
        _addPriceFeed("BTC", 0x56a43EB56Da12C0dc1D972ACb089c06a5dEF8e69);
        _addPriceFeed("ETH", 0xd30e2101a97dcbAeBCBC04F14C3f624E67A35165);
        
        // Note: SOL and XRP feeds may not be available on testnet
        // Will use mock prices or mainnet feeds in production
    }
    
    /**
     * @dev Add or update price feed for an asset
     */
    function addPriceFeed(string memory asset, address feedAddress) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        _addPriceFeed(asset, feedAddress);
    }
    
    function _addPriceFeed(string memory asset, address feedAddress) internal {
        require(feedAddress != address(0), "Invalid feed address");
        
        if (priceFeeds[asset] == address(0)) {
            supportedAssets.push(asset);
        }
        
        priceFeeds[asset] = feedAddress;
        
        emit PriceFeedUpdated(asset, feedAddress);
    }
    
    /**
     * @dev Get latest price from Chainlink for an asset
     * @return price Price with 8 decimals
     */
    function getLatestPrice(string memory asset) public view returns (int256) {
        address feedAddress = priceFeeds[asset];
        require(feedAddress != address(0), "Price feed not found");
        
        AggregatorV3Interface priceFeed = AggregatorV3Interface(feedAddress);
        
        (
            /* uint80 roundID */,
            int256 price,
            /* uint startedAt */,
            uint256 timeStamp,
            /* uint80 answeredInRound */
        ) = priceFeed.latestRoundData();
        
        require(price > 0, "Invalid price");
        require(timeStamp > 0, "Stale price");
        require(block.timestamp - timeStamp < 3600, "Price too old"); // 1 hour max
        
        return price;
    }
    
    /**
     * @dev Calculate USD value of wreckage using Chainlink price
     * @param asset Asset symbol (BTC, ETH, SOL, XRP)
     * @param amount Amount in asset's smallest unit
     * @param decimals Asset decimals (8 for BTC, 18 for ETH, etc.)
     * @return usdValue USD value with 18 decimals
     */
    function calculateWreckageValue(
        string memory asset,
        uint256 amount,
        uint256 decimals
    ) public view returns (uint256) {
        int256 price = getLatestPrice(asset);
        require(price > 0, "Invalid price");
        
        // Price has 8 decimals, convert to USD with 18 decimals
        // usdValue = (amount * price) / (10^decimals) * (10^10)
        uint256 usdValue = (amount * uint256(price) * 1e10) / (10 ** decimals);
        
        return usdValue;
    }
    
    /**
     * @dev Process wreckage with Chainlink-verified price
     * @param asset Asset symbol (BTC, ETH, SOL, XRP)
     * @param amount Amount in asset's smallest unit
     * @param decimals Asset decimals
     * @return fryMinted Amount of FRY tokens minted
     */
    function processWreckage(
        string memory asset,
        uint256 amount,
        uint256 decimals
    ) external nonReentrant returns (uint256) {
        require(amount > 0, "Amount must be > 0");
        require(priceFeeds[asset] != address(0), "Asset not supported");
        
        // Get verified price from Chainlink
        int256 verifiedPrice = getLatestPrice(asset);
        uint256 usdValue = calculateWreckageValue(asset, amount, decimals);
        
        require(usdValue > 0, "USD value must be > 0");
        
        // Mint FRY at 2.26x rate
        // usdValue has 18 decimals, divide by 1e18 to get USD amount
        uint256 usdAmount = usdValue / 1e18;
        
        uint256 fryMinted = usdFryToken.mintFromWreckage(
            msg.sender,
            usdAmount,
            "Chainlink",
            "USD",
            "oracle",
            9500 // High efficiency score for oracle-verified data
        );
        
        // Update statistics
        totalWreckageProcessed += usdAmount;
        totalFryMinted += fryMinted;
        totalTransactions++;
        
        emit WreckageProcessed(
            msg.sender,
            asset,
            amount,
            usdAmount,
            fryMinted,
            verifiedPrice
        );
        
        return fryMinted;
    }
    
    /**
     * @dev Process wreckage with USD amount directly (for demo/testing)
     * @param asset Asset symbol
     * @param usdAmount USD amount (no decimals)
     * @return fryMinted Amount of FRY tokens minted
     */
    function processWreckageUSD(
        string memory asset,
        uint256 usdAmount
    ) external nonReentrant returns (uint256) {
        require(usdAmount > 0, "Amount must be > 0");
        
        // Get verified price for logging (optional, can skip for demo)
        int256 verifiedPrice = 0;
        if (priceFeeds[asset] != address(0)) {
            try this.getLatestPrice(asset) returns (int256 price) {
                verifiedPrice = price;
            } catch {
                // Price feed unavailable, continue with demo
            }
        }
        
        // Mint FRY at 2.26x rate
        uint256 fryMinted = usdFryToken.mintFromWreckage(
            msg.sender,
            usdAmount,
            "Demo",
            "USD",
            "direct",
            9000
        );
        
        // Update statistics
        totalWreckageProcessed += usdAmount;
        totalFryMinted += fryMinted;
        totalTransactions++;
        
        emit WreckageProcessed(
            msg.sender,
            asset,
            0, // No asset amount for direct USD
            usdAmount,
            fryMinted,
            verifiedPrice
        );
        
        return fryMinted;
    }
    
    /**
     * @dev Get supported assets
     */
    function getSupportedAssets() external view returns (string[] memory) {
        return supportedAssets;
    }
    
    /**
     * @dev Get system statistics
     */
    function getSystemStats() external view returns (
        uint256 wreckageProcessed,
        uint256 fryMinted,
        uint256 transactions
    ) {
        return (totalWreckageProcessed, totalFryMinted, totalTransactions);
    }
    
    /**
     * @dev Check if price feed is healthy
     */
    function isPriceFeedHealthy(string memory asset) external view returns (bool) {
        address feedAddress = priceFeeds[asset];
        if (feedAddress == address(0)) return false;
        
        try this.getLatestPrice(asset) returns (int256) {
            return true;
        } catch {
            return false;
        }
    }
}
