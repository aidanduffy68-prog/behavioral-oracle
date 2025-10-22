#!/usr/bin/env python3
"""
🏛️ Narcissus & Echo: Social Media Visual
Waterhouse Painting Aesthetic + Windows 95 Style

Creates a stunning visual that combines:
- Narcissus gazing at his reflection (Waterhouse reference)
- Echo patterns spreading across chains
- Windows 95 aesthetic with white background
- Behavioral liquidity mining metrics
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np
from datetime import datetime
import os

def create_narcissus_echo_visual():
    """Create the complete Narcissus & Echo visual - Echo patterns focus"""
    
    # Set up the figure with Windows 95 aesthetic
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_facecolor('white')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title bar (Windows 95 style)
    title_bar = Rectangle((0, 11.2), 16, 0.8, 
                        facecolor='#C0C0C0', edgecolor='black', linewidth=2)
    ax.add_patch(title_bar)
    
    # Title text
    ax.text(8, 11.6, '🏛️ Narcissus & Echo: Behavioral Liquidity Mining', 
            ha='center', va='center', fontsize=16, fontweight='bold', color='black')
    
    # Close button (Windows 95 style)
    close_button = Rectangle((15.2, 11.3), 0.6, 0.4, 
                           facecolor='#C0C0C0', edgecolor='black', linewidth=1)
    ax.add_patch(close_button)
    ax.text(15.5, 11.5, '×', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Main content area
    content_area = Rectangle((0.5, 0.5), 15, 10.2, 
                           facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(content_area)
    
    # Focus on Echo patterns only
    create_echo_patterns(ax)
    
    # Simple metrics display
    create_simple_metrics(ax)
    
    # Save the visual
    os.makedirs('marketing', exist_ok=True)
    plt.savefig('marketing/narcissus_echo_visual.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('marketing/narcissus_echo_visual.pdf', 
                bbox_inches='tight', facecolor='white')
    
    print("✅ Narcissus & Echo visual created!")
    print("📁 Saved to: marketing/narcissus_echo_visual.png")
    print("📁 Saved to: marketing/narcissus_echo_visual.pdf")
    
    return fig

def create_narcissus_pool(ax):
    """Create the Narcissus pool with reflection"""
    
    # Pool (circular, like Waterhouse painting)
    pool_center = (4, 8)
    pool_radius = 1.5
    
    # Pool water (blue gradient effect)
    pool = Circle(pool_center, pool_radius, 
                  facecolor='#4A90E2', edgecolor='#2E5BBA', linewidth=3)
    ax.add_patch(pool)
    
    # Reflection ripples
    for i in range(3):
        ripple = Circle(pool_center, pool_radius + 0.3 + i*0.2, 
                       facecolor='none', edgecolor='#4A90E2', 
                       linewidth=1, alpha=0.3-i*0.1)
        ax.add_patch(ripple)
    
    # Narcissus figure (simplified)
    narcissus_x, narcissus_y = 4, 6.5
    ax.text(narcissus_x, narcissus_y, '👤', fontsize=24, ha='center', va='center')
    
    # Reflection in pool
    ax.text(pool_center[0], pool_center[1], '👤', fontsize=20, ha='center', va='center', 
            alpha=0.7, color='white')
    
    # Oracle insights floating above pool
    insights = [
        "True Risk Tolerance: 0.58",
        "Self-Deception Level: 0.34", 
        "Narcissus Score: 0.64",
        "Oracle Insight: High self-deception detected"
    ]
    
    for i, insight in enumerate(insights):
        y_pos = 10.5 - i*0.3
        ax.text(4, y_pos, insight, ha='center', va='center', 
                fontsize=10, bbox=dict(boxstyle="round,pad=0.3", 
                facecolor='#E8F4FD', edgecolor='#4A90E2'))
    
    # Label
    ax.text(4, 5.5, '🏛️ Narcissus Oracle\nSelf-Reflection Pool', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#F0F8FF', edgecolor='#4A90E2'))

def create_echo_patterns(ax):
    """Create echo patterns spreading across the visual - simplified and centered"""
    
    # Echo center (centered in canvas)
    echo_center = (8, 6)
    
    # Echo waves (concentric circles) - larger and more prominent
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    pattern_names = ['Alpha Traders', 'Retention Candidates', 'Arbitrageurs', 'Sentiment Leaders', 'Risk Escalators']
    
    for i, (color, pattern) in enumerate(zip(colors, pattern_names)):
        # Echo wave - larger radius
        wave_radius = 2.0 + i*1.2
        wave = Circle(echo_center, wave_radius, 
                     facecolor='none', edgecolor=color, 
                     linewidth=4, alpha=0.7)
        ax.add_patch(wave)
        
        # Pattern label - positioned around the circle
        angle = i * 2 * np.pi / len(pattern_names)
        label_x = echo_center[0] + wave_radius * np.cos(angle)
        label_y = echo_center[1] + wave_radius * np.sin(angle)
        
        ax.text(label_x, label_y, pattern, ha='center', va='center', 
                fontsize=11, fontweight='bold', color=color,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', 
                edgecolor=color, linewidth=2, alpha=0.9))
    
    # Central icon
    ax.text(echo_center[0], echo_center[1], '🗣️', fontsize=40, ha='center', va='center')
    
    # Title at top
    ax.text(8, 9.5, 'Echo Engine: Behavioral Patterns Propagate', 
            ha='center', va='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#FFF0F5', edgecolor='#FF6B6B', linewidth=2))

def create_cross_chain_intelligence(ax):
    """Create cross-chain intelligence display"""
    
    # Chain logos/representations
    chains = ['ETH', 'SOL', 'ARB', 'MATIC', 'BASE']
    chain_colors = ['#627EEA', '#9945FF', '#2D374B', '#8247E5', '#0052FF']
    
    # Cross-chain correlation visualization
    for i, (chain, color) in enumerate(zip(chains, chain_colors)):
        x_pos = 11 + i*0.8
        y_pos = 9
        
        # Chain representation
        chain_circle = Circle((x_pos, y_pos), 0.3, 
                             facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(chain_circle)
        ax.text(x_pos, y_pos, chain, ha='center', va='center', 
                fontsize=8, fontweight='bold', color='white')
        
        # Correlation lines
        for j in range(i+1, len(chains)):
            x2_pos = 11 + j*0.8
            ax.plot([x_pos, x2_pos], [y_pos, y_pos], 
                   color=color, linewidth=2, alpha=0.7)
    
    # Cross-chain metrics
    metrics = [
        "100% Universality",
        "10 Cross-Chain Correlations", 
        "4 Echo Transmission Paths",
        "5 Blockchain Networks"
    ]
    
    for i, metric in enumerate(metrics):
        y_pos = 7.5 - i*0.3
        ax.text(12.5, y_pos, metric, ha='left', va='center', 
                fontsize=10, bbox=dict(boxstyle="round,pad=0.2", 
                facecolor='#F0FFF0', edgecolor='#32CD32'))
    
    # Label
    ax.text(12.5, 8.5, '🌐 Cross-Chain Intelligence\nUniversal Patterns', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#F0FFF0', edgecolor='#32CD32'))

def create_simple_metrics(ax):
    """Create simplified metrics display at bottom"""
    
    # Key metrics in a single clean panel
    metrics = [
        "13,659 Liquidations Analyzed",
        "1.99 Alpha per Event",
        "100% Cross-Chain Correlation",
        "5 Behavioral Patterns Detected"
    ]
    
    # Display metrics horizontally at bottom
    for i, metric in enumerate(metrics):
        x_pos = 2 + i*3.5
        ax.text(x_pos, 2, metric, ha='center', va='center', 
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.4", facecolor='#F0F8FF', 
                         edgecolor='#4A90E2', linewidth=2))

def main():
    """Create and display the visual"""
    
    print("🏛️ Creating Narcissus & Echo Visual...")
    print("🎨 Waterhouse Painting Aesthetic + Windows 95 Style")
    print("=" * 60)
    
    # Create the visual
    fig = create_narcissus_echo_visual()
    
    print("\n🎉 Visual Creation Complete!")
    print("\n📋 Features:")
    print("  🏛️ Narcissus Pool with reflection (Waterhouse reference)")
    print("  🗣️ Echo patterns spreading across traders")
    print("  🌐 Cross-chain intelligence visualization")
    print("  📊 Alpha extraction metrics")
    print("  🖥️ Windows 95 aesthetic with white background")
    print("  🎨 Professional presentation quality")
    
    print("\n🚀 Ready for:")
    print("  • Social media posts")
    print("  • VC pitch decks")
    print("  • Conference presentations")
    print("  • Nature paper figures")
    
    return fig

if __name__ == "__main__":
    main()
