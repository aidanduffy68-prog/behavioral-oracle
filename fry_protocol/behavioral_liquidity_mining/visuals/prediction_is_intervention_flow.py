#!/usr/bin/env python3
"""
Prediction IS Intervention - Flow Diagram

Windows-tab style, pure white background. Shows how causal compression
feeds a read-write intervention loop in a reverse oracle.

Output: prediction_is_intervention_flow.png/.pdf
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ArrowStyle


def add_card(ax, xy, text, width=3.4, height=1.3, fc="#ffffff", ec="#1a1a1a"):
    x, y = xy
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.15",
                         edgecolor=ec, facecolor=fc, linewidth=2)
    ax.add_patch(box)
    ax.text(x + width / 2, y + height / 2, text,
            ha='center', va='center', fontsize=12, fontweight='bold', color='#1a1a1a')
    return (x + width, y + height)


def arrow(ax, p1, p2):
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle=ArrowStyle("Simple", head_width=4, head_length=6),
                                color="#1a1a1a", linewidth=1.2))


def main():
    # Original layout (not banner-sized)
    plt.rcParams['figure.dpi'] = 300
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor('white')

    # Title strip (Windows tab vibe)
    ax.text(9, 9.3, 'prediction IS intervention', ha='center', va='center',
            fontsize=18, fontweight='bold', color='#1a1a1a')
    ax.text(9, 8.6, 'reverse oracles compress causality AND write to it',
            ha='center', va='center', fontsize=12, color='#4d4d4d')

    # Two-column layout
    ax.text(3.0, 7.9, 'Compression', ha='center', va='bottom', fontsize=13, fontweight='bold', color='#1a1a1a')
    ax.text(14.5, 7.9, 'Intervention loop', ha='center', va='bottom', fontsize=13, fontweight='bold', color='#1a1a1a')

    # Left column (vertical)
    add_card(ax, (1.3, 6.8), 'Data stream\n(liquidations, behavior)')
    arrow(ax, (3.0, 6.75), (3.0, 5.5))
    add_card(ax, (1.3, 4.1), 'Causal compression\n(pattern learning)')
    arrow(ax, (3.0, 4.05), (3.0, 2.8))
    add_card(ax, (1.3, 1.4), 'Prediction\n(retention, risk)')

    # Right column (vertical)
    add_card(ax, (12.8, 6.8), 'Intervention\n(incentives, policy)')
    arrow(ax, (14.5, 6.75), (14.5, 5.5))
    add_card(ax, (12.8, 4.1), 'Behavior shift\n(updated state)')
    arrow(ax, (14.5, 4.05), (14.5, 2.8))
    add_card(ax, (12.8, 1.4), 'New observations\n(feedback data)')

    # Cross-links
    arrow(ax, (4.8, 2.05), (12.6, 6.05))  # Prediction -> Intervention
    arrow(ax, (12.6, 1.95), (4.6, 6.05))  # New observations -> Data stream

    # Footer
    ax.text(9, 0.8, 'Greenhouse & Company — Dark intelligence research for crypto',
            ha='center', va='center', fontsize=10, color='#6b6b6b')

    plt.tight_layout()
    plt.savefig('prediction_is_intervention_flow.png', bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.savefig('prediction_is_intervention_flow.pdf', bbox_inches='tight', facecolor='white', pad_inches=0.2)
    print('✅ Generated prediction_is_intervention_flow.[png|pdf]')


if __name__ == '__main__':
    main()


