/* REVIEW ONLY: focused shadow sample. Full-field output is generated from
   json-field-contracts.yaml and json-relation-contracts.yaml after approval. */
WITH source_items AS
(
    SELECT
        dt,
        shop_id,
        shop_name,
        order_id,
        yuce_task_instance_id,
        arrayJoin(arrayZip(JSONExtractArrayRaw(sku_order_list), arrayEnumerate(JSONExtractArrayRaw(sku_order_list)))) AS item_tuple
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = {snapshot_date:String}
), normalized AS
(
    SELECT
        toDate(dt) AS snapshot_date,
        nullIf(trim(shop_id), '') AS shop_id,
        trim(shop_name) AS shop_name,
        nullIf(trim(order_id), '') AS shop_order_id,
        toUInt16(item_tuple.2) AS item_index,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'product_id_str'), '"', ''), '') AS product_id,
        nullIf(JSONExtractString(item_tuple.1, 'product_name'), '') AS product_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'sku_id'), '"', ''), '') AS sku_id,
        arrayStringConcat(arrayMap(x -> concat(JSONExtractString(x, 'name'), '=', JSONExtractString(x, 'value')), JSONExtractArrayRaw(JSONExtractRaw(item_tuple.1, 'spec'))), ';') AS sku_specification,
        toInt64OrNull(JSONExtractRaw(item_tuple.1, 'item_num')) AS item_quantity,
        /* User-confirmed unit: yuan. Preserve the value and standardize scale. */
        toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'goods_price'), 2) AS goods_amount,
        /* pay_amount is explicitly documented as fen; empty stays NULL, invalid values are counted by quality SQL. */
        if(
            nullIf(trim(JSONExtractRaw(item_tuple.1, 'pay_amount')), '') IS NULL,
            CAST(NULL AS Nullable(Decimal128(2))),
            toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'pay_amount'), 2) / 100
        ) AS item_paid_amount,
        nullIf(nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'room_id_str'), '"', ''), ''), '0') AS room_id,
        nullIf(nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'author_id'), '"', ''), ''), '0') AS author_id,
        nullIf(JSONExtractString(item_tuple.1, 'author_name'), '') AS author_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'content_id'), '"', ''), '') AS content_id,
        nullIf(JSONExtractString(item_tuple.1, 'ad_env_type'), '') AS ad_environment_type,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'b_type'), '"', ''), '') AS order_entry_code,
        nullIf(JSONExtractString(item_tuple.1, 'b_type_desc'), '') AS order_entry_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'sub_b_type'), '"', ''), '') AS order_scene_code,
        nullIf(JSONExtractString(item_tuple.1, 'sub_b_type_desc'), '') AS order_scene_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'pay_type'), '"', ''), '') AS payment_type_code,
        if(toInt64OrNull(JSONExtractRaw(item_tuple.1, 'pay_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(item_tuple.1, 'pay_time')), 'Asia/Shanghai')) AS paid_at,
        toDateTime(toInt64OrZero(JSONExtractRaw(item_tuple.1, 'create_time')), 'Asia/Shanghai') AS created_at,
        toDateTime(toInt64OrZero(JSONExtractRaw(item_tuple.1, 'update_time')), 'Asia/Shanghai') AS updated_at,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'order_status'), '"', ''), '') AS order_status_code,
        nullIf(JSONExtractString(item_tuple.1, 'order_status_desc'), '') AS order_status_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'main_status'), '"', ''), '') AS main_status_code,
        nullIf(JSONExtractString(item_tuple.1, 'main_status_desc'), '') AS main_status_name,
        toUInt8(if(replaceAll(JSONExtractRaw(item_tuple.1, 'room_id_str'), '"', '') IN ('', '0'), 1, 0)) AS room_attribution_quality_code,
        toUInt8(if(replaceAll(JSONExtractRaw(item_tuple.1, 'author_id'), '"', '') IN ('', '0'), 1, 0)) AS author_attribution_quality_code,
        '1.2.0' AS cleaning_contract_version,
        yuce_task_instance_id AS source_task_instance_id,
        now('Asia/Shanghai') AS etl_time
    FROM source_items
)
SELECT * FROM normalized;
