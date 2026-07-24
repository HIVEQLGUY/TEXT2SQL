SELECT
    'item_rebuild_key_quality' AS check_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id, item_index)) AS item_index_key_count,
    uniqExact(tuple(shop_id, shop_order_id, sku_order_id)) AS sku_order_key_count,
    countIf(sku_order_id IS NULL) AS sku_order_id_null_count
FROM youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_1;

SELECT
    'package_rebuild_key_quality' AS check_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id, package_id)) AS package_id_key_count,
    uniqExact(tuple(shop_id, shop_order_id, tracking_no)) AS tracking_no_key_count,
    countIf(package_id IS NULL OR package_id = '') AS package_id_null_count,
    countIf(tracking_no IS NULL OR tracking_no = '') AS tracking_no_null_count
FROM youmei_sandbox.dwd_trade_order_logistics_package_df_rebuild_1_3_1;

SELECT
    'package_item_rebuild_key_quality' AS check_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id, package_id, sku_order_id)) AS package_sku_order_key_count,
    uniqExact(tuple(shop_id, shop_order_id, package_id, package_product_index)) AS package_product_index_key_count,
    countIf(sku_order_id IS NULL OR sku_order_id = '') AS sku_order_id_null_count
FROM youmei_sandbox.dwd_trade_order_logistics_package_item_df_rebuild_1_3_1;

SELECT
    'package_to_order_coverage' AS check_name,
    count() AS package_rows,
    countIf(o.shop_order_id IS NULL) AS package_not_in_order_count
FROM youmei_sandbox.dwd_trade_order_logistics_package_df_rebuild_1_3_1 p
LEFT JOIN youmei_sandbox.dwd_trade_order_df o
  ON p.shop_id = o.shop_id
 AND p.shop_order_id = o.shop_order_id;

SELECT
    'package_item_to_item_coverage' AS check_name,
    count() AS package_item_rows,
    countIf(i.sku_order_id IS NULL) AS package_item_not_in_item_count
FROM youmei_sandbox.dwd_trade_order_logistics_package_item_df_rebuild_1_3_1 p
LEFT JOIN youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_1 i
  ON p.shop_id = i.shop_id
 AND p.shop_order_id = i.shop_order_id
 AND p.sku_order_id = i.sku_order_id;

SELECT
    'package_item_to_package_coverage' AS check_name,
    count() AS package_item_rows,
    countIf(pkg.package_id IS NULL) AS package_item_not_in_package_count
FROM youmei_sandbox.dwd_trade_order_logistics_package_item_df_rebuild_1_3_1 p
LEFT JOIN youmei_sandbox.dwd_trade_order_logistics_package_df_rebuild_1_3_1 pkg
  ON p.shop_id = pkg.shop_id
 AND p.shop_order_id = pkg.shop_order_id
 AND p.package_id = pkg.package_id;

WITH by_package AS
(
    SELECT
        shop_id,
        shop_order_id,
        package_id,
        uniqExact(sku_order_id) AS sku_order_count
    FROM youmei_sandbox.dwd_trade_order_logistics_package_item_df_rebuild_1_3_1
    GROUP BY shop_id, shop_order_id, package_id
), by_sku_order AS
(
    SELECT
        shop_id,
        shop_order_id,
        sku_order_id,
        uniqExact(package_id) AS package_id_count,
        uniqExact(tracking_no) AS tracking_no_count
    FROM youmei_sandbox.dwd_trade_order_logistics_package_item_df_rebuild_1_3_1
    GROUP BY shop_id, shop_order_id, sku_order_id
)
SELECT
    'package_sku_cardinality_quality' AS check_name,
    countIf(sku_order_count = 1) AS one_sku_order_packages,
    countIf(sku_order_count > 1) AS multi_sku_order_packages,
    max(sku_order_count) AS max_sku_order_per_package,
    (SELECT count() FROM by_sku_order) AS shipped_sku_order_keys,
    (SELECT countIf(package_id_count = 1) FROM by_sku_order) AS one_package_sku_orders,
    (SELECT countIf(package_id_count > 1) FROM by_sku_order) AS multi_package_sku_orders,
    (SELECT max(package_id_count) FROM by_sku_order) AS max_package_per_sku_order,
    (SELECT countIf(tracking_no_count > 1) FROM by_sku_order) AS multi_tracking_no_sku_orders
FROM by_package;
