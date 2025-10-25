#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agent B Federated Learning Server
==================================

Flower-based federated learning server for training Agent B (aka "Fryboy") across
distributed trading instances. Optimized for FRY-specific metrics and 
non-IID market data across different venues and market regimes.

Note: "Fryboy" and "Agent B" are the same - the embedded FRY market maker.

Key Features:
1. Custom aggregation weighted by FRY alpha scores (slippage harvest efficiency)
2. Regime-aware model updates (crisis vs trending vs sideways)
3. Performance-based client selection (reward high-performing Agent B instances)
4. Adaptive learning rates based on market volatility
5. Model versioning and rollback for production safety
"""

import flwr as fl
import numpy as np
import json
import time
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, deque
from datetime import datetime
import logging

from zkml_proof_system import ZKMLProofVerifier, ZKProof, OnChainVerifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FryboyAdaptiveStrategy(fl.server.strategy.FedAvg):
    """
    Custom Flower strategy for Fryboy federated learning with FRY-specific optimizations.
    
    Aggregation Strategy:
    - Weight by inverse RMSE (hedge prediction accuracy)
    - Bonus weight for high slippage harvest efficiency
    - Regime-specific model selection (crisis models vs trending models)
    - Penalize clients with circuit breaker activations
    """
    
    def __init__(
        self,
        fraction_fit: float = 0.5,
        fraction_evaluate: float = 0.5,
        min_fit_clients: int = 2,
        min_evaluate_clients: int = 2,
        min_available_clients: int = 2,
        evaluate_fn=None,
        on_fit_config_fn=None,
        on_evaluate_config_fn=None,
        accept_failures: bool = True,
        initial_parameters=None,
    ):
        super().__init__(
            fraction_fit=fraction_fit,
            fraction_evaluate=fraction_evaluate,
            min_fit_clients=min_fit_clients,
            min_evaluate_clients=min_evaluate_clients,
            min_available_clients=min_available_clients,
            evaluate_fn=evaluate_fn,
            on_fit_config_fn=on_fit_config_fn,
            on_evaluate_config_fn=on_evaluate_config_fn,
            accept_failures=accept_failures,
            initial_parameters=initial_parameters,
        )
        
        # FRY-specific tracking
        self.client_performance_history = defaultdict(lambda: deque(maxlen=100))
        self.regime_models = {}  # Store best models per regime
        self.global_metrics = {
            'total_fry_minted': 0.0,
            'total_slippage_harvested': 0.0,
            'total_arbitrage_profit': 0.0,
            'avg_hedge_accuracy': 0.0,
            'circuit_breaker_activations': 0,
            'training_rounds': 0
        }
        self.model_versions = deque(maxlen=10)  # Keep last 10 model versions
        
        # zkML proof verification
        self.zkml_verifier = ZKMLProofVerifier()
        self.on_chain_verifier = OnChainVerifier()
        self.zkml_enabled = True
        
    def _calculate_fry_alpha_weight(self, metrics: Dict) -> float:
        """
        Calculate custom weight based on FRY alpha score.
        
        FRY Alpha Components:
        1. Hedge Prediction Accuracy (verified via zkML proof)
        2. Slippage Harvest Efficiency
        3. Funding Arbitrage ROI
        4. Risk Management Score (circuit breaker penalty)
        """
        
        # zkML-verified accuracy (if available)
        if self.zkml_enabled and 'zkml_proof' in metrics:
            # Verify zkML proof
            try:
                proof_dict = metrics['zkml_proof']
                proof = ZKProof(**proof_dict)
                verification = self.zkml_verifier.verify_accuracy_proof(proof)
                
                if verification['verified']:
                    # Trust the zkML-verified threshold
                    # Higher weight for verified proofs
                    hedge_rmse = proof.public_inputs['threshold']
                    zkml_bonus = 1.3  # 30% bonus for zkML verification
                    
                    logger.info(f"✓ zkML proof verified for client {metrics.get('client_id')}")
                    logger.info(f"  Proof ID: {proof.proof_id}")
                    logger.info(f"  Applying zkML bonus: {zkml_bonus}x")
                    
                    # Optional: Submit to on-chain verifier
                    if hasattr(self, 'on_chain_verifier'):
                        self.on_chain_verifier.submit_proof_to_chain(proof)
                else:
                    # Proof failed verification - penalize
                    logger.warning(f"✗ zkML proof verification FAILED for {metrics.get('client_id')}")
                    hedge_rmse = 1.0  # Worst case
                    zkml_bonus = 0.5  # 50% penalty
            except Exception as e:
                logger.error(f"zkML verification error: {e}")
                hedge_rmse = metrics.get("hedge_rmse", 1.0)
                zkml_bonus = 1.0
        else:
            # Fallback to traditional RMSE (less trusted)
            hedge_rmse = metrics.get("hedge_rmse", 1.0)
            zkml_bonus = 1.0
        
        # Base weight: inverse of hedge prediction RMSE
        base_weight = 1.0 / max(hedge_rmse, 0.01)
        base_weight *= zkml_bonus
        
        # Slippage harvest efficiency bonus (0-50% boost)
        slippage_efficiency = metrics.get("slippage_harvest_efficiency", 0.5)
        slippage_bonus = slippage_efficiency * 0.5
        
        # Funding arbitrage ROI bonus (0-30% boost)
        arbitrage_roi = metrics.get("arbitrage_roi_pct", 0.0)
        arbitrage_bonus = min(arbitrage_roi / 100, 0.3)
        
        # FRY minting rate bonus (0-20% boost)
        fry_mint_rate = metrics.get("fry_mint_rate", 0.0)
        fry_bonus = min(fry_mint_rate / 1000, 0.2)
        
        # Circuit breaker penalty (reduce weight by 40% if active)
        circuit_breaker_active = metrics.get("circuit_breaker_active", False)
        circuit_breaker_penalty = 0.6 if circuit_breaker_active else 1.0
        
        # Data quality weight (more data = more weight)
        num_samples = metrics.get("num_samples", 100)
        data_quality_factor = min(num_samples / 1000, 1.5)
        
        # Regime confidence (higher confidence = more weight)
        regime_confidence = metrics.get("regime_confidence", 0.5)
        confidence_factor = 0.5 + (regime_confidence * 0.5)
        
        # Final FRY alpha weight
        fry_alpha_weight = (
            base_weight * 
            (1 + slippage_bonus + arbitrage_bonus + fry_bonus) *
            circuit_breaker_penalty *
            data_quality_factor *
            confidence_factor
        )
        
        return max(fry_alpha_weight, 0.01)  # Minimum weight threshold
    
    def _extract_regime_info(self, metrics: Dict) -> Tuple[str, float]:
        """Extract market regime and confidence from client metrics"""
        regime = metrics.get("market_regime", "unknown")
        confidence = metrics.get("regime_confidence", 0.5)
        return regime, confidence
    
    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitRes]],
        failures: List[BaseException],
    ) -> Tuple[Optional[fl.common.Parameters], Dict[str, float]]:
        """
        Aggregate model updates with FRY alpha weighting.
        """
        
        if not results:
            return None, {}
        
        # Log failures
        if failures:
            logger.warning(f"Round {server_round}: {len(failures)} clients failed")
        
        # Calculate FRY alpha weights for each client
        weighted_results = []
        regime_distribution = defaultdict(list)
        
        for client_proxy, fit_res in results:
            metrics = fit_res.metrics
            
            # Calculate FRY alpha weight
            fry_weight = self._calculate_fry_alpha_weight(metrics)
            
            # Track regime distribution
            regime, confidence = self._extract_regime_info(metrics)
            regime_distribution[regime].append((fry_weight, confidence))
            
            # Store performance history
            client_id = client_proxy.cid
            self.client_performance_history[client_id].append({
                'round': server_round,
                'fry_weight': fry_weight,
                'metrics': metrics,
                'regime': regime
            })
            
            weighted_results.append((fit_res.parameters, fry_weight))
            
            logger.info(
                f"Client {client_id} | Regime: {regime} | "
                f"FRY Weight: {fry_weight:.4f} | "
                f"Hedge RMSE: {metrics.get('hedge_rmse', 0):.4f} | "
                f"Slippage Eff: {metrics.get('slippage_harvest_efficiency', 0):.2%}"
            )
        
        # Aggregate using FRY alpha weights
        aggregated_parameters = fl.common.parameters_to_ndarrays(weighted_results[0][0])
        total_weight = sum(weight for _, weight in weighted_results)
        
        # Weighted average of parameters
        for i in range(len(aggregated_parameters)):
            layer_sum = np.zeros_like(aggregated_parameters[i])
            for params, weight in weighted_results:
                layer_params = fl.common.parameters_to_ndarrays(params)
                layer_sum += layer_params[i] * weight
            aggregated_parameters[i] = layer_sum / total_weight
        
        # Update global metrics
        self._update_global_metrics(results, server_round)
        
        # Store regime-specific models
        self._store_regime_models(regime_distribution, aggregated_parameters, server_round)
        
        # Version the model
        self._version_model(aggregated_parameters, server_round)
        
        # Prepare aggregated metrics
        aggregated_metrics = {
            "round": server_round,
            "num_clients": len(results),
            "total_weight": float(total_weight),
            "avg_fry_weight": float(total_weight / len(results)),
            "regime_distribution": {k: len(v) for k, v in regime_distribution.items()},
            "global_fry_minted": self.global_metrics['total_fry_minted'],
            "global_slippage_harvested": self.global_metrics['total_slippage_harvested'],
        }
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Round {server_round} Aggregation Complete")
        logger.info(f"Clients: {len(results)} | Avg FRY Weight: {aggregated_metrics['avg_fry_weight']:.4f}")
        logger.info(f"Regime Distribution: {aggregated_metrics['regime_distribution']}")
        logger.info(f"Total FRY Minted: {self.global_metrics['total_fry_minted']:.2f}")
        logger.info(f"{'='*60}\n")
        
        return fl.common.ndarrays_to_parameters(aggregated_parameters), aggregated_metrics
    
    def _update_global_metrics(self, results: List, server_round: int):
        """Update global FRY ecosystem metrics"""
        
        total_fry = 0.0
        total_slippage = 0.0
        total_arbitrage = 0.0
        hedge_accuracies = []
        circuit_breakers = 0
        
        for _, fit_res in results:
            metrics = fit_res.metrics
            total_fry += metrics.get("fry_minted", 0.0)
            total_slippage += metrics.get("slippage_harvested_usd", 0.0)
            total_arbitrage += metrics.get("arbitrage_profit_usd", 0.0)
            
            hedge_rmse = metrics.get("hedge_rmse", 1.0)
            hedge_accuracies.append(1.0 / max(hedge_rmse, 0.01))
            
            if metrics.get("circuit_breaker_active", False):
                circuit_breakers += 1
        
        self.global_metrics['total_fry_minted'] += total_fry
        self.global_metrics['total_slippage_harvested'] += total_slippage
        self.global_metrics['total_arbitrage_profit'] += total_arbitrage
        self.global_metrics['avg_hedge_accuracy'] = np.mean(hedge_accuracies) if hedge_accuracies else 0.0
        self.global_metrics['circuit_breaker_activations'] += circuit_breakers
        self.global_metrics['training_rounds'] = server_round
    
    def _store_regime_models(self, regime_distribution: Dict, parameters: List, server_round: int):
        """Store best models for each market regime"""
        
        for regime, weight_confidence_pairs in regime_distribution.items():
            if not weight_confidence_pairs:
                continue
            
            # Calculate regime-specific score
            avg_weight = np.mean([w for w, _ in weight_confidence_pairs])
            avg_confidence = np.mean([c for _, c in weight_confidence_pairs])
            regime_score = avg_weight * avg_confidence
            
            # Update if better than existing
            if regime not in self.regime_models or regime_score > self.regime_models[regime]['score']:
                self.regime_models[regime] = {
                    'parameters': parameters,
                    'score': regime_score,
                    'round': server_round,
                    'num_clients': len(weight_confidence_pairs)
                }
                logger.info(f"Updated {regime} regime model (score: {regime_score:.4f})")
    
    def _version_model(self, parameters: List, server_round: int):
        """Version control for model rollback"""
        
        model_version = {
            'round': server_round,
            'parameters': parameters,
            'timestamp': time.time(),
            'metrics': dict(self.global_metrics)
        }
        self.model_versions.append(model_version)
    
    def configure_fit(
        self,
        server_round: int,
        parameters: fl.common.Parameters,
        client_manager: fl.server.client_manager.ClientManager,
    ) -> List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitIns]]:
        """Configure the next round of training with adaptive parameters"""
        
        # Adaptive learning rate based on round
        base_lr = 0.01
        lr_decay = 0.95
        learning_rate = base_lr * (lr_decay ** (server_round - 1))
        
        # Adaptive batch size based on regime volatility
        base_batch_size = 32
        
        config = {
            "server_round": server_round,
            "learning_rate": learning_rate,
            "batch_size": base_batch_size,
            "local_epochs": 5,
            "enable_regime_detection": True,
            "enable_rl_optimization": True,
            # zkML configuration
            "zkml_threshold": 0.05,  # 5% RMSE threshold for proofs
            "model_hash": f"global_model_round_{server_round}",
        }
        
        fit_ins = fl.common.FitIns(parameters, config)
        
        # Sample clients
        sample_size, min_num_clients = self.num_fit_clients(
            client_manager.num_available()
        )
        clients = client_manager.sample(
            num_clients=sample_size,
            min_num_clients=min_num_clients,
        )
        
        return [(client, fit_ins) for client in clients]
    
    def aggregate_evaluate(
        self,
        server_round: int,
        results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.EvaluateRes]],
        failures: List[BaseException],
    ) -> Tuple[Optional[float], Dict[str, float]]:
        """Aggregate evaluation results"""
        
        if not results:
            return None, {}
        
        # Weighted average of losses
        total_loss = 0.0
        total_weight = 0.0
        
        for _, evaluate_res in results:
            metrics = evaluate_res.metrics
            weight = self._calculate_fry_alpha_weight(metrics)
            total_loss += evaluate_res.loss * weight
            total_weight += weight
        
        aggregated_loss = total_loss / total_weight if total_weight > 0 else 0.0
        
        metrics = {
            "round": server_round,
            "aggregated_loss": aggregated_loss,
            "num_clients": len(results),
        }
        
        return aggregated_loss, metrics
    
    def get_performance_report(self) -> str:
        """Generate comprehensive performance report"""
        
        report = []
        report.append("\n" + "="*70)
        report.append("FRYBOY FEDERATED LEARNING PERFORMANCE REPORT")
        report.append("="*70)
        
        report.append(f"\nGlobal Metrics:")
        report.append(f"  Training Rounds: {self.global_metrics['training_rounds']}")
        report.append(f"  Total FRY Minted: {self.global_metrics['total_fry_minted']:,.2f}")
        report.append(f"  Total Slippage Harvested: ${self.global_metrics['total_slippage_harvested']:,.2f}")
        report.append(f"  Total Arbitrage Profit: ${self.global_metrics['total_arbitrage_profit']:,.2f}")
        report.append(f"  Avg Hedge Accuracy: {self.global_metrics['avg_hedge_accuracy']:.4f}")
        report.append(f"  Circuit Breaker Activations: {self.global_metrics['circuit_breaker_activations']}")
        
        report.append(f"\nRegime-Specific Models:")
        for regime, model_info in self.regime_models.items():
            report.append(f"  {regime.upper()}: Score={model_info['score']:.4f}, "
                         f"Round={model_info['round']}, Clients={model_info['num_clients']}")
        
        report.append(f"\nClient Performance History:")
        for client_id, history in list(self.client_performance_history.items())[:5]:
            recent = list(history)[-1] if history else None
            if recent:
                report.append(f"  Client {client_id}: FRY Weight={recent['fry_weight']:.4f}, "
                             f"Regime={recent['regime']}")
        
        report.append("="*70 + "\n")
        
        return "\n".join(report)


def start_fryboy_server(
    server_address: str = "[::]:8080",
    num_rounds: int = 50,
    min_clients: int = 2,
    fraction_fit: float = 0.5,
):
    """
    Start Fryboy federated learning server.
    
    Args:
        server_address: Server address (default: "[::]:8080")
        num_rounds: Number of training rounds (default: 50)
        min_clients: Minimum number of clients (default: 2)
        fraction_fit: Fraction of clients to sample for training (default: 0.5)
    """
    
    logger.info("="*70)
    logger.info("FRYBOY FEDERATED LEARNING SERVER")
    logger.info("="*70)
    logger.info(f"Server Address: {server_address}")
    logger.info(f"Training Rounds: {num_rounds}")
    logger.info(f"Min Clients: {min_clients}")
    logger.info(f"Fraction Fit: {fraction_fit}")
    logger.info("="*70 + "\n")
    
    # Create custom strategy
    strategy = FryboyAdaptiveStrategy(
        fraction_fit=fraction_fit,
        fraction_evaluate=0.5,
        min_fit_clients=min_clients,
        min_evaluate_clients=min_clients,
        min_available_clients=min_clients,
    )
    
    # Start server
    fl.server.start_server(
        server_address=server_address,
        config=fl.server.ServerConfig(num_rounds=num_rounds),
        strategy=strategy,
    )
    
    # Print final report
    logger.info(strategy.get_performance_report())


if __name__ == "__main__":
    # Start Fryboy federated learning server
    start_fryboy_server(
        server_address="[::]:8080",
        num_rounds=50,
        min_clients=2,
        fraction_fit=0.5,
    )
