DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_1;
DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_logistics_package_df_rebuild_1_3_1;
DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_logistics_package_item_df_rebuild_1_3_1;

CREATE TABLE youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_1 AS youmei_sandbox.dwd_trade_order_item_df;

ALTER TABLE youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_1
    ADD COLUMN IF NOT EXISTS sku_order_id Nullable(String) COMMENT '商品子单号；源自订单商品明细(order_id)，与物流商品信息(sku_order_id)同义统一' AFTER item_index;

INSERT INTO youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_1
(
    snapshot_date,
    shop_id,
    shop_name,
    shop_order_id,
    item_index,
    sku_order_id,
    product_id,
    product_name,
    sku_id,
    sku_specification,
    item_quantity,
    goods_amount,
    item_paid_amount,
    item_actual_receive_amount,
    item_consumer_paid_receive_amount,
    item_platform_discount_receive_amount,
    item_talent_discount_receive_amount,
    item_third_party_discount_receive_amount,
    item_service_provider_discount_receive_amount,
    item_unknown_receive_amount,
    item_unknown_receive_type_codes,
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
    main_status_name
)
WITH item_key_map AS
(
    SELECT DISTINCT
        nullIf(trim(shop_id), '') AS shop_id,
        nullIf(trim(order_id), '') AS shop_order_id,
        toUInt16(item_tuple.2) AS item_index,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'order_id'), '"', ''), '') AS sku_order_id
    FROM
    (
        SELECT
            shop_id,
            order_id,
            arrayJoin(arrayZip(JSONExtractArrayRaw(sku_order_list), arrayEnumerate(JSONExtractArrayRaw(sku_order_list)))) AS item_tuple
        FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
        WHERE dt = '2026-07-22'
    )
)
SELECT
    i.snapshot_date,
    i.shop_id,
    i.shop_name,
    i.shop_order_id,
    i.item_index,
    m.sku_order_id,
    i.product_id,
    i.product_name,
    i.sku_id,
    i.sku_specification,
    i.item_quantity,
    i.goods_amount,
    i.item_paid_amount,
    i.item_actual_receive_amount,
    i.item_consumer_paid_receive_amount,
    i.item_platform_discount_receive_amount,
    i.item_talent_discount_receive_amount,
    i.item_third_party_discount_receive_amount,
    i.item_service_provider_discount_receive_amount,
    i.item_unknown_receive_amount,
    i.item_unknown_receive_type_codes,
    i.room_id,
    i.author_id,
    i.author_name,
    i.content_id,
    i.ad_environment_type,
    i.order_entry_code,
    i.order_entry_name,
    i.order_scene_code,
    i.order_scene_name,
    i.payment_type_code,
    i.paid_at,
    i.created_at,
    i.updated_at,
    i.order_status_code,
    i.order_status_name,
    i.main_status_code,
    i.main_status_name
FROM youmei_sandbox.dwd_trade_order_item_df i
LEFT JOIN item_key_map m
  ON i.shop_id = m.shop_id
 AND i.shop_order_id = m.shop_order_id
 AND i.item_index = m.item_index;

CREATE TABLE youmei_sandbox.dwd_trade_order_logistics_package_df_rebuild_1_3_1
(
    snapshot_date Date COMMENT '数据快照日期',
    shop_id String COMMENT '店铺ID',
    shop_name Nullable(String) COMMENT '店铺名称',
    shop_order_id String COMMENT '店铺订单号',
    package_index UInt16 COMMENT '物流包裹序号，源logistics_info数组位置',
    package_id String COMMENT '包裹ID，源logistics_info.delivery_id',
    tracking_no Nullable(String) COMMENT '快递单号，源logistics_info.tracking_no',
    logistics_company_code Nullable(String) COMMENT '物流公司编码',
    logistics_company_name Nullable(String) COMMENT '物流公司名称',
    shipped_at Nullable(DateTime('Asia/Shanghai')) COMMENT '发货时间',
    package_sku_order_count UInt16 COMMENT '包裹内商品子单数',
    guarantee_amount Nullable(Decimal128(2)) COMMENT '物流保价金额，源单位分，清洗后单位元',
    platform_delivery_discount_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送优惠金额，源单位分，清洗后单位元',
    platform_delivery_paid_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送实付金额，源单位分，清洗后单位元',
    platform_delivery_payable_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送应付金额，源单位分，清洗后单位元',
    hour_up_pickup_code Nullable(String) COMMENT '骑手取件码',
    reverse_tracking_no Nullable(String) COMMENT '逆向快递单号',
    reverse_logistics_company_code Nullable(String) COMMENT '逆向物流公司编码',
    reverse_logistics_company_name Nullable(String) COMMENT '逆向物流公司名称',
    transit_merge_type_code Nullable(String) COMMENT '合单包裹类型编码',
    transit_merge_type_name Nullable(String) COMMENT '合单包裹类型名称'
)
ENGINE = MergeTree
PARTITION BY snapshot_date
ORDER BY (snapshot_date, shop_id, shop_order_id, package_id, package_index);

