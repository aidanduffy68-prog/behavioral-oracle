#!/usr/bin/env python3
"""
Layer 4: Credibility Scoring System
Weight data by source credibility and wallet reputation
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class CredibilityTier(Enum):
    HIGH = "high"          # 0.8-1.0
    MEDIUM = "medium"      # 0.5-0.8
    LOW = "low"           # 0.2-0.5
    UNRELIABLE = "unreliable"  # 0.0-0.2

@dataclass
class CredibilityScore:
    """Comprehensive credibility score for a wallet"""
    wallet_address: str
    overall_score: float
    tier: CredibilityTier
    age_score: float
    volume_score: float
    cross_chain_score: float
    social_score: float
    verification_score: float
    risk_factors: List[str]
    confidence_level: float
    last_updated: datetime

class CredibilityScorer:
    """
    Comprehensive credibility scoring system
    Weights data by source credibility and wallet reputation
    """
    
    def __init__(self):
        # Scoring weights
        self.weights = {
            'age_and_activity': 0.25,
            'trading_volume': 0.25,
            'cross_chain_presence': 0.20,
            'social_signals': 0.15,
            'verification_status': 0.15
        }
        
        # Thresholds
        self.min_age_days = 30
        self.max_age_days = 365 * 3  # 3 years max benefit
        self.min_volume = 1000
        self.max_volume = 10_000_000  # $10M max benefit
        self.max_chains = 5
        
        # Risk factors
        self.risk_factors = {
            'new_wallet': 0.3,
            'low_volume': 0.2,
            'single_chain': 0.15,
            'no_social_presence': 0.1,
            'suspicious_patterns': 0.25
        }
    
    def calculate_credibility_score(self, wallet_data: Dict) -> CredibilityScore:
        """
        Calculate comprehensive credibility score for a wallet
        """
        
        wallet_address = wallet_data.get('wallet_address', '')
        
        # Calculate individual component scores
        age_score = self._calculate_age_score(wallet_data)
        volume_score = self._calculate_volume_score(wallet_data)
        cross_chain_score = self._calculate_cross_chain_score(wallet_data)
        social_score = self._calculate_social_score(wallet_data)
        verification_score = self._calculate_verification_score(wallet_data)
        
        # Calculate weighted overall score
        overall_score = (
            age_score * self.weights['age_and_activity'] +
            volume_score * self.weights['trading_volume'] +
            cross_chain_score * self.weights['cross_chain_presence'] +
            social_score * self.weights['social_signals'] +
            verification_score * self.weights['verification_status']
        )
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(wallet_data, overall_score)
        
        # Apply risk factor penalties
        penalty = sum(self.risk_factors.get(factor, 0) for factor in risk_factors)
        overall_score = max(0.0, overall_score - penalty)
        
        # Determine credibility tier
        tier = self._determine_credibility_tier(overall_score)
        
        # Calculate confidence level
        confidence_level = self._calculate_confidence_level(wallet_data, overall_score)
        
        return CredibilityScore(
            wallet_address=wallet_address,
            overall_score=overall_score,
            tier=tier,
            age_score=age_score,
            volume_score=volume_score,
            cross_chain_score=cross_chain_score,
            social_score=social_score,
            verification_score=verification_score,
            risk_factors=risk_factors,
            confidence_level=confidence_level,
            last_updated=datetime.now()
        )
    
    def _calculate_age_score(self, wallet_data: Dict) -> float:
        """Calculate age and activity score"""
        wallet_age_days = wallet_data.get('wallet_age_days', 0)
        total_trades = wallet_data.get('total_trades', 0)
        
        # Age component (0-1)
        age_component = min(wallet_age_days / self.max_age_days, 1.0)
        
        # Activity component (0-1)
        activity_component = min(total_trades / 100, 1.0)  # 100 trades = max activity score
        
        # Combined age and activity score
        return (age_component * 0.7 + activity_component * 0.3)
    
    def _calculate_volume_score(self, wallet_data: Dict) -> float:
        """Calculate trading volume score"""
        lifetime_volume = wallet_data.get('lifetime_volume', 0)
        
        if lifetime_volume < self.min_volume:
            return 0.0
        
        # Volume score (0-1)
        volume_component = min(lifetime_volume / self.max_volume, 1.0)
        
        # Add bonus for consistent volume over time
        consistency_bonus = self._calculate_volume_consistency(wallet_data)
        
        return min(1.0, volume_component + consistency_bonus)
    
    def _calculate_volume_consistency(self, wallet_data: Dict) -> float:
        """Calculate volume consistency bonus"""
        # Mock implementation - replace with actual consistency calculation
        # Could analyze volume patterns over time
        return 0.1  # 10% bonus for consistent volume
    
    def _calculate_cross_chain_score(self, wallet_data: Dict) -> float:
        """Calculate cross-chain presence score"""
        num_chains_active = wallet_data.get('num_chains_active', 1)
        cross_chain_volume = wallet_data.get('cross_chain_volume', 0)
        
        # Chain diversity component (0-1)
        chain_component = min(num_chains_active / self.max_chains, 1.0)
        
        # Cross-chain volume component (0-1)
        volume_component = min(cross_chain_volume / 1_000_000, 1.0)  # $1M max
        
        return (chain_component * 0.6 + volume_component * 0.4)
    
    def _calculate_social_score(self, wallet_data: Dict) -> float:
        """Calculate social signals score"""
        score = 0.0
        
        # ENS domain
        if wallet_data.get('has_ens_domain', False):
            score += 0.3
        
        # Twitter linked
        if wallet_data.get('twitter_linked', False):
            score += 0.2
        
        # GitHub linked
        if wallet_data.get('github_linked', False):
            score += 0.2
        
        # Discord presence
        if wallet_data.get('discord_active', False):
            score += 0.1
        
        # NFT ownership (indicates human user)
        if wallet_data.get('owns_nfts', False):
            score += 0.1
        
        # DeFi protocol participation
        if wallet_data.get('defi_protocols_used', 0) > 3:
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_verification_score(self, wallet_data: Dict) -> float:
        """Calculate verification status score"""
        score = 0.0
        
        # KYC verification (if available)
        if wallet_data.get('kyc_verified', False):
            score += 0.4
        
        # Multi-sig wallet
        if wallet_data.get('is_multisig', False):
            score += 0.3
        
        # Hardware wallet usage
        if wallet_data.get('uses_hardware_wallet', False):
            score += 0.2
        
        # Reputation from other protocols
        if wallet_data.get('protocol_reputation_score', 0) > 0.7:
            score += 0.1
        
        return min(1.0, score)
    
    def _identify_risk_factors(self, wallet_data: Dict, overall_score: float) -> List[str]:
        """Identify risk factors that could affect credibility"""
        risk_factors = []
        
        wallet_age_days = wallet_data.get('wallet_age_days', 0)
        lifetime_volume = wallet_data.get('lifetime_volume', 0)
        num_chains_active = wallet_data.get('num_chains_active', 1)
        has_social_presence = any([
            wallet_data.get('has_ens_domain', False),
            wallet_data.get('twitter_linked', False),
            wallet_data.get('github_linked', False)
        ])
        
        # New wallet risk
        if wallet_age_days < 90:
            risk_factors.append('new_wallet')
        
        # Low volume risk
        if lifetime_volume < 10_000:
            risk_factors.append('low_volume')
        
        # Single chain risk
        if num_chains_active == 1:
            risk_factors.append('single_chain')
        
        # No social presence risk
        if not has_social_presence:
            risk_factors.append('no_social_presence')
        
        # Suspicious patterns risk
        if self._detect_suspicious_patterns(wallet_data):
            risk_factors.append('suspicious_patterns')
        
        return risk_factors
    
    def _detect_suspicious_patterns(self, wallet_data: Dict) -> bool:
        """Detect suspicious patterns that could indicate bot behavior"""
        # Mock implementation - replace with actual pattern detection
        # Could check for:
        # - Identical transaction amounts
        # - Regular timing patterns
        # - Lack of human-like behavior
        return False
    
    def _determine_credibility_tier(self, score: float) -> CredibilityTier:
        """Determine credibility tier based on score"""
        if score >= 0.8:
            return CredibilityTier.HIGH
        elif score >= 0.5:
            return CredibilityTier.MEDIUM
        elif score >= 0.2:
            return CredibilityTier.LOW
        else:
            return CredibilityTier.UNRELIABLE
    
    def _calculate_confidence_level(self, wallet_data: Dict, overall_score: float) -> float:
        """Calculate confidence level in the credibility score"""
        # Base confidence on data completeness
        data_completeness = self._calculate_data_completeness(wallet_data)
        
        # Adjust confidence based on score consistency
        score_consistency = self._calculate_score_consistency(wallet_data)
        
        # Combined confidence level
        confidence = (data_completeness * 0.6 + score_consistency * 0.4)
        
        return min(1.0, confidence)
    
    def _calculate_data_completeness(self, wallet_data: Dict) -> float:
        """Calculate how complete the wallet data is"""
        required_fields = [
            'wallet_age_days', 'lifetime_volume', 'num_chains_active',
            'total_trades', 'has_ens_domain', 'twitter_linked'
        ]
        
        present_fields = sum(1 for field in required_fields if field in wallet_data)
        return present_fields / len(required_fields)
    
    def _calculate_score_consistency(self, wallet_data: Dict) -> float:
        """Calculate consistency of individual score components"""
        # Mock implementation - could analyze historical score changes
        return 0.8  # 80% consistency
    
    def weight_data_by_credibility(self, event_data: Dict, credibility_score: CredibilityScore) -> Dict:
        """Weight event data based on wallet credibility"""
        
        # Apply credibility weighting to event data
        weighted_data = event_data.copy()
        
        # Weight liquidation value by credibility
        original_value = event_data.get('liquidation_value', 0)
        weighted_value = original_value * credibility_score.overall_score
        weighted_data['liquidation_value'] = weighted_value
        weighted_data['credibility_weight'] = credibility_score.overall_score
        
        # Weight behavioral patterns by credibility
        if 'behavioral_pattern' in event_data:
            weighted_data['pattern_confidence'] = (
                event_data.get('pattern_confidence', 0.5) * credibility_score.overall_score
            )
        
        # Add credibility metadata
        weighted_data['credibility_metadata'] = {
            'tier': credibility_score.tier.value,
            'risk_factors': credibility_score.risk_factors,
            'confidence_level': credibility_score.confidence_level,
            'last_updated': credibility_score.last_updated.isoformat()
        }
        
        return weighted_data
    
    def batch_score_wallets(self, wallets_data: List[Dict]) -> List[CredibilityScore]:
        """Calculate credibility scores for multiple wallets"""
        scores = []
        for wallet_data in wallets_data:
            score = self.calculate_credibility_score(wallet_data)
            scores.append(score)
        return scores
    
    def get_credibility_summary(self, scores: List[CredibilityScore]) -> Dict:
        """Get summary statistics for credibility scores"""
        if not scores:
            return {}
        
        total_wallets = len(scores)
        tier_counts = {tier.value: 0 for tier in CredibilityTier}
        
        for score in scores:
            tier_counts[score.tier.value] += 1
        
        avg_score = sum(s.overall_score for s in scores) / total_wallets
        avg_confidence = sum(s.confidence_level for s in scores) / total_wallets
        
        return {
            'total_wallets': total_wallets,
            'average_score': avg_score,
            'average_confidence': avg_confidence,
            'tier_distribution': tier_counts,
            'high_credibility_rate': tier_counts['high'] / total_wallets,
            'unreliable_rate': tier_counts['unreliable'] / total_wallets
        }

# Example usage
def main():
    """Example usage of credibility scoring system"""
    
    scorer = CredibilityScorer()
    
    # Example wallet data
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
    
    # Calculate credibility score
    credibility_score = scorer.calculate_credibility_score(wallet_data)
    
    print("=== Credibility Score ===")
    print(f"Wallet: {credibility_score.wallet_address}")
    print(f"Overall Score: {credibility_score.overall_score:.3f}")
    print(f"Tier: {credibility_score.tier.value}")
    print(f"Confidence Level: {credibility_score.confidence_level:.3f}")
    print(f"Risk Factors: {credibility_score.risk_factors}")
    
    print("\n=== Component Scores ===")
    print(f"Age Score: {credibility_score.age_score:.3f}")
    print(f"Volume Score: {credibility_score.volume_score:.3f}")
    print(f"Cross-Chain Score: {credibility_score.cross_chain_score:.3f}")
    print(f"Social Score: {credibility_score.social_score:.3f}")
    print(f"Verification Score: {credibility_score.verification_score:.3f}")
    
    # Example event data weighting
    event_data = {
        'wallet_address': '0x1234567890abcdef',
        'liquidation_value': 1500.0,
        'behavioral_pattern': 'conservative',
        'pattern_confidence': 0.8
    }
    
    weighted_data = scorer.weight_data_by_credibility(event_data, credibility_score)
    
    print("\n=== Weighted Event Data ===")
    print(f"Original Value: ${event_data['liquidation_value']}")
    print(f"Weighted Value: ${weighted_data['liquidation_value']:.2f}")
    print(f"Credibility Weight: {weighted_data['credibility_weight']:.3f}")
    print(f"Pattern Confidence: {weighted_data['pattern_confidence']:.3f}")

if __name__ == "__main__":
    main()
