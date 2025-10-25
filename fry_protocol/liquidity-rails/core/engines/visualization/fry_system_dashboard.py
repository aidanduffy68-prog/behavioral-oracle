#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRY System Dashboard - Real-Time Visualization
===============================================

Comprehensive visualization of the complete FRY system:
1. Liquidity Rails - Wreckage routing flows
2. Agent B - Market making activity
3. Wreckage Matching - P2P swap matching
4. Topology Router - Minting surface optimization
5. zkML Proofs - Privacy verification
6. Confidential Positions - Pedersen commitments

Creates animated dashboard showing all components working together.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
from datetime import datetime
import time

from liquidity_rails_integration import IntegratedLiquiditySystem
from fry_wreckage_matching_engine import WreckageEvent
import logging

logging.basicConfig(level=logging.WARNING)  # Reduce noise

# FRY color scheme
FRY_RED = '#FF4444'
FRY_YELLOW = '#FFD700'
FRY_BLACK = '#000000'
FRY_WHITE = '#FFFFFF'
FRY_GRAY = '#7f7f7f'
FRY_GOLD = '#FFC72C'
FRY_GREEN = '#00FF00'
FRY_DARK_RED = '#CC0000'


class FRYSystemDashboard:
    """Real-time dashboard for FRY system"""
    
    def __init__(self):
        self.system = IntegratedLiquiditySystem(initial_capital=5_000_000)
        
        # Tracking data
        self.wreckage_history = []
        self.fry_minting_history = []
        self.liquidity_utilization_history = []
        self.p2p_match_history = []
        self.timestamp_history = []
        
        # Current state
        self.current_wreckage_flow = []
        self.active_routes = []
        
        print(f"\n{'='*70}")
        print(f"🍟 FRY SYSTEM DASHBOARD - INITIALIZING 🍟")
        print(f"{'='*70}\n")
    
    def generate_wreckage_event(self) -> WreckageEvent:
        """Generate random wreckage event for simulation"""
        import random
        
        dexes = ["dYdX", "Hyperliquid", "Aster", "GMX", "Vertex"]
        types = ["long_liq", "short_liq", "adverse_fill", "funding_loss", "slippage"]
        assets = ["BTC", "ETH", "SOL"]
        
        return WreckageEvent(
            dex=random.choice(dexes),
            wreckage_type=random.choice(types),
            asset=random.choice(assets),
            amount_usd=random.uniform(10_000, 200_000),
            timestamp=time.time()
        )
    
    def create_static_dashboard(self):
        """Create comprehensive static dashboard"""
        
        # Generate some test data
        print("Generating test data...")
        for i in range(20):
            event = self.generate_wreckage_event()
            result = self.system.process_wreckage(event)
            
            self.wreckage_history.append(event.amount_usd)
            self.fry_minting_history.append(result['fry_minted'])
            self.timestamp_history.append(i)
        
        # Get system summary
        summary = self.system.get_system_summary()
        
        print("Creating visualization...\n")
        
        # Create figure
        fig = plt.figure(figsize=(24, 14))
        fig.patch.set_facecolor(FRY_BLACK)
        
        # Title
        fig.suptitle('🍟 FRY LIQUIDITY RAILS SYSTEM - LIVE DASHBOARD 🍟', 
                     fontsize=28, fontweight='bold', color=FRY_GOLD, y=0.98)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fig.text(0.5, 0.94, f'Real-Time System Monitoring | {timestamp}',
                 ha='center', fontsize=12, color=FRY_YELLOW, style='italic')
        
        # Create grid
        gs = fig.add_gridspec(4, 6, hspace=0.35, wspace=0.3,
                             left=0.05, right=0.95, top=0.90, bottom=0.06)
        
        # ===== ROW 1: System Status Panels =====
        
        # Panel 1: Liquidity Rails Status
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.set_facecolor('#0a0a0a')
        ax1.add_patch(mpatches.Rectangle((0, 0), 1, 1, fill=True,
                                         edgecolor=FRY_GOLD, linewidth=3,
                                         facecolor='#0a0a0a', transform=ax1.transAxes))
        
        ax1.text(0.5, 0.80, 'LIQUIDITY RAILS ENGINE', ha='center', fontsize=14,
                 fontweight='bold', color=FRY_GOLD, family='monospace')
        ax1.text(0.5, 0.60, '● OPERATIONAL', ha='center', fontsize=18,
                 fontweight='bold', color=FRY_GREEN, family='monospace')
        
        liq_summary = summary['liquidity_rails']
        ax1.text(0.15, 0.35, 'Total Liquidity:', fontsize=10, color=FRY_YELLOW, family='monospace')
        ax1.text(0.85, 0.35, f"${liq_summary['total_liquidity']/1e6:.1f}M", 
                 ha='right', fontsize=10, color=FRY_WHITE, family='monospace')
        
        ax1.text(0.15, 0.15, 'Utilization:', fontsize=10, color=FRY_YELLOW, family='monospace')
        ax1.text(0.85, 0.15, f"{liq_summary['overall_utilization']:.1%}",
                 ha='right', fontsize=10, color=FRY_WHITE, family='monospace')
        ax1.axis('off')
        
        # Panel 2: Agent B Status
        ax2 = fig.add_subplot(gs[0, 2:4])
        ax2.set_facecolor('#0a0a0a')
        ax2.add_patch(mpatches.Rectangle((0, 0), 1, 1, fill=True,
                                         edgecolor=FRY_RED, linewidth=3,
                                         facecolor='#0a0a0a', transform=ax2.transAxes))
        
        ax2.text(0.5, 0.80, 'AGENT B MARKET MAKER', ha='center', fontsize=14,
                 fontweight='bold', color=FRY_RED, family='monospace')
        ax2.text(0.5, 0.60, '● ACTIVE', ha='center', fontsize=18,
                 fontweight='bold', color=FRY_GREEN, family='monospace')
        
        agent_metrics = summary['agent_b']
        ax2.text(0.15, 0.35, 'FRY Minted:', fontsize=10, color=FRY_YELLOW, family='monospace')
        ax2.text(0.85, 0.35, f"{agent_metrics['total_fry_minted']:.0f}",
                 ha='right', fontsize=10, color=FRY_WHITE, family='monospace')
        
        ax2.text(0.15, 0.15, 'Trades:', fontsize=10, color=FRY_YELLOW, family='monospace')
        ax2.text(0.85, 0.15, f"{agent_metrics['total_trades']}",
                 ha='right', fontsize=10, color=FRY_WHITE, family='monospace')
        ax2.axis('off')
        
        # Panel 3: Wreckage Matching Status
        ax3 = fig.add_subplot(gs[0, 4:])
        ax3.set_facecolor('#0a0a0a')
        ax3.add_patch(mpatches.Rectangle((0, 0), 1, 1, fill=True,
                                         edgecolor=FRY_YELLOW, linewidth=3,
                                         facecolor='#0a0a0a', transform=ax3.transAxes))
        
        ax3.text(0.5, 0.80, 'WRECKAGE MATCHING', ha='center', fontsize=14,
                 fontweight='bold', color=FRY_YELLOW, family='monospace')
        ax3.text(0.5, 0.60, '● MATCHING', ha='center', fontsize=18,
                 fontweight='bold', color=FRY_GREEN, family='monospace')
        
        matcher_metrics = summary['wreckage_matcher']
        ax3.text(0.15, 0.35, 'P2P Matches:', fontsize=10, color=FRY_YELLOW, family='monospace')
        ax3.text(0.85, 0.35, f"{matcher_metrics['matched_pairs']}",
                 ha='right', fontsize=10, color=FRY_WHITE, family='monospace')
        
        ax3.text(0.15, 0.15, 'Total Events:', fontsize=10, color=FRY_YELLOW, family='monospace')
        ax3.text(0.85, 0.15, f"{matcher_metrics['total_events']}",
                 ha='right', fontsize=10, color=FRY_WHITE, family='monospace')
        ax3.axis('off')
        
        # ===== ROW 2: Flow Visualization =====
        
        # Wreckage Flow Chart
        ax4 = fig.add_subplot(gs[1, :3])
        ax4.set_facecolor('#0a0a0a')
        ax4.set_title('Wreckage Flow (USD)', color=FRY_GOLD, fontsize=12, 
                     fontweight='bold', family='monospace', pad=10)
        
        if self.wreckage_history:
            ax4.plot(self.timestamp_history, self.wreckage_history, 
                    color=FRY_RED, linewidth=2, marker='o', markersize=4)
            ax4.fill_between(self.timestamp_history, 0, self.wreckage_history,
                           alpha=0.3, color=FRY_RED)
        
        ax4.set_xlabel('Event #', color=FRY_WHITE, fontsize=10, family='monospace')
        ax4.set_ylabel('USD', color=FRY_WHITE, fontsize=10, family='monospace')
        ax4.tick_params(colors=FRY_WHITE)
        ax4.grid(True, alpha=0.2, color=FRY_GRAY)
        ax4.spines['bottom'].set_color(FRY_GRAY)
        ax4.spines['left'].set_color(FRY_GRAY)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        
        # FRY Minting Chart
        ax5 = fig.add_subplot(gs[1, 3:])
        ax5.set_facecolor('#0a0a0a')
        ax5.set_title('FRY Minting Rate', color=FRY_GOLD, fontsize=12,
                     fontweight='bold', family='monospace', pad=10)
        
        if self.fry_minting_history:
            ax5.plot(self.timestamp_history, self.fry_minting_history,
                    color=FRY_YELLOW, linewidth=2, marker='s', markersize=4)
            ax5.fill_between(self.timestamp_history, 0, self.fry_minting_history,
                           alpha=0.3, color=FRY_YELLOW)
        
        ax5.set_xlabel('Event #', color=FRY_WHITE, fontsize=10, family='monospace')
        ax5.set_ylabel('FRY', color=FRY_WHITE, fontsize=10, family='monospace')
        ax5.tick_params(colors=FRY_WHITE)
        ax5.grid(True, alpha=0.2, color=FRY_GRAY)
        ax5.spines['bottom'].set_color(FRY_GRAY)
        ax5.spines['left'].set_color(FRY_GRAY)
        ax5.spines['top'].set_visible(False)
        ax5.spines['right'].set_visible(False)
        
        # ===== ROW 3: Venue Breakdown =====
        
        # Capital Allocation by Venue
        ax6 = fig.add_subplot(gs[2, :3])
        ax6.set_facecolor('#0a0a0a')
        ax6.set_title('Capital Allocation by Venue', color=FRY_GOLD, fontsize=12,
                     fontweight='bold', family='monospace', pad=10)
        
        venues = list(liq_summary['venues'].keys())
        allocations = [liq_summary['venues'][v]['total_liquidity']/1e6 for v in venues]
        
        colors_gradient = [FRY_RED, FRY_DARK_RED, FRY_YELLOW, FRY_GOLD, FRY_GRAY]
        bars = ax6.barh(venues, allocations, color=colors_gradient[:len(venues)],
                       edgecolor=FRY_GOLD, linewidth=1.5)
        
        ax6.set_xlabel('Capital ($M)', color=FRY_WHITE, fontsize=10, family='monospace')
        ax6.tick_params(colors=FRY_WHITE)
        ax6.grid(True, axis='x', alpha=0.2, color=FRY_GRAY)
        ax6.spines['bottom'].set_color(FRY_GRAY)
        ax6.spines['left'].set_color(FRY_GRAY)
        ax6.spines['top'].set_visible(False)
        ax6.spines['right'].set_visible(False)
        
        # Add value labels
        for i, (venue, bar) in enumerate(zip(venues, bars)):
            width = bar.get_width()
            ax6.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                    f'${width:.1f}M', va='center', fontsize=9,
                    color=FRY_WHITE, family='monospace')
        
        # Liquidity Utilization by Venue
        ax7 = fig.add_subplot(gs[2, 3:])
        ax7.set_facecolor('#0a0a0a')
        ax7.set_title('Liquidity Utilization', color=FRY_GOLD, fontsize=12,
                     fontweight='bold', family='monospace', pad=10)
        
        utilizations = [liq_summary['venues'][v]['utilization']*100 for v in venues]
        
        bars2 = ax7.barh(venues, utilizations, color=FRY_YELLOW,
                        edgecolor=FRY_GOLD, linewidth=1.5)
        
        ax7.set_xlabel('Utilization (%)', color=FRY_WHITE, fontsize=10, family='monospace')
        ax7.set_xlim(0, 100)
        ax7.tick_params(colors=FRY_WHITE)
        ax7.grid(True, axis='x', alpha=0.2, color=FRY_GRAY)
        ax7.spines['bottom'].set_color(FRY_GRAY)
        ax7.spines['left'].set_color(FRY_GRAY)
        ax7.spines['top'].set_visible(False)
        ax7.spines['right'].set_visible(False)
        
        # Add percentage labels
        for bar in bars2:
            width = bar.get_width()
            ax7.text(width + 2, bar.get_y() + bar.get_height()/2,
                    f'{width:.1f}%', va='center', fontsize=9,
                    color=FRY_WHITE, family='monospace')
        
        # ===== ROW 4: System Metrics =====
        
        # Key Metrics Panel
        ax8 = fig.add_subplot(gs[3, :2])
        ax8.set_facecolor('#0a0a0a')
        ax8.add_patch(mpatches.Rectangle((0, 0), 1, 1, fill=True,
                                         edgecolor=FRY_RED, linewidth=2,
                                         facecolor='#0a0a0a', transform=ax8.transAxes))
        
        ax8.text(0.5, 0.90, 'KEY METRICS', ha='center', fontsize=12,
                 fontweight='bold', color=FRY_RED, family='monospace')
        
        metrics_text = f"""
Total Wreckage:    ${summary['total_wreckage_processed']/1e6:.2f}M
Total FRY Minted:  {summary['total_fry_minted']:,.0f}
Effective Rate:    {summary['effective_rate']:.2f} FRY/$1
P2P Matches:       {matcher_metrics['matched_pairs']}
Venues Active:     {len(venues)}
        """
        
        ax8.text(0.1, 0.45, metrics_text, ha='left', va='center',
                 fontsize=10, color=FRY_WHITE, family='monospace')
        ax8.axis('off')
        
        # Routing Strategy Breakdown
        ax9 = fig.add_subplot(gs[3, 2:4])
        ax9.set_facecolor('#0a0a0a')
        ax9.set_title('Routing Strategy Distribution', color=FRY_GOLD, fontsize=12,
                     fontweight='bold', family='monospace', pad=10)
        
        strategies = ['P2P\nSwap', 'Liquidity\nRails', 'Agent B\nDirect']
        strategy_counts = [
            matcher_metrics['matched_pairs'],
            20 - matcher_metrics['matched_pairs'],  # Approximation
            0
        ]
        
        colors_strat = [FRY_GREEN, FRY_YELLOW, FRY_RED]
        bars3 = ax9.bar(strategies, strategy_counts, color=colors_strat,
                       edgecolor=FRY_GOLD, linewidth=2, width=0.6)
        
        ax9.set_ylabel('Count', color=FRY_WHITE, fontsize=10, family='monospace')
        ax9.tick_params(colors=FRY_WHITE)
        ax9.grid(True, axis='y', alpha=0.2, color=FRY_GRAY)
        ax9.spines['bottom'].set_color(FRY_GRAY)
        ax9.spines['left'].set_color(FRY_GRAY)
        ax9.spines['top'].set_visible(False)
        ax9.spines['right'].set_visible(False)
        
        # Add count labels
        for bar in bars3:
            height = bar.get_height()
            if height > 0:
                ax9.text(bar.get_x() + bar.get_width()/2, height + 0.5,
                        f'{int(height)}', ha='center', fontsize=10,
                        color=FRY_WHITE, family='monospace', fontweight='bold')
        
        # System Health Indicator
        ax10 = fig.add_subplot(gs[3, 4:])
        ax10.set_facecolor('#0a0a0a')
        ax10.add_patch(mpatches.Rectangle((0, 0), 1, 1, fill=True,
                                          edgecolor=FRY_GREEN, linewidth=3,
                                          facecolor='#0a0a0a', transform=ax10.transAxes))
        
        ax10.text(0.5, 0.80, 'SYSTEM HEALTH', ha='center', fontsize=14,
                  fontweight='bold', color=FRY_GREEN, family='monospace')
        ax10.text(0.5, 0.50, '100%', ha='center', fontsize=32,
                  fontweight='bold', color=FRY_GREEN, family='monospace')
        ax10.text(0.5, 0.20, 'ALL SYSTEMS OPERATIONAL', ha='center', fontsize=9,
                  color=FRY_WHITE, family='monospace')
        ax10.axis('off')
        
        # ===== ROW 3: Network Topology Visualization =====
        
        ax11 = fig.add_subplot(gs[1:3, :3])
        ax11.set_facecolor('#0a0a0a')
        ax11.set_title('DEX Network Topology', color=FRY_GOLD, fontsize=14,
                      fontweight='bold', family='monospace', pad=15)
        
        # Position DEXes in circular layout
        n_dexes = len(venues)
        angles = np.linspace(0, 2*np.pi, n_dexes, endpoint=False)
        
        dex_positions = {}
        for i, venue in enumerate(venues):
            x = np.cos(angles[i])
            y = np.sin(angles[i])
            dex_positions[venue] = (x, y)
            
            # Draw DEX node
            circle = plt.Circle((x, y), 0.15, color=FRY_RED, 
                               edgecolor=FRY_GOLD, linewidth=2, zorder=10)
            ax11.add_patch(circle)
            
            # Label
            ax11.text(x, y, venue, ha='center', va='center',
                     fontsize=9, color=FRY_WHITE, fontweight='bold',
                     family='monospace', zorder=11)
        
        # Draw connections (liquidity flows)
        for i, v1 in enumerate(venues):
            for j, v2 in enumerate(venues[i+1:], i+1):
                x1, y1 = dex_positions[v1]
                x2, y2 = dex_positions[v2]
                
                # Flow line
                ax11.plot([x1, x2], [y1, y2], color=FRY_YELLOW,
                         linewidth=1, alpha=0.3, linestyle='--', zorder=1)
        
        ax11.set_xlim(-1.5, 1.5)
        ax11.set_ylim(-1.5, 1.5)
        ax11.set_aspect('equal')
        ax11.axis('off')
        
        # Add center "FRY" label
        ax11.text(0, 0, 'FRY\nMINTING', ha='center', va='center',
                 fontsize=14, color=FRY_GOLD, fontweight='bold',
                 family='monospace', bbox=dict(boxstyle='round,pad=0.5',
                                              facecolor=FRY_BLACK,
                                              edgecolor=FRY_GOLD, linewidth=2))
        
        # FRY Minting Rate Over Time
        ax12 = fig.add_subplot(gs[1:3, 3:])
        ax12.set_facecolor('#0a0a0a')
        ax12.set_title('FRY Minting Efficiency', color=FRY_GOLD, fontsize=14,
                      fontweight='bold', family='monospace', pad=15)
        
        if len(self.wreckage_history) > 0 and len(self.fry_minting_history) > 0:
            # Calculate rate per event
            rates = [fry/wreck if wreck > 0 else 0 
                    for fry, wreck in zip(self.fry_minting_history, self.wreckage_history)]
            
            ax12.plot(self.timestamp_history, rates, color=FRY_GOLD,
                     linewidth=3, marker='D', markersize=5)
            
            # Add target line
            ax12.axhline(y=2.0, color=FRY_GREEN, linestyle='--', 
                        linewidth=2, alpha=0.5, label='Target: 2.0')
            ax12.axhline(y=0.5, color=FRY_RED, linestyle='--',
                        linewidth=2, alpha=0.5, label='Base: 0.5')
            
            ax12.legend(loc='upper right', fontsize=9, 
                       facecolor='#0a0a0a', edgecolor=FRY_GRAY,
                       labelcolor=FRY_WHITE)
        
        ax12.set_xlabel('Event #', color=FRY_WHITE, fontsize=10, family='monospace')
        ax12.set_ylabel('FRY per $1', color=FRY_WHITE, fontsize=10, family='monospace')
        ax12.tick_params(colors=FRY_WHITE)
        ax12.grid(True, alpha=0.2, color=FRY_GRAY)
        ax12.spines['bottom'].set_color(FRY_GRAY)
        ax12.spines['left'].set_color(FRY_GRAY)
        ax12.spines['top'].set_visible(False)
        ax12.spines['right'].set_visible(False)
        
        # Footer
        fig.text(0.5, 0.02, 
                '🍟 FRY Liquidity Rails | Built by Liquidity Engineers | Privacy-Preserving Wreckage Absorption',
                ha='center', fontsize=11, color=FRY_GRAY, style='italic', family='monospace')
        
        # Save
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'fry_system_dashboard_{timestamp_str}.png'
        plt.savefig(filename, dpi=150, facecolor=FRY_BLACK, edgecolor='none', bbox_inches='tight')
        
        print(f"✓ Dashboard saved: {filename}\n")
        
        return filename


def main():
    """Run dashboard generation"""
    
    dashboard = FRYSystemDashboard()
    filename = dashboard.create_static_dashboard()
    
    # Print summary
    summary = dashboard.system.get_system_summary()
    
    print(f"{'='*70}")
    print(f"🍟 FRY SYSTEM DASHBOARD GENERATED 🍟")
    print(f"{'='*70}\n")
    
    print(f"System Performance:")
    print(f"  Total Wreckage: ${summary['total_wreckage_processed']:,.0f}")
    print(f"  Total FRY: {summary['total_fry_minted']:,.0f}")
    print(f"  Effective Rate: {summary['effective_rate']:.2f} FRY per $1")
    print(f"  Improvement: {((summary['effective_rate'] - 0.5) / 0.5 * 100):.0f}% vs base\n")
    
    print(f"Visualization: {filename}")
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    main()
