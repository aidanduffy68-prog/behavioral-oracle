#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrate Behavioral Liquidity Mining with Real Control Group Data
===================================================================

Connects behavioral miner to actual retention data from FRY recipients and control group.
"""

import sqlite3
import json
import time
from datetime import datetime, timedelta
from behavioral_liquidity_miner import BehavioralLiquidityMiner
import os

def load_control_group_data():
    """Load control group data from retention database"""
    db_path = os.path.join(os.path.dirname(__file__), '../../data/retention/fry_retention.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get control group wallets
    cursor.execute("""
        SELECT wallet_address, liquidation_date, liquidation_amount, 
               protocol, returned, days_tracked
        FROM control_group
    """)
    
    control_wallets = cursor.fetchall()
    conn.close()
    
    return control_wallets

def load_fry_recipient_data():
    """Load FRY recipient data from retention database"""
    db_path = os.path.join(os.path.dirname(__file__), '../../data/retention/fry_retention.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if liquidated_traders table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='liquidated_traders'
    """)
    
    if not cursor.fetchone():
        conn.close()
        return []
    
    # Get FRY recipients
    cursor.execute("""
        SELECT wallet_address, liquidation_date, liquidation_amount,
               fry_received_date, last_activity_date
        FROM liquidated_traders
    """)
    
    fry_wallets = cursor.fetchall()
    conn.close()
    
    return fry_wallets

def convert_to_behavioral_format(wallet_data, is_fry_recipient=True):
    """Convert retention data to behavioral miner format"""
    
    if is_fry_recipient:
        wallet_address, liq_date, liq_amount, fry_date, last_activity = wallet_data
        
        # Calculate if returned
        returned = last_activity is not None and last_activity > fry_date
        
        # Calculate return time
        if returned:
            return_time = (datetime.fromisoformat(last_activity) - 
                          datetime.fromisoformat(fry_date)).total_seconds() / 3600
        else:
            return_time = None
            
    else:  # Control group
        wallet_address, liq_date, liq_amount, protocol, returned, days_tracked = wallet_data
        return_time = None  # Control group didn't return
    
    # Convert to behavioral miner format
    liquidation_timestamp = int(datetime.fromisoformat(liq_date).timestamp()) if isinstance(liq_date, str) else int(time.time())
    
    behavioral_data = {
        'liquidation': {
            'wallet': wallet_address,
            'timestamp': liquidation_timestamp,
            'size': float(liq_amount),
            'asset': 'ETH',  # Default, adjust based on actual data
            'leverage': 10.0,  # Default, adjust based on actual data
            'time_to_liquidation': 24  # Default hours
        },
        'pre_liquidation_trades': [
            # Placeholder - would need actual trading history
            {
                'timestamp': liquidation_timestamp - 86400,
                'size': float(liq_amount) * 0.5,
                'leverage': 8.0,
                'pnl': -float(liq_amount) * 0.1
            }
        ],
        'post_liquidation_trades': [],
        'platform_activity': {
            'arbitrum': {
                'activity_count': 1 if returned else 0,
                'total_volume': float(liq_amount) if returned else 0
            }
        },
        'social_activity': {
            'mentions': []
        }
    }
    
    # Add post-liquidation trades if returned
    if returned and return_time:
        behavioral_data['post_liquidation_trades'] = [
            {
                'timestamp': liquidation_timestamp + int(return_time * 3600),
                'size': float(liq_amount) * 0.3,
                'leverage': 5.0,  # Conservative after liquidation
                'pnl': float(liq_amount) * 0.05
            }
        ]
    
    return behavioral_data

def main():
    """Main integration function"""
    
    print("\n" + "="*80)
    print("Integrating Behavioral Liquidity Mining with Real Data")
    print("="*80 + "\n")
    
    # Load real data
    print("Loading control group data...")
    control_wallets = load_control_group_data()
    print(f"  Loaded {len(control_wallets)} control group wallets")
    
    print("Loading FRY recipient data...")
    fry_wallets = load_fry_recipient_data()
    print(f"  Loaded {len(fry_wallets)} FRY recipient wallets")
    
    # Convert to behavioral format
    print("\nConverting to behavioral format...")
    all_behavioral_data = []
    
    for wallet in control_wallets:
        behavioral_data = convert_to_behavioral_format(wallet, is_fry_recipient=False)
        all_behavioral_data.append(behavioral_data)
    
    for wallet in fry_wallets:
        behavioral_data = convert_to_behavioral_format(wallet, is_fry_recipient=True)
        all_behavioral_data.append(behavioral_data)
    
    print(f"  Converted {len(all_behavioral_data)} wallets to behavioral format")
    
    # Initialize behavioral miner
    print("\nInitializing Behavioral Liquidity Miner...")
    db_path = os.path.join(os.path.dirname(__file__), '../../data/retention/behavioral_liquidity.db')
    miner = BehavioralLiquidityMiner(db_path=db_path)
    
    # Mine patterns
    print("\nMining behavioral patterns from real data...")
    patterns = miner.mine_behavioral_patterns(all_behavioral_data)
    
    print(f"\nDetected {len(patterns)} behavioral patterns:")
    print("-" * 80)
    
    for pattern in patterns:
        print(f"\nPattern: {pattern.pattern_id.upper()}")
        print(f"  Type: {pattern.pattern_type}")
        print(f"  Confidence: {pattern.confidence:.1%}")
        print(f"  Alpha Potential: {pattern.alpha_potential:.2f}")
        print(f"  Sample Size: {pattern.sample_size}")
        print(f"  Criteria: {pattern.pattern_data.get('criteria', 'N/A')}")
    
    # Generate signals
    signals = miner.generate_alpha_signals(patterns)
    
    print(f"\nGenerated Alpha Signals:")
    print("-" * 80)
    
    for signal_type, wallets in signals.items():
        if wallets:
            print(f"  {signal_type}: {len(wallets)} wallets")
    
    # Get summary
    summary = miner.get_pattern_summary()
    
    print(f"\nPattern Summary:")
    print("-" * 80)
    
    for pattern_type, data in summary.items():
        print(f"  {pattern_type}:")
        print(f"    Count: {data['count']}")
        print(f"    Avg Alpha: {data['avg_alpha_potential']:.2f}")
        print(f"    Avg Confidence: {data['avg_confidence']:.1%}")
    
    print("\n" + "="*80)
    print("Integration Complete")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
