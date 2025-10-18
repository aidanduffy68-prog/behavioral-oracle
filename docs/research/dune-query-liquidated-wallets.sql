-- Get all unique wallet addresses liquidated on October 10, 2025
-- For FRY Retention Oracle population

-- ============================================
-- Query: Liquidated Wallets for Retention Tracking
-- ============================================
-- Purpose: Get wallet addresses + liquidation details to populate FRY oracle

SELECT 
  liquidated_user as wallet_address,
  MIN(block_time) as first_liquidation_time,
  COUNT(*) as liquidation_count,
  SUM(collateral_amount) as total_liquidated_usd,
  STRING_AGG(DISTINCT collateral_asset, ', ') as assets_liquidated
FROM hyperliquid.liquidations
WHERE block_time >= TIMESTAMP '2025-10-10 00:00:00'
  AND block_time <= TIMESTAMP '2025-10-10 23:59:59'
GROUP BY liquidated_user
ORDER BY total_liquidated_usd DESC;

-- ============================================
-- Query: Post-Liquidation Activity (30-day tracking)
-- ============================================
-- Purpose: Check if liquidated wallets returned to trading

WITH liquidated_wallets AS (
  SELECT DISTINCT liquidated_user as wallet_address
  FROM hyperliquid.liquidations
  WHERE block_time >= TIMESTAMP '2025-10-10 00:00:00'
    AND block_time <= TIMESTAMP '2025-10-10 23:59:59'
),
post_liquidation_activity AS (
  SELECT 
    t.trader as wallet_address,
    COUNT(*) as trade_count,
    SUM(t.volume_usd) as total_volume_usd,
    MIN(t.block_time) as first_trade_after_liquidation,
    MAX(t.block_time) as last_trade_after_liquidation
  FROM hyperliquid.trades t
  INNER JOIN liquidated_wallets lw ON t.trader = lw.wallet_address
  WHERE t.block_time >= TIMESTAMP '2025-10-10 00:00:00'
    AND t.block_time <= TIMESTAMP '2025-11-09 23:59:59'  -- 30 days
  GROUP BY t.trader
)
SELECT 
  lw.wallet_address,
  CASE 
    WHEN pla.wallet_address IS NOT NULL THEN TRUE 
    ELSE FALSE 
  END as returned_30d,
  COALESCE(pla.trade_count, 0) as trades_30d,
  COALESCE(pla.total_volume_usd, 0) as ltv_30d,
  pla.first_trade_after_liquidation,
  pla.last_trade_after_liquidation
FROM liquidated_wallets lw
LEFT JOIN post_liquidation_activity pla ON lw.wallet_address = pla.wallet_address
ORDER BY ltv_30d DESC;

-- ============================================
-- Query: Retention Metrics Summary
-- ============================================
-- Purpose: Calculate baseline retention rate for FRY comparison

WITH liquidated_wallets AS (
  SELECT DISTINCT liquidated_user as wallet_address
  FROM hyperliquid.liquidations
  WHERE block_time >= TIMESTAMP '2025-10-10 00:00:00'
    AND block_time <= TIMESTAMP '2025-10-10 23:59:59'
),
returned_wallets AS (
  SELECT DISTINCT t.trader as wallet_address
  FROM hyperliquid.trades t
  INNER JOIN liquidated_wallets lw ON t.trader = lw.wallet_address
  WHERE t.block_time >= TIMESTAMP '2025-10-10 00:00:00'
    AND t.block_time <= TIMESTAMP '2025-11-09 23:59:59'  -- 30 days
)
SELECT 
  COUNT(DISTINCT lw.wallet_address) as total_liquidated,
  COUNT(DISTINCT rw.wallet_address) as returned_30d,
  ROUND(100.0 * COUNT(DISTINCT rw.wallet_address) / COUNT(DISTINCT lw.wallet_address), 2) as return_rate_pct
FROM liquidated_wallets lw
LEFT JOIN returned_wallets rw ON lw.wallet_address = rw.wallet_address;
