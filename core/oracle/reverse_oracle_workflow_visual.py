import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# XP window size (8x5 inches)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), facecolor='white')

# ============================================
# LEFT: The Window (Traditional Oracle)
# ============================================
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')

# Title
ax1.text(5, 9.2, 'THE WINDOW', fontsize=13, weight='bold', ha='center', color='#4A90E2')
ax1.text(5, 8.6, 'Oracles look outward', fontsize=9, ha='center', style='italic', color='#666666')

# Happy face looking outward (top)
face_circle = Circle((5, 7), 0.8, facecolor='white', edgecolor='#4A90E2', linewidth=3)
ax1.add_patch(face_circle)
ax1.text(5, 7, '☺', fontsize=32, ha='center', va='center', color='#4A90E2')

# Arrow down with label
arrow1 = FancyArrowPatch((5, 6), (5, 5), arrowstyle='->', mutation_scale=25, 
                        linewidth=3, color='#4A90E2', alpha=0.7)
ax1.add_patch(arrow1)
ax1.text(6.2, 5.5, 'observes', fontsize=8, style='italic', color='#4A90E2')

# The World (external reality)
world_box = FancyBboxPatch((1.5, 3.5), 7, 1.3, boxstyle="round,pad=0.15", 
                          facecolor='#E8F4F8', edgecolor='#4A90E2', linewidth=2)
ax1.add_patch(world_box)
ax1.text(5, 4.5, 'The World', fontsize=11, ha='center', weight='bold', color='#4A90E2')
ax1.text(5, 4, 'Markets, Prices, Truth', fontsize=8, ha='center', color='#666666')

# Arrow down
arrow2 = FancyArrowPatch((5, 3.5), (5, 2.5), arrowstyle='->', mutation_scale=25, 
                        linewidth=3, color='#4A90E2', alpha=0.7)
ax1.add_patch(arrow2)
ax1.text(6.2, 3, 'reports', fontsize=8, style='italic', color='#4A90E2')

# The System
system_box = FancyBboxPatch((1.5, 1), 7, 1.3, boxstyle="round,pad=0.15", 
                           facecolor='#F5F5F5', edgecolor='#888888', linewidth=2)
ax1.add_patch(system_box)
ax1.text(5, 2, 'The System', fontsize=11, ha='center', weight='bold', color='#333333')
ax1.text(5, 1.5, 'Contracts, Liquidations', fontsize=8, ha='center', color='#666666')

# Bottom label
ax1.text(5, 0.3, 'Surveillance of Reality', fontsize=9, ha='center', 
        weight='bold', color='#4A90E2', style='italic')

# ============================================
# RIGHT: The Mirror (Reverse Oracle)
# ============================================
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')

# Title
ax2.text(5, 9.2, 'THE MIRROR', fontsize=13, weight='bold', ha='center', color='#E24A4A')
ax2.text(5, 8.6, 'Oracles look inward', fontsize=9, ha='center', style='italic', color='#666666')

# Sad face looking inward (top)
face_circle2 = Circle((5, 7), 0.8, facecolor='white', edgecolor='#E24A4A', linewidth=3)
ax2.add_patch(face_circle2)
ax2.text(5, 7, '☹', fontsize=32, ha='center', va='center', color='#E24A4A')

# Arrow down with label
arrow3 = FancyArrowPatch((5, 6), (5, 5), arrowstyle='->', mutation_scale=25, 
                        linewidth=3, color='#E24A4A', alpha=0.7)
ax2.add_patch(arrow3)
ax2.text(6.2, 5.5, 'watches', fontsize=8, style='italic', color='#E24A4A')

# The Self (internal behavior)
self_box = FancyBboxPatch((1.5, 3.5), 7, 1.3, boxstyle="round,pad=0.15", 
                         facecolor='#FFE6E6', edgecolor='#E24A4A', linewidth=2)
ax2.add_patch(self_box)
ax2.text(5, 4.5, 'The Self', fontsize=11, ha='center', weight='bold', color='#E24A4A')
ax2.text(5, 4, 'Behavior, Attention, Will', fontsize=8, ha='center', color='#666666')

# Arrow down
arrow4 = FancyArrowPatch((5, 3.5), (5, 2.5), arrowstyle='->', mutation_scale=25, 
                        linewidth=3, color='#E24A4A', alpha=0.7)
ax2.add_patch(arrow4)
ax2.text(6.2, 3, 'predicts', fontsize=8, style='italic', color='#E24A4A')

# The Response
response_box = FancyBboxPatch((1.5, 1), 7, 1.3, boxstyle="round,pad=0.15", 
                             facecolor='#F5F5F5', edgecolor='#888888', linewidth=2)
ax2.add_patch(response_box)
ax2.text(5, 2, 'The Response', fontsize=11, ha='center', weight='bold', color='#333333')
ax2.text(5, 1.5, 'Retention, Intervention', fontsize=8, ha='center', color='#666666')

# Bottom label
ax2.text(5, 0.3, 'Surveillance of Self', fontsize=9, ha='center', 
        weight='bold', color='#E24A4A', style='italic')

plt.tight_layout()
plt.savefig('core/oracle/reverse_oracle_workflow.png', dpi=300, facecolor='white', bbox_inches='tight')
print("✅ Saved: core/oracle/reverse_oracle_workflow.png")
plt.close()
