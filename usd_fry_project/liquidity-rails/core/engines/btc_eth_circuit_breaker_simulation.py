#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BTC/ETH MM Simulation with Circuit Breaker Churn Control
========================================================

Focused simulation on BTC and ETH markets with enhanced circuit breaker
that restricts MM_x trading based on relative churn measurements.
"""

import json
import time
import random
import logging
import numpy as np
from collections import deque

class StrictCircuitBreaker:
    """Enhanced circuit breaker with churn-based trade limiting"""
    
    def __init__(self):
        self.churn_history = deque(maxlen=100)
        self.trade_history = deque(maxlen=50)
        self.current_churn_rate = 0.0
        self.baseline_churn = 0.0
        self.trade_cooldown = 0
        
        self.config = {
            'max_churn_multiplier': 2.0,      # Max 2x baseline churn
            'trade_limit_per_period': 3,      # Max 3 trades per 10-minute period
            'cooldown_duration': 5,           # 5-minute cooldown
            'emergency_brake_multiplier': 4.0 # Emergency stop at 4x baseline
        }
    
    def can_execute_trade(self, proposed_churn, timestamp, asset):
        """Determine if trade can be executed"""
        
        if self.trade_cooldown > 0:
            self.trade_cooldown -= 1
            return False, "Trade cooldown active"
        
        # Check recent trade frequency
        recent_trades = [t for t in self.trade_history 
                        if timestamp - t['timestamp'] <= 600]
        
        if len(recent_trades) >= self.config['trade_limit_per_period']:
            self.trade_cooldown = self.config['cooldown_duration']
            return False, "Trade frequency limit exceeded"
        
        # Check churn limits
        if self.baseline_churn > 0:
            projected_churn_rate = (self.current_churn_rate + proposed_churn) / 2
            churn_multiplier = projected_churn_rate / self.baseline_churn
            
            if churn_multiplier > self.config['emergency_brake_multiplier']:
                self.trade_cooldown = self.config['cooldown_duration'] * 2
                return False, "Emergency churn brake activated"
            
            if churn_multiplier > self.config['max_churn_multiplier']:
                return False, "Churn limit exceeded"
        
        return True, "Trade approved"
    
    def record_trade(self, churn_amount, timestamp, asset, trade_type):
        """Record executed trade"""
        self.trade_history.append({
            'churn': churn_amount,
            'timestamp': timestamp,
            'asset': asset,
            'type': trade_type
        })
        
        self.churn_history.append({
            'amount': churn_amount,
            'timestamp': timestamp
        })
        
        # Update current churn rate
        recent_window = [c for c in self.churn_history 
                        if timestamp - c['timestamp'] <= 1200]  # 20 minutes
        
        if recent_window:
            self.current_churn_rate = sum(c['amount'] for c in recent_window) / len(recent_window)
            
            if self.baseline_churn == 0.0 and len(self.churn_history) >= 10:
                self.baseline_churn = self.current_churn_rate
    
    def get_status(self):
        """Get circuit breaker status"""
        churn_ratio = (self.current_churn_rate / self.baseline_churn 
                      if self.baseline_churn > 0 else 0)
        
        return {
            'status': 'active' if self.trade_cooldown == 0 else 'cooldown',
            'churn_ratio': churn_ratio,
            'cooldown_remaining': self.trade_cooldown,
            'recent_trades': len([t for t in self.trade_history 
                                if time.time() - t['timestamp'] <= 600])
        }

class CryptoMarketMaker:
    """MM_x with circuit breaker and BTC/ETH focus"""
    
    def __init__(self, initial_capital=500000):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        
        self.assets = {
            'BTC': {'inventory': 0.0, 'trades': 0, 'profits': 0.0, 'churn': 0.0},
            'ETH': {'inventory': 0.0, 'trades': 0, 'profits': 0.0, 'churn': 0.0}
        }
        
        self.circuit_breaker = StrictCircuitBreaker()
        self.fry_balance = 0.0
        self.recycled_value = 0.0
        self.total_profits = 0.0
        self.total_trades = 0
        self.blocked_trades = 0
        self.total_churn = 0.0
        
        self.config = {
            'btc_spread': 0.0015, 'eth_spread': 0.002,
            'max_btc_inventory': 6.0, 'max_eth_inventory': 100.0,
            'btc_quote_size': 0.12, 'eth_quote_size': 1.8,
            'fry_recycling_rate': 0.4
        }
    
    def trade_asset(self, asset, market_data, timestamp):
        """Trade specific asset with circuit breaker"""
        
        price = market_data['price']
        volume = market_data.get('volume', 0)
        volatility = market_data.get('volatility', 0.02)
        
        # Asset configuration
        if asset == 'BTC':
            spread = self.config['btc_spread']
            max_inv = self.config['max_btc_inventory']
            quote_size = self.config['btc_quote_size']
        else:
            spread = self.config['eth_spread']
            max_inv = self.config['max_eth_inventory']
            quote_size = self.config['eth_quote_size']
        
        # Dynamic spread with FRY enhancement
        inventory_penalty = abs(self.assets[asset]['inventory']) * 0.0008
        fry_bonus = min(0.0004, self.fry_balance * 0.015)
        dynamic_spread = spread + inventory_penalty + volatility - fry_bonus
        dynamic_spread = max(0.001, dynamic_spread)
        
        bid_price = price * (1 - dynamic_spread / 2)
        ask_price = price * (1 + dynamic_spread / 2)
        
        # Calculate proposed trade size
        trade_size = quote_size * random.uniform(0.7, 1.0)
        proposed_churn = trade_size * price
        
        # Circuit breaker check
        can_trade, reason = self.circuit_breaker.can_execute_trade(
            proposed_churn, timestamp, asset)
        
        if not can_trade:
            self.blocked_trades += 1
            return
        
        # Execute trades
        fill_prob = min(0.4, volume / 2500000)
        
        # Buy
        if (random.random() < fill_prob and 
            self.assets[asset]['inventory'] < max_inv and
            proposed_churn < self.current_capital * 0.15):
            
            cost = trade_size * bid_price
            self.assets[asset]['inventory'] += trade_size
            self.current_capital -= cost
            self.assets[asset]['trades'] += 1
            self.total_trades += 1
            self.assets[asset]['churn'] += cost
            self.total_churn += cost
            
            self.circuit_breaker.record_trade(cost, timestamp, asset, 'buy')
        
        # Sell
        if (random.random() < fill_prob and self.assets[asset]['inventory'] > 0):
            sell_size = min(self.assets[asset]['inventory'], trade_size)
            revenue = sell_size * ask_price
            
            self.assets[asset]['inventory'] -= sell_size
            self.current_capital += revenue
            self.assets[asset]['churn'] += revenue
            self.total_churn += revenue
            
            profit = (ask_price - price) * sell_size * 0.7
            self.assets[asset]['profits'] += profit
            self.total_profits += profit
            
            self.circuit_breaker.record_trade(revenue, timestamp, asset, 'sell')
    
    def update_fry_recycling(self, btc_data, eth_data):
        """Update FRY recycling from market activity"""
        
        btc_slippage = max(0.001, btc_data.get('volume', 0) / 12000000 * 
                          btc_data.get('volatility', 0.02))
        eth_slippage = max(0.001, eth_data.get('volume', 0) / 6000000 * 
                          eth_data.get('volatility', 0.02))
        
        total_slippage = (btc_slippage + eth_slippage) / 2
        
        if total_slippage >= 0.002:
            recycled = total_slippage * self.config['fry_recycling_rate'] * random.uniform(0.9, 1.3)
            self.fry_balance += recycled
            self.recycled_value += recycled
    
    def get_metrics(self):
        """Get performance metrics"""
        btc_value = self.assets['BTC']['inventory'] * 50000
        eth_value = self.assets['ETH']['inventory'] * 3000
        total_capital = self.current_capital + btc_value + eth_value
        
        return {
            'agent_type': 'Crypto_MM_x_CB',
            'total_capital': total_capital,
            'total_return': (total_capital - self.initial_capital) / self.initial_capital,
            'total_profits': self.total_profits,
            'fry_balance': self.fry_balance,
            'recycled_value': self.recycled_value,
            'total_trades': self.total_trades,
            'blocked_trades': self.blocked_trades,
            'total_churn': self.total_churn,
            'btc_metrics': self.assets['BTC'],
            'eth_metrics': self.assets['ETH'],
            'circuit_breaker_status': self.circuit_breaker.get_status()
        }

class TraditionalCryptoMM:
    """MM_y: Traditional crypto market maker"""
    
    def __init__(self, initial_capital=500000):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        
        self.assets = {
            'BTC': {'inventory': 0.0, 'trades': 0, 'profits': 0.0, 'churn': 0.0},
            'ETH': {'inventory': 0.0, 'trades': 0, 'profits': 0.0, 'churn': 0.0}
        }
        
        self.total_profits = 0.0
        self.total_trades = 0
        self.total_churn = 0.0
        
        self.config = {
            'btc_spread': 0.002, 'eth_spread': 0.0025,
            'max_btc_inventory': 4.0, 'max_eth_inventory': 70.0,
            'btc_quote_size': 0.08, 'eth_quote_size': 1.2
        }
    
    def trade_asset(self, asset, market_data):
        """Conservative asset trading"""
        
        price = market_data['price']
        volume = market_data.get('volume', 0)
        volatility = market_data.get('volatility', 0.02)
        
        if asset == 'BTC':
            spread = self.config['btc_spread']
            max_inv = self.config['max_btc_inventory']
            quote_size = self.config['btc_quote_size']
        else:
            spread = self.config['eth_spread']
            max_inv = self.config['max_eth_inventory']
            quote_size = self.config['eth_quote_size']
        
        # Conservative spread
        dynamic_spread = spread + volatility * 2.0 + abs(self.assets[asset]['inventory']) * 0.001
        
        bid_price = price * (1 - dynamic_spread / 2)
        ask_price = price * (1 + dynamic_spread / 2)
        
        fill_prob = min(0.25, volume / 4000000)
        trade_size = quote_size * random.uniform(0.5, 0.8)
        
        # Conservative trading
        if (random.random() < fill_prob and 
            self.assets[asset]['inventory'] < max_inv):
            
            cost = trade_size * bid_price
            if cost < self.current_capital * 0.1:
                self.assets[asset]['inventory'] += trade_size
                self.current_capital -= cost
                self.assets[asset]['trades'] += 1
                self.total_trades += 1
                self.assets[asset]['churn'] += cost
                self.total_churn += cost
        
        if (random.random() < fill_prob and self.assets[asset]['inventory'] > 0):
            sell_size = min(self.assets[asset]['inventory'], trade_size)
            revenue = sell_size * ask_price
            
            self.assets[asset]['inventory'] -= sell_size
            self.current_capital += revenue
            self.assets[asset]['churn'] += revenue
            self.total_churn += revenue
            
            profit = (ask_price - price) * sell_size * 0.8
            self.assets[asset]['profits'] += profit
            self.total_profits += profit
    
    def get_metrics(self):
        """Get performance metrics"""
        btc_value = self.assets['BTC']['inventory'] * 50000
        eth_value = self.assets['ETH']['inventory'] * 3000
        total_capital = self.current_capital + btc_value + eth_value
        
        return {
            'agent_type': 'Traditional_Crypto_MM_y',
            'total_capital': total_capital,
            'total_return': (total_capital - self.initial_capital) / self.initial_capital,
            'total_profits': self.total_profits,
            'total_trades': self.total_trades,
            'total_churn': self.total_churn,
            'btc_metrics': self.assets['BTC'],
            'eth_metrics': self.assets['ETH']
        }

def generate_crypto_data(btc_price, eth_price, volatility=0.035):
    """Generate correlated BTC/ETH market data"""
    
    # Correlated movements
    btc_change = np.random.normal(0, volatility)
    eth_change = 0.7 * btc_change + 0.3 * np.random.normal(0, volatility)
    
    new_btc_price = btc_price * (1 + btc_change)
    new_eth_price = eth_price * (1 + eth_change)
    
    btc_data = {
        'price': new_btc_price,
        'volume': random.uniform(1200000, 4500000),
        'volatility': volatility,
        'social_sentiment': random.uniform(0.4, 0.9),
        'large_orders': random.uniform(0, 0.07)
    }
    
    eth_data = {
        'price': new_eth_price,
        'volume': random.uniform(800000, 2800000),
        'volatility': volatility * 1.15,
        'social_sentiment': random.uniform(0.35, 0.95),
        'large_orders': random.uniform(0, 0.08)
    }
    
    return btc_data, eth_data, new_btc_price, new_eth_price

def run_crypto_simulation(duration_minutes=90):
    """Run BTC/ETH simulation with circuit breaker"""
    
    print("🔄 BTC/ETH Circuit Breaker Simulation")
    print("=" * 60)
    
    mm_x = CryptoMarketMaker(500000)
    mm_y = TraditionalCryptoMM(500000)
    
    btc_price = 50000
    eth_price = 3000
    
    print("MM_x: Circuit Breaker + FRY")
    print("MM_y: Traditional Conservative")
    print("Duration: {} minutes\n".format(duration_minutes))
    
    for minute in range(duration_minutes):
        timestamp = time.time()
        
        # Generate market data
        btc_data, eth_data, btc_price, eth_price = generate_crypto_data(btc_price, eth_price)
        
        # MM_x trading with circuit breaker
        mm_x.trade_asset('BTC', btc_data, timestamp)
        mm_x.trade_asset('ETH', eth_data, timestamp)
        mm_x.update_fry_recycling(btc_data, eth_data)
        
        # MM_y traditional trading
        mm_y.trade_asset('BTC', btc_data)
        mm_y.trade_asset('ETH', eth_data)
        
        # Progress updates
        if minute % 20 == 0:
            mm_x_metrics = mm_x.get_metrics()
            mm_y_metrics = mm_y.get_metrics()
            cb_status = mm_x_metrics['circuit_breaker_status']
            
            print("Min {}: MM_x={:.2f}% ({}blocked, CB:{}) | MM_y={:.2f}% | BTC=${:,.0f}".format(
                minute,
                mm_x_metrics['total_return'] * 100,
                mm_x_metrics['blocked_trades'],
                cb_status['status'][:4],
                mm_y_metrics['total_return'] * 100,
                btc_price
            ))
    
    # Final results
    print("\n📊 Final Results:")
    print("=" * 60)
    
    final_mm_x = mm_x.get_metrics()
    final_mm_y = mm_y.get_metrics()
    
    print("\n🔄 MM_x (Circuit Breaker + FRY):")
    print("Return: {:.2f}%".format(final_mm_x['total_return'] * 100))
    print("Profits: ${:,.2f}".format(final_mm_x['total_profits']))
    print("FRY Balance: {:.4f}".format(final_mm_x['fry_balance']))
    print("Trades: {} ({} blocked)".format(final_mm_x['total_trades'], final_mm_x['blocked_trades']))
    print("Churn: ${:,.2f}".format(final_mm_x['total_churn']))
    
    print("\n🏦 MM_y (Traditional):")
    print("Return: {:.2f}%".format(final_mm_y['total_return'] * 100))
    print("Profits: ${:,.2f}".format(final_mm_y['total_profits']))
    print("Trades: {}".format(final_mm_y['total_trades']))
    print("Churn: ${:,.2f}".format(final_mm_y['total_churn']))
    
    # Analysis
    return_diff = final_mm_x['total_return'] - final_mm_y['total_return']
    churn_diff = final_mm_x['total_churn'] - final_mm_y['total_churn']
    
    print("\n📈 Analysis:")
    print("Return Difference: {:.2f}% ({})".format(
        return_diff * 100, "MM_x Wins" if return_diff > 0 else "MM_y Wins"))
    print("Churn Difference: ${:,.2f}".format(churn_diff))
    print("Circuit Breaker Effectiveness: {:.1f}% trades blocked".format(
        final_mm_x['blocked_trades'] / max(1, final_mm_x['total_trades'] + final_mm_x['blocked_trades']) * 100))
    
    # Save results
    results = {
        'mm_x_final': final_mm_x,
        'mm_y_final': final_mm_y,
        'analysis': {
            'return_difference_pct': return_diff * 100,
            'churn_difference': churn_diff,
            'winner': 'MM_x' if return_diff > 0 else 'MM_y'
        }
    }
    
    results_file = "btc_eth_cb_simulation_{}.json".format(int(time.time()))
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Results saved: {}".format(results_file))
    return results

if __name__ == "__main__":
    run_crypto_simulation(90)
