#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Production zkML Integration Guide
==================================

Complete guide for replacing simulated zkML with production frameworks.
Covers EZKL, Risc0, and deployment strategies.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductionZKMLIntegration:
    """
    Integration manager for production zkML frameworks.
    
    Handles:
    - Framework selection (EZKL vs Risc0)
    - Proof generation pipeline
    - Verification (off-chain and on-chain)
    - Fallback strategies
    """
    
    def __init__(self, framework: str = "ezkl"):
        """
        Initialize production zkML integration.
        
        Args:
            framework: "ezkl" or "risc0"
        """
        self.framework = framework
        
        if framework == "ezkl":
            from zkml_production_ezkl import EZKLProofGenerator
            self.generator_class = EZKLProofGenerator
        elif framework == "risc0":
            from zkml_production_risc0 import Risc0ProofGenerator
            self.generator_class = Risc0ProofGenerator
        else:
            raise ValueError(f"Unknown framework: {framework}")
        
        logger.info(f"Production zkML initialized with {framework}")
    
    def get_integration_steps(self) -> dict:
        """Get step-by-step integration guide"""
        
        if self.framework == "ezkl":
            return {
                'installation': [
                    'pip install ezkl',
                    'Or build from source: git clone https://github.com/zkonduit/ezkl',
                ],
                'setup': [
                    '1. Export PyTorch model to ONNX',
                    '2. Compile ONNX to EZKL circuit',
                    '3. Generate proving/verification keys (trusted setup)',
                    '4. Test proof generation locally',
                ],
                'integration': [
                    '1. Replace ZKMLProofGenerator with EZKLProofGenerator',
                    '2. Add ONNX export in client initialization',
                    '3. Update proof generation in evaluate()',
                    '4. Keep verification logic (compatible)',
                ],
                'deployment': [
                    '1. Generate Solidity verifier contract',
                    '2. Deploy to testnet (Sepolia/Goerli)',
                    '3. Test on-chain verification',
                    '4. Deploy to mainnet/L2',
                ],
                'gas_costs': {
                    'proof_generation': 'Off-chain (free)',
                    'verification': '~250k gas (~$10-50 depending on network)',
                    'optimization': 'Batch verify multiple proofs',
                }
            }
        
        elif self.framework == "risc0":
            return {
                'installation': [
                    'cargo install risc0-zkvm',
                    'pip install risc0-py',
                ],
                'setup': [
                    '1. Write Rust guest program for computation',
                    '2. Compile guest program to zkVM binary',
                    '3. Test execution in zkVM',
                    '4. Generate proof',
                ],
                'integration': [
                    '1. Create guest program for RMSE calculation',
                    '2. Serialize Python data to Rust format',
                    '3. Call zkVM prover',
                    '4. Extract journal (public outputs)',
                ],
                'deployment': [
                    '1. Deploy Risc0 verifier contract',
                    '2. Test on-chain verification',
                    '3. Monitor proof sizes and gas costs',
                ],
                'gas_costs': {
                    'proof_generation': 'Off-chain (free)',
                    'verification': '~500k-1M gas (larger than EZKL)',
                    'optimization': 'Use for complex computations only',
                }
            }


