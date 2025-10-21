#!/usr/bin/env python3
"""
Behavioral Liquidity Mining Engine
==================================

Extracts trading alpha from trader psychology patterns post-liquidation.
Transforms behavioral data into actionable trading signals.

Core Innovation:
- Liquidation events create behavioral "fingerprints" 
- ML models predict future trading behavior from these patterns
- Behavioral patterns become tradeable assets (Behavioral Liquidity)
- Same infrastructure serves retention + alpha generation

Research Direction: "Behavioral Liquidity Mining"
"""

import numpy as np
import pandas as pd
import sqlite3
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FRY color scheme
FRY_RED = "\033[91m"
FRY_YELLOW = "\033[93m"
FRY_GREEN = "\033[92m"
FRY_BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


@dataclass
class BehavioralPattern:
    """Represents a behavioral pattern extracted from trader data"""
    pattern_id: str
    pattern_type: str  # 'retention', 'profitability', 'migration', 'sentiment'
    confidence: float
    alpha_potential: float  # Expected trading alpha from this pattern
    sample_size: int
    pattern_data: Dict


@dataclass
class LiquidationFingerprint:
    """Behavioral fingerprint created from liquidation event"""
    wallet_address: str
    liquidation_timestamp: int
    liquidation_size: float
    asset: str
    leverage: float
    time_to_liquidation: int  # Hours from position open to liquidation
    
    # Behavioral features
    pre_liquidation_activity: Dict
    post_liquidation_activity: Dict
    cross_platform_activity: Dict
    social_sentiment: Dict
    
    # Derived behavioral metrics
    risk_tolerance: float
    recovery_speed: float
    platform_loyalty: float
    trading_consistency: float


