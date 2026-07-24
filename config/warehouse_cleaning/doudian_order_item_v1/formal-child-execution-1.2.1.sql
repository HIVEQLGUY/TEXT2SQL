CREATE TABLE IF NOT EXISTS youmei_sandbox.dwd_json_actual_receive_amount_info_actual_receive_amount_details_df
(
    snapshot_date Date COMMENT '数据快照日期',
    shop_id String COMMENT '店铺ID',
    shop_name Nullable(String) COMMENT '店铺名称',
    shop_order_id String COMMENT '店铺订单号',
    json_item_index UInt16 COMMENT '商家收入金额明细项序号，源JSON数组位置',
    amount_detail_type_code Nullable(String) COMMENT '商家收入金额明细项类型编码',
    amount_detail_type_name Nullable(String) COMMENT '商家收入金额明细项类型名称，未知编码保留编码并标记未知',
    amount Nullable(Decimal128(2)) COMMENT '商家收入明细项金额，源单位分，清洗后单位元'
)
ENGINE = MergeTree
PARTITION BY snapshot_date
ORDER BY (snapshot_date, shop_id, shop_order_id, json_item_index);

CREATE TABLE IF NOT EXISTS youmei_sandbox.dwd_json_logistics_info_df
(
    snapshot_date Date COMMENT '数据快照日期',
    shop_id String COMMENT '店铺ID',
    shop_name Nullable(String) COMMENT '店铺名称',
    shop_order_id String COMMENT '店铺订单号',
    json_item_index UInt16 COMMENT '物流信息序号，源JSON数组位置',
    logistics_company_code Nullable(String) COMMENT '物流公司编码',
    logistics_company_name Nullable(String) COMMENT '物流公司名称',
    package_id Nullable(String) COMMENT '包裹ID',
    tracking_no Nullable(String) COMMENT '物流单号',
    shipped_at Nullable(DateTime('Asia/Shanghai')) COMMENT '发货时间',
    guarantee_amount Nullable(Decimal128(2)) COMMENT '小时达订单保价金额，源单位分，清洗后单位元',
    platform_delivery_discount_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送优惠金额，源单位分，清洗后单位元',
    platform_delivery_paid_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送实付金额，源单位分，清洗后单位元',
    platform_delivery_payable_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送应付金额，源单位分，清洗后单位元',
    hour_up_pickup_code Nullable(String) COMMENT '骑手取件码',
    reverse_tracking_no Nullable(String) COMMENT '逆向物流单号',
    reverse_logistics_company_code Nullable(String) COMMENT '逆向物流公司编码',
    reverse_logistics_company_name Nullable(String) COMMENT '逆向物流公司名称',
    transit_merge_type_code Nullable(String) COMMENT '合单包裹类型编码',
    transit_merge_type_name Nullable(String) COMMENT '合单包裹类型名称'
)
ENGINE = MergeTree
PARTITION BY snapshot_date
ORDER BY (snapshot_date, shop_id, shop_order_id, json_item_index);

INSERT INTO youmei_sandbox.dwd_json_actual_receive_amount_info_actual_receive_amount_details_df
WITH source_details AS
(
    SELECT
        dt,
        shop_id,
        shop_name,
        order_id,
        arrayJoin(
            arrayZip(
                JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(origin_data, 'actual_receive_amount_info'), 'actual_receive_amount_details')),
                arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(origin_data, 'actual_receive_amount_info'), 'actual_receive_amount_details')))
            )
        ) AS item_tuple
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
), normalized AS
(
    SELECT DISTINCT
        toDate(dt) AS snapshot_date,
        nullIf(trim(shop_id), '') AS shop_id,
        nullIf(trim(shop_name), '') AS shop_name,
        nullIf(trim(order_id), '') AS shop_order_id,
        toUInt16(item_tuple.2) AS json_item_index,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), '') AS amount_detail_type_code,
        multiIf(
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), '') = '1', '消费者实付金额',
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), '') = '2', '平台承担优惠金额',
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), '') = '3', '达人承担优惠金额',
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), '') = '4', '三方平台承担优惠金额',
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), '') = '5', '服务商承担优惠金额',
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), '') IS NULL, NULL,
            concat('未知类型:', nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), ''))
        ) AS amount_detail_type_name,
        if(
            nullIf(trim(JSONExtractRaw(item_tuple.1, 'amount')), '') IS NULL,
            CAST(NULL AS Nullable(Decimal128(2))),
            toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'amount'), 2) / 100
        ) AS amount
    FROM source_details
)
SELECT *
FROM normalized
WHERE shop_id IS NOT NULL
  AND shop_order_id IS NOT NULL
  AND (SELECT count() FROM youmei_sandbox.dwd_json_actual_receive_amount_info_actual_receive_amount_details_df WHERE snapshot_date = toDate('2026-07-22')) = 0;

