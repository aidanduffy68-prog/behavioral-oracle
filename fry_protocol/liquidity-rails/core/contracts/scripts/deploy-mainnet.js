const hre = require("hardhat");
const { ethers } = require("hardhat");

async function main() {
  console.log("🍟 Deploying FRY Protocol to Arbitrum Mainnet...\n");

  // Get deployer
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", ethers.formatEther(balance), "ETH\n");

  // Check balance
  if (balance < ethers.parseEther("0.01")) {
    console.error("⚠️  Warning: Low balance. Deployment may fail.");
  }

  // Arbitrum Mainnet addresses
  const USDC_MAINNET = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831";
  const BTC_USD_FEED = "0x6ce185860a4963106506C203335A2910413708e9";
  const ETH_USD_FEED = "0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612";

  // 1. Deploy USD_FRY Token
  console.log("1. Deploying USD_FRY Token...");
  const USDFRYToken = await ethers.getContractFactory("USDFRYToken");
  const usdFryToken = await USDFRYToken.deploy();
  await usdFryToken.waitForDeployment();
  const usdFryAddress = await usdFryToken.getAddress();
  console.log("✓ USD_FRY Token deployed to:", usdFryAddress, "\n");

  // 2. Deploy WreckageProcessorWithOracle
  console.log("2. Deploying WreckageProcessorWithOracle...");
  const WreckageProcessor = await ethers.getContractFactory("WreckageProcessorWithOracle");
  const wreckageProcessor = await WreckageProcessor.deploy(usdFryAddress);
  await wreckageProcessor.waitForDeployment();
  const wreckageAddress = await wreckageProcessor.getAddress();
  console.log("✓ WreckageProcessorWithOracle deployed to:", wreckageAddress, "\n");

  // 3. Deploy FRYPredictionMarket
  console.log("3. Deploying FRYPredictionMarket...");
  const PredictionMarket = await ethers.getContractFactory("FRYPredictionMarket");
  const predictionMarket = await PredictionMarket.deploy(
    usdFryAddress,
    USDC_MAINNET
  );
  await predictionMarket.waitForDeployment();
  const predictionAddress = await predictionMarket.getAddress();
  console.log("✓ FRYPredictionMarket deployed to:", predictionAddress, "\n");

  // 4. Grant minting permissions
  console.log("4. Granting minting permissions...");
  const MINTER_ROLE = await usdFryToken.MINTER_ROLE();
  
  const tx1 = await usdFryToken.grantRole(MINTER_ROLE, wreckageAddress);
  await tx1.wait();
  console.log("✓ Granted MINTER_ROLE to WreckageProcessor");
  
  const tx2 = await usdFryToken.grantRole(MINTER_ROLE, predictionAddress);
  await tx2.wait();
  console.log("✓ Granted MINTER_ROLE to PredictionMarket\n");

  // 5. Create initial prediction market
  console.log("5. Creating initial prediction market...");
  const OPERATOR_ROLE = await predictionMarket.OPERATOR_ROLE();
  const tx3 = await predictionMarket.grantRole(OPERATOR_ROLE, deployer.address);
  await tx3.wait();
  
  // "Will BTC recover 50% of Oct 10 losses within 30 days?"
  // Oct 10 low: $102k, 50% recovery = $112k
  const targetPrice = 112000 * 1e8; // $112k with 8 decimals
  const resolutionTime = Math.floor(Date.now() / 1000) + 86400 * 30; // 30 days from now
  
  const tx4 = await predictionMarket.createMarket(
    "Will BTC recover to $112k within 30 days? (50% of Oct 10 losses)",
    "BTC",
    targetPrice,
    resolutionTime,
    BTC_USD_FEED
  );
  await tx4.wait();
  console.log("✓ Created initial market: 'Will BTC recover to $112k within 30 days?'\n");

  // Summary
  console.log("=".repeat(70));
  console.log("🎉 MAINNET DEPLOYMENT COMPLETE!\n");
  console.log("Contract Addresses:");
  console.log("  USD_FRY Token:              ", usdFryAddress);
  console.log("  WreckageProcessorWithOracle:", wreckageAddress);
  console.log("  FRYPredictionMarket:        ", predictionAddress);
  console.log("\nChainlink Price Feeds (Arbitrum Mainnet):");
  console.log("  BTC/USD:", BTC_USD_FEED);
  console.log("  ETH/USD:", ETH_USD_FEED);
  console.log("\nUSDC Address:");
  console.log("  USDC:   ", USDC_MAINNET);
  console.log("\nNext Steps:");
  console.log("  1. Verify contracts on Arbiscan:");
  console.log("     npx hardhat verify --network arbitrum", usdFryAddress);
  console.log("     npx hardhat verify --network arbitrum", wreckageAddress, usdFryAddress);
  console.log("     npx hardhat verify --network arbitrum", predictionAddress, usdFryAddress, USDC_MAINNET);
  console.log("  2. Update demo with mainnet addresses");
  console.log("  3. Test wreckage processing with real funds");
  console.log("  4. Create more prediction markets");
  console.log("  5. Start user acquisition campaign");
  console.log("=".repeat(70));

  // Save deployment info
  const deploymentInfo = {
    network: "arbitrum",
    chainId: 42161,
    timestamp: new Date().toISOString(),
    deployer: deployer.address,
    contracts: {
      USDFRYToken: usdFryAddress,
      WreckageProcessorWithOracle: wreckageAddress,
      FRYPredictionMarket: predictionAddress
    },
    externalContracts: {
      USDC: USDC_MAINNET
    },
    chainlinkFeeds: {
      BTC_USD: BTC_USD_FEED,
      ETH_USD: ETH_USD_FEED
    },
    initialMarket: {
      question: "Will BTC recover to $112k within 30 days? (50% of Oct 10 losses)",
      asset: "BTC",
      targetPrice: targetPrice.toString(),
      resolutionTime: resolutionTime,
      priceFeed: BTC_USD_FEED
    }
  };

  const fs = require('fs');
  fs.writeFileSync(
    'deployment-mainnet.json',
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("\n✓ Deployment info saved to deployment-mainnet.json");
  
  // Save to docs folder too
  fs.writeFileSync(
    '../../../docs/deployment-mainnet.json',
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("✓ Deployment info saved to docs/deployment-mainnet.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
