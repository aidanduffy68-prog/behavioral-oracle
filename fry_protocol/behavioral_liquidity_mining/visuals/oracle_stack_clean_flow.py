#!/usr/bin/env python3
"""
Oracle Stack Architecture - Clean Flow Diagram (No Checkmark)
Creates a clean, minimal flow diagram without validation badges
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np

def create_clean_flow_diagram():
    """Clean flow diagram without checkmarks or validation badges"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    colors = {
        'layer1': '#1e3a8a',
        'layer2': '#3b82f6', 
        'layer3': '#60a5fa',
        'accent': '#059669',
    }
    
    # Three circles representing layers
    circles = [
        (6, 7.5, 1.2, colors['layer1'], 'Narcissus\nOracle'),
        (6, 5.0, 1.2, colors['layer2'], 'Echo\nEngine'),
        (6, 2.5, 1.2, colors['layer3'], 'Cross-Chain\nDetector')
    ]
    
    for x, y, radius, color, label in circles:
        circle = Circle((x, y), radius, facecolor=color, edgecolor='white', 
                       linewidth=3, alpha=0.9)
        ax.add_patch(circle)
        ax.text(x, y, label, fontsize=12, fontweight='bold', 
                color='white', ha='center', va='center')
    
    # Flow arrows
    arrow_props = dict(arrowstyle='->', lw=4, color=colors['accent'])
    ax.annotate('', xy=(6, 6.2), xytext=(6, 6.8), arrowprops=arrow_props)
    ax.annotate('', xy=(6, 3.7), xytext=(6, 4.3), arrowprops=arrow_props)
    
    # Side metrics
    ax.text(9, 7.5, 'Individual\nPsychology', fontsize=11, ha='center', 
            color=colors['layer1'], fontweight='bold')
    ax.text(9, 5.0, 'Collective\nPatterns', fontsize=11, ha='center', 
            color=colors['layer2'], fontweight='bold')
    ax.text(9, 2.5, 'Universal\nIntelligence', fontsize=11, ha='center', 
            color=colors['layer3'], fontweight='bold')
    
    # Bottom validation (no checkmark)
    ax.text(6, 0.8, '22 Wallets • 42% Retention', 
            fontsize=12, ha='center', color=colors['accent'], fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('behavioral_liquidity_mining/visuals/oracle_stack_clean_flow.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Clean flow diagram created (no checkmark)!")

if __name__ == "__main__":
    create_clean_flow_diagram()