INSERT INTO youmei_sandbox.dwd_json_logistics_info_df
WITH source_details AS
(
    SELECT
        dt,
        shop_id,
        shop_name,
        order_id,
        arrayJoin(
            arrayZip(
                JSONExtractArrayRaw(logistics_info),
                arrayEnumerate(JSONExtractArrayRaw(logistics_info))
            )
        ) AS item_tuple
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
), normalized AS
(
    SELECT DISTINCT
        toDate(dt) AS snapshot_date,
        nullIf(trim(shop_id), '') AS shop_id,
        nullIf(trim(shop_name), '') AS shop_name,
        nullIf(trim(order_id), '') AS shop_order_id,
        toUInt16(item_tuple.2) AS json_item_index,
        nullIf(JSONExtractString(item_tuple.1, 'company'), '') AS logistics_company_code,
        nullIf(JSONExtractString(item_tuple.1, 'company_name'), '') AS logistics_company_name,
        nullIf(JSONExtractString(item_tuple.1, 'delivery_id'), '') AS package_id,
        nullIf(JSONExtractString(item_tuple.1, 'tracking_no'), '') AS tracking_no,
        if(toInt64OrNull(JSONExtractRaw(item_tuple.1, 'ship_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(item_tuple.1, 'ship_time')), 'Asia/Shanghai')) AS shipped_at,
        if(nullIf(trim(JSONExtractRaw(item_tuple.1, 'guarantee_amount')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'guarantee_amount'), 2) / 100) AS guarantee_amount,
        if(nullIf(trim(JSONExtractRaw(item_tuple.1, 'sp_discount_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'sp_discount_price'), 2) / 100) AS platform_delivery_discount_amount,
        if(nullIf(trim(JSONExtractRaw(item_tuple.1, 'sp_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'sp_price'), 2) / 100) AS platform_delivery_paid_amount,
        if(nullIf(trim(JSONExtractRaw(item_tuple.1, 'sp_total_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'sp_total_price'), 2) / 100) AS platform_delivery_payable_amount,
        nullIf(JSONExtractString(item_tuple.1, 'hour_up_pickup_code'), '') AS hour_up_pickup_code,
        nullIf(JSONExtractString(JSONExtractRaw(item_tuple.1, 'reverse_express_info'), 'logistics_code'), '') AS reverse_tracking_no,
        nullIf(JSONExtractString(JSONExtractRaw(item_tuple.1, 'reverse_express_info'), 'logistics_company'), '') AS reverse_logistics_company_code,
        nullIf(JSONExtractString(JSONExtractRaw(item_tuple.1, 'reverse_express_info'), 'logistics_company_name'), '') AS reverse_logistics_company_name,
        nullIf(JSONExtractString(item_tuple.1, 'transit_merge_type'), '') AS transit_merge_type_code,
        multiIf(
            nullIf(JSONExtractString(item_tuple.1, 'transit_merge_type'), '') = 'merge', '合包',
            nullIf(JSONExtractString(item_tuple.1, 'transit_merge_type'), '') = 'single', '非合包',
            nullIf(JSONExtractString(item_tuple.1, 'transit_merge_type'), '') IS NULL, NULL,
            concat('未知类型:', nullIf(JSONExtractString(item_tuple.1, 'transit_merge_type'), ''))
        ) AS transit_merge_type_name
    FROM source_details
)
SELECT *
FROM normalized
WHERE shop_id IS NOT NULL
  AND shop_order_id IS NOT NULL
  AND (SELECT count() FROM youmei_sandbox.dwd_json_logistics_info_df WHERE snapshot_date = toDate('2026-07-22')) = 0;
