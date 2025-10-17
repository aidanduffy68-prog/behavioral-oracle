-- October 10, 2025 Hyperliquid Liquidation Analysis
-- Dune Analytics SQL Queries

-- ============================================
-- Query 1: All Liquidations on October 10
-- ============================================
-- Purpose: Get complete liquidation dataset for the cascade period

SELECT 
  block_time,
  tx_hash,
  liquidated_user,
  liquidator,
  collateral_asset,
  collateral_amount,
  debt_asset,
  debt_amount,
  liquidation_price,
  CASE 
    WHEN liquidation_type = 1 THEN 'Orderbook'
    WHEN liquidation_type = 2 THEN 'Insurance Fund'
    WHEN liquidation_type = 3 THEN 'ADL'
    ELSE 'Unknown'
  END as liquidation_mechanism
FROM hyperliquid.liquidations
WHERE block_time >= TIMESTAMP '2025-10-10 20:00:00'
  AND block_time <= TIMESTAMP '2025-10-10 22:00:00'
ORDER BY block_time ASC;

-- ============================================
-- Query 2: Liquidation Cascade Velocity
-- ============================================
-- Purpose: Track liquidations per minute to identify cascade acceleration

SELECT 
  DATE_TRUNC('minute', block_time) as minute,
  COUNT(*) as liquidation_count,
  SUM(collateral_amount) as total_collateral_liquidated,
  COUNT(DISTINCT liquidated_user) as unique_users_liquidated,
  AVG(liquidation_price) as avg_liquidation_price
FROM hyperliquid.liquidations
WHERE block_time >= TIMESTAMP '2025-10-10 20:00:00'
  AND block_time <= TIMESTAMP '2025-10-10 22:00:00'
GROUP BY DATE_TRUNC('minute', block_time)
ORDER BY minute ASC;

-- ============================================
-- Query 3: Insurance Fund Utilization
-- ============================================
-- Purpose: Track insurance fund depletion during cascade

SELECT 
  block_time,
  insurance_fund_balance,
  insurance_fund_balance - LAG(insurance_fund_balance) OVER (ORDER BY block_time) as balance_change,
  (insurance_fund_balance / MAX(insurance_fund_balance) OVER ()) * 100 as utilization_pct
FROM hyperliquid.insurance_fund_snapshots
WHERE block_time >= TIMESTAMP '2025-10-10 20:00:00'
  AND block_time <= TIMESTAMP '2025-10-10 22:00:00'
ORDER BY block_time ASC;

-- ============================================
-- Query 4: ADL Events (Sophisticated Traders)
-- ============================================
-- Purpose: Identify who got auto-deleveraged (highest P&L traders)

SELECT 
  block_time,
  deleveraged_user,
  position_asset,
  position_size,
  unrealized_pnl,
  leverage,
  (unrealized_pnl / position_size) * leverage as adl_score
FROM hyperliquid.adl_events
WHERE block_time >= TIMESTAMP '2025-10-10 20:00:00'
  AND block_time <= TIMESTAMP '2025-10-10 22:00:00'
ORDER BY adl_score DESC;

-- ============================================
-- Query 5: Top Liquidated Wallets
-- ============================================
-- Purpose: Identify largest losers in the cascade

SELECT 
  liquidated_user,
  COUNT(*) as liquidation_count,
  SUM(collateral_amount) as total_loss,
  AVG(liquidation_price) as avg_liquidation_price,
  MIN(block_time) as first_liquidation,
  MAX(block_time) as last_liquidation
FROM hyperliquid.liquidations
WHERE block_time >= TIMESTAMP '2025-10-10 20:00:00'
  AND block_time <= TIMESTAMP '2025-10-10 22:00:00'
GROUP BY liquidated_user
ORDER BY total_loss DESC
LIMIT 100;

-- ============================================
-- Query 6: Market Maker Liquidity Withdrawal
-- ============================================
-- Purpose: Track top liquidity providers removing liquidity

WITH top_mms AS (
  SELECT DISTINCT maker_address
  FROM hyperliquid.trades
  WHERE block_time >= TIMESTAMP '2025-10-10 00:00:00'
    AND block_time < TIMESTAMP '2025-10-10 20:00:00'
  GROUP BY maker_address
  HAVING SUM(volume) > 1000000  -- Top MMs by volume
  ORDER BY SUM(volume) DESC
  LIMIT 20
)

