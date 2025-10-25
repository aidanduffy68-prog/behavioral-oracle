#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Market Data Collector for Agent B Federated Learning
====================================================

Collects real market data from cryptocurrency exchanges for Agent B training.
Supports multiple venues (Binance, OKX, Bybit, dYdX) and provides features
for hedge ratio prediction, topology routing, and zkML proof generation.

Features Collected:
- OHLCV data (price, volume)
- Order book depth (liquidity)
- Funding rates (perpetual futures)
- Volatility metrics
- Technical indicators (RSI, Bollinger Bands)
- Market microstructure (bid-ask spread, order flow)

Usage:
    collector = MarketDataCollector(['binance', 'okx'])
    data = collector.collect_validation_data('BTC/USDT', hours=100)
"""

import ccxt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketDataCollector:
    """
    Collects real-time and historical market data from cryptocurrency exchanges.
    
    Supports:
    - Binance, OKX, Bybit, dYdX, Kraken
    - Spot and perpetual futures markets
    - Order book data
    - Funding rates
    """
    
    def __init__(self, venues: List[str] = None):
        """
        Initialize market data collector.
        
        Args:
            venues: List of exchange names (e.g., ['binance', 'okx', 'bybit'])
        """
        if venues is None:
            venues = ['binance', 'okx', 'bybit']
        
        self.venues = venues
        self.exchanges = {}
        
        # Initialize exchanges
        for venue in venues:
            try:
                exchange_class = getattr(ccxt, venue)
                self.exchanges[venue] = exchange_class({
                    'enableRateLimit': True,
                    'timeout': 30000,
                })
                logger.info(f"✓ Connected to {venue}")
            except Exception as e:
                logger.error(f"✗ Failed to connect to {venue}: {e}")
        
        logger.info(f"Market Data Collector initialized with {len(self.exchanges)} venues")
    
    def collect_validation_data(self, symbol: str = 'BTC/USDT', 
                                hours: int = 100) -> List[Dict]:
        """
        Collect validation data for Agent B training and zkML proofs.
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            hours: Number of hours of historical data
        
        Returns:
            List of feature dictionaries suitable for hedge ratio prediction
        """
        validation_data = []
        
        for venue, exchange in self.exchanges.items():
            logger.info(f"Collecting data from {venue}...")
            
            try:
                # Get OHLCV data
                ohlcv = exchange.fetch_ohlcv(symbol, '1h', limit=hours)
                
                # Get current order book
                orderbook = exchange.fetch_order_book(symbol)
                
                # Calculate moving averages for context
                closes = [candle[4] for candle in ohlcv]
                volumes = [candle[5] for candle in ohlcv]
                
                avg_volume = np.mean(volumes)
                
                # Process each candle
                for i, candle in enumerate(ohlcv):
                    timestamp, open_price, high, low, close, volume = candle
                    
                    # Skip if not enough history for indicators
                    if i < 20:
                        continue
                    
                    # Calculate features
                    features = self._calculate_features(
                        candle, ohlcv[max(0, i-20):i+1], 
                        orderbook, venue, avg_volume
                    )
                    
                    validation_data.append(features)
                
                logger.info(f"✓ Collected {len(ohlcv)} samples from {venue}")
                
            except Exception as e:
                logger.error(f"✗ Error collecting from {venue}: {e}")
        
        logger.info(f"Total validation samples: {len(validation_data)}")
        return validation_data
    
    def _calculate_features(self, candle: List, history: List, 
                           orderbook: Dict, venue: str, avg_volume: float) -> Dict:
        """Calculate all features for a single data point"""
        
        timestamp, open_price, high, low, close, volume = candle
        
        # Price metrics
        price_change_pct = (close - open_price) / open_price
        volatility = (high - low) / open_price
        
        # Volume metrics
        volume_ratio = volume / avg_volume if avg_volume > 0 else 1.0
        
        # Order book metrics
        bid_price = orderbook['bids'][0][0] if orderbook['bids'] else close
        ask_price = orderbook['asks'][0][0] if orderbook['asks'] else close
        bid_ask_spread = (ask_price - bid_price) / bid_price
        
        # Liquidity depth (sum of top 10 bids/asks)
        liquidity_depth = sum([bid[1] for bid in orderbook['bids'][:10]]) if orderbook['bids'] else 0
        
        # Order flow imbalance
        bid_volume = sum([bid[1] for bid in orderbook['bids'][:10]]) if orderbook['bids'] else 0
        ask_volume = sum([ask[1] for ask in orderbook['asks'][:10]]) if orderbook['asks'] else 0
        order_flow_imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume) if (bid_volume + ask_volume) > 0 else 0
        
        # Technical indicators
        closes = [h[4] for h in history]
        rsi = self._calculate_rsi(closes)
        bollinger_position = self._calculate_bollinger_position(closes, close)
        
        return {
            'timestamp': timestamp,
            'venue': venue,
            'symbol': 'BTC/USDT',
            'close': close,
            'open': open_price,
            'high': high,
            'low': low,
            'volume': volume,
            # Normalized features for ML
            'price_change_pct': price_change_pct,
            'volatility': volatility,
            'volume_ratio': volume_ratio,
            'bid_ask_spread': bid_ask_spread,
            'order_flow_imbalance': order_flow_imbalance,
            'rsi': rsi,
            'bollinger_position': bollinger_position,
            'liquidity_depth': liquidity_depth,
        }
    
    def _calculate_rsi(self, closes: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if len(closes) < period + 1:
            return 50.0
        
        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_bollinger_position(self, closes: List[float], 
                                     current_price: float, period: int = 20) -> float:
        """Calculate position within Bollinger Bands (0 = lower, 0.5 = middle, 1 = upper)"""
        if len(closes) < period:
            return 0.5
        
        recent_closes = closes[-period:]
        sma = np.mean(recent_closes)
        std = np.std(recent_closes)
        
        upper_band = sma + (2 * std)
        lower_band = sma - (2 * std)
        
        if upper_band == lower_band:
            return 0.5
        
        position = (current_price - lower_band) / (upper_band - lower_band)
        return np.clip(position, 0, 1)
    
    def get_funding_rates(self, symbol: str = 'BTC/USDT:USDT') -> Dict[str, float]:
        """
        Get current funding rates across venues for arbitrage opportunities.
        
        Args:
            symbol: Perpetual futures symbol
        
        Returns:
            Dict mapping venue to funding rate
        """
        funding_rates = {}
        
        for venue, exchange in self.exchanges.items():
            try:
                if hasattr(exchange, 'fetch_funding_rate'):
                    rate_data = exchange.fetch_funding_rate(symbol)
                    funding_rates[venue] = rate_data.get('fundingRate', 0.0)
                    logger.info(f"{venue} funding rate: {funding_rates[venue]:.6f}")
            except Exception as e:
                logger.warning(f"Could not fetch funding rate from {venue}: {e}")
        
        return funding_rates
    
    def get_market_depth(self, symbol: str = 'BTC/USDT', 
                        depth: int = 50) -> Dict[str, Dict]:
        """
        Get order book depth for liquidity analysis.
        
        Args:
            symbol: Trading pair
            depth: Number of levels to fetch
        
        Returns:
            Dict mapping venue to order book data
        """
        market_depth = {}
        
        for venue, exchange in self.exchanges.items():
            try:
                orderbook = exchange.fetch_order_book(symbol, limit=depth)
                
                # Calculate depth metrics
                bid_depth = sum([bid[1] for bid in orderbook['bids']])
                ask_depth = sum([ask[1] for ask in orderbook['asks']])
                
                market_depth[venue] = {
                    'bids': orderbook['bids'],
                    'asks': orderbook['asks'],
                    'bid_depth': bid_depth,
                    'ask_depth': ask_depth,
                    'spread': (orderbook['asks'][0][0] - orderbook['bids'][0][0]) / orderbook['bids'][0][0],
                }
                
                logger.info(f"{venue} depth: {bid_depth:.2f} bids, {ask_depth:.2f} asks")
                
            except Exception as e:
                logger.warning(f"Could not fetch depth from {venue}: {e}")
        
        return market_depth
    
    def export_to_csv(self, data: List[Dict], filename: str = None):
        """Export collected data to CSV for analysis"""
        if filename is None:
            filename = f"market_data_{int(time.time())}.csv"
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logger.info(f"✓ Exported {len(data)} samples to {filename}")
        
        return filename
    
    def get_live_market_snapshot(self, symbol: str = 'BTC/USDT') -> Dict:
        """
        Get current market snapshot across all venues.
        
        Useful for real-time Agent B decision making.
        """
        snapshot = {
            'timestamp': time.time(),
            'symbol': symbol,
            'venues': {}
        }
        
        for venue, exchange in self.exchanges.items():
            try:
                # Get ticker
                ticker = exchange.fetch_ticker(symbol)
                
                # Get order book
                orderbook = exchange.fetch_order_book(symbol, limit=10)
                
                snapshot['venues'][venue] = {
                    'price': ticker['last'],
                    'volume_24h': ticker['quoteVolume'],
                    'bid': orderbook['bids'][0][0] if orderbook['bids'] else 0,
                    'ask': orderbook['asks'][0][0] if orderbook['asks'] else 0,
                    'spread': (orderbook['asks'][0][0] - orderbook['bids'][0][0]) / orderbook['bids'][0][0] if orderbook['bids'] and orderbook['asks'] else 0,
                }
                
            except Exception as e:
                logger.warning(f"Could not get snapshot from {venue}: {e}")
        
        return snapshot


def demo_market_data_collection():
    """Demonstrate market data collection"""
    print("\n" + "="*70)
    print("Market Data Collector Demo")
    print("="*70 + "\n")
    
    # Initialize collector
    collector = MarketDataCollector(['binance', 'okx'])
    
    print("\n1. Collecting validation data...")
    print("-" * 70)
    validation_data = collector.collect_validation_data('BTC/USDT', hours=50)
    print(f"Collected {len(validation_data)} samples")
    
    if validation_data:
        sample = validation_data[0]
        print(f"\nSample data point:")
        print(f"  Venue: {sample['venue']}")
        print(f"  Price: ${sample['close']:,.2f}")
        print(f"  Volatility: {sample['volatility']:.4f}")
        print(f"  Volume Ratio: {sample['volume_ratio']:.2f}")
        print(f"  RSI: {sample['rsi']:.2f}")
        print(f"  Bid-Ask Spread: {sample['bid_ask_spread']:.4f}")
    
    print("\n2. Getting funding rates...")
    print("-" * 70)
    funding_rates = collector.get_funding_rates('BTC/USDT:USDT')
    for venue, rate in funding_rates.items():
        print(f"  {venue}: {rate:.6f}")
    
    print("\n3. Getting market depth...")
    print("-" * 70)
    market_depth = collector.get_market_depth('BTC/USDT', depth=20)
    for venue, depth in market_depth.items():
        print(f"  {venue}:")
        print(f"    Bid depth: {depth['bid_depth']:,.2f}")
        print(f"    Ask depth: {depth['ask_depth']:,.2f}")
        print(f"    Spread: {depth['spread']:.4f}")
    
    print("\n4. Live market snapshot...")
    print("-" * 70)
    snapshot = collector.get_live_market_snapshot('BTC/USDT')
    for venue, data in snapshot['venues'].items():
        print(f"  {venue}: ${data['price']:,.2f} | Spread: {data['spread']:.4f}")
    
    print("\n5. Exporting to CSV...")
    print("-" * 70)
    filename = collector.export_to_csv(validation_data)
    print(f"  Saved to: {filename}")
    
    print("\n" + "="*70)
    print("✓ Market data collection complete")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_market_data_collection()
