"""
FRY Degen Subnet - Validator Implementation
Validates trade outcomes and scores miner predictions
"""

import asyncio
import time
import requests
from typing import Dict, List, Optional
import hashlib

from degen_subnet_core import TradeOutcomeData, TradeOutcome, subnet

class HyperliquidValidator:
    """Validate trade outcomes from Hyperliquid"""
    
    def __init__(self, api_url: str = "https://api.hyperliquid.xyz"):
        self.api_url = api_url
        
    async def check_position_status(self, user_address: str, coin: str) -> Optional[Dict]:
        """Check if a position still exists or was liquidated"""
        try:
            response = requests.post(
                f"{self.api_url}/info",
                json={
                    "type": "clearinghouseState",
                    "user": user_address
                }
            )
            data = response.json()
            
            # Look for the specific position
            if "assetPositions" in data:
                for pos in data["assetPositions"]:
                    if "position" in pos and pos['position']['coin'] == coin:
                        return {
                            'exists': True,
                            'szi': float(pos['position']['szi']),
                            'unrealized_pnl': float(pos['position'].get('unrealizedPnl', 0)),
                            'liquidation_px': float(pos['position'].get('liquidationPx', 0))
                        }
            
            # Position doesn't exist anymore
            return {'exists': False}
            
        except Exception as e:
            print(f"Error checking position: {e}")
            return None
    
    async def get_user_fills(self, user_address: str) -> List[Dict]:
        """Get recent fills/trades for a user"""
        try:
            response = requests.post(
                f"{self.api_url}/info",
                json={
                    "type": "userFills",
                    "user": user_address
                }
            )
            return response.json() or []
        except Exception as e:
            print(f"Error fetching fills: {e}")
            return []
    
    async def detect_liquidation(self, user_address: str, coin: str, since_timestamp: int) -> Optional[Dict]:
        """Detect if a liquidation occurred"""
        fills = await self.get_user_fills(user_address)
        
        for fill in fills:
            if (fill.get('coin') == coin and 
                fill.get('time', 0) > since_timestamp and
                fill.get('liquidation', False)):
                
                return {
                    'liquidated': True,
                    'liquidation_time': fill['time'],
                    'liquidation_px': float(fill['px']),
                    'loss_amount': abs(float(fill.get('closedPnl', 0)))
                }
        
        return None

