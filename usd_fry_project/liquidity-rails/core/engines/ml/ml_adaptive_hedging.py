#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ML-Enhanced Adaptive Hedging System for Agent B
===============================================

Machine learning enhanced adaptive hedging with reasoning structures for
sophisticated market regime detection and dynamic hedge optimization.
"""

import numpy as np
import json
import time
from collections import deque
import random
import math

class MarketRegimeDetector:
    """ML-based market regime detection using pattern recognition"""
    
    def __init__(self):
        self.regime_history = deque(maxlen=1000)
        self.feature_history = deque(maxlen=100)
        self.regime_weights = {
            'trending_bull': 0.25,
            'trending_bear': 0.25, 
            'sideways': 0.20,
            'volatile': 0.15,
            'crisis': 0.10,
            'recovery': 0.05
        }
        
    def extract_market_features(self, market_data):
        """Extract key features for regime detection"""
        
        # Price momentum features
        price_change = market_data.get('price_change_pct', 0)
        volume_ratio = market_data.get('volume_ratio', 1.0)
        volatility = market_data.get('volatility', 0.02)
        
        # Technical indicators
        rsi = market_data.get('rsi', 50)
        bb_position = market_data.get('bollinger_position', 0.5)
        
        # Market microstructure
        bid_ask_spread = market_data.get('bid_ask_spread', 0.001)
        order_flow_imbalance = market_data.get('order_flow_imbalance', 0)
        
        features = {
            'momentum': abs(price_change),
            'direction': 1 if price_change > 0 else -1,
            'volume_surge': max(0, volume_ratio - 1),
            'volatility_regime': min(1.0, volatility / 0.05),
            'rsi_extreme': abs(rsi - 50) / 50,
            'bb_extreme': abs(bb_position - 0.5) * 2,
            'liquidity_stress': min(1.0, bid_ask_spread / 0.01),
            'flow_imbalance': abs(order_flow_imbalance)
        }
        
        return features
    
    def detect_regime(self, market_data):
        """Detect current market regime using ML reasoning"""
        
        features = self.extract_market_features(market_data)
        self.feature_history.append(features)
        
        # Regime scoring based on feature patterns
        regime_scores = {}
        
        # Trending Bull: Strong positive momentum, high volume, low volatility
        regime_scores['trending_bull'] = (
            features['momentum'] * features['direction'] * 0.4 +
            features['volume_surge'] * 0.3 +
            (1 - features['volatility_regime']) * 0.3
        ) if features['direction'] > 0 else 0
        
        # Trending Bear: Strong negative momentum, high volume, moderate volatility
        regime_scores['trending_bear'] = (
            features['momentum'] * abs(features['direction']) * 0.4 +
            features['volume_surge'] * 0.3 +
            features['volatility_regime'] * 0.3
        ) if features['direction'] < 0 else 0
        
        # Sideways: Low momentum, normal volume, low volatility
        regime_scores['sideways'] = (
            (1 - features['momentum']) * 0.5 +
            (1 - features['volume_surge']) * 0.3 +
            (1 - features['volatility_regime']) * 0.2
        )
        
        # Volatile: High volatility, extreme RSI, wide spreads
        regime_scores['volatile'] = (
            features['volatility_regime'] * 0.4 +
            features['rsi_extreme'] * 0.3 +
            features['liquidity_stress'] * 0.3
        )
        
        # Crisis: Extreme volatility, liquidity stress, flow imbalance
        regime_scores['crisis'] = (
            min(1.0, features['volatility_regime'] * 1.5) * 0.4 +
            features['liquidity_stress'] * 0.3 +
            features['flow_imbalance'] * 0.3
        )
        
        # Recovery: Positive momentum after crisis, improving liquidity
        recent_crisis = any(r == 'crisis' for r in list(self.regime_history)[-10:])
        regime_scores['recovery'] = (
            features['momentum'] * features['direction'] * 0.4 +
            (1 - features['liquidity_stress']) * 0.3 +
            (0.3 if recent_crisis and features['direction'] > 0 else 0)
        ) if features['direction'] > 0 else 0
        
        # Select regime with highest score
        detected_regime = max(regime_scores, key=regime_scores.get)
        confidence = regime_scores[detected_regime]
        
        self.regime_history.append(detected_regime)
        
        return detected_regime, confidence, regime_scores

class ReinforcementHedgeOptimizer:
    """RL-based hedge ratio optimization"""
    
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1
        self.action_space = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        self.performance_history = deque(maxlen=1000)
        
    def get_state_key(self, regime, lpi_score, position_size_bucket):
        """Create state key for Q-table"""
        lpi_bucket = int(lpi_score * 10) / 10
        return "{}_{:.1f}_{}".format(regime, lpi_bucket, position_size_bucket)
    
    def select_hedge_ratio(self, regime, lpi_score, position_size):
        """Select optimal hedge ratio using Q-learning"""
        
        # Discretize position size
        if position_size < 100000:
            size_bucket = 'small'
        elif position_size < 500000:
            size_bucket = 'medium'
        else:
            size_bucket = 'large'
        
        state_key = self.get_state_key(regime, lpi_score, size_bucket)
        
        # Initialize Q-values if new state
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.action_space}
        
        # Epsilon-greedy action selection
        if random.random() < self.epsilon:
            selected_ratio = random.choice(self.action_space)
        else:
            q_values = self.q_table[state_key]
            selected_ratio = max(q_values, key=q_values.get)
        
        return selected_ratio, state_key
    
    def update_q_value(self, state_key, action, reward, next_state_key=None):
        """Update Q-value based on performance feedback"""
        
        if state_key not in self.q_table:
            return
        
        current_q = self.q_table[state_key][action]
        
        if next_state_key and next_state_key in self.q_table:
            max_next_q = max(self.q_table[next_state_key].values())
        else:
            max_next_q = 0
        
        # Q-learning update
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        
        self.q_table[state_key][action] = new_q

class EnsembleReasoningFramework:
    """Ensemble framework for multi-model decision making"""
    
    def __init__(self):
        self.models = {
            'regime_detector': MarketRegimeDetector(),
            'rl_optimizer': ReinforcementHedgeOptimizer()
        }
        self.decision_history = deque(maxlen=500)
        self.model_weights = {
            'lpi_traditional': 0.3,
            'regime_based': 0.4,
            'rl_optimized': 0.3
        }
        
    def calculate_ensemble_hedge_ratio(self, market_data, lpi_score, position_size, 
                                     traditional_ratio, circuit_breaker_active):
        """Calculate hedge ratio using ensemble of reasoning models"""
        
        # 1. Traditional LPI-based ratio
        traditional_component = traditional_ratio
        
        # 2. Regime-based adjustment
        regime, regime_confidence, regime_scores = self.models['regime_detector'].detect_regime(market_data)
        
        regime_adjustments = {
            'trending_bull': -0.1,    # Reduce hedging in strong uptrend
            'trending_bear': 0.15,    # Increase hedging in downtrend
            'sideways': 0.0,          # Neutral adjustment
            'volatile': 0.2,          # Increase hedging in volatile markets
            'crisis': 0.3,            # Maximum hedging in crisis
            'recovery': -0.05         # Slightly reduce hedging in recovery
        }
        
        regime_adjustment = regime_adjustments.get(regime, 0.0) * regime_confidence
        regime_component = traditional_ratio + regime_adjustment
        
        # 3. RL-optimized ratio
        rl_ratio, rl_state_key = self.models['rl_optimizer'].select_hedge_ratio(
            regime, lpi_score, position_size
        )
        
        # Circuit breaker override
        if circuit_breaker_active:
            # Emergency mode: use maximum of all recommendations
            final_ratio = max(traditional_component, regime_component, rl_ratio, 0.8)
            reasoning = "CIRCUIT_BREAKER_OVERRIDE"
        else:
            # Weighted ensemble
            final_ratio = (
                self.model_weights['lpi_traditional'] * traditional_component +
                self.model_weights['regime_based'] * regime_component +
                self.model_weights['rl_optimized'] * rl_ratio
            )
            reasoning = "ENSEMBLE_WEIGHTED"
        
        # Apply bounds
        final_ratio = max(0.0, min(1.0, final_ratio))
        
        # Record decision for learning
        decision_record = {
            'timestamp': time.time(),
            'regime': regime,
            'regime_confidence': regime_confidence,
            'lpi_score': lpi_score,
            'traditional_ratio': traditional_component,
            'regime_ratio': regime_component,
            'rl_ratio': rl_ratio,
            'final_ratio': final_ratio,
            'reasoning': reasoning,
            'rl_state_key': rl_state_key,
            'position_size': position_size
        }
        
        self.decision_history.append(decision_record)
        
        return final_ratio, decision_record

class MLAdaptiveHedgingEngine:
    """Main ML-enhanced adaptive hedging engine for Agent B"""
    
    def __init__(self, base_config=None):
        self.config = base_config or {
            'base_hedge_ratio': 0.5,
            'min_hedge_ratio': 0.0,
            'max_hedge_ratio': 1.0,
            'lpi_sensitivity': 0.3,
            'circuit_breaker_hedge': 0.8,
            'learning_enabled': True,
            'performance_window': 100
        }
        
        self.ensemble = EnsembleReasoningFramework()
        self.performance_tracker = deque(maxlen=self.config['performance_window'])
        
    def calculate_enhanced_hedge_ratio(self, asset, market_data, position_size, 
                                     lpi_score, circuit_breaker_active, timestamp):
        """Calculate hedge ratio using ML-enhanced reasoning"""
        
        # Traditional LPI-based calculation
        base_ratio = self.config['base_hedge_ratio']
        lpi_adjustment = (lpi_score - 0.5) * self.config['lpi_sensitivity']
        traditional_ratio = base_ratio + lpi_adjustment
        
        # Size adjustment
        size_factor = min(0.2, position_size / 1000000)
        traditional_ratio += size_factor
        
        # ML ensemble enhancement
        final_ratio, decision_record = self.ensemble.calculate_ensemble_hedge_ratio(
            market_data, lpi_score, position_size, traditional_ratio, circuit_breaker_active
        )
        
        # Apply configuration bounds
        final_ratio = max(
            self.config['min_hedge_ratio'],
            min(self.config['max_hedge_ratio'], final_ratio)
        )
        
        return final_ratio, decision_record
    
    def update_performance_feedback(self, hedge_decision, actual_pnl, market_outcome):
        """Update ML models based on performance feedback"""
        
        if not self.config['learning_enabled']:
            return
        
        # Calculate reward based on hedge effectiveness
        expected_loss = hedge_decision['position_size'] * market_outcome.get('price_change_pct', 0)
        actual_loss = expected_loss * (1 - hedge_decision['final_ratio'])
        
        # Reward is negative of actual loss (minimize loss = maximize reward)
        reward = -abs(actual_loss) / max(1, hedge_decision['position_size'] / 100000)
        
        # Update RL model
        if 'rl_state_key' in hedge_decision:
            self.ensemble.models['rl_optimizer'].update_q_value(
                hedge_decision['rl_state_key'],
                hedge_decision['rl_ratio'],
                reward
            )
        
        # Track performance
        performance_record = {
            'timestamp': hedge_decision['timestamp'],
            'hedge_ratio': hedge_decision['final_ratio'],
            'actual_pnl': actual_pnl,
            'reward': reward,
            'regime': hedge_decision['regime'],
            'reasoning': hedge_decision['reasoning']
        }
        
        self.performance_tracker.append(performance_record)
    
    def get_reasoning_explanation(self, decision_record):
        """Generate human-readable explanation of hedging decision"""
        
        explanation = []
        explanation.append("ML-Enhanced Hedging Decision Analysis:")
        explanation.append("=" * 50)
        
        explanation.append("Market Regime: {} (Confidence: {:.1%})".format(
            decision_record['regime'].upper(),
            decision_record['regime_confidence']
        ))
        
        explanation.append("Component Ratios:")
        explanation.append("  Traditional LPI: {:.1%}".format(decision_record['traditional_ratio']))
        explanation.append("  Regime-Adjusted: {:.1%}".format(decision_record['regime_ratio']))
        explanation.append("  RL-Optimized: {:.1%}".format(decision_record['rl_ratio']))
        explanation.append("  Final Ensemble: {:.1%}".format(decision_record['final_ratio']))
        
        explanation.append("Reasoning: {}".format(decision_record['reasoning']))
        
        return "\n".join(explanation)
    
    def get_performance_summary(self):
        """Get ML model performance summary"""
        
        if not self.performance_tracker:
            return "No performance data available"
        
        recent_performance = list(self.performance_tracker)[-50:]
        avg_reward = sum(p['reward'] for p in recent_performance) / len(recent_performance)
        
        regime_performance = {}
        for perf in recent_performance:
            regime = perf['regime']
            if regime not in regime_performance:
                regime_performance[regime] = []
            regime_performance[regime].append(perf['reward'])
        
        summary = []
        summary.append("ML Adaptive Hedging Performance Summary:")
        summary.append("=" * 45)
        summary.append("Average Reward (Recent 50): {:.4f}".format(avg_reward))
        summary.append("Performance by Regime:")
        
        for regime, rewards in regime_performance.items():
            avg_regime_reward = sum(rewards) / len(rewards)
            summary.append("  {}: {:.4f} ({} samples)".format(
                regime.upper(), avg_regime_reward, len(rewards)
            ))
        
        return "\n".join(summary)

def create_ml_enhanced_agent_b():
    """Factory function to create Agent B with ML-enhanced adaptive hedging"""
    
    # This would integrate with the existing AgentB class
    ml_hedging_engine = MLAdaptiveHedgingEngine()
    
    return ml_hedging_engine

if __name__ == "__main__":
    # Demonstration of ML-enhanced adaptive hedging
    print("ML-Enhanced Adaptive Hedging System for Agent B")
    print("=" * 60)
    
    ml_engine = create_ml_enhanced_agent_b()
    
    # Simulate market conditions
    market_scenarios = [
        {'regime': 'trending_bull', 'volatility': 0.02, 'price_change_pct': 0.05},
        {'regime': 'volatile', 'volatility': 0.08, 'price_change_pct': -0.03},
        {'regime': 'crisis', 'volatility': 0.15, 'price_change_pct': -0.12},
        {'regime': 'recovery', 'volatility': 0.06, 'price_change_pct': 0.08}
    ]
    
    for i, scenario in enumerate(market_scenarios):
        print("\nScenario {}: {} Market".format(i+1, scenario['regime'].upper()))
        print("-" * 40)
        
        market_data = {
            'price_change_pct': scenario['price_change_pct'],
            'volatility': scenario['volatility'],
            'volume_ratio': random.uniform(0.8, 2.0),
            'rsi': random.uniform(20, 80),
            'bollinger_position': random.uniform(0, 1),
            'bid_ask_spread': scenario['volatility'] * 0.1,
            'order_flow_imbalance': random.uniform(-0.5, 0.5)
        }
        
        hedge_ratio, decision = ml_engine.calculate_enhanced_hedge_ratio(
            'BTC', market_data, 500000, 0.6, False, time.time()
        )
        
        print("Recommended Hedge Ratio: {:.1%}".format(hedge_ratio))
        print("Market Regime Detected: {}".format(decision['regime'].upper()))
        print("Regime Confidence: {:.1%}".format(decision['regime_confidence']))
        print("Reasoning: {}".format(decision['reasoning']))
    
    print("\n" + "=" * 60)
    print("ML-Enhanced Adaptive Hedging System Ready for Integration")
