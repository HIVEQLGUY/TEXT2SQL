SELECT
    name,
    total_rows,
    total_bytes,
    metadata_modification_time
FROM system.tables
WHERE database = 'youmei_sandbox'
  AND name IN (
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
    )) != 10,
    '待清理对象数量与发布清单不一致'
) AS cleanup_inventory_ready;
