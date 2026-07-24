WITH source_items AS
(
    SELECT
        order_id,
        arrayJoin(arrayZip(JSONExtractArrayRaw(sku_order_list), arrayEnumerate(JSONExtractArrayRaw(sku_order_list)))) AS item_tuple
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE sku_order_list != ''
), normalized AS
(
    SELECT
        order_id,
        toUInt16(item_tuple.2) AS item_index,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'product_id'), '"', ''), '') AS product_id,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'sku_id'), '"', ''), '') AS sku_id,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'room_id'), '"', ''), '') AS room_id,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'author_id'), '"', ''), '') AS author_id,
        toInt64OrNull(JSONExtractRaw(item_tuple.1, 'item_num')) AS item_quantity,
        nullIf(trim(JSONExtractRaw(item_tuple.1, 'goods_price')), '') AS goods_amount_raw,
        nullIf(trim(JSONExtractRaw(item_tuple.1, 'pay_amount')), '') AS item_paid_amount_raw,
        toDecimal64OrNull(JSONExtractRaw(item_tuple.1, 'goods_price'), 2) AS goods_amount_source,
        toDecimal64OrNull(JSONExtractRaw(item_tuple.1, 'pay_amount'), 2) AS item_paid_amount_source
    FROM source_items
)
SELECT
    count() AS expanded_item_count,
    uniqExact(tuple(order_id, item_index)) AS technical_key_count,
    countIf(product_id IS NULL) AS product_id_null_count,
    countIf(sku_id IS NULL) AS sku_id_null_count,
    countIf(item_quantity IS NULL) AS item_quantity_parse_error_count,
    countIf(goods_amount_raw IS NULL) AS goods_amount_empty_count,
    countIf(goods_amount_raw IS NOT NULL AND goods_amount_source IS NULL) AS goods_amount_invalid_count,
    countIf(item_paid_amount_raw IS NULL) AS item_paid_amount_empty_count,
    countIf(item_paid_amount_raw IS NOT NULL AND item_paid_amount_source IS NULL) AS item_paid_amount_invalid_count,
    countIf(room_id IS NULL OR room_id = '0') AS room_id_missing_count,
    countIf(author_id IS NULL OR author_id = '0') AS author_id_missing_count,
    min(goods_amount_source) AS goods_amount_min_yuan,
    max(goods_amount_source) AS goods_amount_max_yuan,
    min(item_paid_amount_source / 100) AS item_paid_amount_min_yuan,
    max(item_paid_amount_source / 100) AS item_paid_amount_max_yuan
FROM normalized;
