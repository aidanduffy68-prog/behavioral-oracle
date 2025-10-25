#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Personal FRY Dark Pool Miner
Real-time loss detection and FRY token minting for a single wallet
Converts your trading losses into Frictional-Rekt-Yield tokens
"""

import json
import time
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PersonalFRYMiner:
    """
    Personal FRY token miner that monitors your wallet for losses and mints FRY accordingly
    """
    
    def __init__(self, wallet_address: str, hyperliquid_api_key: Optional[str] = None):
        self.wallet_address = wallet_address
        self.api_key = hyperliquid_api_key
        self.base_url = "https://api.hyperliquid.xyz"
        
        # FRY minting parameters
        self.total_fry_minted = 0.0
        self.total_losses_absorbed = 0.0
        self.loss_history = []
        self.fry_balance = 0.0
        
        # Pain pricing multipliers
        self.base_multiplier = 1.0
        self.volatility_multiplier = 1.5
        self.leverage_multiplier = 2.0
        self.cascade_multiplier = 3.0
        
        logger.info("Personal FRY Miner initialized for wallet: {}...".format(wallet_address[:8]))
    
    def calculate_fry_multiplier(self, loss_amount: float, leverage: float, 
                                position_size: float, is_liquidation: bool = False) -> float:
        """
        Calculate FRY minting multiplier based on pain characteristics
        """
        multiplier = self.base_multiplier
        
        # Leverage pain multiplier (higher leverage = more FRY)
        if leverage > 10:
            multiplier += (leverage / 10) * 0.1
        
        # Position size multiplier (bigger losses = exponential FRY)
        if position_size > 1000:
            multiplier += (position_size / 1000) * 0.05
        
        # Liquidation bonus (getting rekt = extra FRY)
        if is_liquidation:
            multiplier *= self.cascade_multiplier
        
        # Volatility bonus (rapid losses = more FRY)
        recent_losses = [l for l in self.loss_history if 
                        (datetime.now() - l['timestamp']).seconds < 3600]  # Last hour
        if len(recent_losses) > 3:
            multiplier *= self.volatility_multiplier
        
        return min(multiplier, 10.0)  # Cap at 10x multiplier
    
    def mint_fry_tokens(self, loss_amount: float, leverage: float = 1.0, 
                       position_size: float = 0.0, asset: str = "BTC", 
                       is_liquidation: bool = False) -> Dict:
        """
        Mint FRY tokens based on trading loss with pain pricing
        """
        # Calculate FRY multiplier based on pain characteristics
        multiplier = self.calculate_fry_multiplier(loss_amount, leverage, position_size, is_liquidation)
        
        # Mint FRY tokens (1 USD loss = base FRY * multiplier)
        fry_minted = loss_amount * multiplier
        
        # Create loss record with anonymized hash
        loss_hash = hashlib.sha256("{}_{}_{}".format(
            self.wallet_address, time.time(), loss_amount
        ).encode()).hexdigest()[:16]
        
        loss_record = {
            "timestamp": datetime.now(),
            "loss_hash": loss_hash,
            "loss_amount_usd": loss_amount,
            "asset": asset,
            "leverage": leverage,
            "position_size_usd": position_size,
            "is_liquidation": is_liquidation,
            "pain_multiplier": multiplier,
            "fry_minted": fry_minted
        }
        
        # Update totals
        self.total_fry_minted += fry_minted
        self.total_losses_absorbed += loss_amount
        self.fry_balance += fry_minted
        self.loss_history.append(loss_record)
        
        logger.info("FRY MINTED: {:.2f} FRY from ${:.2f} loss ({}x multiplier)".format(
            fry_minted, loss_amount, multiplier))
        
        return loss_record
    
    async def fetch_wallet_positions(self) -> List[Dict]:
        """
        Fetch current positions from Hyperliquid API
        """
        try:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            # Get user state
            payload = {
                "type": "clearinghouseState",
                "user": self.wallet_address
            }
            
            response = requests.post(f"{self.base_url}/info", json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('assetPositions', [])
            else:
                logger.warning("Failed to fetch positions: {}".format(response.status_code))
                return []
                
        except Exception as e:
            logger.error("Error fetching positions: {}".format(str(e)))
            return []
    
    async def fetch_recent_fills(self) -> List[Dict]:
        """
        Fetch recent trade fills to detect losses
        """
        try:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            payload = {
                "type": "userFills",
                "user": self.wallet_address
            }
            
            response = requests.post(f"{self.base_url}/info", json=payload, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning("Failed to fetch fills: {}".format(response.status_code))
                return []
                
        except Exception as e:
            logger.error("Error fetching fills: {}".format(str(e)))
            return []
    
    def detect_losses_from_fills(self, fills: List[Dict]) -> List[Dict]:
        """
        Analyze fills to detect realized losses
        """
        losses = []
        
        for fill in fills:
            try:
                # Check if this is a losing trade
                pnl = float(fill.get('closedPnl', 0))
                if pnl < 0:  # Negative PnL = loss
                    loss_amount = abs(pnl)
                    
                    # Extract trade details
                    asset = fill.get('coin', 'UNKNOWN')
                    size = float(fill.get('sz', 0))
                    price = float(fill.get('px', 0))
                    position_size = size * price
                    
                    # Estimate leverage (simplified)
                    leverage = fill.get('leverage', 1.0)
                    if isinstance(leverage, str):
                        leverage = float(leverage.replace('x', ''))
                    
                    # Check if this was a liquidation
                    is_liquidation = fill.get('liquidation', False) or 'liq' in fill.get('side', '').lower()
                    
                    losses.append({
                        'loss_amount': loss_amount,
                        'asset': asset,
                        'leverage': leverage,
                        'position_size': position_size,
                        'is_liquidation': is_liquidation,
                        'fill_time': fill.get('time', time.time())
                    })
                    
            except (ValueError, KeyError) as e:
                logger.warning("Error parsing fill: {}".format(str(e)))
                continue
        
        return losses
    
    async def monitor_wallet_losses(self, check_interval: int = 30):
        """
        Continuously monitor wallet for losses and mint FRY tokens
        """
        logger.info("Starting real-time loss monitoring for wallet {}...".format(self.wallet_address[:8]))
        
        last_check_time = datetime.now() - timedelta(minutes=5)
        
        while True:
            try:
                # Fetch recent fills
                fills = await self.fetch_recent_fills()
                
                # Filter fills since last check
                recent_fills = [f for f in fills if 
                              datetime.fromtimestamp(f.get('time', 0) / 1000) > last_check_time]
                
                if recent_fills:
                    logger.info("Found {} recent fills to analyze".format(len(recent_fills)))
                    
                    # Detect losses
                    losses = self.detect_losses_from_fills(recent_fills)
                    
                    # Mint FRY for each loss
                    for loss in losses:
                        self.mint_fry_tokens(
                            loss_amount=loss['loss_amount'],
                            leverage=loss['leverage'],
                            position_size=loss['position_size'],
                            asset=loss['asset'],
                            is_liquidation=loss['is_liquidation']
                        )
                
                last_check_time = datetime.now()
                
                # Log current status
                if len(self.loss_history) > 0:
                    logger.info("FRY Balance: {:.2f} | Total Losses: ${:.2f} | Loss Events: {}".format(
                        self.fry_balance, self.total_losses_absorbed, len(self.loss_history)))
                
                await asyncio.sleep(check_interval)
                
            except Exception as e:
                logger.error("Error in monitoring loop: {}".format(str(e)))
                await asyncio.sleep(check_interval)
    
    def generate_fry_report(self) -> Dict:
        """
        Generate comprehensive FRY mining report
        """
        if not self.loss_history:
            return {"message": "No losses detected yet - keep trading to generate FRY!"}
        
        # Calculate statistics
        total_liquidations = sum(1 for l in self.loss_history if l['is_liquidation'])
        avg_multiplier = sum(l['pain_multiplier'] for l in self.loss_history) / len(self.loss_history)
        largest_loss = max(self.loss_history, key=lambda x: x['loss_amount_usd'])
        most_fry_event = max(self.loss_history, key=lambda x: x['fry_minted'])
        
        # Asset breakdown
        asset_breakdown = {}
        for loss in self.loss_history:
            asset = loss['asset']
            if asset not in asset_breakdown:
                asset_breakdown[asset] = {'losses': 0, 'fry': 0, 'count': 0}
            asset_breakdown[asset]['losses'] += loss['loss_amount_usd']
            asset_breakdown[asset]['fry'] += loss['fry_minted']
            asset_breakdown[asset]['count'] += 1
        
        report = {
            "wallet_address": "{}...{}".format(self.wallet_address[:6], self.wallet_address[-4:]),
            "total_fry_balance": self.fry_balance,
            "total_losses_absorbed": self.total_losses_absorbed,
            "total_loss_events": len(self.loss_history),
            "total_liquidations": total_liquidations,
            "average_pain_multiplier": avg_multiplier,
            "fry_per_dollar_lost": self.total_fry_minted / self.total_losses_absorbed if self.total_losses_absorbed > 0 else 0,
            "largest_loss": {
                "amount": largest_loss['loss_amount_usd'],
                "asset": largest_loss['asset'],
                "fry_generated": largest_loss['fry_minted']
            },
            "most_fry_event": {
                "fry_minted": most_fry_event['fry_minted'],
                "loss_amount": most_fry_event['loss_amount_usd'],
                "multiplier": most_fry_event['pain_multiplier']
            },
            "asset_breakdown": asset_breakdown,
            "recent_activity": self.loss_history[-5:] if len(self.loss_history) >= 5 else self.loss_history
        }
        
        return report
    
    def save_fry_data(self, filename: str = "personal_fry_mining_results.json"):
        """
        Save FRY mining data to file
        """
        data = {
            "wallet_address": self.wallet_address,
            "total_fry_minted": self.total_fry_minted,
            "total_losses_absorbed": self.total_losses_absorbed,
            "fry_balance": self.fry_balance,
            "loss_history": [
                {
                    **loss,
                    "timestamp": loss["timestamp"].isoformat()
                } for loss in self.loss_history
            ],
            "generated_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info("FRY mining data saved to {}".format(filename))

async def main():
    """
    Main function to run personal FRY miner
    """
    # You'll need to replace this with your actual wallet address
    wallet_address = input("Enter your Hyperliquid wallet address: ").strip()
    
    if not wallet_address:
        print("Please provide a valid wallet address")
        return
    
    # Optional: API key for authenticated requests (better rate limits)
    api_key = input("Enter your Hyperliquid API key (optional, press Enter to skip): ").strip()
    if not api_key:
        api_key = None
    
    # Initialize FRY miner
    miner = PersonalFRYMiner(wallet_address, api_key)
    
    print("\n🔥 Personal FRY Dark Pool Miner Started!")
    print("Monitoring wallet for losses and minting FRY tokens...")
    print("Press Ctrl+C to stop and generate report\n")
    
    try:
        # Start monitoring
        await miner.monitor_wallet_losses(check_interval=30)
    except KeyboardInterrupt:
        print("\n\n📊 Generating FRY Mining Report...")
        
        # Generate and display report
        report = miner.generate_fry_report()
        print(json.dumps(report, indent=2, default=str))
        
        # Save data
        miner.save_fry_data()
        
        print("\n🎯 FRY mining session complete!")
        print("Your losses have been converted to FRY tokens with pain-based multipliers.")

if __name__ == "__main__":
    asyncio.run(main())
