#!/usr/bin/env python3
"""
Cross-Chain Intelligence Architecture Visual
Shows the multi-layer cross-chain behavioral intelligence system
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import numpy as np

def create_cross_chain_intelligence_visual():
    """Create visual showing cross-chain intelligence architecture"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.set_facecolor('white')
    ax.axis('off')
    
    # Title
    ax.text(8, 11.5, 'Cross-Chain Intelligence Architecture', 
            ha='center', va='center', fontsize=20, fontweight='bold', color='#1F2937')
    
    # Layer 1: Cross-Chain Behavioral Correlation Engine
    create_correlation_engine(ax)
    
    # Layer 2: Universal Behavioral Fingerprinting
    create_universal_fingerprinting(ax)
    
    # Layer 3: Predictive Cross-Chain Intelligence
    create_predictive_intelligence(ax)
    
    # Cross-Chain Data Flow
    create_data_flow(ax)
    
    # Integration Points
    create_integration_points(ax)
    
    plt.tight_layout()
    plt.savefig('behavioral_liquidity_mining/visuals/cross_chain_intelligence.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('behavioral_liquidity_mining/visuals/cross_chain_intelligence.pdf', 
                bbox_inches='tight', facecolor='white')
    plt.show()

def create_correlation_engine(ax):
    """Create Layer 1: Cross-Chain Behavioral Correlation Engine"""
    
    # Main box
    correlation_box = FancyBboxPatch((1, 8.5), 14, 2, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=2)
    ax.add_patch(correlation_box)
    
    ax.text(8, 10.2, 'Layer 1: Cross-Chain Behavioral Correlation Engine', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1E40AF')
    
    # Sub-components
    components = [
        ("Real-Time Pattern Sync", 2.5, 9.5),
        ("Echo Propagation", 6, 9.5),
        ("Correlation Matrix", 9.5, 9.5),
        ("Pattern Migration", 13, 9.5)
    ]
    
    for comp, x, y in components:
        # Component boxes
        comp_box = Rectangle((x-0.8, y-0.3), 1.6, 0.6, 
                           facecolor='white', edgecolor='#3B82F6', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=9, color='#1E40AF')

def create_universal_fingerprinting(ax):
    """Create Layer 2: Universal Behavioral Fingerprinting"""
    
    # Main box
    fingerprint_box = FancyBboxPatch((1, 5.5), 14, 2, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor='#F0FDF4', edgecolor='#22C55E', linewidth=2)
    ax.add_patch(fingerprint_box)
    
    ax.text(8, 7.2, 'Layer 2: Universal Behavioral Fingerprinting', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#15803D')
    
    # Sub-components
    components = [
        ("Behavioral Passports", 2.5, 6.5),
        ("Multi-Chain Clustering", 6, 6.5),
        ("Cross-Chain Mining", 9.5, 6.5),
        ("Universal Scoring", 13, 6.5)
    ]
    
    for comp, x, y in components:
        # Component boxes
        comp_box = Rectangle((x-0.8, y-0.3), 1.6, 0.6, 
                           facecolor='white', edgecolor='#22C55E', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=9, color='#15803D')

def create_predictive_intelligence(ax):
    """Create Layer 3: Predictive Cross-Chain Intelligence"""
    
    # Main box
    predictive_box = FancyBboxPatch((1, 2.5), 14, 2, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2)
    ax.add_patch(predictive_box)
    
    ax.text(8, 4.2, 'Layer 3: Predictive Cross-Chain Intelligence', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#D97706')
    
    # Sub-components
    components = [
        ("Migration Prediction", 2.5, 3.5),
        ("Contagion Forecasting", 6, 3.5),
        ("Weather Maps", 9.5, 3.5),
        ("Early Warning", 13, 3.5)
    ]
    
    for comp, x, y in components:
        # Component boxes
        comp_box = Rectangle((x-0.8, y-0.3), 1.6, 0.6, 
                           facecolor='white', edgecolor='#F59E0B', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=9, color='#D97706')

def create_data_flow(ax):
    """Create cross-chain data flow visualization"""
    
    # Blockchain icons and connections
    chains = [
        ("ETH", 2, 1.5, '#627EEA'),
        ("SOL", 4, 1.5, '#9945FF'),
        ("ARB", 6, 1.5, '#28A0F0'),
        ("MATIC", 8, 1.5, '#8247E5'),
        ("BASE", 10, 1.5, '#0052FF'),
        ("AVAX", 12, 1.5, '#E84142'),
        ("OP", 14, 1.5, '#FF0420')
    ]
    
    for chain, x, y, color in chains:
        # Chain circles
        chain_circle = Circle((x, y), 0.3, facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(chain_circle)
        ax.text(x, y, chain, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
        
        # Connection lines to layers
        ax.plot([x, x], [y+0.3, 2.5], color=color, linewidth=2, alpha=0.6)
    
    # Data flow arrows
    for i in range(len(chains)-1):
        x1, y1 = chains[i][1], chains[i][2]
        x2, y2 = chains[i+1][1], chains[i+1][2]
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='<->', color='#6B7280', lw=1.5, alpha=0.7))

def create_integration_points(ax):
    """Create integration points section"""
    
    # Integration box
    integration_box = Rectangle((0.5, 0.5), 15, 1, 
                               facecolor='#F9FAFB', edgecolor='#6B7280', linewidth=1)
    ax.add_patch(integration_box)
    
    ax.text(8, 1.2, 'Integration Points', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#374151')
    
    # Integration technologies
    integrations = [
        ("Chainlink CCIP", 2, 0.8),
        ("LayerZero", 4.5, 0.8),
        ("Wormhole", 7, 0.8),
        ("Hyperliquid", 9.5, 0.8),
        ("Cross-Chain APIs", 12, 0.8)
    ]
    
    for tech, x, y in integrations:
        ax.text(x, y, tech, ha='center', va='center', fontsize=9, color='#6B7280')

if __name__ == "__main__":
    create_cross_chain_intelligence_visual()
