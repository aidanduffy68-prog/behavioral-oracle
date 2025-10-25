// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title USDFRYToken
 * @dev USD_FRY - The first wreckage-backed stablecoin
 * 
 * Core Features:
 * - Wreckage-based minting (losses → USD_FRY)
 * - Native stablecoin bonuses (USDH, USDF)
 * - Multi-tier minting rates
 * - USD-denominated, wreckage-backed
 */
contract USDFRYToken is ERC20, AccessControl, ReentrancyGuard {
    
    // Roles
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant ROUTER_ROLE = keccak256("ROUTER_ROLE");
    
    // Minting rates (basis points, 10000 = 100%)
    uint256 public constant BASE_RATE = 5000;           // 0.5 USD_FRY per $1
    uint256 public constant RAILS_RATE = 12000;         // 1.2 USD_FRY per $1
    uint256 public constant P2P_RATE = 14000;           // 1.4 USD_FRY per $1
    uint256 public constant NATIVE_BONUS = 5000;        // 50% bonus
    uint256 public constant EFFICIENCY_BONUS = 3000;    // 30% max
    uint256 public constant LIQUIDITY_BONUS = 6000;     // 60% bonus
    
    // Supply limits
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18; // 1B USD_FRY
    
    // Supported native stablecoins
    mapping(string => bool) public nativeStablecoins;
    mapping(string => string) public stablecoinToDex;
    
    // Wreckage tracking
    struct WreckageEvent {
        address minter;
        uint256 amountUSD;
        uint256 fryMinted;
        string dex;
        string stablecoin;
        uint256 timestamp;
        uint256 mintingRate;
    }
    
    mapping(bytes32 => WreckageEvent) public wreckageEvents;
    bytes32[] public allWreckageIds;
    
    // Statistics
    uint256 public totalWreckageProcessed;
    uint256 public totalFryFromWreckage;
    mapping(address => uint256) public userWreckageProcessed;
    mapping(address => uint256) public userFryEarned;
    
    // Events
    event WreckageMinted(
        bytes32 indexed wreckageId,
        address indexed minter,
        uint256 amountUSD,
        uint256 fryMinted,
        string dex,
        string stablecoin,
        uint256 mintingRate
    );
    
    event NativeStablecoinAdded(string stablecoin, string dex);
    event NativeStablecoinRemoved(string stablecoin);
    
    constructor() ERC20("USD_FRY Wreckage-Backed Stablecoin", "USD_FRY") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        
        // Initialize native stablecoins
        _addNativeStablecoin("USDH", "Hyperliquid");
        _addNativeStablecoin("USDF", "Aster");
    }
    
    /**
     * @dev Mint USD_FRY from wreckage event
     * @param recipient Address to receive FRY
     * @param amountUSD Wreckage amount in USD (18 decimals)
     * @param dex DEX name
     * @param stablecoin Stablecoin used
     * @param routingType Type of routing (base, rails, p2p)
     * @param efficiencyScore Efficiency score (0-10000)
     */
    function mintFromWreckage(
        address recipient,
        uint256 amountUSD,
        string memory dex,
        string memory stablecoin,
        string memory routingType,
        uint256 efficiencyScore
    ) external onlyRole(MINTER_ROLE) nonReentrant returns (uint256) {
        require(recipient != address(0), "Invalid recipient");
        require(amountUSD > 0, "Amount must be > 0");
        require(efficiencyScore <= 10000, "Invalid efficiency score");
        
        // Calculate base USD_FRY amount
        uint256 baseRate = _getBaseRate(routingType);
        uint256 baseFry = (amountUSD * baseRate) / 10000;
        
        // Calculate bonuses
        uint256 totalBonus = 0;
        
        // Native stablecoin bonus
        if (nativeStablecoins[stablecoin]) {
            totalBonus += NATIVE_BONUS;
        }
        
        // Efficiency bonus (scaled by efficiency score)
        totalBonus += (EFFICIENCY_BONUS * efficiencyScore) / 10000;
        
        // Liquidity provision bonus (for rails/p2p)
        if (keccak256(bytes(routingType)) != keccak256(bytes("base"))) {
            totalBonus += LIQUIDITY_BONUS;
        }
        
        // Calculate final USD_FRY amount
        uint256 fryAmount = baseFry + (baseFry * totalBonus) / 10000;
        
        // Check supply limit
        require(totalSupply() + fryAmount <= MAX_SUPPLY, "Max supply exceeded");
        
        // Mint USD_FRY
        _mint(recipient, fryAmount);
        
        // Record wreckage event
        bytes32 wreckageId = keccak256(abi.encodePacked(
            recipient,
            amountUSD,
            dex,
            block.timestamp,
            allWreckageIds.length
        ));
        
        uint256 effectiveRate = (fryAmount * 10000) / amountUSD;
        
        wreckageEvents[wreckageId] = WreckageEvent({
            minter: recipient,
            amountUSD: amountUSD,
            fryMinted: fryAmount,
            dex: dex,
            stablecoin: stablecoin,
            timestamp: block.timestamp,
            mintingRate: effectiveRate
        });
        
        allWreckageIds.push(wreckageId);
        
        // Update statistics
        totalWreckageProcessed += amountUSD;
        totalFryFromWreckage += fryAmount;
        userWreckageProcessed[recipient] += amountUSD;
        userFryEarned[recipient] += fryAmount;
        
        emit WreckageMinted(
            wreckageId,
            recipient,
            amountUSD,
            fryAmount,
            dex,
            stablecoin,
            effectiveRate
        );
        
        return fryAmount;
    }
    
    /**
     * @dev Get base minting rate for routing type
     */
    function _getBaseRate(string memory routingType) internal pure returns (uint256) {
        bytes32 typeHash = keccak256(bytes(routingType));
        
        if (typeHash == keccak256(bytes("p2p"))) {
            return P2P_RATE;
        } else if (typeHash == keccak256(bytes("rails"))) {
            return RAILS_RATE;
        } else {
            return BASE_RATE;
        }
    }
    
    /**
     * @dev Add native stablecoin
     */
    function addNativeStablecoin(
        string memory stablecoin,
        string memory dex
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _addNativeStablecoin(stablecoin, dex);
    }
    
    function _addNativeStablecoin(string memory stablecoin, string memory dex) internal {
        nativeStablecoins[stablecoin] = true;
        stablecoinToDex[stablecoin] = dex;
        emit NativeStablecoinAdded(stablecoin, dex);
    }
    
    /**
     * @dev Remove native stablecoin
     */
    function removeNativeStablecoin(
        string memory stablecoin
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        nativeStablecoins[stablecoin] = false;
        delete stablecoinToDex[stablecoin];
        emit NativeStablecoinRemoved(stablecoin);
    }
    
    /**
     * @dev Get wreckage event by ID
     */
    function getWreckageEvent(bytes32 wreckageId) external view returns (WreckageEvent memory) {
        return wreckageEvents[wreckageId];
    }
    
    /**
     * @dev Get total wreckage events
     */
    function getTotalWreckageEvents() external view returns (uint256) {
        return allWreckageIds.length;
    }
    
    /**
     * @dev Get user statistics
     */
    function getUserStats(address user) external view returns (
        uint256 wreckageProcessed,
        uint256 fryEarned,
        uint256 effectiveRate
    ) {
        wreckageProcessed = userWreckageProcessed[user];
        fryEarned = userFryEarned[user];
        
        if (wreckageProcessed > 0) {
            effectiveRate = (fryEarned * 10000) / wreckageProcessed;
        } else {
            effectiveRate = 0;
        }
    }
    
    /**
     * @dev Get system statistics
     */
    function getSystemStats() external view returns (
        uint256 wreckageProcessed,
        uint256 fryMinted,
        uint256 effectiveRate,
        uint256 supply,
        uint256 maxSupply
    ) {
        wreckageProcessed = totalWreckageProcessed;
        fryMinted = totalFryFromWreckage;
        
        if (wreckageProcessed > 0) {
            effectiveRate = (fryMinted * 10000) / wreckageProcessed;
        } else {
            effectiveRate = 0;
        }
        
        supply = totalSupply();
        maxSupply = MAX_SUPPLY;
    }
    
    /**
     * @dev Check if stablecoin is native
     */
    function isNativeStablecoin(string memory stablecoin) external view returns (bool) {
        return nativeStablecoins[stablecoin];
    }
}
