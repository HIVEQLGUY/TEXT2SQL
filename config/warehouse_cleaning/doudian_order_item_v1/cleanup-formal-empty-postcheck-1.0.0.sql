SELECT throwIf(
    (SELECT count() FROM system.tables
      WHERE database = 'youmei_sandbox'
        AND name = 'dwd_trade_order_logistics_tracking_no_df') != 0,
    '回滚遗留的空正式表仍存在'
);

SELECT
    'formal_empty_rollback_artifact_postcheck' AS check_name,
    (SELECT count() FROM system.tables
      WHERE database = 'youmei_sandbox'
        AND name = 'dwd_trade_order_logistics_tracking_no_df') AS remaining_table_count;
