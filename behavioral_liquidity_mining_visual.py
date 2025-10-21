#!/usr/bin/env python3
"""
Behavioral Liquidity Mining Visual
=================================

Creates a visual showing the behavioral pattern detection process
for the Twitter post about behavioral liquidity mining.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np

# Set up the figure with a modern, technical aesthetic
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')

# Dark background for tech feel
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Title
ax.text(6, 9.2, 'Behavioral Liquidity Mining', fontsize=24, weight='bold', ha='center', 
       color='#00ff88', zorder=10)

ax.text(6, 8.7, 'Extracting Alpha from Trader Psychology', fontsize=14, ha='center', 
       color='#ffffff', style='italic', zorder=10)

# ============================================
# LEFT: Data Input Layer
# ============================================

# Liquidation events box
liquidation_box = FancyBboxPatch((0.5, 6.5), 2.5, 1.5, boxstyle="round,pad=0.1", 
                                facecolor='#1a1a2e', edgecolor='#ff6b6b', linewidth=2, 
                                alpha=0.9, zorder=5)
ax.add_patch(liquidation_box)
ax.text(1.75, 7.5, 'Liquidation Events', fontsize=12, ha='center', weight='bold', 
       color='#ff6b6b', zorder=6)
ax.text(1.75, 7.1, '22 wallets tracked', fontsize=10, ha='center', 
       color='#ffffff', zorder=6)
ax.text(1.75, 6.8, 'Behavioral fingerprints', fontsize=9, ha='center', 
       color='#cccccc', zorder=6)

# Arrow to processing
arrow1 = FancyArrowPatch((3, 7.25), (4.5, 7.25), arrowstyle='->', mutation_scale=15, 
                        linewidth=2, color='#00ff88', alpha=0.8, zorder=5)
ax.add_patch(arrow1)

# ============================================
# CENTER: Pattern Detection Engine
# ============================================

# ML Processing box
ml_box = FancyBboxPatch((4.5, 6), 3, 2.5, boxstyle="round,pad=0.15", 
                        facecolor='#16213e', edgecolor='#00ff88', linewidth=2, 
                        alpha=0.9, zorder=5)
ax.add_patch(ml_box)
ax.text(6, 7.8, 'Pattern Detection Engine', fontsize=12, ha='center', weight='bold', 
       color='#00ff88', zorder=6)
ax.text(6, 7.4, 'ML Behavioral Analysis', fontsize=10, ha='center', 
       color='#ffffff', zorder=6)

# Pattern indicators inside the box
patterns = [
    ('Alpha Traders', '#ff6b6b', 0.3),
    ('Retention', '#4ecdc4', 0.5),
    ('Arbitrage', '#45b7d1', 0.7),
    ('Sentiment', '#f9ca24', 0.9)
]

for i, (pattern, color, y_pos) in enumerate(patterns):
    # Small indicator circles
    circle = Circle((5.2, 6.8 - i*0.3), 0.08, facecolor=color, edgecolor='white', 
                   linewidth=1, zorder=6)
    ax.add_patch(circle)
    ax.text(5.4, 6.8 - i*0.3, pattern, fontsize=9, ha='left', va='center',
           color='white', zorder=6)

# Arrow to output
arrow2 = FancyArrowPatch((7.5, 7.25), (9, 7.25), arrowstyle='->', mutation_scale=15, 
                        linewidth=2, color='#00ff88', alpha=0.8, zorder=5)
ax.add_patch(arrow2)

# ============================================
# RIGHT: Alpha Signals Output
# ============================================

# Alpha signals box
alpha_box = FancyBboxPatch((9, 6.5), 2.5, 1.5, boxstyle="round,pad=0.1", 
                          facecolor='#1a1a2e', edgecolor='#4ecdc4', linewidth=2, 
                          alpha=0.9, zorder=5)
ax.add_patch(alpha_box)
ax.text(10.25, 7.5, 'Alpha Signals', fontsize=12, ha='center', weight='bold', 
       color='#4ecdc4', zorder=6)
ax.text(10.25, 7.1, 'Trading opportunities', fontsize=10, ha='center', 
       color='#ffffff', zorder=6)
ax.text(10.25, 6.8, '42% vs 0% retention', fontsize=9, ha='center', 
       color='#cccccc', zorder=6)

# ============================================
# BOTTOM: Results Summary
# ============================================

# Results box
results_box = FancyBboxPatch((1, 3.5), 10, 2, boxstyle="round,pad=0.2", 
                           facecolor='#0f3460', edgecolor='#f9ca24', linewidth=2, 
                           alpha=0.9, zorder=5)
ax.add_patch(results_box)

ax.text(6, 5, 'Early Results', fontsize=16, ha='center', weight='bold', 
       color='#f9ca24', zorder=6)

# Results metrics
metrics = [
    ('22 wallets tracked', '#ffffff'),
    ('42% vs 0% control retention', '#4ecdc4'),
    ('4 behavioral patterns detected', '#ff6b6b'),
    ('Same infrastructure → retention + alpha', '#00ff88')
]

for i, (metric, color) in enumerate(metrics):
    ax.text(6, 4.5 - i*0.3, f'• {metric}', fontsize=11, ha='center', 
           color=color, zorder=6)

# ============================================
# BOTTOM: Infrastructure Note
# ============================================

infra_box = FancyBboxPatch((2, 1.5), 8, 1.2, boxstyle="round,pad=0.15", 
                          facecolor='#1a1a2e', edgecolor='#666666', linewidth=1, 
                          alpha=0.8, zorder=5)
ax.add_patch(infra_box)

ax.text(6, 2.3, 'Infrastructure: Retention Oracle + Behavioral Mining', fontsize=12, ha='center', 
       color='#ffffff', weight='bold', zorder=6)
ax.text(6, 1.9, 'github.com/aidanduffy68-prog/USD_FRY', fontsize=10, ha='center', 
       color='#00ff88', zorder=6)
ax.text(6, 1.6, 'Building in public 🍟', fontsize=10, ha='center', 
       color='#f9ca24', style='italic', zorder=6)

# ============================================
# DECORATIVE ELEMENTS
# ============================================

# Add some subtle data flow indicators
for i in range(3):
    x = 1 + i * 4
    y = 5.5
    # Small data points
    for j in range(5):
        dot_y = y + (j - 2) * 0.1
        dot = Circle((x, dot_y), 0.02, facecolor='#00ff88', alpha=0.3, zorder=3)
        ax.add_patch(dot)

# Add subtle grid lines
for i in range(1, 12):
    ax.axvline(i, color='#333333', alpha=0.2, linewidth=0.5, zorder=1)
for i in range(1, 10):
    ax.axhline(i, color='#333333', alpha=0.2, linewidth=0.5, zorder=1)

plt.tight_layout()
plt.savefig('behavioral_liquidity_mining_visual.png', dpi=300, facecolor='#0a0a0a', 
           bbox_inches='tight', pad_inches=0.2)
print("✅ Saved: behavioral_liquidity_mining_visual.png")
plt.close()
