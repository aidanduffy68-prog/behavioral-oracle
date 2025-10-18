#!/usr/bin/env python3
"""
FRY Retention Oracle
Tracks liquidated traders and measures 30-day return rates, LTV, and churn signals.
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3

class FRYRetentionOracle:
    """
    Measures trader retention metrics after liquidations.
    
    Key metrics:
    - 30-day return rate: Did trader come back?
    - Lifetime value (LTV): Volume generated post-liquidation
    - Churn signals: Inactivity, withdrawals, cross-platform moves
    """
    
    def __init__(self, db_path: str = "data/fry_retention.db"):
        self.db_path = db_path
        self.base_url = "https://api.hyperliquid.xyz/info"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for tracking liquidations and activity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Liquidations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS liquidations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_address TEXT NOT NULL,
                liquidation_timestamp INTEGER NOT NULL,
                liquidation_size REAL NOT NULL,
                asset TEXT NOT NULL,
                tracked_until INTEGER,
                returned_30d BOOLEAN,
                ltv_30d REAL,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        """)
        
        # Activity table (tracks post-liquidation trading)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_address TEXT NOT NULL,
                activity_timestamp INTEGER NOT NULL,
                activity_type TEXT NOT NULL,
                volume REAL,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        """)
        
        # Retention metrics table (aggregated stats)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retention_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                calculation_date INTEGER NOT NULL,
                total_liquidations INTEGER NOT NULL,
                returned_30d INTEGER NOT NULL,
                return_rate REAL NOT NULL,
                avg_ltv REAL,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized: {self.db_path}")
    
    def fetch_liquidations(self, start_time: Optional[int] = None, end_time: Optional[int] = None) -> List[Dict]:
        """
        Fetch liquidation events from Hyperliquid API.
        
        Args:
            start_time: Unix timestamp (optional)
            end_time: Unix timestamp (optional)
        
        Returns:
            List of liquidation events
        """
        # Note: Hyperliquid API structure may vary - adjust as needed
        payload = {
            "type": "userFills",
            "user": "0x0000000000000000000000000000000000000000"  # Placeholder - need actual query
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Filter for liquidations
            liquidations = []
            # TODO: Parse actual liquidation events from response
            # This is a placeholder structure
            
            return liquidations
        
        except Exception as e:
            print(f"❌ Error fetching liquidations: {e}")
            return []
    
    def track_liquidation(self, wallet_address: str, liquidation_timestamp: int, 
                         liquidation_size: float, asset: str):
        """
        Add a liquidation event to tracking database.
        
        Args:
            wallet_address: Trader's wallet address
            liquidation_timestamp: Unix timestamp of liquidation
            liquidation_size: USD value of liquidation
            asset: Asset that was liquidated
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already tracked
        cursor.execute("""
            SELECT id FROM liquidations 
            WHERE wallet_address = ? AND liquidation_timestamp = ?
        """, (wallet_address, liquidation_timestamp))
        
        if cursor.fetchone():
            print(f"⚠️  Liquidation already tracked: {wallet_address}")
            conn.close()
            return
        
        # Insert new liquidation
        tracked_until = liquidation_timestamp + (30 * 24 * 60 * 60)  # 30 days
        
        cursor.execute("""
            INSERT INTO liquidations 
            (wallet_address, liquidation_timestamp, liquidation_size, asset, tracked_until)
            VALUES (?, ?, ?, ?, ?)
        """, (wallet_address, liquidation_timestamp, liquidation_size, asset, tracked_until))
        
        conn.commit()
        conn.close()
        print(f"✅ Tracking liquidation: {wallet_address} | ${liquidation_size:,.2f}")
    
    def fetch_wallet_activity(self, wallet_address: str, start_time: int, end_time: int) -> List[Dict]:
        """
        Fetch trading activity for a wallet in a time range.
        
        Args:
            wallet_address: Trader's wallet
            start_time: Unix timestamp
            end_time: Unix timestamp
        
        Returns:
            List of activity events
        """
        payload = {
            "type": "userFills",
            "user": wallet_address
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Filter by time range
            activities = []
            # TODO: Parse actual activity from response
            
            return activities
        
        except Exception as e:
            print(f"❌ Error fetching activity for {wallet_address}: {e}")
            return []
    
    def update_retention_metrics(self):
        """
        Check all tracked liquidations and update 30-day return rates.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = int(time.time())
        
        # Get liquidations that need checking (30 days passed, not yet checked)
        cursor.execute("""
            SELECT id, wallet_address, liquidation_timestamp, liquidation_size
            FROM liquidations
            WHERE tracked_until <= ? AND returned_30d IS NULL
        """, (current_time,))
        
        pending_checks = cursor.fetchall()
        
        print(f"📊 Checking {len(pending_checks)} liquidations for 30-day return...")
        
        for liq_id, wallet, liq_time, liq_size in pending_checks:
            # Check if wallet had any activity in 30 days post-liquidation
            end_time = liq_time + (30 * 24 * 60 * 60)
            
            activities = self.fetch_wallet_activity(wallet, liq_time, end_time)
            
            returned = len(activities) > 0
            ltv = sum(a.get('volume', 0) for a in activities) if activities else 0.0
            
            # Update database
            cursor.execute("""
                UPDATE liquidations
                SET returned_30d = ?, ltv_30d = ?
                WHERE id = ?
            """, (returned, ltv, liq_id))
            
            status = "✅ RETURNED" if returned else "❌ CHURNED"
            print(f"{status} | {wallet[:10]}... | LTV: ${ltv:,.2f}")
            
            # Rate limit API calls
            time.sleep(0.5)
        
        conn.commit()
        
        # Calculate aggregate metrics
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN returned_30d = 1 THEN 1 ELSE 0 END) as returned,
                AVG(CASE WHEN returned_30d = 1 THEN ltv_30d ELSE NULL END) as avg_ltv
            FROM liquidations
            WHERE returned_30d IS NOT NULL
        """)
        
        total, returned, avg_ltv = cursor.fetchone()
        
        if total > 0:
            return_rate = (returned / total) * 100
            
            cursor.execute("""
                INSERT INTO retention_metrics 
                (calculation_date, total_liquidations, returned_30d, return_rate, avg_ltv)
                VALUES (?, ?, ?, ?, ?)
            """, (current_time, total, returned, return_rate, avg_ltv or 0.0))
            
            conn.commit()
            
            print("\n" + "="*60)
            print("📈 RETENTION METRICS")
            print("="*60)
            print(f"Total liquidations tracked: {total}")
            print(f"Returned within 30 days: {returned} ({return_rate:.1f}%)")
            print(f"Average LTV (returned traders): ${avg_ltv:,.2f}" if avg_ltv else "Average LTV: N/A")
            print("="*60)
        
        conn.close()
    
    def get_retention_report(self) -> pd.DataFrame:
        """
        Generate retention report as DataFrame.
        
        Returns:
            DataFrame with retention metrics over time
        """
        conn = sqlite3.connect(self.db_path)
        
        df = pd.read_sql_query("""
            SELECT 
                datetime(calculation_date, 'unixepoch') as date,
                total_liquidations,
                returned_30d,
                return_rate,
                avg_ltv
            FROM retention_metrics
            ORDER BY calculation_date DESC
        """, conn)
        
        conn.close()
        
        return df
    
    def simulate_fry_impact(self, fry_multiplier: float = 2.26) -> Dict:
        """
        Simulate impact of FRY retention incentive.
        
        Args:
            fry_multiplier: Expected retention rate multiplier with FRY
        
        Returns:
            Dict with baseline vs. FRY-enhanced metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get baseline metrics
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN returned_30d = 1 THEN 1 ELSE 0 END) as returned,
                SUM(liquidation_size) as total_liquidated,
                AVG(CASE WHEN returned_30d = 1 THEN ltv_30d ELSE NULL END) as avg_ltv
            FROM liquidations
            WHERE returned_30d IS NOT NULL
        """)
        
        total, returned, total_liquidated, avg_ltv = cursor.fetchone()
        conn.close()
        
        if not total:
            return {"error": "No data available"}
        
        baseline_return_rate = (returned / total) * 100
        fry_return_rate = min(baseline_return_rate * fry_multiplier, 100)
        
        baseline_retained_traders = returned
        fry_retained_traders = int((fry_return_rate / 100) * total)
        
        additional_retained = fry_retained_traders - baseline_retained_traders
        additional_ltv = additional_retained * (avg_ltv or 0)
        
        return {
            "baseline": {
                "return_rate": baseline_return_rate,
                "retained_traders": baseline_retained_traders,
                "total_ltv": baseline_retained_traders * (avg_ltv or 0)
            },
            "with_fry": {
                "return_rate": fry_return_rate,
                "retained_traders": fry_retained_traders,
                "total_ltv": fry_retained_traders * (avg_ltv or 0)
            },
            "improvement": {
                "additional_traders": additional_retained,
                "additional_ltv": additional_ltv,
                "roi_multiplier": fry_multiplier
            }
        }


