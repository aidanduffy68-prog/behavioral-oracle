#!/usr/bin/env python3
"""
Cross-Chain Intelligence Security Architecture Visual
Shows the multi-layered security system protecting behavioral data and cross-chain communications
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Polygon
import numpy as np

def create_security_architecture_visual():
    """Create visual showing cross-chain intelligence security architecture"""
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 14)
    ax.set_facecolor('white')
    ax.axis('off')
    
    # Title
    ax.text(9, 13.5, 'Cross-Chain Intelligence Security Architecture', 
            ha='center', va='center', fontsize=22, fontweight='bold', color='#1F2937')
    
    # Security Layers
    create_privacy_security_layer(ax)
    create_communication_security_layer(ax)
    create_prediction_security_layer(ax)
    create_financial_security_layer(ax)
    create_resilience_security_layer(ax)
    create_monitoring_layer(ax)
    
    # Threat Vectors
    create_threat_vectors(ax)
    
    # Security Guarantees
    create_security_guarantees(ax)
    
    plt.tight_layout()
    plt.savefig('behavioral_liquidity_mining/security/security_architecture.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('behavioral_liquidity_mining/security/security_architecture.pdf', 
                bbox_inches='tight', facecolor='white')
    plt.show()

def create_privacy_security_layer(ax):
    """Create Layer 1: Behavioral Data Privacy Security"""
    
    # Main box
    privacy_box = FancyBboxPatch((1, 11), 16, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=2)
    ax.add_patch(privacy_box)
    
    ax.text(9, 12.2, 'Layer 1: Behavioral Data Privacy Security', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1E40AF')
    
    # Sub-components
    components = [
        ("ZK Behavioral Proofs", 2.5, 11.6),
        ("Differential Privacy", 6, 11.6),
        ("Pedersen Commitments", 9.5, 11.6),
        ("Privacy Aggregation", 13, 11.6)
    ]
    
    for comp, x, y in components:
        # Component boxes
        comp_box = Rectangle((x-0.7, y-0.2), 1.4, 0.4, 
                           facecolor='white', edgecolor='#3B82F6', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, color='#1E40AF')

def create_communication_security_layer(ax):
    """Create Layer 2: Cross-Chain Communication Security"""
    
    # Main box
    comm_box = FancyBboxPatch((1, 9), 16, 1.5, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#F0FDF4', edgecolor='#22C55E', linewidth=2)
    ax.add_patch(comm_box)
    
    ax.text(9, 10.2, 'Layer 2: Cross-Chain Communication Security', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#15803D')
    
    # Sub-components
    components = [
        ("Ed25519 Signatures", 2.5, 9.6),
        ("AES-256-GCM Encryption", 6, 9.6),
        ("BLS Aggregation", 9.5, 9.6),
        ("Onion Routing", 13, 9.6)
    ]
    
    for comp, x, y in components:
        # Component boxes
        comp_box = Rectangle((x-0.7, y-0.2), 1.4, 0.4, 
                           facecolor='white', edgecolor='#22C55E', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, color='#15803D')

def create_prediction_security_layer(ax):
    """Create Layer 3: Prediction Integrity Security"""
    
    # Main box
    pred_box = FancyBboxPatch((1, 7), 16, 1.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2)
    ax.add_patch(pred_box)
    
    ax.text(9, 8.2, 'Layer 3: Prediction Integrity Security', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#D97706')
    
    # Sub-components
    components = [
        ("Commit-Reveal Scheme", 2.5, 7.6),
        ("Anti-Front-Running", 6, 7.6),
        ("Prediction Verification", 9.5, 7.6),
        ("Manipulation Detection", 13, 7.6)
    ]
    
    for comp, x, y in components:
        # Component boxes
        comp_box = Rectangle((x-0.7, y-0.2), 1.4, 0.4, 
                           facecolor='white', edgecolor='#F59E0B', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, color='#D97706')

def create_financial_security_layer(ax):
    """Create Layer 4: Financial Security"""
    
    # Main box
    fin_box = FancyBboxPatch((1, 5), 16, 1.5, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#FEE2E2', edgecolor='#EF4444', linewidth=2)
    ax.add_patch(fin_box)
    
    ax.text(9, 6.2, 'Layer 4: Financial Security', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#DC2626')
    
    # Sub-components
    components = [
        ("Rate Limiting", 2.5, 5.6),
        ("Circuit Breakers", 6, 5.6),
        ("Slippage Protection", 9.5, 5.6),
        ("Alpha Protection", 13, 5.6)
    ]
    
    for comp, x, y in components:
        # Component boxes
        comp_box = Rectangle((x-0.7, y-0.2), 1.4, 0.4, 
                           facecolor='white', edgecolor='#EF4444', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, color='#DC2626')

def create_resilience_security_layer(ax):
    """Create Layer 5: System Resilience Security"""
    
    # Main box
    res_box = FancyBboxPatch((1, 3), 16, 1.5, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#F3E8FF', edgecolor='#8B5CF6', linewidth=2)
    ax.add_patch(res_box)
    
    ax.text(9, 4.2, 'Layer 5: System Resilience Security', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#7C3AED')
    
    # Sub-components
    components = [
        ("Byzantine Fault Tolerance", 2.5, 3.6),
        ("Attack Surface Minimization", 6, 3.6),
        ("Defense in Depth", 9.5, 3.6),
        ("Graceful Degradation", 13, 3.6)
    ]
    
    for comp, x, y in components:
        # Component boxes
        comp_box = Rectangle((x-0.7, y-0.2), 1.4, 0.4, 
                           facecolor='white', edgecolor='#8B5CF6', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, color='#7C3AED')

def create_monitoring_layer(ax):
    """Create Layer 6: Monitoring and Incident Response"""
    
    # Main box
    mon_box = FancyBboxPatch((1, 1), 16, 1.5, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2)
    ax.add_patch(mon_box)
    
    ax.text(9, 2.2, 'Layer 6: Monitoring and Incident Response', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#059669')
    
    # Sub-components
    components = [
        ("Real-Time Monitoring", 2.5, 1.6),
        ("Threat Detection", 6, 1.6),
        ("Incident Response", 9.5, 1.6),
        ("Security Audits", 13, 1.6)
    ]
    
    for comp, x, y in components:
        # Component boxes
        comp_box = Rectangle((x-0.7, y-0.2), 1.4, 0.4, 
                           facecolor='white', edgecolor='#10B981', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, color='#059669')

def create_threat_vectors(ax):
    """Create threat vectors visualization"""
    
    # Threat vectors around the perimeter
    threats = [
        ("Data Breach", 0.5, 12, '#EF4444'),
        ("Front-Running", 17.5, 12, '#EF4444'),
        ("Manipulation", 0.5, 8, '#EF4444'),
        ("Byzantine Attack", 17.5, 8, '#EF4444'),
        ("Cross-Chain Attack", 0.5, 4, '#EF4444'),
        ("Alpha Extraction", 17.5, 4, '#EF4444')
    ]
    
    for threat, x, y, color in threats:
        # Threat arrows pointing inward
        if x < 9:  # Left side threats
            ax.annotate('', xy=(2, y), xytext=(x, y),
                       arrowprops=dict(arrowstyle='->', color=color, lw=2))
        else:  # Right side threats
            ax.annotate('', xy=(16, y), xytext=(x, y),
                       arrowprops=dict(arrowstyle='->', color=color, lw=2))
        
        ax.text(x, y+0.3, threat, ha='center', va='center', 
                fontsize=9, fontweight='bold', color=color)

def create_security_guarantees(ax):
    """Create security guarantees section"""
    
    # Security guarantees box
    guarantees_box = Rectangle((0.5, 0.2), 17, 0.6, 
                             facecolor='#F9FAFB', edgecolor='#6B7280', linewidth=1)
    ax.add_patch(guarantees_box)
    
    ax.text(9, 0.7, 'Security Guarantees', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#374151')
    
    # Guarantee types
    guarantees = [
        ("Privacy: ZK Proofs + Differential Privacy", 3, 0.5),
        ("Integrity: Cryptographic Verification", 9, 0.5),
        ("Availability: Byzantine Fault Tolerance", 15, 0.5)
    ]
    
    for guarantee, x, y in guarantees:
        ax.text(x, y, guarantee, ha='center', va='center', 
                fontsize=9, color='#6B7280')

if __name__ == "__main__":
    create_security_architecture_visual()
