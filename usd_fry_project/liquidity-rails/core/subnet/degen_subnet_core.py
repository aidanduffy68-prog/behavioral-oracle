"""
FRY Degen Subnet - Core Runtime
Bittensor-inspired subnet for identifying and predicting degenerate trading outcomes
"""

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum
import numpy as np
from collections import defaultdict

class TradeOutcome(Enum):
    REKT = "rekt"
    SURVIVED = "survived"
    MOON = "moon"

@dataclass
class DegenPrediction:
    """Miner's prediction for a degen trade"""
    trade_id: str
    miner_id: str
    degen_score: float  # 0-100 scale
    predicted_loss_probability: float  # 0-1
    predicted_rekt_timeline: int  # seconds until liquidation
    leverage: float
    position_size: float
    volatility: float
    liquidity_score: float
    fomo_factor: float
    timestamp: int
    signature: str
    
    def to_dict(self):
        return asdict(self)
    
    def hash(self) -> str:
        """Generate unique hash for prediction"""
        data = f"{self.trade_id}{self.miner_id}{self.degen_score}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()

@dataclass
class TradeOutcomeData:
    """Actual outcome of a trade"""
    trade_id: str
    outcome: TradeOutcome
    loss_amount: float
    liquidation_time: Optional[int]
    final_pnl: float
    timestamp: int
    
    def to_dict(self):
        return {
            **asdict(self),
            'outcome': self.outcome.value
        }

@dataclass
class MinerScore:
    """Score for a miner's prediction"""
    miner_id: str
    prediction_hash: str
    accuracy_score: float
    extreme_degen_bonus: float
    consistency_bonus: float
    speed_bonus: float
    final_score: float
    validator_id: str
    timestamp: int

