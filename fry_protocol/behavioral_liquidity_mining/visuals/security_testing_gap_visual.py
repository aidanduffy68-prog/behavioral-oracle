#!/usr/bin/env python3
"""
The Security Testing Gap Visual
Shows difference between most DeFi projects and FRY Protocol
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

# Set high DPI for publication quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Figure size optimized for Windows tab
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# Background - pure white
ax.set_facecolor('white')

# Left side: Most DeFi Projects
left_box = FancyBboxPatch((1, 0.5), 6, 7.5,
                         boxstyle="round,pad=0.2",
                         edgecolor='#dc3545', facecolor='#fff5f5',
                         linewidth=3, zorder=1)
ax.add_patch(left_box)

ax.text(4, 7.5, 'Most DeFi Projects', ha='center', va='top',
        fontsize=22, fontweight='bold', color='#1a1a1a')

# Checkmarks and steps for left side
left_steps = [
    'Test normal use cases ✓',
    'Deploy to mainnet ✓',
    'Hope no one finds bugs 🤞',
]

for i, step in enumerate(left_steps):
    y = 6.5 - i * 0.8
    color = '#dc3545' if i == 2 else '#28a745'
    
    # Checkmark/emoji circle
    circle = plt.Circle((1.5, y), 0.12, color=color, zorder=2)
    ax.add_patch(circle)
    
    # Text
    ax.text(1.8, y, step, ha='left', va='center',
            fontsize=15, fontweight='bold', color='#1a1a1a')

# Result box for left side
result_left = FancyBboxPatch((2, 2.5), 4, 1,
                            boxstyle="round,pad=0.15",
                            edgecolor='#dc3545', facecolor='#dc3545',
                            linewidth=2, zorder=1)
ax.add_patch(result_left)

ax.text(4, 3.2, 'Result:', ha='center', va='bottom',
        fontsize=14, fontweight='bold', color='white')
ax.text(4, 2.9, '$3.8B lost in 2024', ha='center', va='center',
        fontsize=18, fontweight='bold', color='white')

# Right side: FRY Protocol
right_box = FancyBboxPatch((9, 0.5), 6, 7.5,
                          boxstyle="round,pad=0.2",
                          edgecolor='#28a745', facecolor='#f0f9ff',
                          linewidth=3, zorder=1)
ax.add_patch(right_box)

ax.text(12, 7.5, 'FRY Protocol', ha='center', va='top',
        fontsize=22, fontweight='bold', color='#1a1a1a')

# Checkmarks and steps for right side
right_steps = [
    'Test normal use cases ✓',
    'Test 2,780 attack scenarios ✓',
    'Find vulnerabilities before launch ✓',
    'Fix before real money at risk ✓',
]

for i, step in enumerate(right_steps):
    y = 6.5 - i * 0.7
    color = '#28a745'
    
    # Checkmark circle
    circle = plt.Circle((9.5, y), 0.12, color=color, zorder=2)
    ax.add_patch(circle)
    
    # Text
    ax.text(9.8, y, step, ha='left', va='center',
            fontsize=15, fontweight='bold', color='#1a1a1a')

# Result box for right side
result_right = FancyBboxPatch((10, 2.5), 4, 1,
                             boxstyle="round,pad=0.15",
                             edgecolor='#28a745', facecolor='#28a745',
                             linewidth=2, zorder=1)
ax.add_patch(result_right)

ax.text(12, 3.2, 'Result:', ha='center', va='bottom',
        fontsize=14, fontweight='bold', color='white')
ax.text(12, 2.9, '99.1% detection rate', ha='center', va='center',
        fontsize=18, fontweight='bold', color='white')

# Bottom text
bottom_box = FancyBboxPatch((2, 0.2), 12, 0.8,
                           boxstyle="round,pad=0.15",
                           edgecolor='#1a1a1a', facecolor='#e9ecef',
                           linewidth=2, zorder=1)
ax.add_patch(bottom_box)

ax.text(8, 0.7, 'The difference: Testing attacks at scale BEFORE deployment',
        ha='center', va='center', fontsize=16, fontweight='bold',
        color='#1a1a1a')

# Border
border = patches.Rectangle((0.2, 0.2), 15.6, 8.6, 
                          linewidth=2, edgecolor='#e0e0e0', 
                          facecolor='none', zorder=0)
ax.add_patch(border)

plt.tight_layout()
plt.savefig('security_testing_gap.png', bbox_inches='tight', 
            facecolor='white', edgecolor='none', pad_inches=0.2)
plt.savefig('security_testing_gap.pdf', bbox_inches='tight', 
            facecolor='white', edgecolor='none', pad_inches=0.2)
print("✅ Security testing gap visual generated!")
print("📄 Files: security_testing_gap.png, security_testing_gap.pdf")