INSERT INTO youmei_sandbox.dwd_trade_order_logistics_package_df_rebuild_1_3_1
WITH package_rows AS
(
    SELECT DISTINCT
        toDate(dt) AS snapshot_date,
        nullIf(trim(shop_id), '') AS shop_id,
        nullIf(trim(shop_name), '') AS shop_name,
        nullIf(trim(order_id), '') AS shop_order_id,
        toUInt16(pkg_tuple.2) AS package_index,
        nullIf(JSONExtractString(pkg_tuple.1, 'delivery_id'), '') AS package_id,
        nullIf(JSONExtractString(pkg_tuple.1, 'tracking_no'), '') AS tracking_no,
        nullIf(JSONExtractString(pkg_tuple.1, 'company'), '') AS logistics_company_code,
        nullIf(JSONExtractString(pkg_tuple.1, 'company_name'), '') AS logistics_company_name,
        if(toInt64OrNull(JSONExtractRaw(pkg_tuple.1, 'ship_time')) IS NULL OR toInt64OrZero(JSONExtractRaw(pkg_tuple.1, 'ship_time')) = 0, NULL, toDateTime(toInt64OrZero(JSONExtractRaw(pkg_tuple.1, 'ship_time')), 'Asia/Shanghai')) AS shipped_at,
        if(nullIf(trim(JSONExtractRaw(pkg_tuple.1, 'guarantee_amount')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(pkg_tuple.1, 'guarantee_amount'), 2) / 100) AS guarantee_amount,
        if(nullIf(trim(JSONExtractRaw(pkg_tuple.1, 'sp_discount_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(pkg_tuple.1, 'sp_discount_price'), 2) / 100) AS platform_delivery_discount_amount,
        if(nullIf(trim(JSONExtractRaw(pkg_tuple.1, 'sp_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(pkg_tuple.1, 'sp_price'), 2) / 100) AS platform_delivery_paid_amount,
        if(nullIf(trim(JSONExtractRaw(pkg_tuple.1, 'sp_total_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(pkg_tuple.1, 'sp_total_price'), 2) / 100) AS platform_delivery_payable_amount,
        nullIf(JSONExtractString(pkg_tuple.1, 'hour_up_pickup_code'), '') AS hour_up_pickup_code,
        nullIf(JSONExtractString(JSONExtractRaw(pkg_tuple.1, 'reverse_express_info'), 'logistics_code'), '') AS reverse_tracking_no,
        nullIf(JSONExtractString(JSONExtractRaw(pkg_tuple.1, 'reverse_express_info'), 'logistics_company'), '') AS reverse_logistics_company_code,
        nullIf(JSONExtractString(JSONExtractRaw(pkg_tuple.1, 'reverse_express_info'), 'logistics_company_name'), '') AS reverse_logistics_company_name,
        nullIf(JSONExtractString(pkg_tuple.1, 'transit_merge_type'), '') AS transit_merge_type_code,
        multiIf(
            nullIf(JSONExtractString(pkg_tuple.1, 'transit_merge_type'), '') = 'merge', '合包',
            nullIf(JSONExtractString(pkg_tuple.1, 'transit_merge_type'), '') = 'single', '非合包',
            nullIf(JSONExtractString(pkg_tuple.1, 'transit_merge_type'), '') IS NULL, NULL,
            concat('未知类型:', nullIf(JSONExtractString(pkg_tuple.1, 'transit_merge_type'), ''))
        ) AS transit_merge_type_name,
        pkg_tuple.1 AS package_json
    FROM
    (
        SELECT
            dt,
            shop_id,
            shop_name,
            order_id,
            arrayJoin(arrayZip(JSONExtractArrayRaw(logistics_info), arrayEnumerate(JSONExtractArrayRaw(logistics_info)))) AS pkg_tuple
        FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
        WHERE dt = '2026-07-22'
    )
), package_counts AS
(
    SELECT
        shop_id,
        shop_order_id,
        package_id,
        toUInt16(uniqExact(nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_order_id'), '"', ''), ''))) AS package_sku_order_count
    FROM package_rows
    ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
    GROUP BY shop_id, shop_order_id, package_id
)
SELECT
    p.snapshot_date,
    p.shop_id,
    p.shop_name,
    p.shop_order_id,
    p.package_index,
    p.package_id,
    p.tracking_no,
    p.logistics_company_code,
    p.logistics_company_name,
    p.shipped_at,
    coalesce(c.package_sku_order_count, toUInt16(0)) AS package_sku_order_count,
    p.guarantee_amount,
    p.platform_delivery_discount_amount,
    p.platform_delivery_paid_amount,
    p.platform_delivery_payable_amount,
    p.hour_up_pickup_code,
    p.reverse_tracking_no,
    p.reverse_logistics_company_code,
    p.reverse_logistics_company_name,
    p.transit_merge_type_code,
    p.transit_merge_type_name
FROM package_rows p
LEFT JOIN package_counts c
  ON p.shop_id = c.shop_id
 AND p.shop_order_id = c.shop_order_id
 AND p.package_id = c.package_id
WHERE p.shop_id IS NOT NULL
  AND p.shop_order_id IS NOT NULL
  AND p.package_id IS NOT NULL;

CREATE TABLE youmei_sandbox.dwd_trade_order_logistics_package_item_df_rebuild_1_3_1
(
    snapshot_date Date COMMENT '数据快照日期',
    shop_id String COMMENT '店铺ID',
    shop_name Nullable(String) COMMENT '店铺名称',
    shop_order_id String COMMENT '店铺订单号',
    package_id String COMMENT '包裹ID',
    tracking_no Nullable(String) COMMENT '快递单号',
    package_index UInt16 COMMENT '物流包裹序号，源logistics_info数组位置',
    package_product_index UInt16 COMMENT '包裹商品序号，源product_info数组位置',
    sku_order_id String COMMENT '商品子单号；源物流商品信息product_info.sku_order_id',
    product_id Nullable(String) COMMENT '商品ID',
    product_name Nullable(String) COMMENT '商品名称',
    sku_id Nullable(String) COMMENT 'SKU ID',
    sku_specification Nullable(String) COMMENT 'SKU规格，已展开为名称和值',
    outer_sku_id Nullable(String) COMMENT '外部SKU ID',
    shipped_product_count Nullable(Int64) COMMENT '包裹内该商品子单发货数量',
    product_price_amount Nullable(Decimal128(2)) COMMENT '包裹商品单价，源单位分，清洗后单位元',
    logistics_company_code Nullable(String) COMMENT '物流公司编码',
    logistics_company_name Nullable(String) COMMENT '物流公司名称',
    shipped_at Nullable(DateTime('Asia/Shanghai')) COMMENT '发货时间'
)
ENGINE = MergeTree
PARTITION BY snapshot_date
ORDER BY (snapshot_date, shop_id, shop_order_id, package_id, sku_order_id, package_product_index);

INSERT INTO youmei_sandbox.dwd_trade_order_logistics_package_item_df_rebuild_1_3_1
WITH package_rows AS
(
    SELECT DISTINCT
        toDate(dt) AS snapshot_date,
        nullIf(trim(shop_id), '') AS shop_id,
        nullIf(trim(shop_name), '') AS shop_name,
        nullIf(trim(order_id), '') AS shop_order_id,
        toUInt16(pkg_tuple.2) AS package_index,
        nullIf(JSONExtractString(pkg_tuple.1, 'delivery_id'), '') AS package_id,
        nullIf(JSONExtractString(pkg_tuple.1, 'tracking_no'), '') AS tracking_no,
        nullIf(JSONExtractString(pkg_tuple.1, 'company'), '') AS logistics_company_code,
        nullIf(JSONExtractString(pkg_tuple.1, 'company_name'), '') AS logistics_company_name,
        if(toInt64OrNull(JSONExtractRaw(pkg_tuple.1, 'ship_time')) IS NULL OR toInt64OrZero(JSONExtractRaw(pkg_tuple.1, 'ship_time')) = 0, NULL, toDateTime(toInt64OrZero(JSONExtractRaw(pkg_tuple.1, 'ship_time')), 'Asia/Shanghai')) AS shipped_at,
        pkg_tuple.1 AS package_json
    FROM
    (
        SELECT
            dt,
            shop_id,
            shop_name,
            order_id,
            arrayJoin(arrayZip(JSONExtractArrayRaw(logistics_info), arrayEnumerate(JSONExtractArrayRaw(logistics_info)))) AS pkg_tuple
        FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
        WHERE dt = '2026-07-22'
    )
), normalized AS
(
    SELECT DISTINCT
        p.snapshot_date,
        p.shop_id,
        p.shop_name,
        p.shop_order_id,
        p.package_id,
        p.tracking_no,
        p.package_index,
        toUInt16(product_tuple.2) AS package_product_index,
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_order_id'), '"', ''), '') AS sku_order_id,
        coalesce(
            nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'product_id_str'), '"', ''), ''),
            nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'product_id'), '"', ''), '')
        ) AS product_id,
        nullIf(JSONExtractString(product_tuple.1, 'product_name'), '') AS product_name,
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_id'), '"', ''), '') AS sku_id,
        arrayStringConcat(arrayMap(x -> concat(JSONExtractString(x, 'name'), '=', JSONExtractString(x, 'value')), JSONExtractArrayRaw(JSONExtractRaw(product_tuple.1, 'sku_specs'))), ';') AS sku_specification,
        nullIf(JSONExtractString(product_tuple.1, 'outer_sku_id'), '') AS outer_sku_id,
        toInt64OrNull(JSONExtractRaw(product_tuple.1, 'product_count')) AS shipped_product_count,
        if(nullIf(trim(JSONExtractRaw(product_tuple.1, 'price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(product_tuple.1, 'price'), 2) / 100) AS product_price_amount,
        p.logistics_company_code,
        p.logistics_company_name,
        p.shipped_at
    FROM package_rows p
    ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
)
SELECT *
FROM normalized
WHERE shop_id IS NOT NULL
  AND shop_order_id IS NOT NULL
  AND package_id IS NOT NULL
  AND sku_order_id IS NOT NULL;
