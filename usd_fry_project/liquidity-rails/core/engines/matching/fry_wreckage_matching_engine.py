#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRY Funding Rate Swap Matching Engine
======================================

A variant of FRY that uses funding rate swaps instead of token swaps to match
wreckage across DEXes (dYdX, Hyperliquid, Aster, etc.) in a peer-to-peer system.

Core Concept:
- Market makers on different DEXes experience losses (wreckage) from adverse selection,
  slippage, liquidations, and funding imbalances.
- Instead of physically trading tokens, participants swap funding rate exposure.
- Long liquidations on one DEX (negative funding exposure) swap with short liquidations
  on another (positive funding exposure).
- Funding rate swaps are cash-settled based on actual funding payments.
- Matched swaps mint FRY at enhanced rates; unmatched wreckage mints at base rates.
- Creates a cross-DEX loss-netting layer via synthetic exposure without token movement.

Features:
- Wreckage collection from multiple DEXes
- Funding rate swap matching algorithm
- Cash-settled swap execution (no token transfers)
- Enhanced FRY minting for matched swap pairs
- Real-time matching dashboard simulation

Usage:
    python3 core/fry_wreckage_matching_engine.py
"""

import random
import time
from datetime import datetime
from typing import List, Dict, Tuple

# FRY color scheme for terminal
FRY_RED = "\033[91m"
FRY_YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# DEX venues
DEXES = ["dYdX", "Hyperliquid", "Aster", "GMX", "Vertex"]

# Wreckage types
WRECKAGE_TYPES = {
    "long_liq": "Long Liquidation",
    "short_liq": "Short Liquidation",
    "adverse_fill": "Adverse Fill (MM)",
    "funding_loss": "Funding Rate Loss",
    "slippage": "Slippage Loss"
}


class WreckageEvent:
    """Represents a single wreckage event from a DEX with funding rate exposure"""
    
    def __init__(self, dex: str, wreckage_type: str, asset: str, amount_usd: float, timestamp: float):
        self.dex = dex
        self.wreckage_type = wreckage_type
        self.asset = asset
        self.amount_usd = amount_usd
        self.timestamp = timestamp
        self.matched = False
        self.match_partner = None
        
        # Funding rate exposure (annualized)
        self.funding_exposure = self._calculate_funding_exposure()
        
    def _calculate_funding_exposure(self) -> float:
        """Calculate funding rate exposure based on wreckage type"""
        # Long liqs = negative funding exposure (paid funding)
        # Short liqs = positive funding exposure (received funding)
        if self.wreckage_type == "long_liq":
            return -random.uniform(0.05, 0.25)  # -5% to -25% annualized
        elif self.wreckage_type == "short_liq":
            return random.uniform(0.05, 0.25)   # +5% to +25% annualized
        elif self.wreckage_type == "funding_loss":
            return random.uniform(-0.15, 0.15)  # Variable exposure
        else:
            return random.uniform(-0.10, 0.10)  # Other types have smaller exposure
        
    def __repr__(self):
        return f"<Wreckage {self.dex} {self.wreckage_type} ${self.amount_usd:.2f} {self.asset} funding={self.funding_exposure:.2%}>"
    
    def is_offsetting(self, other: 'WreckageEvent') -> bool:
        """Check if two wreckage events can offset via funding rate swap"""
        # Same asset required
        if self.asset != other.asset:
            return False
        
        # Different DEXes (cross-venue matching)
        if self.dex == other.dex:
            return False
        
        # Opposite funding exposure signs (one pays, one receives)
        if (self.funding_exposure * other.funding_exposure) >= 0:
            return False  # Same sign, can't offset
        
        return True


class FRYWreckageMatchingEngine:
    """Cross-DEX funding rate swap matching and FRY minting engine"""
    
    def __init__(self):
        self.wreckage_pool: List[WreckageEvent] = []
        self.matched_pairs: List[Tuple[WreckageEvent, WreckageEvent]] = []
        self.funding_swaps: List[Dict] = []  # Track swap details
        self.total_fry_minted = 0.0
        self.total_wreckage_collected = 0.0
        self.total_swap_notional = 0.0
        
        # Minting rates
        self.base_fry_rate = 0.5  # 0.5 FRY per $1 wreckage (unmatched)
        self.swap_fry_rate = 1.4  # 1.4 FRY per $1 wreckage (funding swap matched)
        self.funding_efficiency_bonus = 1.8  # Bonus for funding rate swap efficiency
        
        print(FRY_RED + BOLD + "🔄 FRY Funding Rate Swap Matching Engine Initialized" + RESET)
        print(DIM + "Cross-DEX loss netting via cash-settled funding swaps" + RESET)
    
    def collect_wreckage(self, event: WreckageEvent):
        """Add wreckage event to the pool"""
        self.wreckage_pool.append(event)
        self.total_wreckage_collected += event.amount_usd
    
    def match_wreckage(self) -> int:
        """
        Match offsetting wreckage events across DEXes
        Returns number of new matches found
        """
        matches_found = 0
        unmatched = [w for w in self.wreckage_pool if not w.matched]
        
        for i, w1 in enumerate(unmatched):
            if w1.matched:
                continue
                
            for w2 in unmatched[i+1:]:
                if w2.matched:
                    continue
                
                if w1.is_offsetting(w2):
                    # Match found!
                    w1.matched = True
                    w2.matched = True
                    w1.match_partner = w2
                    w2.match_partner = w1
                    
                    self.matched_pairs.append((w1, w2))
                    matches_found += 1
                    
                    # Mint FRY for matched pair
                    self._mint_matched_pair(w1, w2)
                    break
        
        # Mint FRY for remaining unmatched wreckage at base rate
        still_unmatched = [w for w in self.wreckage_pool if not w.matched]
        for w in still_unmatched:
            self._mint_unmatched(w)
            w.matched = True  # Mark as processed
        
        return matches_found
    
    def _mint_matched_pair(self, w1: WreckageEvent, w2: WreckageEvent):
        """Mint FRY for a matched funding rate swap at enhanced rate"""
        total_wreckage = w1.amount_usd + w2.amount_usd
        
        # Calculate swap notional and hedge efficiency
        swap_notional = min(w1.amount_usd, w2.amount_usd)
        funding_hedge_quality = abs(w1.funding_exposure + w2.funding_exposure) / max(abs(w1.funding_exposure), abs(w2.funding_exposure))
        hedge_efficiency = 1.0 - funding_hedge_quality  # Better hedge = lower residual
        
        # Enhanced rate for funding swaps
        base_fry = total_wreckage * self.swap_fry_rate
        
        # Funding efficiency bonus (better hedges get more FRY)
        efficiency_fry = base_fry * (self.funding_efficiency_bonus - 1.0) * hedge_efficiency
        
        total_fry = base_fry + efficiency_fry
        self.total_fry_minted += total_fry
        self.total_swap_notional += swap_notional
        
        # Record swap details
        self.funding_swaps.append({
            'dex1': w1.dex,
            'dex2': w2.dex,
            'asset': w1.asset,
            'notional': swap_notional,
            'funding1': w1.funding_exposure,
            'funding2': w2.funding_exposure,
            'hedge_efficiency': hedge_efficiency,
            'fry_minted': total_fry
        })
        
        return total_fry
    
    def _mint_unmatched(self, w: WreckageEvent):
        """Mint FRY for unmatched wreckage at base rate"""
        fry = w.amount_usd * self.base_fry_rate
        self.total_fry_minted += fry
        return fry
    
    def simulate_wreckage_stream(self, duration_seconds: int = 60, events_per_second: float = 2.0):
        """Simulate real-time wreckage collection and matching"""
        print(f"\n{FRY_YELLOW}📊 Simulating wreckage stream for {duration_seconds}s...{RESET}")
        
        assets = ["BTC", "ETH", "SOL", "AVAX", "BNB"]
        start_time = time.time()
        event_count = 0
        
        while time.time() - start_time < duration_seconds:
            # Generate random wreckage events
            if random.random() < events_per_second / 10:  # Probabilistic event generation
                dex = random.choice(DEXES)
                wreckage_type = random.choice(list(WRECKAGE_TYPES.keys()))
                asset = random.choice(assets)
                amount = random.uniform(100, 5000)
                
                event = WreckageEvent(dex, wreckage_type, asset, amount, time.time())
                self.collect_wreckage(event)
                event_count += 1
                
                # Periodic matching
                if event_count % 5 == 0:
                    matches = self.match_wreckage()
                    if matches > 0:
                        print(f"{FRY_RED}✓{RESET} Matched {matches} wreckage pair(s)")
            
            time.sleep(0.1)
        
        # Final matching pass
        final_matches = self.match_wreckage()
        print(f"\n{FRY_YELLOW}Final matching: {final_matches} additional pairs{RESET}")
    
    def display_summary(self):
        """Display matching engine summary"""
        print(f"\n{BOLD}{'='*70}{RESET}")
        print(f"{FRY_RED}{BOLD}FRY Wreckage Matching Summary{RESET}")
        print(f"{BOLD}{'='*70}{RESET}")
        
        total_events = len(self.wreckage_pool)
        matched_events = sum(1 for w in self.wreckage_pool if w.matched)
        match_rate = (matched_events / total_events * 100) if total_events > 0 else 0
        
        print(f"\n{BOLD}Wreckage Collection:{RESET}")
        print(f"  Total Events: {total_events}")
        print(f"  Total Wreckage: ${self.total_wreckage_collected:,.2f}")
        print(f"  Matched Events: {matched_events} ({match_rate:.1f}%)")
        print(f"  Matched Pairs: {len(self.matched_pairs)}")
        
        print(f"\n{BOLD}FRY Minting:{RESET}")
        print(f"  Total FRY Minted: {FRY_YELLOW}{self.total_fry_minted:,.2f} FRY{RESET}")
        
        if self.total_wreckage_collected > 0:
            effective_rate = self.total_fry_minted / self.total_wreckage_collected
            print(f"  Effective Rate: {effective_rate:.2f} FRY per $1 wreckage")
            improvement = ((effective_rate - self.base_fry_rate) / self.base_fry_rate) * 100
            print(f"  Rate Improvement: {FRY_RED}+{improvement:.1f}%{RESET} vs base rate")
        
        print(f"\n{BOLD}Funding Rate Swaps:{RESET}")
        print(f"  Total Swap Notional: ${self.total_swap_notional:,.2f}")
        print(f"  Number of Swaps: {len(self.funding_swaps)}")
        
        if self.funding_swaps:
            avg_efficiency = sum(s['hedge_efficiency'] for s in self.funding_swaps) / len(self.funding_swaps)
            print(f"  Average Hedge Efficiency: {avg_efficiency:.1%}")
            print(f"  {FRY_YELLOW}Note: Swaps are cash-settled, no token transfers{RESET}")
        
        # Cross-DEX breakdown
        print(f"\n{BOLD}Cross-DEX Matching:{RESET}")
        dex_pairs = {}
        for w1, w2 in self.matched_pairs:
            pair_key = tuple(sorted([w1.dex, w2.dex]))
            dex_pairs[pair_key] = dex_pairs.get(pair_key, 0) + 1
        
        for (dex1, dex2), count in sorted(dex_pairs.items(), key=lambda x: -x[1]):
            print(f"  {dex1} <--> {dex2}: {count} matches")
        
        # Asset breakdown
        print(f"\n{BOLD}Top Assets by Wreckage:{RESET}")
        asset_wreckage = {}
        for w in self.wreckage_pool:
            asset_wreckage[w.asset] = asset_wreckage.get(w.asset, 0) + w.amount_usd
        
        for asset, amount in sorted(asset_wreckage.items(), key=lambda x: -x[1])[:5]:
            print(f"  {asset}: ${amount:,.2f}")
        
        print(f"\n{BOLD}{'='*70}{RESET}")
    
    def export_matches(self, filename: str = None):
        """Export matched pairs to JSON"""
        if filename is None:
            filename = f"fry_wreckage_matches_{int(time.time())}.json"
        
        import json
        data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total_events": len(self.wreckage_pool),
                "matched_pairs": len(self.matched_pairs),
                "total_fry_minted": self.total_fry_minted,
                "total_wreckage": self.total_wreckage_collected
            },
            "matched_pairs": [
                {
                    "pair_id": i,
                    "event1": {
                        "dex": w1.dex,
                        "type": w1.wreckage_type,
                        "asset": w1.asset,
                        "amount_usd": w1.amount_usd
                    },
                    "event2": {
                        "dex": w2.dex,
                        "type": w2.wreckage_type,
                        "asset": w2.asset,
                        "amount_usd": w2.amount_usd
                    }
                }
                for i, (w1, w2) in enumerate(self.matched_pairs)
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"{FRY_YELLOW}📄 Exported to {filename}{RESET}")


def main():
    """Demo the FRY wreckage matching engine"""
    print(f"\n{FRY_RED}{BOLD}FRY Wreckage-to-Wreckage Matching Engine{RESET}")
    print(f"{DIM}Cross-DEX loss netting for enhanced capital efficiency{RESET}\n")
    
    engine = FRYWreckageMatchingEngine()
    
    # Simulate wreckage stream
    engine.simulate_wreckage_stream(duration_seconds=30, events_per_second=3.0)
    
    # Display results
    engine.display_summary()
    
    # Export
    engine.export_matches()
    
    print(f"\n{FRY_YELLOW}💡 Key Insight:{RESET}")
    print("  Funding rate swaps create a peer-to-peer loss-netting layer WITHOUT token transfers.")
    print("  Participants swap funding exposure (cash-settled) to hedge complementary losses")
    print("  across venues, minting FRY at enhanced rates based on hedge efficiency.")
    print("  This creates synthetic cross-DEX exposure without moving assets.")


if __name__ == "__main__":
    main()
