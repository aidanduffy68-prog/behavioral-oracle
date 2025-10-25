"""
FRY Degen Subnet - Bittensor Protocol Definition
Custom protocol for degen trade prediction and validation
"""

import bittensor as bt
from typing import Optional, Dict, List
from pydantic import Field

class DegenProtocol(bt.StreamingSynapse):
    """
    Custom Bittensor protocol for FRY Degen Subnet
    
    This protocol enables:
    - Real-time degen trade detection
    - Loss probability prediction
    - Liquidation timeline estimation
    - FRY token minting integration
    """
    
    # Request fields (sent by validator to miner)
    trader_address: str = Field(
        ...,
        description="Ethereum/Hyperliquid address of trader"
    )
    
    coin: str = Field(
        ...,
        description="Trading pair (e.g., 'XRP', 'BTC', 'FARTCOIN')"
    )
    
    position_data: Dict = Field(
        default_factory=dict,
        description="Position data from Hyperliquid API"
    )
    
    request_type: str = Field(
        default="predict",
        description="Type of request: 'predict', 'validate', 'score'"
    )
    
    # Response fields (returned by miner)
    degen_score: float = Field(
        default=0.0,
        description="Degen score 0-100 (higher = more degen)"
    )
    
    predicted_loss_probability: float = Field(
        default=0.0,
        description="Probability of loss/liquidation (0-1)"
    )
    
    predicted_rekt_timeline: int = Field(
        default=0,
        description="Estimated seconds until liquidation"
    )
    
    confidence: float = Field(
        default=0.0,
        description="Miner's confidence in prediction (0-1)"
    )
    
    reasoning: str = Field(
        default="",
        description="Human-readable explanation of prediction"
    )
    
    # Metadata
    miner_hotkey: Optional[str] = Field(
        default=None,
        description="Miner's hotkey address"
    )
    
    prediction_timestamp: Optional[int] = Field(
        default=None,
        description="Unix timestamp of prediction"
    )
    
    # FRY-specific fields
    fry_multiplier: float = Field(
        default=1.0,
        description="FRY minting multiplier based on degen score"
    )
    
    estimated_fry_mint: float = Field(
        default=0.0,
        description="Estimated FRY tokens to mint if prediction correct"
    )
    
    def deserialize(self) -> Dict:
        """Deserialize response from miner"""
        return {
            'degen_score': self.degen_score,
            'predicted_loss_probability': self.predicted_loss_probability,
            'predicted_rekt_timeline': self.predicted_rekt_timeline,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'fry_multiplier': self.fry_multiplier,
            'estimated_fry_mint': self.estimated_fry_mint
        }

