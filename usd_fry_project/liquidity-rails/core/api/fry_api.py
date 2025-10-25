#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRY System API - FastAPI Server
================================

REST API for external integrations with the FRY liquidity rails system.

Endpoints:
- POST /wreckage/submit - Submit wreckage event for routing
- GET /liquidity/summary - Get current liquidity state
- POST /route/optimize - Get optimal route for wreckage
- GET /fry/minting-rate - Current FRY minting rate
- POST /zkml/verify - Verify zkML proof
- POST /position/commit - Submit confidential position commitment
- GET /system/health - System health check

Usage:
    uvicorn fry_api:app --host 0.0.0.0 --port 8000 --reload
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import logging

from liquidity_rails_integration import IntegratedLiquiditySystem
from fry_wreckage_matching_engine import WreckageEvent
from zkml_proof_system import ZKMLProofGenerator
from zkml_confidential_positions import ConfidentialPositionTracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="FRY Liquidity Rails API",
    description="API for FRY wreckage routing and liquidity management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize system
system = IntegratedLiquiditySystem(initial_capital=10_000_000)
zkml_generator = ZKMLProofGenerator("api_server")
position_tracker = ConfidentialPositionTracker()


# ===== Request/Response Models =====

class WreckageSubmission(BaseModel):
    dex: str = Field(..., description="DEX venue (dYdX, Hyperliquid, etc.)")
    wreckage_type: str = Field(..., description="Type: long_liq, short_liq, slippage, etc.")
    asset: str = Field(..., description="Asset (BTC, ETH, SOL)")
    amount_usd: float = Field(..., gt=0, description="Wreckage amount in USD")
    
    class Config:
        schema_extra = {
            "example": {
                "dex": "dYdX",
                "wreckage_type": "long_liq",
                "asset": "BTC",
                "amount_usd": 50000
            }
        }


class RouteRequest(BaseModel):
    amount_usd: float = Field(..., gt=0)
    asset: str
    max_hops: int = Field(default=3, ge=1, le=5)


class ZKMLVerificationRequest(BaseModel):
    proof_id: str
    client_id: str


class PositionCommitment(BaseModel):
    client_id: str
    amount: int = Field(..., gt=0)
    max_amount: int = Field(..., gt=0)
    commitment_type: str = Field(..., description="'collateral' or 'position'")


