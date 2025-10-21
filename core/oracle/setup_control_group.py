# -*- coding: utf-8 -*-
"""
Setup control group tracking for retention comparison
Find 10 liquidated wallets that did NOT receive FRY
"""

import sqlite3
from datetime import datetime, timedelta
import json

# Note: Web3 integration commented out for now
# Install with: pip install web3
# from web3 import Web3
# w3 = Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc'))

def find_liquidated_wallets_arbitrum():
    """
    Find recent liquidation events on Arbitrum
    Look for wallets that lost money but didn't receive FRY
    """
    
    # Common perp protocols on Arbitrum
    protocols = {
        'GMX': '0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a',  # GMX Router
        'Gains': '0x6B8D3C08072a020aC065c467ce922e3A36D3F9d6',  # Gains Trading
        # Add more as needed
    }
    
    control_wallets = []
    
    # For now, manually add some example wallets
    # In production, query actual liquidation events
    example_wallets = [
        {
            'wallet_address': '0x1234567890123456789012345678901234567890',
            'liquidation_date': datetime.now() - timedelta(days=10),
            'liquidation_amount': 150.0,
            'protocol': 'GMX',
            'received_fry': False
        }
    ]
    
    return example_wallets

def create_control_group_table():
    """Create database table for control group tracking"""
    import os
    db_path = os.path.join(os.path.dirname(__file__), '../../data/retention/fry_retention.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS control_group (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT UNIQUE NOT NULL,
            liquidation_date TIMESTAMP NOT NULL,
            liquidation_amount REAL NOT NULL,
            protocol TEXT,
            last_activity_date TIMESTAMP,
            returned BOOLEAN DEFAULT 0,
            days_tracked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Control group table created")

def add_control_wallet(wallet_address, liquidation_amount, protocol='Unknown'):
    """Add a wallet to control group tracking"""
    import os
    db_path = os.path.join(os.path.dirname(__file__), '../../data/retention/fry_retention.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    liquidation_date = datetime.now() - timedelta(days=10)  # Adjust as needed
    
    cursor.execute('''
        INSERT OR IGNORE INTO control_group 
        (wallet_address, liquidation_date, liquidation_amount, protocol)
        VALUES (?, ?, ?, ?)
    ''', (wallet_address, liquidation_date, liquidation_amount, protocol))
    
    conn.commit()
    conn.close()
    print("Added control wallet: " + wallet_address[:10] + "...")

def check_control_wallet_activity(wallet_address):
    """
    Check if a control group wallet has returned to trading
    Look for any on-chain activity post-liquidation
    
    TODO: Implement Web3 integration to check actual on-chain activity
    For now, returns False (no activity detected)
    """
    # Placeholder - will implement Web3 checking later
    return False, None

def update_control_group_activity():
    """Check all control group wallets for activity"""
    import os
    db_path = os.path.join(os.path.dirname(__file__), '../../data/retention/fry_retention.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT wallet_address, liquidation_date FROM control_group WHERE returned = 0")
    wallets = cursor.fetchall()
    
    for wallet_address, liquidation_date in wallets:
        returned, activity_date = check_control_wallet_activity(wallet_address)
        
        if returned:
            cursor.execute('''
                UPDATE control_group 
                SET returned = 1, last_activity_date = ?
                WHERE wallet_address = ?
            ''', (activity_date, wallet_address))
            print("Control wallet returned: " + wallet_address[:10] + "...")
        
        # Update days tracked
        days_tracked = (datetime.now() - datetime.fromisoformat(liquidation_date)).days
        cursor.execute('''
            UPDATE control_group 
            SET days_tracked = ?
            WHERE wallet_address = ?
        ''', (days_tracked, wallet_address))
    
    conn.commit()
    conn.close()
    print("Control group activity updated")

def get_control_group_metrics():
    """Get current control group retention metrics"""
    import os
    db_path = os.path.join(os.path.dirname(__file__), '../../data/retention/fry_retention.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM control_group")
    total_wallets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM control_group WHERE returned = 1")
    returned_wallets = cursor.fetchone()[0]
    
    retention_rate = (returned_wallets / total_wallets * 100) if total_wallets > 0 else 0
    
    conn.close()
    
    return {
        'total_wallets': total_wallets,
        'returned_wallets': returned_wallets,
        'retention_rate': round(retention_rate, 1)
    }

if __name__ == "__main__":
    print("Setting up control group tracking...")
    
    # Step 1: Create table
    create_control_group_table()
    
    # Step 2: Add 10 example wallets (replace with real liquidated wallets)
    example_wallets = [
        ('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb', 125.50, 'GMX'),
        ('0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063', 89.30, 'GMX'),
        ('0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', 234.75, 'Gains'),
        ('0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1', 156.20, 'GMX'),
        ('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8', 98.40, 'Gains'),
        ('0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9', 178.90, 'GMX'),
        ('0x82aF49447D8a07e3bd95BD0d56f35241523fBab1', 203.15, 'GMX'),
        ('0xf97f4df75117a78c1A5a0DBb814Af92458539FB4', 145.60, 'Gains'),
        ('0x17FC002b466eEc40DaE837Fc4bE5c67993ddBd6F', 267.80, 'GMX'),
        ('0x912CE59144191C1204E64559FE8253a0e49E6548', 112.35, 'Gains'),
    ]
    
    for wallet, amount, protocol in example_wallets:
        add_control_wallet(wallet, amount, protocol)
    
    print("\nControl group setup complete!")
    print("\nNext steps:")
    print("1. Run this script daily to check wallet activity")
    print("2. Update dashboard with control group comparison")
    print("3. Wait 30 days for full retention data")
