#!/usr/bin/env python3
"""
Oracle Stack Architecture - Minimal Visual Options
Creates cleaner, less text-heavy versions of the three-layer architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np

def create_minimal_oracle_stack():
    """Option 1: Minimal text, focus on visual hierarchy"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    colors = {
        'layer1': '#1e3a8a',  # Deep blue
        'layer2': '#3b82f6',  # Medium blue  
        'layer3': '#60a5fa',  # Light blue
        'accent': '#059669',  # Green accent
    }
    
    # Layer 1: Narcissus Oracle
    layer1_box = FancyBboxPatch(
        (1, 7.5), 8, 2.0,
        boxstyle="round,pad=0.1",
        facecolor=colors['layer1'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(layer1_box)
    
    ax.text(5, 8.8, 'Narcissus Oracle', fontsize=16, fontweight='bold', 
            color='white', ha='center')
    ax.text(5, 8.3, 'Individual Psychology', fontsize=12, color='white', 
            ha='center', alpha=0.9)
    
    # Key metrics only
    ax.text(3, 7.8, 'Risk Tolerance: 0.58', fontsize=11, color='white', ha='left')
    ax.text(7, 7.8, 'Narcissus Score: 0.64', fontsize=11, color='white', ha='left')
    
    # Layer 2: Echo Engine
    layer2_box = FancyBboxPatch(
        (1, 4.5), 8, 2.0,
        boxstyle="round,pad=0.1",
        facecolor=colors['layer2'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(layer2_box)
    
    ax.text(5, 5.8, 'Echo Engine', fontsize=16, fontweight='bold', 
            color='white', ha='center')
    ax.text(5, 5.3, 'Collective Patterns', fontsize=12, color='white', 
            ha='center', alpha=0.9)
    
    # Key metrics only
    ax.text(3, 4.8, 'Coherence: 71-82%', fontsize=11, color='white', ha='left')
    ax.text(7, 4.8, 'Alpha: 1.57×', fontsize=11, color='white', ha='left')
    
    # Layer 3: Cross-Chain Detector
    layer3_box = FancyBboxPatch(
        (1, 1.5), 8, 2.0,
        boxstyle="round,pad=0.1",
        facecolor=colors['layer3'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(layer3_box)
    
    ax.text(5, 2.8, 'Cross-Chain Detector', fontsize=16, fontweight='bold', 
            color='white', ha='center')
    ax.text(5, 2.3, 'Universal Intelligence', fontsize=12, color='white', 
            ha='center', alpha=0.9)
    
    # Key metrics only
    ax.text(3, 1.8, 'Correlation: 0.92', fontsize=11, color='white', ha='left')
    ax.text(7, 1.8, '5 Chains', fontsize=11, color='white', ha='left')
    
    # Data flow arrows
    arrow_props = dict(arrowstyle='->', lw=4, color=colors['accent'])
    ax.annotate('', xy=(5, 6.4), xytext=(5, 6.9), arrowprops=arrow_props)
    ax.annotate('', xy=(5, 3.4), xytext=(5, 3.9), arrowprops=arrow_props)
    
    # Simple validation badge
    validation_circle = Circle((10, 8), 0.8, facecolor=colors['accent'], 
                              edgecolor='white', linewidth=2, alpha=0.9)
    ax.add_patch(validation_circle)
    ax.text(10, 8, '✓', fontsize=20, color='white', ha='center', va='center')
    ax.text(10, 7.2, '22 wallets\n42% retention', fontsize=10, color='black', 
            ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig('behavioral_liquidity_mining/visuals/oracle_stack_minimal.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Minimal Oracle Stack created!")

def create_icon_based_stack():
    """Option 2: Icon-based, very visual"""
    
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
    
    # Layer 1: Mirror/Reflection icon
    layer1_box = FancyBboxPatch(
        (1, 7.5), 8, 2.0,
        boxstyle="round,pad=0.1",
        facecolor=colors['layer1'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(layer1_box)
    
    # Mirror icon (simplified)
    mirror = Rectangle((3.5, 8.2), 3, 0.8, facecolor='white', alpha=0.3)
    ax.add_patch(mirror)
    ax.text(5, 8.6, 'Narcissus', fontsize=16, fontweight='bold', 
            color='white', ha='center')
    ax.text(5, 8.0, 'Self-Reflection', fontsize=12, color='white', ha='center')
    
    # Layer 2: Echo/Ripple icon
    layer2_box = FancyBboxPatch(
        (1, 4.5), 8, 2.0,
        boxstyle="round,pad=0.1",
        facecolor=colors['layer2'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(layer2_box)
    
    # Echo ripples
    for i, radius in enumerate([0.3, 0.6, 0.9]):
        circle = Circle((5, 5.5), radius, fill=False, edgecolor='white', 
                       linewidth=2, alpha=0.7-i*0.2)
        ax.add_patch(circle)
    ax.text(5, 5.5, 'Echo', fontsize=16, fontweight='bold', 
            color='white', ha='center')
    ax.text(5, 4.8, 'Pattern Propagation', fontsize=12, color='white', ha='center')
    
    # Layer 3: Network/Chain icon
    layer3_box = FancyBboxPatch(
        (1, 1.5), 8, 2.0,
        boxstyle="round,pad=0.1",
        facecolor=colors['layer3'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(layer3_box)
    
    # Network nodes
    nodes = [(3.5, 2.5), (5, 2.5), (6.5, 2.5)]
    for x, y in nodes:
        circle = Circle((x, y), 0.2, facecolor='white', alpha=0.8)
        ax.add_patch(circle)
    
    # Connect nodes
    ax.plot([3.5, 5, 6.5], [2.5, 2.5, 2.5], 'w-', linewidth=2, alpha=0.8)
    ax.text(5, 2.0, 'Cross-Chain', fontsize=16, fontweight='bold', 
            color='white', ha='center')
    ax.text(5, 1.6, 'Universal Network', fontsize=12, color='white', ha='center')
    
    # Data flow arrows
    arrow_props = dict(arrowstyle='->', lw=4, color=colors['accent'])
    ax.annotate('', xy=(5, 6.4), xytext=(5, 6.9), arrowprops=arrow_props)
    ax.annotate('', xy=(5, 3.4), xytext=(5, 3.9), arrowprops=arrow_props)
    
    # Simple metrics
    ax.text(10, 8, '22 Wallets', fontsize=14, fontweight='bold', ha='center')
    ax.text(10, 7.5, '42% Retention', fontsize=12, ha='center')
    ax.text(10, 7.0, '✓ Validated', fontsize=12, ha='center', color=colors['accent'])
    
    plt.tight_layout()
    plt.savefig('behavioral_liquidity_mining/visuals/oracle_stack_icons.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Icon-based Oracle Stack created!")

def create_flow_diagram():
    """Option 3: Clean flow diagram"""
    
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
    
    # Bottom validation
    ax.text(6, 0.8, '22 Wallets • 42% Retention • Validated', 
            fontsize=12, ha='center', color=colors['accent'], fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('behavioral_liquidity_mining/visuals/oracle_stack_flow.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Flow diagram Oracle Stack created!")

if __name__ == "__main__":
    print("Creating three visual options...")
    create_minimal_oracle_stack()
    create_icon_based_stack()
    create_flow_diagram()
    print("\n✅ All three options created!")
    print("📁 Files saved:")
    print("   • oracle_stack_minimal.png (Option 1: Minimal text)")
    print("   • oracle_stack_icons.png (Option 2: Icon-based)")
    print("   • oracle_stack_flow.png (Option 3: Clean flow)")

