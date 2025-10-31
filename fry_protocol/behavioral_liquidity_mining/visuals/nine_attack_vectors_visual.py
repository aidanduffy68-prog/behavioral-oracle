#!/usr/bin/env python3
"""
Nine Attack Vectors Visual
Shows all attack types and their detection rates
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle

# Set high DPI for publication quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Figure size optimized for social media
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Background - pure white
ax.set_facecolor('white')

# Title
ax.text(5, 9.5, 'Nine Attack Vectors Fully Defended', 
        ha='center', va='top', fontsize=22, fontweight='bold',
        color='#1a1a1a')

# Severity legend
ax.text(1, 8.5, 'CRITICAL', ha='left', va='center', fontsize=12, 
        fontweight='bold', color='#dc3545')
ax.text(1, 8.2, 'HIGH', ha='left', va='center', fontsize=12, 
        fontweight='bold', color='#ff6b35')
ax.text(1, 7.9, 'MEDIUM', ha='left', va='center', fontsize=12, 
        fontweight='bold', color='#ffc107')
ax.text(1, 7.6, 'LOW', ha='left', va='center', fontsize=12, 
        fontweight='bold', color='#28a745')

# Define attack vectors with position
attacks = [
    # Row 1 (top)
    ('Fake Account Farming', 'HIGH', 100, '#ff6b35', 2, 7.7),
    ('Coordination Ring', 'HIGH', 100, '#ff6b35', 5, 7.7),
    ('Cross-Chain Gaming', 'HIGH', 100, '#ff6b35', 8, 7.7),
    
    # Row 2 (middle-high)
    ('Code Exploit', 'CRITICAL', 100, '#dc3545', 2, 6.0),
    ('Governance Takeover', 'HIGH', 100, '#ff6b35', 5, 6.0),
    ('Fake Retention', 'MEDIUM', 100, '#ffc107', 8, 6.0),
    
    # Row 3 (middle-low)
    ('Front-running Claims', 'MEDIUM', 100, '#ffc107', 2, 4.3),
    ('Min. Threshold Farming', 'MEDIUM', 100, '#ffc107', 5, 4.3),
    ('Spam Attack', 'LOW', 100, '#28a745', 8, 4.3),
]

# Define severity colors
severity_colors = {
    'CRITICAL': '#dc3545',
    'HIGH': '#ff6b35',
    'MEDIUM': '#ffc107',
    'LOW': '#28a745'
}

for name, severity, rate, color, x, y in attacks:
    # Outer box
    box = FancyBboxPatch((x-1.35, y-0.5), 2.7, 1.0,
                        boxstyle="round,pad=0.1",
                        edgecolor=color, facecolor='white',
                        linewidth=2.5)
    ax.add_patch(box)
    
    # Status circle (top right)
    circle = plt.Circle((x+1.0, y+0.35), 0.08, color='#28a745', zorder=3)
    ax.add_patch(circle)
    ax.text(x+1.0, y+0.35, 'OK', ha='center', va='center',
            fontsize=8, color='white', fontweight='bold')
    
    # Attack name
    ax.text(x, y+0.15, name, ha='center', va='center',
            fontsize=11, fontweight='bold', color='#1a1a1a')
    
    # Severity badge
    severity_color = severity_colors[severity]
    ax.text(x, y-0.1, severity, ha='center', va='center',
            fontsize=10, fontweight='bold', 
            color=severity_color)
    
    # Detection rate
    ax.text(x, y-0.35, f'{rate}%', ha='center', va='center',
            fontsize=14, fontweight='bold', color='#28a745')

# Bottom summary box
summary_box = FancyBboxPatch((1, 0.5), 8, 1.2,
                            boxstyle="round,pad=0.15",
                            edgecolor='#28a745', facecolor='#f0f9ff',
                            linewidth=2.5, zorder=1)
ax.add_patch(summary_box)

ax.text(5, 1.4, 'ALL NINE ATTACK VECTORS: 100% DETECTED', 
        ha='center', va='center', fontsize=16, fontweight='bold', 
        color='#1a1a1a')

ax.text(5, 0.9, 'Five-layer validation framework proven effective',
        ha='center', va='center', fontsize=12, color='#666666')

# Border
border = patches.Rectangle((0.2, 0.2), 9.6, 9.6, 
                          linewidth=2, edgecolor='#e0e0e0', 
                          facecolor='none', zorder=0)
ax.add_patch(border)

plt.tight_layout()
plt.savefig('nine_attack_vectors.png', bbox_inches='tight', 
            facecolor='white', edgecolor='none', pad_inches=0.2)
plt.savefig('nine_attack_vectors.pdf', bbox_inches='tight', 
            facecolor='white', edgecolor='none', pad_inches=0.2)
print("✅ Nine attack vectors visual generated!")
print("📄 Files: nine_attack_vectors.png, nine_attack_vectors.pdf")

