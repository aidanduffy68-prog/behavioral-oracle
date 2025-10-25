#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Topology-Aware Routing Engine for Agent B
==========================================

Integrates the FRY v3 Network Topology × Minting Surface visualization
with Agent B's federated learning system. Uses number theory and gradient
descent on the minting surface to find optimal cross-DEX routes.

Key Features:
1. Minting surface gradient calculation (dy/dx)
2. Topological path optimization across DEX network
3. Number theory-enhanced route decomposition
4. Federated learning integration for distributed optimization

Based on the FRY v3 topology showing:
- dYdX (16%), Aster (12%), Hyperliquid, GMX (40%)
- Trade routes: efficiency-optimized vs funding-optimized
- 3D minting surface (hedge efficiency × swap notional → dy/dx)
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


def prime_factorize(n: int) -> List[int]:
    """Decompose notional into prime factors for optimal sub-routing"""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def gcd(a: int, b: int) -> int:
    """Euclidean algorithm for GCD - finds optimal notional matching"""
    while b:
        a, b = b, a % b
    return a


class MintingSurface:
    """
    3D minting surface model: f(hedge_efficiency, swap_notional) → dy/dx
    
    The surface represents FRY minting potential across the parameter space.
    Higher dy/dx gradients indicate better minting opportunities.
    """
    
    def __init__(self):
        # Surface parameters calibrated from visualization
        self.base_minting_rate = 1.4  # Base FRY per $1
        self.efficiency_weight = 2.5  # Hedge efficiency impact
        self.notional_weight = 0.8    # Swap notional impact
        self.gradient_threshold = 1.5 # Minimum dy/dx for route selection
        
    def calculate_gradient(self, hedge_efficiency: float, swap_notional: float) -> float:
        """
        Calculate dy/dx gradient at point on minting surface.
        
        Args:
            hedge_efficiency: 0.0 to 1.0 (e.g., 0.40 for GMX's 40%)
            swap_notional: In $10K units (e.g., 0.5 for $5K)
        
        Returns:
            dy/dx gradient value (higher = better minting)
        """
        # Normalize inputs
        eff_norm = hedge_efficiency
        notional_norm = swap_notional / 100  # Scale to reasonable range
        
        # Surface function: exponential decay with efficiency boost
        surface_height = (
            self.base_minting_rate * 
            (1 + self.efficiency_weight * eff_norm) *
            np.exp(-notional_norm * 0.5)
        )
        
        # Gradient (partial derivative approximation)
        dy_dx = (
            self.efficiency_weight * surface_height +
            self.notional_weight * (1 - notional_norm)
        )
        
        return dy_dx
    
    def find_optimal_zone(self, efficiency_range: Tuple[float, float], 
                         notional_range: Tuple[float, float]) -> Dict:
        """
        Find optimal zone on minting surface within given ranges.
        
        Returns point with maximum dy/dx gradient.
        """
        best_gradient = -np.inf
        best_point = None
        
        # Grid search over parameter space
        for eff in np.linspace(efficiency_range[0], efficiency_range[1], 20):
            for notional in np.linspace(notional_range[0], notional_range[1], 20):
                gradient = self.calculate_gradient(eff, notional)
                
                if gradient > best_gradient:
                    best_gradient = gradient
                    best_point = (eff, notional)
        
        return {
            'hedge_efficiency': best_point[0],
            'swap_notional': best_point[1],
            'dy_dx': best_gradient,
            'fry_multiplier': 1.0 + (best_gradient / self.base_minting_rate)
        }


