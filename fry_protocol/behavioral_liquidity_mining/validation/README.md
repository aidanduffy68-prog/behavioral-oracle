# Validation Framework

**Enterprise-Grade Validation System for Behavioral Oracle**

This validation framework implements a five-layer validation system following Chaos Labs best practices for oracle data integrity.

## 🏗️ Architecture

### Layer 1: Input Validation
**Purpose**: Validate data quality before it enters the oracle system
**Implementation**: `input_validator.py`

**Validation Rules**:
- Minimum wallet age: 30 days
- Minimum trading history: 10 trades
- Liquidation value range: $1,000 - $1,000,000
- Wallet address format validation
- Bot detection and filtering
- Cross-chain activity verification

### Layer 2: Anomaly Detection
**Purpose**: Detect suspicious patterns during data processing
**Implementation**: `anomaly_detector.py`

**Detection Types**:
- **Spike Detection**: Events exceeding 10x average rate
- **Pattern Repetition**: >80% identical behavioral patterns
- **Cross-Chain Correlation**: Low correlation between chains
- **Timing Patterns**: Suspiciously regular event timing
- **Impossible Sequences**: Logically impossible behavior sequences

### Layer 3: Multi-Party Validation
**Purpose**: Consensus validation using multiple data sources
**Implementation**: `multi_party_validator.py`

**Data Sources**:
- **Primary**: Hyperliquid API
- **Validation**: dYdX subgraph
- **Price Verification**: Chainlink oracles
- **Independent Check**: On-chain monitoring

**Consensus Rules**:
- Minimum 2 data sources required
- Maximum 5% deviation between sources
- Pause oracle if sources disagree (Chaos Labs approach)

### Layer 4: Credibility Scoring
**Purpose**: Weight data by source credibility and wallet reputation
**Implementation**: `credibility_scorer.py`

**Scoring Components**:
- **Age & Activity** (25%): Wallet age + trading frequency
- **Trading Volume** (25%): Lifetime volume + consistency
- **Cross-Chain Presence** (20%): Multi-chain activity
- **Social Signals** (15%): ENS, Twitter, GitHub, Discord
- **Verification Status** (15%): KYC, multi-sig, hardware wallet

**Credibility Tiers**:
- **HIGH** (0.8-1.0): Established, verified wallets
- **MEDIUM** (0.5-0.8): Active wallets with verification
- **LOW** (0.2-0.5): New or limited activity wallets
- **UNRELIABLE** (0.0-0.2): Suspicious or bot-like wallets

### Layer 5: Adversarial Red Teaming
**Purpose**: Actively test and break the validation system
**Implementation**: `red_team_attacker.py`, `red_team_framework.py`

**Attack Vectors**:
- **Sybil Wallets**: Test detection of coordinated fake wallets
- **Collusion Attacks**: Test coordinated manipulation attempts
- **Model Poisoning**: Test data corruption resistance
- **Retention Gaming**: Test metric manipulation detection
- **Edge Cases**: Test boundary condition handling
- **Data Manipulation**: Test data integrity validation

## 🚀 Usage

### Basic Validation
```python
from complete_validator import CompleteValidator

validator = CompleteValidator()

# Validate single event
result = await validator.validate_complete_event(event_data, recent_events)

if result.overall_valid:
    print(f"Event validated with {result.confidence_score:.2f} confidence")
else:
    print(f"Validation failed: {result.input_reason}")
```

### Batch Validation
```python
# Validate multiple events
results = await validator.validate_batch_events(events, recent_events)

# Get validation summary
summary = validator.get_validation_summary(results)
print(f"Validation rate: {summary['validation_rate']:.2%}")
```

### Red Team Testing
```python
from red_team_framework import RedTeamFramework

# Run comprehensive red team assessment
framework = RedTeamFramework()
report = await framework.run_full_red_team_assessment()

# Print security assessment
framework.print_assessment_report(report)

# Security score and vulnerability count
print(f"Security Score: {report['assessment_summary']['security_score']:.1f}/100")
print(f"Critical Vulnerabilities: {report['assessment_summary']['vulnerability_count']['critical']}")
```

## 🛡️ Security Features

### Oracle Pause Mechanism
When data sources disagree, the oracle automatically pauses:
- Logs pause event with detailed disagreement information
- Notifies administrators
- Sets oracle status to "PAUSED"
- Prevents corrupted data from entering the system

