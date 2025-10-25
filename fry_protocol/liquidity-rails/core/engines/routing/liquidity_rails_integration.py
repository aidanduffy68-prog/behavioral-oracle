#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Liquidity Rails Integration Layer
==================================

Connects the liquidity rails engine with existing FRY infrastructure:
- Agent B (market maker)
- Wreckage matching engine (peer-to-peer swaps)
- Topology routing (minting surface optimization)

Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    Wreckage Sources                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│            LIQUIDITY RAILS ENGINE                           │
│  (Optimal routing, capital allocation, liquidity pooling)  │
└──────┬──────────────────────────────────────┬───────────────┘
       │                                      │
       ▼                                      ▼
┌──────────────────┐              ┌──────────────────────────┐
│  Agent B         │              │  Wreckage Matching       │
│  (Market Maker)  │◄────────────►│  (P2P Swaps)            │
│  - Slippage      │              │  - Funding swaps         │
│  - Hedging       │              │  - Cross-DEX netting     │
│  - Arbitrage     │              │                          │
└──────────────────┘              └──────────────────────────┘
       │                                      │
       └──────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Topology Routing Engine                        │
│  (Minting surface gradients, number theory bonuses)        │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  FRY Minting Layer                          │
└─────────────────────────────────────────────────────────────┘
"""

from liquidity_rails_engine import LiquidityRailsEngine, WreckageRoute
from fry_wreckage_matching_engine import FRYWreckageMatchingEngine, WreckageEvent
from topology_routing_engine import TopologyAwareAgentB
from typing import Dict, List, Optional
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FRY_RED = "\033[91m"
FRY_YELLOW = "\033[93m"
FRY_GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"


class IntegratedLiquiditySystem:
    """
    Unified system integrating liquidity rails with existing infrastructure.
    
    Flow:
    1. Wreckage arrives → Liquidity Rails route it
    2. Try P2P matching first (wreckage matching engine)
    3. Unmatched wreckage → Agent B market makes
    4. All routing optimized via topology engine
    """
    
    def __init__(self, initial_capital: float = 1_000_000):
        # Initialize all components
        self.liquidity_rails = LiquidityRailsEngine()
        self.wreckage_matcher = FRYWreckageMatchingEngine()
        self.topology_router = TopologyAwareAgentB()
        
        # Mock Agent B for integration (avoid complex dependencies)
        self.agent_b = self._create_mock_agent_b(initial_capital)
        
        self.total_wreckage_processed = 0.0
        self.total_fry_minted = 0.0
        
        logger.info(f"{FRY_RED}{BOLD}🔗 Integrated Liquidity System Initialized{RESET}")
        logger.info(f"Components: Liquidity Rails + Agent B + Wreckage Matcher + Topology Router")
    
    def _create_mock_agent_b(self, initial_capital):
        """Create mock Agent B for integration testing"""
        class MockAgentB:
            def __init__(self, capital):
                self.capital = capital
                self.total_fry_minted = 0
            
            def analyze_market_opportunity(self, market_data, funding_rates):
                return {
                    'slippage_harvest': {
                        'fry_minted': np.random.uniform(10, 50),
                        'profit_usd': np.random.uniform(100, 500)
                    }
                }
            
            def get_agent_b_metrics(self):
                return {
                    'total_fry_minted': self.total_fry_minted,
                    'total_trades': 0
                }
        
        return MockAgentB(initial_capital)
    
    def process_wreckage(self, wreckage_event: WreckageEvent) -> Dict:
        """
        Process wreckage through the integrated system.
        
        Strategy:
        1. Check for P2P match (cheapest, highest FRY)
        2. If no match, route via liquidity rails
        3. Agent B market makes the final fill
        4. Topology optimization throughout
        """
        
        logger.info(f"\n{FRY_YELLOW}Processing wreckage:{RESET} {wreckage_event}")
        
        result = {
            'wreckage': wreckage_event,
            'strategy': None,
            'fry_minted': 0.0,
            'cost_bps': 0.0,
            'route': None
        }
        
        # Step 1: Try P2P matching first (best rate)
        self.wreckage_matcher.collect_wreckage(wreckage_event)
        matches = self.wreckage_matcher.match_wreckage()
        
        if matches > 0 and wreckage_event.matched:
            # P2P match found! Highest FRY rate
            result['strategy'] = 'p2p_swap'
            result['fry_minted'] = wreckage_event.amount_usd * self.wreckage_matcher.swap_fry_rate
            result['cost_bps'] = 0  # No cost for P2P
            
            logger.info(f"{FRY_GREEN}✓ P2P match found{RESET} | FRY: {result['fry_minted']:.2f}")
            
        else:
            # Step 2: No P2P match, route via liquidity rails
            route = self.liquidity_rails.route_wreckage(
                wreckage_event.amount_usd,
                wreckage_event.asset,
                max_hops=3
            )
            
            if route:
                # Step 3: Agent B market makes the fill
                agent_b_result = self._agent_b_fill(wreckage_event, route)
                
                result['strategy'] = 'liquidity_rails'
                result['fry_minted'] = route.fry_minted + agent_b_result['fry_bonus']
                result['cost_bps'] = route.total_cost_bps
                result['route'] = route
                
                # Execute route
                self.liquidity_rails.execute_route(route)
                
                logger.info(f"{FRY_GREEN}✓ Routed via liquidity rails{RESET} | FRY: {result['fry_minted']:.2f}")
            
            else:
                # Step 4: Fallback - Agent B direct market making
                agent_b_result = self._agent_b_direct_fill(wreckage_event)
                
                result['strategy'] = 'agent_b_direct'
                result['fry_minted'] = agent_b_result['fry_minted']
                result['cost_bps'] = agent_b_result['cost_bps']
                
                logger.info(f"{FRY_YELLOW}⚠ Agent B direct fill{RESET} | FRY: {result['fry_minted']:.2f}")
        
        # Update totals
        self.total_wreckage_processed += wreckage_event.amount_usd
        self.total_fry_minted += result['fry_minted']
        
        return result
    
    def _agent_b_fill(self, wreckage: WreckageEvent, route: WreckageRoute) -> Dict:
        """
        Agent B market makes the routed wreckage.
        
        Agent B provides:
        - Slippage harvesting bonus
        - Adaptive hedging
        - Funding arbitrage
        """
        
        # Create market data for Agent B
        market_data = {
            'asset': wreckage.asset,
            'price': 50000 if wreckage.asset == 'BTC' else 3000,  # Placeholder
            'volume': wreckage.amount_usd,
            'volatility': 0.02,
            'bid_ask_spread': route.total_cost_bps / 10000,
            'order_book_depth': route.hops[0]['liquidity_depth'] if route.hops else 1_000_000,
            'social_sentiment': 0.5,
            'liquidity_depth': route.hops[0]['liquidity_depth'] if route.hops else 1_000_000,
        }
        
        funding_rates = {
            hop['venue']: 0.0001 for hop in route.hops
        }
        
        # Agent B analyzes opportunity
        opportunities = self.agent_b.analyze_market_opportunity(market_data, funding_rates)
        
        # Slippage harvesting bonus
        fry_bonus = 0.0
        if opportunities.get('slippage_harvest'):
            fry_bonus = opportunities['slippage_harvest'].get('fry_minted', 0)
        
        return {
            'fry_bonus': fry_bonus,
            'opportunities': opportunities
        }
    
    def _agent_b_direct_fill(self, wreckage: WreckageEvent) -> Dict:
        """
        Agent B directly market makes wreckage (no routing).
        
        Used as fallback when no liquidity rails route available.
        """
        
        market_data = {
            'asset': wreckage.asset,
            'price': 50000 if wreckage.asset == 'BTC' else 3000,
            'volume': wreckage.amount_usd,
            'volatility': 0.03,  # Higher vol for direct fill
            'bid_ask_spread': 0.005,
            'order_book_depth': 500_000,
            'social_sentiment': 0.5,
            'liquidity_depth': 500_000,
        }
        
        funding_rates = {'default': 0.0001}
        
        opportunities = self.agent_b.analyze_market_opportunity(market_data, funding_rates)
        
        # Base FRY minting (lower rate for direct fill)
        base_fry = wreckage.amount_usd * 0.8  # 0.8 FRY per $1
        
        # Add Agent B bonuses
        if opportunities.get('slippage_harvest'):
            base_fry += opportunities['slippage_harvest'].get('fry_minted', 0)
        
        return {
            'fry_minted': base_fry,
            'cost_bps': 30,  # Higher cost for direct fill
            'opportunities': opportunities
        }
    
    def optimize_capital_allocation(self, total_capital: float) -> Dict:
        """
        Optimize capital allocation across venues using topology + liquidity rails.
        
        Combines:
        - Liquidity rails capital allocation
        - Topology minting surface gradients
        - Agent B positioning
        """
        
        # Get liquidity rails allocation
        rails_allocation = self.liquidity_rails.allocate_capital(total_capital * 0.7)
        
        # Reserve capital for Agent B market making
        agent_b_capital = total_capital * 0.3
        
        # Optimize via topology (only for venues in topology network)
        topology_routes = []
        topology_venues = ['dYdX', 'Hyperliquid', 'Aster', 'GMX']
        for venue in rails_allocation.keys():
            if venue in topology_venues:
                route = self.topology_router.optimize_cross_dex_trade(
                    trade_size=rails_allocation[venue],
                    preferred_dexes=[venue]
                )
                if route:
                    topology_routes.append(route)
        
        return {
            'rails_allocation': rails_allocation,
            'agent_b_capital': agent_b_capital,
            'topology_routes': topology_routes,
            'total_capital': total_capital
        }
    
    def get_system_summary(self) -> Dict:
        """Get comprehensive system summary"""
        
        liquidity_summary = self.liquidity_rails.get_liquidity_summary()
        agent_b_metrics = self.agent_b.get_agent_b_metrics()
        
        return {
            'total_wreckage_processed': self.total_wreckage_processed,
            'total_fry_minted': self.total_fry_minted,
            'effective_rate': self.total_fry_minted / self.total_wreckage_processed if self.total_wreckage_processed > 0 else 0,
            'liquidity_rails': liquidity_summary,
            'agent_b': agent_b_metrics,
            'wreckage_matcher': {
                'total_events': len(self.wreckage_matcher.wreckage_pool),
                'matched_pairs': len(self.wreckage_matcher.matched_pairs),
                'total_fry': self.wreckage_matcher.total_fry_minted
            }
        }


def demo_integrated_system():
    """Demonstrate integrated liquidity system"""
    
    print(f"\n{FRY_RED}{BOLD}{'='*70}{RESET}")
    print(f"{FRY_RED}{BOLD}Integrated Liquidity System - Demo{RESET}")
    print(f"{FRY_RED}{BOLD}{'='*70}{RESET}\n")
    
    # Initialize system
    system = IntegratedLiquiditySystem(initial_capital=5_000_000)
    
    print(f"{BOLD}System Components:{RESET}")
    print(f"  ✓ Liquidity Rails Engine")
    print(f"  ✓ Agent B (Market Maker)")
    print(f"  ✓ Wreckage Matching Engine")
    print(f"  ✓ Topology Router\n")
    
    # Process wreckage events
    print(f"{BOLD}Processing Wreckage Events:{RESET}")
    print("-" * 70)
    
    wreckage_events = [
        WreckageEvent("dYdX", "long_liq", "BTC", 75_000, 0),
        WreckageEvent("Hyperliquid", "short_liq", "BTC", 80_000, 0),
        WreckageEvent("Aster", "slippage", "ETH", 120_000, 0),
        WreckageEvent("GMX", "adverse_fill", "BTC", 50_000, 0),
        WreckageEvent("Vertex", "funding_loss", "ETH", 90_000, 0),
    ]
    
    for event in wreckage_events:
        result = system.process_wreckage(event)
        print(f"  Strategy: {result['strategy']}")
        print(f"  FRY Minted: {FRY_GREEN}{result['fry_minted']:.2f}{RESET}")
        if result['route']:
            print(f"  Route: {' → '.join([h['venue'] for h in result['route'].hops])}")
        print()
    
    # Optimize capital allocation
    print(f"{BOLD}Capital Allocation:{RESET}")
    print("-" * 70)
    
    allocation = system.optimize_capital_allocation(total_capital=5_000_000)
    print(f"  Liquidity Rails: ${sum(allocation['rails_allocation'].values()):,.0f}")
    print(f"  Agent B Reserve: ${allocation['agent_b_capital']:,.0f}")
    
    for venue, amount in sorted(allocation['rails_allocation'].items(), key=lambda x: -x[1]):
        pct = (amount / 5_000_000) * 100
        print(f"    {venue}: ${amount:,.0f} ({pct:.1f}%)")
    
    # System summary
    print(f"\n{BOLD}System Summary:{RESET}")
    print("-" * 70)
    
    summary = system.get_system_summary()
    print(f"  Total Wreckage: ${summary['total_wreckage_processed']:,.0f}")
    print(f"  Total FRY Minted: {FRY_GREEN}{summary['total_fry_minted']:,.2f} FRY{RESET}")
    print(f"  Effective Rate: {summary['effective_rate']:.2f} FRY per $1")
    print(f"  P2P Matches: {summary['wreckage_matcher']['matched_pairs']}")
    
    print(f"\n{FRY_RED}{BOLD}{'='*70}{RESET}")
    print(f"{FRY_YELLOW}💡 Integrated system combines:{RESET}")
    print(f"{FRY_YELLOW}   • P2P matching (highest FRY rate){RESET}")
    print(f"{FRY_YELLOW}   • Liquidity rails (optimal routing){RESET}")
    print(f"{FRY_YELLOW}   • Agent B (market making + bonuses){RESET}")
    print(f"{FRY_YELLOW}   • Topology optimization (minting surface){RESET}")
    print(f"{FRY_RED}{BOLD}{'='*70}{RESET}\n")


if __name__ == "__main__":
    demo_integrated_system()