class BehavioralFeatureExtractor:
    """Extracts behavioral features from trader activity data"""
    
    def __init__(self):
        self.feature_cache = {}
        
    def extract_liquidation_fingerprint(self, wallet_data: Dict) -> LiquidationFingerprint:
        """Extract behavioral fingerprint from wallet activity data"""
        
        # Core liquidation data
        liquidation = wallet_data['liquidation']
        
        # Pre-liquidation behavioral features
        pre_activity = self._analyze_pre_liquidation_behavior(wallet_data)
        
        # Post-liquidation behavioral features  
        post_activity = self._analyze_post_liquidation_behavior(wallet_data)
        
        # Cross-platform analysis
        cross_platform = self._analyze_cross_platform_behavior(wallet_data)
        
        # Social sentiment analysis
        social_sentiment = self._analyze_social_sentiment(wallet_data)
        
        # Derived behavioral metrics
        risk_tolerance = self._calculate_risk_tolerance(pre_activity)
        recovery_speed = self._calculate_recovery_speed(post_activity)
        platform_loyalty = self._calculate_platform_loyalty(cross_platform)
        trading_consistency = self._calculate_trading_consistency(pre_activity)
        
        return LiquidationFingerprint(
            wallet_address=liquidation['wallet'],
            liquidation_timestamp=liquidation['timestamp'],
            liquidation_size=liquidation['size'],
            asset=liquidation['asset'],
            leverage=liquidation['leverage'],
            time_to_liquidation=liquidation['time_to_liquidation'],
            pre_liquidation_activity=pre_activity,
            post_liquidation_activity=post_activity,
            cross_platform_activity=cross_platform,
            social_sentiment=social_sentiment,
            risk_tolerance=risk_tolerance,
            recovery_speed=recovery_speed,
            platform_loyalty=platform_loyalty,
            trading_consistency=trading_consistency
        )
    
    def _analyze_pre_liquidation_behavior(self, wallet_data: Dict) -> Dict:
        """Analyze trading behavior before liquidation"""
        
        trades = wallet_data.get('pre_liquidation_trades', [])
        
        if not trades:
            return {'trading_frequency': 0, 'avg_position_size': 0, 'leverage_trend': 0}
        
        # Trading frequency (trades per day)
        time_span = max(t['timestamp'] for t in trades) - min(t['timestamp'] for t in trades)
        trading_frequency = len(trades) / max(time_span / (24 * 3600), 1)
        
        # Average position size trend
        position_sizes = [t['size'] for t in trades]
        avg_position_size = np.mean(position_sizes)
        
        # Leverage trend (increasing/decreasing)
        leverages = [t['leverage'] for t in trades]
        leverage_trend = np.polyfit(range(len(leverages)), leverages, 1)[0] if len(leverages) > 1 else 0
        
        # Risk escalation pattern
        risk_escalation = self._detect_risk_escalation(trades)
        
        return {
            'trading_frequency': trading_frequency,
            'avg_position_size': avg_position_size,
            'leverage_trend': leverage_trend,
            'risk_escalation': risk_escalation,
            'total_trades': len(trades),
            'win_rate': self._calculate_win_rate(trades)
        }
    
    def _analyze_post_liquidation_behavior(self, wallet_data: Dict) -> Dict:
        """Analyze trading behavior after liquidation"""
        
        trades = wallet_data.get('post_liquidation_trades', [])
        
        if not trades:
            return {'return_time': None, 'recovery_trading': False, 'conservative_shift': 0}
        
        # Time to return to trading
        liquidation_time = wallet_data['liquidation']['timestamp']
        first_post_trade = min(t['timestamp'] for t in trades)
        return_time = (first_post_trade - liquidation_time) / 3600  # Hours
        
        # Recovery trading patterns
        recovery_trading = len(trades) > 0
        
        # Conservative shift (reduced leverage, smaller positions)
        avg_leverage_post = np.mean([t['leverage'] for t in trades])
        avg_leverage_pre = np.mean([t['leverage'] for t in wallet_data.get('pre_liquidation_trades', [])])
        conservative_shift = avg_leverage_pre - avg_leverage_post if avg_leverage_pre > 0 else 0
        
        return {
            'return_time': return_time,
            'recovery_trading': recovery_trading,
            'conservative_shift': conservative_shift,
            'post_trades_count': len(trades),
            'avg_position_size_post': np.mean([t['size'] for t in trades]) if trades else 0
        }
    
    def _analyze_cross_platform_behavior(self, wallet_data: Dict) -> Dict:
        """Analyze behavior across different platforms"""
        
        platforms = wallet_data.get('platform_activity', {})
        
        if not platforms:
            return {'platform_diversity': 0, 'primary_platform': None, 'migration_pattern': 'none'}
        
        # Platform diversity
        platform_diversity = len(platforms)
        
        # Primary platform (most activity)
        primary_platform = max(platforms.items(), key=lambda x: x[1]['activity_count'])[0]
        
        # Migration pattern
        migration_pattern = self._detect_migration_pattern(platforms)
        
        return {
            'platform_diversity': platform_diversity,
            'primary_platform': primary_platform,
            'migration_pattern': migration_pattern,
            'platforms': list(platforms.keys())
        }
    
    def _analyze_social_sentiment(self, wallet_data: Dict) -> Dict:
        """Analyze social media sentiment around liquidation"""
        
        social_data = wallet_data.get('social_activity', {})
        
        if not social_data:
            return {'sentiment_score': 0, 'mention_count': 0, 'sentiment_trend': 'neutral'}
        
        # Sentiment analysis (simplified)
        mentions = social_data.get('mentions', [])
        sentiment_scores = [m.get('sentiment', 0) for m in mentions]
        
        avg_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0
        mention_count = len(mentions)
        
        # Sentiment trend over time
        sentiment_trend = self._calculate_sentiment_trend(mentions)
        
        return {
            'sentiment_score': avg_sentiment,
            'mention_count': mention_count,
            'sentiment_trend': sentiment_trend,
            'platforms': list(set(m.get('platform', 'unknown') for m in mentions))
        }
    
    def _calculate_risk_tolerance(self, pre_activity: Dict) -> float:
        """Calculate risk tolerance score (0-1)"""
        
        leverage_trend = pre_activity.get('leverage_trend', 0)
        risk_escalation = pre_activity.get('risk_escalation', 0)
        avg_position_size = pre_activity.get('avg_position_size', 0)
        
        # Higher leverage trend + risk escalation + larger positions = higher risk tolerance
        risk_score = (
            max(0, min(1, leverage_trend * 10)) * 0.4 +
            max(0, min(1, risk_escalation)) * 0.3 +
            max(0, min(1, avg_position_size / 100000)) * 0.3
        )
        
        return risk_score
    
    def _calculate_recovery_speed(self, post_activity: Dict) -> float:
        """Calculate recovery speed score (0-1)"""
        
        return_time = post_activity.get('return_time')
        if return_time is None:
            return 0.0
        
        # Faster return = higher recovery speed
        # 0 hours = 1.0, 24 hours = 0.5, 168 hours (1 week) = 0.0
        recovery_score = max(0, 1 - (return_time / 168))
        
        return recovery_score
    
    def _calculate_platform_loyalty(self, cross_platform: Dict) -> float:
        """Calculate platform loyalty score (0-1)"""
        
        platform_diversity = cross_platform.get('platform_diversity', 0)
        migration_pattern = cross_platform.get('migration_pattern', 'none')
        
        # Lower diversity + no migration = higher loyalty
        diversity_penalty = min(1, platform_diversity / 3)  # Penalty for using many platforms
        migration_penalty = 0.5 if migration_pattern == 'frequent' else 0
        
        loyalty_score = max(0, 1 - diversity_penalty - migration_penalty)
        
        return loyalty_score
    
    def _calculate_trading_consistency(self, pre_activity: Dict) -> float:
        """Calculate trading consistency score (0-1)"""
        
        trading_frequency = pre_activity.get('trading_frequency', 0)
        win_rate = pre_activity.get('win_rate', 0)
        
        # Consistent trading frequency + decent win rate = higher consistency
        frequency_score = min(1, trading_frequency / 5)  # Normalize to daily trading
        win_rate_score = win_rate
        
        consistency_score = (frequency_score * 0.6 + win_rate_score * 0.4)
        
        return consistency_score
    
    def _detect_risk_escalation(self, trades: List[Dict]) -> float:
        """Detect if trader was escalating risk before liquidation"""
        
        if len(trades) < 3:
            return 0.0
        
        # Look for increasing leverage and position sizes
        leverages = [t['leverage'] for t in trades[-5:]]  # Last 5 trades
        sizes = [t['size'] for t in trades[-5:]]
        
        leverage_trend = np.polyfit(range(len(leverages)), leverages, 1)[0] if len(leverages) > 1 else 0
        size_trend = np.polyfit(range(len(sizes)), sizes, 1)[0] if len(sizes) > 1 else 0
        
        # Risk escalation = positive trends in both leverage and size
        escalation_score = max(0, leverage_trend * size_trend)
        
        return min(1, escalation_score)
    
    def _calculate_win_rate(self, trades: List[Dict]) -> float:
        """Calculate win rate from trade data"""
        
        if not trades:
            return 0.0
        
        profitable_trades = sum(1 for t in trades if t.get('pnl', 0) > 0)
        return profitable_trades / len(trades)
    
    def _detect_migration_pattern(self, platforms: Dict) -> str:
        """Detect platform migration pattern"""
        
        if len(platforms) <= 1:
            return 'none'
        
        # Simple heuristic: if activity is spread across platforms, it's frequent migration
        total_activity = sum(p['activity_count'] for p in platforms.values())
        max_platform_activity = max(p['activity_count'] for p in platforms.values())
        
        if max_platform_activity / total_activity < 0.7:
            return 'frequent'
        else:
            return 'occasional'
    
    def _calculate_sentiment_trend(self, mentions: List[Dict]) -> str:
        """Calculate sentiment trend over time"""
        
        if len(mentions) < 2:
            return 'neutral'
        
        # Sort by timestamp and calculate trend
        sorted_mentions = sorted(mentions, key=lambda x: x.get('timestamp', 0))
        sentiments = [m.get('sentiment', 0) for m in sorted_mentions]
        
        trend = np.polyfit(range(len(sentiments)), sentiments, 1)[0]
        
        if trend > 0.1:
            return 'improving'
        elif trend < -0.1:
            return 'deteriorating'
        else:
            return 'stable'


