DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3;

CREATE TABLE youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3
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

INSERT INTO youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_3
SELECT
    snapshot_date,
    shop_id,
    shop_name,
    shop_order_id,
    tracking_no,
    logistics_company_names,
    first_shipped_at,
    latest_shipped_at,
    package_count,
    package_product_row_count,
    sku_order_count,
    sku_order_ids,
    shipped_product_count,
    guarantee_amount,
    platform_delivery_discount_amount,
    platform_delivery_paid_amount,
    platform_delivery_payable_amount,
    avg_product_price_amount
FROM youmei_sandbox.dwd_trade_order_logistics_tracking_no_shadow_1_3_3;

