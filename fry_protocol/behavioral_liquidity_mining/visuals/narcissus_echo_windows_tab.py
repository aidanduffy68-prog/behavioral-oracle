#!/usr/bin/env python3
"""
🏛️ Narcissus & Echo: Windows Tab Visual (Simplified)
Clean content area design for Windows tab aesthetic

Focus: Content area only, no overhead titles or outside boxes
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle
import numpy as np
from datetime import datetime
import os

def create_windows_tab_visual():
    """Create simplified visual for Windows tab aesthetic"""
    
    # Set up the figure - just the content area
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_facecolor('white')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Create simplified visual elements
    create_narcissus_pool_simple(ax)
    create_echo_patterns_simple(ax)
    create_cross_chain_simple(ax)
    create_metrics_simple(ax)
    
    # Save the simplified visual
    os.makedirs('behavioral_liquidity_mining/visuals', exist_ok=True)
    plt.savefig('behavioral_liquidity_mining/visuals/narcissus_echo_windows_tab.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('behavioral_liquidity_mining/visuals/narcissus_echo_windows_tab.pdf', 
                bbox_inches='tight', facecolor='white')
    
    print("✅ Windows Tab Visual created!")
    print("📁 Saved to: behavioral_liquidity_mining/visuals/narcissus_echo_windows_tab.png")
    print("📁 Saved to: behavioral_liquidity_mining/visuals/narcissus_echo_windows_tab.pdf")
    
    return fig

def create_narcissus_pool_simple(ax):
    """Create simplified Narcissus pool"""
    
    # Pool (circular)
    pool_center = (4, 8)
    pool_radius = 1.5
    
    # Pool water (deep blue)
    pool = Circle(pool_center, pool_radius, 
                  facecolor='#1E3A8A', edgecolor='#1E40AF', linewidth=2)
    ax.add_patch(pool)
    
    # Narcissus figure
    narcissus_x, narcissus_y = 4, 6.5
    ax.text(narcissus_x, narcissus_y, '👤', fontsize=20, ha='center', va='center')
    
    # Reflection in pool
    ax.text(pool_center[0], pool_center[1], '👤', fontsize=16, ha='center', va='center', 
            alpha=0.7, color='white')
    
    # Trader metrics around the pool
    metrics = [
        "True Risk Tolerance: 0.58",
        "Self-Deception Level: 0.34", 
        "Narcissus Score: 0.64",
        "Oracle Insight: High self-deception detected"
    ]
    
    angles = [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]
    for i, (metric, angle) in enumerate(zip(metrics, angles)):
        x_pos = pool_center[0] + 1.8 * np.cos(angle)
        y_pos = pool_center[1] + 1.8 * np.sin(angle)
        
        ax.text(x_pos, y_pos, metric, ha='center', va='center', 
                fontsize=8, color='#1E3A8A', fontweight='bold')
    
    # Label
    ax.text(4, 5.5, '🏛️ Narcissus Oracle\nSelf-Reflection Pool', 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#1E3A8A')

def create_echo_patterns_simple(ax):
    """Create simplified echo patterns"""
    
    # Echo center
    echo_center = (7, 7)
    
    # Echo waves (concentric circles)
    colors = ['#8B5CF6', '#A855F7', '#C084FC', '#DDD6FE']
    
    for i, color in enumerate(colors):
        wave_radius = 1.2 + i*0.6
        wave = Circle(echo_center, wave_radius, 
                     facecolor='none', edgecolor=color, 
                     linewidth=2, alpha=0.6)
        ax.add_patch(wave)
    
    # Behavioral archetypes
    archetypes = [
        ('🎯', 'Alpha Traders', 'high risk, high return'),
        ('📊', 'Retention Candidates', 'learned lesson, conservative'),
        ('🔄', 'Arbitrageurs', 'cross-platform, low loyalty'),
        ('📱', 'Sentiment Leaders', 'social influence, volatile')
    ]
    
    archetype_angles = [np.pi/6, 5*np.pi/6, 7*np.pi/6, 11*np.pi/6]
    for i, (icon, name, description) in enumerate(archetypes):
        angle = archetype_angles[i]
        x_pos = echo_center[0] + 2.2 * np.cos(angle)
        y_pos = echo_center[1] + 2.2 * np.sin(angle)
        
        ax.text(x_pos, y_pos, f"{icon} {name}\n{description}", 
                ha='center', va='center', fontsize=8, fontweight='bold',
                color='#8B5CF6')
    
    # Echo Engine label
    ax.text(7, 5, '🗣️ Echo Engine\nPattern Propagation\nEcho Coherence: 71-82%', 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#8B5CF6')

def create_cross_chain_simple(ax):
    """Create simplified cross-chain intelligence"""
    
    # Chain representations
    chains = ['ETH', 'SOL', 'ARB', 'MATIC', 'BASE']
    chain_colors = ['#627EEA', '#9945FF', '#2D374B', '#8247E5', '#0052FF']
    
    for i, (chain, color) in enumerate(zip(chains, chain_colors)):
        x_pos = 11 + i*0.8
        y_pos = 9
        
        # Chain circle
        chain_circle = Circle((x_pos, y_pos), 0.25, 
                             facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(chain_circle)
        ax.text(x_pos, y_pos, chain, ha='center', va='center', 
                fontsize=7, fontweight='bold', color='white')
    
    # Cross-chain metrics
    metrics = [
        "5 Blockchain Networks",
        "10 Cross-Chain Correlations", 
        "4 Echo Transmission Paths",
        "High Cross-Chain Correlation (Simulated)"
    ]
    
    for i, metric in enumerate(metrics):
        y_pos = 7.5 - i*0.3
        ax.text(12, y_pos, metric, ha='left', va='center', 
                fontsize=9, color='#F59E0B', fontweight='bold')
    
    # Label
    ax.text(12, 8.5, '🌐 Cross-Chain Intelligence\nUniversal Patterns', 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#F59E0B')

def create_metrics_simple(ax):
    """Create simplified metrics display"""
    
    # Left panel: Real Validation
    real_metrics = [
        "22 wallets tracked",
        "42% vs 0% retention", 
        "4 behavioral patterns detected",
        "71-82% pattern coherence",
        "10 days validated"
    ]
    
    ax.text(2, 3, '✅ Validated Results', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#15803D')
    
    for i, metric in enumerate(real_metrics):
        y_pos = 2.5 - i*0.2
        ax.text(2, y_pos, metric, ha='center', va='center', fontsize=9, color='#15803D')
    
    # Right panel: Simulated Framework
    sim_metrics = [
        "5 blockchain networks",
        "10 cross-chain correlations", 
        "4 echo transmission paths",
        "Awaiting real-world validation",
        "Framework ready for deployment"
    ]
    
    ax.text(14, 3, '🔬 Simulated Testing', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#D97706')
    
    for i, metric in enumerate(sim_metrics):
        y_pos = 2.5 - i*0.2
        ax.text(14, y_pos, metric, ha='center', va='center', fontsize=9, color='#D97706')
    
    # System status
    ax.text(8, 1, 'System Status: Beta (Active Development)', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#6B7280')

def main():
    """Create and display the simplified visual"""
    
    print("🏛️ Creating Windows Tab Visual...")
    print("🎨 Simplified design for Windows tab aesthetic")
    print("=" * 50)
    
    # Create the simplified visual
    fig = create_windows_tab_visual()
    
    print("\n🎉 Windows Tab Visual Complete!")
    print("\n✅ Simplified Features:")
    print("  🏛️ Narcissus Pool with trader metrics")
    print("  🗣️ Echo Engine with behavioral archetypes")
    print("  🌐 Cross-Chain Intelligence visualization")
    print("  ✅ Real vs Simulated validation badges")
    print("  📊 Clean metrics display")
    print("  🎨 Windows tab aesthetic")
    
    print("\n🚀 Ready for:")
    print("  • Windows tab integration")
    print("  • Clean, professional presentation")
    print("  • Focus on content area")
    
    return fig

if __name__ == "__main__":
    main()

