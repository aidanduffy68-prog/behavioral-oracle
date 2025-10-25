const hre = require("hardhat");

async function main() {
  console.log("🍟 Deploying Chainlink-integrated contracts to Arbitrum Sepolia...\n");

  // Get deployer
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString(), "\n");

  // 1. Deploy USD_FRY Token (if not already deployed)
  console.log("1. Deploying USD_FRY Token...");
  const USDFRYToken = await ethers.getContractFactory("USDFRYToken");
  const usdFryToken = await USDFRYToken.deploy();
  await usdFryToken.deployed();
  console.log("✓ USD_FRY Token deployed to:", usdFryToken.address, "\n");

  // 2. Deploy WreckageProcessorWithOracle
  console.log("2. Deploying WreckageProcessorWithOracle...");
  const WreckageProcessor = await ethers.getContractFactory("WreckageProcessorWithOracle");
  const wreckageProcessor = await WreckageProcessor.deploy(usdFryToken.address);
  await wreckageProcessor.deployed();
  console.log("✓ WreckageProcessorWithOracle deployed to:", wreckageProcessor.address, "\n");

  // 3. Deploy FRYPredictionMarket (using USDC on Arbitrum Sepolia)
  console.log("3. Deploying FRYPredictionMarket...");
  const usdcAddress = "0x75faf114eafb1BDbe2F0316DF893fd58CE46AA4d"; // USDC on Arbitrum Sepolia
  const PredictionMarket = await ethers.getContractFactory("FRYPredictionMarket");
  const predictionMarket = await PredictionMarket.deploy(
    usdFryToken.address,
    usdcAddress
  );
  await predictionMarket.deployed();
  console.log("✓ FRYPredictionMarket deployed to:", predictionMarket.address, "\n");

  // 4. Grant minting permissions
  console.log("4. Granting minting permissions...");
  const MINTER_ROLE = await usdFryToken.MINTER_ROLE();
  await usdFryToken.grantRole(MINTER_ROLE, wreckageProcessor.address);
  console.log("✓ Granted MINTER_ROLE to WreckageProcessor");
  await usdFryToken.grantRole(MINTER_ROLE, predictionMarket.address);
  console.log("✓ Granted MINTER_ROLE to PredictionMarket\n");

  // 5. Create sample prediction market
  console.log("5. Creating sample prediction market...");
  const btcPriceFeed = "0x56a43EB56Da12C0dc1D972ACb089c06a5dEF8e69"; // BTC/USD on Arbitrum Sepolia
  const targetPrice = 100000 * 1e8; // $100k with 8 decimals
  const resolutionTime = Math.floor(Date.now() / 1000) + 86400 * 30; // 30 days from now

  const OPERATOR_ROLE = await predictionMarket.OPERATOR_ROLE();
  await predictionMarket.grantRole(OPERATOR_ROLE, deployer.address);
  
  const tx = await predictionMarket.createMarket(
    "Will BTC hit $100k within 30 days?",
    "BTC",
    targetPrice,
    resolutionTime,
    btcPriceFeed
  );
  await tx.wait();
  console.log("✓ Created sample market: 'Will BTC hit $100k within 30 days?'\n");

  // Summary
  console.log("=" .repeat(60));
  console.log("🎉 Deployment Complete!\n");
  console.log("Contract Addresses:");
  console.log("  USD_FRY Token:              ", usdFryToken.address);
  console.log("  WreckageProcessorWithOracle:", wreckageProcessor.address);
  console.log("  FRYPredictionMarket:        ", predictionMarket.address);
  console.log("\nChainlink Price Feeds (Arbitrum Sepolia):");
  console.log("  BTC/USD:", btcPriceFeed);
  console.log("  ETH/USD: 0xd30e2101a97dcbAeBCBC04F14C3f624E67A35165");
  console.log("\nNext Steps:");
  console.log("  1. Verify contracts on Arbiscan");
  console.log("  2. Update demo with contract addresses");
  console.log("  3. Test wreckage processing with Chainlink prices");
  console.log("  4. Create more prediction markets");
  console.log("=" .repeat(60));

  // Save deployment info
  const deploymentInfo = {
    network: "arbitrumSepolia",
    timestamp: new Date().toISOString(),
    deployer: deployer.address,
    contracts: {
      USDFRYToken: usdFryToken.address,
      WreckageProcessorWithOracle: wreckageProcessor.address,
      FRYPredictionMarket: predictionMarket.address
    },
    chainlinkFeeds: {
      BTC_USD: btcPriceFeed,
      ETH_USD: "0xd30e2101a97dcbAeBCBC04F14C3f624E67A35165"
    },
    sampleMarket: {
      question: "Will BTC hit $100k within 30 days?",
      targetPrice: targetPrice.toString(),
      resolutionTime: resolutionTime
    }
  };

  const fs = require('fs');
  fs.writeFileSync(
    'deployment-oracle-contracts.json',
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("\n✓ Deployment info saved to deployment-oracle-contracts.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
