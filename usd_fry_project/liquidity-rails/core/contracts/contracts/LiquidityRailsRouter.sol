// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

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
 * @title LiquidityRailsRouter
 * @dev On-chain router for wreckage routing across DEX venues
 * 
 * Features:
 * - Multi-hop routing (up to 3 hops)
 * - Native stablecoin integration (USDH, USDF)
 * - Optimal path finding
 * - USD_FRY minting with bonuses
 */
contract LiquidityRailsRouter is ReentrancyGuard, AccessControl {
    
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    
    IUSDFRYToken public usdFryToken;
    
    // Venue configuration
    struct Venue {
        string name;
        string stablecoin;
        uint256 liquidityUSD;
        uint256 costBps;        // Cost in basis points
        bool isActive;
    }
    
    mapping(bytes32 => Venue) public venues;
    bytes32[] public venueIds;
    
    // Route tracking
    struct Route {
        bytes32[] venueIds;
        uint256 totalCostBps;
        uint256 fryMinted;
        uint256 timestamp;
    }
    
    mapping(bytes32 => Route) public routes;
    bytes32[] public allRouteIds;
    
    // Statistics
    uint256 public totalWreckageRouted;
    uint256 public totalFryMinted;
    uint256 public totalRoutesExecuted;
    
    // Events
    event VenueAdded(bytes32 indexed venueId, string name, string stablecoin);
    event VenueUpdated(bytes32 indexed venueId, uint256 liquidity, uint256 costBps);
    event VenueDeactivated(bytes32 indexed venueId);
    
    event RouteExecuted(
        bytes32 indexed routeId,
        address indexed user,
        uint256 amountUSD,
        uint256 fryMinted,
        uint256 numHops,
        uint256 totalCostBps
    );
    
    constructor(address _usdFryToken) {
        usdFryToken = IUSDFRYToken(_usdFryToken);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(OPERATOR_ROLE, msg.sender);
        
        // Initialize venues with native stablecoins
        _addVenue("Hyperliquid", "USDH", 150_000_000 * 10**18, 7);
        _addVenue("Aster", "USDF", 75_000_000 * 10**18, 9);
    }
    
    /**
     * @dev Add new venue
     */
    function addVenue(
        string memory name,
        string memory stablecoin,
        uint256 liquidityUSD,
        uint256 costBps
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _addVenue(name, stablecoin, liquidityUSD, costBps);
    }
    
    function _addVenue(
        string memory name,
        string memory stablecoin,
        uint256 liquidityUSD,
        uint256 costBps
    ) internal {
        bytes32 venueId = keccak256(abi.encodePacked(name, stablecoin));
        
        venues[venueId] = Venue({
            name: name,
            stablecoin: stablecoin,
            liquidityUSD: liquidityUSD,
            costBps: costBps,
            isActive: true
        });
        
        venueIds.push(venueId);
        
        emit VenueAdded(venueId, name, stablecoin);
    }
    
    /**
     * @dev Update venue liquidity and cost
     */
    function updateVenue(
        bytes32 venueId,
        uint256 liquidityUSD,
        uint256 costBps
    ) external onlyRole(OPERATOR_ROLE) {
        require(venues[venueId].isActive, "Venue not active");
        
        venues[venueId].liquidityUSD = liquidityUSD;
        venues[venueId].costBps = costBps;
        
        emit VenueUpdated(venueId, liquidityUSD, costBps);
    }
    
    /**
     * @dev Deactivate venue
     */
    function deactivateVenue(bytes32 venueId) external onlyRole(DEFAULT_ADMIN_ROLE) {
        venues[venueId].isActive = false;
        emit VenueDeactivated(venueId);
    }
    
    /**
     * @dev Route wreckage through optimal path
     * @param amountUSD Wreckage amount in USD
     * @param maxHops Maximum number of hops (1-3)
     * @return fryMinted Amount of FRY minted
     */
    function routeWreckage(
        uint256 amountUSD,
        uint256 maxHops
    ) external nonReentrant returns (uint256) {
        require(amountUSD > 0, "Amount must be > 0");
        require(maxHops > 0 && maxHops <= 3, "Invalid max hops");
        
        // Find optimal route
        (bytes32[] memory optimalPath, uint256 totalCost) = _findOptimalRoute(amountUSD, maxHops);
        require(optimalPath.length > 0, "No route found");
        
        // Calculate efficiency score (10000 - cost)
        uint256 efficiencyScore = totalCost < 10000 ? 10000 - totalCost : 0;
        
        // Determine routing type based on hops
        string memory routingType = optimalPath.length == 1 ? "base" : "rails";
        
        // Get first venue's stablecoin
        Venue memory firstVenue = venues[optimalPath[0]];
        
        // Mint USD_FRY
        uint256 fryMinted = usdFryToken.mintFromWreckage(
            msg.sender,
            amountUSD,
            firstVenue.name,
            firstVenue.stablecoin,
            routingType,
            efficiencyScore
        );
        
        // Record route
        bytes32 routeId = keccak256(abi.encodePacked(
            msg.sender,
            amountUSD,
            block.timestamp,
            allRouteIds.length
        ));
        
        routes[routeId] = Route({
            venueIds: optimalPath,
            totalCostBps: totalCost,
            fryMinted: fryMinted,
            timestamp: block.timestamp
        });
        
        allRouteIds.push(routeId);
        
        // Update statistics
        totalWreckageRouted += amountUSD;
        totalFryMinted += fryMinted;
        totalRoutesExecuted++;
        
        emit RouteExecuted(
            routeId,
            msg.sender,
            amountUSD,
            fryMinted,
            optimalPath.length,
            totalCost
        );
        
        return fryMinted;
    }
    
    /**
     * @dev Find optimal route through venues
     * @return path Array of venue IDs
     * @return totalCost Total cost in basis points
     */
    function _findOptimalRoute(
        uint256 amountUSD,
        uint256 maxHops
    ) internal view returns (bytes32[] memory path, uint256 totalCost) {
        uint256 bestCost = type(uint256).max;
        bytes32[] memory bestPath;
        
        // Single-hop routes
        for (uint256 i = 0; i < venueIds.length; i++) {
            bytes32 venueId = venueIds[i];
            Venue memory venue = venues[venueId];
            
            if (!venue.isActive || venue.liquidityUSD < amountUSD) continue;
            
            uint256 cost = venue.costBps;
            
            if (cost < bestCost) {
                bestCost = cost;
                bestPath = new bytes32[](1);
                bestPath[0] = venueId;
            }
        }
        
        // Multi-hop routes (if maxHops > 1)
        if (maxHops > 1) {
            for (uint256 i = 0; i < venueIds.length; i++) {
                for (uint256 j = 0; j < venueIds.length; j++) {
                    if (i == j) continue;
                    
                    bytes32 venue1 = venueIds[i];
                    bytes32 venue2 = venueIds[j];
                    
                    if (!venues[venue1].isActive || !venues[venue2].isActive) continue;
                    
                    uint256 splitAmount = amountUSD / 2;
                    if (venues[venue1].liquidityUSD < splitAmount || 
                        venues[venue2].liquidityUSD < splitAmount) continue;
                    
                    uint256 cost = (venues[venue1].costBps + venues[venue2].costBps) / 2;
                    
                    if (cost < bestCost) {
                        bestCost = cost;
                        bestPath = new bytes32[](2);
                        bestPath[0] = venue1;
                        bestPath[1] = venue2;
                    }
                }
            }
        }
        
        return (bestPath, bestCost);
    }
    
    /**
     * @dev Get route details
     */
    function getRoute(bytes32 routeId) external view returns (Route memory) {
        return routes[routeId];
    }
    
    /**
     * @dev Get venue details
     */
    function getVenue(bytes32 venueId) external view returns (Venue memory) {
        return venues[venueId];
    }
    
    /**
     * @dev Get all active venues
     */
    function getActiveVenues() external view returns (bytes32[] memory) {
        uint256 activeCount = 0;
        for (uint256 i = 0; i < venueIds.length; i++) {
            if (venues[venueIds[i]].isActive) {
                activeCount++;
            }
        }
        
        bytes32[] memory activeVenues = new bytes32[](activeCount);
        uint256 index = 0;
        
        for (uint256 i = 0; i < venueIds.length; i++) {
            if (venues[venueIds[i]].isActive) {
                activeVenues[index] = venueIds[i];
                index++;
            }
        }
        
        return activeVenues;
    }
    
    /**
     * @dev Get system statistics
     */
    function getSystemStats() external view returns (
        uint256 wreckageRouted,
        uint256 fryMinted,
        uint256 routesExecuted,
        uint256 activeVenues
    ) {
        wreckageRouted = totalWreckageRouted;
        fryMinted = totalFryMinted;
        routesExecuted = totalRoutesExecuted;
        
        uint256 count = 0;
        for (uint256 i = 0; i < venueIds.length; i++) {
            if (venues[venueIds[i]].isActive) {
                count++;
            }
        }
        activeVenues = count;
    }
}
