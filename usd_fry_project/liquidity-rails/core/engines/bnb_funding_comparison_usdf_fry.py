#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BNB Funding Rate Comparison
USDF loss-recycle (mints on short liquidations on up-moves) vs FRY stable-peg (mints on long liquidations on down-moves)

Simulates a BNB market with a stylized baseline funding rate driven by momentum and
open-interest imbalance proxies. Then applies two stabilization mechanisms:
- USDF: When price accelerates upward and shorts get squeezed (short liqs), programmatically
         dampens positive funding spikes toward 0% by recycling losses (short-side wreckage).
- FRY:  When price accelerates downward and longs get wiped (long liqs), dampens negative
         funding spikes toward 0% via wreckage absorption and FRY mint.

Outputs:
- PNG plot with baseline vs USDF-stabilized vs FRY-stabilized funding series
- Console metrics: mean funding, mean |funding|, volatility (std), tail mass (|funding| > thresholds),
  and reduction percentages compared to baseline.

Run:
    python3 core/bnb_funding_comparison_usdf_fry.py
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Non-interactive backend
plt.switch_backend('Agg')

# FRY scheme on white
WHITE = '#FFFFFF'
BLACK = '#000000'
RED = '#FF4444'      # FRY
YELLOW = '#FFD700'   # Accents / USDF fill
GRAY = '#7f7f7f'
LIGHT_GRAY = '#d9d9d9'
BLUE = '#2e75b6'     # Baseline
GREEN = '#70ad47'    # USDF curve

rng = np.random.default_rng(1337)


def simulate_bnb_series(T=365):
    """Simulate BNB price and baseline funding rates for T days."""
    # Price path (lognormal-like with regime noise)
    prices = [300.0]
    drift = 0.0005
    vol = 0.04
    for t in range(1, T):
        shock = rng.normal(drift, vol)
        prices.append(max(5.0, prices[-1] * (1.0 + shock)))
    prices = np.array(prices)

    # Momentum proxy
    mom = np.concatenate([[0.0], np.diff(prices) / np.maximum(1e-9, prices[:-1])])
    # Volatility proxy (rolling std of returns)
    window = 7
    rets = mom
    vol_roll = np.array([
        np.std(rets[max(0, i-window+1):i+1]) if i > 0 else 0.0
        for i in range(len(rets))
    ])
    # OI imbalance proxy (random but persistent)
    oi_imb = np.zeros(T)
    for i in range(1, T):
        oi_imb[i] = 0.9 * oi_imb[i-1] + rng.normal(0, 0.05)

    # Baseline funding centered near 0, influenced by momentum, vol, OI imbalance
    baseline = 0.20 * mom + 0.5 * oi_imb + 0.05 * (vol_roll - np.mean(vol_roll))
    # Add noise and clip to realistic band +/- 30% annualized
    baseline += rng.normal(0, 0.01, size=T)
    baseline = np.clip(baseline, -0.30, 0.30)

    return prices, mom, baseline


def apply_usdf_stabilizer(baseline, mom, strength=0.6):
    """USDF loss-recycle dampens positive funding during strong up-moves (short liqs)."""
    stabilized = baseline.copy()
    pos_mask = (baseline > 0) & (mom > np.percentile(mom, 60))
    # Pull positive spikes toward 0 by factor `strength` where conditions hold
    stabilized[pos_mask] = baseline[pos_mask] * (1.0 - strength)
    return stabilized


def apply_fry_stabilizer(baseline, mom, strength=0.6):
    """FRY stable-peg dampens negative funding during strong down-moves (long liqs)."""
    stabilized = baseline.copy()
    neg_mask = (baseline < 0) & (mom < np.percentile(mom, 40))
    stabilized[neg_mask] = baseline[neg_mask] * (1.0 - strength)
    return stabilized


def metrics(series):
    m = {}
    m['mean'] = float(np.mean(series))
    m['mean_abs'] = float(np.mean(np.abs(series)))
    m['std'] = float(np.std(series))
    # Tail mass beyond 10% and 20%
    m['tail_10'] = float(np.mean(np.abs(series) > 0.10))
    m['tail_20'] = float(np.mean(np.abs(series) > 0.20))
    return m


def reduction(base_m, comp_m):
    def red(a, b):
        return (a - b) / a if a != 0 else 0.0
    return {
        'mean_abs_reduction': red(base_m['mean_abs'], comp_m['mean_abs']),
        'std_reduction': red(base_m['std'], comp_m['std']),
        'tail10_reduction': red(base_m['tail_10'], comp_m['tail_10']),
        'tail20_reduction': red(base_m['tail_20'], comp_m['tail_20']),
    }