class TopologyRouter:
    """
    Network topology router for cross-DEX swap optimization.
    
    Implements the FRY v3 network topology with:
    - DEX nodes (dYdX, Aster, Hyperliquid, GMX)
    - Trade routes (efficiency-optimized, funding-optimized)
    - Minting surface integration
    """
    
    def __init__(self):
        # DEX network from visualization
        self.dex_network = {
            'dYdX': {
                'efficiency': 0.16,
                'notional_capacity': 50000,  # $50K capacity
                'funding_rate': -0.0015,
                'connections': ['Aster', 'Hyperliquid']
            },
            'Aster': {
                'efficiency': 0.12,
                'notional_capacity': 30000,
                'funding_rate': -0.0012,
                'connections': ['dYdX', 'Hyperliquid']
            },
            'Hyperliquid': {
                'efficiency': 0.25,  # Central hub
                'notional_capacity': 80000,
                'funding_rate': 0.0018,
                'connections': ['dYdX', 'Aster', 'GMX']
            },
            'GMX': {
                'efficiency': 0.40,  # Highest efficiency
                'notional_capacity': 40000,
                'funding_rate': 0.0020,
                'connections': ['Hyperliquid']
            }
        }
        
        self.minting_surface = MintingSurface()
        self.route_cache = {}
        
    def calculate_route_score(self, path: List[str], trade_size: float) -> Dict:
        """
        Score a route through the DEX network using minting surface.
        
        Args:
            path: List of DEX names forming the route
            trade_size: Total trade size in USD
        
        Returns:
            Route score with FRY minting estimate
        """
        total_gradient = 0.0
        total_fry = 0.0
        route_efficiency = 1.0
        
        # Calculate per-hop metrics
        for i, dex_name in enumerate(path):
            dex = self.dex_network[dex_name]
            
            # Allocate trade size proportionally
            hop_size = trade_size / len(path)
            swap_notional = hop_size / 10000  # Convert to $10K units
            
            # Calculate minting gradient at this point
            gradient = self.minting_surface.calculate_gradient(
                dex['efficiency'],
                swap_notional
            )
            
            # Number theory optimization
            nt_bonus = self._calculate_number_theory_bonus(
                int(hop_size),
                dex['notional_capacity']
            )
            
            # FRY minting for this hop
            hop_fry = hop_size * self.minting_surface.base_minting_rate * (1 + gradient) * nt_bonus
            
            total_gradient += gradient
            total_fry += hop_fry
            route_efficiency *= dex['efficiency']
        
        return {
            'path': path,
            'total_gradient': total_gradient,
            'avg_gradient': total_gradient / len(path),
            'total_fry': total_fry,
            'route_efficiency': route_efficiency,
            'fry_per_dollar': total_fry / trade_size
        }
    
    def _calculate_number_theory_bonus(self, trade_size: int, capacity: int) -> float:
        """
        Calculate number theory bonus using GCD and prime factorization.
        
        Higher bonus for trades that align well with DEX capacity.
        """
        # GCD-based alignment
        optimal_size = gcd(trade_size, capacity)
        gcd_bonus = optimal_size / min(trade_size, capacity)
        
        # Prime factorization alignment
        trade_primes = set(prime_factorize(trade_size))
        capacity_primes = set(prime_factorize(capacity))
        prime_overlap = len(trade_primes & capacity_primes) / max(len(trade_primes), 1)
        
        # Combined bonus (10-30% improvement)
        nt_bonus = 1.0 + (0.15 * gcd_bonus + 0.15 * prime_overlap)
        
        return nt_bonus
    
    def find_optimal_route(self, start_dex: str, end_dex: str, 
                          trade_size: float, route_type: str = 'efficiency') -> Dict:
        """
        Find optimal route through DEX network.
        
        Args:
            start_dex: Starting DEX
            end_dex: Ending DEX
            trade_size: Trade size in USD
            route_type: 'efficiency' or 'funding'
        
        Returns:
            Optimal route with minting estimates
        """
        # BFS to find all paths
        all_paths = self._find_all_paths(start_dex, end_dex)
        
        if not all_paths:
            return None
        
        # Score each path
        scored_routes = []
        for path in all_paths:
            score = self.calculate_route_score(path, trade_size)
            scored_routes.append(score)
        
        # Select best route based on type
        if route_type == 'efficiency':
            # Maximize FRY per dollar
            best_route = max(scored_routes, key=lambda x: x['fry_per_dollar'])
        else:  # funding
            # Maximize total gradient (funding opportunity)
            best_route = max(scored_routes, key=lambda x: x['total_gradient'])
        
        return best_route
    
    def _find_all_paths(self, start: str, end: str, 
                       path: List[str] = None, max_hops: int = 4) -> List[List[str]]:
        """Find all paths between two DEXes (BFS with max hops)"""
        if path is None:
            path = []
        
        path = path + [start]
        
        if start == end:
            return [path]
        
        if len(path) >= max_hops:
            return []
        
        if start not in self.dex_network:
            return []
        
        paths = []
        for node in self.dex_network[start]['connections']:
            if node not in path:  # Avoid cycles
                newpaths = self._find_all_paths(node, end, path, max_hops)
                paths.extend(newpaths)
        
        return paths
    
    def get_topology_features(self, route: Dict) -> np.ndarray:
        """
        Extract topology features for federated learning.
        
        Returns feature vector for neural network training.
        """
        if not route:
            return np.zeros(10)
        
        features = [
            route['total_gradient'],
            route['avg_gradient'],
            route['route_efficiency'],
            route['fry_per_dollar'],
            len(route['path']),  # Path length
            np.mean([self.dex_network[dex]['efficiency'] for dex in route['path']]),
            np.std([self.dex_network[dex]['efficiency'] for dex in route['path']]),
            np.mean([abs(self.dex_network[dex]['funding_rate']) for dex in route['path']]),
            route['total_fry'] / 10000,  # Normalized FRY
            1.0 if 'GMX' in route['path'] else 0.0,  # GMX bonus (40% efficiency)
        ]
        
        return np.array(features, dtype=np.float32)


