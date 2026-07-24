/* Deterministic ClickHouse shadow execution for contract 1.2.0.
   This is not the formal full-field DWD. It materializes the confirmed core
   order-item fields and records the complete JSON contract coverage counts. */

DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_item_shadow_1_2_0;

CREATE TABLE youmei_sandbox.dwd_trade_order_item_shadow_1_2_0
(
    snapshot_date Date,
    shop_id Nullable(String),
    shop_name Nullable(String),
    shop_order_id String,
    item_index UInt16,
    product_id Nullable(String),
    product_name Nullable(String),
    sku_id Nullable(String),
    sku_specification Nullable(String),
    item_quantity Nullable(Int64),
    goods_amount Nullable(Decimal128(2)),
    item_paid_amount Nullable(Decimal128(2)),
    room_id Nullable(String),
    author_id Nullable(String),
    author_name Nullable(String),
    content_id Nullable(String),
    ad_environment_type Nullable(String),
    order_entry_code Nullable(String),
    order_entry_name Nullable(String),
    order_scene_code Nullable(String),
    order_scene_name Nullable(String),
    payment_type_code Nullable(String),
    paid_at Nullable(DateTime('Asia/Shanghai')),
    created_at Nullable(DateTime('Asia/Shanghai')),
    updated_at Nullable(DateTime('Asia/Shanghai')),
    order_status_code Nullable(String),
    order_status_name Nullable(String),
    main_status_code Nullable(String),
    main_status_name Nullable(String),
    documented_json_path_count UInt16,
    documented_scalar_field_count UInt16,
    documented_business_relation_count UInt8,
    json_expansion_status String,
    cleaning_contract_version String,
    source_task_instance_id Nullable(String),
    etl_time DateTime('Asia/Shanghai')
)
ENGINE = MergeTree
PARTITION BY snapshot_date
ORDER BY (snapshot_date, shop_order_id, item_index);

INSERT INTO youmei_sandbox.dwd_trade_order_item_shadow_1_2_0
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
    WHERE dt = '2026-07-21'
), normalized AS
(
    SELECT
        toDate(dt) AS snapshot_date,
        nullIf(trim(shop_id), '') AS shop_id,
        nullIf(trim(shop_name), '') AS shop_name,
        nullIf(trim(order_id), '') AS shop_order_id,
        toUInt16(item_tuple.2) AS item_index,
        coalesce(
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'product_id_str'), '"', ''), ''),
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'product_id'), '"', ''), '')
        ) AS product_id,
        nullIf(JSONExtractString(item_tuple.1, 'product_name'), '') AS product_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'sku_id'), '"', ''), '') AS sku_id,
        arrayStringConcat(
            arrayMap(
                x -> concat(JSONExtractString(x, 'name'), '=', JSONExtractString(x, 'value')),
                JSONExtractArrayRaw(JSONExtractRaw(item_tuple.1, 'spec'))
            ), ';'
        ) AS sku_specification,
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
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'content_id'), '"', ''), '') AS content_id,
        nullIf(JSONExtractString(item_tuple.1, 'ad_env_type'), '') AS ad_environment_type,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'b_type'), '"', ''), '') AS order_entry_code,
        nullIf(JSONExtractString(item_tuple.1, 'b_type_desc'), '') AS order_entry_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'sub_b_type'), '"', ''), '') AS order_scene_code,
        nullIf(JSONExtractString(item_tuple.1, 'sub_b_type_desc'), '') AS order_scene_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'pay_type'), '"', ''), '') AS payment_type_code,
        if(toInt64OrNull(JSONExtractRaw(item_tuple.1, 'pay_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(item_tuple.1, 'pay_time')), 'Asia/Shanghai')) AS paid_at,
        if(toInt64OrNull(JSONExtractRaw(item_tuple.1, 'create_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(item_tuple.1, 'create_time')), 'Asia/Shanghai')) AS created_at,
        if(toInt64OrNull(JSONExtractRaw(item_tuple.1, 'update_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(item_tuple.1, 'update_time')), 'Asia/Shanghai')) AS updated_at,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'order_status'), '"', ''), '') AS order_status_code,
        nullIf(JSONExtractString(item_tuple.1, 'order_status_desc'), '') AS order_status_name,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'main_status'), '"', ''), '') AS main_status_code,
        nullIf(JSONExtractString(item_tuple.1, 'main_status_desc'), '') AS main_status_name,
        yuce_task_instance_id AS source_task_instance_id
    FROM source_items
)
SELECT
    snapshot_date,
    shop_id,
    shop_name,
    shop_order_id,
    item_index,
    product_id,
    product_name,
    sku_id,
    sku_specification,
    item_quantity,
    goods_amount,
    item_paid_amount,
    room_id,
    author_id,
    author_name,
    content_id,
    ad_environment_type,
    order_entry_code,
    order_entry_name,
    order_scene_code,
    order_scene_name,
    payment_type_code,
    paid_at,
    created_at,
    updated_at,
    order_status_code,
    order_status_name,
    main_status_code,
    main_status_name,
    toUInt16(622) AS documented_json_path_count,
    toUInt16(502) AS documented_scalar_field_count,
    toUInt8(51) AS documented_business_relation_count,
    'all_documented_fields_contracted_arrays_relationized' AS json_expansion_status,
    '1.2.0' AS cleaning_contract_version,
    source_task_instance_id,
    now('Asia/Shanghai') AS etl_time
FROM normalized
WHERE shop_order_id IS NOT NULL;
