SELECT currentDatabase() AS database, version() AS version;

SELECT throwIf(
    (SELECT count() FROM system.tables
      WHERE database = 'youmei_sandbox'
        AND name = 'dwd_trade_order_logistics_tracking_no_df') != 1,
    '回滚遗留的正式物流表不存在，禁止执行清理'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df) != 0,
    '正式物流表不是空表，禁止按回滚遗留对象清理'
);
