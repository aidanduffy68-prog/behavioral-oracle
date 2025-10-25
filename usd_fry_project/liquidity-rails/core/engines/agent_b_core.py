#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agent B: The Embedded FRY Market Maker
=====================================

Agent B is the FRY-native market maker that sits at the table and directly
arbitrages toxic flows using FRY mechanics. The "Phil Ivey" of FRY.

Core Functions:
1. Slippage Harvesting - Converts adverse retail trades into FRY mint events
2. Adaptive Hedging - Uses LPI + circuit breaker logic for aggressiveness
3. Funding Arbitrage Execution - Cross-venue capital allocation with FRY
4. Rekt Master Safety Net - Whale protection and loss recycling
"""

import time
import random
import logging
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, deque
import time
import json
from v2_circuit_breaker import CircuitBreakerSystem
from v2_slippage_engine import SlippageEstimate
from ml_adaptive_hedging import MLAdaptiveHedgingEngine

logger = logging.getLogger(__name__)

class SlippageHarvester:
    """
    Slippage Harvesting Engine - Converts adverse retail trades into FRY mint events
    """
    
    def __init__(self, config=None):
        self.config = config or {
            'min_slippage_threshold': 0.002,  # 0.2% minimum
            'fry_conversion_rate': 1.0,       # 1 FRY per $1 slippage
            'volatility_multiplier': 1.5,    # Volatility bonus
            'retail_detection_threshold': 0.7, # Social sentiment threshold
            'harvest_efficiency': 0.85        # 85% harvest efficiency
        }
        
        self.harvested_slippage = 0.0
        self.fry_minted = 0.0
        self.harvest_events = []
        
    def detect_retail_flow(self, market_data):
        """Detect retail trading activity patterns"""
        
        volume = market_data.get('volume', 0)
        social_sentiment = market_data.get('social_sentiment', 0.5)
        order_size_distribution = market_data.get('order_size_dist', 'normal')
        price_volatility = market_data.get('volatility', 0.05)
        
        # Retail indicators
        high_social_activity = social_sentiment > self.config['retail_detection_threshold']
        small_order_dominance = order_size_distribution == 'retail_heavy'
        momentum_trading = price_volatility > 0.04 and volume > 1000000
        
        retail_score = sum([high_social_activity, small_order_dominance, momentum_trading]) / 3
        
        return {
            'is_retail_flow': retail_score > 0.6,
            'retail_intensity': retail_score,
            'social_sentiment': social_sentiment,
            'volume_profile': volume,
            'volatility_level': price_volatility
        }
    
    def calculate_harvestable_slippage(self, asset, trade_size, market_data, retail_flow):
        """Calculate slippage that can be harvested and converted to FRY"""
        
        # Base slippage calculation
        volatility = market_data.get('volatility', 0.05)
        liquidity_depth = market_data.get('liquidity_depth', 1000000)
        
        # Slippage estimation
        base_slippage = (trade_size / liquidity_depth) * volatility
        
        # Retail flow amplification
        if retail_flow['is_retail_flow']:
            retail_amplifier = 1 + (retail_flow['retail_intensity'] * 0.5)
            base_slippage *= retail_amplifier
        
        # Volatility bonus
        if volatility > 0.04:
            volatility_bonus = (volatility - 0.04) * self.config['volatility_multiplier']
            base_slippage += volatility_bonus
        
        return max(0, base_slippage)
    
    def harvest_slippage(self, asset, trade_size, market_data, timestamp):
        """Execute slippage harvesting and FRY minting"""
        
        # Detect retail flow
        retail_flow = self.detect_retail_flow(market_data)
        
        # Calculate harvestable slippage
        slippage_amount = self.calculate_harvestable_slippage(
            asset, trade_size, market_data, retail_flow
        )
        
        if slippage_amount < self.config['min_slippage_threshold']:
            return None
        
        # Convert slippage to FRY tokens
        slippage_value_usd = slippage_amount * trade_size
        fry_minted = slippage_value_usd * self.config['fry_conversion_rate'] * self.config['harvest_efficiency']
        
        # Apply retail flow bonus
        if retail_flow['is_retail_flow']:
            fry_minted *= (1 + retail_flow['retail_intensity'] * 0.3)
        
        # Record harvest event
        harvest_event = {
            'timestamp': timestamp,
            'asset': asset,
            'trade_size': trade_size,
            'slippage_pct': slippage_amount,
            'slippage_value_usd': slippage_value_usd,
            'fry_minted': fry_minted,
            'retail_flow': retail_flow,
            'market_conditions': {
                'volatility': market_data.get('volatility', 0),
                'volume': market_data.get('volume', 0),
                'liquidity_depth': market_data.get('liquidity_depth', 0)
            }
        }
        
        self.harvest_events.append(harvest_event)
        self.harvested_slippage += slippage_value_usd
        self.fry_minted += fry_minted
        
        logger.info("Harvested ${:.2f} slippage -> {:.4f} FRY from {}".format(slippage_value_usd, fry_minted, asset))
        
        return harvest_event

class AdaptiveHedgingEngine:
    """
    Adaptive Hedging System using LPI + Circuit Breaker Logic
    """
    
    def __init__(self, circuit_breaker_system):
        self.circuit_breaker = circuit_breaker_system
        self.positions = {}
        self.hedging_history = deque(maxlen=1000)
        
        self.config = {
            'base_hedge_ratio': 0.7,      # 70% base hedge
            'max_hedge_ratio': 0.95,      # 95% max hedge
            'min_hedge_ratio': 0.3,       # 30% min hedge
            'lpi_sensitivity': 0.5,       # LPI adjustment sensitivity
            'circuit_breaker_hedge': 0.9  # 90% hedge when CB active
        }
        
    def calculate_lpi_score(self, market_data):
        """Calculate Liquidity Pressure Index (LPI) score"""
        
        volume = market_data.get('volume', 0)
        volatility = market_data.get('volatility', 0.05)
        spread = market_data.get('bid_ask_spread', 0.001)
        order_book_depth = market_data.get('order_book_depth', 1000000)
        
        # LPI components
        volume_pressure = min(1.0, volume / 5000000)  # Normalize to 5M volume
        volatility_pressure = min(1.0, volatility / 0.1)  # Normalize to 10% vol
        spread_pressure = min(1.0, spread / 0.01)  # Normalize to 1% spread
        depth_pressure = max(0, 1 - (order_book_depth / 1000000))  # Inverse depth
        
        # Weighted LPI score
        lpi_score = (
            volume_pressure * 0.3 +
            volatility_pressure * 0.3 +
            spread_pressure * 0.2 +
            depth_pressure * 0.2
        )
        
        return min(1.0, lpi_score)
    
    def determine_hedge_ratio(self, asset, market_data, position_size):
        """Determine optimal hedge ratio based on conditions"""
        
        # Calculate LPI
        lpi_score = self.calculate_lpi_score(market_data)
        
        # Base hedge ratio
        base_ratio = self.config['base_hedge_ratio']
        
        # LPI adjustment
        lpi_adjustment = (lpi_score - 0.5) * self.config['lpi_sensitivity']
        adjusted_ratio = base_ratio + lpi_adjustment
        
        # Circuit breaker override
        if self.circuit_breaker.active:
            adjusted_ratio = self.config['circuit_breaker_hedge']
            logger.warning("Circuit breaker active - using emergency hedge ratio: {:.2f}".format(adjusted_ratio))
        
        # Position size adjustment (larger positions need more hedging)
        size_factor = min(0.2, position_size / 1000000)  # Up to 20% increase for $1M position
        adjusted_ratio += size_factor
        
        # Apply bounds
        final_ratio = max(
            self.config['min_hedge_ratio'],
            min(self.config['max_hedge_ratio'], adjusted_ratio)
        )
        
        return final_ratio, lpi_score
    
    def execute_adaptive_hedge(self, asset, position_size, market_data, timestamp):
        """Execute adaptive hedging based on current conditions"""
        
        hedge_ratio, lpi_score = self.determine_hedge_ratio(asset, market_data, position_size)
        hedge_size = position_size * hedge_ratio
        
        # Record hedging decision
        hedge_record = {
            'timestamp': timestamp,
            'asset': asset,
            'position_size': position_size,
            'hedge_ratio': hedge_ratio,
            'hedge_size': hedge_size,
            'lpi_score': lpi_score,
            'circuit_breaker_active': self.circuit_breaker.active,
            'market_conditions': market_data
        }
        
        self.hedging_history.append(hedge_record)
        
        # Update position tracking
        if asset not in self.positions:
            self.positions[asset] = {'long': 0, 'short': 0, 'hedge': 0}
        
        self.positions[asset]['hedge'] = hedge_size
        
        logger.info("Adaptive hedge for {}: {:.1%} ratio, ${:,.0f} hedge".format(asset, hedge_ratio, hedge_size))
        
        return hedge_record

class FundingArbitrageEngine:
    """
    Funding Arbitrage Execution Engine with FRY Enhancements
    """
    
    def __init__(self, slippage_engine):
        self.slippage_engine = slippage_engine
        self.active_positions = {}
        self.arbitrage_history = []
        
        self.config = {
            'min_spread_threshold': 0.001,    # 0.1% minimum spread
            'max_position_size': 1000000,     # $1M max position
            'fry_enhancement_factor': 1.3,    # 30% FRY enhancement
            'venue_preference': {              # Venue scoring
                'binance': 1.0,
                'okx': 0.9,
                'bybit': 0.85,
                'kucoin': 0.8
            }
        }
    
    def analyze_funding_opportunity(self, asset, funding_rates, market_data):
        """Analyze cross-venue funding arbitrage opportunity"""
        
        if len(funding_rates) < 2:
            return None
        
        # Find best spread
        sorted_rates = sorted(funding_rates.items(), key=lambda x: x[1])
        long_venue, long_rate = sorted_rates[0]   # Lowest rate (go long here)
        short_venue, short_rate = sorted_rates[-1] # Highest rate (go short here)
        
        spread = short_rate - long_rate
        
        if spread < self.config['min_spread_threshold']:
            return None
        
        # Calculate optimal position size
        market_cap = market_data.get('market_cap_usd', 10000000)
        liquidity_factor = min(1.0, market_cap / 100000000)  # Scale by market cap
        base_position = max(1000, self.config['max_position_size'] * liquidity_factor)  # Minimum $1k position
        
        # Slippage analysis
        slippage_estimate = self.slippage_engine.estimate_slippage(
            asset, base_position, market_cap
        )
        
        # FRY enhancement calculation
        slippage_cost = (slippage_estimate.total_cost_pct / 100) * base_position
        fry_value = slippage_cost * self.config['fry_enhancement_factor']
        
        # Net profit calculation
        gross_profit = spread * base_position
        trading_costs = base_position * 0.002  # 0.1% each side
        net_traditional_profit = gross_profit - slippage_cost - trading_costs
        total_fry_value = net_traditional_profit + fry_value
        
        return {
            'asset': asset,
            'long_venue': long_venue,
            'short_venue': short_venue,
            'funding_spread': spread,
            'position_size': base_position,
            'gross_profit': gross_profit,
            'slippage_cost': slippage_cost,
            'fry_enhancement': fry_value,
            'net_traditional_profit': net_traditional_profit,
            'total_fry_value': total_fry_value,
            'roi_pct': (total_fry_value / base_position) * 100,
            'slippage_estimate': slippage_estimate
        }
    
    def execute_funding_arbitrage(self, opportunity, timestamp):
        """Execute funding arbitrage with FRY enhancements"""
        
        if not opportunity:
            return None
        
        asset = opportunity['asset']
        position_id = "{}_{}".format(asset, int(timestamp))
        
        # Execute the arbitrage
        execution_record = {
            'position_id': position_id,
            'timestamp': timestamp,
            'asset': asset,
            'strategy': 'fry_funding_arbitrage',
            'long_venue': opportunity['long_venue'],
            'short_venue': opportunity['short_venue'],
            'position_size': opportunity['position_size'],
            'funding_spread': opportunity['funding_spread'],
            'expected_profit': opportunity['total_fry_value'],
            'fry_enhancement': opportunity['fry_enhancement'],
            'status': 'active'
        }
        
        self.active_positions[position_id] = execution_record
        self.arbitrage_history.append(execution_record)
        
        logger.info("Executed FRY funding arbitrage: {} ${:,.0f} spread={:.4f} expected=${:,.2f}".format(
            asset, opportunity['position_size'], opportunity['funding_spread'], opportunity['total_fry_value']))
        
        return execution_record

class RektMasterSafetyNet:
    """
    Rekt Master Safety Net - Whale protection and loss recycling system
    """
    
    def __init__(self):
        self.protected_positions = {}
        self.recycled_losses = 0.0
        self.safety_events = []
        
        self.config = {
            'whale_threshold': 100000,        # $100k+ positions
            'max_protection_ratio': 0.8,     # Protect up to 80% of loss
            'time_extension_hours': 24,      # 24 hour extension
            'recycling_efficiency': 0.6,     # 60% loss recycling
            'system_stability_fee': 0.02     # 2% fee for protection
        }
    
    def identify_whale_position(self, position_data):
        """Identify positions that qualify for whale protection"""
        
        position_size = position_data.get('size_usd', 0)
        unrealized_pnl = position_data.get('unrealized_pnl', 0)
        time_to_liquidation = position_data.get('time_to_liquidation_hours', 0)
        
        is_whale = position_size >= self.config['whale_threshold']
        is_at_risk = unrealized_pnl < -position_size * 0.5  # 50%+ loss
        needs_time = time_to_liquidation < 2  # Less than 2 hours
        
        return is_whale and is_at_risk and needs_time
    
    def calculate_protection_parameters(self, position_data):
        """Calculate protection parameters for whale position"""
        
        position_size = position_data['size_usd']
        unrealized_loss = abs(position_data['unrealized_pnl'])
        
        # Protection amount (capped)
        max_protection = unrealized_loss * self.config['max_protection_ratio']
        
        # System stability fee
        stability_fee = max_protection * self.config['system_stability_fee']
        net_protection = max_protection - stability_fee
        
        # Time extension
        time_extension = self.config['time_extension_hours']
        
        return {
            'protection_amount': net_protection,
            'stability_fee': stability_fee,
            'time_extension_hours': time_extension,
            'recycling_value': unrealized_loss * self.config['recycling_efficiency']
        }
    
    def activate_safety_net(self, position_data, timestamp):
        """Activate safety net for whale position"""
        
        if not self.identify_whale_position(position_data):
            return None
        
        protection_params = self.calculate_protection_parameters(position_data)
        position_id = position_data.get('position_id', "pos_{}".format(int(timestamp)))
        
        # Create safety net record
        safety_record = {
            'position_id': position_id,
            'timestamp': timestamp,
            'trader_id': position_data.get('trader_id', 'unknown'),
            'asset': position_data.get('asset', 'unknown'),
            'original_size': position_data['size_usd'],
            'unrealized_loss': abs(position_data['unrealized_pnl']),
            'protection_amount': protection_params['protection_amount'],
            'stability_fee': protection_params['stability_fee'],
            'time_extension_hours': protection_params['time_extension_hours'],
            'recycling_value': protection_params['recycling_value'],
            'status': 'active'
        }
        
        self.protected_positions[position_id] = safety_record
        self.safety_events.append(safety_record)
        self.recycled_losses += protection_params['recycling_value']
        
        logger.info("Safety net activated for {}: ${:,.2f} protection, {}h extension".format(
            position_id, protection_params['protection_amount'], protection_params['time_extension_hours']))
        
        return safety_record

class AgentB:
    """
    Agent B: The Embedded FRY Market Maker
    
    The "Phil Ivey" of FRY - sits at the table and clips edges without being the house.
    """
    
    def __init__(self, initial_capital=1000000):
        """Initialize Agent B with core components"""
        
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {}
        self.fry_balance = 0.0
        self.total_fry_minted = 0.0
        
        # Circuit breaker integration (needed first)
        self.circuit_breaker = CircuitBreakerSystem()
        
        # Initialize core components
        self.slippage_harvester = SlippageHarvester()
        self.adaptive_hedging = AdaptiveHedgingEngine(self.circuit_breaker)
        self.funding_arbitrage = FundingArbitrageEngine()
        self.safety_net = RektMasterSafetyNet()
        
        # ML-Enhanced Adaptive Hedging
        self.ml_hedging_engine = MLAdaptiveHedgingEngine()
        
        # Performance tracking
        self.performance_metrics = {
            'total_trades': 0,
            'total_profits': 0.0,
            'slippage_harvested': 0.0,
            'fry_value_usd': 0.0,
            'losses_recycled': 0.0,
            'protected_whale_positions': 0,
            'active_positions': 0,
            'active_arbitrage_positions': 0,
            'circuit_breaker_active': False,
            'total_return_pct': 0.0
        }
    
    def analyze_market_opportunity(self, market_data, funding_rates=None):
        """Analyze market for Agent B opportunities across all functions"""
        
        asset = market_data.get('asset', 'UNKNOWN')
        timestamp = time.time()
        
        opportunities = {
            'timestamp': timestamp,
            'asset': asset,
            'slippage_harvest': None,
            'funding_arbitrage': None,
            'hedge_adjustment': None,
            'safety_net_trigger': None
        }
        
        # 1. Slippage Harvesting Analysis
        if market_data.get('volume', 0) > 500000:  # Minimum volume threshold
            trade_size = market_data.get('estimated_trade_size', 50000)
            harvest_event = self.slippage_harvester.harvest_slippage(
                asset, trade_size, market_data, timestamp
            )
            if harvest_event:
                opportunities['slippage_harvest'] = harvest_event
                self.total_fry_minted += harvest_event['fry_minted']
        
        # 2. Funding Arbitrage Analysis
        if funding_rates and len(funding_rates) >= 2:
            arb_opportunity = self.funding_arbitrage.analyze_funding_opportunity(
                asset, funding_rates, market_data
            )
            if arb_opportunity and arb_opportunity['roi_pct'] > 1.0:  # 1%+ ROI threshold
                opportunities['funding_arbitrage'] = arb_opportunity
        
        # 3. Adaptive Hedging
        current_position = self.positions.get(asset, {}).get('size', 0)
        if abs(current_position) > 10000:  # $10k+ position
            lpi_score = self.adaptive_hedging.calculate_lpi_score(market_data)
            ml_hedge_ratio, ml_decision = self.ml_hedging_engine.calculate_enhanced_hedge_ratio(
                asset, market_data, abs(current_position), lpi_score, 
                self.circuit_breaker.active, timestamp
            )
            
            # Execute hedge with ML-enhanced ratio
            hedge_record = self.adaptive_hedging.execute_adaptive_hedge(
                asset, abs(current_position), market_data, timestamp
            )
            hedge_record['ml_enhanced_ratio'] = ml_hedge_ratio
            hedge_record['ml_decision'] = ml_decision
            
            opportunities['hedge_adjustment'] = hedge_record
        
        # 4. Safety Net Monitoring
        position_data = market_data.get('position_data')
        if position_data:
            safety_activation = self.safety_net.activate_safety_net(position_data, timestamp)
            if safety_activation:
                opportunities['safety_net_trigger'] = safety_activation
        
        return opportunities
    
    def execute_agent_b_strategy(self, opportunities):
        """Execute Agent B strategy based on identified opportunities"""
        
        executed_actions = []
        
        # Execute funding arbitrage
        if opportunities['funding_arbitrage']:
            arb_execution = self.funding_arbitrage.execute_funding_arbitrage(
                opportunities['funding_arbitrage'], opportunities['timestamp']
            )
            if arb_execution:
                executed_actions.append(('funding_arbitrage', arb_execution))
                self.total_profits += opportunities['funding_arbitrage']['total_fry_value']
                self.total_trades += 1
        
        # Record slippage harvest
        if opportunities['slippage_harvest']:
            executed_actions.append(('slippage_harvest', opportunities['slippage_harvest']))
        
        # Record hedge adjustment
        if opportunities['hedge_adjustment']:
            executed_actions.append(('hedge_adjustment', opportunities['hedge_adjustment']))
        
        # Record safety net activation
        if opportunities['safety_net_trigger']:
            executed_actions.append(('safety_net', opportunities['safety_net_trigger']))
        
        return executed_actions
    
    def get_agent_b_metrics(self):
        """Get comprehensive Agent B performance metrics"""
        
        total_capital = self.current_capital + sum(
            pos.get('value', 0) for pos in self.positions.values()
        )
        
        return {
            'agent_type': 'Agent_B_Embedded_FRY_MM',
            'total_capital': total_capital,
            'total_return_pct': ((total_capital - self.initial_capital) / self.initial_capital) * 100,
            'total_profits': self.total_profits,
            'total_fry_minted': self.total_fry_minted,
            'fry_value_usd': self.total_fry_minted * 0.10,  # Assuming $0.10 per FRY
            'total_trades': self.total_trades,
            'slippage_harvested': self.slippage_harvester.harvested_slippage,
            'losses_recycled': self.safety_net.recycled_losses,
            'active_positions': len(self.positions),
            'active_arbitrage_positions': len(self.funding_arbitrage.active_positions),
            'protected_whale_positions': len(self.safety_net.protected_positions),
            'circuit_breaker_active': self.circuit_breaker.active,
            'performance_components': {
                'traditional_profits': self.total_profits - (self.total_fry_minted * 0.10),
                'fry_enhancement_value': self.total_fry_minted * 0.10,
                'slippage_conversion_efficiency': self.slippage_harvester.config['harvest_efficiency'],
                'safety_net_protection_provided': sum(
                    pos['protection_amount'] for pos in self.safety_net.protected_positions.values()
                )
            }
        }

def simulate_agent_b_vs_traditional_mm(duration_minutes=180):
    """Simulate Agent B vs Traditional Market Maker comparison"""
    
    print("🤖 Agent B vs Traditional MM Simulation")
    print("=" * 60)
    print("Agent B: The Embedded FRY Market Maker")
    print("Traditional MM: Standard Market Making Strategy")
    print("Duration: {} minutes\n".format(duration_minutes))
    
    # Initialize agents
    agent_b = AgentB(1000000)  # $1M starting capital
    
    # Simulation data
    assets = ['BTC', 'ETH', 'SOL', 'AVAX', 'MATIC']
    asset_prices = {'BTC': 45000, 'ETH': 2800, 'SOL': 100, 'AVAX': 25, 'MATIC': 0.8}
    
    for minute in range(duration_minutes):
        timestamp = time.time()
        
        # Simulate each asset
        for asset in assets:
            # Generate market data
            market_data = {
                'asset': asset,
                'price': asset_prices[asset] * (1 + np.random.normal(0, 0.02)),
                'volume': random.uniform(1000000, 5000000),
                'volatility': random.uniform(0.03, 0.08),
                'social_sentiment': random.uniform(0.3, 0.9),
                'liquidity_depth': random.uniform(500000, 2000000),
                'bid_ask_spread': random.uniform(0.001, 0.005),
                'order_book_depth': random.uniform(800000, 1500000),
                'estimated_trade_size': random.uniform(10000, 100000)
            }
            
            # Generate funding rates
            funding_rates = {
                'binance': random.uniform(-0.005, 0.015),
                'okx': random.uniform(-0.007, 0.012),
                'bybit': random.uniform(-0.006, 0.014),
                'kucoin': random.uniform(-0.008, 0.016)
            }
            
            # Agent B analysis and execution
            opportunities = agent_b.analyze_market_opportunity(market_data, funding_rates)
            executed_actions = agent_b.execute_agent_b_strategy(opportunities)
            
            # Update asset price
            asset_prices[asset] = market_data['price']
        
        # Progress updates
        if minute % 30 == 0:
            metrics = agent_b.get_agent_b_metrics()
            print("Min {}: Return={:.2f}% | FRY={:.2f} | Trades={}".format(
                minute, metrics['total_return_pct'], metrics['total_fry_minted'], metrics['total_trades']))
    
    # Final results
    final_metrics = agent_b.get_agent_b_metrics()
    
    print("\n🏆 Agent B Final Results:")
    print("=" * 50)
    print("Total Return: {:.2f}%".format(final_metrics['total_return_pct']))
    print("Total Profits: ${:,.2f}".format(final_metrics['total_profits']))
    print("FRY Minted: {:.2f} tokens".format(final_metrics['total_fry_minted']))
    print("FRY Value: ${:,.2f}".format(final_metrics['fry_value_usd']))
    print("Slippage Harvested: ${:,.2f}".format(final_metrics['slippage_harvested']))
    print("Losses Recycled: ${:,.2f}".format(final_metrics['losses_recycled']))
    print("Total Trades: {}".format(final_metrics['total_trades']))
    print("Active Positions: {}".format(final_metrics['active_positions']))
    print("Protected Whales: {}".format(final_metrics['protected_whale_positions']))
    
    return final_metrics

if __name__ == "__main__":
    simulate_agent_b_vs_traditional_mm(180)
