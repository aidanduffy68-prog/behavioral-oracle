#!/usr/bin/env python3
"""
Agent B Testnet Runner
Connects to Hyperliquid testnet and processes real wreckage
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List
import requests
from web3 import Web3

class HyperliquidTestnetClient:
    """Client for Hyperliquid testnet API"""
    
    def __init__(self):
        self.base_url = "https://api.hyperliquid-testnet.xyz"
        self.session = requests.Session()
    
    def get_funding_rates(self) -> List[Dict]:
        """Get current funding rates for all markets"""
        try:
            response = self.session.post(f"{self.base_url}/info", json={
                "type": "metaAndAssetCtxs"
            })
            data = response.json()
            
            funding_rates = []
            
            # Handle different API response structures
            if isinstance(data, list) and len(data) > 1:
                contexts = data[1]
            else:
                contexts = data.get("assetCtxs", [])
            
            for ctx in contexts:
                asset_name = ctx.get("coin") or ctx.get("name") or "UNKNOWN"
                funding_rates.append({
                    "asset": asset_name,
                    "funding_rate": float(ctx.get("funding", 0)),
                    "open_interest": float(ctx.get("openInterest", 0)),
                    "mark_price": float(ctx.get("markPx", 0))
                })
            
            return funding_rates
        except Exception as e:
            print(f"Error parsing funding rates: {e}")
            return []
    
    def get_recent_liquidations(self, lookback_hours: int = 1) -> List[Dict]:
        """Get recent liquidation events"""
        response = self.session.post(f"{self.base_url}/info", json={
            "type": "userFills",
            "user": "0x0000000000000000000000000000000000000000"  # Public liquidations
        })
        
        # Parse liquidations
        liquidations = []
        # Note: Hyperliquid API structure may vary
        # Adjust based on actual response
        
        return liquidations
    
    def get_market_data(self, asset: str) -> Dict:
        """Get market data for specific asset"""
        response = self.session.post(f"{self.base_url}/info", json={
            "type": "l2Book",
            "coin": asset
        })
        return response.json()


class AgentBTestnet:
    """Agent B running on testnet with real data"""
    
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Initialize Hyperliquid client
        self.hl_client = HyperliquidTestnetClient()
        
        # Initialize Web3 for contract interaction
        self.w3 = Web3(Web3.HTTPProvider(
            self.config.get("rpc_url", "https://sepolia-rollup.arbitrum.io/rpc")
        ))
        
        # Load contract ABIs and addresses
        self.contracts = self._load_contracts()
        
        # Performance tracking
        self.stats = {
            "wreckage_processed": 0,
            "fry_minted": 0,
            "trades_executed": 0,
            "slippage_harvested": 0,
            "start_time": datetime.now()
        }
    
    def _load_contracts(self) -> Dict:
        """Load deployed contract instances"""
        contracts = {}
        
        # Load deployment.json
        try:
            with open('../../contracts/deployment.json') as f:
                deployment = json.load(f)
            
            # Load ABIs (simplified - you'd load from artifacts)
            contracts['token'] = deployment['contracts']['USDFRYToken']
            contracts['router'] = deployment['contracts']['LiquidityRailsRouter']
            contracts['matching'] = deployment['contracts']['WreckageMatchingPool']
            
        except FileNotFoundError:
            print("⚠️  No deployment.json found. Deploy contracts first!")
            print("   Run: cd ../../contracts && npm run deploy:testnet")
        
        return contracts
    
    async def monitor_funding_rates(self):
        """Monitor funding rates and identify wreckage opportunities"""
        print("\n📊 Monitoring Hyperliquid testnet funding rates...")
        
        while True:
            try:
                rates = self.hl_client.get_funding_rates()
                
                # Identify high funding rate positions (potential wreckage)
                high_funding = [r for r in rates if abs(r['funding_rate']) > 0.01]
                
                if high_funding:
                    print(f"\n🔥 High funding detected:")
                    for rate in high_funding[:3]:
                        print(f"   {rate['asset']}: {rate['funding_rate']*100:.3f}% "
                              f"(OI: ${rate['open_interest']:,.0f})")
                        
                        # Simulate wreckage from funding payments
                        wreckage_amount = rate['open_interest'] * abs(rate['funding_rate']) * 0.1
                        if wreckage_amount > 100:  # Minimum threshold
                            await self.process_wreckage({
                                "type": "funding_loss",
                                "asset": rate['asset'],
                                "amount_usd": wreckage_amount,
                                "dex": "Hyperliquid",
                                "stablecoin": "USDH"
                            })
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"❌ Error monitoring funding: {e}")
                await asyncio.sleep(60)
    
    async def process_wreckage(self, wreckage: Dict):
        """Process wreckage event and mint FRY"""
        print(f"\n🍟 Processing wreckage: ${wreckage['amount_usd']:.2f}")
        
        # Calculate FRY minting
        base_rate = 1.2  # Liquidity rails rate
        usdh_bonus = 1.5  # Native stablecoin bonus
        fry_minted = wreckage['amount_usd'] * base_rate * usdh_bonus
        
        print(f"   FRY to mint: {fry_minted:.2f}")
        print(f"   Effective rate: {fry_minted/wreckage['amount_usd']:.2f} FRY/$1")
        
        # Update stats
        self.stats['wreckage_processed'] += wreckage['amount_usd']
        self.stats['fry_minted'] += fry_minted
        self.stats['trades_executed'] += 1
        
        # TODO: Actually call smart contract to mint
        # This requires gas and a funded wallet
        # For now, just simulate
        
        return {
            "success": True,
            "fry_minted": fry_minted,
            "tx_hash": "0x" + "0" * 64  # Simulated
        }
    
    def print_stats(self):
        """Print current performance stats"""
        runtime = (datetime.now() - self.stats['start_time']).total_seconds() / 3600
        
        print("\n" + "="*70)
        print("📊 AGENT B TESTNET STATS")
        print("="*70)
        print(f"Runtime:              {runtime:.2f} hours")
        print(f"Wreckage Processed:   ${self.stats['wreckage_processed']:,.2f}")
        print(f"FRY Minted:           {self.stats['fry_minted']:,.2f}")
        print(f"Trades Executed:      {self.stats['trades_executed']}")
        print(f"Avg Minting Rate:     {self.stats['fry_minted']/max(self.stats['wreckage_processed'],1):.2f} FRY/$1")
        print("="*70 + "\n")
    
    async def run(self):
        """Main event loop"""
        print("\n🚀 Agent B Testnet Starting...")
        print(f"   Network: {self.config.get('network', 'arbitrum-sepolia')}")
        print(f"   DEX: Hyperliquid Testnet")
        print(f"   Capital: ${self.config['capital']['initial_usdc']:,}")
        
        # Start monitoring
        try:
            while True:
                await self.monitor_funding_rates()
                
                # Print stats every 10 minutes
                if int(time.time()) % 600 == 0:
                    self.print_stats()
                    
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping Agent B...")
            self.print_stats()
            print("✅ Testnet run complete!\n")


async def main():
    """Entry point"""
    import sys
    
    config_path = sys.argv[1] if len(sys.argv) > 1 else "testnet_config.json"
    
    agent = AgentBTestnet(config_path)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
