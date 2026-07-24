DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3__candidate__1_3_3;

CREATE TABLE youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3__candidate__1_3_3
(
    snapshot_date Date COMMENT '数据快照日期',
    shop_id String COMMENT '店铺ID',
    shop_name Nullable(String) COMMENT '店铺名称',
    shop_order_id String COMMENT '店铺订单号',
    tracking_no String COMMENT '快递单号；用于后续运费匹配',
    logistics_company_names Nullable(String) COMMENT '物流公司名称列表，按快递单号粒度去重拼接',
    first_shipped_at Nullable(DateTime('Asia/Shanghai')) COMMENT '最早发货时间',
    latest_shipped_at Nullable(DateTime('Asia/Shanghai')) COMMENT '最晚发货时间',
    package_count UInt16 COMMENT '快递单号下源包裹记录数；包裹ID不作为业务粒度，仅用于汇总计数',
    package_product_row_count UInt32 COMMENT '快递单号下物流商品关系行数',
    sku_order_count UInt32 COMMENT '快递单号下商品子单数',
    sku_order_ids Nullable(String) COMMENT '商品子单号列表，按快递单号粒度去重拼接',
    shipped_product_count Nullable(Int64) COMMENT '发货商品数量合计',
    guarantee_amount Nullable(Decimal128(2)) COMMENT '物流保价金额合计，源单位分，清洗后单位元',
    platform_delivery_discount_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送优惠金额合计，源单位分，清洗后单位元',
    platform_delivery_paid_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送实付金额合计，源单位分，清洗后单位元',
    platform_delivery_payable_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送应付金额合计，源单位分，清洗后单位元',
    avg_product_price_amount Nullable(Decimal128(2)) COMMENT '物流商品单价平均值，源单位分，清洗后单位元；平均型指标按快递单号粒度取平均'
)
ENGINE = MergeTree
PARTITION BY snapshot_date
ORDER BY (snapshot_date, shop_id, shop_order_id, tracking_no);

INSERT INTO youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3__candidate__1_3_3
WITH package_rows AS
(
    SELECT DISTINCT
        toDate(dt) AS snapshot_date,
        nullIf(trim(shop_id), '') AS shop_id,
        nullIf(trim(shop_name), '') AS shop_name,
        nullIf(trim(order_id), '') AS shop_order_id,
        toUInt16(pkg_tuple.2) AS package_index,
        nullIf(JSONExtractString(pkg_tuple.1, 'tracking_no'), '') AS tracking_no,
        nullIf(JSONExtractString(pkg_tuple.1, 'company_name'), '') AS logistics_company_name,
        if(toInt64OrNull(JSONExtractRaw(pkg_tuple.1, 'ship_time')) IS NULL OR toInt64OrZero(JSONExtractRaw(pkg_tuple.1, 'ship_time')) = 0, NULL, toDateTime(toInt64OrZero(JSONExtractRaw(pkg_tuple.1, 'ship_time')), 'Asia/Shanghai')) AS shipped_at,
        if(nullIf(trim(JSONExtractRaw(pkg_tuple.1, 'guarantee_amount')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(pkg_tuple.1, 'guarantee_amount'), 2) / 100) AS guarantee_amount,
        if(nullIf(trim(JSONExtractRaw(pkg_tuple.1, 'sp_discount_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(pkg_tuple.1, 'sp_discount_price'), 2) / 100) AS platform_delivery_discount_amount,
        if(nullIf(trim(JSONExtractRaw(pkg_tuple.1, 'sp_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(pkg_tuple.1, 'sp_price'), 2) / 100) AS platform_delivery_paid_amount,
        if(nullIf(trim(JSONExtractRaw(pkg_tuple.1, 'sp_total_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(pkg_tuple.1, 'sp_total_price'), 2) / 100) AS platform_delivery_payable_amount,
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
        WHERE dt = '2026-07-23'
    )
), tracking_rollup AS
(
    SELECT
        snapshot_date,
        shop_id,
        any(shop_name) AS shop_name,
        shop_order_id,
        tracking_no,
        nullIf(arrayStringConcat(arraySort(groupUniqArrayIf(assumeNotNull(logistics_company_name), logistics_company_name IS NOT NULL)), ','), '') AS logistics_company_names,
        min(shipped_at) AS first_shipped_at,
        max(shipped_at) AS latest_shipped_at,
        toUInt16(count()) AS package_count,
        sum(guarantee_amount) AS guarantee_amount,
        sum(platform_delivery_discount_amount) AS platform_delivery_discount_amount,
        sum(platform_delivery_paid_amount) AS platform_delivery_paid_amount,
        sum(platform_delivery_payable_amount) AS platform_delivery_payable_amount
    FROM package_rows
    WHERE shop_id IS NOT NULL
      AND shop_order_id IS NOT NULL
      AND tracking_no IS NOT NULL
    GROUP BY snapshot_date, shop_id, shop_order_id, tracking_no
), product_rollup AS
(
    SELECT
        snapshot_date,
        shop_id,
        shop_order_id,
        tracking_no,
        toUInt32(count()) AS package_product_row_count,
        toUInt32(uniqExact(sku_order_id)) AS sku_order_count,
        nullIf(arrayStringConcat(arraySort(groupUniqArrayIf(assumeNotNull(sku_order_id), sku_order_id IS NOT NULL)), ','), '') AS sku_order_ids,
        sum(shipped_product_count) AS shipped_product_count,
        avg(product_price_amount) AS avg_product_price_amount
    FROM
    (
        SELECT DISTINCT
            p.snapshot_date,
            p.shop_id,
            p.shop_order_id,
            p.tracking_no,
            toUInt16(product_tuple.2) AS package_product_index,
            nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_order_id'), '"', ''), '') AS sku_order_id,
            toInt64OrNull(JSONExtractRaw(product_tuple.1, 'product_count')) AS shipped_product_count,
            if(nullIf(trim(JSONExtractRaw(product_tuple.1, 'price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(product_tuple.1, 'price'), 2) / 100) AS product_price_amount
        FROM package_rows p
        ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
        WHERE p.shop_id IS NOT NULL
          AND p.shop_order_id IS NOT NULL
          AND p.tracking_no IS NOT NULL
    )
    GROUP BY snapshot_date, shop_id, shop_order_id, tracking_no
)
SELECT
    t.snapshot_date,
    t.shop_id,
    t.shop_name,
    t.shop_order_id,
    t.tracking_no,
    t.logistics_company_names,
    t.first_shipped_at,
    t.latest_shipped_at,
    t.package_count,
    coalesce(p.package_product_row_count, toUInt32(0)) AS package_product_row_count,
    coalesce(p.sku_order_count, toUInt32(0)) AS sku_order_count,
    p.sku_order_ids,
    p.shipped_product_count,
    t.guarantee_amount,
    t.platform_delivery_discount_amount,
    t.platform_delivery_paid_amount,
    t.platform_delivery_payable_amount,
    p.avg_product_price_amount
FROM tracking_rollup t
LEFT JOIN product_rollup p
  ON t.snapshot_date = p.snapshot_date
 AND t.shop_id = p.shop_id
 AND t.shop_order_id = p.shop_order_id
 AND t.tracking_no = p.tracking_no;
