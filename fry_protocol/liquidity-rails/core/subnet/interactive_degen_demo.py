"""
FRY Degen Subnet - Interactive Demo
Choose positions to analyze or run live monitoring
"""

import asyncio
import requests
from typing import Dict, List
import time

class InteractiveDegenDemo:
    """Interactive demo with menu options"""
    
    def __init__(self):
        self.hyperliquid_api = "https://api.hyperliquid.xyz"
        self.your_wallet = "0xf551aF8d5373B042DBB9F0933C59213B534174e4"
        
    async def get_all_positions(self) -> List[Dict]:
        """Get all your positions from Hyperliquid"""
        try:
            response = requests.post(
                f"{self.hyperliquid_api}/info",
                json={
                    "type": "clearinghouseState",
                    "user": self.your_wallet
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
                            'liquidation_px': float(pos['position'].get('liquidationPx', 0)),
                            'margin_used': float(pos['position'].get('marginUsed', 0))
                        })
            
            return positions
        except Exception as e:
            print(f"❌ Error fetching positions: {e}")
            return []
    
    def calculate_degen_score(self, position: Dict) -> float:
        """Calculate degen score 0-100"""
        
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
        
        margin_score = 10
        
        total_score = leverage_score + size_score + pnl_score + liq_score + margin_score
        return min(total_score, 100)
    
    def analyze_position(self, position: Dict):
        """Analyze and display position prediction"""
        
        print("\n" + "="*60)
        print(f"📊 ANALYZING: {position['coin']}")
        print("="*60)
        
        position_value = abs(position['szi']) * position['entry_px']
        print(f"   Size: ${position_value:,.2f}")
        print(f"   Entry: ${position['entry_px']:.2f}")
        print(f"   Leverage: {position['leverage']:.0f}x")
        print(f"   Unrealized PnL: ${position['unrealized_pnl']:,.2f}")
        
        if position.get('liquidation_px', 0) > 0:
            distance = abs(position['liquidation_px'] - position['entry_px']) / position['entry_px'] * 100
            print(f"   Liquidation: ${position['liquidation_px']:.2f} ({distance:.1f}% away)")
        
        # Degen score
        degen_score = self.calculate_degen_score(position)
        print(f"\n   🔥 DEGEN SCORE: {degen_score:.0f}/100")
        
        # Prediction
        loss_probability = min(degen_score / 100 * 0.9, 0.95)
        print(f"   📉 Loss Probability: {loss_probability:.1%}")
        
        # FRY potential
        if position['unrealized_pnl'] < 0:
            potential_loss = abs(position['unrealized_pnl'])
            fry_multiplier = 10 if degen_score >= 90 else 5 if degen_score >= 80 else 2
            potential_fry = potential_loss * 10 * fry_multiplier
            
            print(f"\n   🍟 If Liquidated:")
            print(f"      Loss: ${potential_loss:,.2f}")
            print(f"      FRY Mint: {potential_fry:,.0f} FRY ({fry_multiplier}x multiplier)")
    
    async def live_monitor(self):
        """Live monitoring mode"""
        
        print("\n🔴 LIVE MONITORING MODE")
        print("Checking positions every 30 seconds...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                positions = await self.get_all_positions()
                
                if not positions:
                    print("No positions found")
                else:
                    print(f"\n⏰ {time.strftime('%H:%M:%S')} - Monitoring {len(positions)} positions:")
                    
                    for pos in positions:
                        degen_score = self.calculate_degen_score(pos)
                        pnl_emoji = "📉" if pos['unrealized_pnl'] < 0 else "📈"
                        
                        print(f"   {pnl_emoji} {pos['coin']:8} | "
                              f"Degen: {degen_score:3.0f}/100 | "
                              f"PnL: ${pos['unrealized_pnl']:8,.2f} | "
                              f"Lev: {pos['leverage']:3.0f}x")
                        
                        # Alert if extreme degen
                        if degen_score > 80:
                            print(f"      ⚠️  EXTREME DEGEN ALERT!")
                
                await asyncio.sleep(30)
                
        except KeyboardInterrupt:
            print("\n\n✅ Monitoring stopped")
    
    async def run_interactive(self):
        """Run interactive menu"""
        
        while True:
            print("\n" + "🍟"*30)
            print("\n   FRY DEGEN SUBNET - INTERACTIVE DEMO")
            print("\n" + "🍟"*30)
            
            print("\n📋 MENU:")
            print("   1. Analyze all positions")
            print("   2. Analyze specific coin")
            print("   3. Live monitoring (30s updates)")
            print("   4. Simulate custom position")
            print("   5. Exit")
            
            choice = input("\n👉 Choose option (1-5): ").strip()
            
            if choice == "1":
                positions = await self.get_all_positions()
                if not positions:
                    print("\n❌ No positions found")
                    print("Using demo positions...")
                    positions = [
                        {
                            'coin': 'XRP',
                            'szi': 100,
                            'entry_px': 33.40,
                            'leverage': 50,
                            'unrealized_pnl': -6560,
                            'liquidation_px': 30.0,
                            'margin_used': 3340
                        },
                        {
                            'coin': 'FARTCOIN',
                            'szi': 50,
                            'entry_px': 28.61,
                            'leverage': 40,
                            'unrealized_pnl': -1696,
                            'liquidation_px': 25.0,
                            'margin_used': 1430
                        }
                    ]
                
                for pos in positions:
                    self.analyze_position(pos)
                
                input("\nPress Enter to continue...")
            
            elif choice == "2":
                coin = input("\n👉 Enter coin symbol (e.g., XRP, BTC): ").strip().upper()
                positions = await self.get_all_positions()
                
                found = False
                for pos in positions:
                    if pos['coin'] == coin:
                        self.analyze_position(pos)
                        found = True
                        break
                
                if not found:
                    print(f"\n❌ No {coin} position found")
                
                input("\nPress Enter to continue...")
            
            elif choice == "3":
                await self.live_monitor()
            
            elif choice == "4":
                print("\n📝 CREATE CUSTOM POSITION:")
                coin = input("   Coin: ").strip().upper()
                entry = float(input("   Entry price: $"))
                size = float(input("   Position size: $"))
                leverage = float(input("   Leverage: "))
                pnl = float(input("   Unrealized PnL: $"))
                
                custom_pos = {
                    'coin': coin,
                    'szi': size / entry,
                    'entry_px': entry,
                    'leverage': leverage,
                    'unrealized_pnl': pnl,
                    'liquidation_px': entry * 0.9,  # Estimate
                    'margin_used': size
                }
                
                self.analyze_position(custom_pos)
                input("\nPress Enter to continue...")
            
            elif choice == "5":
                print("\n👋 Thanks for using FRY Degen Subnet!")
                print("🚀 To run the real Bittensor subnet:")
                print("   python3 bittensor_degen_miner.py --netuid 1 --subtensor.network test\n")
                break
            
            else:
                print("\n❌ Invalid choice, try again")

if __name__ == "__main__":
    demo = InteractiveDegenDemo()
    asyncio.run(demo.run_interactive())
