SELECT currentDatabase() AS database, version() AS version;

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f WHERE dt = '2026-07-23') = 0,
    '当前源表缺少 2026-07-23 快照分区'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f WHERE dt = '2026-07-23')
    != (SELECT uniqExact(tuple(shop_id, order_id)) FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f WHERE dt = '2026-07-23'),
    '当前源表店铺ID与店铺订单号存在重复主单键'
);