class DegenValidator:
    """Validator that verifies trade outcomes and scores miners"""
    
    def __init__(self, validator_id: str, wallet_address: str):
        self.validator_id = validator_id
        self.wallet_address = wallet_address
        self.hyperliquid = HyperliquidValidator()
        self.tracked_predictions = {}  # trade_id -> prediction data
        
    async def register(self, stake: float) -> bool:
        """Register as a validator on the subnet"""
        success = subnet.register_validator(self.validator_id, stake)
        if success:
            print(f"✅ Validator {self.validator_id} registered with {stake} FRY stake")
        else:
            print(f"❌ Failed to register validator {self.validator_id}")
        return success
    
    def track_prediction(self, trade_id: str, prediction_data: Dict):
        """Start tracking a prediction for validation"""
        self.tracked_predictions[trade_id] = {
            **prediction_data,
            'tracking_started': int(time.time())
        }
        print(f"👁️  Tracking prediction: {trade_id[:16]}...")
    
    async def validate_outcome(self, trade_id: str) -> Optional[TradeOutcomeData]:
        """Validate the actual outcome of a trade"""
        
        if trade_id not in self.tracked_predictions:
            print(f"⚠️  Trade {trade_id} not being tracked")
            return None
        
        pred_data = self.tracked_predictions[trade_id]
        
        # Extract trader address and coin from trade_id
        # Format: {address}_{coin}_{timestamp}
        parts = trade_id.split('_')
        if len(parts) < 3:
            return None
        
        trader_address = parts[0]
        coin = parts[1]
        pred_timestamp = int(parts[2])
        
        # Check for liquidation
        liquidation = await self.hyperliquid.detect_liquidation(
            trader_address, 
            coin, 
            pred_timestamp
        )
        
        if liquidation and liquidation['liquidated']:
            # Position was liquidated = REKT
            outcome = TradeOutcomeData(
                trade_id=trade_id,
                outcome=TradeOutcome.REKT,
                loss_amount=liquidation['loss_amount'],
                liquidation_time=liquidation['liquidation_time'],
                final_pnl=-liquidation['loss_amount'],
                timestamp=int(time.time())
            )
            print(f"💀 REKT confirmed: {trade_id[:16]}... (${liquidation['loss_amount']:.2f} loss)")
            return outcome
        
        # Check if position still exists
        position = await self.hyperliquid.check_position_status(trader_address, coin)
        
        if position and position['exists']:
            # Position still open, check if it's winning
            unrealized_pnl = position['unrealized_pnl']
            
            # Check if enough time has passed
            time_elapsed = int(time.time()) - pred_timestamp
            
            if time_elapsed > 86400:  # 24 hours passed
                if unrealized_pnl > 1000:  # Significant profit
                    outcome = TradeOutcomeData(
                        trade_id=trade_id,
                        outcome=TradeOutcome.MOON,
                        loss_amount=0,
                        liquidation_time=None,
                        final_pnl=unrealized_pnl,
                        timestamp=int(time.time())
                    )
                    print(f"🚀 MOON confirmed: {trade_id[:16]}... (${unrealized_pnl:.2f} profit)")
                    return outcome
                else:
                    outcome = TradeOutcomeData(
                        trade_id=trade_id,
                        outcome=TradeOutcome.SURVIVED,
                        loss_amount=0,
                        liquidation_time=None,
                        final_pnl=unrealized_pnl,
                        timestamp=int(time.time())
                    )
                    print(f"😅 SURVIVED: {trade_id[:16]}... (${unrealized_pnl:.2f} PnL)")
                    return outcome
        else:
            # Position closed, check fills for final PnL
            fills = await self.hyperliquid.get_user_fills(trader_address)
            
            for fill in fills:
                if (fill.get('coin') == coin and 
                    fill.get('time', 0) > pred_timestamp and
                    'closedPnl' in fill):
                    
                    final_pnl = float(fill['closedPnl'])
                    
                    if final_pnl < -100:  # Significant loss
                        outcome = TradeOutcomeData(
                            trade_id=trade_id,
                            outcome=TradeOutcome.REKT,
                            loss_amount=abs(final_pnl),
                            liquidation_time=fill['time'],
                            final_pnl=final_pnl,
                            timestamp=int(time.time())
                        )
                        print(f"💀 REKT (closed): {trade_id[:16]}... (${abs(final_pnl):.2f} loss)")
                        return outcome
                    elif final_pnl > 100:  # Significant profit
                        outcome = TradeOutcomeData(
                            trade_id=trade_id,
                            outcome=TradeOutcome.MOON,
                            loss_amount=0,
                            liquidation_time=None,
                            final_pnl=final_pnl,
                            timestamp=int(time.time())
                        )
                        print(f"🚀 MOON (closed): {trade_id[:16]}... (${final_pnl:.2f} profit)")
                        return outcome
        
        return None  # Not ready to validate yet
    
    async def submit_outcome(self, outcome: TradeOutcomeData) -> bool:
        """Submit validated outcome to subnet"""
        success = subnet.submit_outcome(outcome)
        
        if success:
            print(f"✅ Outcome submitted: {outcome.trade_id[:16]}... ({outcome.outcome.value})")
            
            # Mint FRY if it was a loss (integrate with casino backend)
            if outcome.outcome == TradeOutcome.REKT:
                await self.mint_fry_from_loss(outcome)
        else:
            print(f"❌ Failed to submit outcome: {outcome.trade_id[:16]}...")
        
        return success
    
    async def mint_fry_from_loss(self, outcome: TradeOutcomeData):
        """Mint FRY tokens from confirmed loss (integrate with casino backend)"""
        try:
            # Call the FRY FastAPI backend to mint tokens
            response = requests.post(
                "http://localhost:8000/mirror",
                json={
                    "pnl": -outcome.loss_amount,  # Negative for loss
                    "symbol": "SUBNET",
                    "trade_type": "subnet_validated"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                fry_minted = data['balance_update']['fry_change']
                print(f"🍟 Minted {fry_minted:.0f} FRY from validated loss")
            else:
                print(f"⚠️  Failed to mint FRY: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error minting FRY: {e}")
    
    async def validation_loop(self, interval: int = 60):
        """Main validation loop"""
        print(f"🔍 Validator {self.validator_id} started validating...")
        print(f"   Validation interval: {interval}s")
        
        while True:
            try:
                # Check all tracked predictions
                for trade_id in list(self.tracked_predictions.keys()):
                    outcome = await self.validate_outcome(trade_id)
                    
                    if outcome:
                        await self.submit_outcome(outcome)
                        # Remove from tracking once validated
                        del self.tracked_predictions[trade_id]
                
                # Get subnet stats
                stats = subnet.get_subnet_stats()
                print(f"\n📊 Subnet Stats:")
                print(f"   Predictions: {stats['total_predictions']}")
                print(f"   Outcomes: {stats['total_outcomes']}")
                print(f"   Accuracy: {stats['accuracy_rate']:.1%}")
                print(f"   Tracking: {len(self.tracked_predictions)} predictions\n")
                
                # Wait for next validation cycle
                await asyncio.sleep(interval)
                
            except Exception as e:
                print(f"❌ Validation error: {e}")
                await asyncio.sleep(interval)

# Example usage
async def main():
    # Create validator
    validator = DegenValidator(
        validator_id="validator_001",
        wallet_address="0xYourValidatorWallet"
    )
    
    # Register with 10000 FRY stake (10x miner requirement)
    await validator.register(stake=10000)
    
    # In production, this would listen to subnet for new predictions
    # For now, manually track predictions
    
    # Start validation loop
    await validator.validation_loop(interval=30)

if __name__ == "__main__":
    asyncio.run(main())
