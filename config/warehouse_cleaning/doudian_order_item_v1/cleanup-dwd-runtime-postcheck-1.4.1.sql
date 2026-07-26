SELECT
    name,
    engine,
    total_rows,
    total_bytes
FROM system.tables
WHERE database = 'youmei_sandbox'
  AND (positionCaseInsensitive(name, 'dwd') > 0)
ORDER BY name;

SELECT throwIf(
    (SELECT count() FROM system.tables WHERE database = 'youmei_sandbox' AND name IN (
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
    )) != 0,
    '仍存在未清理的历史DWD对象'
) AS stale_objects_absent;

SELECT throwIf(
    (SELECT count() FROM system.tables WHERE database = 'youmei_sandbox' AND name IN (
        'dwd_trade_order_df',
        'dwd_trade_order_item_df',
        'dwd_trade_order_logistics_tracking_no_shadow_1_3_3'
    )) != 3,
    '当前正式表或待审阅影子表数量不正确'
) AS current_objects_present;
