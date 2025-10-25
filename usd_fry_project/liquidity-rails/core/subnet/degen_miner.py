"""
FRY Degen Subnet - Miner Implementation
Scans markets for degenerate trades and submits predictions to validators
"""

import asyncio
import time
import requests
from typing import Dict, List, Optional
import numpy as np
from dataclasses import dataclass
import hashlib

from degen_subnet_core import DegenPrediction, subnet, TradeOutcome

class HyperliquidScanner:
    """Scan Hyperliquid for degen trading opportunities"""
    
    def __init__(self, api_url: str = "https://api.hyperliquid.xyz"):
        self.api_url = api_url
        
    async def get_open_positions(self, user_address: str) -> List[Dict]:
        """Fetch user's open positions"""
        try:
            response = requests.post(
                f"{self.api_url}/info",
                json={
                    "type": "clearinghouseState",
                    "user": user_address
                }
            )
            data = response.json()
            
            positions = []
            if "assetPositions" in data:
                for pos in data["assetPositions"]:
                    if "position" in pos:
                        positions.append({
                            'coin': pos['position']['coin'],
                            'szi': float(pos['position']['szi']),
                            'entry_px': float(pos['position']['entryPx']),
                            'leverage': float(pos['position'].get('leverage', {}).get('value', 1)),
                            'unrealized_pnl': float(pos['position'].get('unrealizedPnl', 0)),
                            'liquidation_px': float(pos['position'].get('liquidationPx', 0))
                        })
            
            return positions
        except Exception as e:
            print(f"Error fetching positions: {e}")
            return []
    
    async def get_funding_rates(self) -> Dict[str, float]:
        """Get current funding rates"""
        try:
            response = requests.post(
                f"{self.api_url}/info",
                json={"type": "metaAndAssetCtxs"}
            )
            data = response.json()
            
            funding_rates = {}
            if isinstance(data, list) and len(data) > 1:
                for ctx in data[1]:
                    if 'coin' in ctx and 'funding' in ctx:
                        funding_rates[ctx['coin']] = float(ctx['funding'])
            
            return funding_rates
        except Exception as e:
            print(f"Error fetching funding rates: {e}")
            return {}
    
    async def get_market_volatility(self, coin: str) -> float:
        """Calculate recent volatility for a coin"""
        try:
            response = requests.post(
                f"{self.api_url}/info",
                json={
                    "type": "candleSnapshot",
                    "req": {
                        "coin": coin,
                        "interval": "1h",
                        "startTime": int(time.time() * 1000) - 86400000  # 24h ago
                    }
                }
            )
            data = response.json()
            
            if not data:
                return 0.0
            
            # Calculate volatility from price changes
            prices = [float(candle['c']) for candle in data]
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns) * 100  # As percentage
            
            return volatility
        except Exception as e:
            print(f"Error calculating volatility: {e}")
            return 0.0

