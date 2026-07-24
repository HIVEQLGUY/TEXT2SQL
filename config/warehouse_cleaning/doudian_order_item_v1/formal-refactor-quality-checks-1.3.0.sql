SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_df_rebuild_1_3_0 WHERE snapshot_date = toDate('2026-07-22')) != 49695,
    'refactored order DWD row count mismatch'
);

SELECT throwIf(
    (
        SELECT uniqExact(tuple(shop_id, shop_order_id))
        FROM youmei_sandbox.dwd_trade_order_df_rebuild_1_3_0
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 49695,
    'refactored order DWD composite key is not unique'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0 WHERE snapshot_date = toDate('2026-07-22')) != 85770,
    'refactored item DWD row count mismatch'
);

SELECT throwIf(
    (
        SELECT uniqExact(tuple(shop_id, shop_order_id, item_index))
        FROM youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 85770,
    'refactored item DWD composite key is not unique'
);

SELECT throwIf(
    (
        SELECT countIf(product_id IS NULL OR sku_id IS NULL OR item_quantity IS NULL)
        FROM youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 0,
    'refactored item required identifiers or quantity contain NULL'
);

SELECT throwIf(
    (
        SELECT count()
        FROM system.columns
        WHERE database = 'youmei_sandbox'
          AND table IN ('dwd_trade_order_df_rebuild_1_3_0', 'dwd_trade_order_item_df_rebuild_1_3_0')
          AND (name IN ('origin_data', 'sku_order_list', 'logistics_info', 'actual_receive_amount_info', 'json_item_index') OR type LIKE 'JSON%')
    ) != 0,
    'refactored DWD contains raw JSON or child-grain key columns'
);

SELECT throwIf(
    (
        SELECT count()
        FROM youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0 i
        LEFT JOIN youmei_sandbox.dwd_trade_order_df_rebuild_1_3_0 h
          ON i.snapshot_date = h.snapshot_date
         AND i.shop_id = h.shop_id
         AND i.shop_order_id = h.shop_order_id
        WHERE i.snapshot_date = toDate('2026-07-22')
          AND h.shop_order_id IS NULL
    ) != 0,
    'refactored item DWD has missing parent order header'
);

SELECT throwIf(
    (
        SELECT sum(actual_receive_amount)
        FROM youmei_sandbox.dwd_trade_order_df_rebuild_1_3_0
        WHERE snapshot_date = toDate('2026-07-22')
    ) != toDecimal128(6352569.57, 2),
    'refactored order actual receive amount sum mismatch'
);

SELECT throwIf(
    (
        SELECT sum(item_actual_receive_amount)
        FROM youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0
        WHERE snapshot_date = toDate('2026-07-22')
    ) != toDecimal128(6352569.57, 2),
    'refactored item actual receive amount sum mismatch'
);

SELECT throwIf(
    (
        SELECT sum(consumer_paid_receive_amount)
             + sum(platform_discount_receive_amount)
             + sum(talent_discount_receive_amount)
             + sum(third_party_discount_receive_amount)
             + coalesce(sum(service_provider_discount_receive_amount), toDecimal128(0, 2))
             + sum(unknown_receive_amount)
        FROM youmei_sandbox.dwd_trade_order_df_rebuild_1_3_0
        WHERE snapshot_date = toDate('2026-07-22')
    ) != toDecimal128(6352569.57, 2),
    'refactored order receive pivot amount sum mismatch'
);

SELECT throwIf(
    (
        SELECT sum(item_consumer_paid_receive_amount)
             + sum(item_platform_discount_receive_amount)
             + sum(item_talent_discount_receive_amount)
             + sum(item_third_party_discount_receive_amount)
             + coalesce(sum(item_service_provider_discount_receive_amount), toDecimal128(0, 2))
             + sum(item_unknown_receive_amount)
        FROM youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0
        WHERE snapshot_date = toDate('2026-07-22')
    ) != toDecimal128(6352569.57, 2),
    'refactored item receive pivot amount sum mismatch'
);

SELECT
    'DWD_抖店订单主单事实全量快照表重构版(dwd_trade_order_df_rebuild_1_3_0)' AS table_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id)) AS key_count,
    sum(actual_receive_amount) AS actual_receive_amount_sum_yuan,
    sum(unknown_receive_amount) AS unknown_receive_amount_sum_yuan,
    countIf(unknown_receive_type_codes IS NOT NULL) AS unknown_receive_order_count,
    sum(logistics_package_count) AS logistics_package_count
FROM youmei_sandbox.dwd_trade_order_df_rebuild_1_3_0
WHERE snapshot_date = toDate('2026-07-22');

SELECT
    'DWD_抖店订单商品明细事实全量快照表重构版(dwd_trade_order_item_df_rebuild_1_3_0)' AS table_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id, item_index)) AS key_count,
    sum(item_actual_receive_amount) AS item_actual_receive_amount_sum_yuan,
    sum(item_unknown_receive_amount) AS item_unknown_receive_amount_sum_yuan,
    countIf(item_unknown_receive_type_codes IS NOT NULL) AS unknown_receive_item_count
FROM youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0
WHERE snapshot_date = toDate('2026-07-22');
