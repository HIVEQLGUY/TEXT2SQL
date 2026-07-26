SELECT
    'formal_tracking_no_key_quality' AS check_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id, tracking_no)) AS tracking_no_key_count,
    countIf(tracking_no IS NULL OR tracking_no = '') AS tracking_no_null_count
FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3;

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3) = 0,
    '正式快递单号粒度候选表为空'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3)
    != (SELECT uniqExact(tuple(shop_id, shop_order_id, tracking_no))
          FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3),
    '正式快递单号粒度候选表复合键不唯一'
);

SELECT throwIf(
    (SELECT countIf(tracking_no IS NULL OR tracking_no = '')
       FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3) != 0,
    '正式快递单号粒度候选表存在空快递单号'
);

SELECT throwIf(
    (SELECT count() FROM system.columns
      WHERE database = 'youmei_sandbox'
        AND table = 'dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3'
        AND name = 'package_id') != 0,
    '正式快递单号粒度候选表不应存在包裹ID字段'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3)
    != (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3)
    OR (SELECT sum(package_count) FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3)
       != (SELECT sum(package_count) FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3)
    OR (SELECT sum(package_product_row_count) FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3)
       != (SELECT sum(package_product_row_count) FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3)
    OR (SELECT sum(sku_order_count) FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3)
       != (SELECT sum(sku_order_count) FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3),
    '正式候选表与已批准影子结果的行数或汇总值不一致'
);

