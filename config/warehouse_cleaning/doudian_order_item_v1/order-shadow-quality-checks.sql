SELECT throwIf(
    (
        SELECT count()
        FROM
        (
            WITH dup AS
            (
                SELECT shop_id, order_id
                FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
                WHERE dt = '2026-07-22'
                GROUP BY shop_id, order_id
                HAVING count() > 1
            )
            SELECT shop_id, order_id
            FROM
            (
                SELECT shop_id, order_id, uniqExact(cityHash64(tuple(*))) AS row_hash_versions
                FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
                INNER JOIN dup USING (shop_id, order_id)
                WHERE dt = '2026-07-22'
                GROUP BY shop_id, order_id
            )
            WHERE row_hash_versions > 1
        )
    ) != 0,
    'source has conflicting duplicated order-header rows'
);

SELECT throwIf(
    (SELECT count() FROM youmei_sandbox.dwd_trade_order_shadow_1_2_0) != 49695,
    'order shadow row count mismatch after deterministic deduplication'
);

SELECT throwIf(
    (
        SELECT uniqExact(tuple(shop_id, shop_order_id))
        FROM youmei_sandbox.dwd_trade_order_shadow_1_2_0
    ) != 49695,
    'order shadow composite key is not unique'
);

SELECT throwIf(
    (
        SELECT countIf(shop_id = '' OR shop_order_id = '')
        FROM youmei_sandbox.dwd_trade_order_shadow_1_2_0
    ) != 0,
    'order shadow required key fields contain empty values'
);

SELECT throwIf(
    (
        SELECT count()
        FROM system.columns
        WHERE database = 'youmei_sandbox'
          AND table = 'dwd_trade_order_shadow_1_2_0'
          AND (name IN ('origin_data', 'sku_order_list') OR type LIKE 'JSON%')
    ) != 0,
    'order shadow contains raw JSON columns'
);

SELECT throwIf(
    (
        SELECT count()
        FROM system.columns
        WHERE database = 'youmei_sandbox'
          AND table = 'dwd_trade_order_shadow_1_2_0'
          AND name IN ('post_receiver', 'post_phone', 'post_address', 'encrypted_post_phone', 'encrypted_post_receiver', 'buyer_words', 'seller_words')
    ) != 7,
    'order shadow expected business contact/address/message columns are missing'
);

SELECT
    count() AS order_shadow_row_count,
    uniqExact(tuple(shop_id, shop_order_id)) AS order_shadow_key_count,
    min(snapshot_date) AS min_snapshot_date,
    max(snapshot_date) AS max_snapshot_date,
    countIf(paid_at IS NULL) AS paid_at_null_count,
    countIf(finished_at IS NULL) AS finished_at_null_count,
    min(order_amount) AS order_amount_min_yuan,
    max(order_amount) AS order_amount_max_yuan,
    min(paid_amount) AS paid_amount_min_yuan,
    max(paid_amount) AS paid_amount_max_yuan,
    sum(paid_amount) AS paid_amount_sum_yuan
FROM youmei_sandbox.dwd_trade_order_shadow_1_2_0;