class BehavioralPatternDetector:
    """Detects behavioral patterns from liquidation fingerprints"""
    
    def __init__(self):
        self.patterns = {}
        self.pattern_history = deque(maxlen=1000)
        
    def detect_patterns(self, fingerprints: List[LiquidationFingerprint]) -> List[BehavioralPattern]:
        """Detect behavioral patterns from fingerprints"""
        
        patterns = []
        
        # Pattern 1: High Recovery Speed + High Risk Tolerance = Alpha Traders
        alpha_pattern = self._detect_alpha_trader_pattern(fingerprints)
        if alpha_pattern:
            patterns.append(alpha_pattern)
        
        # Pattern 2: Platform Loyalty + Conservative Shift = Reliable Returnees  
        retention_pattern = self._detect_retention_pattern(fingerprints)
        if retention_pattern:
            patterns.append(retention_pattern)
        
        # Pattern 3: Cross-Platform Activity + High Trading Consistency = Arbitrageurs
        arbitrage_pattern = self._detect_arbitrage_pattern(fingerprints)
        if arbitrage_pattern:
            patterns.append(arbitrage_pattern)
        
        # Pattern 4: Social Sentiment + Recovery Speed = Market Sentiment Leaders
        sentiment_pattern = self._detect_sentiment_leader_pattern(fingerprints)
        if sentiment_pattern:
            patterns.append(sentiment_pattern)
        
        return patterns
    
    def _detect_alpha_trader_pattern(self, fingerprints: List[LiquidationFingerprint]) -> Optional[BehavioralPattern]:
        """Detect traders likely to generate alpha post-liquidation"""
        
        # Criteria: High recovery speed + High risk tolerance + Good trading consistency
        alpha_candidates = [
            f for f in fingerprints 
            if f.recovery_speed > 0.7 and f.risk_tolerance > 0.6 and f.trading_consistency > 0.5
        ]
        
        if len(alpha_candidates) < 5:
            return None
        
        # Calculate alpha potential
        avg_recovery = np.mean([f.recovery_speed for f in alpha_candidates])
        avg_risk = np.mean([f.risk_tolerance for f in alpha_candidates])
        avg_consistency = np.mean([f.trading_consistency for f in alpha_candidates])
        
        alpha_potential = (avg_recovery * 0.4 + avg_risk * 0.3 + avg_consistency * 0.3)
        
        return BehavioralPattern(
            pattern_id="alpha_traders",
            pattern_type="profitability",
            confidence=len(alpha_candidates) / len(fingerprints),
            alpha_potential=alpha_potential,
            sample_size=len(alpha_candidates),
            pattern_data={
                'criteria': 'high_recovery_speed + high_risk_tolerance + good_consistency',
                'avg_recovery_speed': avg_recovery,
                'avg_risk_tolerance': avg_risk,
                'avg_trading_consistency': avg_consistency,
                'wallets': [f.wallet_address for f in alpha_candidates]
            }
        )
    
    def _detect_retention_pattern(self, fingerprints: List[LiquidationFingerprint]) -> Optional[BehavioralPattern]:
        """Detect traders likely to return and stay"""
        
        # Criteria: High platform loyalty + Conservative shift + Decent recovery speed
        retention_candidates = [
            f for f in fingerprints 
            if f.platform_loyalty > 0.7 and f.post_liquidation_activity.get('conservative_shift', 0) > 0.1 and f.recovery_speed > 0.3
        ]
        
        if len(retention_candidates) < 5:
            return None
        
        avg_loyalty = np.mean([f.platform_loyalty for f in retention_candidates])
        avg_conservative_shift = np.mean([f.post_liquidation_activity.get('conservative_shift', 0) for f in retention_candidates])
        avg_recovery = np.mean([f.recovery_speed for f in retention_candidates])
        
        retention_potential = (avg_loyalty * 0.5 + avg_conservative_shift * 0.3 + avg_recovery * 0.2)
        
        return BehavioralPattern(
            pattern_id="retention_candidates",
            pattern_type="retention",
            confidence=len(retention_candidates) / len(fingerprints),
            alpha_potential=retention_potential,
            sample_size=len(retention_candidates),
            pattern_data={
                'criteria': 'high_loyalty + conservative_shift + decent_recovery',
                'avg_platform_loyalty': avg_loyalty,
                'avg_conservative_shift': avg_conservative_shift,
                'avg_recovery_speed': avg_recovery,
                'wallets': [f.wallet_address for f in retention_candidates]
            }
        )
    
    def _detect_arbitrage_pattern(self, fingerprints: List[LiquidationFingerprint]) -> Optional[BehavioralPattern]:
        """Detect traders likely to arbitrage across platforms"""
        
        # Criteria: High platform diversity + High trading consistency + Low platform loyalty
        arbitrage_candidates = [
            f for f in fingerprints 
            if f.cross_platform_activity.get('platform_diversity', 0) > 2 and 
               f.trading_consistency > 0.6 and 
               f.platform_loyalty < 0.5
        ]
        
        if len(arbitrage_candidates) < 3:
            return None
        
        avg_diversity = np.mean([f.cross_platform_activity.get('platform_diversity', 0) for f in arbitrage_candidates])
        avg_consistency = np.mean([f.trading_consistency for f in arbitrage_candidates])
        avg_loyalty = np.mean([f.platform_loyalty for f in arbitrage_candidates])
        
        arbitrage_potential = (avg_diversity * 0.4 + avg_consistency * 0.4 + (1 - avg_loyalty) * 0.2)
        
        return BehavioralPattern(
            pattern_id="arbitrage_traders",
            pattern_type="migration",
            confidence=len(arbitrage_candidates) / len(fingerprints),
            alpha_potential=arbitrage_potential,
            sample_size=len(arbitrage_candidates),
            pattern_data={
                'criteria': 'high_diversity + high_consistency + low_loyalty',
                'avg_platform_diversity': avg_diversity,
                'avg_trading_consistency': avg_consistency,
                'avg_platform_loyalty': avg_loyalty,
                'wallets': [f.wallet_address for f in arbitrage_candidates]
            }
        )
    
    def _detect_sentiment_leader_pattern(self, fingerprints: List[LiquidationFingerprint]) -> Optional[BehavioralPattern]:
        """Detect traders who influence market sentiment"""
        
        # Criteria: High social activity + High recovery speed + Sentiment influence
        sentiment_candidates = [
            f for f in fingerprints 
            if f.social_sentiment.get('mention_count', 0) > 5 and 
               f.recovery_speed > 0.5 and
               f.social_sentiment.get('sentiment_score', 0) != 0
        ]
        
        if len(sentiment_candidates) < 3:
            return None
        
        avg_mentions = np.mean([f.social_sentiment.get('mention_count', 0) for f in sentiment_candidates])
        avg_recovery = np.mean([f.recovery_speed for f in sentiment_candidates])
        avg_sentiment = np.mean([f.social_sentiment.get('sentiment_score', 0) for f in sentiment_candidates])
        
        sentiment_potential = (avg_mentions * 0.3 + avg_recovery * 0.4 + abs(avg_sentiment) * 0.3)
        
        return BehavioralPattern(
            pattern_id="sentiment_leaders",
            pattern_type="sentiment",
            confidence=len(sentiment_candidates) / len(fingerprints),
            alpha_potential=sentiment_potential,
            sample_size=len(sentiment_candidates),
            pattern_data={
                'criteria': 'high_social_activity + high_recovery + sentiment_influence',
                'avg_mention_count': avg_mentions,
                'avg_recovery_speed': avg_recovery,
                'avg_sentiment_score': avg_sentiment,
                'wallets': [f.wallet_address for f in sentiment_candidates]
            }
        )


