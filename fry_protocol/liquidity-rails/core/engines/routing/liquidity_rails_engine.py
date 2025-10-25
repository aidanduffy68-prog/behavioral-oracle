#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRY Liquidity Rails Engine
===========================

Infrastructure layer for routing wreckage through optimal liquidity paths.
Built by liquidity engineers for capital-efficient wreckage absorption.

Core Concept:
- Wreckage matching engine handles peer-to-peer matching
- Liquidity rails provide the plumbing for optimal routing
- Capital flows between venues based on liquidity gradients
- Market-making layer absorbs unmatched wreckage

Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    Wreckage Sources                         │
│  (Liquidations, Slippage, Funding Losses, Adverse Fills)   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              LIQUIDITY RAILS ENGINE                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Router    │→ │  Aggregator  │→ │  Market Maker   │  │
│  │  (Optimal   │  │  (Liquidity  │  │  (Absorption)   │  │
│  │   Paths)    │  │   Pooling)   │  │                 │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  FRY Minting Layer                          │
│  Enhanced rates for efficient routing + liquidity provision │
└─────────────────────────────────────────────────────────────┘

Features:
- Optimal wreckage routing across DEX network
- Liquidity aggregation for better fills
- Capital allocation based on minting surface gradients
- Market-making for unmatched wreckage
- Integration with topology + matching engines

Usage:
    from liquidity_rails_engine import LiquidityRailsEngine
    
    rails = LiquidityRailsEngine()
    route = rails.route_wreckage(wreckage_event)
    rails.execute_route(route)
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FRY color scheme
FRY_RED = "\033[91m"
FRY_YELLOW = "\033[93m"
FRY_GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"


@dataclass
class LiquidityPool:
    """Represents a liquidity pool at a DEX venue"""
    venue: str
    asset: str
    depth_usd: float
    spread_bps: float
    funding_rate: float
    utilization: float  # 0.0 to 1.0
    
    def available_liquidity(self) -> float:
        """Available liquidity for wreckage absorption"""
        return self.depth_usd * (1.0 - self.utilization)
    
    def cost_to_fill(self, amount_usd: float) -> float:
        """Cost to fill wreckage through this pool (slippage + spread)"""
        if amount_usd > self.available_liquidity():
            return float('inf')  # Can't fill
        
        # Slippage model: quadratic in fill ratio
        fill_ratio = amount_usd / self.depth_usd
        slippage_bps = fill_ratio ** 2 * 100  # Quadratic slippage
        
        total_cost_bps = self.spread_bps + slippage_bps
        return total_cost_bps


@dataclass
class WreckageRoute:
    """Optimal route for wreckage through liquidity rails"""
    wreckage_amount: float
    asset: str
    hops: List[Dict]  # List of venue hops with amounts
    total_cost_bps: float
    fry_minted: float
    efficiency_score: float
    
    def __repr__(self):
        path = " → ".join([h['venue'] for h in self.hops])
        return f"<Route {self.asset} ${self.wreckage_amount:.0f} via {path} | FRY: {self.fry_minted:.2f}>"