def main():
    """Main execution."""
    print("="*60)
    print("FRY RETENTION ORACLE")
    print("="*60)
    
    oracle = FRYRetentionOracle()
    
    # Example: Track a liquidation
    # oracle.track_liquidation(
    #     wallet_address="0x1234567890abcdef",
    #     liquidation_timestamp=int(time.time()) - (35 * 24 * 60 * 60),  # 35 days ago
    #     liquidation_size=10000.0,
    #     asset="ETH"
    # )
    
    # Update metrics for all tracked liquidations
    oracle.update_retention_metrics()
    
    # Generate report
    report = oracle.get_retention_report()
    if not report.empty:
        print("\n📊 RETENTION REPORT:")
        print(report.to_string(index=False))
    
    # Simulate FRY impact
    simulation = oracle.simulate_fry_impact()
    if "error" not in simulation:
        print("\n🍟 FRY IMPACT SIMULATION:")
        print(f"Baseline return rate: {simulation['baseline']['return_rate']:.1f}%")
        print(f"With FRY return rate: {simulation['with_fry']['return_rate']:.1f}%")
        print(f"Additional traders retained: {simulation['improvement']['additional_traders']}")
        print(f"Additional LTV: ${simulation['improvement']['additional_ltv']:,.2f}")


if __name__ == "__main__":
    main()
