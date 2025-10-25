"""
FRY Degen Subnet - Bittensor Validator Neuron
Real Bittensor integration for validating degen predictions
"""

import bittensor as bt
import asyncio
import time
import requests
import torch
from typing import Dict, List, Optional
import json

from bittensor_degen_miner import DegenSynapse

class DegenValidator:
    """Bittensor validator for FRY Degen Subnet"""
    
    def __init__(self, config=None):
        # Initialize Bittensor components
        self.config = config or self.get_config()
        
        # Setup wallet
        self.wallet = bt.wallet(config=self.config)
        self.subtensor = bt.subtensor(config=self.config)
        self.metagraph = self.subtensor.metagraph(self.config.netuid)
        
        # Setup dendrite (validator client)
        self.dendrite = bt.dendrite(wallet=self.wallet)
        
        # Hyperliquid API
        self.hyperliquid_api = "https://api.hyperliquid.xyz"
        
        # FRY Casino integration
        self.casino_api = "http://localhost:8000"
        
        # Tracking
        self.prediction_history = {}  # uid -> list of predictions
        self.miner_scores = torch.zeros(len(self.metagraph.uids))
        
        bt.logging.info(f"🍟 FRY Degen Validator initialized")
        bt.logging.info(f"   Wallet: {self.wallet.hotkey.ss58_address}")
        bt.logging.info(f"   Network: {self.config.subtensor.network}")
        bt.logging.info(f"   Netuid: {self.config.netuid}")
    
    @classmethod
    def get_config(cls):
        """Get Bittensor configuration"""
        parser = bt.ArgumentParser()
        parser.add_argument('--netuid', type=int, default=1, help='Subnet netuid')
        parser.add_argument('--subtensor.network', type=str, default='test', help='Bittensor network')
        parser.add_argument('--wallet.name', type=str, default='validator', help='Wallet name')
        parser.add_argument('--wallet.hotkey', type=str, default='default', help='Wallet hotkey')
        parser.add_argument('--neuron.epoch_length', type=int, default=100, help='Blocks per epoch')
        
        bt.subtensor.add_args(parser)
        bt.wallet.add_args(parser)
        
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
    
    async def query_miners(self, trader_address: str, coin: str, position_data: Dict) -> List[DegenSynapse]:
        """Query all miners for predictions"""
        
        # Get active miner UIDs
        miner_uids = []
        for uid in self.metagraph.uids:
            if self.metagraph.axons[uid].is_serving:
                miner_uids.append(uid)
        
        if not miner_uids:
            bt.logging.warning("No active miners found")
            return []
        
        bt.logging.info(f"📡 Querying {len(miner_uids)} miners...")
        
        # Create synapses
        synapses = [
            DegenSynapse(
                trader_address=trader_address,
                coin=coin,
                position_data=position_data
            )
            for _ in miner_uids
        ]
        
        # Query miners
        responses = await self.dendrite(
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            synapses=synapses,
            deserialize=True,
            timeout=12
        )
        
        return responses
    
    def score_predictions(self, responses: List[DegenSynapse], actual_outcome: Optional[Dict] = None) -> torch.Tensor:
        """Score miner predictions"""
        
        scores = torch.zeros(len(self.metagraph.uids))
        
        if not responses:
            return scores
        
        # If we have actual outcome, score based on accuracy
        if actual_outcome:
            for i, response in enumerate(responses):
                if response.degen_score == 0:
                    continue
                
                # Calculate accuracy
                actual_rekt = actual_outcome.get('liquidated', False)
                predicted_rekt = response.predicted_loss_probability > 0.5
                
                # Accuracy score
                if actual_rekt == predicted_rekt:
                    accuracy = 1.0
                else:
                    accuracy = 0.0
                
                # Degen score accuracy
                actual_degen = actual_outcome.get('degen_score', 50)
                degen_error = abs(response.degen_score - actual_degen) / 100
                degen_accuracy = 1.0 - degen_error
                
                # Combined score
                final_score = (accuracy * 0.7 + degen_accuracy * 0.3) * response.confidence
                
                # Get miner UID
                uid = self.metagraph.hotkeys.index(response.axon.hotkey)
                scores[uid] = final_score
        
        else:
            # Score based on consensus and confidence
            degen_scores = [r.degen_score for r in responses if r.degen_score > 0]
            
            if degen_scores:
                median_score = torch.tensor(degen_scores).median().item()
                
                for i, response in enumerate(responses):
                    if response.degen_score == 0:
                        continue
                    
                    # Reward consensus
                    deviation = abs(response.degen_score - median_score) / 100
                    consensus_score = 1.0 - deviation
                    
                    # Weight by confidence
                    final_score = consensus_score * response.confidence
                    
                    uid = self.metagraph.hotkeys.index(response.axon.hotkey)
                    scores[uid] = final_score
        
        # Normalize scores
        if scores.sum() > 0:
            scores = scores / scores.sum()
        
        return scores
    
    async def check_liquidation(self, trader_address: str, coin: str, since_timestamp: int) -> Optional[Dict]:
        """Check if position was liquidated"""
        try:
            response = requests.post(
                f"{self.hyperliquid_api}/info",
                json={
                    "type": "userFills",
                    "user": trader_address
                }
            )
            fills = response.json() or []
            
            for fill in fills:
                if (fill.get('coin') == coin and 
                    fill.get('time', 0) > since_timestamp and
                    fill.get('liquidation', False)):
                    
                    return {
                        'liquidated': True,
                        'liquidation_time': fill['time'],
                        'loss_amount': abs(float(fill.get('closedPnl', 0)))
                    }
            
            return {'liquidated': False}
        except Exception as e:
            bt.logging.error(f"Error checking liquidation: {e}")
            return None
    
    async def mint_fry_from_loss(self, loss_amount: float, trader_address: str, coin: str):
        """Mint FRY tokens via casino backend"""
        try:
            response = requests.post(
                f"{self.casino_api}/mirror",
                json={
                    "pnl": -loss_amount,
                    "symbol": coin,
                    "trade_type": "bittensor_validated"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                fry_minted = data['balance_update']['fry_change']
                bt.logging.info(f"🍟 Minted {fry_minted:.0f} FRY from ${loss_amount:.2f} loss")
                return fry_minted
            else:
                bt.logging.warning(f"Failed to mint FRY: {response.status_code}")
                return 0
        except Exception as e:
            bt.logging.error(f"Error minting FRY: {e}")
            return 0
    
    def set_weights(self, scores: torch.Tensor):
        """Set weights on the Bittensor network"""
        
        try:
            # Only set weights for non-zero scores
            uids = torch.where(scores > 0)[0]
            weights = scores[uids]
            
            if len(uids) == 0:
                bt.logging.warning("No miners to set weights for")
                return
            
            # Set weights on chain
            result = self.subtensor.set_weights(
                netuid=self.config.netuid,
                wallet=self.wallet,
                uids=uids,
                weights=weights,
                wait_for_inclusion=False,
                wait_for_finalization=False
            )
            
            if result:
                bt.logging.info(f"✅ Set weights for {len(uids)} miners")
            else:
                bt.logging.warning("Failed to set weights")
                
        except Exception as e:
            bt.logging.error(f"Error setting weights: {e}")
    
    async def validation_loop(self):
        """Main validation loop"""
        
        bt.logging.info("🔍 Starting validation loop...")
        
        # Example: Monitor your XRP position
        trader_address = "0xf551aF8d5373B042DBB9F0933C59213B534174e4"
        coin = "XRP"
        
        step = 0
        
        while True:
            try:
                step += 1
                bt.logging.info(f"\n{'='*60}")
                bt.logging.info(f"Validation Step {step}")
                bt.logging.info(f"{'='*60}")
                
                # Get position data
                position = await self.get_position_data(trader_address, coin)
                
                if not position:
                    bt.logging.info(f"No {coin} position found for {trader_address[:10]}...")
                    await asyncio.sleep(60)
                    continue
                
                bt.logging.info(f"📊 Position: {coin} | Size: ${abs(position['szi']) * position['entry_px']:.2f} | "
                              f"Leverage: {position['leverage']:.0f}x | PnL: ${position['unrealized_pnl']:.2f}")
                
                # Query miners
                responses = await self.query_miners(trader_address, coin, position)
                
                if not responses:
                    bt.logging.warning("No responses from miners")
                    await asyncio.sleep(60)
                    continue
                
                # Log predictions
                bt.logging.info(f"\n📈 Miner Predictions:")
                for i, response in enumerate(responses):
                    if response.degen_score > 0:
                        bt.logging.info(f"   Miner {i}: degen={response.degen_score:.0f}, "
                                      f"loss_prob={response.predicted_loss_probability:.1%}, "
                                      f"confidence={response.confidence:.2f}")
                        bt.logging.info(f"            {response.reasoning}")
                
                # Check for liquidation (for positions we've been tracking)
                prediction_timestamp = int(time.time()) - 3600  # Check last hour
                liquidation = await self.check_liquidation(trader_address, coin, prediction_timestamp)
                
                if liquidation and liquidation.get('liquidated'):
                    bt.logging.info(f"\n💀 LIQUIDATION DETECTED!")
                    bt.logging.info(f"   Loss: ${liquidation['loss_amount']:.2f}")
                    
                    # Mint FRY
                    await self.mint_fry_from_loss(
                        liquidation['loss_amount'],
                        trader_address,
                        coin
                    )
                    
                    # Score miners based on actual outcome
                    actual_outcome = {
                        'liquidated': True,
                        'degen_score': 95,  # High degen if liquidated
                        'loss_amount': liquidation['loss_amount']
                    }
                    scores = self.score_predictions(responses, actual_outcome)
                else:
                    # Score based on consensus
                    scores = self.score_predictions(responses)
                
                # Update running scores (EMA)
                alpha = 0.3
                self.miner_scores = alpha * scores + (1 - alpha) * self.miner_scores
                
                # Set weights every 10 steps
                if step % 10 == 0:
                    self.set_weights(self.miner_scores)
                    
                    # Log top miners
                    top_uids = torch.argsort(self.miner_scores, descending=True)[:5]
                    bt.logging.info(f"\n🏆 Top Miners:")
                    for uid in top_uids:
                        if self.miner_scores[uid] > 0:
                            bt.logging.info(f"   UID {uid}: score={self.miner_scores[uid]:.4f}")
                
                # Sync metagraph every 5 steps
                if step % 5 == 0:
                    self.metagraph.sync(subtensor=self.subtensor)
                    bt.logging.info(f"🔄 Metagraph synced. Total neurons: {len(self.metagraph.uids)}")
                
                # Wait before next validation
                await asyncio.sleep(60)  # Validate every minute
                
            except KeyboardInterrupt:
                bt.logging.info("⏹️  Validator stopped")
                break
            except Exception as e:
                bt.logging.error(f"❌ Validation error: {e}")
                await asyncio.sleep(60)
    
    def run(self):
        """Run the validator"""
        
        bt.logging.info("🚀 Starting FRY Degen Validator...")
        bt.logging.info(f"   Hotkey: {self.wallet.hotkey.ss58_address}")
        bt.logging.info(f"   Monitoring positions on Hyperliquid")
        bt.logging.info(f"   FRY Casino: {self.casino_api}")
        
        # Run validation loop
        asyncio.run(self.validation_loop())

if __name__ == "__main__":
    validator = DegenValidator()
    validator.run()
