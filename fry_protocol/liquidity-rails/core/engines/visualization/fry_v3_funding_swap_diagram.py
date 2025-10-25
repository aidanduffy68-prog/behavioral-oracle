#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRY v3 Funding Rate Swap Architecture Diagram
==============================================

Visual diagram showing the FRY v3 funding rate swap matching engine:
- Cross-DEX wreckage collection
- Funding exposure calculation
- Peer-to-peer swap matching
- Cash settlement (no token transfers)
- Enhanced FRY minting based on hedge efficiency

Output: PNG diagram with FRY color scheme
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

plt.switch_backend('Agg')

# FRY color scheme
WHITE = '#FFFFFF'
BLACK = '#000000'
RED = '#FF4444'
YELLOW = '#FFD700'
GRAY = '#7f7f7f'
LIGHT_GRAY = '#d9d9d9'
DARK_RED = '#CC0000'

def create_fry_v3_diagram():
    fig, ax = plt.subplots(figsize=(14, 10), facecolor=WHITE)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.7, 'FRY v3: Funding Rate Swap Protocol', 
            ha='center', va='top', fontsize=22, fontweight='bold', color=BLACK)
    ax.text(5, 9.3, 'Cross-DEX loss netting through cash-settled funding swaps',
            ha='center', va='top', fontsize=11, color=GRAY)
    
    # ===== SECTION 1: How It Works =====
    y_start = 8.8
    
    # Step 1: Wreckage Collection
    step1_box = FancyBboxPatch((0.5, y_start-0.8), 4.0, 0.7,
                              boxstyle="round,pad=0.1",
                              facecolor=RED, edgecolor=BLACK, linewidth=2, alpha=0.15)
    ax.add_patch(step1_box)
    ax.text(0.7, y_start-0.3, '1', ha='center', va='center',
           fontsize=16, fontweight='bold', color=WHITE,
           bbox=dict(boxstyle='circle,pad=0.3', facecolor=RED, edgecolor=BLACK, linewidth=2))
    ax.text(2.5, y_start-0.25, 'Wreckage Collection', ha='center', va='center',
           fontsize=12, fontweight='bold', color=BLACK)
    ax.text(2.5, y_start-0.55, 'DEXes report losses with funding exposure\n(long liqs = negative, short liqs = positive)',
           ha='center', va='center', fontsize=9, color=GRAY)
    
    # Step 2: Matching
    step2_box = FancyBboxPatch((5.5, y_start-0.8), 4.0, 0.7,
                              boxstyle="round,pad=0.1",
                              facecolor=YELLOW, edgecolor=BLACK, linewidth=2, alpha=0.15)
    ax.add_patch(step2_box)
    ax.text(5.7, y_start-0.3, '2', ha='center', va='center',
           fontsize=16, fontweight='bold', color=BLACK,
           bbox=dict(boxstyle='circle,pad=0.3', facecolor=YELLOW, edgecolor=BLACK, linewidth=2))
    ax.text(7.5, y_start-0.25, 'Swap Matching', ha='center', va='center',
           fontsize=12, fontweight='bold', color=BLACK)
    ax.text(7.5, y_start-0.55, 'Algorithm pairs opposite funding exposures\nacross different DEXes',
           ha='center', va='center', fontsize=9, color=GRAY)
    
    # Arrow between steps
    arrow = FancyArrowPatch((4.6, y_start-0.45), (5.4, y_start-0.45),
                           arrowstyle='->', mutation_scale=20, linewidth=3, color=BLACK)
    ax.add_patch(arrow)
    
    # ===== SECTION 2: Example Swap Flow =====
    y_example = 7.3
    
    ax.text(5.0, y_example, 'Example: Cross-DEX Funding Swap', ha='center', va='center',
           fontsize=13, fontweight='bold', color=BLACK)
    
    # DEX A (dYdX) - Long Liquidation
    dex_a_box = FancyBboxPatch((0.8, y_example-1.2), 1.8, 0.9,
                              boxstyle="round,pad=0.08",
                              facecolor=RED, edgecolor=BLACK, linewidth=2, alpha=0.2)
    ax.add_patch(dex_a_box)
    ax.text(1.7, y_example-0.55, 'dYdX', ha='center', va='center',
           fontsize=11, fontweight='bold', color=BLACK)
    ax.text(1.7, y_example-0.8, 'Long Liq\n$5,000', ha='center', va='center',
           fontsize=9, color=BLACK)
    ax.text(1.7, y_example-1.05, '-15% funding', ha='center', va='center',
           fontsize=9, fontweight='bold', color=RED)
    
    # Swap arrow
    swap_arrow = FancyArrowPatch((2.7, y_example-0.75), (7.3, y_example-0.75),
                                arrowstyle='<->', mutation_scale=25, linewidth=4, 
                                color=YELLOW, linestyle='-')
    ax.add_patch(swap_arrow)
    ax.text(5.0, y_example-0.45, 'FUNDING SWAP', ha='center', va='center',
           fontsize=11, fontweight='bold', color=BLACK,
           bbox=dict(boxstyle='round,pad=0.3', facecolor=YELLOW, alpha=0.7, edgecolor=BLACK, linewidth=2))
    ax.text(5.0, y_example-1.15, 'Cash-settled\nNo tokens moved', ha='center', va='center',
           fontsize=8, color=GRAY, style='italic')
    
    # DEX B (Hyperliquid) - Short Liquidation
    dex_b_box = FancyBboxPatch((7.4, y_example-1.2), 1.8, 0.9,
                              boxstyle="round,pad=0.08",
                              facecolor=YELLOW, edgecolor=BLACK, linewidth=2, alpha=0.2)
    ax.add_patch(dex_b_box)
    ax.text(8.3, y_example-0.55, 'Hyperliquid', ha='center', va='center',
           fontsize=11, fontweight='bold', color=BLACK)
    ax.text(8.3, y_example-0.8, 'Short Liq\n$5,000', ha='center', va='center',
           fontsize=9, color=BLACK)
    ax.text(8.3, y_example-1.05, '+18% funding', ha='center', va='center',
           fontsize=9, fontweight='bold', color=DARK_RED)
    
    # ===== SECTION 3: Swap Outcome =====
    y_outcome = 5.5
    
    ax.text(5.0, y_outcome+0.3, 'Swap Outcome', ha='center', va='center',
           fontsize=13, fontweight='bold', color=BLACK)
    
    # Outcome box
    outcome_box = FancyBboxPatch((1.5, y_outcome-1.0), 7.0, 0.9,
                                boxstyle="round,pad=0.1",
                                facecolor=LIGHT_GRAY, edgecolor=BLACK, linewidth=2)
    ax.add_patch(outcome_box)
    
    # Left side - swap details
    ax.text(2.0, y_outcome-0.3, '• Notional: $5,000', ha='left', va='center',
           fontsize=10, color=BLACK)
    ax.text(2.0, y_outcome-0.55, '• Net Funding: $12.50/day', ha='left', va='center',
           fontsize=10, color=BLACK)
    ax.text(2.0, y_outcome-0.8, '• Hedge Efficiency: 85%', ha='left', va='center',
           fontsize=10, color=BLACK)
    
    # Right side - FRY minting
    ax.text(8.0, y_outcome-0.3, 'FRY Minted:', ha='right', va='center',
           fontsize=10, fontweight='bold', color=BLACK)
    ax.text(8.0, y_outcome-0.55, '7,000 FRY', ha='right', va='center',
           fontsize=11, fontweight='bold', color=RED)
    ax.text(8.0, y_outcome-0.8, '(1.4x base + efficiency bonus)', ha='right', va='center',
           fontsize=8, color=GRAY)
    
    # ===== SECTION 4: Key Benefits =====
    y_benefits = 3.8
    
    ax.text(5.0, y_benefits+0.3, 'Why v3 Matters', ha='center', va='center',
           fontsize=13, fontweight='bold', color=BLACK)
    
    benefits = [
        {'icon': '🔒', 'title': 'No Custody Risk', 'desc': 'Cash-settled swaps\nNo token transfers'},
        {'icon': '⚡', 'title': 'Capital Efficient', 'desc': '+65% FRY minting\nvs base rate'},
        {'icon': '🌐', 'title': 'Cross-DEX', 'desc': 'Synthetic exposure\nacross venues'},
        {'icon': '📊', 'title': 'Hedge Quality', 'desc': 'Rewards efficient\nmatching (43% avg)'}
    ]
    
    for i, benefit in enumerate(benefits):
        x_pos = 1.2 + i * 2.2
        benefit_box = FancyBboxPatch((x_pos-0.5, y_benefits-0.9), 1.8, 0.8,
                                    boxstyle="round,pad=0.08",
                                    facecolor=YELLOW if i % 2 == 0 else RED,
                                    edgecolor=BLACK, linewidth=1.5, alpha=0.15)
        ax.add_patch(benefit_box)
        ax.text(x_pos+0.4, y_benefits-0.25, benefit['icon'], ha='center', va='center',
               fontsize=20)
        ax.text(x_pos+0.4, y_benefits-0.5, benefit['title'], ha='center', va='center',
               fontsize=9, fontweight='bold', color=BLACK)
        ax.text(x_pos+0.4, y_benefits-0.75, benefit['desc'], ha='center', va='center',
               fontsize=7, color=GRAY)
    
    # ===== SECTION 5: Performance Metrics =====
    y_metrics = 2.2
    
    ax.text(5.0, y_metrics+0.3, 'Performance Metrics', ha='center', va='center',
           fontsize=13, fontweight='bold', color=BLACK)
    
    metrics_box = FancyBboxPatch((1.0, y_metrics-0.9), 8.0, 0.8,
                                boxstyle="round,pad=0.1",
                                facecolor=RED, edgecolor=BLACK, linewidth=2, alpha=0.1)
    ax.add_patch(metrics_box)
    
    # Metrics in columns
    metrics_data = [
        ('Total Swaps', '12 pairs'),
        ('Swap Notional', '$22.7K'),
        ('Avg Efficiency', '43.6%'),
        ('FRY Minted', '229K FRY'),
        ('Rate Improvement', '+65.1%')
    ]
    
    for i, (label, value) in enumerate(metrics_data):
        x_pos = 1.5 + i * 1.7
        ax.text(x_pos, y_metrics-0.25, label, ha='center', va='center',
               fontsize=8, color=GRAY)
        ax.text(x_pos, y_metrics-0.55, value, ha='center', va='center',
               fontsize=10, fontweight='bold', color=BLACK)
    
    # ===== FOOTER =====
    ax.text(5.0, 0.8, 'FRY v3 = Pure derivatives layer for cross-DEX loss netting without token movement',
           ha='center', va='center', fontsize=10, style='italic', color=GRAY)
    ax.text(5.0, 0.4, 'Participants hedge funding exposure, earn enhanced FRY based on hedge quality',
           ha='center', va='center', fontsize=9, color=GRAY)
    
    plt.tight_layout()
    
    from datetime import datetime
    filename = f"fry_v3_funding_swap_diagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    
    return filename

def main():
    print("🎨 Generating FRY v3 Funding Rate Swap Diagram...")
    filename = create_fry_v3_diagram()
    print(f"✅ Diagram saved: {filename}")
    print("\n📊 FRY v3 Architecture:")
    print("   Layer 1: DEX wreckage collection with funding exposure")
    print("   Layer 2: Peer-to-peer swap matching algorithm")
    print("   Layer 3: Cash-settled swap execution (no tokens)")
    print("   Layer 4: Enhanced FRY minting based on hedge efficiency")

if __name__ == '__main__':
    main()
