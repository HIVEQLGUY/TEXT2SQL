SELECT
    table,
    sum(rows) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS disk_on_disk
FROM system.parts
WHERE database = 'youmei_sandbox'
  AND active
  AND table IN ('dwd_trade_order_df', 'dwd_trade_order_item_df')
GROUP BY table
ORDER BY table;

SELECT
    table,
    count() AS column_count
FROM system.columns
WHERE database = 'youmei_sandbox'
  AND table IN ('dwd_trade_order_df', 'dwd_trade_order_item_df')
GROUP BY table
ORDER BY table;

SELECT
    snapshot_date,
    count() AS order_header_rows,
    uniqExact(tuple(shop_id, shop_order_id)) AS order_header_keys,
    sum(paid_amount) AS paid_amount_sum_yuan
FROM youmei_sandbox.dwd_trade_order_df
GROUP BY snapshot_date
ORDER BY snapshot_date;

SELECT
    snapshot_date,
    count() AS order_item_rows,
    uniqExact(tuple(shop_id, shop_order_id, item_index)) AS order_item_keys,
    countIf(room_id IS NULL) AS room_id_null_count,
    countIf(author_id IS NULL) AS author_id_null_count
FROM youmei_sandbox.dwd_trade_order_item_df
GROUP BY snapshot_date
ORDER BY snapshot_date;
