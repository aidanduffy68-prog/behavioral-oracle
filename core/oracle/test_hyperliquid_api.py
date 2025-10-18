#!/usr/bin/env python3
"""
Test Hyperliquid API access and understand data structure.
"""

import requests
import json
from datetime import datetime

def test_hyperliquid_api():
    """Test various Hyperliquid API endpoints."""
    base_url = "https://api.hyperliquid.xyz/info"
    
    print("="*60)
    print("TESTING HYPERLIQUID API")
    print("="*60)
    print()
    
    # Test 1: Get metadata
    print("📡 Test 1: Fetching metadata...")
    try:
        payload = {"type": "meta"}
        response = requests.post(base_url, json=payload, timeout=10)
        response.raise_for_status()
        meta = response.json()
        print("✅ Success!")
        print(f"Response: {json.dumps(meta, indent=2)[:500]}...")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 2: Get all mids (current prices)
    print("📡 Test 2: Fetching current prices...")
    try:
        payload = {"type": "allMids"}
        response = requests.post(base_url, json=payload, timeout=10)
        response.raise_for_status()
        mids = response.json()
        print("✅ Success!")
        print(f"Found {len(mids)} assets")
        if mids:
            print(f"Sample: {list(mids.items())[:3]}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 3: Get user fills (need real wallet address)
    print("📡 Test 3: Testing user fills endpoint...")
    print("⚠️  Need real wallet address to test")
    print("   Example usage:")
    print("   payload = {'type': 'userFills', 'user': '0x...'}")
    print()
    
    # Test 4: Get user state
    print("📡 Test 4: Testing user state endpoint...")
    print("⚠️  Need real wallet address to test")
    print("   Example usage:")
    print("   payload = {'type': 'clearinghouseState', 'user': '0x...'}")
    print()
    
    print("="*60)
    print("NEXT STEPS")
    print("="*60)
    print("1. Get list of liquidated wallets from October 10")
    print("2. Query each wallet's fills to find liquidation events")
    print("3. Track those wallets for 30-day activity")
    print("4. Populate FRY retention oracle")
    print("="*60)

if __name__ == "__main__":
    test_hyperliquid_api()