class DegenRewardModel:
    """
    Reward model for scoring miner predictions
    Integrates with FRY tokenomics
    """
    
    def __init__(self):
        self.base_fry_rate = 10  # 10 FRY per $1 lost
        self.max_multiplier = 100  # Max 100x multiplier
    
    def calculate_fry_multiplier(self, degen_score: float) -> float:
        """Calculate FRY minting multiplier based on degen score"""
        
        # Higher degen score = higher multiplier
        if degen_score >= 90:
            return 10.0  # 10x for extreme degens
        elif degen_score >= 80:
            return 5.0
        elif degen_score >= 70:
            return 3.0
        elif degen_score >= 60:
            return 2.0
        else:
            return 1.0
    
    def score_prediction(
        self,
        prediction: Dict,
        actual_outcome: Optional[Dict] = None
    ) -> float:
        """
        Score a miner's prediction
        
        Args:
            prediction: Miner's prediction data
            actual_outcome: Actual trade outcome (if available)
        
        Returns:
            Score between 0 and 1
        """
        
        if not actual_outcome:
            # Score based on consensus if no outcome yet
            return self._score_by_consensus(prediction)
        
        # Score based on accuracy
        accuracy_score = 0.0
        
        # 1. Loss probability accuracy (50% weight)
        actual_rekt = actual_outcome.get('liquidated', False)
        predicted_rekt = prediction['predicted_loss_probability'] > 0.5
        
        if actual_rekt == predicted_rekt:
            loss_accuracy = 1.0 - abs(
                prediction['predicted_loss_probability'] - 
                (1.0 if actual_rekt else 0.0)
            )
        else:
            loss_accuracy = 0.0
        
        accuracy_score += loss_accuracy * 0.5
        
        # 2. Timeline accuracy (30% weight)
        if actual_rekt and actual_outcome.get('liquidation_time'):
            predicted_time = prediction['predicted_rekt_timeline']
            actual_time = actual_outcome['liquidation_time'] - prediction.get('prediction_timestamp', 0)
            
            time_error = abs(predicted_time - actual_time) / max(predicted_time, actual_time, 1)
            timeline_accuracy = max(0, 1.0 - time_error)
            accuracy_score += timeline_accuracy * 0.3
        
        # 3. Degen score accuracy (20% weight)
        actual_degen = self._calculate_actual_degen_score(actual_outcome)
        degen_error = abs(prediction['degen_score'] - actual_degen) / 100
        degen_accuracy = 1.0 - degen_error
        accuracy_score += degen_accuracy * 0.2
        
        # Weight by confidence
        final_score = accuracy_score * prediction['confidence']
        
        return final_score
    
    def _score_by_consensus(self, prediction: Dict) -> float:
        """Score prediction based on consensus (when no outcome available)"""
        
        # For now, just return confidence
        # In production, compare with other miners' predictions
        return prediction['confidence'] * 0.5
    
    def _calculate_actual_degen_score(self, outcome: Dict) -> float:
        """Calculate what the degen score should have been"""
        
        if outcome.get('liquidated'):
            loss_amount = outcome.get('loss_amount', 0)
            
            # Higher loss = higher degen score
            if loss_amount > 10000:
                return 95
            elif loss_amount > 5000:
                return 85
            elif loss_amount > 1000:
                return 70
            else:
                return 50
        else:
            return 30  # Survived = lower degen score
    
    def calculate_fry_reward(
        self,
        loss_amount: float,
        degen_score: float,
        accuracy_score: float
    ) -> float:
        """
        Calculate FRY tokens to mint
        
        Args:
            loss_amount: Dollar amount lost
            degen_score: Degen score of the trade
            accuracy_score: Miner's prediction accuracy
        
        Returns:
            FRY tokens to mint
        """
        
        # Base FRY from loss
        base_fry = loss_amount * self.base_fry_rate
        
        # Multiplier from degen score
        multiplier = self.calculate_fry_multiplier(degen_score)
        
        # Bonus for accurate prediction
        accuracy_bonus = 1.0 + (accuracy_score * 0.5)  # Up to 1.5x bonus
        
        total_fry = base_fry * multiplier * accuracy_bonus
        
        return min(total_fry, loss_amount * self.base_fry_rate * self.max_multiplier)

class SubnetConfig:
    """Configuration for FRY Degen Subnet"""
    
    # Subnet parameters
    NETUID = 1  # Subnet ID on Bittensor
    NETWORK = "test"  # "test" or "finney" (mainnet)
    
    # Staking requirements
    MIN_MINER_STAKE = 1000  # 1000 TAO to mine
    MIN_VALIDATOR_STAKE = 10000  # 10000 TAO to validate
    
    # Validation parameters
    EPOCH_LENGTH = 100  # Blocks per epoch
    VALIDATION_INTERVAL = 60  # Seconds between validations
    QUERY_TIMEOUT = 12  # Seconds to wait for miner response
    
    # Scoring parameters
    SCORE_EMA_ALPHA = 0.3  # Exponential moving average weight
    MIN_SCORE_THRESHOLD = 0.1  # Minimum score to receive rewards
    
    # FRY integration
    CASINO_API_URL = "http://localhost:8000"
    FRY_MINT_ENABLED = True
    
    # Hyperliquid integration
    HYPERLIQUID_API_URL = "https://api.hyperliquid.xyz"
    MONITORED_ADDRESSES = [
        "0xf551aF8d5373B042DBB9F0933C59213B534174e4"  # Your wallet
    ]
    MONITORED_COINS = ["XRP", "FARTCOIN", "BTC", "ETH"]
    
    @classmethod
    def get_bittensor_config(cls):
        """Get Bittensor config object"""
        parser = bt.ArgumentParser()
        
        parser.add_argument('--netuid', type=int, default=cls.NETUID)
        parser.add_argument('--subtensor.network', type=str, default=cls.NETWORK)
        parser.add_argument('--neuron.epoch_length', type=int, default=cls.EPOCH_LENGTH)
        
        bt.subtensor.add_args(parser)
        bt.wallet.add_args(parser)
        bt.axon.add_args(parser)
        
        return bt.config(parser)

# Export protocol components
__all__ = [
    'DegenProtocol',
    'DegenRewardModel',
    'SubnetConfig'
]
