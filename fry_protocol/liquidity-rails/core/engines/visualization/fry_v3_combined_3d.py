#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRY v3: Combined 3D Network + Minting Surface
==============================================

Ultimate visualization combining:
- 3D network graph (DEX nodes + swap connections)
- 3D FRY minting surface (notional × efficiency)
- Shows how network topology maps to minting dynamics

Output: Single mind-blowing 3D visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

plt.switch_backend('Agg')

# FRY colors
WHITE = '#FFFFFF'
BLACK = '#000000'
RED = '#FF4444'
YELLOW = '#FFD700'
GRAY = '#7f7f7f'
DARK_RED = '#CC0000'


def generate_combined_3d():
    """Combined 3D network + minting surface"""
    fig = plt.figure(figsize=(18, 14), facecolor=WHITE)
    ax = fig.add_subplot(111, projection='3d', facecolor=WHITE)
    
    # ===== LAYER 1: FRY Minting Surface (base layer) =====
    # Create mesh for minting surface
    notional = np.linspace(1000, 10000, 40)
    efficiency = np.linspace(0.5, 0.95, 40)
    N, E = np.meshgrid(notional, efficiency)
    
    # FRY minting formula
    base_rate = 1.4
    FRY = base_rate * N * (1 + E * 0.8) / 10000  # Scaled for visibility
    
    # Plot surface with transparency
    surf = ax.plot_surface(N/10000, E, FRY, cmap='hot', alpha=0.3, 
                          linewidth=0, antialiased=True, zorder=1)
    
    # Add contour lines on surface
    ax.contour(N/10000, E, FRY, zdir='z', offset=0, cmap='hot', 
              alpha=0.2, linewidths=1, zorder=1)
    
    # ===== LAYER 2: DEX Network with FryBot Dealing Flow =====
    # DEX nodes positioned in the efficiency-notional space
    dexes = [
        {'name': 'dYdX', 'notional': 5000, 'efficiency': 0.85, 'funding': -0.15, 'volume': 45000},
        {'name': 'Hyperliquid', 'notional': 3200, 'efficiency': 0.78, 'funding': 0.18, 'volume': 38000},
        {'name': 'Aster', 'notional': 4500, 'efficiency': 0.82, 'funding': -0.12, 'volume': 32000},
        {'name': 'GMX', 'notional': 2700, 'efficiency': 0.71, 'funding': 0.20, 'volume': 28000},
    ]
    
    # Calculate FRY output for each DEX (Z position)
    for dex in dexes:
        dex['x'] = dex['notional'] / 10000
        dex['y'] = dex['efficiency']
        dex['z'] = base_rate * dex['notional'] * (1 + dex['efficiency'] * 0.8) / 10000
    
    # ===== TRADE 1: FryBot dealing flow - optimal efficiency routing =====
    # Order DEXes by efficiency for optimal routing
    sorted_dexes_1 = sorted(enumerate(dexes), key=lambda x: x[1]['efficiency'], reverse=True)
    
    # Create continuous dealing flow path for Trade 1
    flow_path_1 = []
    for idx, (i, dex) in enumerate(sorted_dexes_1):
        flow_path_1.append((dex['x'], dex['y'], dex['z']))
    
    # Draw Trade 1 flow
    for i in range(len(flow_path_1) - 1):
        x1, y1, z1 = flow_path_1[i]
        x2, y2, z2 = flow_path_1[i + 1]
        
        # Gradient from yellow (high efficiency) to red (lower efficiency)
        progress = i / (len(flow_path_1) - 1)
        color = YELLOW if progress < 0.5 else RED
        linewidth = 6 - (i * 1.5)  # Taper as we move through venues
        
        ax.plot([x1, x2], [y1, y2], [z1, z2], color=color, linewidth=linewidth, 
               alpha=0.85, zorder=10, linestyle='-')
        
        # Add flow direction arrows
        mid_x, mid_y, mid_z = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
        dx, dy, dz = (x2 - x1) * 0.1, (y2 - y1) * 0.1, (z2 - z1) * 0.1
        ax.quiver(mid_x, mid_y, mid_z, dx, dy, dz, 
                 color=color, arrow_length_ratio=0.3, linewidth=2, alpha=0.7, zorder=11)
    
    # ===== TRADE 2: Alternative routing (funding-based) =====
    # Order DEXes by funding rate (negative to positive) for different strategy
    sorted_dexes_2 = sorted(enumerate(dexes), key=lambda x: x[1]['funding'])
    
    # Create continuous dealing flow path for Trade 2
    flow_path_2 = []
    for idx, (i, dex) in enumerate(sorted_dexes_2):
        # Slightly offset to make it visible
        offset = 0.02
        flow_path_2.append((dex['x'] + offset, dex['y'] - offset*0.5, dex['z'] + offset*2))
    
    # Draw Trade 2 flow (slightly transparent, different style)
    for i in range(len(flow_path_2) - 1):
        x1, y1, z1 = flow_path_2[i]
        x2, y2, z2 = flow_path_2[i + 1]
        
        # Different color scheme for Trade 2 (cyan to purple gradient)
        progress = i / (len(flow_path_2) - 1)
        color = '#00FFFF' if progress < 0.5 else '#FF00FF'
        linewidth = 5 - (i * 1.2)
        
        ax.plot([x1, x2], [y1, y2], [z1, z2], color=color, linewidth=linewidth, 
               alpha=0.6, zorder=9, linestyle='--')
        
        # Add flow direction arrows for Trade 2
        mid_x, mid_y, mid_z = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
        dx, dy, dz = (x2 - x1) * 0.1, (y2 - y1) * 0.1, (z2 - z1) * 0.1
        ax.quiver(mid_x, mid_y, mid_z, dx, dy, dz, 
                 color=color, arrow_length_ratio=0.3, linewidth=1.5, alpha=0.5, zorder=9)
    
    # Draw DEX nodes as spheres
    for dex in dexes:
        node_size = 300 + (dex['volume'] / 80)
        node_color = RED if dex['funding'] < 0 else YELLOW
        
        ax.scatter([dex['x']], [dex['y']], [dex['z']], 
                  s=node_size, c=node_color, edgecolors=WHITE, linewidths=3, 
                  alpha=0.95, zorder=12, depthshade=True)
        
        # DEX name with connector line
        ax.plot([dex['x'], dex['x']], [dex['y'], dex['y']], [dex['z'], dex['z'] + 0.15],
               color=WHITE, linewidth=1, alpha=0.5, zorder=11)
        
        ax.text(dex['x'], dex['y'], dex['z'] + 0.18, dex['name'], 
               ha='center', va='bottom', fontsize=11, fontweight='bold', 
               color=WHITE, zorder=13)
        
        # Funding rate inside node
        funding_text = f"{dex['funding']:+.0%}"
        ax.text(dex['x'], dex['y'], dex['z'], funding_text, 
               ha='center', va='center', fontsize=8, fontweight='bold', 
               color=BLACK if dex['funding'] > 0 else WHITE, zorder=13)
    
    # ===== Styling =====
    ax.set_xlabel('Swap Notional ($10K)', fontsize=11, fontweight='bold', color=BLACK, labelpad=10)
    ax.set_ylabel('Hedge Efficiency', fontsize=11, fontweight='bold', color=BLACK, labelpad=10)
    ax.set_zlabel('FRY Minted (scaled)', fontsize=11, fontweight='bold', color=BLACK, labelpad=10)
    
    # Transparent panes
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor(GRAY)
    ax.yaxis.pane.set_edgecolor(GRAY)
    ax.zaxis.pane.set_edgecolor(GRAY)
    ax.xaxis.pane.set_alpha(0.1)
    ax.yaxis.pane.set_alpha(0.1)
    ax.zaxis.pane.set_alpha(0.1)
    
    ax.grid(True, alpha=0.15, color=GRAY)
    
    ax.tick_params(colors=BLACK, labelsize=9)
    ax.xaxis.label.set_color(BLACK)
    ax.yaxis.label.set_color(BLACK)
    ax.zaxis.label.set_color(BLACK)
    
    # Optimal viewing angle
    ax.view_init(elev=25, azim=135)
    
    # Set axis limits for better view
    ax.set_xlim(0.1, 1.0)
    ax.set_ylim(0.5, 1.0)
    
    # Add legend/labels to differentiate the two trade routes (left side, above vertical axis)
    legend_text = (
        "Trade Routes:\n"
        "━━━ Trade 1: Efficiency-optimized\n"
        "        (Yellow→Red, by hedge quality)\n"
        "- - - Trade 2: Funding-optimized\n"
        "        (Cyan→Purple, by funding rate)"
    )
    ax.text2D(0.02, 0.55, legend_text, transform=ax.transAxes, fontsize=11, 
             color=BLACK, va='center', family='monospace',
             bbox=dict(boxstyle='round,pad=0.6', facecolor=WHITE, alpha=0.9, 
                      edgecolor=BLACK, linewidth=2))
    
    plt.tight_layout()
    filename = f"fry_v3_combined_3d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    return filename


def main():
    print("🎨 Generating FRY v3 Combined 3D Visualization...\n")
    
    filename = generate_combined_3d()
    
    print(f"✅ Combined visualization generated: {filename}\n")
    
    print("💡 Pitch Angle:")
    print("   This shows the ENTIRE system in one view:")
    print("   • The surface is the FRY minting function (notional × efficiency)")
    print("   • DEX nodes are positioned in this parameter space")
    print("   • Their HEIGHT shows actual FRY output")
    print("   • Swap lines connect nodes across the surface")
    print("   • You can see how network topology emerges from optimization\n")
    
    print("🔥 Quant Impact:")
    print("   'The network isn't arbitrary—it's the natural equilibrium")
    print("    that emerges when you optimize FRY minting across DEXes.")
    print("    This is a phase diagram of the protocol.'")


if __name__ == '__main__':
    main()
