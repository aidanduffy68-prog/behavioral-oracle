"""
FRY Degen Subnet - Bittensor Miner Neuron
Real Bittensor integration for degen trade prediction
"""

import bittensor as bt
import asyncio
import time
import requests
import numpy as np
from typing import Dict, List, Optional
import json

class DegenSynapse(bt.Synapse):
    """Custom synapse for degen trade predictions"""
    
    # Request fields
    trader_address: str
    coin: str
    position_data: Dict
    
    # Response fields
    degen_score: float = 0.0
    predicted_loss_probability: float = 0.0
    predicted_rekt_timeline: int = 0
    confidence: float = 0.0
    reasoning: str = ""

class DegenMiner:
    """Bittensor miner for FRY Degen Subnet"""
    
    def __init__(self, config=None):
        # Initialize Bittensor components
        self.config = config or self.get_config()
        
        # Setup wallet
        self.wallet = bt.wallet(config=self.config)
        self.subtensor = bt.subtensor(config=self.config)
        self.metagraph = self.subtensor.metagraph(self.config.netuid)
        
        # Setup axon (miner server)
        self.axon = bt.axon(wallet=self.wallet, config=self.config)
        
        # Hyperliquid scanner
        self.hyperliquid_api = "https://api.hyperliquid.xyz"
        
        bt.logging.info(f"🍟 FRY Degen Miner initialized")
        bt.logging.info(f"   Wallet: {self.wallet.hotkey.ss58_address}")
        bt.logging.info(f"   Network: {self.config.subtensor.network}")
        bt.logging.info(f"   Netuid: {self.config.netuid}")
    
    @classmethod
    def get_config(cls):
        """Get Bittensor configuration"""
        parser = bt.ArgumentParser()
        parser.add_argument('--netuid', type=int, default=1, help='Subnet netuid')
        parser.add_argument('--subtensor.network', type=str, default='test', help='Bittensor network')
        parser.add_argument('--wallet.name', type=str, default='miner', help='Wallet name')
        parser.add_argument('--wallet.hotkey', type=str, default='default', help='Wallet hotkey')
        parser.add_argument('--axon.port', type=int, default=8091, help='Axon port')
        
        bt.subtensor.add_args(parser)
        bt.wallet.add_args(parser)
        bt.axon.add_args(parser)
        
        config = bt.config(parser)
        return config
    
    async def get_position_data(self, trader_address: str, coin: str) -> Optional[Dict]:
        """Fetch position data from Hyperliquid"""
        try:
            response = requests.post(
                f"{self.hyperliquid_api}/info",
                json={
                    "type": "clearinghouseState",
                    "user": trader_address
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
            bt.logging.error(f"Error fetching position: {e}")
            return None
    
    async def get_market_volatility(self, coin: str) -> float:
        """Calculate recent volatility"""
        try:
            response = requests.post(
                f"{self.hyperliquid_api}/info",
                json={
                    "type": "candleSnapshot",
                    "req": {
                        "coin": coin,
                        "interval": "1h",
                        "startTime": int(time.time() * 1000) - 86400000
                    }
                }
            )
            data = response.json()
            
            if not data:
                return 0.0
            
            prices = [float(candle['c']) for candle in data]
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns) * 100
            
            return volatility
        except:
            return 0.0
    
    async def calculate_degen_score(self, position: Dict) -> float:
        """Calculate 0-100 degen score"""
        
        # Leverage factor (max 30 points)
        leverage = position.get('leverage', 1)
        leverage_score = min(leverage / 100 * 30, 30)
        
        # Position size factor (max 25 points)
        position_value = abs(position['szi']) * position['entry_px']
        size_score = min(position_value / 50000 * 25, 25)
        
        # Volatility factor (max 20 points)
        volatility = await self.get_market_volatility(position['coin'])
        vol_score = min(volatility / 10 * 20, 20)
        
        # Unrealized PnL factor (max 15 points)
        unrealized_pnl = position.get('unrealized_pnl', 0)
        if unrealized_pnl < 0:
            pnl_score = min(abs(unrealized_pnl) / 1000 * 15, 15)
        else:
            pnl_score = 0
        
        # Distance to liquidation (max 10 points)
        if position.get('liquidation_px', 0) > 0:
            entry_px = position['entry_px']
            liq_px = position['liquidation_px']
            distance = abs(liq_px - entry_px) / entry_px
            liq_score = max(0, 10 - (distance * 100))  # Closer to liq = higher score
        else:
            liq_score = 0
        
        total_score = leverage_score + size_score + vol_score + pnl_score + liq_score
        return min(total_score, 100)
    
    async def predict_degen(self, synapse: DegenSynapse) -> DegenSynapse:
        """Main prediction function - called by validators"""
        
        bt.logging.info(f"📊 Prediction request: {synapse.trader_address[:10]}... {synapse.coin}")
        
        try:
            # Get position data
            position = synapse.position_data
            if not position:
                position = await self.get_position_data(synapse.trader_address, synapse.coin)
            
            if not position:
                synapse.degen_score = 0.0
                synapse.confidence = 0.0
                synapse.reasoning = "Position not found"
                return synapse
            
            # Calculate degen score
            degen_score = await self.calculate_degen_score(position)
            
            # Predict loss probability
            loss_probability = min(degen_score / 100 * 0.9, 0.95)  # Max 95%
            
            # Estimate time to liquidation
            if position.get('liquidation_px', 0) > 0:
                entry_px = position['entry_px']
                liq_px = position['liquidation_px']
                distance_to_liq = abs(liq_px - entry_px) / entry_px
                
                volatility = await self.get_market_volatility(position['coin'])
                estimated_hours = distance_to_liq / (volatility / 100) if volatility > 0 else 24
                rekt_timeline = int(estimated_hours * 3600)
            else:
                rekt_timeline = 86400  # 24 hours default
            
            # Calculate confidence based on data quality
            confidence = 0.8 if position.get('liquidation_px', 0) > 0 else 0.5
            
            # Generate reasoning
            reasoning_parts = []
            if position.get('leverage', 1) > 50:
                reasoning_parts.append(f"{position['leverage']:.0f}x leverage")
            if position.get('unrealized_pnl', 0) < -1000:
                reasoning_parts.append(f"${abs(position['unrealized_pnl']):.0f} underwater")
            if degen_score > 80:
                reasoning_parts.append("extreme degen detected")
            
            reasoning = " | ".join(reasoning_parts) if reasoning_parts else "moderate risk"
            
            # Fill synapse response
            synapse.degen_score = degen_score
            synapse.predicted_loss_probability = loss_probability
            synapse.predicted_rekt_timeline = rekt_timeline
            synapse.confidence = confidence
            synapse.reasoning = reasoning
            
            bt.logging.info(f"✅ Prediction: degen={degen_score:.0f}, loss_prob={loss_probability:.2%}, timeline={rekt_timeline}s")
            
        except Exception as e:
            bt.logging.error(f"❌ Prediction error: {e}")
            synapse.degen_score = 0.0
            synapse.confidence = 0.0
            synapse.reasoning = f"Error: {str(e)}"
        
        return synapse
    
    async def blacklist_fn(self, synapse: DegenSynapse) -> tuple[bool, str]:
        """Blacklist function - reject requests from non-validators"""
        
        # Check if requester is a validator
        caller_uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        
        if caller_uid is None:
            return True, "Unrecognized hotkey"
        
        # Check stake
        stake = self.metagraph.S[caller_uid].item()
        if stake < 1000:  # Require 1000 TAO stake
            return True, f"Insufficient stake: {stake}"
        
        return False, "Accepted"
    
    async def priority_fn(self, synapse: DegenSynapse) -> float:
        """Priority function - prioritize high-stake validators"""
        
        try:
            caller_uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
            stake = self.metagraph.S[caller_uid].item()
            return stake
        except:
            return 0.0
    
    def run(self):
        """Run the miner"""
        
        bt.logging.info("🚀 Starting FRY Degen Miner...")
        
        # Attach forward function to axon
        self.axon.attach(
            forward_fn=self.predict_degen,
            blacklist_fn=self.blacklist_fn,
            priority_fn=self.priority_fn
        )
        
        # Serve axon
        self.axon.serve(netuid=self.config.netuid, subtensor=self.subtensor)
        self.axon.start()
        
        bt.logging.info(f"✅ Miner running on port {self.config.axon.port}")
        bt.logging.info(f"   Hotkey: {self.wallet.hotkey.ss58_address}")
        
        # Keep running
        try:
            while True:
                # Sync metagraph every 5 minutes
                time.sleep(300)
                self.metagraph.sync(subtensor=self.subtensor)
                bt.logging.info(f"🔄 Metagraph synced. Total neurons: {len(self.metagraph.uids)}")
                
        except KeyboardInterrupt:
            bt.logging.info("⏹️  Miner stopped")
            self.axon.stop()

if __name__ == "__main__":
    miner = DegenMiner()
    miner.run()
