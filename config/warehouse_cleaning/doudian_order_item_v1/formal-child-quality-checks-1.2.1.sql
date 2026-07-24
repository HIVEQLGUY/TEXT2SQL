SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_json_actual_receive_amount_info_actual_receive_amount_details_df WHERE snapshot_date = toDate('2026-07-22')) != 72575,
    'actual receive amount detail DWD row count mismatch'
);

SELECT throwIf(
    (
        SELECT uniqExact(tuple(shop_id, shop_order_id, json_item_index))
        FROM youmei_sandbox.dwd_json_actual_receive_amount_info_actual_receive_amount_details_df
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 72575,
    'actual receive amount detail DWD composite key is not unique'
);

SELECT throwIf(
    (
        SELECT count() - uniqExact(tuple(shop_id, shop_order_id, json_item_index))
        FROM youmei_sandbox.dwd_json_actual_receive_amount_info_actual_receive_amount_details_df
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 0,
    'actual receive amount detail target contains same key with different content'
);

SELECT throwIf(
    (
        SELECT countIf(amount IS NULL OR amount_detail_type_code IS NULL)
        FROM youmei_sandbox.dwd_json_actual_receive_amount_info_actual_receive_amount_details_df
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 0,
    'actual receive amount detail required fields contain NULL'
);

SELECT throwIf(
    (
        SELECT count()
        FROM youmei_sandbox.dwd_json_actual_receive_amount_info_actual_receive_amount_details_df d
        LEFT JOIN youmei_sandbox.dwd_trade_order_df h
          ON d.snapshot_date = h.snapshot_date
         AND d.shop_id = h.shop_id
         AND d.shop_order_id = h.shop_order_id
        WHERE d.snapshot_date = toDate('2026-07-22')
          AND h.shop_order_id IS NULL
    ) != 0,
    'actual receive amount detail has missing parent order header'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_json_logistics_info_df WHERE snapshot_date = toDate('2026-07-22')) != 42839,
    'logistics info DWD row count mismatch'
);

SELECT throwIf(
    (
        SELECT uniqExact(tuple(shop_id, shop_order_id, json_item_index))
        FROM youmei_sandbox.dwd_json_logistics_info_df
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 42839,
    'logistics info DWD composite key is not unique'
);

SELECT throwIf(
    (
        SELECT count() - uniqExact(tuple(shop_id, shop_order_id, json_item_index))
        FROM youmei_sandbox.dwd_json_logistics_info_df
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 0,
    'logistics info target contains same key with different content'
);

SELECT throwIf(
    (
        SELECT count()
        FROM youmei_sandbox.dwd_json_logistics_info_df d
        LEFT JOIN youmei_sandbox.dwd_trade_order_df h
          ON d.snapshot_date = h.snapshot_date
         AND d.shop_id = h.shop_id
         AND d.shop_order_id = h.shop_order_id
        WHERE d.snapshot_date = toDate('2026-07-22')
          AND h.shop_order_id IS NULL
    ) != 0,
    'logistics info has missing parent order header'
);

SELECT throwIf(
    (
        SELECT count()
        FROM system.columns
        WHERE database = 'youmei_sandbox'
          AND table IN ('dwd_json_actual_receive_amount_info_actual_receive_amount_details_df', 'dwd_json_logistics_info_df')
          AND (name IN ('origin_data', 'actual_receive_amount_info', 'logistics_info') OR type LIKE 'JSON%')
    ) != 0,
    'child DWD contains raw JSON columns'
);

SELECT
    'DWD_抖店订单商家收入金额明细项事实全量快照表(dwd_json_actual_receive_amount_info_actual_receive_amount_details_df)' AS table_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id, json_item_index)) AS key_count,
    sum(amount) AS amount_sum_yuan,
    countIf(startsWith(coalesce(amount_detail_type_name, ''), '未知类型:')) AS unknown_type_count
FROM youmei_sandbox.dwd_json_actual_receive_amount_info_actual_receive_amount_details_df
WHERE snapshot_date = toDate('2026-07-22');

SELECT
    'DWD_抖店订单物流信息事实全量快照表(dwd_json_logistics_info_df)' AS table_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id, json_item_index)) AS key_count,
    countIf(tracking_no IS NULL) AS tracking_no_null_count,
    countIf(shipped_at IS NULL) AS shipped_at_null_count,
    sum(platform_delivery_payable_amount) AS platform_delivery_payable_amount_sum_yuan
FROM youmei_sandbox.dwd_json_logistics_info_df
WHERE snapshot_date = toDate('2026-07-22');
