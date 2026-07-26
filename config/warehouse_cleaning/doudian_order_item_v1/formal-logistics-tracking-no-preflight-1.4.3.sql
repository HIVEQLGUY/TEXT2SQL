SELECT currentDatabase() AS database, version() AS version;

SELECT throwIf(
    (SELECT count() FROM system.tables
      WHERE database = 'youmei_sandbox'
        AND name = 'dwd_trade_order_logistics_tracking_no_shadow_1_3_3') != 1,
    '已批准的快递单号粒度影子表不存在'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3) = 0,
    '已批准的快递单号粒度影子结果为空'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3)
    != (SELECT uniqExact(tuple(shop_id, shop_order_id, tracking_no))
          FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3),
    '已批准的快递单号粒度影子结果复合键不唯一'
);

SELECT throwIf(
    (SELECT min(snapshot_date) FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3) != toDate('2026-07-23')
    OR (SELECT max(snapshot_date) FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3) != toDate('2026-07-23'),
    '影子结果不是已批准的 2026-07-23 快照'
);

SELECT throwIf(
    (SELECT count() FROM system.columns
      WHERE database = 'youmei_sandbox'
        AND table = 'dwd_trade_order_logistics_tracking_no_shadow_1_3_3'
        AND name = 'package_id') != 0,
    '快递单号粒度正式表不允许保留包裹ID字段'
);