class BehavioralLiquidityMiner:
    """Main engine for mining behavioral liquidity"""
    
    def __init__(self, db_path: str = "data/behavioral_liquidity.db"):
        self.db_path = db_path
        self.feature_extractor = BehavioralFeatureExtractor()
        self.pattern_detector = BehavioralPatternDetector()
        self.init_database()
        
        logger.info(f"{FRY_BLUE}{BOLD}🧠 Behavioral Liquidity Miner Initialized{RESET}")
        logger.info("Mining trading alpha from trader psychology patterns")
    
    def init_database(self):
        """Initialize database for behavioral pattern storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Behavioral patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS behavioral_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT NOT NULL,
                pattern_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                alpha_potential REAL NOT NULL,
                sample_size INTEGER NOT NULL,
                pattern_data TEXT NOT NULL,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        """)
        
        # Liquidation fingerprints table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS liquidation_fingerprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_address TEXT NOT NULL,
                liquidation_timestamp INTEGER NOT NULL,
                liquidation_size REAL NOT NULL,
                asset TEXT NOT NULL,
                leverage REAL NOT NULL,
                risk_tolerance REAL NOT NULL,
                recovery_speed REAL NOT NULL,
                platform_loyalty REAL NOT NULL,
                trading_consistency REAL NOT NULL,
                behavioral_data TEXT NOT NULL,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Behavioral database initialized: {self.db_path}")
    
    def mine_behavioral_patterns(self, wallet_data_list: List[Dict]) -> List[BehavioralPattern]:
        """Mine behavioral patterns from wallet data"""
        
        logger.info(f"{FRY_YELLOW}Mining behavioral patterns from {len(wallet_data_list)} wallets...{RESET}")
        
        # Extract fingerprints
        fingerprints = []
        for wallet_data in wallet_data_list:
            try:
                fingerprint = self.feature_extractor.extract_liquidation_fingerprint(wallet_data)
                fingerprints.append(fingerprint)
                self._store_fingerprint(fingerprint)
            except Exception as e:
                logger.warning(f"Failed to extract fingerprint: {e}")
        
        logger.info(f"✅ Extracted {len(fingerprints)} behavioral fingerprints")
        
        # Detect patterns
        patterns = self.pattern_detector.detect_patterns(fingerprints)
        
        # Store patterns
        for pattern in patterns:
            self._store_pattern(pattern)
        
        logger.info(f"✅ Detected {len(patterns)} behavioral patterns")
        
        return patterns
    
    def _store_fingerprint(self, fingerprint: LiquidationFingerprint):
        """Store fingerprint in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO liquidation_fingerprints 
            (wallet_address, liquidation_timestamp, liquidation_size, asset, leverage,
             risk_tolerance, recovery_speed, platform_loyalty, trading_consistency, behavioral_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fingerprint.wallet_address,
            fingerprint.liquidation_timestamp,
            fingerprint.liquidation_size,
            fingerprint.asset,
            fingerprint.leverage,
            fingerprint.risk_tolerance,
            fingerprint.recovery_speed,
            fingerprint.platform_loyalty,
            fingerprint.trading_consistency,
            json.dumps({
                'pre_liquidation': fingerprint.pre_liquidation_activity,
                'post_liquidation': fingerprint.post_liquidation_activity,
                'cross_platform': fingerprint.cross_platform_activity,
                'social_sentiment': fingerprint.social_sentiment
            })
        ))
        
        conn.commit()
        conn.close()
    
    def _store_pattern(self, pattern: BehavioralPattern):
        """Store pattern in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO behavioral_patterns 
            (pattern_id, pattern_type, confidence, alpha_potential, sample_size, pattern_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            pattern.pattern_id,
            pattern.pattern_type,
            pattern.confidence,
            pattern.alpha_potential,
            pattern.sample_size,
            json.dumps(pattern.pattern_data)
        ))
        
        conn.commit()
        conn.close()
    
    def get_pattern_summary(self) -> Dict:
        """Get summary of detected behavioral patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT pattern_type, COUNT(*), AVG(alpha_potential), AVG(confidence)
            FROM behavioral_patterns
            GROUP BY pattern_type
        """)
        
        patterns = cursor.fetchall()
        conn.close()
        
        summary = {}
        for pattern_type, count, avg_alpha, avg_confidence in patterns:
            summary[pattern_type] = {
                'count': count,
                'avg_alpha_potential': avg_alpha,
                'avg_confidence': avg_confidence
            }
        
        return summary
    
    def generate_alpha_signals(self, patterns: List[BehavioralPattern]) -> Dict:
        """Generate trading alpha signals from behavioral patterns"""
        
        signals = {
            'alpha_traders': [],
            'retention_targets': [],
            'arbitrage_opportunities': [],
            'sentiment_leaders': []
        }
        
        for pattern in patterns:
            if pattern.pattern_type == 'profitability':
                signals['alpha_traders'].extend(pattern.pattern_data.get('wallets', []))
            elif pattern.pattern_type == 'retention':
                signals['retention_targets'].extend(pattern.pattern_data.get('wallets', []))
            elif pattern.pattern_type == 'migration':
                signals['arbitrage_opportunities'].extend(pattern.pattern_data.get('wallets', []))
            elif pattern.pattern_type == 'sentiment':
                signals['sentiment_leaders'].extend(pattern.pattern_data.get('wallets', []))
        
        return signals