### Credibility Weighting
Data is weighted by wallet credibility:
- High-credibility wallets have more influence
- Low-credibility wallets are appropriately discounted
- Risk factors are identified and penalized
- Social signals and verification status considered

### Adversarial Red Teaming
Continuous security testing through:
- **Sybil Detection**: Identifies coordinated fake wallets
- **Collusion Prevention**: Detects coordinated manipulation
- **Model Poisoning Resistance**: Prevents data corruption
- **Retention Gaming Detection**: Identifies metric manipulation
- **Edge Case Handling**: Tests boundary conditions
- **Data Integrity Validation**: Ensures data authenticity

### Audit Trail
All validation events are logged with:
- Timestamp
- Validation results
- Source disagreements
- Confidence scores
- Credibility scores
- Anomaly details
- Red team test results

## 📊 Validation Metrics

### Confidence Scoring
- **1.0**: Perfect consensus across all sources
- **0.7-0.9**: High confidence with minor deviations
- **0.5-0.7**: Medium confidence with some disagreement
- **<0.5**: Low confidence, requires review

### Validation Rates
- **Input Validation**: ~95% pass rate (filters bots and invalid data)
- **Anomaly Detection**: ~90% pass rate (flags suspicious patterns)
- **Multi-Party Consensus**: ~85% pass rate (requires source agreement)

## 🔧 Configuration

### Validation Thresholds
```python
# Input validation
min_wallet_age_days = 30
min_total_trades = 10
min_liquidation_value = 1000.0

# Anomaly detection
spike_threshold_multiplier = 10
pattern_repetition_threshold = 0.8
cross_chain_correlation_threshold = 0.3

# Multi-party validation
consensus_threshold = 0.75
max_price_deviation = 0.05
validation_timeout = 30  # seconds
```

## 🎯 Integration Points

### With Behavioral Oracle
```python
# Integrate with main oracle system
from behavioral_oracle import BehavioralOracle
from complete_validator import CompleteValidator

oracle = BehavioralOracle()
validator = CompleteValidator()

# Validate before processing
validation_result = await validator.validate_complete_event(event_data, recent_events)

if validation_result.overall_valid:
    oracle_result = await oracle.process_event(event_data)
else:
    oracle.pause_processing(validation_result)
```

### With Chaos Labs Integration
```python
# Extend Chaos Labs risk management
from chaos_labs_integration import ChaosLabsClient
from complete_validator import CompleteValidator

chaos_client = ChaosLabsClient()
validator = CompleteValidator()

# Add behavioral validation to existing risk checks
def enhanced_risk_assessment(event_data):
    # Existing Chaos Labs risk checks
    market_risk = chaos_client.assess_market_risk(event_data)
    
    # Add behavioral validation
    behavioral_validation = await validator.validate_complete_event(event_data, recent_events)
    
    return {
        'market_risk': market_risk,
        'behavioral_validation': behavioral_validation,
        'overall_risk': calculate_combined_risk(market_risk, behavioral_validation)
    }
```

## 📈 Performance

### Validation Speed
- **Input Validation**: <1ms per event
- **Anomaly Detection**: 5-10ms per event
- **Multi-Party Validation**: 100-500ms per event (network dependent)

### Scalability
- **Batch Processing**: Up to 1000 events per second
- **Async Processing**: Non-blocking validation pipeline
- **Caching**: Source data caching for improved performance

## 🔍 Monitoring

### Validation Dashboard
Track validation metrics in real-time:
- Validation pass rates by layer
- Source disagreement frequency
- Oracle pause events
- Anomaly detection alerts

### Alerting
- **High Priority**: Oracle pause events
- **Medium Priority**: Anomaly detection alerts
- **Low Priority**: Validation rate drops

## 🚨 Error Handling

### Graceful Degradation
- If one data source fails, continue with remaining sources
- If all sources fail, pause oracle until recovery
- Automatic retry with exponential backoff

### Recovery Procedures
- **Source Recovery**: Automatic reconnection to failed sources
- **Oracle Restart**: Manual restart after resolving disagreements
- **Data Reconciliation**: Post-incident data validation and correction

This validation framework ensures your behavioral oracle maintains the highest standards of data integrity and reliability, following enterprise-grade practices from Chaos Labs and other leading oracle providers.
