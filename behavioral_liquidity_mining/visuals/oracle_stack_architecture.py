#!/usr/bin/env python3
"""
Oracle Stack Architecture Visual
Creates a layered diagram showing the three-tier oracle architecture
for the Mirror article "How It Works: Three Layers" section
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np

def create_oracle_stack_visual():
    """Create a clean, professional oracle stack architecture diagram"""
    
    # Set up the figure with clean styling - resized for Windows tab
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Color scheme - professional blues and grays
    colors = {
        'layer1': '#1e3a8a',  # Deep blue
        'layer2': '#3b82f6',  # Medium blue  
        'layer3': '#60a5fa',  # Light blue
        'text': '#1f2937',    # Dark gray
        'accent': '#059669',  # Green accent
        'background': '#ffffff'
    }
    
    # Layer 1: Narcissus Oracle (Individual Level)
    layer1_box = FancyBboxPatch(
        (1, 8.5), 9, 3.0,
        boxstyle="round,pad=0.15",
        facecolor=colors['layer1'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(layer1_box)
    
    # Layer 1 content
    ax.text(5.5, 10.7, 'Layer 1: Narcissus Oracle', 
            fontsize=18, fontweight='bold', color='white', ha='center')
    ax.text(5.5, 10.2, 'Individual Trader Psychology', 
            fontsize=14, color='white', ha='center', alpha=0.9)
    
    # Layer 1 metrics
    metrics1 = [
        'True Risk Tolerance: 0.58',
        'Self-Deception Level: 0.34', 
        'Narcissus Score: 0.64',
        'Oracle Insight: High self-deception detected'
    ]
    
    for i, metric in enumerate(metrics1):
        ax.text(2.5, 9.5 - i*0.25, f"• {metric}", 
                fontsize=14, color='white', alpha=0.95, fontweight='normal')
    
    # Layer 2: Echo Engine (Collective Level)
    layer2_box = FancyBboxPatch(
        (1, 5.0), 9, 3.0,
        boxstyle="round,pad=0.15",
        facecolor=colors['layer2'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(layer2_box)
    
    # Layer 2 content
    ax.text(5.5, 7.2, 'Layer 2: Echo Engine', 
            fontsize=18, fontweight='bold', color='white', ha='center')
    ax.text(5.5, 6.7, 'Collective Behavioral Patterns', 
            fontsize=14, color='white', ha='center', alpha=0.9)
    
    # Layer 2 metrics
    metrics2 = [
        'Echo Coherence: 71-82%',
        'Pattern Clusters: 4 detected',
        'Alpha Extraction: 1.57× baseline',
        'Retention Prediction: 42% vs 0% control'
    ]
    
    for i, metric in enumerate(metrics2):
        ax.text(2.5, 6.0 - i*0.25, f"• {metric}", 
                fontsize=14, color='white', alpha=0.95, fontweight='normal')
    
    # Layer 3: Cross-Chain Detector (Universal Level)
    layer3_box = FancyBboxPatch(
        (1, 1.5), 9, 3.0,
        boxstyle="round,pad=0.15",
        facecolor=colors['layer3'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(layer3_box)
    
    # Layer 3 content
    ax.text(5.5, 3.7, 'Layer 3: Cross-Chain Detector', 
            fontsize=18, fontweight='bold', color='white', ha='center')
    ax.text(5.5, 3.2, 'Universal Behavioral Intelligence', 
            fontsize=14, color='white', ha='center', alpha=0.9)
    
    # Layer 3 metrics
    metrics3 = [
        'Cross-Chain Correlation: 0.92 ETH↔ARB',
        'Universal Patterns: 5 chains analyzed',
        'Echo Transmission: 4 paths detected',
        'Status: Beta (Active Development)'
    ]
    
    for i, metric in enumerate(metrics3):
        ax.text(2.5, 2.5 - i*0.25, f"• {metric}", 
                fontsize=14, color='white', alpha=0.95, fontweight='normal')
    
    # Data flow arrows
    arrow_props = dict(arrowstyle='->', lw=4, color=colors['accent'])
    
    # Arrow from Layer 1 to Layer 2
    ax.annotate('', xy=(5.5, 7.9), xytext=(5.5, 8.4),
                arrowprops=arrow_props)
    
    # Arrow from Layer 2 to Layer 3  
    ax.annotate('', xy=(5.5, 4.9), xytext=(5.5, 5.4),
                arrowprops=arrow_props)
    
    # Validation badges
    validated_box = FancyBboxPatch(
        (10.5, 9.5), 2.5, 2.0,
        boxstyle="round,pad=0.1",
        facecolor=colors['accent'],
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(validated_box)
    ax.text(11.75, 10.8, 'Validated', fontsize=13, fontweight='bold', 
            color='white', ha='center')
    ax.text(11.75, 10.2, '22 wallets', fontsize=12, color='white', ha='center')
    ax.text(11.75, 9.7, '42% retention', fontsize=12, color='white', ha='center')
    
    simulated_box = FancyBboxPatch(
        (10.5, 6.5), 2.5, 2.0,
        boxstyle="round,pad=0.1",
        facecolor='#f59e0b',
        edgecolor='white',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(simulated_box)
    ax.text(11.75, 7.8, 'Simulated', fontsize=13, fontweight='bold', 
            color='white', ha='center')
    ax.text(11.75, 7.2, '5 chains', fontsize=12, color='white', ha='center')
    ax.text(11.75, 6.7, 'Cross-chain', fontsize=12, color='white', ha='center')
    
    # Behavioral archetypes legend
    archetypes_box = FancyBboxPatch(
        (10.5, 1.0), 2.5, 4.0,
        boxstyle="round,pad=0.1",
        facecolor='#f3f4f6',
        edgecolor='#d1d5db',
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(archetypes_box)
    
    ax.text(11.75, 4.5, 'Behavioral', fontsize=13, fontweight='bold', 
            color=colors['text'], ha='center')
    ax.text(11.75, 4.0, 'Archetypes', fontsize=13, fontweight='bold', 
            color=colors['text'], ha='center')
    
    archetypes = [
        'Alpha Traders',
        'Retention Candidates', 
        'Arbitrageurs',
        'Sentiment Leaders'
    ]
    
    for i, archetype in enumerate(archetypes):
        ax.text(10.7, 3.2 - i*0.3, archetype, 
                fontsize=12, color=colors['text'], ha='left')
    
    # Save the visual
    plt.tight_layout()
    plt.savefig('behavioral_liquidity_mining/visuals/oracle_stack_architecture.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('behavioral_liquidity_mining/visuals/oracle_stack_architecture.pdf', 
                bbox_inches='tight', facecolor='white')
    
    print("✅ Oracle Stack Architecture visual created!")
    print("📁 Files saved:")
    print("   • behavioral_liquidity_mining/visuals/oracle_stack_architecture.png")
    print("   • behavioral_liquidity_mining/visuals/oracle_stack_architecture.pdf")
    
    plt.show()

if __name__ == "__main__":
    create_oracle_stack_visual()