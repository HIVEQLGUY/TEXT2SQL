SELECT currentDatabase() AS database, version() AS version;

SELECT
    name,
    engine,
    total_rows,
    total_bytes
FROM system.tables
WHERE database = 'youmei_sandbox'
  AND name IN (
    'dwd_trade_order_df',
    'dwd_trade_order_item_df',
    'dwd_trade_order_logistics_tracking_no_shadow_1_3_3',
    'dwd_trade_order_shadow_1_2_0',
    'dwd_trade_order_item_shadow_1_2_0',
    'dwd_trade_order_logistics_tracking_no_shadow_1_3_2',
    'dwd_trade_order_logistics_package_validation_1_3_1',
    'dwd_trade_order_logistics_package_item_validation_1_3_1',
    'dwd_trade_order_df_backup_1_2_0',
    'dwd_trade_order_item_df_backup_1_2_0',
    'dwd_trade_order_item_df_direct_logistics_backup_1_3_1',
    'dwd_deprecated_actual_receive_amount_detail_backup_1_2_1',
    'dwd_deprecated_logistics_info_backup_1_2_1'
  )
ORDER BY name;

SELECT throwIf(
    (SELECT count() FROM system.tables WHERE database = 'youmei_sandbox' AND name = 'dwd_trade_order_df') != 1,
    '当前正式订单主单事实表不存在'
) AS formal_order_present;

SELECT throwIf(
    (SELECT count() FROM system.tables WHERE database = 'youmei_sandbox' AND name = 'dwd_trade_order_item_df') != 1,
    '当前正式订单商品明细事实表不存在'
) AS formal_item_present;

SELECT throwIf(
    (SELECT count() FROM system.tables WHERE database = 'youmei_sandbox' AND name = 'dwd_trade_order_logistics_tracking_no_shadow_1_3_3') != 1,
    '当前待审阅快递单号粒度影子表不存在'
) AS latest_shadow_present;