class DegenMiner:
    """Miner that identifies degen trades and submits predictions"""
    
    def __init__(self, miner_id: str, wallet_address: str):
        self.miner_id = miner_id
        self.wallet_address = wallet_address
        self.scanner = HyperliquidScanner()
        self.monitored_addresses = []
        
    async def register(self, stake: float) -> bool:
        """Register as a miner on the subnet"""
        success = subnet.register_miner(self.miner_id, stake)
        if success:
            print(f"✅ Miner {self.miner_id} registered with {stake} FRY stake")
        else:
            print(f"❌ Failed to register miner {self.miner_id}")
        return success
    
    def add_monitored_address(self, address: str):
        """Add a wallet address to monitor"""
        self.monitored_addresses.append(address)
        print(f"👀 Now monitoring: {address}")
    
    async def scan_for_degens(self) -> List[DegenPrediction]:
        """Scan all monitored addresses for degen opportunities"""
        predictions = []
        
        for address in self.monitored_addresses:
            positions = await self.scanner.get_open_positions(address)
            
            for pos in positions:
                degen_score = await self.calculate_degen_score(pos)
                
                # Only predict on high degen scores (>60)
                if degen_score > 60:
                    prediction = await self.create_prediction(address, pos, degen_score)
                    predictions.append(prediction)
        
        return predictions
    
    async def calculate_degen_score(self, position: Dict) -> float:
        """Calculate 0-100 degen score for a position"""
        
        # Leverage factor (max 30 points)
        leverage = position.get('leverage', 1)
        leverage_score = min(leverage / 100 * 30, 30)
        
        # Position size factor (max 25 points)
        # Assume positions >$10k are large
        position_value = abs(position['szi']) * position['entry_px']
        size_score = min(position_value / 50000 * 25, 25)
        
        # Volatility factor (max 20 points)
        volatility = await self.scanner.get_market_volatility(position['coin'])
        vol_score = min(volatility / 10 * 20, 20)
        
        # Unrealized PnL factor (max 15 points)
        # Deep underwater = higher degen score
        unrealized_pnl = position.get('unrealized_pnl', 0)
        if unrealized_pnl < 0:
            pnl_score = min(abs(unrealized_pnl) / 1000 * 15, 15)
        else:
            pnl_score = 0
        
        # Funding rate factor (max 10 points)
        funding_rates = await self.scanner.get_funding_rates()
        funding = abs(funding_rates.get(position['coin'], 0))
        funding_score = min(funding * 10000, 10)  # Funding is small decimal
        
        total_score = leverage_score + size_score + vol_score + pnl_score + funding_score
        return min(total_score, 100)
    
    async def create_prediction(self, trader_address: str, position: Dict, degen_score: float) -> DegenPrediction:
        """Create a prediction for a degen position"""
        
        # Predict loss probability based on degen score
        loss_probability = degen_score / 100 * 0.9  # Max 90% loss probability
        
        # Estimate time to liquidation
        if position.get('liquidation_px', 0) > 0:
            entry_px = position['entry_px']
            liq_px = position['liquidation_px']
            distance_to_liq = abs(liq_px - entry_px) / entry_px
            
            # Higher volatility = faster liquidation
            volatility = await self.scanner.get_market_volatility(position['coin'])
            estimated_hours = distance_to_liq / (volatility / 100) if volatility > 0 else 24
            rekt_timeline = int(estimated_hours * 3600)  # Convert to seconds
        else:
            rekt_timeline = 86400  # Default 24 hours
        
        # Create trade ID
        trade_id = f"{trader_address}_{position['coin']}_{int(time.time())}"
        
        # Sign prediction
        signature = self._sign_prediction(trade_id, degen_score)
        
        return DegenPrediction(
            trade_id=trade_id,
            miner_id=self.miner_id,
            degen_score=degen_score,
            predicted_loss_probability=loss_probability,
            predicted_rekt_timeline=rekt_timeline,
            leverage=position.get('leverage', 1),
            position_size=abs(position['szi']) * position['entry_px'],
            volatility=await self.scanner.get_market_volatility(position['coin']),
            liquidity_score=50.0,  # TODO: Calculate actual liquidity
            fomo_factor=degen_score / 100,
            timestamp=int(time.time()),
            signature=signature
        )
    
    def _sign_prediction(self, trade_id: str, degen_score: float) -> str:
        """Sign a prediction (simplified)"""
        data = f"{self.miner_id}{trade_id}{degen_score}{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    async def submit_prediction(self, prediction: DegenPrediction) -> bool:
        """Submit prediction to subnet"""
        success = subnet.submit_prediction(prediction)
        
        if success:
            print(f"📤 Submitted prediction: {prediction.trade_id[:16]}... "
                  f"(degen: {prediction.degen_score:.0f}, "
                  f"loss prob: {prediction.predicted_loss_probability:.1%})")
        else:
            print(f"❌ Failed to submit prediction: {prediction.trade_id[:16]}...")
        
        return success
    
    async def mine_loop(self, interval: int = 60):
        """Main mining loop"""
        print(f"⛏️  Miner {self.miner_id} started mining...")
        print(f"   Monitoring {len(self.monitored_addresses)} addresses")
        print(f"   Scan interval: {interval}s")
        
        while True:
            try:
                # Scan for degen trades
                predictions = await self.scan_for_degens()
                
                # Submit predictions
                for prediction in predictions:
                    await self.submit_prediction(prediction)
                
                if predictions:
                    print(f"✅ Submitted {len(predictions)} predictions")
                else:
                    print(f"🔍 No degen trades found (score >60)")
                
                # Wait for next scan
                await asyncio.sleep(interval)
                
            except Exception as e:
                print(f"❌ Mining error: {e}")
                await asyncio.sleep(interval)

# Example usage
async def main():
    # Create miner
    miner = DegenMiner(
        miner_id="miner_001",
        wallet_address="0xYourWalletHere"
    )
    
    # Register with 1000 FRY stake
    await miner.register(stake=1000)
    
    # Add addresses to monitor
    miner.add_monitored_address("0xf551aF8d5373B042DBB9F0933C59213B534174e4")  # Your wallet
    
    # Start mining
    await miner.mine_loop(interval=30)  # Scan every 30 seconds

if __name__ == "__main__":
    asyncio.run(main())
