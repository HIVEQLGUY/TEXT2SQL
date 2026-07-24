SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_df WHERE snapshot_date = toDate('2026-07-22')) != 49695,
    'formal order header DWD row count mismatch'
);

SELECT throwIf(
    (
        SELECT uniqExact(tuple(shop_id, shop_order_id))
        FROM youmei_sandbox.dwd_trade_order_df
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 49695,
    'formal order header DWD composite key is not unique'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_item_df WHERE snapshot_date = toDate('2026-07-22')) != 85770,
    'formal order item DWD row count mismatch'
);

SELECT throwIf(
    (
        SELECT uniqExact(tuple(shop_id, shop_order_id, item_index))
        FROM youmei_sandbox.dwd_trade_order_item_df
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 85770,
    'formal order item DWD composite key is not unique'
);

SELECT throwIf(
    (
        SELECT countIf(product_id IS NULL OR sku_id IS NULL OR item_quantity IS NULL)
        FROM youmei_sandbox.dwd_trade_order_item_df
        WHERE snapshot_date = toDate('2026-07-22')
    ) != 0,
    'formal order item required identifiers or quantity contain NULL'
);

SELECT throwIf(
    (
        SELECT count()
        FROM system.columns
        WHERE database = 'youmei_sandbox'
          AND table IN ('dwd_trade_order_df', 'dwd_trade_order_item_df')
          AND (name = 'sku_order_list' OR type LIKE 'JSON%')
    ) != 0,
    'formal DWD contains raw JSON columns'
);

SELECT throwIf(
    (
        SELECT count()
        FROM youmei_sandbox.dwd_trade_order_item_df i
        LEFT JOIN youmei_sandbox.dwd_trade_order_df h
          ON i.snapshot_date = h.snapshot_date
         AND i.shop_id = h.shop_id
         AND i.shop_order_id = h.shop_order_id
        WHERE i.snapshot_date = toDate('2026-07-22')
          AND h.shop_order_id IS NULL
    ) != 0,
    'formal order item DWD has missing parent order header'
);

SELECT
    'DWD_抖店订单主单事实全量快照表(dwd_trade_order_df)' AS table_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id)) AS key_count,
    min(order_amount) AS order_amount_min_yuan,
    max(order_amount) AS order_amount_max_yuan,
    sum(paid_amount) AS paid_amount_sum_yuan
FROM youmei_sandbox.dwd_trade_order_df
WHERE snapshot_date = toDate('2026-07-22');

SELECT
    'DWD_抖店订单商品明细事实全量快照表(dwd_trade_order_item_df)' AS table_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, shop_order_id, item_index)) AS key_count,
    countIf(room_id IS NULL) AS room_id_null_count,
    countIf(author_id IS NULL) AS author_id_null_count,
    min(goods_amount) AS goods_amount_min_yuan,
    max(goods_amount) AS goods_amount_max_yuan,
    min(item_paid_amount) AS item_paid_amount_min_yuan,
    max(item_paid_amount) AS item_paid_amount_max_yuan
FROM youmei_sandbox.dwd_trade_order_item_df
WHERE snapshot_date = toDate('2026-07-22');