class DegenSubnetCore:
    """Core subnet runtime managing consensus and rewards"""
    
    def __init__(self, subnet_id: int = 1):
        self.subnet_id = subnet_id
        self.predictions: Dict[str, List[DegenPrediction]] = defaultdict(list)
        self.outcomes: Dict[str, TradeOutcomeData] = {}
        self.miner_scores: Dict[str, List[MinerScore]] = defaultdict(list)
        self.validator_stakes: Dict[str, float] = {}
        self.miner_stakes: Dict[str, float] = {}
        
        # Subnet configuration
        self.config = {
            'tempo': 360,  # Validator set updates every 360 blocks
            'immunity_period': 7200,  # New miners immune for 7200 blocks
            'min_stake': 1000,  # 1000 FRY minimum
            'max_validators': 64,
            'max_miners': 4096,
            'block_time': 12,  # 12 seconds
            'emission_per_block': 1.0,  # 1 DEGEN per block
        }
        
        # Emission distribution
        self.emission_split = {
            'miners': 0.41,
            'validators': 0.41,
            'owner': 0.18
        }
        
        # Miner history for consistency bonus
        self.miner_history: Dict[str, List[float]] = defaultdict(list)
        
    def register_miner(self, miner_id: str, stake: float) -> bool:
        """Register a new miner"""
        if stake < self.config['min_stake']:
            return False
        
        if len(self.miner_stakes) >= self.config['max_miners']:
            return False
            
        self.miner_stakes[miner_id] = stake
        return True
    
    def register_validator(self, validator_id: str, stake: float) -> bool:
        """Register a new validator"""
        if stake < self.config['min_stake'] * 10:  # Validators need 10x miner stake
            return False
        
        if len(self.validator_stakes) >= self.config['max_validators']:
            return False
            
        self.validator_stakes[validator_id] = stake
        return True
    
    def submit_prediction(self, prediction: DegenPrediction) -> bool:
        """Miner submits a degen prediction"""
        if prediction.miner_id not in self.miner_stakes:
            return False
        
        # Validate prediction
        if not (0 <= prediction.degen_score <= 100):
            return False
        if not (0 <= prediction.predicted_loss_probability <= 1):
            return False
            
        self.predictions[prediction.trade_id].append(prediction)
        return True
    
    def submit_outcome(self, outcome: TradeOutcomeData) -> bool:
        """Validator submits actual trade outcome"""
        self.outcomes[outcome.trade_id] = outcome
        
        # Score all predictions for this trade
        if outcome.trade_id in self.predictions:
            self._score_predictions(outcome.trade_id)
        
        return True
    
    def _score_predictions(self, trade_id: str):
        """Score all miner predictions for a trade"""
        outcome = self.outcomes[trade_id]
        predictions = self.predictions[trade_id]
        
        for prediction in predictions:
            score = self._calculate_miner_score(prediction, outcome)
            self.miner_scores[prediction.miner_id].append(score)
            
            # Update miner history for consistency tracking
            self.miner_history[prediction.miner_id].append(score.accuracy_score)
    
    def _calculate_miner_score(self, prediction: DegenPrediction, outcome: TradeOutcomeData) -> MinerScore:
        """Calculate score for a single prediction"""
        
        # Base accuracy score
        accuracy = self._calculate_accuracy(prediction, outcome)
        
        # Extreme degen bonus (2x for $10k+ losses)
        extreme_bonus = 1.0 if outcome.loss_amount > 10000 else 0.0
        
        # Consistency bonus based on historical performance
        consistency_bonus = self._calculate_consistency_bonus(prediction.miner_id)
        
        # Speed bonus for early detection
        speed_bonus = self._calculate_speed_bonus(prediction, outcome)
        
        # Final score with multipliers
        final_score = accuracy * (1 + extreme_bonus + consistency_bonus + speed_bonus)
        final_score = min(final_score, 10.0)  # Cap at 10x
        
        return MinerScore(
            miner_id=prediction.miner_id,
            prediction_hash=prediction.hash(),
            accuracy_score=accuracy,
            extreme_degen_bonus=extreme_bonus,
            consistency_bonus=consistency_bonus,
            speed_bonus=speed_bonus,
            final_score=final_score,
            validator_id="system",  # TODO: Track which validator scored this
            timestamp=int(time.time())
        )
    
    def _calculate_accuracy(self, prediction: DegenPrediction, outcome: TradeOutcomeData) -> float:
        """Calculate prediction accuracy score"""
        
        # Loss probability accuracy
        actual_loss = 1.0 if outcome.outcome == TradeOutcome.REKT else 0.0
        loss_error = abs(prediction.predicted_loss_probability - actual_loss)
        loss_accuracy = 1.0 - loss_error
        
        # Timeline accuracy (if rekt occurred)
        timeline_accuracy = 1.0
        if outcome.outcome == TradeOutcome.REKT and outcome.liquidation_time:
            time_error = abs(prediction.predicted_rekt_timeline - outcome.liquidation_time)
            max_error = 3600  # 1 hour max error
            timeline_accuracy = max(0, 1.0 - (time_error / max_error))
        
        # Degen score accuracy (how well did they identify the risk level)
        expected_degen = self._calculate_actual_degen_score(outcome)
        degen_error = abs(prediction.degen_score - expected_degen) / 100
        degen_accuracy = 1.0 - degen_error
        
        # Weighted average
        return (loss_accuracy * 0.5 + timeline_accuracy * 0.3 + degen_accuracy * 0.2)
    
    def _calculate_actual_degen_score(self, outcome: TradeOutcomeData) -> float:
        """Calculate what the degen score should have been based on outcome"""
        if outcome.outcome == TradeOutcome.REKT:
            # Higher loss = higher degen score
            loss_factor = min(outcome.loss_amount / 10000, 1.0) * 50
            speed_factor = 50 if outcome.liquidation_time and outcome.liquidation_time < 3600 else 25
            return loss_factor + speed_factor
        elif outcome.outcome == TradeOutcome.MOON:
            return 30  # Risky but worked out
        else:
            return 20  # Survived, moderate risk
    
    def _calculate_consistency_bonus(self, miner_id: str) -> float:
        """Calculate bonus based on historical accuracy"""
        history = self.miner_history.get(miner_id, [])
        if len(history) < 10:
            return 0.0
        
        # Average of last 50 predictions
        recent_history = history[-50:]
        avg_accuracy = np.mean(recent_history)
        
        # Bonus scales with accuracy
        if avg_accuracy > 0.8:
            return 0.2
        elif avg_accuracy > 0.6:
            return 0.1
        else:
            return 0.0
    
    def _calculate_speed_bonus(self, prediction: DegenPrediction, outcome: TradeOutcomeData) -> float:
        """Calculate bonus for early detection"""
        if outcome.liquidation_time:
            detection_speed = outcome.liquidation_time - prediction.timestamp
            if detection_speed > 3600:  # Predicted >1 hour early
                return 0.15
            elif detection_speed > 1800:  # Predicted >30 min early
                return 0.1
            elif detection_speed > 600:  # Predicted >10 min early
                return 0.05
        return 0.0
    
    def calculate_block_rewards(self, block_number: int) -> Dict[str, Dict[str, float]]:
        """Calculate and distribute rewards for a block"""
        total_emission = self.config['emission_per_block']
        
        # Calculate miner rewards
        miner_pool = total_emission * self.emission_split['miners']
        miner_rewards = self._distribute_miner_rewards(miner_pool)
        
        # Calculate validator rewards
        validator_pool = total_emission * self.emission_split['validators']
        validator_rewards = self._distribute_validator_rewards(validator_pool)
        
        # Owner reward
        owner_reward = total_emission * self.emission_split['owner']
        
        return {
            'miners': miner_rewards,
            'validators': validator_rewards,
            'owner': {'subnet_owner': owner_reward},
            'block_number': block_number,
            'total_emission': total_emission
        }
    
    def _distribute_miner_rewards(self, total_pool: float) -> Dict[str, float]:
        """Distribute rewards to miners based on scores"""
        if not self.miner_scores:
            return {}
        
        # Calculate total weighted scores
        miner_weights = {}
        for miner_id, scores in self.miner_scores.items():
            # Use recent scores (last 100)
            recent_scores = scores[-100:]
            avg_score = np.mean([s.final_score for s in recent_scores])
            miner_weights[miner_id] = avg_score
        
        total_weight = sum(miner_weights.values())
        if total_weight == 0:
            return {}
        
        # Distribute proportionally
        rewards = {}
        for miner_id, weight in miner_weights.items():
            rewards[miner_id] = (weight / total_weight) * total_pool
        
        return rewards
    
    def _distribute_validator_rewards(self, total_pool: float) -> Dict[str, float]:
        """Distribute rewards to validators based on consensus"""
        if not self.validator_stakes:
            return {}
        
        # For now, distribute based on stake (TODO: implement consensus scoring)
        total_stake = sum(self.validator_stakes.values())
        
        rewards = {}
        for validator_id, stake in self.validator_stakes.items():
            rewards[validator_id] = (stake / total_stake) * total_pool
        
        return rewards
    
    def get_leaderboard(self, limit: int = 10) -> Dict[str, List[Dict]]:
        """Get top miners and validators"""
        
        # Top miners by average score
        miner_avgs = {}
        for miner_id, scores in self.miner_scores.items():
            recent_scores = scores[-100:]
            miner_avgs[miner_id] = {
                'miner_id': miner_id,
                'avg_score': np.mean([s.final_score for s in recent_scores]),
                'total_predictions': len(scores),
                'stake': self.miner_stakes.get(miner_id, 0)
            }
        
        top_miners = sorted(
            miner_avgs.values(),
            key=lambda x: x['avg_score'],
            reverse=True
        )[:limit]
        
        # Top validators by stake
        top_validators = sorted(
            [{'validator_id': v, 'stake': s} for v, s in self.validator_stakes.items()],
            key=lambda x: x['stake'],
            reverse=True
        )[:limit]
        
        return {
            'top_miners': top_miners,
            'top_validators': top_validators,
            'total_miners': len(self.miner_stakes),
            'total_validators': len(self.validator_stakes),
            'total_predictions': sum(len(p) for p in self.predictions.values()),
            'total_outcomes': len(self.outcomes)
        }
    
    def get_subnet_stats(self) -> Dict:
        """Get overall subnet statistics"""
        total_predictions = sum(len(p) for p in self.predictions.values())
        total_outcomes = len(self.outcomes)
        
        # Calculate accuracy rate
        rekt_predictions = sum(
            1 for preds in self.predictions.values()
            for p in preds
            if p.predicted_loss_probability > 0.5
        )
        
        actual_rekts = sum(
            1 for o in self.outcomes.values()
            if o.outcome == TradeOutcome.REKT
        )
        
        return {
            'subnet_id': self.subnet_id,
            'total_miners': len(self.miner_stakes),
            'total_validators': len(self.validator_stakes),
            'total_predictions': total_predictions,
            'total_outcomes': total_outcomes,
            'rekt_predictions': rekt_predictions,
            'actual_rekts': actual_rekts,
            'accuracy_rate': actual_rekts / max(rekt_predictions, 1),
            'total_staked': sum(self.miner_stakes.values()) + sum(self.validator_stakes.values()),
            'config': self.config
        }

# Singleton instance
subnet = DegenSubnetCore()
