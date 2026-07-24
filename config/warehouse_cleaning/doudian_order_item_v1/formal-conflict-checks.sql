WITH normalized AS
(
    SELECT
        toDate(dt) AS snapshot_date,
        nullIf(trim(shop_id), '') AS shop_id,
        nullIf(trim(order_id), '') AS shop_order_id,
        nullIf(trim(shop_name), '') AS shop_name,
        nullIf(trim(order_status), '') AS order_status_code,
        nullIf(trim(order_status_desc), '') AS order_status_name,
        nullIf(trim(main_status), '') AS main_status_code,
        nullIf(trim(main_status_desc), '') AS main_status_name,
        nullIf(trim(pay_type), '') AS payment_type_code,
        if(toInt64OrNull(nullIf(pay_time, '')) IS NULL OR toInt64OrZero(pay_time) = 0, NULL, toDateTime(toInt64OrZero(pay_time), 'Asia/Shanghai')) AS paid_at,
        if(toInt64OrNull(nullIf(create_time, '')) IS NULL OR toInt64OrZero(create_time) = 0, NULL, toDateTime(toInt64OrZero(create_time), 'Asia/Shanghai')) AS created_at,
        if(nullIf(trim(pay_amount), '') IS NULL, NULL, toDecimal128OrNull(pay_amount, 2) / 100) AS paid_amount
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
)
SELECT throwIf(
    (
        SELECT count()
        FROM
        (
            SELECT
                shop_id,
                shop_order_id,
                countDistinct(cityHash64(toString(tuple(
                    snapshot_date,
                    shop_name,
                    order_status_code,
                    order_status_name,
                    main_status_code,
                    main_status_name,
                    payment_type_code,
                    paid_at,
                    created_at,
                    paid_amount
                )))) AS content_versions
            FROM normalized
            GROUP BY shop_id, shop_order_id
            HAVING content_versions > 1
        )
    ) != 0,
    'formal order header has conflicting duplicate business keys'
);

WITH source_items AS
(
    SELECT
        dt,
        shop_id,
        shop_name,
        order_id,
        arrayJoin(arrayZip(JSONExtractArrayRaw(sku_order_list), arrayEnumerate(JSONExtractArrayRaw(sku_order_list)))) AS item_tuple
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
), normalized AS
(
    SELECT
        toDate(dt) AS snapshot_date,
        nullIf(trim(shop_id), '') AS shop_id,
        nullIf(trim(order_id), '') AS shop_order_id,
        toUInt16(item_tuple.2) AS item_index,
        coalesce(
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'product_id_str'), '"', ''), ''),
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'product_id'), '"', ''), '')
        ) AS product_id,
        nullIf(JSONExtractString(item_tuple.1, 'product_name'), '') AS product_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'sku_id'), '"', ''), '') AS sku_id,
        toInt64OrNull(JSONExtractRaw(item_tuple.1, 'item_num')) AS item_quantity,
        toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'goods_price'), 2) AS goods_amount,
        if(
            nullIf(trim(JSONExtractRaw(item_tuple.1, 'pay_amount')), '') IS NULL,
            CAST(NULL AS Nullable(Decimal128(2))),
            toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'pay_amount'), 2) / 100
        ) AS item_paid_amount,
        nullIf(nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'room_id_str'), '"', ''), ''), '0') AS room_id,
        nullIf(nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'author_id'), '"', ''), ''), '0') AS author_id,
        nullIf(JSONExtractString(item_tuple.1, 'author_name'), '') AS author_name,
        if(toInt64OrNull(JSONExtractRaw(item_tuple.1, 'pay_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(item_tuple.1, 'pay_time')), 'Asia/Shanghai')) AS paid_at
    FROM source_items
)
SELECT throwIf(
    (
        SELECT count()
        FROM
        (
            SELECT
                shop_id,
                shop_order_id,
                item_index,
                countDistinct(cityHash64(toString(tuple(
                    snapshot_date,
                    product_id,
                    product_name,
                    sku_id,
                    item_quantity,
                    goods_amount,
                    item_paid_amount,
                    room_id,
                    author_id,
                    author_name,
                    paid_at
                )))) AS content_versions
            FROM normalized
            GROUP BY shop_id, shop_order_id, item_index
            HAVING content_versions > 1
        )
    ) != 0,
    'formal order item has conflicting duplicate business keys'
);

WITH source_items AS
(
    SELECT
        shop_id,
        order_id,
        arrayJoin(arrayEnumerate(JSONExtractArrayRaw(sku_order_list))) AS item_index
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
)
SELECT
    count() AS item_source_rows,
    uniqExact(tuple(shop_id, order_id, item_index)) AS item_unique_keys,
    count() - uniqExact(tuple(shop_id, order_id, item_index)) AS duplicate_item_rows
FROM source_items;
