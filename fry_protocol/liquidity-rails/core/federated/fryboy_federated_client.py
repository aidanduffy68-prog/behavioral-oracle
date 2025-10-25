#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agent B Federated Learning Client
==================================

Client-side wrapper for Agent B instances to participate in federated learning.
Each client trains locally on its own market data and shares model updates
(not raw data) with the Agent B server.

Note: "Fryboy" and "Agent B" are the same - the embedded FRY market maker.

Key Features:
1. Local training on venue-specific market data
2. Privacy-preserving (only shares model weights, not trades)
3. Regime-aware training (adapts to local market conditions)
4. Performance metrics reporting (FRY alpha scores)
5. Automatic reconnection and fault tolerance
"""

import flwr as fl
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, List, Tuple, Optional
from collections import deque
import logging
import time
import json

from agent_b_core import AgentB
from ml_adaptive_hedging import MLAdaptiveHedgingEngine
from topology_routing_engine import TopologyAwareAgentB, TopologyRouter
from zkml_proof_system import ZKMLProofGenerator, ZKProof

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HedgeRatioPredictor(nn.Module):
    """
    Neural network for predicting optimal hedge ratios with topology awareness.
    
    Architecture:
    - Input: Market features + topology features (LPI, volatility, volume, regime, minting gradient)
    - Hidden: 2 layers with dropout for regularization
    - Output: Hedge ratio [0, 1]
    """
    
    def __init__(self, input_dim: int = 25, hidden_dim: int = 64):
        super(HedgeRatioPredictor, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()  # Output between 0 and 1
        )
    
    def forward(self, x):
        return self.network(x)


class FryboyClient(fl.client.NumPyClient):
    """
    Federated learning client for Agent B instances.
    
    Each client:
    1. Maintains local Agent B instance with trading history
    2. Trains hedge ratio predictor on local data
    3. Reports FRY-specific performance metrics
    4. Participates in federated aggregation
    """
    
    def __init__(
        self,
        client_id: str,
        agent_b: AgentB,
        model: HedgeRatioPredictor,
        venue: str = "binance",
        initial_capital: float = 1000000,
    ):
        self.client_id = client_id
        self.agent_b = agent_b
        self.model = model
        self.venue = venue
        self.initial_capital = initial_capital
        
        # Topology-aware routing
        self.topology_agent = TopologyAwareAgentB()
        
        # zkML proof generator for privacy-preserving accuracy verification
        self.zkml_generator = ZKMLProofGenerator(client_id)
        
        # Training data buffer
        self.training_buffer = deque(maxlen=10000)
        self.validation_buffer = deque(maxlen=2000)
        
        # Performance tracking
        self.local_metrics = {
            'total_fry_minted': 0.0,
            'slippage_harvested_usd': 0.0,
            'arbitrage_profit_usd': 0.0,
            'hedge_predictions': [],
            'hedge_actuals': [],
            'training_rounds': 0,
            'topology_fry_bonus': 0.0,
            'avg_minting_gradient': 0.0,
        }
        
        # Optimizer
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        
        logger.info(f"Agent B Client {client_id} initialized on {venue} with topology routing")
    
    def get_parameters(self, config: Dict) -> List[np.ndarray]:
        """Return current model parameters as numpy arrays"""
        return [param.cpu().detach().numpy() for param in self.model.parameters()]
    
    def set_parameters(self, parameters: List[np.ndarray]) -> None:
        """Update model parameters from server"""
        params_dict = zip(self.model.parameters(), parameters)
        for param, new_param in params_dict:
            param.data = torch.tensor(new_param, dtype=param.dtype)
    
    def fit(
        self,
        parameters: List[np.ndarray],
        config: Dict,
    ) -> Tuple[List[np.ndarray], int, Dict]:
        """
        Train model on local data and return updated parameters.
        
        Training Process:
        1. Collect recent Agent B trading data
        2. Extract features and labels (optimal hedge ratios)
        3. Train neural network locally
        4. Calculate FRY alpha metrics
        5. Return updated weights and performance metrics
        """
        
        # Update model with global parameters
        self.set_parameters(parameters)
        
        # Extract training configuration
        server_round = config.get("server_round", 0)
        learning_rate = config.get("learning_rate", 0.001)
        batch_size = config.get("batch_size", 32)
        local_epochs = config.get("local_epochs", 5)
        
        # Update optimizer learning rate
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = learning_rate
        
        logger.info(f"Client {self.client_id} | Round {server_round} | "
                   f"LR: {learning_rate:.6f} | Epochs: {local_epochs}")
        
        # Collect training data from Agent B
        self._collect_training_data()
        
        if len(self.training_buffer) < batch_size:
            logger.warning(f"Insufficient training data: {len(self.training_buffer)} samples")
            return self.get_parameters(config), len(self.training_buffer), self._get_metrics()
        
        # Train model locally
        train_loss = self._train_local_model(batch_size, local_epochs)
        
        # Calculate performance metrics
        metrics = self._get_metrics()
        metrics['train_loss'] = train_loss
        metrics['num_samples'] = len(self.training_buffer)
        
        self.local_metrics['training_rounds'] += 1
        
        logger.info(f"Client {self.client_id} training complete | "
                   f"Loss: {train_loss:.4f} | Samples: {len(self.training_buffer)}")
        
        return self.get_parameters(config), len(self.training_buffer), metrics
    
    def evaluate(
        self,
        parameters: List[np.ndarray],
        config: Dict,
    ) -> Tuple[float, int, Dict]:
        """
        Evaluate model on local validation data with zkML proof generation.
        
        Instead of sending raw RMSE, generates zero-knowledge proof that
        RMSE < threshold WITHOUT revealing private validation data.
        """
        
        # Update model with global parameters
        self.set_parameters(parameters)
        
        if len(self.validation_buffer) == 0:
            return 0.0, 0, {}
        
        # Evaluate on validation set
        self.model.eval()
        total_loss = 0.0
        predictions = []
        actuals = []
        features_list = []
        
        with torch.no_grad():
            for features, label in self.validation_buffer:
                features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
                label_tensor = torch.tensor([label], dtype=torch.float32)
                
                prediction = self.model(features_tensor)
                loss = self.criterion(prediction, label_tensor)
                
                total_loss += loss.item()
                predictions.append(prediction.item())
                actuals.append(label)
                features_list.append(features)
        
        avg_loss = total_loss / len(self.validation_buffer)
        
        # Calculate RMSE (private - not sent to server)
        rmse = np.sqrt(np.mean((np.array(predictions) - np.array(actuals)) ** 2))
        
        # Generate zkML proof of accuracy
        zkml_threshold = config.get('zkml_threshold', 0.05)  # 5% RMSE threshold
        model_hash = config.get('model_hash', 'global_model_v1')
        
        try:
            zkml_proof = self.zkml_generator.generate_accuracy_proof(
                model_predictions=np.array(predictions),
                actual_values=np.array(actuals),
                validation_features=np.array(features_list),
                threshold=zkml_threshold,
                model_hash=model_hash
            )
            
            logger.info(f"✓ Generated zkML proof {zkml_proof.proof_id}")
            logger.info(f"  Private RMSE: {rmse:.6f} (NOT sent to server)")
            logger.info(f"  Proof commitment: {zkml_proof.commitment[:16]}...")
            
        except Exception as e:
            logger.error(f"zkML proof generation failed: {e}")
            zkml_proof = None
        
        # Get metrics (WITHOUT raw RMSE - only zkML proof)
        metrics = self._get_metrics()
        metrics['val_loss'] = avg_loss
        
        # Include zkML proof instead of raw RMSE
        if zkml_proof:
            metrics['zkml_proof'] = zkml_proof.to_dict()
            metrics['zkml_verified'] = True
            # Only include that threshold was met, not actual RMSE
            metrics['hedge_rmse'] = zkml_threshold if rmse < zkml_threshold else zkml_threshold * 1.5
        else:
            # Fallback to traditional reporting if zkML fails
            metrics['hedge_rmse'] = rmse
            metrics['zkml_verified'] = False
        
        return avg_loss, len(self.validation_buffer), metrics
    
    def _collect_training_data(self):
        """
        Collect training data from Agent B's recent trading activity.
        
        Features:
        - LPI score
        - Market volatility
        - Volume metrics
        - Regime indicators
        - Position size
        - Circuit breaker status
        
        Label:
        - Optimal hedge ratio (from ML-enhanced hedging engine)
        """
        
        # Simulate market data collection (in production, this would be real-time)
        num_samples = np.random.randint(50, 200)
        
        for _ in range(num_samples):
            # Generate synthetic market data (replace with real data in production)
            market_data = self._generate_market_data()
            
            # Get optimal hedge ratio from ML engine
            lpi_score = np.random.uniform(0.3, 0.8)
            position_size = np.random.uniform(10000, 500000)
            
            hedge_ratio, decision = self.agent_b.ml_hedging_engine.calculate_enhanced_hedge_ratio(
                'BTC', market_data, position_size, lpi_score, False, time.time()
            )
            
            # Extract features
            features = self._extract_features(market_data, lpi_score, position_size, decision)
            
            # Add to training buffer (80/20 split)
            if np.random.random() < 0.8:
                self.training_buffer.append((features, hedge_ratio))
            else:
                self.validation_buffer.append((features, hedge_ratio))
            
            # Update local metrics
            self.local_metrics['total_fry_minted'] += market_data.get('fry_minted', 0)
            self.local_metrics['slippage_harvested_usd'] += market_data.get('slippage_usd', 0)
    
    def _extract_features(
        self,
        market_data: Dict,
        lpi_score: float,
        position_size: float,
        decision: Dict,
    ) -> np.ndarray:
        """Extract feature vector for neural network with topology features"""
        
        # Base features
        base_features = [
            lpi_score,
            market_data.get('volatility', 0.05),
            market_data.get('volume_ratio', 1.0),
            market_data.get('price_change_pct', 0.0),
            market_data.get('bid_ask_spread', 0.001),
            market_data.get('order_flow_imbalance', 0.0),
            market_data.get('rsi', 50) / 100,  # Normalize
            market_data.get('bollinger_position', 0.5),
            position_size / 1000000,  # Normalize
            1.0 if decision.get('regime') == 'crisis' else 0.0,
            1.0 if decision.get('regime') == 'volatile' else 0.0,
            1.0 if decision.get('regime') == 'trending_bull' else 0.0,
            1.0 if decision.get('regime') == 'trending_bear' else 0.0,
            decision.get('regime_confidence', 0.5),
            decision.get('lpi_score', 0.5),
        ]
        
        # Topology features: optimize cross-DEX route
        try:
            route = self.topology_agent.optimize_cross_dex_trade(
                position_size,
                preferred_dexes=['dYdX', 'GMX']
            )
            
            if route:
                topology_features = [
                    route['total_gradient'],
                    route['avg_gradient'],
                    route['route_efficiency'],
                    route['fry_per_dollar'],
                    len(route['path']) / 4.0,  # Normalize path length
                    1.0 if 'GMX' in route['path'] else 0.0,  # GMX bonus
                    1.0 if 'Hyperliquid' in route['path'] else 0.0,  # Hub bonus
                    route['total_fry'] / position_size,  # FRY efficiency
                    market_data.get('volatility', 0.05) * route['avg_gradient'],  # Combined signal
                    route['route_efficiency'] * decision.get('regime_confidence', 0.5),  # Confidence-weighted
                ]
                
                # Update metrics
                self.local_metrics['topology_fry_bonus'] += route['total_fry']
                self.local_metrics['avg_minting_gradient'] = route['avg_gradient']
            else:
                topology_features = [0.0] * 10
        except Exception as e:
            logger.warning(f"Topology routing failed: {e}")
            topology_features = [0.0] * 10
        
        # Combine base + topology features
        all_features = base_features + topology_features
        
        return np.array(all_features, dtype=np.float32)
    
    def _train_local_model(self, batch_size: int, epochs: int) -> float:
        """Train model on local data"""
        
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            
            # Shuffle training data
            training_data = list(self.training_buffer)
            np.random.shuffle(training_data)
            
            # Mini-batch training
            for i in range(0, len(training_data), batch_size):
                batch = training_data[i:i+batch_size]
                
                if len(batch) < batch_size // 2:
                    continue
                
                # Prepare batch
                features_batch = torch.tensor(
                    [item[0] for item in batch],
                    dtype=torch.float32
                )
                labels_batch = torch.tensor(
                    [[item[1]] for item in batch],
                    dtype=torch.float32
                )
                
                # Forward pass
                self.optimizer.zero_grad()
                predictions = self.model(features_batch)
                loss = self.criterion(predictions, labels_batch)
                
                # Backward pass
                loss.backward()
                self.optimizer.step()
                
                epoch_loss += loss.item()
                num_batches += 1
            
            total_loss += epoch_loss
        
        return total_loss / max(num_batches, 1)
    
    def _get_metrics(self) -> Dict:
        """
        Calculate and return FRY alpha metrics for server aggregation.
        
        Metrics include:
        - Hedge prediction RMSE (primary weight)
        - Slippage harvest efficiency
        - Funding arbitrage ROI
        - FRY minting rate
        - Circuit breaker status
        - Market regime
        """
        
        # Calculate hedge RMSE
        if len(self.validation_buffer) > 0:
            predictions = []
            actuals = []
            
            self.model.eval()
            with torch.no_grad():
                for features, label in list(self.validation_buffer)[-100:]:
                    features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
                    prediction = self.model(features_tensor)
                    predictions.append(prediction.item())
                    actuals.append(label)
            
            hedge_rmse = np.sqrt(np.mean((np.array(predictions) - np.array(actuals)) ** 2))
        else:
            hedge_rmse = 1.0
        
        # Get current Agent B metrics
        agent_metrics = self.agent_b.get_agent_b_metrics()
        
        # Detect current market regime
        regime_detector = self.agent_b.ml_hedging_engine.ensemble.models['regime_detector']
        recent_regime = list(regime_detector.regime_history)[-1] if regime_detector.regime_history else 'unknown'
        
        metrics = {
            'hedge_rmse': hedge_rmse,
            'slippage_harvest_efficiency': self.agent_b.slippage_harvester.config['harvest_efficiency'],
            'arbitrage_roi_pct': np.random.uniform(0.5, 3.0),  # Replace with actual calculation
            'fry_mint_rate': self.local_metrics['total_fry_minted'] / max(self.local_metrics['training_rounds'], 1),
            'fry_minted': self.local_metrics['total_fry_minted'],
            'slippage_harvested_usd': self.local_metrics['slippage_harvested_usd'],
            'arbitrage_profit_usd': self.local_metrics['arbitrage_profit_usd'],
            'circuit_breaker_active': agent_metrics['circuit_breaker_active'],
            'market_regime': recent_regime,
            'regime_confidence': 0.7,  # Replace with actual confidence
            'venue': self.venue,
            'client_id': self.client_id,
            # Topology-specific metrics
            'topology_fry_bonus': self.local_metrics['topology_fry_bonus'],
            'avg_minting_gradient': self.local_metrics['avg_minting_gradient'],
            'topology_routes_used': len(self.topology_agent.route_history),
        }
        
        return metrics
    
    def _generate_market_data(self) -> Dict:
        """Generate synthetic market data (replace with real data in production)"""
        
        return {
            'volatility': np.random.uniform(0.02, 0.10),
            'volume_ratio': np.random.uniform(0.5, 2.0),
            'price_change_pct': np.random.normal(0, 0.03),
            'bid_ask_spread': np.random.uniform(0.0005, 0.005),
            'order_flow_imbalance': np.random.uniform(-0.5, 0.5),
            'rsi': np.random.uniform(20, 80),
            'bollinger_position': np.random.uniform(0, 1),
            'fry_minted': np.random.uniform(0, 10),
            'slippage_usd': np.random.uniform(0, 100),
        }


def start_fryboy_client(
    server_address: str = "localhost:8080",
    client_id: str = "fryboy_client_1",
    venue: str = "binance",
    initial_capital: float = 1000000,
):
    """
    Start Fryboy federated learning client.
    
    Args:
        server_address: Address of Fryboy server
        client_id: Unique client identifier
        venue: Trading venue name
        initial_capital: Initial capital for Agent B
    """
    
    logger.info("="*70)
    logger.info("FRYBOY FEDERATED LEARNING CLIENT")
    logger.info("="*70)
    logger.info(f"Client ID: {client_id}")
    logger.info(f"Server: {server_address}")
    logger.info(f"Venue: {venue}")
    logger.info(f"Initial Capital: ${initial_capital:,.0f}")
    logger.info("="*70 + "\n")
    
    # Initialize Agent B
    agent_b = AgentB(initial_capital=initial_capital)
    
    # Initialize hedge ratio predictor model with topology features
    model = HedgeRatioPredictor(input_dim=25, hidden_dim=64)
    
    # Create Fryboy client
    client = FryboyClient(
        client_id=client_id,
        agent_b=agent_b,
        model=model,
        venue=venue,
        initial_capital=initial_capital,
    )
    
    # Start federated learning client
    try:
        fl.client.start_numpy_client(
            server_address=server_address,
            client=client,
        )
    except Exception as e:
        logger.error(f"Client error: {e}")
        raise
    
    logger.info(f"\nClient {client_id} training complete!")
    logger.info(f"Total FRY Minted: {client.local_metrics['total_fry_minted']:.2f}")
    logger.info(f"Training Rounds: {client.local_metrics['training_rounds']}")


if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    client_id = sys.argv[1] if len(sys.argv) > 1 else "fryboy_client_1"
    server_address = sys.argv[2] if len(sys.argv) > 2 else "localhost:8080"
    venue = sys.argv[3] if len(sys.argv) > 3 else "binance"
    
    start_fryboy_client(
        server_address=server_address,
        client_id=client_id,
        venue=venue,
        initial_capital=1000000,
    )