def demo_behavioral_liquidity_mining():
    """Demonstrate behavioral liquidity mining"""
    
    print(f"\n{FRY_BLUE}{BOLD}{'='*80}{RESET}")
    print(f"{FRY_BLUE}{BOLD}Behavioral Liquidity Mining Engine - Demo{RESET}")
    print(f"{FRY_BLUE}{BOLD}{'='*80}{RESET}\n")
    
    # Initialize miner
    miner = BehavioralLiquidityMiner()
    
    # Generate sample wallet data
    sample_wallets = generate_sample_wallet_data()
    
    print(f"{BOLD}Sample Wallet Data Generated:{RESET}")
    print(f"  Total wallets: {len(sample_wallets)}")
    print(f"  Liquidation events: {sum(1 for w in sample_wallets if 'liquidation' in w)}")
    print()
    
    # Mine behavioral patterns
    patterns = miner.mine_behavioral_patterns(sample_wallets)
    
    print(f"{BOLD}Detected Behavioral Patterns:{RESET}")
    print("-" * 80)
    
    for pattern in patterns:
        print(f"\n{FRY_GREEN}Pattern: {pattern.pattern_id.upper()}{RESET}")
        print(f"  Type: {pattern.pattern_type}")
        print(f"  Confidence: {pattern.confidence:.1%}")
        print(f"  Alpha Potential: {pattern.alpha_potential:.2f}")
        print(f"  Sample Size: {pattern.sample_size}")
        print(f"  Criteria: {pattern.pattern_data.get('criteria', 'N/A')}")
    
    # Generate alpha signals
    signals = miner.generate_alpha_signals(patterns)
    
    print(f"\n{BOLD}Generated Alpha Signals:{RESET}")
    print("-" * 80)
    
    for signal_type, wallets in signals.items():
        if wallets:
            print(f"  {signal_type}: {len(wallets)} wallets")
            print(f"    Sample: {wallets[:3]}")
    
    # Pattern summary
    summary = miner.get_pattern_summary()
    
    print(f"\n{BOLD}Pattern Summary:{RESET}")
    print("-" * 80)
    
    for pattern_type, data in summary.items():
        print(f"  {pattern_type}:")
        print(f"    Count: {data['count']}")
        print(f"    Avg Alpha: {data['avg_alpha_potential']:.2f}")
        print(f"    Avg Confidence: {data['avg_confidence']:.1%}")
    
    print(f"\n{FRY_BLUE}{BOLD}{'='*80}{RESET}")
    print(f"{FRY_YELLOW}💡 Behavioral Liquidity Mining transforms trader psychology into trading alpha{RESET}")
    print(f"{FRY_YELLOW}   Same infrastructure serves retention + profitability prediction{RESET}")
    print(f"{FRY_BLUE}{BOLD}{'='*80}{RESET}\n")