class LiquidityRailsEngine:
    """
    Core engine for routing wreckage through optimal liquidity paths.
    
    Integrates with:
    - Topology routing (minting surface gradients)
    - Wreckage matching (peer-to-peer swaps)
    - Agent B (market-making)
    """
    
    def __init__(self):
        self.liquidity_pools: Dict[str, List[LiquidityPool]] = {}
        self.capital_allocations: Dict[str, float] = {}
        self.total_wreckage_routed = 0.0
        self.total_fry_minted = 0.0
        
        # Minting rates
        self.base_fry_rate = 0.5  # Unoptimized
        self.rails_fry_rate = 1.2  # Optimized routing
        self.liquidity_bonus = 1.6  # Liquidity provision bonus
        
        # Initialize default liquidity pools
        self._initialize_liquidity_pools()
        
        logger.info(f"{FRY_RED}{BOLD}🛤️  Liquidity Rails Engine Initialized{RESET}")
        logger.info(f"Optimal wreckage routing across {len(self.liquidity_pools)} venues")
    
    def _initialize_liquidity_pools(self):
        """Initialize liquidity pools for major DEXes"""
        
        venues_config = [
            # venue, BTC_depth, ETH_depth, spread_bps, funding_rate
            ("dYdX", 50_000_000, 30_000_000, 2.5, -0.0015),
            ("Hyperliquid", 35_000_000, 25_000_000, 3.0, 0.0018),
            ("Aster", 40_000_000, 28_000_000, 2.8, -0.0012),
            ("GMX", 25_000_000, 18_000_000, 4.0, 0.0020),
            ("Vertex", 30_000_000, 20_000_000, 3.5, 0.0005),
        ]
        
        for venue, btc_depth, eth_depth, spread, funding in venues_config:
            if venue not in self.liquidity_pools:
                self.liquidity_pools[venue] = []
            
            # BTC pool
            self.liquidity_pools[venue].append(LiquidityPool(
                venue=venue,
                asset="BTC",
                depth_usd=btc_depth,
                spread_bps=spread,
                funding_rate=funding,
                utilization=np.random.uniform(0.3, 0.7)
            ))
            
            # ETH pool
            self.liquidity_pools[venue].append(LiquidityPool(
                venue=venue,
                asset="ETH",
                depth_usd=eth_depth,
                spread_bps=spread,
                funding_rate=funding,
                utilization=np.random.uniform(0.3, 0.7)
            ))
        
        logger.info(f"Initialized {sum(len(pools) for pools in self.liquidity_pools.values())} liquidity pools")
    
    def route_wreckage(self, amount_usd: float, asset: str, 
                       max_hops: int = 3) -> Optional[WreckageRoute]:
        """
        Find optimal route for wreckage through liquidity rails.
        
        Uses dynamic programming to find lowest-cost path with highest FRY yield.
        
        Args:
            amount_usd: Wreckage amount in USD
            asset: Asset type (BTC, ETH, etc.)
            max_hops: Maximum number of venue hops
        
        Returns:
            Optimal WreckageRoute or None if no route found
        """
        
        # Get all pools for this asset
        available_pools = []
        for venue, pools in self.liquidity_pools.items():
            for pool in pools:
                if pool.asset == asset and pool.available_liquidity() >= amount_usd * 0.1:
                    available_pools.append(pool)
        
        if not available_pools:
            logger.warning(f"No liquidity pools available for {asset}")
            return None
        
        # Single-hop routes (direct fill)
        best_route = None
        best_score = -float('inf')
        
        for pool in available_pools:
            cost_bps = pool.cost_to_fill(amount_usd)
            if cost_bps == float('inf'):
                continue
            
            # Calculate FRY minting for this route
            fry_minted = self._calculate_fry_minting(
                amount_usd, cost_bps, num_hops=1
            )
            
            # Efficiency score: FRY minted per cost
            efficiency = fry_minted / (1 + cost_bps / 100)
            
            if efficiency > best_score:
                best_score = efficiency
                best_route = WreckageRoute(
                    wreckage_amount=amount_usd,
                    asset=asset,
                    hops=[{
                        'venue': pool.venue,
                        'amount': amount_usd,
                        'cost_bps': cost_bps,
                        'liquidity_depth': pool.depth_usd
                    }],
                    total_cost_bps=cost_bps,
                    fry_minted=fry_minted,
                    efficiency_score=efficiency
                )
        
        # Multi-hop routes (split across venues)
        if max_hops > 1:
            multi_hop_route = self._find_multi_hop_route(
                amount_usd, asset, available_pools, max_hops
            )
            
            if multi_hop_route and multi_hop_route.efficiency_score > best_score:
                best_route = multi_hop_route
        
        if best_route:
            logger.info(f"{FRY_GREEN}✓{RESET} Optimal route found: {best_route}")
        
        return best_route
    
    def _find_multi_hop_route(self, amount_usd: float, asset: str,
                             pools: List[LiquidityPool], 
                             max_hops: int) -> Optional[WreckageRoute]:
        """
        Find optimal multi-hop route by splitting wreckage across venues.
        
        Uses greedy algorithm: fill cheapest pools first until wreckage absorbed.
        """
        
        # Sort pools by cost
        pool_costs = [(pool, pool.cost_to_fill(amount_usd / max_hops)) 
                     for pool in pools]
        pool_costs.sort(key=lambda x: x[1])
        
        hops = []
        remaining = amount_usd
        total_cost = 0.0
        
        for pool, _ in pool_costs[:max_hops]:
            if remaining <= 0:
                break
            
            # Fill as much as possible in this pool
            fill_amount = min(remaining, pool.available_liquidity())
            cost_bps = pool.cost_to_fill(fill_amount)
            
            if cost_bps == float('inf'):
                continue
            
            hops.append({
                'venue': pool.venue,
                'amount': fill_amount,
                'cost_bps': cost_bps,
                'liquidity_depth': pool.depth_usd
            })
            
            remaining -= fill_amount
            total_cost += cost_bps * (fill_amount / amount_usd)
        
        if remaining > amount_usd * 0.05:  # More than 5% unfilled
            return None
        
        # Calculate FRY minting for multi-hop route
        fry_minted = self._calculate_fry_minting(
            amount_usd, total_cost, num_hops=len(hops)
        )
        
        efficiency = fry_minted / (1 + total_cost / 100)
        
        return WreckageRoute(
            wreckage_amount=amount_usd,
            asset=asset,
            hops=hops,
            total_cost_bps=total_cost,
            fry_minted=fry_minted,
            efficiency_score=efficiency
        )
    
    def _calculate_fry_minting(self, amount_usd: float, 
                               cost_bps: float, num_hops: int) -> float:
        """
        Calculate FRY minting for a route.
        
        Factors:
        - Base amount
        - Routing efficiency (lower cost = more FRY)
        - Multi-hop bonus (liquidity aggregation)
        - Liquidity provision bonus
        """
        
        # Base FRY
        base_fry = amount_usd * self.rails_fry_rate
        
        # Efficiency bonus (lower cost = higher bonus)
        efficiency_bonus = (1 - cost_bps / MAX_COST_BPS) * 0.3
        
        # Multi-hop bonus
        multi_hop_bonus = (num_hops - 1) * 0.15
        
        # Liquidity provision bonus
        liquidity_bonus = 0.6  # 60% bonus for providing liquidity
        
        # Native stablecoin bonus (50% for using USDH/USDF)
        native_bonus = 0.0
        for hop in self.route.hops:
            if hop['venue'] in DEXES:
                native_bonus += 0.5  # 50% bonus per native stablecoin venue
        
        total_multiplier = 1 + efficiency_bonus + multi_hop_bonus + liquidity_bonus + native_bonus
        fry_minted = base_fry * total_multiplier
        
        return fry_minted
    
    def execute_route(self, route: WreckageRoute) -> Dict:
        """
        Execute wreckage route through liquidity rails.
        
        Returns execution summary with FRY minted.
        """
        
        logger.info(f"{FRY_YELLOW}Executing route:{RESET} {route}")
        
        # Update pool utilizations
        for hop in route.hops:
            venue = hop['venue']
            amount = hop['amount']
            
            # Find pool and update utilization
            for pool in self.liquidity_pools.get(venue, []):
                if pool.asset == route.asset:
                    fill_ratio = amount / pool.depth_usd
                    pool.utilization = min(pool.utilization + fill_ratio, 0.95)
        
        # Mint FRY
        self.total_fry_minted += route.fry_minted
        self.total_wreckage_routed += route.wreckage_amount
        
        execution_summary = {
            'route': route,
            'fry_minted': route.fry_minted,
            'cost_bps': route.total_cost_bps,
            'hops': len(route.hops),
            'efficiency': route.efficiency_score,
            'status': 'executed'
        }
        
        logger.info(f"{FRY_GREEN}✓ Route executed{RESET} | FRY minted: {route.fry_minted:.2f}")
        
        return execution_summary
    
    def allocate_capital(self, total_capital: float) -> Dict[str, float]:
        """
        Allocate capital across venues based on minting surface gradients.
        
        Uses topology routing to find optimal capital distribution.
        """
        
        # Calculate minting potential for each venue
        venue_scores = {}
        
        for venue, pools in self.liquidity_pools.items():
            # Score based on: liquidity depth, low utilization, favorable funding
            total_depth = sum(p.depth_usd for p in pools)
            avg_utilization = np.mean([p.utilization for p in pools])
            avg_funding = np.mean([abs(p.funding_rate) for p in pools])
            
            # Higher score = more capital allocation
            score = total_depth * (1 - avg_utilization) / (1 + avg_funding * 100)
            venue_scores[venue] = score
        
        # Normalize to capital allocation
        total_score = sum(venue_scores.values())
        
        for venue in venue_scores:
            allocation = (venue_scores[venue] / total_score) * total_capital
            self.capital_allocations[venue] = allocation
        
        logger.info(f"{FRY_YELLOW}Capital allocated across {len(self.capital_allocations)} venues{RESET}")
        
        return self.capital_allocations
    
    def get_liquidity_summary(self) -> Dict:
        """Get summary of liquidity rails state"""
        
        total_liquidity = 0
        total_available = 0
        venue_breakdown = {}
        
        for venue, pools in self.liquidity_pools.items():
            venue_liquidity = sum(p.depth_usd for p in pools)
            venue_available = sum(p.available_liquidity() for p in pools)
            
            total_liquidity += venue_liquidity
            total_available += venue_available
            
            venue_breakdown[venue] = {
                'total_liquidity': venue_liquidity,
                'available_liquidity': venue_available,
                'utilization': 1.0 - (venue_available / venue_liquidity) if venue_liquidity > 0 else 0,
                'num_pools': len(pools)
            }
        
        return {
            'total_liquidity': total_liquidity,
            'total_available': total_available,
            'overall_utilization': 1.0 - (total_available / total_liquidity) if total_liquidity > 0 else 0,
            'venues': venue_breakdown,
            'total_wreckage_routed': self.total_wreckage_routed,
            'total_fry_minted': self.total_fry_minted,
            'effective_rate': self.total_fry_minted / self.total_wreckage_routed if self.total_wreckage_routed > 0 else 0
        }


