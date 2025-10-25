#!/usr/bin/env python3
"""
Red Team Testing Framework
Comprehensive adversarial testing for the validation system
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List
import sys
import os

# Add validation modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from red_team_attacker import RedTeamAttacker, AttackType, AttackSeverity
from complete_validator import CompleteValidator

class RedTeamFramework:
    """
    Comprehensive red team testing framework
    """
    
    def __init__(self):
        self.attacker = RedTeamAttacker()
        self.validator = CompleteValidator()
        self.test_results = []
        
    async def run_full_red_team_assessment(self) -> Dict:
        """
        Run complete red team assessment
        """
        
        print("🔴 Starting Full Red Team Assessment...")
        print("=" * 60)
        
        # Test all attack vectors
        attack_results = await self.attacker.run_comprehensive_red_team_test()
        
        # Generate comprehensive report
        assessment_report = self._generate_assessment_report(attack_results)
        
        # Save detailed results
        self._save_detailed_results(attack_results)
        
        return assessment_report
    
    def _generate_assessment_report(self, attack_results: List) -> Dict:
        """Generate comprehensive assessment report"""
        
        # Calculate overall security score
        total_attacks = len(attack_results)
        successful_attacks = len([r for r in attack_results if r.success])
        
        if total_attacks == 0:
            security_score = 100
        else:
            security_score = max(0, 100 - (successful_attacks / total_attacks) * 100)
        
        # Categorize vulnerabilities
        vulnerabilities = {
            'critical': [r for r in attack_results if r.severity == AttackSeverity.CRITICAL and r.success],
            'high': [r for r in attack_results if r.severity == AttackSeverity.HIGH and r.success],
            'medium': [r for r in attack_results if r.severity == AttackSeverity.MEDIUM and r.success],
            'low': [r for r in attack_results if r.severity == AttackSeverity.LOW and r.success]
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(vulnerabilities)
        
        report = {
            'assessment_summary': {
                'security_score': security_score,
                'total_attacks_tested': total_attacks,
                'successful_attacks': successful_attacks,
                'vulnerability_count': {
                    'critical': len(vulnerabilities['critical']),
                    'high': len(vulnerabilities['high']),
                    'medium': len(vulnerabilities['medium']),
                    'low': len(vulnerabilities['low'])
                },
                'assessment_date': datetime.now().isoformat()
            },
            'vulnerabilities': vulnerabilities,
            'recommendations': recommendations,
            'next_steps': self._generate_next_steps(vulnerabilities)
        }
        
        return report
    
    def _generate_recommendations(self, vulnerabilities: Dict) -> List[Dict]:
        """Generate prioritized recommendations"""
        
        recommendations = []
        
        # Critical vulnerabilities
        if vulnerabilities['critical']:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'Immediate remediation required',
                'vulnerabilities': [v.attack_type.value for v in vulnerabilities['critical']],
                'mitigations': self._get_mitigations(vulnerabilities['critical'])
            })
        
        # High vulnerabilities
        if vulnerabilities['high']:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Urgent remediation within 48 hours',
                'vulnerabilities': [v.attack_type.value for v in vulnerabilities['high']],
                'mitigations': self._get_mitigations(vulnerabilities['high'])
            })
        
        # Medium vulnerabilities
        if vulnerabilities['medium']:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Remediation within 1 week',
                'vulnerabilities': [v.attack_type.value for v in vulnerabilities['medium']],
                'mitigations': self._get_mitigations(vulnerabilities['medium'])
            })
        
        # Low vulnerabilities
        if vulnerabilities['low']:
            recommendations.append({
                'priority': 'LOW',
                'action': 'Remediation within 1 month',
                'vulnerabilities': [v.attack_type.value for v in vulnerabilities['low']],
                'mitigations': self._get_mitigations(vulnerabilities['low'])
            })
        
        return recommendations
    
    def _get_mitigations(self, vulnerabilities: List) -> List[str]:
        """Extract mitigation suggestions from vulnerabilities"""
        
        mitigations = []
        for vuln in vulnerabilities:
            mitigations.extend(vuln.mitigation_suggestions)
        
        # Remove duplicates and return unique mitigations
        return list(set(mitigations))
    
    def _generate_next_steps(self, vulnerabilities: Dict) -> List[str]:
        """Generate next steps based on vulnerabilities found"""
        
        next_steps = []
        
        if vulnerabilities['critical'] or vulnerabilities['high']:
            next_steps.extend([
                "🚨 IMMEDIATE ACTION REQUIRED",
                "1. Pause production system until critical vulnerabilities are fixed",
                "2. Implement emergency patches for high-severity issues",
                "3. Conduct additional security review",
                "4. Re-run red team testing after fixes"
            ])
        elif vulnerabilities['medium']:
            next_steps.extend([
                "⚠️ URGENT ACTION RECOMMENDED",
                "1. Schedule remediation for medium-severity vulnerabilities",
                "2. Implement additional monitoring",
                "3. Plan security improvements",
                "4. Re-run red team testing after fixes"
            ])
        else:
            next_steps.extend([
                "✅ SECURITY STATUS: GOOD",
                "1. Continue regular red team testing",
                "2. Monitor for new attack vectors",
                "3. Maintain security best practices",
                "4. Schedule next assessment in 30 days"
            ])
        
        return next_steps
    
    def _save_detailed_results(self, attack_results: List):
        """Save detailed test results to file"""
        
        detailed_results = []
        for result in attack_results:
            detailed_results.append({
                'attack_type': result.attack_type.value,
                'severity': result.severity.value,
                'success': result.success,
                'description': result.description,
                'vulnerability_details': result.vulnerability_details,
                'mitigation_suggestions': result.mitigation_suggestions,
                'timestamp': result.timestamp.isoformat()
            })
        
        with open('red_team_detailed_results.json', 'w') as f:
            json.dump(detailed_results, f, indent=2)
    
    def print_assessment_report(self, report: Dict):
        """Print formatted assessment report"""
        
        print("\n" + "=" * 60)
        print("🔴 RED TEAM ASSESSMENT REPORT")
        print("=" * 60)
        
        summary = report['assessment_summary']
        print(f"\n📊 SECURITY SCORE: {summary['security_score']:.1f}/100")
        print(f"Total Attacks Tested: {summary['total_attacks_tested']}")
        print(f"Successful Attacks: {summary['successful_attacks']}")
        
        vuln_count = summary['vulnerability_count']
        print(f"\n🚨 VULNERABILITIES FOUND:")
        print(f"  Critical: {vuln_count['critical']}")
        print(f"  High: {vuln_count['high']}")
        print(f"  Medium: {vuln_count['medium']}")
        print(f"  Low: {vuln_count['low']}")
        
        print(f"\n📋 RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"\n  {rec['priority']} PRIORITY:")
            print(f"  Action: {rec['action']}")
            print(f"  Vulnerabilities: {', '.join(rec['vulnerabilities'])}")
            print(f"  Key Mitigations:")
            for mitigation in rec['mitigations'][:3]:  # Show top 3
                print(f"    - {mitigation}")
        
        print(f"\n🎯 NEXT STEPS:")
        for step in report['next_steps']:
            print(f"  {step}")
        
        print("\n" + "=" * 60)

# Example usage
async def main():
    """Example usage of red team framework"""
    
    framework = RedTeamFramework()
    
    # Run full assessment
    report = await framework.run_full_red_team_assessment()
    
    # Print report
    framework.print_assessment_report(report)
    
    # Save report
    with open('red_team_assessment_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n✅ Red team assessment complete!")
    print("📄 Detailed results saved to red_team_detailed_results.json")
    print("📊 Assessment report saved to red_team_assessment_report.json")

if __name__ == "__main__":
    asyncio.run(main())
