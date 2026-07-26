SELECT throwIf(
    (SELECT count() FROM system.tables
      WHERE database = 'youmei_sandbox'
        AND name = 'dwd_trade_order_logistics_tracking_no_df') != 1,
    '正式快递单号粒度表不存在'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df) = 0,
    '正式快递单号粒度表为空'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df)
    != (SELECT uniqExact(tuple(shop_id, shop_order_id, tracking_no))
          FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df),
    '正式快递单号粒度表复合键不唯一'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df)
    != (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3),
    '正式表与影子结果行数不一致'
);

SELECT
    'formal_tracking_no_postcheck' AS check_name,
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df) AS formal_row_count,
    (SELECT uniqExact(tuple(shop_id, shop_order_id, tracking_no))
       FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df) AS formal_key_count,
    (SELECT count() FROM system.columns
       WHERE database = 'youmei_sandbox'
         AND table = 'dwd_trade_order_logistics_tracking_no_df') AS formal_column_count;
