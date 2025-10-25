#!/bin/bash

# FRY Degen Subnet - Free Testnet Setup
# No real money required!

echo "🍟 FRY DEGEN SUBNET - FREE TESTNET SETUP 🍟"
echo "=========================================="
echo ""

# Check if bittensor is installed
if ! python3 -c "import bittensor" 2>/dev/null; then
    echo "📦 Installing Bittensor..."
    pip3 install bittensor
fi

echo "✅ Bittensor installed"
echo ""

# Create wallets
echo "🔑 Creating wallets..."
echo ""

# Miner wallet
echo "Creating miner wallet..."
python3 << 'EOF'
import bittensor as bt
import os

# Create miner wallet
wallet = bt.wallet(name='miner', hotkey='default')

# Check if already exists
if not os.path.exists(wallet.path):
    wallet.create_if_non_existent(coldkey_use_password=False, hotkey_use_password=False)
    print(f"✅ Miner wallet created: {wallet.hotkey.ss58_address}")
else:
    print(f"✅ Miner wallet exists: {wallet.hotkey.ss58_address}")
EOF

echo ""

# Validator wallet
echo "Creating validator wallet..."
python3 << 'EOF'
import bittensor as bt
import os

# Create validator wallet
wallet = bt.wallet(name='validator', hotkey='default')

# Check if already exists
if not os.path.exists(wallet.path):
    wallet.create_if_non_existent(coldkey_use_password=False, hotkey_use_password=False)
    print(f"✅ Validator wallet created: {wallet.hotkey.ss58_address}")
else:
    print(f"✅ Validator wallet exists: {wallet.hotkey.ss58_address}")
EOF

echo ""
echo "=========================================="
echo "🎉 TESTNET SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "📝 NEXT STEPS:"
echo ""
echo "1. Get free testnet TAO:"
echo "   Visit: https://faucet.bittensor.com"
echo "   Or run: python3 -c 'import bittensor as bt; w=bt.wallet(name=\"miner\"); print(w.hotkey.ss58_address)'"
echo ""
echo "2. Run the miner:"
echo "   python3 bittensor_degen_miner.py --netuid 1 --subtensor.network test --wallet.name miner"
echo ""
echo "3. Run the validator:"
echo "   python3 bittensor_degen_validator.py --netuid 1 --subtensor.network test --wallet.name validator"
echo ""
echo "4. Start FRY Casino backend:"
echo "   python3 /tmp/usd_fry_casino/core/fry_fastapi_backend.py"
echo ""
echo "💡 Everything is FREE on testnet - no real money needed!"
echo ""
