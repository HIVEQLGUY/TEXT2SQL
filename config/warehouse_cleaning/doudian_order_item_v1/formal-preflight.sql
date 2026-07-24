SELECT currentDatabase() AS database, version() AS version;

SELECT
    name,
    total_rows,
    total_bytes
FROM system.tables
WHERE database = 'youmei_sandbox'
  AND name IN (
      'ods_api_dd_sale_order_list_info_f',
      'dwd_trade_order_shadow_1_2_0',
      'dwd_trade_order_item_shadow_1_2_0',
      'dwd_trade_order_df',
      'dwd_trade_order_item_df'
  )
ORDER BY name;

SELECT
    dt,
    count() AS source_rows,
    uniqExact(tuple(shop_id, order_id)) AS unique_order_keys,
    sum(length(JSONExtractArrayRaw(sku_order_list))) AS expanded_item_rows
FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
GROUP BY dt
ORDER BY dt;

SELECT
    snapshot_date,
    count() AS rows,
    uniqExact(tuple(shop_id, shop_order_id)) AS keys
FROM youmei_sandbox.dwd_trade_order_shadow_1_2_0
GROUP BY snapshot_date
ORDER BY snapshot_date;

SELECT
    snapshot_date,
    count() AS rows,
    uniqExact(tuple(shop_order_id, item_index)) AS keys
FROM youmei_sandbox.dwd_trade_order_item_shadow_1_2_0
GROUP BY snapshot_date
ORDER BY snapshot_date;
