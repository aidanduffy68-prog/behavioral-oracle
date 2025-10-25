#!/usr/bin/env python3
"""
Anomaly Detection Module
Layer 2: Anomaly detection during data processing
"""

from datetime import datetime, timedelta
from typing import List, Dict
import statistics

class AnomalyDetector:
    """
    Anomaly detection system for behavioral data
    Flags suspicious patterns for human review
    """
    
    def __init__(self):
        self.spike_threshold_multiplier = 10  # 10x average
        self.pattern_repetition_threshold = 0.8  # 80% identical patterns
        self.cross_chain_correlation_threshold = 0.3  # Minimum correlation
        self.timing_pattern_threshold = 0.9  # Suspicious timing threshold
    
    def detect_anomalies(self, recent_events: List[Dict]) -> List[Dict]:
        """
        Detect anomalies in recent events
        Returns list of detected anomalies
        """
        
        if not recent_events:
            return []
        
        anomalies = []
        
        # Spike detection
        spike_anomalies = self._detect_spikes(recent_events)
        anomalies.extend(spike_anomalies)
        
        # Pattern repetition detection
        repetition_anomalies = self._detect_pattern_repetition(recent_events)
        anomalies.extend(repetition_anomalies)
        
        # Cross-chain correlation check
        correlation_anomalies = self._detect_cross_chain_correlation(recent_events)
        anomalies.extend(correlation_anomalies)
        
        # Timing pattern detection
        timing_anomalies = self._detect_timing_patterns(recent_events)
        anomalies.extend(timing_anomalies)
        
        # Impossible behavior sequences
        sequence_anomalies = self._detect_impossible_sequences(recent_events)
        anomalies.extend(sequence_anomalies)
        
        return anomalies
    
    def _detect_spikes(self, events: List[Dict]) -> List[Dict]:
        """Detect event spikes"""
        anomalies = []
        
        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)
        twenty_four_hours_ago = current_time - timedelta(hours=24)
        
        # Count events in last hour
        recent_events_count = len([e for e in events if e.get('timestamp', current_time) > one_hour_ago])
        
        # Count events in last 24 hours
        daily_events = [e for e in events if e.get('timestamp', current_time) > twenty_four_hours_ago]
        average_hourly_events = len(daily_events) / 24
        
        if average_hourly_events > 0:
            spike_ratio = recent_events_count / average_hourly_events
            
            if spike_ratio > self.spike_threshold_multiplier:
                anomalies.append({
                    'type': 'spike_detection',
                    'severity': 'high',
                    'description': f'Event spike: {recent_events_count} vs {average_hourly_events:.1f} average',
                    'threshold_exceeded': spike_ratio,
                    'timestamp': current_time.isoformat()
                })
        
        return anomalies
    
    def _detect_pattern_repetition(self, events: List[Dict]) -> List[Dict]:
        """Detect pattern repetition"""
        anomalies = []
        
        patterns = [e.get('behavioral_pattern', 'unknown') for e in events]
        
        if len(patterns) > 0:
            # Find most common pattern
            pattern_counts = {}
            for pattern in patterns:
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            
            most_common_pattern = max(pattern_counts, key=pattern_counts.get)
            repetition_ratio = pattern_counts[most_common_pattern] / len(patterns)
            
            if repetition_ratio > self.pattern_repetition_threshold:
                anomalies.append({
                    'type': 'pattern_repetition',
                    'severity': 'medium',
                    'description': f'High pattern repetition: {repetition_ratio:.1%} ({most_common_pattern})',
                    'threshold_exceeded': repetition_ratio,
                    'timestamp': datetime.now().isoformat()
                })
        
        return anomalies
    
    def _detect_cross_chain_correlation(self, events: List[Dict]) -> List[Dict]:
        """Detect cross-chain correlation issues"""
        anomalies = []
        
        # Group events by chain
        chain_events = {}
        for event in events:
            chain = event.get('chain', 'unknown')
            if chain not in chain_events:
                chain_events[chain] = []
            chain_events[chain].append(event)
        
        # Calculate correlation between chains
        chains = list(chain_events.keys())
        if len(chains) >= 2:
            correlations = []
            
            for i in range(len(chains)):
                for j in range(i + 1, len(chains)):
                    chain1 = chains[i]
                    chain2 = chains[j]
                    
                    correlation = self._calculate_chain_correlation(
                        chain_events[chain1], 
                        chain_events[chain2]
                    )
                    correlations.append(correlation)
            
            if correlations:
                avg_correlation = statistics.mean(correlations)
                
                if avg_correlation < self.cross_chain_correlation_threshold:
                    anomalies.append({
                        'type': 'cross_chain_correlation',
                        'severity': 'high',
                        'description': f'Low cross-chain correlation: {avg_correlation:.2f}',
                        'threshold_exceeded': self.cross_chain_correlation_threshold - avg_correlation,
                        'timestamp': datetime.now().isoformat()
                    })
        
        return anomalies
    
    def _calculate_chain_correlation(self, chain1_events: List[Dict], chain2_events: List[Dict]) -> float:
        """Calculate correlation between two chains"""
        # Simple correlation based on event timing
        if not chain1_events or not chain2_events:
            return 0.0
        
        # Extract timestamps
        timestamps1 = [e.get('timestamp', datetime.now()) for e in chain1_events]
        timestamps2 = [e.get('timestamp', datetime.now()) for e in chain2_events]
        
        # Calculate time-based correlation
        # This is a simplified implementation
        return 0.5  # Mock correlation value
    
    def _detect_timing_patterns(self, events: List[Dict]) -> List[Dict]:
        """Detect suspicious timing patterns"""
        anomalies = []
        
        if len(events) < 3:
            return anomalies
        
        # Extract timestamps
        timestamps = [e.get('timestamp', datetime.now()) for e in events]
        timestamps.sort()
        
        # Calculate intervals between events
        intervals = []
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i-1]).total_seconds()
            intervals.append(interval)
        
        if intervals:
            # Check for suspiciously regular intervals
            if len(intervals) > 1:
                interval_variance = statistics.variance(intervals)
                mean_interval = statistics.mean(intervals)
                
                # Low variance indicates regular timing (potentially automated)
                if mean_interval > 0 and interval_variance / mean_interval < 0.1:
                    anomalies.append({
                        'type': 'timing_patterns',
                        'severity': 'medium',
                        'description': 'Suspiciously regular timing patterns detected',
                        'threshold_exceeded': True,
                        'timestamp': datetime.now().isoformat()
                    })
        
        return anomalies
    
    def _detect_impossible_sequences(self, events: List[Dict]) -> List[Dict]:
        """Detect impossible behavior sequences"""
        anomalies = []
        
        if len(events) < 2:
            return anomalies
        
        # Check for impossible sequences
        for i in range(1, len(events)):
            prev_event = events[i-1]
            curr_event = events[i]
            
            # Example: Check for impossible liquidation recovery
            prev_liquidation = prev_event.get('liquidation_value', 0)
            curr_liquidation = curr_event.get('liquidation_value', 0)
            
            # If current liquidation is significantly larger than previous
            # and happened very quickly, it might be impossible
            if (curr_liquidation > prev_liquidation * 10 and 
                self._time_between_events(prev_event, curr_event) < 60):  # Less than 1 minute
                
                anomalies.append({
                    'type': 'impossible_sequences',
                    'severity': 'high',
                    'description': 'Impossible liquidation sequence detected',
                    'threshold_exceeded': True,
                    'timestamp': datetime.now().isoformat()
                })
        
        return anomalies
    
    def _time_between_events(self, event1: Dict, event2: Dict) -> float:
        """Calculate time between two events in seconds"""
        timestamp1 = event1.get('timestamp', datetime.now())
        timestamp2 = event2.get('timestamp', datetime.now())
        
        return abs((timestamp2 - timestamp1).total_seconds())
