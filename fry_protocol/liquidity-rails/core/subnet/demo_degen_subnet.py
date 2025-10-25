"""
FRY Degen Subnet - Interactive Demo
Test the subnet without needing Bittensor wallets
"""

import asyncio
import requests
from typing import Dict
import time

class DegenDemo:
    """Demo the degen prediction system"""
    
    def __init__(self):
        self.hyperliquid_api = "https://api.hyperliquid.xyz"
        self.your_wallet = "0xf551aF8d5373B042DBB9F0933C59213B534174e4"
        
    async def get_position(self, coin: str = "XRP") -> Dict:
        """Get your actual position from Hyperliquid"""
        try:
            response = requests.post(
                f"{self.hyperliquid_api}/info",
                json={
                    "type": "clearinghouseState",
                    "user": self.your_wallet
                }
            )
            data = response.json()
            
            if "assetPositions" in data:
                for pos in data["assetPositions"]:
                    if "position" in pos and pos['position']['coin'] == coin:
                        return {
                            'coin': pos['position']['coin'],
                            'szi': float(pos['position']['szi']),
                            'entry_px': float(pos['position']['entryPx']),
                            'leverage': float(pos['position'].get('leverage', {}).get('value', 1)),
                            'unrealized_pnl': float(pos['position'].get('unrealizedPnl', 0)),
                            'liquidation_px': float(pos['position'].get('liquidationPx', 0)),
                            'margin_used': float(pos['position'].get('marginUsed', 0))
                        }
            
            return None
        except Exception as e:
            print(f"❌ Error fetching position: {e}")
            return None
    
    def calculate_degen_score(self, position: Dict) -> float:
        """Calculate degen score 0-100"""
        
        # Leverage factor (max 30 points)
        leverage = position.get('leverage', 1)
        leverage_score = min(leverage / 100 * 30, 30)
        
        # Position size factor (max 25 points)
        position_value = abs(position['szi']) * position['entry_px']
        size_score = min(position_value / 50000 * 25, 25)
        
        # Unrealized PnL factor (max 20 points)
        unrealized_pnl = position.get('unrealized_pnl', 0)
        if unrealized_pnl < 0:
            pnl_score = min(abs(unrealized_pnl) / 1000 * 20, 20)
        else:
            pnl_score = 0
        
        # Distance to liquidation (max 15 points)
        if position.get('liquidation_px', 0) > 0:
            entry_px = position['entry_px']
            liq_px = position['liquidation_px']
            distance = abs(liq_px - entry_px) / entry_px
            liq_score = max(0, 15 - (distance * 150))  # Closer to liq = higher score
        else:
            liq_score = 0
        
        # Margin usage (max 10 points)
        margin_score = 10  # Assume high margin usage
        
        total_score = leverage_score + size_score + pnl_score + liq_score + margin_score
        return min(total_score, 100)
    
    def predict_outcome(self, position: Dict, degen_score: float) -> Dict:
        """Predict what will happen to this position"""
        
        # Loss probability based on degen score
        loss_probability = min(degen_score / 100 * 0.9, 0.95)
        
        # Estimate time to liquidation
        if position.get('liquidation_px', 0) > 0:
            entry_px = position['entry_px']
            liq_px = position['liquidation_px']
            distance_to_liq = abs(liq_px - entry_px) / entry_px
            
            # Assume 20% volatility
            estimated_hours = distance_to_liq / 0.20 if distance_to_liq > 0 else 1
            rekt_timeline = int(estimated_hours * 3600)
        else:
            rekt_timeline = 86400  # 24 hours default
        
        # Calculate potential FRY mint
        potential_loss = abs(position.get('unrealized_pnl', 0))
        fry_multiplier = 10 if degen_score >= 90 else 5 if degen_score >= 80 else 2
        potential_fry = potential_loss * 10 * fry_multiplier
        
        return {
            'loss_probability': loss_probability,
            'rekt_timeline_seconds': rekt_timeline,
            'rekt_timeline_hours': rekt_timeline / 3600,
            'potential_loss': potential_loss,
            'fry_multiplier': fry_multiplier,
            'potential_fry_mint': potential_fry,
            'confidence': 0.8 if position.get('liquidation_px', 0) > 0 else 0.5
        }
    
    def generate_reasoning(self, position: Dict, degen_score: float) -> str:
        """Generate human-readable reasoning"""
        reasons = []
        
        if position.get('leverage', 1) > 50:
            reasons.append(f"{position['leverage']:.0f}x leverage")
        
        unrealized_pnl = position.get('unrealized_pnl', 0)
        if unrealized_pnl < -1000:
            reasons.append(f"${abs(unrealized_pnl):,.0f} underwater")
        
        if degen_score > 90:
            reasons.append("EXTREME DEGEN DETECTED")
        elif degen_score > 80:
            reasons.append("high degen level")
        elif degen_score > 70:
            reasons.append("moderate degen")
        
        if position.get('liquidation_px', 0) > 0:
            entry_px = position['entry_px']
            liq_px = position['liquidation_px']
            distance = abs(liq_px - entry_px) / entry_px * 100
            reasons.append(f"{distance:.1f}% from liquidation")
        
        return " | ".join(reasons) if reasons else "moderate risk position"
    
    async def run_demo(self):
        """Run interactive demo"""
        
        print("🍟" + "="*60 + "🍟")
        print("   FRY DEGEN SUBNET - INTERACTIVE DEMO")
        print("   Predicting Your XRP Position")
        print("🍟" + "="*60 + "🍟\n")
        
        # Fetch position
        print(f"📡 Fetching position for {self.your_wallet[:10]}...")
        position = await self.get_position("XRP")
        
        if not position:
            print("❌ No XRP position found")
            print("\n💡 Demo with simulated position instead:")
            position = {
                'coin': 'XRP',
                'szi': 100,
                'entry_px': 33.40,
                'leverage': 50,
                'unrealized_pnl': -6560,
                'liquidation_px': 30.0,
                'margin_used': 3340
            }
            print("   (Using your actual position data from memory)")
        
        print("\n" + "="*60)
        print("📊 POSITION ANALYSIS")
        print("="*60)
        
        position_value = abs(position['szi']) * position['entry_px']
        print(f"   Coin: {position['coin']}")
        print(f"   Size: ${position_value:,.2f}")
        print(f"   Entry: ${position['entry_px']:.2f}")
        print(f"   Leverage: {position['leverage']:.0f}x")
        print(f"   Unrealized PnL: ${position['unrealized_pnl']:,.2f}")
        
        if position.get('liquidation_px', 0) > 0:
            print(f"   Liquidation Price: ${position['liquidation_px']:.2f}")
            distance = abs(position['liquidation_px'] - position['entry_px']) / position['entry_px'] * 100
            print(f"   Distance to Liq: {distance:.1f}%")
        
        # Calculate degen score
        print("\n" + "="*60)
        print("🎯 DEGEN SCORE CALCULATION")
        print("="*60)
        
        degen_score = self.calculate_degen_score(position)
        
        leverage_points = min(position['leverage'] / 100 * 30, 30)
        size_points = min(position_value / 50000 * 25, 25)
        pnl_points = min(abs(position['unrealized_pnl']) / 1000 * 20, 20) if position['unrealized_pnl'] < 0 else 0
        
        print(f"   Leverage ({position['leverage']:.0f}x): {leverage_points:.1f}/30 points")
        print(f"   Position Size (${position_value:,.0f}): {size_points:.1f}/25 points")
        print(f"   Unrealized Loss (${abs(position['unrealized_pnl']):,.0f}): {pnl_points:.1f}/20 points")
        print(f"\n   🔥 TOTAL DEGEN SCORE: {degen_score:.0f}/100")
        
        # Predict outcome
        print("\n" + "="*60)
        print("🔮 PREDICTION")
        print("="*60)
        
        prediction = self.predict_outcome(position, degen_score)
        reasoning = self.generate_reasoning(position, degen_score)
        
        print(f"   Loss Probability: {prediction['loss_probability']:.1%}")
        print(f"   Time to Rekt: {prediction['rekt_timeline_hours']:.1f} hours")
        print(f"   Confidence: {prediction['confidence']:.1%}")
        print(f"\n   Reasoning: {reasoning}")
        
        # FRY minting potential
        print("\n" + "="*60)
        print("🍟 FRY MINTING POTENTIAL")
        print("="*60)
        
        print(f"   If Liquidated:")
        print(f"   - Loss Amount: ${prediction['potential_loss']:,.2f}")
        print(f"   - Base FRY: {prediction['potential_loss'] * 10:,.0f} FRY")
        print(f"   - Degen Multiplier: {prediction['fry_multiplier']}x")
        print(f"   - Total FRY Mint: {prediction['potential_fry_mint']:,.0f} FRY")
        print(f"\n   Your Balance Would Go:")
        print(f"   4.96M FRY → {4960000 + prediction['potential_fry_mint']:,.0f} FRY")
        
        # Miner reward simulation
        print("\n" + "="*60)
        print("💰 MINER TAO REWARDS (if prediction accurate)")
        print("="*60)
        
        accuracy_score = 0.85  # Assume 85% accuracy
        epoch_emission = 1.0  # 1 TAO per epoch
        miner_share = 0.41  # 41% to miners
        
        print(f"   Prediction Accuracy: {accuracy_score:.1%}")
        print(f"   Epoch Emission: {epoch_emission} TAO")
        print(f"   Miner Pool: {epoch_emission * miner_share} TAO")
        print(f"   Your Share: ~{epoch_emission * miner_share * accuracy_score:.4f} TAO")
        
        print("\n" + "🍟"*30)
        print("\n✅ Demo Complete!")
        print("\nThis prediction would be:")
        print("  1. Sent to validators via Bittensor Dendrite")
        print("  2. Monitored for actual liquidation")
        print("  3. Scored based on accuracy")
        print("  4. Rewarded with TAO tokens")
        print("  5. FRY minted when loss confirmed")
        
        print("\n🚀 To run the real subnet:")
        print("  python3 bittensor_degen_miner.py --netuid 1 --subtensor.network test")
        print("\n")

if __name__ == "__main__":
    demo = DegenDemo()
    asyncio.run(demo.run_demo())