class TopologyAwareAgentB:
    """
    Agent B with topology-aware routing for federated learning.
    
    Integrates minting surface optimization with existing Agent B logic.
    """
    
    def __init__(self):
        self.topology_router = TopologyRouter()
        self.route_history = []
        self.performance_metrics = {
            'total_routes': 0,
            'avg_gradient': 0.0,
            'total_fry_from_topology': 0.0,
        }
    
    def optimize_cross_dex_trade(self, trade_size: float, 
                                 preferred_dexes: List[str] = None) -> Dict:
        """
        Optimize cross-DEX trade using topology and minting surface.
        
        Args:
            trade_size: Trade size in USD
            preferred_dexes: Optional list of preferred DEXes
        
        Returns:
            Optimal route with execution plan
        """
        if preferred_dexes is None:
            preferred_dexes = ['dYdX', 'GMX']  # Default: low to high efficiency
        
        # Find optimal route
        route = self.topology_router.find_optimal_route(
            preferred_dexes[0],
            preferred_dexes[-1],
            trade_size,
            route_type='efficiency'
        )
        
        if route:
            self.route_history.append(route)
            self.performance_metrics['total_routes'] += 1
            self.performance_metrics['total_fry_from_topology'] += route['total_fry']
            self.performance_metrics['avg_gradient'] = np.mean([
                r['avg_gradient'] for r in self.route_history
            ])
            
            logger.info(f"Topology route: {' → '.join(route['path'])} | "
                       f"FRY: {route['total_fry']:.2f} | "
                       f"Gradient: {route['avg_gradient']:.3f}")
        
        return route
    
    def get_topology_training_data(self) -> List[Tuple[np.ndarray, float]]:
        """
        Generate training data for federated learning.
        
        Returns:
            List of (features, label) pairs where label is FRY minting efficiency
        """
        training_data = []
        
        for route in self.route_history:
            features = self.topology_router.get_topology_features(route)
            label = route['fry_per_dollar']  # Target: FRY efficiency
            training_data.append((features, label))
        
        return training_data


if __name__ == "__main__":
    # Demo topology-aware routing
    print("🍟 Topology-Aware Routing Engine for Agent B")
    print("=" * 60)
    
    agent = TopologyAwareAgentB()
    
    # Test route optimization
    trade_size = 25000  # $25K trade
    route = agent.optimize_cross_dex_trade(trade_size, ['dYdX', 'GMX'])
    
    if route:
        print(f"\nOptimal Route: {' → '.join(route['path'])}")
        print(f"Total FRY Minted: {route['total_fry']:.2f}")
        print(f"FRY per Dollar: {route['fry_per_dollar']:.4f}")
        print(f"Average Gradient: {route['avg_gradient']:.3f}")
        print(f"Route Efficiency: {route['route_efficiency']:.2%}")
        
        # Show topology features
        features = agent.topology_router.get_topology_features(route)
        print(f"\nTopology Features (for FL training):")
        print(f"  Feature Vector: {features}")
    
    print("\n" + "=" * 60)
    print("Ready for federated learning integration")
