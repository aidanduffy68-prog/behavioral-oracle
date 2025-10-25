const hre = require("hardhat");
const fs = require('fs');

async function main() {
  console.log("\n🔍 Verifying FRY Protocol Contracts on Arbiscan...\n");
  
  // Load deployment info
  const deploymentInfo = JSON.parse(fs.readFileSync('deployment.json', 'utf8'));
  const contracts = deploymentInfo.contracts;
  
  console.log("Network:", deploymentInfo.network);
  console.log("Deployer:", deploymentInfo.deployer);
  console.log("\n" + "=".repeat(70) + "\n");
  
  try {
    // Verify USDFRYToken
    console.log("📝 Verifying USDFRYToken...");
    await hre.run("verify:verify", {
      address: contracts.USDFRYToken,
      constructorArguments: []
    });
    console.log("✅ USDFRYToken verified");
    
    // Verify AgentBVerifier
    console.log("\n📝 Verifying AgentBVerifier...");
    await hre.run("verify:verify", {
      address: contracts.AgentBVerifier,
      constructorArguments: []
    });
    console.log("✅ AgentBVerifier verified");
    
    // Verify ConfidentialPositionVerifier
    console.log("\n📝 Verifying ConfidentialPositionVerifier...");
    await hre.run("verify:verify", {
      address: contracts.ConfidentialPositionVerifier,
      constructorArguments: []
    });
    console.log("✅ ConfidentialPositionVerifier verified");
    
    // Verify LiquidityRailsRouter
    console.log("\n📝 Verifying LiquidityRailsRouter...");
    await hre.run("verify:verify", {
      address: contracts.LiquidityRailsRouter,
      constructorArguments: [contracts.USDFRYToken]
    });
    console.log("✅ LiquidityRailsRouter verified");
    
    // Verify WreckageMatchingPool
    console.log("\n📝 Verifying WreckageMatchingPool...");
    await hre.run("verify:verify", {
      address: contracts.WreckageMatchingPool,
      constructorArguments: [contracts.USDFRYToken]
    });
    console.log("✅ WreckageMatchingPool verified");
    
    console.log("\n" + "=".repeat(70));
    console.log("\n🎉 All contracts verified on Arbiscan!\n");
    
  } catch (error) {
    console.error("\n❌ Verification error:", error.message);
    console.log("\nNote: Contracts may already be verified or need a few minutes after deployment.");
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
