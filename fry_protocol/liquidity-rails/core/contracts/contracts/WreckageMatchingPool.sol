// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

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
 * @title WreckageMatchingPool
 * @dev P2P matching pool for offsetting funding rate positions
 * 
 * Features:
 * - Cash-settled funding rate swaps
 * - Cross-DEX position matching
 * - Highest USD_FRY minting rate (1.4x)
 * - No token transfers needed
 */
contract WreckageMatchingPool is ReentrancyGuard, AccessControl {
    
    bytes32 public constant MATCHER_ROLE = keccak256("MATCHER_ROLE");
    
    IUSDFRYToken public usdFryToken;
    
    // Position types
    enum PositionType { LONG, SHORT }
    
    // Wreckage position
    struct WreckagePosition {
        address trader;
        PositionType positionType;
        string dex;
        string asset;
        uint256 amountUSD;
        uint256 fundingRate;  // Basis points
        uint256 timestamp;
        bool isMatched;
        bytes32 matchId;
    }
    
    // Match between two positions
    struct Match {
        bytes32 position1Id;
        bytes32 position2Id;
        uint256 matchedAmount;
        uint256 fryMinted1;
        uint256 fryMinted2;
        uint256 timestamp;
    }
    
    mapping(bytes32 => WreckagePosition) public positions;
    mapping(bytes32 => Match) public matches;
    
    bytes32[] public unmatchedPositions;
    bytes32[] public allMatchIds;
    
    // Statistics
    uint256 public totalPositionsSubmitted;
    uint256 public totalPositionsMatched;
    uint256 public totalMatchedVolume;
    uint256 public totalFryFromMatching;
    
    // Events
    event PositionSubmitted(
        bytes32 indexed positionId,
        address indexed trader,
        PositionType positionType,
        string dex,
        string asset,
        uint256 amountUSD
    );
    
    event PositionsMatched(
        bytes32 indexed matchId,
        bytes32 position1Id,
        bytes32 position2Id,
        uint256 matchedAmount,
        uint256 fryMinted1,
        uint256 fryMinted2
    );
    
    constructor(address _usdFryToken) {
        usdFryToken = IUSDFRYToken(_usdFryToken);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MATCHER_ROLE, msg.sender);
    }
    
    /**
     * @dev Submit wreckage position for matching
     */
    function submitPosition(
        PositionType positionType,
        string memory dex,
        string memory asset,
        uint256 amountUSD,
        uint256 fundingRate
    ) external nonReentrant returns (bytes32) {
        require(amountUSD > 0, "Amount must be > 0");
        require(fundingRate > 0, "Funding rate must be > 0");
        
        bytes32 positionId = keccak256(abi.encodePacked(
            msg.sender,
            positionType,
            dex,
            asset,
            amountUSD,
            block.timestamp,
            totalPositionsSubmitted
        ));
        
        positions[positionId] = WreckagePosition({
            trader: msg.sender,
            positionType: positionType,
            dex: dex,
            asset: asset,
            amountUSD: amountUSD,
            fundingRate: fundingRate,
            timestamp: block.timestamp,
            isMatched: false,
            matchId: bytes32(0)
        });
        
        unmatchedPositions.push(positionId);
        totalPositionsSubmitted++;
        
        emit PositionSubmitted(
            positionId,
            msg.sender,
            positionType,
            dex,
            asset,
            amountUSD
        );
        
        // Try to match immediately
        _tryMatch(positionId);
        
        return positionId;
    }
    
    /**
     * @dev Try to match a position with existing unmatched positions
     */
    function _tryMatch(bytes32 newPositionId) internal {
        WreckagePosition storage newPos = positions[newPositionId];
        
        // Look for offsetting position
        for (uint256 i = 0; i < unmatchedPositions.length; i++) {
            bytes32 candidateId = unmatchedPositions[i];
            
            if (candidateId == newPositionId) continue;
            
            WreckagePosition storage candidate = positions[candidateId];
            
            if (candidate.isMatched) continue;
            
            // Check if positions offset each other
            if (_canMatch(newPos, candidate)) {
                _executeMatch(newPositionId, candidateId);
                return;
            }
        }
    }
    
    /**
     * @dev Check if two positions can be matched
     */
    function _canMatch(
        WreckagePosition storage pos1,
        WreckagePosition storage pos2
    ) internal view returns (bool) {
        // Must be opposite position types
        if (pos1.positionType == pos2.positionType) return false;
        
        // Must be same asset
        if (keccak256(bytes(pos1.asset)) != keccak256(bytes(pos2.asset))) return false;
        
        // Must have similar amounts (within 20%)
        uint256 minAmount = pos1.amountUSD < pos2.amountUSD ? pos1.amountUSD : pos2.amountUSD;
        uint256 maxAmount = pos1.amountUSD > pos2.amountUSD ? pos1.amountUSD : pos2.amountUSD;
        
        if (maxAmount > minAmount * 120 / 100) return false;
        
        return true;
    }
    
    /**
     * @dev Execute match between two positions
     */
    function _executeMatch(bytes32 pos1Id, bytes32 pos2Id) internal {
        WreckagePosition storage pos1 = positions[pos1Id];
        WreckagePosition storage pos2 = positions[pos2Id];
        
        // Calculate matched amount (minimum of the two)
        uint256 matchedAmount = pos1.amountUSD < pos2.amountUSD ? 
            pos1.amountUSD : pos2.amountUSD;
        
        // Mint USD_FRY for both traders (P2P rate = 1.4x)
        // Efficiency score = 10000 (100%) for P2P matches
        uint256 fryMinted1 = usdFryToken.mintFromWreckage(
            pos1.trader,
            matchedAmount,
            pos1.dex,
            "USDH", // Default to native stablecoin
            "p2p",
            10000
        );
        
        uint256 fryMinted2 = usdFryToken.mintFromWreckage(
            pos2.trader,
            matchedAmount,
            pos2.dex,
            "USDH",
            "p2p",
            10000
        );
        
        // Create match record
        bytes32 matchId = keccak256(abi.encodePacked(
            pos1Id,
            pos2Id,
            block.timestamp
        ));
        
        matches[matchId] = Match({
            position1Id: pos1Id,
            position2Id: pos2Id,
            matchedAmount: matchedAmount,
            fryMinted1: fryMinted1,
            fryMinted2: fryMinted2,
            timestamp: block.timestamp
        });
        
        allMatchIds.push(matchId);
        
        // Mark positions as matched
        pos1.isMatched = true;
        pos1.matchId = matchId;
        pos2.isMatched = true;
        pos2.matchId = matchId;
        
        // Update statistics
        totalPositionsMatched += 2;
        totalMatchedVolume += matchedAmount * 2;
        totalFryFromMatching += fryMinted1 + fryMinted2;
        
        emit PositionsMatched(
            matchId,
            pos1Id,
            pos2Id,
            matchedAmount,
            fryMinted1,
            fryMinted2
        );
    }
    
    /**
     * @dev Manual match by operator (for complex cases)
     */
    function manualMatch(
        bytes32 pos1Id,
        bytes32 pos2Id
    ) external onlyRole(MATCHER_ROLE) nonReentrant {
        WreckagePosition storage pos1 = positions[pos1Id];
        WreckagePosition storage pos2 = positions[pos2Id];
        
        require(!pos1.isMatched, "Position 1 already matched");
        require(!pos2.isMatched, "Position 2 already matched");
        require(_canMatch(pos1, pos2), "Positions cannot be matched");
        
        _executeMatch(pos1Id, pos2Id);
    }
    
    /**
     * @dev Get position details
     */
    function getPosition(bytes32 positionId) external view returns (WreckagePosition memory) {
        return positions[positionId];
    }
    
    /**
     * @dev Get match details
     */
    function getMatch(bytes32 matchId) external view returns (Match memory) {
        return matches[matchId];
    }
    
    /**
     * @dev Get unmatched positions count
     */
    function getUnmatchedCount() external view returns (uint256) {
        uint256 count = 0;
        for (uint256 i = 0; i < unmatchedPositions.length; i++) {
            if (!positions[unmatchedPositions[i]].isMatched) {
                count++;
            }
        }
        return count;
    }
    
    /**
     * @dev Get system statistics
     */
    function getSystemStats() external view returns (
        uint256 positionsSubmitted,
        uint256 positionsMatched,
        uint256 matchedVolume,
        uint256 fryMinted,
        uint256 matchRate
    ) {
        positionsSubmitted = totalPositionsSubmitted;
        positionsMatched = totalPositionsMatched;
        matchedVolume = totalMatchedVolume;
        fryMinted = totalFryFromMatching;
        
        if (positionsSubmitted > 0) {
            matchRate = (positionsMatched * 10000) / positionsSubmitted;
        } else {
            matchRate = 0;
        }
    }
}
