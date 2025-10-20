"""
Generate public retention metrics for dashboard
Updates retention-dashboard.html with real data from oracle database
"""

import sqlite3
from datetime import datetime, timedelta
import json

def get_retention_metrics():
    """Fetch current retention metrics from oracle database"""
    conn = sqlite3.connect('../../data/retention/fry_retention.db')
    cursor = conn.cursor()
    
    # Get total wallets tracked
    cursor.execute("SELECT COUNT(*) FROM liquidated_traders")
    total_wallets = cursor.fetchone()[0]
    
    # Get wallets that returned (had activity after receiving FRY)
    cursor.execute("""
        SELECT COUNT(*) FROM liquidated_traders 
        WHERE last_activity_date > fry_received_date
    """)
    returned_wallets = cursor.fetchone()[0]
    
    # Calculate retention rate
    retention_rate = (returned_wallets / total_wallets * 100) if total_wallets > 0 else 0
    
    # Get days since launch
    launch_date = datetime(2025, 10, 11)
    days_since_launch = (datetime.now() - launch_date).days
    
    # Get total FRY distributed
    cursor.execute("SELECT SUM(fry_amount) FROM liquidated_traders")
    total_fry = cursor.fetchone()[0] or 0
    
    # Get wallet details for display
    cursor.execute("""
        SELECT 
            wallet_address,
            liquidation_date,
            fry_received_date,
            last_activity_date,
            CASE WHEN last_activity_date > fry_received_date THEN 1 ELSE 0 END as returned
        FROM liquidated_traders
        ORDER BY liquidation_date DESC
    """)
    wallets = cursor.fetchall()
    
    conn.close()
    
    return {
        'total_wallets': total_wallets,
        'returned_wallets': returned_wallets,
        'retention_rate': round(retention_rate, 1),
        'days_since_launch': days_since_launch,
        'total_fry_usd': round(total_fry * 0.85, 2),  # Assuming FRY ~$0.85
        'baseline_rate': 10,  # Industry baseline at 9 days
        'improvement_factor': round(retention_rate / 10, 1) if retention_rate > 0 else 0,
        'wallets': wallets,
        'last_updated': datetime.now().strftime('%B %d, %Y')
    }

def anonymize_address(address):
    """Anonymize wallet address for public display"""
    return f"{address[:6]}...{address[-4:]}"

def update_dashboard_html(metrics):
    """Update retention-dashboard.html with current metrics"""
    
    # Read template
    with open('../../docs/retention-dashboard.html', 'r') as f:
        html = f.read()
    
    # Update metrics
    html = html.replace('Wallets Tracked</div>\n                <div class="metric-value">12</div>', 
                       f'Wallets Tracked</div>\n                <div class="metric-value">{metrics["total_wallets"]}</div>')
    
    html = html.replace('Current Retention Rate</div>\n                <div class="metric-value">42%</div>', 
                       f'Current Retention Rate</div>\n                <div class="metric-value">{metrics["retention_rate"]}%</div>')
    
    html = html.replace('5 of 12 wallets returned', 
                       f'{metrics["returned_wallets"]} of {metrics["total_wallets"]} wallets returned')
    
    html = html.replace('4.2× baseline', 
                       f'{metrics["improvement_factor"]}× baseline')
    
    html = html.replace('Days Tracked</div>\n                <div class="metric-value">9</div>', 
                       f'Days Tracked</div>\n                <div class="metric-value">{metrics["days_since_launch"]}</div>')
    
    html = html.replace('FRY Distributed</div>\n                <div class="metric-value">$2,847</div>', 
                       f'FRY Distributed</div>\n                <div class="metric-value">${metrics["total_fry_usd"]:,.0f}</div>')
    
    html = html.replace('Last Updated:</strong> October 20, 2025 | <strong>Days Since Launch:</strong> 9 days', 
                       f'Last Updated:</strong> {metrics["last_updated"]} | <strong>Days Since Launch:</strong> {metrics["days_since_launch"]} days')
    
    # Write updated HTML
    with open('../../docs/retention-dashboard.html', 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard updated: {metrics['retention_rate']}% retention ({metrics['returned_wallets']}/{metrics['total_wallets']} wallets)")

if __name__ == "__main__":
    metrics = get_retention_metrics()
    update_dashboard_html(metrics)
    
    # Also output JSON for API endpoint
    with open('../../docs/retention-metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"✅ Metrics JSON generated: docs/retention-metrics.json")