def generate_sample_wallet_data() -> List[Dict]:
    """Generate sample wallet data for demonstration"""
    
    np.random.seed(42)
    wallets = []
    
    for i in range(50):
        # Generate liquidation event
        liquidation = {
            'wallet': f"0x{'%040x' % np.random.randint(0, 2**63)}",
            'timestamp': int(time.time()) - np.random.randint(0, 30*24*3600),
            'size': np.random.uniform(1000, 100000),
            'asset': np.random.choice(['BTC', 'ETH', 'SOL']),
            'leverage': np.random.uniform(2, 20),
            'time_to_liquidation': np.random.randint(1, 168)  # Hours
        }
        
        # Generate pre-liquidation trades
        num_pre_trades = np.random.randint(3, 20)
        pre_trades = []
        for j in range(num_pre_trades):
            pre_trades.append({
                'timestamp': liquidation['timestamp'] - np.random.randint(3600, 7*24*3600),
                'size': np.random.uniform(1000, 50000),
                'leverage': np.random.uniform(1, liquidation['leverage']),
                'pnl': np.random.uniform(-10000, 15000)
            })
        
        # Generate post-liquidation trades
        num_post_trades = np.random.randint(0, 10)
        post_trades = []
        for j in range(num_post_trades):
            post_trades.append({
                'timestamp': liquidation['timestamp'] + np.random.randint(3600, 14*24*3600),
                'size': np.random.uniform(500, 20000),
                'leverage': np.random.uniform(1, liquidation['leverage'] * 0.7),
                'pnl': np.random.uniform(-5000, 8000)
            })
        
        # Generate platform activity
        platforms = ['hyperliquid', 'dydx', 'gmx', 'vertex']
        platform_activity = {}
        for platform in np.random.choice(platforms, size=np.random.randint(1, 4), replace=False):
            platform_activity[platform] = {
                'activity_count': np.random.randint(1, 20),
                'total_volume': np.random.uniform(10000, 100000)
            }
        
        # Generate social activity
        social_activity = {
            'mentions': [
                {
                    'platform': np.random.choice(['twitter', 'discord', 'telegram']),
                    'sentiment': np.random.uniform(-1, 1),
                    'timestamp': liquidation['timestamp'] + np.random.randint(0, 7*24*3600)
                }
                for _ in range(np.random.randint(0, 10))
            ]
        }
        
        wallet_data = {
            'liquidation': liquidation,
            'pre_liquidation_trades': pre_trades,
            'post_liquidation_trades': post_trades,
            'platform_activity': platform_activity,
            'social_activity': social_activity
        }
        
        wallets.append(wallet_data)
    
    return wallets


if __name__ == "__main__":
    demo_behavioral_liquidity_mining()
