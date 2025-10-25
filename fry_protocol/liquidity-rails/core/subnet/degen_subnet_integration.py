"""
FRY Degen Subnet - Integration with Losers Casino Backend
Merges Bittensor-style subnet with existing FRY casino infrastructure
"""

import asyncio
import requests
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from degen_subnet_core import subnet, DegenPrediction, TradeOutcomeData, TradeOutcome
from degen_miner import DegenMiner
from degen_validator import DegenValidator

# FastAPI app for subnet API
app = FastAPI(title="FRY Degen Subnet API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class MinerRegistration(BaseModel):
    miner_id: str
    wallet_address: str
    stake: float

class ValidatorRegistration(BaseModel):
    validator_id: str
    wallet_address: str
    stake: float

class PredictionSubmission(BaseModel):
    trade_id: str
    miner_id: str
    degen_score: float
    predicted_loss_probability: float
    predicted_rekt_timeline: int
    leverage: float
    position_size: float
    volatility: float
    liquidity_score: float
    fomo_factor: float

class OutcomeSubmission(BaseModel):
    trade_id: str
    outcome: str  # "rekt", "survived", "moon"
    loss_amount: float
    liquidation_time: int = None
    final_pnl: float

class FRYCasinoIntegration:
    """Integration layer with FRY Casino backend"""
    
    def __init__(self, casino_api_url: str = "http://localhost:8000"):
        self.casino_api_url = casino_api_url
    
    async def mint_fry_from_subnet_loss(self, loss_amount: float, trade_id: str) -> Dict:
        """Mint FRY tokens when subnet validates a loss"""
        try:
            response = requests.post(
                f"{self.casino_api_url}/mirror",
                json={
                    "pnl": -loss_amount,  # Negative for loss
                    "symbol": "SUBNET",
                    "trade_type": "subnet_validated"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'fry_minted': data['balance_update']['fry_change'],
                    'new_balance': data['balance_update']['balance_after']
                }
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def burn_fry_from_subnet_profit(self, profit_amount: float, trade_id: str) -> Dict:
        """Burn FRY tokens when subnet validates a profit"""
        try:
            response = requests.post(
                f"{self.casino_api_url}/mirror",
                json={
                    "pnl": profit_amount,  # Positive for profit
                    "symbol": "SUBNET",
                    "trade_type": "subnet_validated"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'fry_burned': abs(data['balance_update']['fry_change']),
                    'new_balance': data['balance_update']['balance_after']
                }
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def get_casino_balance(self) -> float:
        """Get current FRY balance from casino"""
        try:
            response = requests.get(f"{self.casino_api_url}/balance")
            if response.status_code == 200:
                return response.json()['balance']
            return 0.0
        except:
            return 0.0

# Global integration instance
casino_integration = FRYCasinoIntegration()

# API Routes
@app.post("/subnet/miner/register")
async def register_miner(reg: MinerRegistration):
    """Register a new miner"""
    success = subnet.register_miner(reg.miner_id, reg.stake)
    
    if success:
        return {
            'success': True,
            'miner_id': reg.miner_id,
            'stake': reg.stake,
            'message': 'Miner registered successfully'
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to register miner")

@app.post("/subnet/validator/register")
async def register_validator(reg: ValidatorRegistration):
    """Register a new validator"""
    success = subnet.register_validator(reg.validator_id, reg.stake)
    
    if success:
        return {
            'success': True,
            'validator_id': reg.validator_id,
            'stake': reg.stake,
            'message': 'Validator registered successfully'
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to register validator")

@app.post("/subnet/prediction/submit")
async def submit_prediction(pred: PredictionSubmission):
    """Submit a degen prediction"""
    import time
    import hashlib
    
    # Create prediction object
    prediction = DegenPrediction(
        trade_id=pred.trade_id,
        miner_id=pred.miner_id,
        degen_score=pred.degen_score,
        predicted_loss_probability=pred.predicted_loss_probability,
        predicted_rekt_timeline=pred.predicted_rekt_timeline,
        leverage=pred.leverage,
        position_size=pred.position_size,
        volatility=pred.volatility,
        liquidity_score=pred.liquidity_score,
        fomo_factor=pred.fomo_factor,
        timestamp=int(time.time()),
        signature=hashlib.sha256(f"{pred.miner_id}{pred.trade_id}".encode()).hexdigest()
    )
    
    success = subnet.submit_prediction(prediction)
    
    if success:
        return {
            'success': True,
            'prediction_hash': prediction.hash(),
            'trade_id': pred.trade_id,
            'degen_score': pred.degen_score
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to submit prediction")

@app.post("/subnet/outcome/submit")
async def submit_outcome(outcome: OutcomeSubmission):
    """Submit a validated trade outcome"""
    import time
    
    # Map string to enum
    outcome_map = {
        'rekt': TradeOutcome.REKT,
        'survived': TradeOutcome.SURVIVED,
        'moon': TradeOutcome.MOON
    }
    
    outcome_data = TradeOutcomeData(
        trade_id=outcome.trade_id,
        outcome=outcome_map[outcome.outcome.lower()],
        loss_amount=outcome.loss_amount,
        liquidation_time=outcome.liquidation_time,
        final_pnl=outcome.final_pnl,
        timestamp=int(time.time())
    )
    
    success = subnet.submit_outcome(outcome_data)
    
    if success:
        # Integrate with FRY casino
        if outcome_data.outcome == TradeOutcome.REKT:
            mint_result = await casino_integration.mint_fry_from_subnet_loss(
                outcome.loss_amount,
                outcome.trade_id
            )
            return {
                'success': True,
                'outcome': outcome.outcome,
                'fry_integration': mint_result
            }
        elif outcome_data.outcome == TradeOutcome.MOON:
            burn_result = await casino_integration.burn_fry_from_subnet_profit(
                outcome.final_pnl,
                outcome.trade_id
            )
            return {
                'success': True,
                'outcome': outcome.outcome,
                'fry_integration': burn_result
            }
        else:
            return {
                'success': True,
                'outcome': outcome.outcome,
                'fry_integration': {'success': True, 'message': 'No FRY change for survived outcome'}
            }
    else:
        raise HTTPException(status_code=400, detail="Failed to submit outcome")

@app.get("/subnet/leaderboard")
async def get_leaderboard(limit: int = 10):
    """Get subnet leaderboard"""
    return subnet.get_leaderboard(limit)

@app.get("/subnet/stats")
async def get_subnet_stats():
    """Get subnet statistics"""
    stats = subnet.get_subnet_stats()
    
    # Add FRY casino balance
    casino_balance = await casino_integration.get_casino_balance()
    stats['fry_casino_balance'] = casino_balance
    
    return stats

@app.get("/subnet/predictions/{trade_id}")
async def get_predictions(trade_id: str):
    """Get all predictions for a trade"""
    predictions = subnet.predictions.get(trade_id, [])
    return [pred.to_dict() for pred in predictions]

@app.get("/subnet/rewards/{block_number}")
async def get_block_rewards(block_number: int):
    """Get reward distribution for a block"""
    return subnet.calculate_block_rewards(block_number)

@app.get("/subnet/miner/{miner_id}/scores")
async def get_miner_scores(miner_id: str, limit: int = 50):
    """Get recent scores for a miner"""
    scores = subnet.miner_scores.get(miner_id, [])[-limit:]
    return [
        {
            'prediction_hash': s.prediction_hash,
            'accuracy_score': s.accuracy_score,
            'final_score': s.final_score,
            'timestamp': s.timestamp
        }
        for s in scores
    ]

@app.get("/subnet/integration/status")
async def get_integration_status():
    """Check integration status with FRY casino"""
    casino_balance = await casino_integration.get_casino_balance()
    
    return {
        'subnet_active': True,
        'casino_connected': casino_balance > 0,
        'casino_balance': casino_balance,
        'casino_api_url': casino_integration.casino_api_url,
        'total_miners': len(subnet.miner_stakes),
        'total_validators': len(subnet.validator_stakes),
        'total_predictions': sum(len(p) for p in subnet.predictions.values()),
        'total_outcomes': len(subnet.outcomes)
    }

# Background task to process rewards
async def reward_distribution_task():
    """Background task to distribute DEGEN token rewards"""
    block_number = 0
    
    while True:
        try:
            # Calculate and distribute rewards every 12 seconds (block time)
            rewards = subnet.calculate_block_rewards(block_number)
            
            # Log rewards
            if rewards['miners'] or rewards['validators']:
                print(f"\n💰 Block #{block_number} Rewards:")
                print(f"   Total Emission: {rewards['total_emission']} DEGEN")
                
                if rewards['miners']:
                    top_miner = max(rewards['miners'].items(), key=lambda x: x[1])
                    print(f"   Top Miner: {top_miner[0]} ({top_miner[1]:.4f} DEGEN)")
                
                if rewards['validators']:
                    top_validator = max(rewards['validators'].items(), key=lambda x: x[1])
                    print(f"   Top Validator: {top_validator[0]} ({top_validator[1]:.4f} DEGEN)")
            
            block_number += 1
            await asyncio.sleep(12)  # 12 second block time
            
        except Exception as e:
            print(f"❌ Reward distribution error: {e}")
            await asyncio.sleep(12)

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    asyncio.create_task(reward_distribution_task())
    print("🚀 FRY Degen Subnet API started")
    print("   Casino integration: http://localhost:8000")
    print("   Subnet API: http://localhost:8001")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
