SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3) = 0,
    '快递单号粒度影子表为空'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3)
    != (SELECT uniqExact(tuple(shop_id, shop_order_id, tracking_no)) FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3),
    '快递单号粒度复合键不唯一'
);

SELECT throwIf(
    (SELECT countIf(tracking_no IS NULL OR tracking_no = '') FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3) != 0,
    '快递单号为空'
);

SELECT throwIf(
    (SELECT count() FROM system.columns WHERE database = 'youmei_sandbox' AND table = 'dwd_trade_order_logistics_tracking_no_shadow_1_3_3' AND name = 'package_id') != 0,
    '影子表不应保留包裹ID粒度字段'
);
