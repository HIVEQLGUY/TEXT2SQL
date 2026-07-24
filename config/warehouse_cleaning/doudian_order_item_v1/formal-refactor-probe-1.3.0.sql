WITH details AS
(
    SELECT DISTINCT
        shop_id,
        order_id,
        toUInt16(item_tuple.2) AS detail_index,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), '') AS type_code,
        if(
            nullIf(trim(JSONExtractRaw(item_tuple.1, 'amount')), '') IS NULL,
            CAST(NULL AS Nullable(Decimal128(2))),
            toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'amount'), 2) / 100
        ) AS amount
    FROM
    (
        SELECT
            shop_id,
            order_id,
            arrayJoin(
                arrayZip(
                    JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(origin_data, 'actual_receive_amount_info'), 'actual_receive_amount_details')),
                    arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(origin_data, 'actual_receive_amount_info'), 'actual_receive_amount_details')))
                )
            ) AS item_tuple
        FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
        WHERE dt = '2026-07-22'
    )
)
SELECT
    '订单主单级商家收入金额明细项' AS scope_name,
    count() AS detail_rows,
    uniqExact(tuple(shop_id, order_id, detail_index)) AS key_count,
    sum(amount) AS total_amount,
    sumIf(amount, type_code = '1') AS type1_amount,
    sumIf(amount, type_code = '2') AS type2_amount,
    sumIf(amount, type_code = '3') AS type3_amount,
    sumIf(amount, type_code = '4') AS type4_amount,
    sumIf(amount, type_code = '5') AS type5_amount,
    sumIf(amount, type_code NOT IN ('1', '2', '3', '4', '5') OR type_code IS NULL) AS unknown_amount,
    arrayStringConcat(arraySort(groupArrayDistinct(type_code)), ',') AS type_codes
FROM details;

WITH source_items AS
(
    SELECT
        shop_id,
        order_id,
        arrayJoin(arrayZip(JSONExtractArrayRaw(sku_order_list), arrayEnumerate(JSONExtractArrayRaw(sku_order_list)))) AS item_tuple
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
), details AS
(
    SELECT DISTINCT
        shop_id,
        order_id,
        toUInt16(item_tuple.2) AS item_index,
        toUInt16(detail_tuple.2) AS detail_index,
        nullIf(replaceAll(JSONExtractRaw(detail_tuple.1, 'type'), '"', ''), '') AS type_code,
        if(
            nullIf(trim(JSONExtractRaw(detail_tuple.1, 'amount')), '') IS NULL,
            CAST(NULL AS Nullable(Decimal128(2))),
            toDecimal128OrNull(JSONExtractRaw(detail_tuple.1, 'amount'), 2) / 100
        ) AS amount
    FROM source_items
    ARRAY JOIN arrayZip(
        JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(item_tuple.1, 'actual_receive_amount_info'), 'actual_receive_amount_details')),
        arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(item_tuple.1, 'actual_receive_amount_info'), 'actual_receive_amount_details')))
    ) AS detail_tuple
)
SELECT
    '商品明细级商家收入金额明细项' AS scope_name,
    count() AS detail_rows,
    uniqExact(tuple(shop_id, order_id, item_index, detail_index)) AS key_count,
    sum(amount) AS total_amount,
    sumIf(amount, type_code = '1') AS type1_amount,
    sumIf(amount, type_code = '2') AS type2_amount,
    sumIf(amount, type_code = '3') AS type3_amount,
    sumIf(amount, type_code = '4') AS type4_amount,
    sumIf(amount, type_code = '5') AS type5_amount,
    sumIf(amount, type_code NOT IN ('1', '2', '3', '4', '5') OR type_code IS NULL) AS unknown_amount,
    arrayStringConcat(arraySort(groupArrayDistinct(type_code)), ',') AS type_codes
FROM details;
