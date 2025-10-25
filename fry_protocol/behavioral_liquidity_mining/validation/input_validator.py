#!/usr/bin/env python3
"""
Input Validation Module
Layer 1: Input validation before data enters the oracle
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional
import re

class InputValidator:
    """
    Input validation system for liquidation events
    Ensures data quality before processing
    """
    
    def __init__(self):
        self.min_wallet_age_days = 30
        self.min_total_trades = 10
        self.min_liquidation_value = 1000.0
        self.max_liquidation_value = 1000000.0  # Prevent unrealistic values
    
    def validate_liquidation_event(self, event: dict) -> Tuple[bool, Optional[str]]:
        """
        Validate liquidation event before processing
        Returns (is_valid, reason_if_invalid)
        """
        
        # Extract event data
        wallet_address = event.get('wallet_address')
        liquidation_value = event.get('liquidation_value', 0)
        wallet_age_days = event.get('wallet_age_days', 0)
        total_trades = event.get('total_trades', 0)
        
        # Validate wallet address
        if not self._is_valid_wallet_address(wallet_address):
            return False, "Invalid wallet address format"
        
        # Validate wallet age
        if wallet_age_days < self.min_wallet_age_days:
            return False, f"Wallet too new ({wallet_age_days} days < {self.min_wallet_age_days} days)"
        
        # Validate trading history
        if total_trades < self.min_total_trades:
            return False, f"Insufficient trading history ({total_trades} < {self.min_total_trades} trades)"
        
        # Validate liquidation value
        if liquidation_value < self.min_liquidation_value:
            return False, f"Liquidation value too small (${liquidation_value} < ${self.min_liquidation_value})"
        
        if liquidation_value > self.max_liquidation_value:
            return False, f"Liquidation value too large (${liquidation_value} > ${self.max_liquidation_value})"
        
        # Check for known bot patterns
        if self._is_known_bot(wallet_address):
            return False, "Known bot wallet detected"
        
        # Validate cross-chain activity
        if not self._has_sufficient_chain_activity(wallet_address):
            return False, "Insufficient cross-chain activity"
        
        return True, None
    
    def _is_valid_wallet_address(self, address: str) -> bool:
        """Validate wallet address format"""
        if not address:
            return False
        
        # Check Ethereum address format
        if re.match(r'^0x[a-fA-F0-9]{40}$', address):
            return True
        
        # Check Solana address format
        if re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', address):
            return True
        
        return False
    
    def _is_known_bot(self, wallet_address: str) -> bool:
        """Check if wallet matches known bot patterns"""
        # Mock implementation - replace with actual bot detection
        known_bots = [
            '0x0000000000000000000000000000000000000000',  # Example bot address
            '0x1111111111111111111111111111111111111111'   # Example bot address
        ]
        
        return wallet_address.lower() in [bot.lower() for bot in known_bots]
    
    def _has_sufficient_chain_activity(self, wallet_address: str) -> bool:
        """Ensure wallet has activity across multiple chains"""
        # Mock implementation - replace with actual cross-chain check
        # For now, assume all addresses have sufficient activity
        return True
    
    def validate_batch_events(self, events: list) -> list:
        """Validate multiple events"""
        results = []
        for event in events:
            is_valid, reason = self.validate_liquidation_event(event)
            results.append({
                'event': event,
                'valid': is_valid,
                'reason': reason
            })
        return results
