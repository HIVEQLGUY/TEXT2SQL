SELECT
    count() AS shadow_row_count,
    uniqExact(tuple(shop_order_id, item_index)) AS shadow_key_count,
    countIf(shop_order_id = '') AS empty_shop_order_id_count,
    countIf(product_id IS NULL) AS product_id_null_count,
    countIf(sku_id IS NULL) AS sku_id_null_count,
    countIf(item_quantity IS NULL) AS item_quantity_null_count,
    countIf(goods_amount IS NULL) AS goods_amount_null_count,
    countIf(item_paid_amount IS NULL) AS item_paid_amount_null_count,
    min(goods_amount) AS goods_amount_min_yuan,
    max(goods_amount) AS goods_amount_max_yuan,
    min(item_paid_amount) AS item_paid_amount_min_yuan,
    max(item_paid_amount) AS item_paid_amount_max_yuan,
    uniqExact(documented_json_path_count) AS json_path_count_versions,
    uniqExact(documented_scalar_field_count) AS json_scalar_count_versions,
    uniqExact(documented_business_relation_count) AS json_relation_count_versions,
    uniqExact(json_expansion_status) AS json_expansion_status_versions,
    uniqExact(cleaning_contract_version) AS contract_versions
FROM youmei_sandbox.dwd_trade_order_item_shadow_1_2_0;

SELECT
    count() AS raw_json_column_count
FROM system.columns
WHERE database = 'youmei_sandbox'
  AND table = 'dwd_trade_order_item_shadow_1_2_0'
  AND (name = 'sku_order_list' OR type LIKE 'JSON%');

SELECT name
FROM system.tables
WHERE database = 'youmei_sandbox'
  AND name IN ('dwd_trade_order_item_shadow_1_2_0', 'dwd_trade_order_df', 'dwd_trade_order_item_df')
ORDER BY name;