def demo_liquidity_rails():
    """Demonstrate liquidity rails engine"""
    
    print(f"\n{FRY_RED}{BOLD}{'='*70}{RESET}")
    print(f"{FRY_RED}{BOLD}FRY Liquidity Rails Engine - Demo{RESET}")
    print(f"{FRY_RED}{BOLD}{'='*70}{RESET}\n")
    
    # Initialize engine
    rails = LiquidityRailsEngine()
    
    # Get initial liquidity summary
    summary = rails.get_liquidity_summary()
    print(f"{BOLD}Initial Liquidity State:{RESET}")
    print(f"  Total Liquidity: ${summary['total_liquidity']:,.0f}")
    print(f"  Available: ${summary['total_available']:,.0f}")
    print(f"  Utilization: {summary['overall_utilization']:.1%}\n")
    
    # Route some wreckage
    print(f"{BOLD}Routing Wreckage Events:{RESET}")
    print("-" * 70)
    
    wreckage_events = [
        (50_000, "BTC"),
        (125_000, "ETH"),
        (75_000, "BTC"),
        (200_000, "ETH"),
        (100_000, "BTC"),
    ]
    
    total_fry = 0
    
    for amount, asset in wreckage_events:
        print(f"\n{FRY_YELLOW}Wreckage:{RESET} ${amount:,} {asset}")
        
        # Find optimal route
        route = rails.route_wreckage(amount, asset, max_hops=3)
        
        if route:
            # Execute route
            result = rails.execute_route(route)
            total_fry += result['fry_minted']
            
            print(f"  Route: {' → '.join([h['venue'] for h in route.hops])}")
            print(f"  Cost: {route.total_cost_bps:.2f} bps")
            print(f"  FRY Minted: {FRY_GREEN}{route.fry_minted:.2f}{RESET}")
            print(f"  Efficiency: {route.efficiency_score:.2f}")
        else:
            print(f"  {FRY_RED}✗ No route found{RESET}")
    
    # Allocate capital
    print(f"\n{BOLD}Capital Allocation:{RESET}")
    print("-" * 70)
    
    allocations = rails.allocate_capital(total_capital=10_000_000)
    for venue, amount in sorted(allocations.items(), key=lambda x: -x[1]):
        pct = (amount / 10_000_000) * 100
        print(f"  {venue}: ${amount:,.0f} ({pct:.1f}%)")
    
    # Final summary
    final_summary = rails.get_liquidity_summary()
    
    print(f"\n{BOLD}Final Summary:{RESET}")
    print("-" * 70)
    print(f"  Total Wreckage Routed: ${final_summary['total_wreckage_routed']:,.0f}")
    print(f"  Total FRY Minted: {FRY_GREEN}{final_summary['total_fry_minted']:,.2f} FRY{RESET}")
    print(f"  Effective Rate: {final_summary['effective_rate']:.2f} FRY per $1")
    print(f"  Final Utilization: {final_summary['overall_utilization']:.1%}")
    
    improvement = ((final_summary['effective_rate'] - rails.base_fry_rate) / rails.base_fry_rate) * 100
    print(f"  Rate Improvement: {FRY_RED}+{improvement:.1f}%{RESET} vs base rate")
    
    print(f"\n{FRY_RED}{BOLD}{'='*70}{RESET}")
    print(f"{FRY_YELLOW}💡 Liquidity Rails provide optimal routing for wreckage absorption{RESET}")
    print(f"{FRY_YELLOW}   Multi-hop routing + liquidity aggregation = enhanced FRY minting{RESET}")
    print(f"{FRY_RED}{BOLD}{'='*70}{RESET}\n")


if __name__ == "__main__":
    demo_liquidity_rails()
