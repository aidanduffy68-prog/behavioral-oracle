#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
$ASTER-$FRY vs $ASTER-$USDF Capital Efficiency Comparison

This script simulates capital efficiency of native token denominated pool (ASTER-FRY)
vs a traditional stable-denominated pool (ASTER-USDF). It mirrors the methodology
used in prior HYPE comparisons, adapted for ASTER.

Output:
- PNG chart with both efficiency curves and the filled efficiency gap
- Console metrics with average and max efficiency advantage
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Non-interactive backend for PNG output
plt.switch_backend('Agg')

# FRY color scheme
WHITE = '#FFFFFF'
BLACK = '#000000'
RED = '#FF4444'
YELLOW = '#FFD700'
GRAY = '#7f7f7f'
LIGHT_GRAY = '#d9d9d9'


def simulate(price_points=60):
    """Simulate ASTER price range and pool metrics."""
    # Price range for ASTER, flexible
    aster_prices = np.logspace(np.log10(0.25), np.log10(20.0), price_points)

    usdf_eff = []
    fry_eff = []

    base_reserves_aster = 80_000.0
    fry_minting_rate = 15.0  # FRY per ASTER lost (nominal)

    for px in aster_prices:
        # Activity rises with price (bounded)
        vol_factor = min(px / 1.5, 5.0)
        daily_losses_usd = 10_000 * vol_factor
        daily_losses_aster = daily_losses_usd / px

        # TVL in ASTER terms (reserves + locked backing)
        backing_ratio = 0.6
        aster_locked = daily_losses_aster * backing_ratio
        pool_tvl_aster = base_reserves_aster + aster_locked

        # USDF-ASTER (traditional): minimal native benefits
        usdf_multiplier = 1.0
        if px >= 2.0:
            usdf_multiplier *= 1.15
        if px >= 5.0:
            usdf_multiplier *= 1.10  # still modest
        usdf_fry_output = daily_losses_aster * fry_minting_rate * usdf_multiplier
        usdf_efficiency = usdf_fry_output / pool_tvl_aster
        usdf_eff.append(usdf_efficiency)

        # ASTER-FRY (native): full native stack multipliers
        base_mult = 1.0
        if px >= 1.0:
            base_mult *= 1.3
        if px >= 2.0:
            base_mult *= 1.6
        if px >= 5.0:
            base_mult *= 1.5
        liquidity_bonus = 2.0
        governance_bonus = 1.5
        arbitrage_bonus = min(px * 0.5, 3.0)
        total_mult = min(base_mult * liquidity_bonus * governance_bonus * arbitrage_bonus, 25.0)
        fry_output = daily_losses_aster * fry_minting_rate * total_mult
        fry_efficiency = fry_output / pool_tvl_aster
        fry_eff.append(fry_efficiency)

    return aster_prices, np.array(usdf_eff), np.array(fry_eff)


def plot(aster_prices, usdf_eff, fry_eff):
    fig = plt.figure(figsize=(12, 8), facecolor=WHITE)
    ax = fig.add_subplot(111)
    ax.patch.set_facecolor(WHITE)

    # Curves
    ax.plot(aster_prices, usdf_eff, color=GRAY, linewidth=2.5, linestyle='--', alpha=0.9, label='ASTER-USDF (Traditional)')
    ax.plot(aster_prices, fry_eff, color=RED, linewidth=3, alpha=0.95, label='ASTER-FRY (Native)')

    # Fill gap
    ax.fill_between(aster_prices, usdf_eff, fry_eff, where=(fry_eff >= usdf_eff), color=YELLOW, alpha=0.25, label='Efficiency Advantage')

    # Axes styling
    ax.set_title('Capital Efficiency: ASTER-FRY vs ASTER-USDF', fontsize=16, fontweight='bold', color=BLACK)
    ax.set_xlabel('ASTER Price (USD)', color=BLACK, fontsize=12)
    ax.set_ylabel('Capital Efficiency Ratio (FRY output / TVL)', color=BLACK, fontsize=12)
    ax.set_xscale('log')
    ax.grid(True, alpha=0.35, color=LIGHT_GRAY, linewidth=0.7)
    for spine in ax.spines.values():
        spine.set_color(GRAY)
        spine.set_linewidth(0.8)

    # Legend
    leg = ax.legend(loc='upper left', facecolor=WHITE, edgecolor=GRAY, fontsize=11)
    leg.get_frame().set_edgecolor(GRAY)

    # Summary in suptitle
    ratios = fry_eff / np.maximum(usdf_eff, 1e-9)
    avg_adv = float(np.mean(ratios))
    max_adv = float(np.max(ratios))

    fig.suptitle(f"Average Advantage: {avg_adv:.1f}x | Max Advantage: {max_adv:.1f}x", y=0.94, fontsize=12, color=BLACK)

    plt.tight_layout()
    plt.subplots_adjust(top=0.88)

    fname = f"aster_fry_vs_usdf_efficiency_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(fname, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()

    return fname, avg_adv, max_adv


def main():
    print("🚀 ASTER-FRY vs ASTER-USDF Capital Efficiency Simulation")
    prices, usdf, fry = simulate(price_points=75)
    print("📈 Generating chart...")
    fname, avg_adv, max_adv = plot(prices, usdf, fry)

    print("\n📊 Results:")
    print(f"   File: {fname}")
    print(f"   Average Efficiency Advantage: {avg_adv:.1f}x")
    print(f"   Maximum Efficiency Gap: {max_adv:.1f}x")

    # Quick context
    print("\n🔍 Interpretation:")
    if avg_adv > 2.0:
        print("   • Native ASTER-FRY pool shows superior capital efficiency vs ASTER-USDF")
    if max_adv > 5.0:
        print("   • Large advantage spikes under favorable price regimes")
    print("   • Native token denomination compounds utility via multipliers (liquidity, governance, arbitrage)")


if __name__ == '__main__':
    main()
