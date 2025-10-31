#!/usr/bin/env python3
"""
Read vs Read-Write Oracles - Contrast Diagram

Left: read-only (reports state)
Right: read-write (changes state)

Output: read_vs_readwrite_flow.png/.pdf
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def card(ax, x, y, w, h, title, bullets, color):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.18",
                         edgecolor='#1a1a1a', facecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h - 0.5, title, ha='center', va='top', fontsize=14, fontweight='bold')
    for i, line in enumerate(bullets):
        ax.text(x + 0.4, y + h - 1.2 - 0.7*i, f"• {line}", ha='left', va='top', fontsize=12)


def example(ax, x, y, w):
    ax.text(x, y, 'Example:', ha='left', va='center', fontsize=12, color='#1a1a1a', fontweight='bold')
    ax.text(x + 1.0, y, '55% risk → +100 FRY → 45%',
            ha='left', va='center', fontsize=12, color='#1a1a1a')


def main():
    # Original layout (not banner-sized)
    plt.rcParams['figure.dpi'] = 300
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor('white')

    ax.text(9, 9.3, 'read vs read-write oracles', ha='center', va='center', fontsize=18, fontweight='bold')
    ax.text(9, 8.6, 'read: observe | read-write: observe + act', ha='center', va='center', fontsize=12, color='#4d4d4d')

    # Left (read-only)
    card(ax, 1.0, 2.0, 7.5, 5.5,
         'read-only oracle',
         [
             'compresses market causality',
             'reports the state',
             'no effect on outcomes',
             'example: price feeds'
         ],
         color="#f7f7f7")

    # Right (read-write)
    card(ax, 9.5, 2.0, 7.5, 5.5,
         'read-write oracle',
         [
             'compresses behavioral causality',
             'changes the state (policy/incentives)',
             'prediction closes the loop',
             'example: retention oracle (Narcissus)'
         ],
         color="#eefaf1")

    # Example line removed for cleaner layout at small sizes

    ax.text(9, 0.7, 'Greenhouse & Company — Dark intelligence research for crypto',
            ha='center', va='center', fontsize=10, color='#6b6b6b')

    plt.tight_layout()
    plt.savefig('read_vs_readwrite_flow.png', bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.savefig('read_vs_readwrite_flow.pdf', bbox_inches='tight', facecolor='white', pad_inches=0.2)
    print('✅ Generated read_vs_readwrite_flow.[png|pdf]')


if __name__ == '__main__':
    main()


