const hre = require("hardhat");

async function main() {
  console.log("\n🍟 FRY Protocol Deployment Starting...\n");
  
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "ETH");
  console.log("Network:", hre.network.name);
  console.log("\n" + "=".repeat(70) + "\n");
  
  // 1. Deploy USD_FRY Token
  console.log("📝 Deploying USDFRYToken...");
  const USDFRYToken = await hre.ethers.getContractFactory("USDFRYToken");
  const usdFryToken = await USDFRYToken.deploy();
  await usdFryToken.waitForDeployment();
  const usdFryTokenAddress = await usdFryToken.getAddress();
  console.log("✅ USDFRYToken deployed to:", usdFryTokenAddress);
  
  // 2. Deploy AgentBVerifier
  console.log("\n📝 Deploying AgentBVerifier...");
  const AgentBVerifier = await hre.ethers.getContractFactory("AgentBVerifier");
  const agentBVerifier = await AgentBVerifier.deploy();
  await agentBVerifier.waitForDeployment();
  const agentBVerifierAddress = await agentBVerifier.getAddress();
  console.log("✅ AgentBVerifier deployed to:", agentBVerifierAddress);
  
  // 3. Deploy ConfidentialPositionVerifier
  console.log("\n📝 Deploying ConfidentialPositionVerifier...");
  const ConfidentialPositionVerifier = await hre.ethers.getContractFactory("ConfidentialPositionVerifier");
  const positionVerifier = await ConfidentialPositionVerifier.deploy();
  await positionVerifier.waitForDeployment();
  const positionVerifierAddress = await positionVerifier.getAddress();
  console.log("✅ ConfidentialPositionVerifier deployed to:", positionVerifierAddress);
  
  // 4. Deploy LiquidityRailsRouter
  console.log("\n📝 Deploying LiquidityRailsRouter...");
  const LiquidityRailsRouter = await hre.ethers.getContractFactory("LiquidityRailsRouter");
  const router = await LiquidityRailsRouter.deploy(usdFryTokenAddress);
  await router.waitForDeployment();
  const routerAddress = await router.getAddress();
  console.log("✅ LiquidityRailsRouter deployed to:", routerAddress);
  
  // 5. Deploy WreckageMatchingPool
  console.log("\n📝 Deploying WreckageMatchingPool...");
  const WreckageMatchingPool = await hre.ethers.getContractFactory("WreckageMatchingPool");
  const matchingPool = await WreckageMatchingPool.deploy(usdFryTokenAddress);
  await matchingPool.waitForDeployment();
  const matchingPoolAddress = await matchingPool.getAddress();
  console.log("✅ WreckageMatchingPool deployed to:", matchingPoolAddress);
  
  // 6. Grant roles
  console.log("\n📝 Setting up roles...");
  
  const MINTER_ROLE = await usdFryToken.MINTER_ROLE();
  
  // Grant MINTER_ROLE to router
  await usdFryToken.grantRole(MINTER_ROLE, routerAddress);
  console.log("✅ Granted MINTER_ROLE to LiquidityRailsRouter");
  
  // Grant MINTER_ROLE to matching pool
  await usdFryToken.grantRole(MINTER_ROLE, matchingPoolAddress);
  console.log("✅ Granted MINTER_ROLE to WreckageMatchingPool");
  
  // Summary
  console.log("\n" + "=".repeat(70));
  console.log("\n🎉 Deployment Complete!\n");
  console.log("Contract Addresses:");
  console.log("-------------------");
  console.log("USDFRYToken:                   ", usdFryTokenAddress);
  console.log("AgentBVerifier:                ", agentBVerifierAddress);
  console.log("ConfidentialPositionVerifier:  ", positionVerifierAddress);
  console.log("LiquidityRailsRouter:          ", routerAddress);
  console.log("WreckageMatchingPool:          ", matchingPoolAddress);
  console.log("\n" + "=".repeat(70) + "\n");
  
  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      USDFRYToken: usdFryTokenAddress,
      AgentBVerifier: agentBVerifierAddress,
      ConfidentialPositionVerifier: positionVerifierAddress,
      LiquidityRailsRouter: routerAddress,
      WreckageMatchingPool: matchingPoolAddress
    }
  };
  
  const fs = require('fs');
  fs.writeFileSync(
    'deployment.json',
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("💾 Deployment info saved to deployment.json\n");
  
  // Verification instructions
  if (hre.network.name !== "hardhat") {
    console.log("📋 To verify contracts on Arbiscan, run:");
    console.log(`npx hardhat verify --network ${hre.network.name} ${usdFryTokenAddress}`);
    console.log(`npx hardhat verify --network ${hre.network.name} ${agentBVerifierAddress}`);
    console.log(`npx hardhat verify --network ${hre.network.name} ${positionVerifierAddress}`);
    console.log(`npx hardhat verify --network ${hre.network.name} ${routerAddress} ${usdFryTokenAddress}`);
    console.log(`npx hardhat verify --network ${hre.network.name} ${matchingPoolAddress} ${usdFryTokenAddress}`);
    console.log("\n");
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
