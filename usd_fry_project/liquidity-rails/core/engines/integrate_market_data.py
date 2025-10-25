#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Integration Example: Market Data → Agent B Training
===================================================

Shows how to integrate real market data with Agent B federated learning.
"""

import numpy as np
from market_data_collector import MarketDataCollector
from agent_b_core import AgentB

def integrate_real_data_with_agent_b():
    """
    Example: Use real market data for Agent B training
    """
    
    print("="*70)
    print("Integrating Real Market Data with Agent B")
    print("="*70 + "\n")
    
    # 1. Collect real market data
    print("Step 1: Collecting market data from exchanges...")
    collector = MarketDataCollector(['binance'])
    validation_data = collector.collect_validation_data('BTC/USDT', hours=50)
    
    print(f"✓ Collected {len(validation_data)} samples\n")
    
    # 2. Initialize Agent B
    print("Step 2: Initializing Agent B...")
    agent_b = AgentB(initial_capital=1000000)
    print("✓ Agent B initialized\n")
    
    # 3. Process market data for Agent B
    print("Step 3: Processing data for hedge ratio prediction...")
    
    training_samples = []
    for data_point in validation_data[:100]:  # Use first 100 samples
        # Create market data dict for Agent B
        market_data = {
            'asset': 'BTC',
            'price': data_point['close'],
            'volume': data_point['volume'],
            'volatility': data_point['volatility'],
            'bid_ask_spread': data_point['bid_ask_spread'],
            'order_book_depth': data_point['liquidity_depth'],
            'social_sentiment': 0.5,  # Would come from sentiment analysis
            'liquidity_depth': data_point['liquidity_depth'],
        }
        
        # Get funding rates for arbitrage
        funding_rates = {
            'binance': np.random.uniform(-0.005, 0.015),  # Would be real
            'okx': np.random.uniform(-0.007, 0.012),
        }
        
        # Analyze opportunities
        opportunities = agent_b.analyze_market_opportunity(market_data, funding_rates)
        
        training_samples.append({
            'market_data': market_data,
            'opportunities': opportunities,
            'timestamp': data_point['timestamp']
        })
    
    print(f"✓ Processed {len(training_samples)} training samples\n")
    
    # 4. Get Agent B metrics
    print("Step 4: Agent B Performance Metrics")
    print("-" * 70)
    metrics = agent_b.get_agent_b_metrics()
    print(f"Total FRY Minted: {metrics['total_fry_minted']:.2f}")
    print(f"Slippage Harvested: ${metrics['slippage_harvested']:,.2f}")
    print(f"Total Trades: {metrics['total_trades']}")
    
    print("\n" + "="*70)
    print("✓ Integration complete - Ready for federated learning")
    print("="*70)
    
    return training_samples


if __name__ == "__main__":
    integrate_real_data_with_agent_b()
