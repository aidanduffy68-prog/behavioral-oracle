#!/usr/bin/env python3
"""
🔌 Behavioral Intelligence API Integration
Chaos Labs Oracle Enhancement

This module provides API endpoints for integrating behavioral intelligence
with Chaos Labs' existing oracle infrastructure.

New API Endpoints:
- /behavioral-risk/{wallet}
- /retention-probability/{trader}
- /echo-patterns/{asset}
- /cross-chain-correlation/{chain}
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from dataclasses import dataclass
import asyncio
import aiohttp

app = Flask(__name__)
CORS(app)

@dataclass
class BehavioralRiskScore:
    """Behavioral risk assessment for a wallet"""
    wallet_address: str
    narcissus_score: float
    self_deception_level: float
    risk_tolerance: float
    echo_potential: float
    behavioral_risk_level: str
    retention_probability: float
    last_updated: datetime

@dataclass
class EchoPattern:
    """Echo pattern detection for an asset"""
    asset: str
    pattern_name: str
    coherence: float
    amplification_factor: float
    affected_wallets: int
    cross_chain_correlation: float
    risk_level: str

class BehavioralIntelligenceAPI:
    """API service for behavioral intelligence integration"""
    
    def __init__(self, db_path: str = "data/behavioral_intelligence.db"):
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self):
        """Setup behavioral intelligence database"""
        import os
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Behavioral risk scores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS behavioral_risk_scores (
                id INTEGER PRIMARY KEY,
                wallet_address TEXT UNIQUE,
                narcissus_score REAL,
                self_deception_level REAL,
                risk_tolerance REAL,
                echo_potential REAL,
                behavioral_risk_level TEXT,
                retention_probability REAL,
                last_updated DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Echo patterns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS echo_patterns (
                id INTEGER PRIMARY KEY,
                asset TEXT,
                pattern_name TEXT,
                coherence REAL,
                amplification_factor REAL,
                affected_wallets INTEGER,
                cross_chain_correlation REAL,
                risk_level TEXT,
                detected_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Cross-chain correlations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cross_chain_correlations (
                id INTEGER PRIMARY KEY,
                chain_1 TEXT,
                chain_2 TEXT,
                correlation_strength REAL,
                behavioral_pattern TEXT,
                universality_score REAL,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_behavioral_risk(self, wallet_address: str) -> BehavioralRiskScore:
        """Get behavioral risk score for a wallet"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if we have recent data
        cursor.execute("""
            SELECT * FROM behavioral_risk_scores 
            WHERE wallet_address = ? 
            AND last_updated > datetime('now', '-1 hour')
        """, (wallet_address,))
        
        result = cursor.fetchone()
        
        if result:
            # Return cached data
            conn.close()
            return BehavioralRiskScore(
                wallet_address=result[1],
                narcissus_score=result[2],
                self_deception_level=result[3],
                risk_tolerance=result[4],
                echo_potential=result[5],
                behavioral_risk_level=result[6],
                retention_probability=result[7],
                last_updated=datetime.fromisoformat(result[8])
            )
        
        # Generate new behavioral risk score
        risk_score = self._calculate_behavioral_risk(wallet_address)
        
        # Store in database
        cursor.execute("""
            INSERT OR REPLACE INTO behavioral_risk_scores 
            (wallet_address, narcissus_score, self_deception_level, risk_tolerance, 
             echo_potential, behavioral_risk_level, retention_probability, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            wallet_address, risk_score.narcissus_score, risk_score.self_deception_level,
            risk_score.risk_tolerance, risk_score.echo_potential, risk_score.behavioral_risk_level,
            risk_score.retention_probability, risk_score.last_updated.isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return risk_score
    
    def _calculate_behavioral_risk(self, wallet_address: str) -> BehavioralRiskScore:
        """Calculate behavioral risk score for a wallet"""
        
        # Simulate behavioral analysis (replace with real implementation)
        narcissus_score = np.random.beta(2, 3)  # Skewed toward lower scores
        self_deception_level = np.random.beta(3, 2)  # Skewed toward higher deception
        risk_tolerance = np.random.beta(2, 5)  # Skewed toward lower risk
        echo_potential = np.random.beta(2, 4)  # Skewed toward lower echo
        
        # Calculate behavioral risk level
        if narcissus_score > 0.8:
            behavioral_risk_level = "HIGH"
            retention_probability = 0.15
        elif narcissus_score > 0.6:
            behavioral_risk_level = "MEDIUM"
            retention_probability = 0.35
        else:
            behavioral_risk_level = "LOW"
            retention_probability = 0.65
        
        return BehavioralRiskScore(
            wallet_address=wallet_address,
            narcissus_score=narcissus_score,
            self_deception_level=self_deception_level,
            risk_tolerance=risk_tolerance,
            echo_potential=echo_potential,
            behavioral_risk_level=behavioral_risk_level,
            retention_probability=retention_probability,
            last_updated=datetime.now()
        )
    
    def get_retention_probability(self, trader_address: str) -> Dict:
        """Get retention probability for a trader"""
        
        behavioral_risk = self.get_behavioral_risk(trader_address)
        
        return {
            "trader_address": trader_address,
            "retention_probability": behavioral_risk.retention_probability,
            "confidence_level": "HIGH" if behavioral_risk.narcissus_score < 0.6 else "MEDIUM",
            "risk_factors": {
                "narcissus_score": behavioral_risk.narcissus_score,
                "self_deception_level": behavioral_risk.self_deception_level,
                "behavioral_risk_level": behavioral_risk.behavioral_risk_level
            },
            "recommendations": self._get_retention_recommendations(behavioral_risk),
            "last_updated": behavioral_risk.last_updated.isoformat()
        }
    
    def _get_retention_recommendations(self, risk_score: BehavioralRiskScore) -> List[str]:
        """Get retention recommendations based on behavioral risk"""
        
        recommendations = []
        
        if risk_score.narcissus_score > 0.8:
            recommendations.extend([
                "High liquidation risk - consider reducing leverage",
                "Self-destructive pattern detected - intervention recommended",
                "Low retention probability - focus on risk management"
            ])
        elif risk_score.narcissus_score > 0.6:
            recommendations.extend([
                "Moderate risk - monitor behavioral patterns",
                "Consider educational resources for risk awareness",
                "Medium retention probability - engagement strategies needed"
            ])
        else:
            recommendations.extend([
                "Low risk trader - likely to return",
                "Good retention candidate - maintain engagement",
                "High retention probability - optimize incentives"
            ])
        
        return recommendations
    
    def get_echo_patterns(self, asset: str) -> List[EchoPattern]:
        """Get echo patterns for an asset"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent echo patterns for the asset
        cursor.execute("""
            SELECT * FROM echo_patterns 
            WHERE asset = ? 
            AND detected_at > datetime('now', '-24 hours')
            ORDER BY detected_at DESC
        """, (asset,))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            return [EchoPattern(
                asset=result[1],
                pattern_name=result[2],
                coherence=result[3],
                amplification_factor=result[4],
                affected_wallets=result[5],
                cross_chain_correlation=result[6],
                risk_level=result[7]
            ) for result in results]
        
        # Generate sample echo patterns
        return self._generate_sample_echo_patterns(asset)
    
    def _generate_sample_echo_patterns(self, asset: str) -> List[EchoPattern]:
        """Generate sample echo patterns for an asset"""
        
        patterns = [
            EchoPattern(
                asset=asset,
                pattern_name="leverage_addiction",
                coherence=0.85,
                amplification_factor=0.72,
                affected_wallets=15,
                cross_chain_correlation=0.91,
                risk_level="HIGH"
            ),
            EchoPattern(
                asset=asset,
                pattern_name="blue_chip_gambling",
                coherence=0.78,
                amplification_factor=0.65,
                affected_wallets=23,
                cross_chain_correlation=0.87,
                risk_level="MEDIUM"
            ),
            EchoPattern(
                asset=asset,
                pattern_name="risk_escalation",
                coherence=0.92,
                amplification_factor=0.88,
                affected_wallets=8,
                cross_chain_correlation=0.94,
                risk_level="HIGH"
            )
        ]
        
        return patterns
    
    def get_cross_chain_correlation(self, chain: str) -> Dict:
        """Get cross-chain behavioral correlations for a chain"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get correlations involving the specified chain
        cursor.execute("""
            SELECT * FROM cross_chain_correlations 
            WHERE chain_1 = ? OR chain_2 = ?
            ORDER BY correlation_strength DESC
        """, (chain, chain))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            correlations = []
            for result in results:
                other_chain = result[2] if result[1] == chain else result[1]
                correlations.append({
                    "chain": other_chain,
                    "correlation_strength": result[3],
                    "behavioral_pattern": result[4],
                    "universality_score": result[5],
                    "last_updated": result[6]
                })
            
            return {
                "source_chain": chain,
                "correlations": correlations,
                "average_correlation": np.mean([c["correlation_strength"] for c in correlations]),
                "universality_score": np.mean([c["universality_score"] for c in correlations])
            }
        
        # Generate sample correlations
        return self._generate_sample_correlations(chain)
    
    def _generate_sample_correlations(self, chain: str) -> Dict:
        """Generate sample cross-chain correlations"""
        
        other_chains = ["Ethereum", "Solana", "Arbitrum", "Polygon", "Base"]
        other_chains = [c for c in other_chains if c != chain]
        
        correlations = []
        for other_chain in other_chains:
            correlation_strength = np.random.uniform(0.7, 0.95)
            correlations.append({
                "chain": other_chain,
                "correlation_strength": correlation_strength,
                "behavioral_pattern": np.random.choice([
                    "leverage_addiction", "blue_chip_gambling", 
                    "risk_escalation", "liquidation_cycle"
                ]),
                "universality_score": np.random.uniform(0.8, 1.0),
                "last_updated": datetime.now().isoformat()
            })
        
        return {
            "source_chain": chain,
            "correlations": correlations,
            "average_correlation": np.mean([c["correlation_strength"] for c in correlations]),
            "universality_score": np.mean([c["universality_score"] for c in correlations])
        }

# Initialize API service
api_service = BehavioralIntelligenceAPI()

# API Routes
@app.route('/behavioral-risk/<wallet_address>', methods=['GET'])
def get_behavioral_risk_endpoint(wallet_address: str):
    """Get behavioral risk score for a wallet"""
    try:
        risk_score = api_service.get_behavioral_risk(wallet_address)
        
        return jsonify({
            "wallet_address": risk_score.wallet_address,
            "narcissus_score": risk_score.narcissus_score,
            "self_deception_level": risk_score.self_deception_level,
            "risk_tolerance": risk_score.risk_tolerance,
            "echo_potential": risk_score.echo_potential,
            "behavioral_risk_level": risk_score.behavioral_risk_level,
            "retention_probability": risk_score.retention_probability,
            "last_updated": risk_score.last_updated.isoformat(),
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/retention-probability/<trader_address>', methods=['GET'])
def get_retention_probability_endpoint(trader_address: str):
    """Get retention probability for a trader"""
    try:
        retention_data = api_service.get_retention_probability(trader_address)
        return jsonify({**retention_data, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/echo-patterns/<asset>', methods=['GET'])
def get_echo_patterns_endpoint(asset: str):
    """Get echo patterns for an asset"""
    try:
        patterns = api_service.get_echo_patterns(asset)
        
        return jsonify({
            "asset": asset,
            "patterns": [
                {
                    "pattern_name": pattern.pattern_name,
                    "coherence": pattern.coherence,
                    "amplification_factor": pattern.amplification_factor,
                    "affected_wallets": pattern.affected_wallets,
                    "cross_chain_correlation": pattern.cross_chain_correlation,
                    "risk_level": pattern.risk_level
                }
                for pattern in patterns
            ],
            "total_patterns": len(patterns),
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/cross-chain-correlation/<chain>', methods=['GET'])
def get_cross_chain_correlation_endpoint(chain: str):
    """Get cross-chain behavioral correlations for a chain"""
    try:
        correlation_data = api_service.get_cross_chain_correlation(chain)
        return jsonify({**correlation_data, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Behavioral Intelligence API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/chaos-integration/risk-parameters', methods=['POST'])
def enhanced_risk_parameters():
    """Enhanced risk parameters combining Chaos market risk + behavioral risk"""
    try:
        data = request.get_json()
        wallet_address = data.get('wallet_address')
        asset = data.get('asset')
        
        # Get behavioral risk
        behavioral_risk = api_service.get_behavioral_risk(wallet_address)
        
        # Get echo patterns
        echo_patterns = api_service.get_echo_patterns(asset)
        
        # Calculate enhanced risk parameters
        enhanced_params = {
            "wallet_address": wallet_address,
            "asset": asset,
            "market_risk": {
                "funding_rate": data.get('funding_rate', 0.01),
                "open_interest_cap": data.get('open_interest_cap', 1000000),
                "liquidation_threshold": data.get('liquidation_threshold', 0.8)
            },
            "behavioral_risk": {
                "narcissus_score": behavioral_risk.narcissus_score,
                "self_deception_level": behavioral_risk.self_deception_level,
                "retention_probability": behavioral_risk.retention_probability,
                "behavioral_risk_level": behavioral_risk.behavioral_risk_level
            },
            "echo_patterns": [
                {
                    "pattern_name": pattern.pattern_name,
                    "coherence": pattern.coherence,
                    "amplification_factor": pattern.amplification_factor,
                    "risk_level": pattern.risk_level
                }
                for pattern in echo_patterns
            ],
            "enhanced_recommendations": {
                "adjusted_funding_rate": data.get('funding_rate', 0.01) * (1 + behavioral_risk.narcissus_score * 0.1),
                "adjusted_liquidation_threshold": data.get('liquidation_threshold', 0.8) * (1 - behavioral_risk.narcissus_score * 0.05),
                "retention_incentive_multiplier": behavioral_risk.retention_probability * 2,
                "risk_warning": "HIGH" if behavioral_risk.narcissus_score > 0.8 else "NORMAL"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify({**enhanced_params, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == "__main__":
    print("🔌 Starting Behavioral Intelligence API...")
    print("📡 Available endpoints:")
    print("  GET  /behavioral-risk/{wallet}")
    print("  GET  /retention-probability/{trader}")
    print("  GET  /echo-patterns/{asset}")
    print("  GET  /cross-chain-correlation/{chain}")
    print("  POST /chaos-integration/risk-parameters")
    print("  GET  /health")
    print("\n🚀 API ready for Chaos Labs integration!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

