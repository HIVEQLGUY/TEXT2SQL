SELECT
    'order_df' AS table_name,
    count() AS row_count,
    (SELECT count() FROM system.columns WHERE database = 'youmei_sandbox' AND table = 'dwd_trade_order_df') AS column_count
FROM youmei_sandbox.dwd_trade_order_df;

SELECT
    'order_item_df' AS table_name,
    count() AS row_count,
    (SELECT count() FROM system.columns WHERE database = 'youmei_sandbox' AND table = 'dwd_trade_order_item_df') AS column_count,
    uniqExact(tuple(shop_id, shop_order_id, sku_order_id)) AS sku_order_key_count,
    countIf(sku_order_id IS NULL) AS sku_order_id_null_count
FROM youmei_sandbox.dwd_trade_order_item_df;

SELECT
    'logistics_package_df' AS table_name,
    count() AS row_count,
    (SELECT count() FROM system.columns WHERE database = 'youmei_sandbox' AND table = 'dwd_trade_order_logistics_package_df') AS column_count,
    uniqExact(tuple(shop_id, shop_order_id, package_id)) AS package_key_count,
    uniqExact(tuple(shop_id, shop_order_id, tracking_no)) AS tracking_no_key_count
FROM youmei_sandbox.dwd_trade_order_logistics_package_df;

SELECT
    'logistics_package_item_df' AS table_name,
    count() AS row_count,
    (SELECT count() FROM system.columns WHERE database = 'youmei_sandbox' AND table = 'dwd_trade_order_logistics_package_item_df') AS column_count,
    uniqExact(tuple(shop_id, shop_order_id, package_id, sku_order_id)) AS package_sku_order_key_count
FROM youmei_sandbox.dwd_trade_order_logistics_package_item_df;

SELECT
    name
FROM system.tables
WHERE database = 'youmei_sandbox'
  AND name IN
  (
      'dwd_trade_order_item_df',
      'dwd_trade_order_item_df_backup_1_3_0',
      'dwd_trade_order_logistics_package_df',
      'dwd_trade_order_logistics_package_item_df'
  )
ORDER BY name;
