#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRY v3 Mechanics Slide
======================

Clean, presentation-ready slide explaining FRY v3 mechanics.
Perfect for GitDocs, pitch decks, or technical presentations.

Output: High-quality PNG slide
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from datetime import datetime

plt.switch_backend('Agg')

# FRY colors
WHITE = '#FFFFFF'
BLACK = '#000000'
RED = '#FF4444'
YELLOW = '#FFD700'
GRAY = '#7f7f7f'
LIGHT_GRAY = '#d9d9d9'
DARK_RED = '#CC0000'


def create_mechanics_slide():
    """Generate FRY v3 mechanics slide"""
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=WHITE)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # ===== HEADER =====
    ax.text(8, 8.6, 'FRY v3: Funding Rate Swap Mechanics', 
            ha='center', va='top', fontsize=32, fontweight='bold', color=BLACK)
    ax.text(8, 8.15, 'Cross-DEX loss netting through cash-settled funding swaps',
            ha='center', va='top', fontsize=15, color=GRAY, style='italic')
    
    # Divider line
    ax.plot([0.5, 15.5], [7.85, 7.85], color=LIGHT_GRAY, linewidth=3)
    
    # ===== TOP SECTION: ELEVATED 3-PART FLOW =====
    y_top = 7.0
    
    # Problem box (larger, more prominent)
    problem_box = FancyBboxPatch((0.5, y_top-1.1), 4.8, 1.0,
                                boxstyle="round,pad=0.12",
                                facecolor=RED, edgecolor=BLACK, linewidth=3, alpha=0.2)
    ax.add_patch(problem_box)
    
    ax.text(2.9, y_top-0.25, 'The Problem', ha='center', va='center',
           fontsize=18, fontweight='bold', color=DARK_RED)
    ax.text(2.9, y_top-0.6, 'DEXes have opposite\nfunding exposures', ha='center', va='center',
           fontsize=13, color=BLACK, fontweight='bold')
    ax.text(2.9, y_top-0.95, 'Inefficient capital allocation', ha='center', va='center',
           fontsize=11, color=GRAY, style='italic')
    
    # Arrow 1
    arrow_top1 = FancyArrowPatch((5.4, y_top-0.6), (5.9, y_top-0.6),
                                arrowstyle='->', mutation_scale=35, linewidth=4, color=BLACK)
    ax.add_patch(arrow_top1)
    
    # Solution box
    solution_box = FancyBboxPatch((6.0, y_top-1.1), 4.8, 1.0,
                                 boxstyle="round,pad=0.12",
                                 facecolor=YELLOW, edgecolor=BLACK, linewidth=3, alpha=0.25)
    ax.add_patch(solution_box)
    
    ax.text(8.4, y_top-0.25, 'The Solution', ha='center', va='center',
           fontsize=18, fontweight='bold', color=DARK_RED)
    ax.text(8.4, y_top-0.6, 'Match opposite exposures\nvia funding swaps', ha='center', va='center',
           fontsize=13, color=BLACK, fontweight='bold')
    ax.text(8.4, y_top-0.95, 'No token transfers, pure derivatives', ha='center', va='center',
           fontsize=11, color=GRAY, style='italic')
    
    # Arrow 2
    arrow_top2 = FancyArrowPatch((10.9, y_top-0.6), (11.4, y_top-0.6),
                                arrowstyle='->', mutation_scale=35, linewidth=4, color=BLACK)
    ax.add_patch(arrow_top2)
    
    # Result box
    result_box = FancyBboxPatch((11.5, y_top-1.1), 4.8, 1.0,
                               boxstyle="round,pad=0.12",
                               facecolor=YELLOW, edgecolor=BLACK, linewidth=3, alpha=0.4)
    ax.add_patch(result_box)
    
    ax.text(13.9, y_top-0.25, 'The Result', ha='center', va='center',
           fontsize=18, fontweight='bold', color=DARK_RED)
    ax.text(13.9, y_top-0.6, 'Enhanced FRY minting\n+ stabilized funding', ha='center', va='center',
           fontsize=13, color=BLACK, fontweight='bold')
    ax.text(13.9, y_top-0.95, 'Provable convergence dynamics', ha='center', va='center',
           fontsize=11, color=GRAY, style='italic')
    
    # ===== MAIN FLOW DIAGRAM (OPTIMIZED) =====
    y_flow = 4.2
    
    # Section title
    ax.text(8, y_flow+1.2, 'How It Works', ha='center', va='center',
           fontsize=22, fontweight='bold', color=BLACK)
    
    # Step boxes - wider and better spaced
    step_width = 3.5
    step_height = 1.6
    
    # Step 1: Wreckage Collection
    step1_box = FancyBboxPatch((0.3, y_flow-0.8), step_width, step_height,
                              boxstyle="round,pad=0.15",
                              facecolor=RED, edgecolor=BLACK, linewidth=3, alpha=0.2)
    ax.add_patch(step1_box)
    
    ax.text(0.65, y_flow+0.5, '1', ha='center', va='center',
           fontsize=26, fontweight='bold', color=WHITE,
           bbox=dict(boxstyle='circle,pad=0.5', facecolor=RED, edgecolor=BLACK, linewidth=3))
    
    ax.text(2.05, y_flow+0.55, 'Wreckage Collection', ha='left', va='top',
           fontsize=16, fontweight='bold', color=BLACK)
    ax.text(2.05, y_flow+0.15, '• DEXes report losses', ha='left', va='top',
           fontsize=11, color=BLACK)
    ax.text(2.05, y_flow-0.15, '• Calculate funding exposure', ha='left', va='top',
           fontsize=11, color=BLACK)
    ax.text(2.05, y_flow-0.5, '• Long liqs = negative', ha='left', va='top',
           fontsize=10, color=GRAY, style='italic')
    
    # Arrow 1->2
    arrow1 = FancyArrowPatch((3.9, y_flow), (4.5, y_flow),
                            arrowstyle='->', mutation_scale=40, linewidth=4, color=BLACK)
    ax.add_patch(arrow1)
    
    # Step 2: Matching Algorithm
    step2_box = FancyBboxPatch((4.6, y_flow-0.8), step_width, step_height,
                              boxstyle="round,pad=0.15",
                              facecolor=YELLOW, edgecolor=BLACK, linewidth=3, alpha=0.25)
    ax.add_patch(step2_box)
    
    ax.text(4.95, y_flow+0.5, '2', ha='center', va='center',
           fontsize=26, fontweight='bold', color=BLACK,
           bbox=dict(boxstyle='circle,pad=0.5', facecolor=YELLOW, edgecolor=BLACK, linewidth=3))
    
    ax.text(6.35, y_flow+0.55, 'Swap Matching', ha='left', va='top',
           fontsize=16, fontweight='bold', color=BLACK)
    ax.text(6.35, y_flow+0.15, '• Pair opposite exposures', ha='left', va='top',
           fontsize=11, color=BLACK)
    ax.text(6.35, y_flow-0.15, '• Number theory optimization', ha='left', va='top',
           fontsize=11, color=BLACK)
    ax.text(6.35, y_flow-0.5, '• GCD for sizing', ha='left', va='top',
           fontsize=10, color=GRAY, style='italic')
    
    # Arrow 2->3
    arrow2 = FancyArrowPatch((8.2, y_flow), (8.8, y_flow),
                            arrowstyle='->', mutation_scale=40, linewidth=4, color=BLACK)
    ax.add_patch(arrow2)
    
    # Step 3: Swap Execution
    step3_box = FancyBboxPatch((8.9, y_flow-0.8), step_width, step_height,
                              boxstyle="round,pad=0.15",
                              facecolor=LIGHT_GRAY, edgecolor=BLACK, linewidth=3)
    ax.add_patch(step3_box)
    
    ax.text(9.25, y_flow+0.5, '3', ha='center', va='center',
           fontsize=26, fontweight='bold', color=WHITE,
           bbox=dict(boxstyle='circle,pad=0.5', facecolor=BLACK, edgecolor=BLACK, linewidth=3))
    
    ax.text(10.65, y_flow+0.55, 'Cash Settlement', ha='left', va='top',
           fontsize=16, fontweight='bold', color=BLACK)
    ax.text(10.65, y_flow+0.15, '• No token transfers', ha='left', va='top',
           fontsize=11, color=BLACK)
    ax.text(10.65, y_flow-0.15, '• Pure funding swap', ha='left', va='top',
           fontsize=11, color=BLACK)
    ax.text(10.65, y_flow-0.5, '• Daily settlement', ha='left', va='top',
           fontsize=10, color=GRAY, style='italic')
    
    # Arrow 3->4
    arrow3 = FancyArrowPatch((12.5, y_flow), (13.1, y_flow),
                            arrowstyle='->', mutation_scale=40, linewidth=4, color=BLACK)
    ax.add_patch(arrow3)
    
    # Step 4: FRY Minting
    step4_box = FancyBboxPatch((13.2, y_flow-0.8), step_width, step_height,
                              boxstyle="round,pad=0.15",
                              facecolor=RED, edgecolor=BLACK, linewidth=3, alpha=0.4)
    ax.add_patch(step4_box)
    
    ax.text(13.55, y_flow+0.5, '4', ha='center', va='center',
           fontsize=26, fontweight='bold', color=WHITE,
           bbox=dict(boxstyle='circle,pad=0.5', facecolor=RED, edgecolor=BLACK, linewidth=3))
    
    ax.text(14.95, y_flow+0.55, 'FRY Minting', ha='left', va='top',
           fontsize=16, fontweight='bold', color=BLACK)
    ax.text(14.95, y_flow+0.15, '• Rate: 1.4 FRY/$1', ha='left', va='top',
           fontsize=11, color=BLACK)
    ax.text(14.95, y_flow-0.15, '• Efficiency bonus 1.8x', ha='left', va='top',
           fontsize=11, color=BLACK)
    ax.text(14.95, y_flow-0.5, '• Quality rewards', ha='left', va='top',
           fontsize=10, color=GRAY, style='italic')
    
    # ===== FOOTER =====
    footer_box = FancyBboxPatch((0.5, 0.3), 15, 1.2,
                               boxstyle="round,pad=0.1",
                               facecolor=BLACK, edgecolor=YELLOW, linewidth=3, alpha=0.9)
    ax.add_patch(footer_box)
    
    ax.text(8, 1.2, 'Why FRY v3?', ha='center', va='center',
           fontsize=14, fontweight='bold', color=YELLOW)
    
    benefits = [
        '✓ No custody risk (cash-settled)',
        '✓ Zero token transfers',
        '✓ Mathematical optimization (number theory)',
        '✓ Provable convergence',
    ]
    
    for i, benefit in enumerate(benefits):
        x_pos = 1.5 + i * 3.5
        ax.text(x_pos, 0.7, benefit, ha='left', va='center',
               fontsize=11, color=WHITE, fontweight='bold')
    
    plt.tight_layout()
    filename = f"fry_v3_mechanics_slide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    return filename


def main():
    print("🎨 Generating FRY v3 Mechanics Slide...\n")
    
    filename = create_mechanics_slide()
    
    print(f"✅ Mechanics slide generated: {filename}\n")
    print("📊 Slide Features:")
    print("   • 16:9 aspect ratio (standard presentation)")
    print("   • Clean, professional layout")
    print("   • 4-step flow diagram with numbered steps")
    print("   • Key metrics section with performance data")
    print("   • Footer with core benefits")
    print("   • Ready for GitDocs, pitch decks, or technical docs\n")
    print("💡 Usage:")
    print("   • Drop directly into slides")
    print("   • Embed in GitDocs/README")
    print("   • Print for physical presentations")
    print("   • Share as standalone explainer")


if __name__ == '__main__':
    main()
