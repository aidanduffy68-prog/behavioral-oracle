#!/usr/bin/env python3
"""
Behavioral Liquidity Mining - Windows 95 Style Visual
====================================================

Creates a Windows 95-style visual for the behavioral liquidity mining post.
Fits perfectly in a classic text editor window with white background.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

# Set up the figure - Windows 95 style
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')

# White background like Windows 95
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# Title in Windows 95 style
ax.text(5, 6.5, 'Behavioral Liquidity Mining', fontsize=20, weight='bold', ha='center', 
       color='#000080', zorder=10)

ax.text(5, 6.1, 'Extracting Alpha from Trader Psychology', fontsize=12, ha='center', 
       color='#000000', zorder=10)

# ============================================
# Main Flow Boxes (Windows 95 style)
# ============================================

# Input box - Windows 95 button style
input_box = Rectangle((0.5, 4.5), 2, 1, facecolor='#c0c0c0', edgecolor='#808080', 
                     linewidth=2, zorder=5)
ax.add_patch(input_box)
# Inner highlight
inner_box1 = Rectangle((0.6, 4.6), 1.8, 0.8, facecolor='#e0e0e0', edgecolor='#ffffff', 
                      linewidth=1, zorder=6)
ax.add_patch(inner_box1)

ax.text(1.5, 5.2, 'Liquidation Events', fontsize=11, ha='center', weight='bold', 
       color='#000000', zorder=7)
ax.text(1.5, 4.9, '22 wallets tracked', fontsize=9, ha='center', 
       color='#000000', zorder=7)

# Arrow 1
arrow1 = FancyArrowPatch((2.5, 5), (3.5, 5), arrowstyle='->', mutation_scale=15, 
                        linewidth=2, color='#000000', zorder=5)
ax.add_patch(arrow1)

# Processing box
process_box = Rectangle((3.5, 4.5), 3, 1, facecolor='#c0c0c0', edgecolor='#808080', 
                       linewidth=2, zorder=5)
ax.add_patch(process_box)
inner_box2 = Rectangle((3.6, 4.6), 2.8, 0.8, facecolor='#e0e0e0', edgecolor='#ffffff', 
                      linewidth=1, zorder=6)
ax.add_patch(inner_box2)

ax.text(5, 5.2, 'Pattern Detection Engine', fontsize=11, ha='center', weight='bold', 
       color='#000000', zorder=7)
ax.text(5, 4.9, 'ML Behavioral Analysis', fontsize=9, ha='center', 
       color='#000000', zorder=7)

# Arrow 2
arrow2 = FancyArrowPatch((6.5, 5), (7.5, 5), arrowstyle='->', mutation_scale=15, 
                        linewidth=2, color='#000000', zorder=5)
ax.add_patch(arrow2)

# Output box
output_box = Rectangle((7.5, 4.5), 2, 1, facecolor='#c0c0c0', edgecolor='#808080', 
                      linewidth=2, zorder=5)
ax.add_patch(output_box)
inner_box3 = Rectangle((7.6, 4.6), 1.8, 0.8, facecolor='#e0e0e0', edgecolor='#ffffff', 
                      linewidth=1, zorder=6)
ax.add_patch(inner_box3)

ax.text(8.5, 5.2, 'Alpha Signals', fontsize=11, ha='center', weight='bold', 
       color='#000000', zorder=7)
ax.text(8.5, 4.9, '42% vs 0% retention', fontsize=9, ha='center', 
       color='#000000', zorder=7)

# ============================================
# Pattern Types (Windows 95 buttons)
# ============================================

patterns_y = 3
pattern_names = ['Alpha Traders', 'Retention', 'Arbitrageurs', 'Sentiment']
pattern_descriptions = ['high recovery + risk', 'loyalty + conservative', 'cross-platform + consistency', 'social influence']

for i, (name, desc) in enumerate(zip(pattern_names, pattern_descriptions)):
    x = 0.5 + i * 2.25
    
    # Windows 95 button style
    button = Rectangle((x, patterns_y), 2, 0.8, facecolor='#c0c0c0', edgecolor='#808080', 
                      linewidth=2, zorder=5)
    ax.add_patch(button)
    
    # Inner highlight
    inner_button = Rectangle((x + 0.05, patterns_y + 0.05), 1.9, 0.7, facecolor='#e0e0e0', 
                           edgecolor='#ffffff', linewidth=1, zorder=6)
    ax.add_patch(inner_button)
    
    # Button text
    ax.text(x + 1, patterns_y + 0.5, name, fontsize=10, ha='center', weight='bold',
           color='#000000', zorder=7)
    
    ax.text(x + 1, patterns_y + 0.2, desc, fontsize=8, ha='center',
           color='#000000', zorder=7)

# ============================================
# Results Section (Windows 95 style)
# ============================================

# Results box
results_box = Rectangle((1, 1.5), 8, 1, facecolor='#c0c0c0', edgecolor='#808080', 
                       linewidth=2, zorder=5)
ax.add_patch(results_box)
inner_results = Rectangle((1.05, 1.55), 7.9, 0.9, facecolor='#e0e0e0', edgecolor='#ffffff', 
                         linewidth=1, zorder=6)
ax.add_patch(inner_results)

ax.text(5, 2.2, 'Early Results: 22 wallets tracked, 42% vs 0% control group retention', 
       fontsize=11, ha='center', weight='bold', color='#000000', zorder=7)

ax.text(5, 1.8, 'Same infrastructure → retention + alpha extraction', 
       fontsize=10, ha='center', color='#000000', zorder=7)

# ============================================
# Bottom Info
# ============================================

ax.text(5, 0.8, 'github.com/aidanduffy68-prog/USD_FRY', fontsize=10, ha='center',
       color='#000080', zorder=6)

ax.text(5, 0.4, 'Building in public', fontsize=9, ha='center', style='italic',
       color='#000000', zorder=6)

# Add some Windows 95 style decorative elements
# Small squares in corners
for x, y in [(0.2, 6.8), (9.8, 6.8), (0.2, 0.2), (9.8, 0.2)]:
    corner = Rectangle((x, y), 0.1, 0.1, facecolor='#808080', zorder=3)
    ax.add_patch(corner)

plt.tight_layout()
plt.savefig('behavioral_mining_windows95.png', dpi=300, facecolor='#ffffff', 
           bbox_inches='tight', pad_inches=0.1)
print("✅ Saved: behavioral_mining_windows95.png")
plt.close()
