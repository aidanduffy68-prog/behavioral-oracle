#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRY v3 Topology × Minting Insights Slide
=========================================

Clean slide with Visualization Key, Network Stats, and Key Insights
from the combined 3D topology visualization.

Output: High-quality PNG slide
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def create_insights_slide():
    """Generate FRY v3 topology insights slide"""
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=WHITE)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # ===== HEADER =====
    ax.text(8, 8.5, 'FRY v3: Network Topology × Minting Surface', 
            ha='center', va='top', fontsize=32, fontweight='bold', color=BLACK)
    ax.text(8, 8.05, 'Understanding the 3D visualization',
            ha='center', va='top', fontsize=15, color=GRAY, style='italic')
    
    # Divider line
    ax.plot([0.5, 15.5], [7.75, 7.75], color=LIGHT_GRAY, linewidth=3)
    
    # ===== VISUALIZATION KEY =====
    y_key = 6.8
    
    key_box = FancyBboxPatch((0.5, y_key-2.0), 5.0, 1.9,
                            boxstyle="round,pad=0.15",
                            facecolor=YELLOW, edgecolor=BLACK, linewidth=3, alpha=0.15)
    ax.add_patch(key_box)
    
    ax.text(3.0, y_key-0.1, 'Visualization Key', ha='center', va='top',
           fontsize=20, fontweight='bold', color=BLACK)
    
    key_lines = [
        '• Surface = FRY minting function',
        '• Nodes = DEX positions in parameter space',
        '• Lines = Active funding swaps',
        '• Node height = FRY output at that point',
        '• Yellow = Positive funding | Red = Negative'
    ]
    
    y_pos = y_key - 0.5
    for line in key_lines:
        ax.text(0.8, y_pos, line, ha='left', va='top',
               fontsize=13, color=BLACK)
        y_pos -= 0.28
    
    # ===== NETWORK STATS =====
    stats_box = FancyBboxPatch((6.0, y_key-2.0), 4.5, 1.9,
                              boxstyle="round,pad=0.15",
                              facecolor=RED, edgecolor=BLACK, linewidth=3, alpha=0.15)
    ax.add_patch(stats_box)
    
    ax.text(8.25, y_key-0.1, 'Network Stats', ha='center', va='top',
           fontsize=20, fontweight='bold', color=BLACK)
    
    stats_lines = [
        '• 4 DEXes mapped to surface',
        '• 3 active swaps',
        '• Avg efficiency: 79%',
        '• Total notional: $11.9K',
        '• Surface shows optimal zones'
    ]
    
    y_pos = y_key - 0.5
    for line in stats_lines:
        ax.text(6.3, y_pos, line, ha='left', va='top',
               fontsize=13, color=BLACK)
        y_pos -= 0.28
    
    # ===== KEY INSIGHTS =====
    insights_box = FancyBboxPatch((11.0, y_key-2.0), 4.5, 1.9,
                                 boxstyle="round,pad=0.15",
                                 facecolor=YELLOW, edgecolor=BLACK, linewidth=3, alpha=0.3)
    ax.add_patch(insights_box)
    
    ax.text(13.25, y_key-0.1, 'Key Insights', ha='center', va='top',
           fontsize=20, fontweight='bold', color=BLACK)
    
    insights_lines = [
        'DEXes cluster in high-efficiency',
        'zones of the minting surface.',
        '',
        'Network topology emerges from',
        'optimization dynamics.'
    ]
    
    y_pos = y_key - 0.5
    for line in insights_lines:
        if line:
            ax.text(11.3, y_pos, line, ha='left', va='top',
                   fontsize=13, color=BLACK, fontweight='bold')
        y_pos -= 0.28
    
    # ===== MAIN EXPLANATION SECTION =====
    y_explain = 3.8
    
    ax.text(8, y_explain+0.5, 'What This Means', ha='center', va='top',
           fontsize=24, fontweight='bold', color=BLACK)
    
    # Left column - The Visualization
    left_box = FancyBboxPatch((0.5, y_explain-2.2), 7.0, 2.1,
                             boxstyle="round,pad=0.15",
                             facecolor=LIGHT_GRAY, edgecolor=BLACK, linewidth=2, alpha=0.3)
    ax.add_patch(left_box)
    
    ax.text(4.0, y_explain-0.1, 'The Visualization', ha='center', va='top',
           fontsize=18, fontweight='bold', color=DARK_RED)
    
    viz_text = [
        'The 3D surface represents the theoretical FRY',
        'output for any combination of swap notional',
        'and hedge efficiency.',
        '',
        'DEX nodes are positioned at their actual',
        '(notional, efficiency) coordinates.',
        '',
        'Their height shows real FRY minting at that point.'
    ]
    
    y_pos = y_explain - 0.5
    for line in viz_text:
        if line:
            ax.text(4.0, y_pos, line, ha='center', va='top',
                   fontsize=12, color=BLACK)
        y_pos -= 0.22
    
    # Right column - The Insight
    right_box = FancyBboxPatch((8.5, y_explain-2.2), 7.0, 2.1,
                              boxstyle="round,pad=0.15",
                              facecolor=RED, edgecolor=BLACK, linewidth=2, alpha=0.15)
    ax.add_patch(right_box)
    
    ax.text(12.0, y_explain-0.1, 'The Insight', ha='center', va='top',
           fontsize=18, fontweight='bold', color=DARK_RED)
    
    insight_text = [
        'The network isn\'t arbitrary—it\'s the natural',
        'equilibrium that emerges when you optimize',
        'FRY minting across DEXes.',
        '',
        'This is a phase diagram of the protocol.',
        '',
        'Topology = optimization dynamics made visible.'
    ]
    
    y_pos = y_explain - 0.5
    for line in insight_text:
        if line:
            ax.text(12.0, y_pos, line, ha='center', va='top',
                   fontsize=12, color=BLACK, fontweight='bold' if 'equilibrium' in line or 'phase diagram' in line else 'normal')
        y_pos -= 0.22
    
    # ===== FOOTER =====
    footer_box = FancyBboxPatch((0.5, 0.2), 15, 0.9,
                               boxstyle="round,pad=0.1",
                               facecolor=BLACK, edgecolor=YELLOW, linewidth=3, alpha=0.9)
    ax.add_patch(footer_box)
    
    ax.text(8, 0.75, 'FRY v3 = Mathematical optimization meets network topology', 
           ha='center', va='center', fontsize=16, fontweight='bold', color=YELLOW)
    ax.text(8, 0.4, 'The surface shows where to mint. The network shows where DEXes actually are.', 
           ha='center', va='center', fontsize=12, color=WHITE, style='italic')
    
    plt.tight_layout()
    filename = f"fry_v3_topology_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    return filename


def main():
    print("🎨 Generating FRY v3 Topology Insights Slide...\n")
    
    filename = create_insights_slide()
    
    print(f"✅ Insights slide generated: {filename}\n")
    print("📊 Slide Contents:")
    print("   • Visualization Key - explains the 3D elements")
    print("   • Network Stats - key metrics from the topology")
    print("   • Key Insights - what the visualization reveals")
    print("   • Main Explanation - what it means and why it matters\n")
    print("💡 Perfect for:")
    print("   • Following the 3D visualization")
    print("   • Explaining the topology concept")
    print("   • Technical presentations")
    print("   • Documentation")


if __name__ == '__main__':
    main()
