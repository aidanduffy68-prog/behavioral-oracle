// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

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
 * @title FRYPredictionMarket
 * @dev Prediction markets with Chainlink auto-resolution and wreckage processing
 * 
 * Features:
 * - Price-based prediction markets
 * - Chainlink oracle auto-resolution
 * - Losers receive FRY tokens at 2.26x rate
 * - Winners receive stablecoin payouts
 */
contract FRYPredictionMarket is ReentrancyGuard, AccessControl {
    
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    
    IUSDFRYToken public usdFryToken;
    IERC20 public stablecoin; // USDC or similar
    
    // Market structure
    struct Market {
        uint256 id;
        string question;
        string asset; // BTC, ETH, etc.
        uint256 targetPrice; // Price with 8 decimals
        uint256 resolutionTime;
        bool resolved;
        bool outcome; // true = YES (price >= target), false = NO
        uint256 totalYesBets;
        uint256 totalNoBets;
        address priceFeed;
    }
    
    // Bet structure
    struct Bet {
        address bettor;
        uint256 marketId;
        bool prediction; // true = YES, false = NO
        uint256 amount;
        bool claimed;
    }
    
    mapping(uint256 => Market) public markets;
    mapping(uint256 => Bet[]) public marketBets;
    mapping(address => uint256[]) public userBets;
    
    uint256 public marketCount;
    uint256 public totalMarketsResolved;
    uint256 public totalWreckageProcessed;
    
    // Events
    event MarketCreated(
        uint256 indexed marketId,
        string question,
        string asset,
        uint256 targetPrice,
        uint256 resolutionTime
    );
    
    event BetPlaced(
        uint256 indexed marketId,
        address indexed bettor,
        bool prediction,
        uint256 amount
    );
    
    event MarketResolved(
        uint256 indexed marketId,
        bool outcome,
        int256 finalPrice,
        uint256 timestamp
    );
    
    event WreckageProcessed(
        uint256 indexed marketId,
        address indexed loser,
        uint256 lossAmount,
        uint256 fryMinted
    );
    
    event WinningsClaimed(
        uint256 indexed marketId,
        address indexed winner,
        uint256 payout
    );
    
    constructor(address _usdFryToken, address _stablecoin) {
        usdFryToken = IUSDFRYToken(_usdFryToken);
        stablecoin = IERC20(_stablecoin);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(OPERATOR_ROLE, msg.sender);
    }
    
    /**
     * @dev Create price-based prediction market
     * @param question Market question
     * @param asset Asset symbol (BTC, ETH, etc.)
     * @param targetPrice Target price with 8 decimals
     * @param resolutionTime Unix timestamp for resolution
     * @param priceFeed Chainlink price feed address
     */
    function createMarket(
        string memory question,
        string memory asset,
        uint256 targetPrice,
        uint256 resolutionTime,
        address priceFeed
    ) external onlyRole(OPERATOR_ROLE) returns (uint256) {
        require(resolutionTime > block.timestamp, "Resolution time must be in future");
        require(priceFeed != address(0), "Invalid price feed");
        require(targetPrice > 0, "Invalid target price");
        
        uint256 marketId = marketCount++;
        
        markets[marketId] = Market({
            id: marketId,
            question: question,
            asset: asset,
            targetPrice: targetPrice,
            resolutionTime: resolutionTime,
            resolved: false,
            outcome: false,
            totalYesBets: 0,
            totalNoBets: 0,
            priceFeed: priceFeed
        });
        
        emit MarketCreated(marketId, question, asset, targetPrice, resolutionTime);
        
        return marketId;
    }
    
    /**
     * @dev Place bet on market
     * @param marketId Market ID
     * @param prediction true = YES, false = NO
     * @param amount Bet amount in stablecoin
     */
    function placeBet(
        uint256 marketId,
        bool prediction,
        uint256 amount
    ) external nonReentrant {
        Market storage market = markets[marketId];
        
        require(!market.resolved, "Market already resolved");
        require(block.timestamp < market.resolutionTime, "Market closed");
        require(amount > 0, "Amount must be > 0");
        
        // Transfer stablecoin from bettor
        require(
            stablecoin.transferFrom(msg.sender, address(this), amount),
            "Transfer failed"
        );
        
        // Record bet
        Bet memory newBet = Bet({
            bettor: msg.sender,
            marketId: marketId,
            prediction: prediction,
            amount: amount,
            claimed: false
        });
        
        marketBets[marketId].push(newBet);
        userBets[msg.sender].push(marketBets[marketId].length - 1);
        
        // Update totals
        if (prediction) {
            market.totalYesBets += amount;
        } else {
            market.totalNoBets += amount;
        }
        
        emit BetPlaced(marketId, msg.sender, prediction, amount);
    }
    
    /**
     * @dev Resolve market using Chainlink price feed
     * @param marketId Market ID
     */
    function resolveMarket(uint256 marketId) external nonReentrant {
        Market storage market = markets[marketId];
        
        require(!market.resolved, "Already resolved");
        require(block.timestamp >= market.resolutionTime, "Too early to resolve");
        
        // Get price from Chainlink
        AggregatorV3Interface priceFeed = AggregatorV3Interface(market.priceFeed);
        
        (
            /* uint80 roundID */,
            int256 price,
            /* uint startedAt */,
            uint256 timeStamp,
            /* uint80 answeredInRound */
        ) = priceFeed.latestRoundData();
        
        require(price > 0, "Invalid price");
        require(timeStamp > 0, "Stale price");
        
        // Determine outcome: YES if price >= target, NO otherwise
        market.outcome = uint256(price) >= market.targetPrice;
        market.resolved = true;
        totalMarketsResolved++;
        
        emit MarketResolved(marketId, market.outcome, price, block.timestamp);
        
        // Process wreckage for losers
        _processMarketLosses(marketId);
    }
    
    /**
     * @dev Process losses and mint FRY to losers
     */
    function _processMarketLosses(uint256 marketId) internal {
        Market storage market = markets[marketId];
        Bet[] storage bets = marketBets[marketId];
        
        for (uint256 i = 0; i < bets.length; i++) {
            Bet storage bet = bets[i];
            
            // Check if this bet lost
            if (bet.prediction != market.outcome) {
                // Mint FRY to loser at 2.26x rate
                uint256 fryMinted = usdFryToken.mintFromWreckage(
                    bet.bettor,
                    bet.amount,
                    "PredictionMarket",
                    "USDC",
                    "market_loss",
                    8500 // Efficiency score for prediction market
                );
                
                totalWreckageProcessed += bet.amount;
                
                emit WreckageProcessed(marketId, bet.bettor, bet.amount, fryMinted);
            }
        }
    }
    
    /**
     * @dev Claim winnings
     * @param marketId Market ID
     */
    function claimWinnings(uint256 marketId) external nonReentrant {
        Market storage market = markets[marketId];
        require(market.resolved, "Market not resolved");
        
        Bet[] storage bets = marketBets[marketId];
        uint256 totalPayout = 0;
        
        for (uint256 i = 0; i < bets.length; i++) {
            Bet storage bet = bets[i];
            
            // Check if this is a winning bet by this user
            if (bet.bettor == msg.sender && 
                bet.prediction == market.outcome && 
                !bet.claimed) {
                
                // Calculate payout
                uint256 winningPool = market.outcome ? market.totalYesBets : market.totalNoBets;
                uint256 losingPool = market.outcome ? market.totalNoBets : market.totalYesBets;
                
                // Payout = bet amount + (bet amount / winning pool) * (losing pool * 0.7)
                // 70% of losing pool goes to winners, 30% to FRY backing
                uint256 share = (bet.amount * losingPool * 70) / (winningPool * 100);
                uint256 payout = bet.amount + share;
                
                totalPayout += payout;
                bet.claimed = true;
            }
        }
        
        require(totalPayout > 0, "No winnings to claim");
        
        // Transfer winnings
        require(
            stablecoin.transfer(msg.sender, totalPayout),
            "Transfer failed"
        );
        
        emit WinningsClaimed(marketId, msg.sender, totalPayout);
    }
    
    /**
     * @dev Get market details
     */
    function getMarket(uint256 marketId) external view returns (Market memory) {
        return markets[marketId];
    }
    
    /**
     * @dev Get market bets
     */
    function getMarketBets(uint256 marketId) external view returns (Bet[] memory) {
        return marketBets[marketId];
    }
    
    /**
     * @dev Get user's bets
     */
    function getUserBets(address user) external view returns (uint256[] memory) {
        return userBets[user];
    }
    
    /**
     * @dev Get system statistics
     */
    function getSystemStats() external view returns (
        uint256 totalMarkets,
        uint256 marketsResolved,
        uint256 wreckageProcessed
    ) {
        return (marketCount, totalMarketsResolved, totalWreckageProcessed);
    }
}
