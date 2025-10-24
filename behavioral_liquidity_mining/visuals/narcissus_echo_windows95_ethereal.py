#!/usr/bin/env python3
"""
🏛️ Narcissus & Echo: Windows 95 Aesthetic with Ethereal Background
Creates the retro-futuristic visual matching the Windows 95 text editor aesthetic
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, ConnectionPatch
import numpy as np
from datetime import datetime
import os

def create_windows95_narcissus_echo():
    """Create Windows 95 style visual with ethereal background"""
    
    # Set up the figure with larger canvas for background effects
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_facecolor('#E6F3FF')  # Soft blue background
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Create ethereal background elements
    create_ethereal_background(ax)
    
    # Windows 95 title bar
    title_bar = Rectangle((2, 9.5), 12, 1.2, 
                        facecolor='#C0C0C0', edgecolor='black', linewidth=2)
    ax.add_patch(title_bar)
    
    # Title bar text
    ax.text(8, 10.1, 'Text File Editor - README.TXT', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='black')
    
    # Windows 95 control buttons
    # Help button
    help_btn = Rectangle((12.8, 9.7), 0.4, 0.6, 
                       facecolor='#C0C0C0', edgecolor='black', linewidth=1)
    ax.add_patch(help_btn)
    ax.text(13, 10, '?', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Minimize button
    min_btn = Rectangle((13.3, 9.7), 0.4, 0.6, 
                      facecolor='#C0C0C0', edgecolor='black', linewidth=1)
    ax.add_patch(min_btn)
    ax.text(13.5, 10, '_', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Close button
    close_btn = Rectangle((13.8, 9.7), 0.4, 0.6, 
                        facecolor='#C0C0C0', edgecolor='black', linewidth=1)
    ax.add_patch(close_btn)
    ax.text(14, 10, '×', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Menu bar
    menu_bar = Rectangle((2, 9.0), 12, 0.4, 
                       facecolor='#C0C0C0', edgecolor='black', linewidth=1)
    ax.add_patch(menu_bar)
    
    # Menu items
    menu_items = ['File', 'Edit', 'Sizes', 'Window']
    for i, item in enumerate(menu_items):
        ax.text(2.5 + i*2, 9.2, item, ha='center', va='center', 
                fontsize=10, color='black')
    
    # Main content area (white background)
    content_area = Rectangle((2, 1.5), 12, 7.2, 
                           facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(content_area)
    
    # Scrollbar
    scrollbar = Rectangle((13.7, 1.7), 0.2, 6.8, 
                        facecolor='#C0C0C0', edgecolor='black', linewidth=1)
    ax.add_patch(scrollbar)
    
    # Scrollbar handle
    scroll_handle = Rectangle((13.7, 7.5), 0.2, 1.0, 
                            facecolor='#808080', edgecolor='black', linewidth=1)
    ax.add_patch(scroll_handle)
    
    # Create the three-layer architecture inside the window
    create_windows95_architecture(ax)
    
    # Add pixelated titles
    create_pixelated_titles(ax)
    
    # Add GH CO logo
    create_gh_logo(ax)
    
    # Save the visual
    os.makedirs('behavioral_liquidity_mining/visuals', exist_ok=True)
    plt.savefig('behavioral_liquidity_mining/visuals/narcissus_echo_windows95.png', 
                dpi=300, bbox_inches='tight', facecolor='#E6F3FF')
    plt.savefig('behavioral_liquidity_mining/visuals/narcissus_echo_windows95.pdf', 
                bbox_inches='tight', facecolor='#E6F3FF')
    
    print("✅ Windows 95 Narcissus & Echo visual created!")
    print("📁 Saved to: behavioral_liquidity_mining/visuals/narcissus_echo_windows95.png")
    
    return fig

def create_ethereal_background(ax):
    """Create the ethereal background with light trails and bubbles"""
    
    # Soft landscape background (blurred effect)
    landscape = Rectangle((0, 0), 16, 12, 
                         facecolor='#F0F8FF', edgecolor='none', alpha=0.3)
    ax.add_patch(landscape)
    
    # Glowing light trails (green energy)
    trail_x = np.linspace(0, 8, 100)
    trail_y = 2 + 3 * np.sin(trail_x * 0.5) * np.exp(-trail_x * 0.1)
    
    ax.plot(trail_x, trail_y, color='#00FF88', linewidth=8, alpha=0.6)
    ax.plot(trail_x, trail_y, color='#88FFAA', linewidth=4, alpha=0.8)
    ax.plot(trail_x, trail_y, color='#CCFFDD', linewidth=2, alpha=1.0)
    
    # Additional light trails
    trail2_x = np.linspace(1, 6, 80)
    trail2_y = 1 + 2 * np.cos(trail2_x * 0.3) * np.exp(-trail2_x * 0.15)
    
    ax.plot(trail2_x, trail2_y, color='#00FF88', linewidth=6, alpha=0.4)
    ax.plot(trail2_x, trail2_y, color='#88FFAA', linewidth=3, alpha=0.6)
    
    # Iridescent bubbles
    bubble_positions = [
        (3, 8, 0.8), (5, 6, 0.5), (7, 9, 0.6), (9, 4, 0.4), 
        (11, 7, 0.7), (13, 5, 0.3), (1, 3, 0.5), (15, 8, 0.4)
    ]
    
    for x, y, size in bubble_positions:
        # Outer glow
        bubble_outer = Circle((x, y), size, facecolor='#FFFFFF', alpha=0.3)
        ax.add_patch(bubble_outer)
        
        # Main bubble with rainbow effect
        bubble_main = Circle((x, y), size*0.7, facecolor='#FFFFFF', alpha=0.7)
        ax.add_patch(bubble_main)
        
        # Inner highlight
        bubble_inner = Circle((x-size*0.2, y+size*0.2), size*0.3, 
                            facecolor='#FFFFFF', alpha=0.9)
        ax.add_patch(bubble_inner)

def create_windows95_architecture(ax):
    """Create the three-layer architecture inside the Windows window"""
    
    # Layer 1: Narcissus Oracle (dark blue circle)
    narcissus_circle = Circle((8, 7.5), 0.8, 
                             facecolor='#1E3A8A', edgecolor='white', linewidth=2)
    ax.add_patch(narcissus_circle)
    ax.text(8, 7.5, 'Narcissus\nOracle', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')
    
    # Side label
    ax.text(9.5, 7.5, 'Individual\nPsychology', ha='center', va='center', 
            fontsize=9, color='#1E3A8A', fontweight='bold')
    
    # Layer 2: Echo Engine (medium blue circle)
    echo_circle = Circle((8, 5.0), 0.8, 
                        facecolor='#3B82F6', edgecolor='white', linewidth=2)
    ax.add_patch(echo_circle)
    ax.text(8, 5.0, 'Echo\nEngine', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')
    
    # Side label
    ax.text(9.5, 5.0, 'Collective\nPatterns', ha='center', va='center', 
            fontsize=9, color='#3B82F6', fontweight='bold')
    
    # Layer 3: Cross-Chain Detector (light blue circle)
    crosschain_circle = Circle((8, 2.5), 0.8, 
                              facecolor='#60A5FA', edgecolor='white', linewidth=2)
    ax.add_patch(crosschain_circle)
    ax.text(8, 2.5, 'Cross-Chain\nDetector', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')
    
    # Side label
    ax.text(9.5, 2.5, 'Universal\nIntelligence', ha='center', va='center', 
            fontsize=9, color='#60A5FA', fontweight='bold')
    
    # Flow arrows (green)
    arrow_props = dict(arrowstyle='->', lw=3, color='#059669')
    ax.annotate('', xy=(8, 6.2), xytext=(8, 6.8), arrowprops=arrow_props)
    ax.annotate('', xy=(8, 3.7), xytext=(8, 4.3), arrowprops=arrow_props)
    
    # Bottom metrics
    ax.text(8, 1.8, '22 Wallets • 42% Retention', 
            ha='center', va='center', fontsize=10, color='#059669', fontweight='bold')

def create_pixelated_titles(ax):
    """Create pixelated titles like in the reference image"""
    
    # Top title
    ax.text(8, 11.5, 'the oracle stack', 
            ha='center', va='center', fontsize=16, fontweight='bold', 
            color='white', bbox=dict(boxstyle="round,pad=0.3", 
            facecolor='black', edgecolor='white', linewidth=2))
    
    # Bottom title
    ax.text(8, 0.5, 'three layer architecture', 
            ha='center', va='center', fontsize=16, fontweight='bold', 
            color='white', bbox=dict(boxstyle="round,pad=0.3", 
            facecolor='black', edgecolor='white', linewidth=2))

def create_gh_logo(ax):
    """Create the GH CO logo in bottom left"""
    
    # Logo background
    logo_bg = Rectangle((0.5, 0.5), 1.5, 1.0, 
                       facecolor='#059669', edgecolor='white', linewidth=2)
    ax.add_patch(logo_bg)
    
    # Logo text
    ax.text(1.25, 1.0, 'GH CO.', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')

def main():
    """Create and display the Windows 95 style visual"""
    
    print("🏛️ Creating Windows 95 Narcissus & Echo Visual...")
    print("🎨 Retro-futuristic aesthetic with ethereal background")
    print("=" * 60)
    
    # Create the visual
    fig = create_windows95_narcissus_echo()
    
    print("\n🎉 Windows 95 Visual Complete!")
    print("\n✅ Features Applied:")
    print("  🖥️ Windows 95 text editor window styling")
    print("  🌟 Ethereal background with light trails")
    print("  💫 Iridescent floating bubbles")
    print("  🎯 Clean three-layer architecture")
    print("  📝 Pixelated titles with black backgrounds")
    print("  🏢 GH CO logo in bottom left")
    print("  🎨 Soft blue background color")
    
    return fig

if __name__ == "__main__":
    main()