def print_migration_guide():
    """Print complete migration guide from simulation to production"""
    
    print("\n" + "="*70)
    print("MIGRATION GUIDE: Simulation → Production zkML")
    print("="*70 + "\n")
    
    print("PHASE 1: Local Testing (Week 1)")
    print("-" * 70)
    print("""
    1. Install EZKL:
       pip install ezkl
    
    2. Test with small model:
       python3 zkml_production_ezkl.py
    
    3. Verify proof generation works:
       - Export model to ONNX ✓
       - Compile circuit ✓
       - Generate proof ✓
       - Verify proof ✓
    
    4. Measure performance:
       - Proof generation time: ~10-60 seconds
       - Proof size: ~200 bytes
       - Verification time: <1 second
    """)
    
    print("\nPHASE 2: Integration (Week 2)")
    print("-" * 70)
    print("""
    1. Update fryboy_federated_client.py:
    
       from zkml_production_ezkl import EZKLProofGenerator
       
       class FryboyClient(fl.client.NumPyClient):
           def __init__(self, ...):
               # Replace simulated generator
               self.zkml_generator = EZKLProofGenerator(client_id)
               
               # One-time setup
               onnx_path = self.zkml_generator.export_model_to_onnx(
                   self.model, input_shape=(1, 25)
               )
               self.zkml_generator.compile_circuit(onnx_path)
               self.zkml_generator.setup_proving_keys()
           
           def evaluate(self, ...):
               # Generate real proof
               witness = self.zkml_generator.generate_witness(
                   self.model, features, predictions, actuals
               )
               proof = self.zkml_generator.generate_proof(threshold=0.05)
               
               # Verify locally
               verified = self.zkml_generator.verify_proof(proof)
    
    2. Update fryboy_federated_server.py:
       - Keep existing verification logic
       - Add EZKL-specific proof parsing
       - Handle larger proof sizes
    
    3. Test with 2 clients:
       - Verify proofs are generated
       - Check aggregation works
       - Monitor performance
    """)
    
    print("\nPHASE 3: On-Chain Deployment (Week 3-4)")
    print("-" * 70)
    print("""
    1. Generate Solidity verifier:
       ezkl create-evm-verifier --vk-path vk.key --sol-code-path verifier.sol
    
    2. Deploy to testnet:
       - Compile with Hardhat/Foundry
       - Deploy to Sepolia
       - Test verification with sample proofs
    
    3. Integrate with OnChainVerifier:
       - Update contract address
       - Add web3 calls
       - Handle gas estimation
    
    4. Monitor costs:
       - Track gas per verification
       - Optimize batch verification
       - Consider L2 deployment (Arbitrum/Optimism)
    """)
    
    print("\nPHASE 4: Production Scaling (Week 5+)")
    print("-" * 70)
    print("""
    1. Optimize proof generation:
       - Parallel proof generation
       - Proof caching
       - Batch proofs
    
    2. Deploy to mainnet:
       - Audit smart contracts
       - Set up monitoring
       - Implement fallback
    
    3. Scale to 5+ venues:
       - Distributed proof generation
       - Load balancing
       - Redundancy
    
    4. Monitor and iterate:
       - Track verification rates
       - Optimize gas costs
       - Update circuits as needed
    """)
    
    print("\n" + "="*70)
    print("COST ANALYSIS")
    print("="*70 + "\n")
    
    print("Per-Proof Costs:")
    print("  Proof Generation: FREE (off-chain)")
    print("  Verification (Ethereum): ~$10-50 per proof")
    print("  Verification (Arbitrum): ~$0.50-2 per proof")
    print("  Verification (Optimism): ~$0.50-2 per proof")
    
    print("\nOptimization Strategies:")
    print("  1. Batch verification: Verify 10 proofs in one tx")
    print("  2. L2 deployment: 10-20x cheaper than mainnet")
    print("  3. Proof aggregation: Combine multiple proofs")
    print("  4. Selective verification: Only verify suspicious clients")
    
    print("\n" + "="*70)
    print("FALLBACK STRATEGY")
    print("="*70 + "\n")
    
    print("""
    If zkML proof generation fails:
    
    1. Try 3 times with exponential backoff
    2. Fall back to simulated proof (with warning)
    3. Mark client as "unverified" (lower weight)
    4. Log failure for investigation
    5. Continue training (don't block)
    
    Code:
        try:
            proof = ezkl_generator.generate_proof(threshold)
        except Exception as e:
            logger.warning(f"zkML failed, using fallback: {e}")
            proof = simulated_generator.generate_proof(...)
            proof['verified'] = False
            proof['fallback'] = True
    """)
    
    print("\n" + "="*70)
    print("PRODUCTION CHECKLIST")
    print("="*70 + "\n")
    
    checklist = [
        "[ ] EZKL installed and tested",
        "[ ] Model exports to ONNX successfully",
        "[ ] Circuit compilation works",
        "[ ] Proof generation < 60 seconds",
        "[ ] Proof size < 500 bytes",
        "[ ] Verification works off-chain",
        "[ ] Solidity verifier generated",
        "[ ] Contract deployed to testnet",
        "[ ] On-chain verification tested",
        "[ ] Gas costs acceptable",
        "[ ] Fallback strategy implemented",
        "[ ] Monitoring/alerting set up",
        "[ ] Documentation updated",
        "[ ] Team trained on zkML ops",
    ]
    
    for item in checklist:
        print(f"  {item}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    print_migration_guide()
