#!/usr/bin/env python3
"""
Behavioral Liquidity Mining - Twitter Visual
==========================================

Creates a clean, Twitter-optimized visual for the behavioral liquidity mining post.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# Set up the figure - Twitter optimized (16:9 ratio)
fig = plt.figure(figsize=(12, 6.75))
ax = fig.add_subplot(111)
ax.set_xlim(0, 12)
ax.set_ylim(0, 6.75)
ax.axis('off')

# Dark background
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Title
ax.text(6, 6, 'Behavioral Liquidity Mining', fontsize=28, weight='bold', ha='center', 
       color='#00ff88', zorder=10)

ax.text(6, 5.5, 'Extracting Alpha from Trader Psychology', fontsize=16, ha='center', 
       color='#ffffff', style='italic', zorder=10)

# ============================================
# Main Flow: Input → Processing → Output
# ============================================

# Input box
input_box = FancyBboxPatch((0.5, 3.5), 2.5, 1.5, boxstyle="round,pad=0.15", 
                          facecolor='#1a1a2e', edgecolor='#ff6b6b', linewidth=2, 
                          alpha=0.9, zorder=5)
ax.add_patch(input_box)
ax.text(1.75, 4.5, 'Liquidation Events', fontsize=14, ha='center', weight='bold', 
       color='#ff6b6b', zorder=6)
ax.text(1.75, 4.1, '22 wallets tracked', fontsize=12, ha='center', 
       color='#ffffff', zorder=6)
ax.text(1.75, 3.8, 'Behavioral fingerprints', fontsize=10, ha='center', 
       color='#cccccc', zorder=6)

# Arrow 1
arrow1 = FancyArrowPatch((3, 4.25), (4.2, 4.25), arrowstyle='->', mutation_scale=20, 
                        linewidth=3, color='#00ff88', alpha=0.8, zorder=5)
ax.add_patch(arrow1)

# Processing box
process_box = FancyBboxPatch((4.2, 3.5), 3.6, 1.5, boxstyle="round,pad=0.15", 
                            facecolor='#16213e', edgecolor='#00ff88', linewidth=2, 
                            alpha=0.9, zorder=5)
ax.add_patch(process_box)
ax.text(6, 4.5, 'Pattern Detection', fontsize=14, ha='center', weight='bold', 
       color='#00ff88', zorder=6)
ax.text(6, 4.1, 'ML Behavioral Analysis', fontsize=12, ha='center', 
       color='#ffffff', zorder=6)
ax.text(6, 3.8, '4 patterns identified', fontsize=10, ha='center', 
       color='#cccccc', zorder=6)

# Arrow 2
arrow2 = FancyArrowPatch((7.8, 4.25), (9, 4.25), arrowstyle='->', mutation_scale=20, 
                        linewidth=3, color='#00ff88', alpha=0.8, zorder=5)
ax.add_patch(arrow2)

# Output box
output_box = FancyBboxPatch((9, 3.5), 2.5, 1.5, boxstyle="round,pad=0.15", 
                           facecolor='#1a1a2e', edgecolor='#4ecdc4', linewidth=2, 
                           alpha=0.9, zorder=5)
ax.add_patch(output_box)
ax.text(10.25, 4.5, 'Alpha Signals', fontsize=14, ha='center', weight='bold', 
       color='#4ecdc4', zorder=6)
ax.text(10.25, 4.1, 'Trading opportunities', fontsize=12, ha='center', 
       color='#ffffff', zorder=6)
ax.text(10.25, 3.8, '42% vs 0% retention', fontsize=10, ha='center', 
       color='#cccccc', zorder=6)

# ============================================
# Pattern Types
# ============================================

patterns_y = 2.5
pattern_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24']
pattern_names = ['Alpha Traders', 'Retention', 'Arbitrageurs', 'Sentiment Leaders']
pattern_descriptions = ['high recovery + risk', 'loyalty + conservative', 'cross-platform + consistency', 'social influence']

for i, (color, name, desc) in enumerate(zip(pattern_colors, pattern_names, pattern_descriptions)):
    x = 1.5 + i * 2.25
    
    # Pattern circle
    circle = Circle((x, patterns_y), 0.3, facecolor=color, edgecolor='white', 
                   linewidth=2, zorder=6)
    ax.add_patch(circle)
    
    # Pattern name
    ax.text(x, patterns_y + 0.5, name, fontsize=11, ha='center', weight='bold',
           color=color, zorder=6)
    
    # Pattern description
    ax.text(x, patterns_y - 0.5, desc, fontsize=9, ha='center',
           color='#cccccc', zorder=6)

# ============================================
# Bottom: Infrastructure & Results
# ============================================

# Results summary
results_text = "Early Results: 22 wallets tracked, 42% vs 0% control group retention"
ax.text(6, 1.5, results_text, fontsize=14, ha='center', weight='bold',
       color='#f9ca24', zorder=6)

# Infrastructure note
infra_text = "Same infrastructure → retention + alpha extraction"
ax.text(6, 1, infra_text, fontsize=12, ha='center',
       color='#00ff88', zorder=6)

# GitHub link
github_text = "github.com/aidanduffy68-prog/USD_FRY"
ax.text(6, 0.5, github_text, fontsize=11, ha='center',
       color='#ffffff', zorder=6)

# Building in public
ax.text(6, 0.1, "Building in public", fontsize=10, ha='center', style='italic',
       color='#f9ca24', zorder=6)

plt.tight_layout()
plt.savefig('behavioral_mining_twitter.png', dpi=300, facecolor='#0a0a0a', 
           bbox_inches='tight', pad_inches=0.1)
print("✅ Saved: behavioral_mining_twitter.png")
plt.close()
