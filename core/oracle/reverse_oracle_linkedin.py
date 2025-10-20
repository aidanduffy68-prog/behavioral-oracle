import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# XP window size (8x5 inches)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), facecolor='white')

# ============================================
# LEFT: Traditional Oracle
# ============================================
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')

# Title
ax1.text(5, 9.2, 'Traditional Oracle', fontsize=13, weight='bold', ha='center', color='#0066CC')
ax1.text(5, 8.5, 'Price Discovery', fontsize=10, ha='center', style='italic', color='#666666')

# Market Data (top)
market_box = FancyBboxPatch((1.5, 6.5), 7, 1.2, boxstyle="round,pad=0.15", 
                           facecolor='#E8F4F8', edgecolor='#0066CC', linewidth=2)
ax1.add_patch(market_box)
ax1.text(5, 7.4, 'Market Data', fontsize=11, ha='center', weight='bold', color='#0066CC')
ax1.text(5, 6.9, 'BTC/USD, ETH/USD, Prices', fontsize=9, ha='center', color='#666666')

# Arrow down
arrow1 = FancyArrowPatch((5, 6.5), (5, 5.5), arrowstyle='->', mutation_scale=25, 
                        linewidth=3, color='#0066CC', alpha=0.7)
ax1.add_patch(arrow1)

# Oracle Layer (middle)
oracle_box = FancyBboxPatch((1.5, 4), 7, 1.2, boxstyle="round,pad=0.15", 
                           facecolor='#FFF4E6', edgecolor='#FF8800', linewidth=2)
ax1.add_patch(oracle_box)
ax1.text(5, 4.9, 'Oracle', fontsize=11, ha='center', weight='bold', color='#FF8800')
ax1.text(5, 4.4, 'Chainlink, Pyth, Stork', fontsize=9, ha='center', color='#666666')

# Arrow down
arrow2 = FancyArrowPatch((5, 4), (5, 3), arrowstyle='->', mutation_scale=25, 
                        linewidth=3, color='#FF8800', alpha=0.7)
ax1.add_patch(arrow2)

# Smart Contracts (bottom)
contract_box = FancyBboxPatch((1.5, 1.5), 7, 1.2, boxstyle="round,pad=0.15", 
                             facecolor='#F5F5F5', edgecolor='#333333', linewidth=2)
ax1.add_patch(contract_box)
ax1.text(5, 2.4, 'Smart Contracts', fontsize=11, ha='center', weight='bold', color='#333333')
ax1.text(5, 1.9, 'Liquidations, Settlements', fontsize=9, ha='center', color='#666666')

# Bottom label
ax1.text(5, 0.5, 'Measures External Reality', fontsize=9, ha='center', 
        weight='bold', color='#0066CC')

# ============================================
# RIGHT: Reverse Oracle
# ============================================
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')

# Title
ax2.text(5, 9.2, 'Reverse Oracle', fontsize=13, weight='bold', ha='center', color='#CC0000')
ax2.text(5, 8.5, 'Behavior Prediction', fontsize=10, ha='center', style='italic', color='#666666')

# User Behavior (top)
behavior_box = FancyBboxPatch((1.5, 6.5), 7, 1.2, boxstyle="round,pad=0.15", 
                             facecolor='#FFE6E6', edgecolor='#CC0000', linewidth=2)
ax2.add_patch(behavior_box)
ax2.text(5, 7.4, 'User Behavior', fontsize=11, ha='center', weight='bold', color='#CC0000')
ax2.text(5, 6.9, 'Activity, Deposits, Churn', fontsize=9, ha='center', color='#666666')

# Arrow down
arrow3 = FancyArrowPatch((5, 6.5), (5, 5.5), arrowstyle='->', mutation_scale=25, 
                        linewidth=3, color='#CC0000', alpha=0.7)
ax2.add_patch(arrow3)

# Reverse Oracle Layer (middle)
reverse_oracle_box = FancyBboxPatch((1.5, 4), 7, 1.2, boxstyle="round,pad=0.15", 
                                   facecolor='#FFF4E6', edgecolor='#FF8800', linewidth=2)
ax2.add_patch(reverse_oracle_box)
ax2.text(5, 4.9, 'Reverse Oracle', fontsize=11, ha='center', weight='bold', color='#FF8800')
ax2.text(5, 4.4, 'FRY Retention Oracle', fontsize=9, ha='center', color='#666666')

# Arrow down
arrow4 = FancyArrowPatch((5, 4), (5, 3), arrowstyle='->', mutation_scale=25, 
                        linewidth=3, color='#FF8800', alpha=0.7)
ax2.add_patch(arrow4)

# Retention System (bottom)
retention_box = FancyBboxPatch((1.5, 1.5), 7, 1.2, boxstyle="round,pad=0.15", 
                              facecolor='#E6F7E6', edgecolor='#00AA00', linewidth=2)
ax2.add_patch(retention_box)
ax2.text(5, 2.4, 'Retention System', fontsize=11, ha='center', weight='bold', color='#00AA00')
ax2.text(5, 1.9, 'FRY Allocation, AMM', fontsize=9, ha='center', color='#666666')

# Bottom label
ax2.text(5, 0.5, 'Predicts Internal Behavior', fontsize=9, ha='center', 
        weight='bold', color='#CC0000')

plt.tight_layout()
plt.savefig('core/oracle/reverse_oracle_linkedin.png', dpi=300, facecolor='white', bbox_inches='tight')
print("✅ Saved: core/oracle/reverse_oracle_linkedin.png")
plt.close()
