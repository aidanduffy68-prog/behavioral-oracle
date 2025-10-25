#!/usr/bin/env python3
"""
Complete Validation Framework
Integrates all three validation layers:
1. Input Validation
2. Anomaly Detection  
3. Multi-Party Validation
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from multi_party_validator import MultiPartyValidator, ValidationStatus
from input_validator import InputValidator
from anomaly_detector import AnomalyDetector
from credibility_scorer import CredibilityScorer, CredibilityTier

class ValidationLayer(Enum):
    INPUT_VALIDATION = "input_validation"
    ANOMALY_DETECTION = "anomaly_detection"
    MULTI_PARTY_VALIDATION = "multi_party_validation"
    CREDIBILITY_SCORING = "credibility_scoring"

@dataclass
class CompleteValidationResult:
    """Complete validation result from all four layers"""
    input_valid: bool
    input_reason: Optional[str]
    anomalies_detected: List[Dict]
    multi_party_status: ValidationStatus
    consensus_value: Optional[float]
    confidence_score: float
    credibility_score: float
    credibility_tier: CredibilityTier
    weighted_data: Dict
    overall_valid: bool
    validation_timestamp: datetime
    layer_results: Dict[ValidationLayer, bool]

class CompleteValidator:
    """
    Complete validation system integrating all four layers
    Follows Chaos Labs approach with comprehensive validation
    """
    
    def __init__(self):
        self.input_validator = InputValidator()
        self.anomaly_detector = AnomalyDetector()
        self.multi_party_validator = MultiPartyValidator()
        self.credibility_scorer = CredibilityScorer()
        
        # Validation thresholds
        self.min_confidence_score = 0.7
        self.max_anomalies = 2
        self.require_all_layers = True
        self.min_credibility_score = 0.3  # Minimum credibility for processing
    
    async def validate_complete_event(self, event_data: Dict, recent_events: List[Dict], wallet_data: Dict = None) -> CompleteValidationResult:
        """
        Complete validation pipeline:
        1. Input validation
        2. Anomaly detection
        3. Multi-party validation
        4. Credibility scoring
        """
        
        validation_timestamp = datetime.now()
        layer_results = {}
        
        # Layer 1: Input Validation
        input_valid, input_reason = self.input_validator.validate_liquidation_event(event_data)
        layer_results[ValidationLayer.INPUT_VALIDATION] = input_valid
        
        if not input_valid:
            return CompleteValidationResult(
                input_valid=False,
                input_reason=input_reason,
                anomalies_detected=[],
                multi_party_status=ValidationStatus.ERROR,
                consensus_value=None,
                confidence_score=0.0,
                overall_valid=False,
                validation_timestamp=validation_timestamp,
                layer_results=layer_results
            )
        
        # Layer 2: Anomaly Detection
        anomalies = self.anomaly_detector.detect_anomalies(recent_events)
        layer_results[ValidationLayer.ANOMALY_DETECTION] = len(anomalies) <= self.max_anomalies
        
        if len(anomalies) > self.max_anomalies:
            return CompleteValidationResult(
                input_valid=True,
                input_reason=None,
                anomalies_detected=anomalies,
                multi_party_status=ValidationStatus.ERROR,
                consensus_value=None,
                confidence_score=0.0,
                overall_valid=False,
                validation_timestamp=validation_timestamp,
                layer_results=layer_results
            )
        
        # Layer 3: Multi-Party Validation
        multi_party_result = await self.multi_party_validator.validate_liquidation_event(event_data)
        layer_results[ValidationLayer.MULTI_PARTY_VALIDATION] = multi_party_result.status == ValidationStatus.CONSENSUS
        
        # Layer 4: Credibility Scoring
        if wallet_data:
            credibility_score_obj = self.credibility_scorer.calculate_credibility_score(wallet_data)
            credibility_passed = credibility_score_obj.overall_score >= self.min_credibility_score
            layer_results[ValidationLayer.CREDIBILITY_SCORING] = credibility_passed
            
            # Weight event data by credibility
            weighted_data = self.credibility_scorer.weight_data_by_credibility(event_data, credibility_score_obj)
        else:
            # Default credibility if no wallet data provided
            credibility_score_obj = None
            credibility_passed = True  # Don't fail if no wallet data
            layer_results[ValidationLayer.CREDIBILITY_SCORING] = credibility_passed
            weighted_data = event_data.copy()
            weighted_data['credibility_weight'] = 0.5  # Default weight
        
        # Determine overall validity
        overall_valid = self._determine_overall_validity(layer_results, multi_party_result, credibility_score_obj)
        
        return CompleteValidationResult(
            input_valid=input_valid,
            input_reason=input_reason,
            anomalies_detected=anomalies,
            multi_party_status=multi_party_result.status,
            consensus_value=multi_party_result.consensus_value,
            confidence_score=multi_party_result.confidence_score,
            credibility_score=credibility_score_obj.overall_score if credibility_score_obj else 0.5,
            credibility_tier=credibility_score_obj.tier if credibility_score_obj else CredibilityTier.MEDIUM,
            weighted_data=weighted_data,
            overall_valid=overall_valid,
            validation_timestamp=validation_timestamp,
            layer_results=layer_results
        )
    
    def _determine_overall_validity(self, layer_results: Dict[ValidationLayer, bool], 
                                  multi_party_result, credibility_score_obj) -> bool:
        """Determine if event passes overall validation"""
        
        # All layers must pass if require_all_layers is True
        if self.require_all_layers:
            return (all(layer_results.values()) and 
                   multi_party_result.status == ValidationStatus.CONSENSUS)
        
        # At least input validation, multi-party consensus, and minimum credibility required
        credibility_check = True
        if credibility_score_obj:
            credibility_check = credibility_score_obj.overall_score >= self.min_credibility_score
        
        return (layer_results[ValidationLayer.INPUT_VALIDATION] and 
                multi_party_result.status == ValidationStatus.CONSENSUS and
                multi_party_result.confidence_score >= self.min_confidence_score and
                credibility_check)
    
    async def validate_batch_events(self, events: List[Dict], recent_events: List[Dict]) -> List[CompleteValidationResult]:
        """Validate multiple events in batch"""
        
        tasks = []
        for event in events:
            task = self.validate_complete_event(event, recent_events)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
    
    def get_validation_summary(self, results: List[CompleteValidationResult]) -> Dict:
        """Get summary statistics from validation results"""
        
        total_events = len(results)
        valid_events = sum(1 for r in results if r.overall_valid)
        invalid_events = total_events - valid_events
        
        # Layer breakdown
        input_valid = sum(1 for r in results if r.input_valid)
        anomaly_valid = sum(1 for r in results if len(r.anomalies_detected) <= self.max_anomalies)
        multi_party_valid = sum(1 for r in results if r.multi_party_status == ValidationStatus.CONSENSUS)
        credibility_valid = sum(1 for r in results if r.credibility_score >= self.min_credibility_score)
        
        # Average scores
        avg_confidence = sum(r.confidence_score for r in results) / total_events if total_events > 0 else 0
        avg_credibility = sum(r.credibility_score for r in results) / total_events if total_events > 0 else 0
        
        # Credibility tier distribution
        tier_counts = {}
        for tier in CredibilityTier:
            tier_counts[tier.value] = sum(1 for r in results if r.credibility_tier == tier)
        
        return {
            'total_events': total_events,
            'valid_events': valid_events,
            'invalid_events': invalid_events,
            'validation_rate': valid_events / total_events if total_events > 0 else 0,
            'layer_breakdown': {
                'input_validation': input_valid,
                'anomaly_detection': anomaly_valid,
                'multi_party_validation': multi_party_valid,
                'credibility_scoring': credibility_valid
            },
            'average_confidence_score': avg_confidence,
            'average_credibility_score': avg_credibility,
            'credibility_tier_distribution': tier_counts,
            'high_credibility_rate': tier_counts.get('high', 0) / total_events if total_events > 0 else 0,
            'unreliable_rate': tier_counts.get('unreliable', 0) / total_events if total_events > 0 else 0,
            'validation_timestamp': datetime.now().isoformat()
        }

# Example usage
async def main():
    """Example usage of complete validation system"""
    
    validator = CompleteValidator()
    
    # Test event data
    test_event = {
        'wallet_address': '0x1234567890abcdef',
        'liquidation_value': 1500.0,
        'wallet_age_days': 45,
        'total_trades': 25,
        'timestamp': datetime.now(),
        'chain': 'arbitrum',
        'asset': 'ETH'
    }
    
    # Mock wallet data for credibility scoring
    wallet_data = {
        'wallet_address': '0x1234567890abcdef',
        'wallet_age_days': 180,
        'lifetime_volume': 500_000,
        'total_trades': 45,
        'num_chains_active': 3,
        'cross_chain_volume': 200_000,
        'has_ens_domain': True,
        'twitter_linked': True,
        'github_linked': False,
        'discord_active': True,
        'owns_nfts': True,
        'defi_protocols_used': 5,
        'kyc_verified': False,
        'is_multisig': False,
        'uses_hardware_wallet': True,
        'protocol_reputation_score': 0.8
    }
    
    # Mock recent events for anomaly detection
    recent_events = [
        {
            'wallet_address': '0x1234567890abcdef',
            'behavioral_pattern': 'conservative',
            'timestamp': datetime.now(),
            'chain': 'arbitrum'
        }
    ]
    
    # Validate the event
    result = await validator.validate_complete_event(test_event, recent_events, wallet_data)
    
    print("=== Complete Validation Result ===")
    print(f"Overall Valid: {result.overall_valid}")
    print(f"Input Valid: {result.input_valid}")
    print(f"Input Reason: {result.input_reason}")
    print(f"Anomalies Detected: {len(result.anomalies_detected)}")
    print(f"Multi-Party Status: {result.multi_party_status.value}")
    print(f"Consensus Value: {result.consensus_value}")
    print(f"Confidence Score: {result.confidence_score:.2f}")
    print(f"Credibility Score: {result.credibility_score:.2f}")
    print(f"Credibility Tier: {result.credibility_tier.value}")
    print(f"Weighted Value: ${result.weighted_data.get('liquidation_value', 0):.2f}")
    print(f"Validation Timestamp: {result.validation_timestamp}")
    
    print("\n=== Layer Results ===")
    for layer, passed in result.layer_results.items():
        print(f"{layer.value}: {'PASS' if passed else 'FAIL'}")

if __name__ == "__main__":
    asyncio.run(main())