SELECT 
  DATE_TRUNC('minute', block_time) as minute,
  maker_address,
  SUM(CASE WHEN side = 'bid' THEN liquidity_amount ELSE 0 END) as bid_liquidity,
  SUM(CASE WHEN side = 'ask' THEN liquidity_amount ELSE 0 END) as ask_liquidity,
  SUM(liquidity_amount) as total_liquidity
FROM hyperliquid.liquidity_events
WHERE maker_address IN (SELECT maker_address FROM top_mms)
  AND block_time >= TIMESTAMP '2025-10-10 20:00:00'
  AND block_time <= TIMESTAMP '2025-10-10 22:00:00'
GROUP BY DATE_TRUNC('minute', block_time), maker_address
ORDER BY minute ASC, maker_address;

-- ============================================
-- Query 7: Cross-Asset Price Correlation
-- ============================================
-- Purpose: Track USDe, wBETH, BNSOL prices during manipulation

SELECT 
  DATE_TRUNC('minute', block_time) as minute,
  asset,
  AVG(price) as avg_price,
  MIN(price) as min_price,
  MAX(price) as max_price,
  STDDEV(price) as price_volatility
FROM hyperliquid.oracle_prices
WHERE asset IN ('USDe', 'wBETH', 'BNSOL')
  AND block_time >= TIMESTAMP '2025-10-10 20:00:00'
  AND block_time <= TIMESTAMP '2025-10-10 22:00:00'
GROUP BY DATE_TRUNC('minute', block_time), asset
ORDER BY minute ASC, asset;

-- ============================================
-- Query 8: Volume Spike Detection
-- ============================================
-- Purpose: Identify unusual volume spikes that triggered cascade

WITH baseline_volume AS (
  SELECT 
    asset,
    AVG(volume) as avg_volume,
    STDDEV(volume) as stddev_volume
  FROM hyperliquid.trades
  WHERE block_time >= TIMESTAMP '2025-10-01 00:00:00'
    AND block_time < TIMESTAMP '2025-10-10 20:00:00'
  GROUP BY asset
)

SELECT 
  DATE_TRUNC('minute', t.block_time) as minute,
  t.asset,
  SUM(t.volume) as minute_volume,
  b.avg_volume,
  (SUM(t.volume) - b.avg_volume) / b.stddev_volume as z_score
FROM hyperliquid.trades t
JOIN baseline_volume b ON t.asset = b.asset
WHERE t.block_time >= TIMESTAMP '2025-10-10 20:00:00'
  AND t.block_time <= TIMESTAMP '2025-10-10 22:00:00'
GROUP BY DATE_TRUNC('minute', t.block_time), t.asset, b.avg_volume, b.stddev_volume
HAVING (SUM(t.volume) - b.avg_volume) / b.stddev_volume > 3  -- 3+ standard deviations
ORDER BY z_score DESC;

-- ============================================
-- Query 9: Trader Retention Analysis
-- ============================================
-- Purpose: Track how many liquidated traders returned to platform

WITH liquidated_users AS (
  SELECT DISTINCT liquidated_user
  FROM hyperliquid.liquidations
  WHERE block_time >= TIMESTAMP '2025-10-10 20:00:00'
    AND block_time <= TIMESTAMP '2025-10-10 22:00:00'
)

SELECT 
  COUNT(DISTINCT l.liquidated_user) as total_liquidated,
  COUNT(DISTINCT t.trader_address) as returned_traders,
  (COUNT(DISTINCT t.trader_address) * 100.0 / COUNT(DISTINCT l.liquidated_user)) as retention_rate
FROM liquidated_users l
LEFT JOIN hyperliquid.trades t 
  ON l.liquidated_user = t.trader_address
  AND t.block_time > TIMESTAMP '2025-10-10 22:00:00'
  AND t.block_time <= TIMESTAMP '2025-10-17 22:00:00'  -- 7 days post-event
;

-- ============================================
-- Query 10: Dashboard Summary Stats
-- ============================================
-- Purpose: Key metrics for dashboard header

SELECT 
  COUNT(DISTINCT liquidated_user) as unique_liquidated_users,
  COUNT(*) as total_liquidations,
  SUM(collateral_amount) as total_value_liquidated,
  AVG(collateral_amount) as avg_liquidation_size,
  MIN(block_time) as cascade_start,
  MAX(block_time) as cascade_end,
  EXTRACT(EPOCH FROM (MAX(block_time) - MIN(block_time))) / 60 as cascade_duration_minutes
FROM hyperliquid.liquidations
WHERE block_time >= TIMESTAMP '2025-10-10 20:00:00'
  AND block_time <= TIMESTAMP '2025-10-10 22:00:00';