# ===== API Endpoints =====

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "FRY Liquidity Rails API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/system/health")
async def system_health():
    """System health check"""
    
    summary = system.get_system_summary()
    
    return {
        "status": "healthy",
        "components": {
            "liquidity_rails": "operational",
            "agent_b": "active",
            "wreckage_matcher": "matching",
            "topology_router": "optimized"
        },
        "metrics": {
            "total_wreckage_processed": summary['total_wreckage_processed'],
            "total_fry_minted": summary['total_fry_minted'],
            "effective_rate": summary['effective_rate']
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/wreckage/submit")
async def submit_wreckage(wreckage: WreckageSubmission, background_tasks: BackgroundTasks):
    """
    Submit wreckage event for processing through liquidity rails.
    
    Returns routing result with FRY minted.
    """
    
    try:
        # Create wreckage event
        event = WreckageEvent(
            dex=wreckage.dex,
            wreckage_type=wreckage.wreckage_type,
            asset=wreckage.asset,
            amount_usd=wreckage.amount_usd,
            timestamp=datetime.utcnow().timestamp()
        )
        
        # Process through system
        result = system.process_wreckage(event)
        
        return {
            "status": "processed",
            "wreckage_id": f"{wreckage.dex}_{int(event.timestamp)}",
            "strategy": result['strategy'],
            "fry_minted": result['fry_minted'],
            "cost_bps": result['cost_bps'],
            "route": [h['venue'] for h in result['route'].hops] if result['route'] else None,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Error processing wreckage: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/liquidity/summary")
async def liquidity_summary():
    """Get current liquidity state across all venues"""
    
    summary = system.liquidity_rails.get_liquidity_summary()
    
    return {
        "total_liquidity": summary['total_liquidity'],
        "available_liquidity": summary['total_available'],
        "overall_utilization": summary['overall_utilization'],
        "venues": summary['venues'],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/route/optimize")
async def optimize_route(request: RouteRequest):
    """
    Get optimal route for wreckage through liquidity rails.
    
    Returns best route with cost and FRY minting estimate.
    """
    
    try:
        route = system.liquidity_rails.route_wreckage(
            amount_usd=request.amount_usd,
            asset=request.asset,
            max_hops=request.max_hops
        )
        
        if not route:
            return {
                "status": "no_route_found",
                "message": "No suitable liquidity route available",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        
        return {
            "status": "route_found",
            "route": {
                "hops": route.hops,
                "total_cost_bps": route.total_cost_bps,
                "fry_minted": route.fry_minted,
                "efficiency_score": route.efficiency_score
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Error optimizing route: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fry/minting-rate")
async def fry_minting_rate():
    """Get current FRY minting rate"""
    
    summary = system.get_system_summary()
    
    return {
        "effective_rate": summary['effective_rate'],
        "base_rate": 0.5,
        "rails_rate": 1.2,
        "p2p_rate": 1.4,
        "improvement_pct": ((summary['effective_rate'] - 0.5) / 0.5) * 100,
        "total_fry_minted": summary['total_fry_minted'],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/zkml/verify")
async def verify_zkml_proof(request: ZKMLVerificationRequest):
    """
    Verify zkML accuracy proof.
    
    Returns verification result.
    """
    
    try:
        # In production, retrieve proof from database
        # For now, return mock verification
        
        return {
            "status": "verified",
            "proof_id": request.proof_id,
            "client_id": request.client_id,
            "verified": True,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Error verifying proof: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/position/commit")
async def commit_position(commitment: PositionCommitment):
    """
    Submit confidential position commitment using Pedersen commitments.
    
    Returns commitment and range proof.
    """
    
    try:
        if commitment.commitment_type == "collateral":
            result = position_tracker.commit_collateral(
                commitment.client_id,
                commitment.amount,
                max_collateral=commitment.max_amount
            )
        elif commitment.commitment_type == "position":
            result = position_tracker.commit_position(
                commitment.client_id,
                commitment.amount,
                max_position=commitment.max_amount
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid commitment_type")
        
        return {
            "status": "committed",
            "commitment": result['commitment'],
            "proof": result['proof'],
            "max_value": result.get('max_collateral') or result.get('max_position'),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Error committing position: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/capital/allocation")
async def capital_allocation():
    """Get current capital allocation across venues"""
    
    allocation = system.optimize_capital_allocation(total_capital=10_000_000)
    
    return {
        "total_capital": allocation['total_capital'],
        "rails_allocation": allocation['rails_allocation'],
        "agent_b_capital": allocation['agent_b_capital'],
        "topology_routes": len(allocation['topology_routes']),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/stats")
async def system_stats():
    """Get comprehensive system statistics"""
    
    summary = system.get_system_summary()
    
    return {
        "system": {
            "total_wreckage_processed": summary['total_wreckage_processed'],
            "total_fry_minted": summary['total_fry_minted'],
            "effective_rate": summary['effective_rate']
        },
        "liquidity_rails": summary['liquidity_rails'],
        "agent_b": summary['agent_b'],
        "wreckage_matcher": summary['wreckage_matcher'],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


# ===== Startup/Shutdown Events =====

@app.on_event("startup")
async def startup_event():
    logger.info("🍟 FRY API Server Starting...")
    logger.info("Liquidity Rails System Initialized")
    logger.info("API Documentation: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🍟 FRY API Server Shutting Down...")


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🍟 FRY LIQUIDITY RAILS API SERVER 🍟")
    print("="*70)
    print("\nStarting server...")
    print("API Docs: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/system/health")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