def plot(prices, baseline, usdf, fry):
    T = len(baseline)
    x = np.arange(T)
    fig = plt.figure(figsize=(16, 10), facecolor=WHITE)
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3, height_ratios=[1, 1])

    # Top Left: Price
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x, prices, color=BLACK, linewidth=2.0)
    ax1.set_title('BNB Price (Simulated)', fontsize=14, fontweight='bold', color=BLACK)
    ax1.set_ylabel('Price (USD)', color=BLACK)
    ax1.grid(True, alpha=0.3, color=LIGHT_GRAY)
    for s in ax1.spines.values():
        s.set_color(GRAY); s.set_linewidth(0.8)

    # Top Right: USDF Mechanism Explanation
    ax_explain = fig.add_subplot(gs[0, 1])
    ax_explain.set_xlim(0, 1)
    ax_explain.set_ylim(0, 1)
    ax_explain.axis('off')
    
    # Title
    ax_explain.text(0.5, 0.95, 'USDF Loss Recycle Mechanism', ha='center', va='top', 
                    fontsize=13, fontweight='bold', color=GREEN)
    
    # Explanation text
    explanation = [
        "Theoretical Design:",
        "",
        "1. Collateral Segregation",
        "   • Short liquidation proceeds held in separate reserve",
        "   • Does not enter circulating USDF supply",
        "",
        "2. Mint-Burn Symmetry",
        "   • USDF minted against 100% collateral backing",
        "   • Loss recycle uses reserve to buy/burn USDF",
        "   • Net supply remains constant",
        "",
        "3. Peg Maintenance",
        "   • 1:1 redemption always available",
        "   • Reserve acts as stabilization buffer",
        "   • Arbitrage keeps market price at $1.00",
        "",
        "4. Funding Dampening",
        "   • Reserve deployed during positive funding spikes",
        "   • Absorbs short-side wreckage without inflation",
        "   • Stabilizes without compromising peg"
    ]
    
    y_pos = 0.85
    for line in explanation:
        if line.startswith(('1.', '2.', '3.', '4.')):
            ax_explain.text(0.05, y_pos, line, ha='left', va='top', fontsize=10, 
                          fontweight='bold', color=BLACK)
        elif line.startswith('   •'):
            ax_explain.text(0.08, y_pos, line, ha='left', va='top', fontsize=9, color=GRAY)
        elif line == "Theoretical Design:":
            ax_explain.text(0.05, y_pos, line, ha='left', va='top', fontsize=10, 
                          fontweight='bold', color=GREEN)
        else:
            ax_explain.text(0.05, y_pos, line, ha='left', va='top', fontsize=9, color=BLACK)
        y_pos -= 0.04

    # Bottom: Funding (spanning both columns)
    ax2 = fig.add_subplot(gs[1, :])
    ax2.axhspan(-0.02, 0.02, color=LIGHT_GRAY, alpha=0.4, label='Stable Zone (±2%)')
    ax2.plot(x, baseline, color=BLUE, linewidth=2.0, alpha=0.9, label='Baseline Funding')
    ax2.plot(x, usdf, color=GREEN, linewidth=2.4, alpha=0.95, label='USDF Loss-Recycle (short liqs)')
    ax2.plot(x, fry, color=RED, linewidth=2.4, alpha=0.95, label='FRY Stable-Peg (long liqs)')
    ax2.set_title('BNB Funding Rate: Baseline vs USDF vs FRY', fontsize=14, fontweight='bold', color=BLACK)
    ax2.set_xlabel('Time (days)', fontsize=11)
    ax2.set_ylabel('Funding (annualized)', color=BLACK, fontsize=11)
    ax2.grid(True, alpha=0.3, color=LIGHT_GRAY)
    for s in ax2.spines.values():
        s.set_color(GRAY); s.set_linewidth(0.8)
    leg = ax2.legend(loc='upper right', facecolor=WHITE, edgecolor=GRAY, fontsize=10)
    leg.get_frame().set_edgecolor(GRAY)

    fig.suptitle('USDF (short-liq dampening) vs FRY (long-liq dampening) Stabilization on BNB',
                 fontsize=16, fontweight='bold', color=BLACK)

    plt.tight_layout(); plt.subplots_adjust(top=0.93)
    fname = f"bnb_funding_usdf_fry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(fname, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    return fname


def main():
    print('🚀 BNB Funding Comparison: USDF (short liqs) vs FRY (long liqs)')
    prices, mom, baseline = simulate_bnb_series(T=365)
    usdf = apply_usdf_stabilizer(baseline, mom, strength=0.6)
    fry = apply_fry_stabilizer(baseline, mom, strength=0.6)

    base_m = metrics(baseline)
    usdf_m = metrics(usdf)
    fry_m = metrics(fry)

    usdf_red = reduction(base_m, usdf_m)
    fry_red = reduction(base_m, fry_m)

    fname = plot(prices, baseline, usdf, fry)

    print('\n📊 Metrics (annualized funding):')
    def pfx(m):
        return f"mean={m['mean']:.3f}, mean|f|={m['mean_abs']:.3f}, std={m['std']:.3f}, tail10={m['tail_10']:.2%}, tail20={m['tail_20']:.2%}"
    print('   Baseline: ' + pfx(base_m))
    print('   USDF:     ' + pfx(usdf_m))
    print('   FRY:      ' + pfx(fry_m))

    print('\n🔻 Reductions vs Baseline:')
    def pfxr(r):
        return f"|f|:{r['mean_abs_reduction']:.1%}  std:{r['std_reduction']:.1%}  tail10:{r['tail10_reduction']:.1%}  tail20:{r['tail20_reduction']:.1%}"
    print('   USDF: ' + pfxr(usdf_red))
    print('   FRY:  ' + pfxr(fry_red))

    print(f"\n🖼️ Saved: {fname}")


if __name__ == '__main__':
    main()
