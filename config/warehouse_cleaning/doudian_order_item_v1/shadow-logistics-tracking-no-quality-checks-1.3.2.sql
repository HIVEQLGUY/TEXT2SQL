SELECT
    'tracking_no_shadow_key_quality' AS check_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id, tracking_no)) AS tracking_no_key_count,
    countIf(tracking_no IS NULL OR tracking_no = '') AS tracking_no_null_count
FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_2;

SELECT
    'tracking_no_shadow_no_package_id_column' AS check_name,
    countIf(name ILIKE '%package_id%') AS package_id_column_count
FROM system.columns
WHERE database = 'youmei_sandbox'
  AND table = 'dwd_trade_order_logistics_tracking_no_shadow_1_3_2';

SELECT
    'tracking_no_shadow_source_reconciliation' AS check_name,
    sum(package_count) AS shadow_package_count,
    sum(package_product_row_count) AS shadow_package_product_row_count,
    sum(sku_order_count) AS shadow_sku_order_count,
    sum(shipped_product_count) AS shadow_shipped_product_count,
    sum(guarantee_amount) AS shadow_guarantee_amount,
    sum(platform_delivery_discount_amount) AS shadow_platform_delivery_discount_amount,
    sum(platform_delivery_paid_amount) AS shadow_platform_delivery_paid_amount,
    sum(platform_delivery_payable_amount) AS shadow_platform_delivery_payable_amount
FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_2;

SELECT
    'formal_dwd_after_revert' AS check_name,
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_df) AS order_rows,
    (SELECT count() FROM system.columns WHERE database = 'youmei_sandbox' AND table = 'dwd_trade_order_df') AS order_column_count,
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_item_df) AS item_rows,
    (SELECT count() FROM system.columns WHERE database = 'youmei_sandbox' AND table = 'dwd_trade_order_item_df') AS item_column_count,
    (SELECT count() FROM system.tables WHERE database = 'youmei_sandbox' AND name IN ('dwd_trade_order_logistics_package_df', 'dwd_trade_order_logistics_package_item_df')) AS direct_logistics_formal_table_count;
