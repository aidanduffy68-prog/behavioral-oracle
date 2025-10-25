#!/usr/bin/env python3
"""
Layer 3: Multi-Party Validation System
Chaos Labs-style approach with multiple data sources and consensus validation
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class DataSource(Enum):
    HYPERLIQUID_API = "hyperliquid_api"
    DYDX_SUBGRAPH = "dydx_subgraph"
    CHAINLINK_ORACLES = "chainlink_oracles"
    ONCHAIN_MONITORING = "onchain_monitoring"

class ValidationStatus(Enum):
    CONSENSUS = "consensus"
    DISAGREEMENT = "disagreement"
    INSUFFICIENT_DATA = "insufficient_data"
    ERROR = "error"

@dataclass
class LiquidationEvent:
    wallet_address: str
    liquidation_value: float
    timestamp: datetime
    chain: str
    asset: str
    price_at_liquidation: float
    source: DataSource

@dataclass
class ValidationResult:
    status: ValidationStatus
    consensus_value: Optional[float]
    source_disagreements: List[Dict]
    confidence_score: float
    validation_timestamp: datetime

class MultiPartyValidator:
    """
    Multi-party validation system following Chaos Labs approach
    Uses multiple data sources and requires consensus
    """
    
    def __init__(self):
        self.data_sources = {
            DataSource.HYPERLIQUID_API: HyperliquidValidator(),
            DataSource.DYDX_SUBGRAPH: DyDxValidator(),
            DataSource.CHAINLINK_ORACLES: ChainlinkValidator(),
            DataSource.ONCHAIN_MONITORING: OnChainValidator()
        }
        self.consensus_threshold = 0.75  # 75% agreement required
        self.max_price_deviation = 0.05  # 5% max deviation between sources
        self.validation_timeout = 30  # 30 seconds timeout per source
    
    async def validate_liquidation_event(self, event_data: Dict) -> ValidationResult:
        """
        Validate liquidation event using multiple data sources
        Follows Chaos Labs approach: pause oracle if sources disagree
        """
        
        # Extract basic event data
        wallet_address = event_data.get('wallet_address')
        timestamp = event_data.get('timestamp', datetime.now())
        chain = event_data.get('chain', 'arbitrum')
        asset = event_data.get('asset', 'ETH')
        
        # Collect data from all sources
        source_results = await self._collect_source_data(wallet_address, timestamp, chain, asset)
        
        # Check for consensus
        validation_result = self._check_consensus(source_results)
        
        # If no consensus, pause oracle
        if validation_result.status == ValidationStatus.DISAGREEMENT:
            await self._pause_oracle(validation_result)
        
        return validation_result
    
    async def _collect_source_data(self, wallet_address: str, timestamp: datetime, 
                                 chain: str, asset: str) -> Dict[DataSource, LiquidationEvent]:
        """Collect data from all sources with timeout"""
        
        source_results = {}
        tasks = []
        
        # Create async tasks for each source
        for source, validator in self.data_sources.items():
            task = asyncio.create_task(
                self._get_source_data_with_timeout(validator, wallet_address, timestamp, chain, asset)
            )
            tasks.append((source, task))
        
        # Wait for all tasks with timeout
        for source, task in tasks:
            try:
                result = await asyncio.wait_for(task, timeout=self.validation_timeout)
                if result:
                    source_results[source] = result
            except asyncio.TimeoutError:
                print(f"Timeout getting data from {source.value}")
            except Exception as e:
                print(f"Error getting data from {source.value}: {e}")
        
        return source_results
    
    async def _get_source_data_with_timeout(self, validator, wallet_address: str, 
                                          timestamp: datetime, chain: str, asset: str) -> Optional[LiquidationEvent]:
        """Get data from single source with error handling"""
        try:
            return await validator.get_liquidation_data(wallet_address, timestamp, chain, asset)
        except Exception as e:
            print(f"Error in validator {validator.__class__.__name__}: {e}")
            return None
    
    def _check_consensus(self, source_results: Dict[DataSource, LiquidationEvent]) -> ValidationResult:
        """Check consensus between data sources"""
        
        if len(source_results) < 2:
            return ValidationResult(
                status=ValidationStatus.INSUFFICIENT_DATA,
                consensus_value=None,
                source_disagreements=[],
                confidence_score=0.0,
                validation_timestamp=datetime.now()
            )
        
        # Extract liquidation values
        liquidation_values = []
        source_disagreements = []
        
        for source, event in source_results.items():
            liquidation_values.append(event.liquidation_value)
        
        # Calculate consensus
        if len(liquidation_values) >= 2:
            # Check if values are within acceptable range
            max_value = max(liquidation_values)
            min_value = min(liquidation_values)
            deviation = (max_value - min_value) / max_value if max_value > 0 else 0
            
            if deviation <= self.max_price_deviation:
                # Consensus reached
                consensus_value = sum(liquidation_values) / len(liquidation_values)
                confidence_score = 1.0 - (deviation / self.max_price_deviation)
                
                return ValidationResult(
                    status=ValidationStatus.CONSENSUS,
                    consensus_value=consensus_value,
                    source_disagreements=[],
                    confidence_score=confidence_score,
                    validation_timestamp=datetime.now()
                )
            else:
                # Sources disagree
                for i, source1 in enumerate(source_results.keys()):
                    for j, source2 in enumerate(source_results.keys()):
                        if i < j:
                            val1 = liquidation_values[i]
                            val2 = liquidation_values[j]
                            disagreement = abs(val1 - val2) / max(val1, val2)
                            
                            if disagreement > self.max_price_deviation:
                                source_disagreements.append({
                                    'source1': source1.value,
                                    'source2': source2.value,
                                    'value1': val1,
                                    'value2': val2,
                                    'disagreement_percent': disagreement * 100
                                })
                
                return ValidationResult(
                    status=ValidationStatus.DISAGREEMENT,
                    consensus_value=None,
                    source_disagreements=source_disagreements,
                    confidence_score=0.0,
                    validation_timestamp=datetime.now()
                )
        
        return ValidationResult(
            status=ValidationStatus.INSUFFICIENT_DATA,
            consensus_value=None,
            source_disagreements=[],
            confidence_score=0.0,
            validation_timestamp=datetime.now()
        )
    
    async def _pause_oracle(self, validation_result: ValidationResult):
        """Pause oracle when sources disagree - Chaos Labs approach"""
        
        print("🚨 ORACLE PAUSED - Data source disagreement detected")
        print(f"Disagreements: {len(validation_result.source_disagreements)}")
        
        for disagreement in validation_result.source_disagreements:
            print(f"  {disagreement['source1']} vs {disagreement['source2']}: "
                  f"{disagreement['disagreement_percent']:.2f}% difference")
        
        # Log the pause event
        await self._log_oracle_pause(validation_result)
        
        # Notify administrators
        await self._notify_administrators(validation_result)
        
        # Set oracle status to paused
        await self._set_oracle_status("PAUSED")
    
    async def _log_oracle_pause(self, validation_result: ValidationResult):
        """Log oracle pause event for audit trail"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'oracle_paused',
            'reason': 'data_source_disagreement',
            'disagreements': validation_result.source_disagreements,
            'sources_checked': len(validation_result.source_disagreements) + 1
        }
        
        # Log to file or database
        with open('oracle_pause_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    async def _notify_administrators(self, validation_result: ValidationResult):
        """Notify administrators of oracle pause"""
        # Send alerts to administrators
        # Could integrate with Slack, email, or other notification systems
        print("📧 Administrators notified of oracle pause")
    
    async def _set_oracle_status(self, status: str):
        """Set oracle status in system"""
        # Update oracle status in database or configuration
        print(f"🔧 Oracle status set to: {status}")

class HyperliquidValidator:
    """Primary data source: Hyperliquid API"""
    
    async def get_liquidation_data(self, wallet_address: str, timestamp: datetime, 
                                 chain: str, asset: str) -> LiquidationEvent:
        """Get liquidation data from Hyperliquid API"""
        
        # Simulate API call
        await asyncio.sleep(0.1)  # Simulate network delay
        
        # Mock data - replace with actual Hyperliquid API call
        return LiquidationEvent(
            wallet_address=wallet_address,
            liquidation_value=1500.0,  # Mock value
            timestamp=timestamp,
            chain=chain,
            asset=asset,
            price_at_liquidation=2000.0,  # Mock ETH price
            source=DataSource.HYPERLIQUID_API
        )

class DyDxValidator:
    """Validation source: dYdX subgraph"""
    
    async def get_liquidation_data(self, wallet_address: str, timestamp: datetime, 
                                 chain: str, asset: str) -> LiquidationEvent:
        """Get liquidation data from dYdX subgraph"""
        
        # Simulate subgraph query
        await asyncio.sleep(0.2)  # Simulate subgraph delay
        
        # Mock data - replace with actual dYdX subgraph query
        return LiquidationEvent(
            wallet_address=wallet_address,
            liquidation_value=1520.0,  # Slightly different mock value
            timestamp=timestamp,
            chain=chain,
            asset=asset,
            price_at_liquidation=2005.0,  # Slightly different price
            source=DataSource.DYDX_SUBGRAPH
        )

class ChainlinkValidator:
    """Price verification: Chainlink oracles"""
    
    async def get_liquidation_data(self, wallet_address: str, timestamp: datetime, 
                                 chain: str, asset: str) -> LiquidationEvent:
        """Get price data from Chainlink oracles"""
        
        # Simulate Chainlink oracle call
        await asyncio.sleep(0.15)  # Simulate oracle delay
        
        # Mock data - replace with actual Chainlink oracle call
        return LiquidationEvent(
            wallet_address=wallet_address,
            liquidation_value=1480.0,  # Different mock value
            timestamp=timestamp,
            chain=chain,
            asset=asset,
            price_at_liquidation=1995.0,  # Different price
            source=DataSource.CHAINLINK_ORACLES
        )

class OnChainValidator:
    """Independent check: On-chain monitoring"""
    
    async def get_liquidation_data(self, wallet_address: str, timestamp: datetime, 
                                 chain: str, asset: str) -> LiquidationEvent:
        """Get liquidation data from on-chain monitoring"""
        
        # Simulate on-chain monitoring
        await asyncio.sleep(0.3)  # Simulate on-chain delay
        
        # Mock data - replace with actual on-chain monitoring
        return LiquidationEvent(
            wallet_address=wallet_address,
            liquidation_value=1510.0,  # Another mock value
            timestamp=timestamp,
            chain=chain,
            asset=asset,
            price_at_liquidation=2002.0,  # Another price
            source=DataSource.ONCHAIN_MONITORING
        )

# Example usage
async def main():
    """Example usage of multi-party validation system"""
    
    validator = MultiPartyValidator()
    
    # Test event data
    test_event = {
        'wallet_address': '0x1234567890abcdef',
        'timestamp': datetime.now(),
        'chain': 'arbitrum',
        'asset': 'ETH'
    }
    
    # Validate the event
    result = await validator.validate_liquidation_event(test_event)
    
    print(f"Validation Status: {result.status.value}")
    print(f"Consensus Value: {result.consensus_value}")
    print(f"Confidence Score: {result.confidence_score:.2f}")
    print(f"Source Disagreements: {len(result.source_disagreements)}")
    
    if result.source_disagreements:
        print("Disagreements:")
        for disagreement in result.source_disagreements:
            print(f"  {disagreement['source1']} vs {disagreement['source2']}: "
                  f"{disagreement['disagreement_percent']:.2f}% difference")

if __name__ == "__main__":
    asyncio.run(main())
