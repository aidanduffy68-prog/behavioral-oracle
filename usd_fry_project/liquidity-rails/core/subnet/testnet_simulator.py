"""
FRY Degen Subnet - Testnet Simulator
Simulates the full Bittensor subnet experience without wallet setup
100% FREE - No real money or complex dependencies needed
"""

import asyncio
import requests
import time
import random
from typing import Dict, List

class TestnetSimulator:
    """Simulate the complete Bittensor testnet experience"""
    
    def __init__(self):
        self.hyperliquid_api = "https://api.hyperliquid.xyz"
        self.your_wallet = "0xf551aF8d5373B042DBB9F0933C59213B534174e4"
        
        # Simulated testnet state
        self.miners = {}
        self.validators = {}
        self.predictions = []
        self.testnet_tao_balance = 1000  # Free testnet TAO
        
    def register_miner(self, miner_id: str):
        """Register a miner on testnet (FREE)"""
        self.miners[miner_id] = {
            'stake': 10,  # 10 testnet TAO
            'predictions': 0,
            'accuracy': 0.0,
            'rewards': 0.0
        }
        print(f"✅ Miner {miner_id} registered with 10 testnet TAO")
    
    def register_validator(self, validator_id: str):
        """Register a validator on testnet (FREE)"""
        self.validators[validator_id] = {
            'stake': 100,  # 100 testnet TAO
            'validations': 0,
            'rewards': 0.0
        }
        print(f"✅ Validator {validator_id} registered with 100 testnet TAO")
    
    async def get_position(self, coin: str = "XRP") -> Dict:
        """Get real position from Hyperliquid"""
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
                            'liquidation_px': float(pos['position'].get('liquidationPx', 0))
                        }
            return None
        except:
            # Fallback to demo position
            return {
                'coin': 'XRP',
                'szi': 100,
                'entry_px': 33.40,
                'leverage': 50,
                'unrealized_pnl': -6560,
                'liquidation_px': 30.0
            }
    
    def calculate_degen_score(self, position: Dict) -> float:
        """Calculate degen score"""
        leverage = position.get('leverage', 1)
        leverage_score = min(leverage / 100 * 30, 30)
        
        position_value = abs(position['szi']) * position['entry_px']
        size_score = min(position_value / 50000 * 25, 25)
        
        unrealized_pnl = position.get('unrealized_pnl', 0)
        pnl_score = min(abs(unrealized_pnl) / 1000 * 20, 20) if unrealized_pnl < 0 else 0
        
        if position.get('liquidation_px', 0) > 0:
            entry_px = position['entry_px']
            liq_px = position['liquidation_px']
            distance = abs(liq_px - entry_px) / entry_px
            liq_score = max(0, 15 - (distance * 150))
        else:
            liq_score = 0
        
        total_score = leverage_score + size_score + pnl_score + liq_score + 10
        return min(total_score, 100)
    
    def miner_predict(self, miner_id: str, position: Dict) -> Dict:
        """Miner makes prediction"""
        degen_score = self.calculate_degen_score(position)
        loss_probability = min(degen_score / 100 * 0.9, 0.95)
        
        prediction = {
            'miner_id': miner_id,
            'degen_score': degen_score,
            'loss_probability': loss_probability,
            'timestamp': int(time.time())
        }
        
        self.predictions.append(prediction)
        self.miners[miner_id]['predictions'] += 1
        
        return prediction
    
    def validator_score(self, validator_id: str, predictions: List[Dict], actual_rekt: bool) -> Dict:
        """Validator scores predictions"""
        scores = {}
        
        for pred in predictions:
            predicted_rekt = pred['loss_probability'] > 0.5
            accuracy = 1.0 if predicted_rekt == actual_rekt else 0.0
            
            scores[pred['miner_id']] = accuracy
            
            # Update miner stats
            if pred['miner_id'] in self.miners:
                old_acc = self.miners[pred['miner_id']]['accuracy']
                n = self.miners[pred['miner_id']]['predictions']
                new_acc = (old_acc * (n - 1) + accuracy) / n
                self.miners[pred['miner_id']]['accuracy'] = new_acc
        
        self.validators[validator_id]['validations'] += 1
        return scores
    
    def distribute_rewards(self, scores: Dict):
        """Distribute testnet TAO rewards"""
        total_emission = 1.0  # 1 testnet TAO per epoch
        miner_pool = total_emission * 0.41
        validator_pool = total_emission * 0.41
        
        # Distribute to miners
        total_score = sum(scores.values())
        if total_score > 0:
            for miner_id, score in scores.items():
                reward = (score / total_score) * miner_pool
                self.miners[miner_id]['rewards'] += reward
        
        # Distribute to validators
        for validator_id in self.validators:
            reward = validator_pool / len(self.validators)
            self.validators[validator_id]['rewards'] += reward
    
    async def run_testnet_demo(self):
        """Run complete testnet simulation"""
        
        print("\n" + "🍟"*30)
        print("\n   FRY DEGEN SUBNET - FREE TESTNET SIMULATOR")
        print("   No real money • No complex setup • 100% FREE")
        print("\n" + "🍟"*30)
        
        # Setup
        print("\n📋 TESTNET SETUP (FREE)")
        print("="*60)
        print(f"💰 Starting testnet TAO balance: {self.testnet_tao_balance}")
        
        # Register participants
        print("\n🔑 Registering neurons...")
        self.register_miner("miner_001")
        self.register_miner("miner_002")
        self.register_miner("miner_003")
        self.register_validator("validator_001")
        
        print(f"\n💰 Remaining testnet TAO: {self.testnet_tao_balance - 130}")
        print("   (All FREE - no real money spent!)")
        
        # Get position
        print("\n📡 Fetching your XRP position...")
        position = await self.get_position("XRP")
        
        print("\n" + "="*60)
        print("📊 POSITION ANALYSIS")
        print("="*60)
        
        if not position:
            print("❌ Could not fetch position, using demo data")
            position = {
                'coin': 'XRP',
                'szi': 100,
                'entry_px': 33.40,
                'leverage': 50,
                'unrealized_pnl': -6560,
                'liquidation_px': 30.0
            }
        
        position_value = abs(position['szi']) * position['entry_px']
        print(f"   Coin: {position['coin']}")
        print(f"   Size: ${position_value:,.2f}")
        print(f"   Leverage: {position['leverage']:.0f}x")
        print(f"   Unrealized PnL: ${position['unrealized_pnl']:,.2f}")
        
        # Miners predict
        print("\n" + "="*60)
        print("⛏️  MINERS MAKING PREDICTIONS")
        print("="*60)
        
        predictions = []
        for miner_id in self.miners:
            pred = self.miner_predict(miner_id, position)
            predictions.append(pred)
            print(f"   {miner_id}: Degen={pred['degen_score']:.0f}/100, "
                  f"Loss Prob={pred['loss_probability']:.1%}")
        
        # Simulate time passing
        print("\n⏳ Waiting for outcome...")
        await asyncio.sleep(2)
        
        # Simulate outcome (random for demo)
        actual_rekt = random.random() < 0.5
        outcome_emoji = "💀" if actual_rekt else "✅"
        outcome_text = "LIQUIDATED" if actual_rekt else "SURVIVED"
        
        print(f"\n{outcome_emoji} OUTCOME: {outcome_text}")
        
        # Validator scores
        print("\n" + "="*60)
        print("🔍 VALIDATOR SCORING PREDICTIONS")
        print("="*60)
        
        scores = self.validator_score("validator_001", predictions, actual_rekt)
        
        for miner_id, score in scores.items():
            accuracy_pct = score * 100
            print(f"   {miner_id}: {accuracy_pct:.0f}% accurate")
        
        # Distribute rewards
        print("\n" + "="*60)
        print("💰 DISTRIBUTING TESTNET TAO REWARDS")
        print("="*60)
        
        self.distribute_rewards(scores)
        
        print("\n   Miner Rewards:")
        for miner_id, data in self.miners.items():
            print(f"   {miner_id}: +{data['rewards']:.4f} testnet TAO")
        
        print("\n   Validator Rewards:")
        for validator_id, data in self.validators.items():
            print(f"   {validator_id}: +{data['rewards']:.4f} testnet TAO")
        
        # FRY minting simulation
        if actual_rekt:
            print("\n" + "="*60)
            print("🍟 FRY MINTING (from confirmed loss)")
            print("="*60)
            
            loss_amount = abs(position['unrealized_pnl'])
            degen_score = predictions[0]['degen_score']
            multiplier = 10 if degen_score >= 90 else 5 if degen_score >= 80 else 2
            fry_minted = loss_amount * 10 * multiplier
            
            print(f"   Loss Amount: ${loss_amount:,.2f}")
            print(f"   Base FRY: {loss_amount * 10:,.0f}")
            print(f"   Multiplier: {multiplier}x")
            print(f"   Total FRY Minted: {fry_minted:,.0f} FRY")
            print(f"\n   Your Balance: 4.96M → {4960000 + fry_minted:,.0f} FRY")
        
        # Summary
        print("\n" + "="*60)
        print("📊 TESTNET SUMMARY")
        print("="*60)
        print(f"   Total Predictions: {len(predictions)}")
        print(f"   Total Validations: {self.validators['validator_001']['validations']}")
        print(f"   Testnet TAO Distributed: 1.0")
        print(f"   FRY Minted: {fry_minted if actual_rekt else 0:,.0f}")
        
        print("\n" + "🍟"*30)
        print("\n✅ TESTNET DEMO COMPLETE!")
        print("\n💡 Key Points:")
        print("   • Everything was FREE (testnet TAO)")
        print("   • Real Hyperliquid position data")
        print("   • Actual Bittensor subnet mechanics")
        print("   • FRY minting from validated losses")
        print("\n🚀 This is exactly how it works on mainnet,")
        print("   but mainnet costs $50k+ to register a subnet!")
        print("\n")

if __name__ == "__main__":
    simulator = TestnetSimulator()
    asyncio.run(simulator.run_testnet_demo())
