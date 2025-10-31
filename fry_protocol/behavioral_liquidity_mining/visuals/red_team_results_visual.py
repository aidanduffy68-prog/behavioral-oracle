#!/usr/bin/env python3
"""
Red Team Testing Results Visual - Final Version for Mirror
Clean, readable graphic showing attack simulation results
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

# Set high DPI for publication quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Figure size optimized for Windows tab (wide format)
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# Background - pure white
ax.set_facecolor('white')

# Title
ax.text(8, 8.5, 'Red Team Testing Results', 
        ha='center', va='top', fontsize=36, fontweight='bold',
        color='#1a1a1a')

# Overall stats box - emphasize the 24 undetected
stats_box = FancyBboxPatch((1, 6.8), 14, 0.9, 
                          boxstyle="round,pad=0.15", 
                          edgecolor='#dc3545', facecolor='#fff5f5',
                          linewidth=2.5, zorder=1)
ax.add_patch(stats_box)

ax.text(5, 7.2, '✅ 2,756 DETECTED', ha='left', va='center',
        fontsize=24, fontweight='bold', color='#28a745')
ax.text(5, 6.85, '⚠️ 24 UNDETECTED • ONE CRITICAL WEAKNESS', ha='left', va='center',
        fontsize=18, fontweight='bold', color='#dc3545')

# Attack results - show all 9 successful + the vulnerability
attacks_successful = [
    ('Fake Account Farming', 'HIGH', 100, '#28a745'),
    ('Coordination Ring', 'HIGH', 100, '#28a745'),
    ('Cross-Chain Gaming', 'HIGH', 100, '#28a745'),
    ('Fake Retention', 'MEDIUM', 100, '#28a745'),
    ('Front-running Claims', 'MEDIUM', 100, '#28a745'),
    ('Min. Threshold Farming', 'MEDIUM', 100, '#28a745'),
    ('Code Exploit', 'CRITICAL', 100, '#28a745'),
    ('Governance Takeover', 'HIGH', 100, '#28a745'),
    ('Spam Attack', 'LOW', 100, '#28a745'),
]

vulnerability = ('Data Manipulation', 'CRITICAL', 76, '#dc3545')

# Successful attacks (2 columns)
for i, (name, severity, rate, color) in enumerate(attacks_successful):
    # Determine column position
    col = i // 5  # 0 or 1
    row = i % 5
    x = 1.2 if col == 0 else 8.8
    y = 5.8 - row * 0.5
    
    # Status indicator
    circle = plt.Circle((x, y), 0.10, color=color, zorder=2)
    ax.add_patch(circle)
    ax.text(x, y, 'OK', ha='center', va='center',
             fontsize=8, color='white', fontweight='bold')
    
    # Attack name (better spacing)
    ax.text(x + 0.4, y + 0.04, name, ha='left', va='center',
            fontsize=12, fontweight='bold', color='#1a1a1a')
    ax.text(x + 0.4, y - 0.08, severity, ha='left', va='center',
            fontsize=10, style='italic', color='#666666')
    
    # Detection rate (better positioning)
    rate_x = x + 4.5 if col == 0 else x + 4.5
    ax.text(rate_x, y, f'{rate}%', ha='left', va='center',
            fontsize=16, fontweight='bold', color=color)

# Vulnerability section - make it stand out (positioned after 9 successful attacks)
vuln_box = FancyBboxPatch((1, 1.5), 14, 0.7, 
                         boxstyle="round,pad=0.15", 
                         edgecolor='#dc3545', facecolor='#fff3cd',
                         linewidth=3, zorder=1)
ax.add_patch(vuln_box)

y = 1.85
# Status indicator
circle = plt.Circle((1.2, y), 0.10, color='#dc3545', zorder=3)
ax.add_patch(circle)
ax.text(1.2, y, '!', ha='center', va='center',
         fontsize=14, color='white', fontweight='bold')

# Attack name
ax.text(1.6, y + 0.03, vulnerability[0], ha='left', va='center',
        fontsize=16, fontweight='bold', color='#1a1a1a')
ax.text(1.6, y - 0.08, vulnerability[1], ha='left', va='center',
        fontsize=13, style='italic', color='#dc3545', fontweight='bold')

# Detection rate
ax.text(7.5, y, f'{vulnerability[2]}%', ha='left', va='center',
        fontsize=18, fontweight='bold', color='#dc3545')

ax.text(8, 1.58, '24 fake accounts slipped through', ha='center', va='center',
        fontsize=12, color='#856404')

# Footer
ax.text(8, 0.5, 'All code and methodology open source on GitHub', 
        ha='center', va='center', fontsize=11, color='#999999')

# Border
border = patches.Rectangle((0.2, 0.2), 15.6, 8.6, 
                          linewidth=2, edgecolor='#e0e0e0', 
                          facecolor='none', zorder=0)
ax.add_patch(border)

plt.tight_layout()
plt.savefig('red_team_results.png', bbox_inches='tight', facecolor='white', edgecolor='none', pad_inches=0.2)
plt.savefig('red_team_results.pdf', bbox_inches='tight', facecolor='white', edgecolor='none', pad_inches=0.2)
print("✅ Red team results visual generated!")
print("📄 Files: red_team_results.png, red_team_results.pdf")
