import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# XP window size (8x5 inches)
fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot(111)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Frutiger Aero gradient background (sky blue to white)
gradient = np.linspace(0, 1, 256).reshape(1, -1)
gradient = np.vstack((gradient, gradient))
ax.imshow(gradient, aspect='auto', extent=[0, 10, 0, 10], 
         cmap='Blues_r', alpha=0.3, zorder=0)

# Add subtle bubbles/orbs in background
np.random.seed(42)
for _ in range(15):
    x = np.random.uniform(0, 10)
    y = np.random.uniform(0, 10)
    size = np.random.uniform(0.2, 0.6)
    bubble = Circle((x, y), size, facecolor='white', edgecolor='#4A90E2', 
                   linewidth=1, alpha=0.3, zorder=1)
    ax.add_patch(bubble)

# Title at top
ax.text(5, 9.3, 'reverse oracles', fontsize=18, weight='bold', ha='center', 
       color='white', style='italic', 
       bbox=dict(boxstyle='round,pad=0.5', facecolor='#4A90E2', edgecolor='none', alpha=0.8),
       zorder=10)

# ============================================
# LEFT: Traditional Oracle
# ============================================

# Oracle icon (left side)
oracle_circle = Circle((2.5, 6.5), 0.7, facecolor='#E8F4F8', edgecolor='#0066CC', 
                      linewidth=3, zorder=5)
ax.add_patch(oracle_circle)
ax.text(2.5, 6.5, '🔮', fontsize=28, ha='center', va='center', zorder=6)

# Label
ax.text(2.5, 5.3, 'Traditional', fontsize=10, ha='center', weight='bold', 
       color='#0066CC', zorder=5)
ax.text(2.5, 4.9, 'Price Discovery', fontsize=8, ha='center', 
       color='#666666', style='italic', zorder=5)

# Arrow down
arrow1 = FancyArrowPatch((2.5, 4.6), (2.5, 3.5), arrowstyle='->', mutation_scale=20, 
                        linewidth=2.5, color='#0066CC', alpha=0.7, zorder=5)
ax.add_patch(arrow1)

# Box
box1 = FancyBboxPatch((1, 2), 3, 1.2, boxstyle="round,pad=0.15", 
                     facecolor='white', edgecolor='#0066CC', linewidth=2, 
                     alpha=0.9, zorder=5)
ax.add_patch(box1)
ax.text(2.5, 2.8, 'Markets', fontsize=10, ha='center', weight='bold', 
       color='#0066CC', zorder=6)
ax.text(2.5, 2.4, 'BTC, ETH, Prices', fontsize=7, ha='center', 
       color='#666666', zorder=6)

# ============================================
# RIGHT: Reverse Oracle
# ============================================

# Oracle icon (right side)
reverse_circle = Circle((7.5, 6.5), 0.7, facecolor='#FFE6E6', edgecolor='#CC0000', 
                       linewidth=3, zorder=5)
ax.add_patch(reverse_circle)
ax.text(7.5, 6.5, '🪞', fontsize=28, ha='center', va='center', zorder=6)

# Label
ax.text(7.5, 5.3, 'Reverse', fontsize=10, ha='center', weight='bold', 
       color='#CC0000', zorder=5)
ax.text(7.5, 4.9, 'Behavior Prediction', fontsize=8, ha='center', 
       color='#666666', style='italic', zorder=5)

# Arrow down
arrow2 = FancyArrowPatch((7.5, 4.6), (7.5, 3.5), arrowstyle='->', mutation_scale=20, 
                        linewidth=2.5, color='#CC0000', alpha=0.7, zorder=5)
ax.add_patch(arrow2)

# Box
box2 = FancyBboxPatch((6, 2), 3, 1.2, boxstyle="round,pad=0.15", 
                     facecolor='white', edgecolor='#CC0000', linewidth=2, 
                     alpha=0.9, zorder=5)
ax.add_patch(box2)
ax.text(7.5, 2.8, 'Traders', fontsize=10, ha='center', weight='bold', 
       color='#CC0000', zorder=6)
ax.text(7.5, 2.4, 'Activity, Churn', fontsize=7, ha='center', 
       color='#666666', zorder=6)

# Bottom tagline
ax.text(5, 0.7, 'predicting traders, not prices', fontsize=11, ha='center', 
       weight='bold', color='#4A90E2', style='italic', zorder=10)

plt.tight_layout()
plt.savefig('core/oracle/reverse_oracle_frutiger.png', dpi=300, facecolor='white', bbox_inches='tight')
print("✅ Saved: core/oracle/reverse_oracle_frutiger.png")
plt.close()
