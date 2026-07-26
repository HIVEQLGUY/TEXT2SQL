SELECT
    'formal_empty_rollback_artifact_quality' AS check_name,
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df) AS row_count,
    (SELECT count() FROM system.columns
      WHERE database = 'youmei_sandbox'
        AND table = 'dwd_trade_order_logistics_tracking_no_df') AS column_count;

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df) != 0,
    '回滚遗留正式表已有数据，禁止清理'
);
