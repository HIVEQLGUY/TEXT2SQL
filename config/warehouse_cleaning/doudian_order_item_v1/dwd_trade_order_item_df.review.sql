/*
  REVIEW ONLY: the contract is reviewed; goods_price is user-confirmed as yuan.
  This DDL is only the focused item relation and not the complete documented
  JSON field output. Do not execute until cleaning-contract.yaml becomes approved/active and the
  field-level amount decisions are approved and the execution approval file is approved.
*/
CREATE TABLE IF NOT EXISTS youmei_sandbox.dwd_trade_order_item_df
(
    snapshot_date Date COMMENT '数据快照日期',
    shop_id String COMMENT '店铺ID',
    shop_name String COMMENT '店铺名称',
    shop_order_id String COMMENT '店铺订单号',
    item_index UInt16 COMMENT '商品明细序号，源JSON数组位置',
    product_id String COMMENT '商品ID',
    product_name String COMMENT '商品名称',
    sku_id String COMMENT 'SKU ID',
    sku_specification String COMMENT 'SKU规格，已展开为名称和值',
    item_quantity Int64 COMMENT '商品数量',
    goods_amount Decimal128(2) COMMENT '商品原价，单位为元，统一保留两位小数',
    item_paid_amount Decimal128(2) COMMENT '商品支付金额，接口文档单位为分，清洗后转为元并保留两位小数',
    room_id Nullable(String) COMMENT '直播间ID，空值和0统一为NULL',
    author_id Nullable(String) COMMENT '达人ID，空值和0统一为NULL',
    author_name Nullable(String) COMMENT '达人名称，接口字段语义待进一步确认',
    content_id Nullable(String) COMMENT '内容ID',
    ad_environment_type Nullable(String) COMMENT '广告环境类型',
    order_entry_code Nullable(String) COMMENT '下单端编码',
    order_entry_name Nullable(String) COMMENT '下单端名称',
    order_scene_code Nullable(String) COMMENT '下单场景编码',
    order_scene_name Nullable(String) COMMENT '下单场景名称',
    payment_type_code Nullable(String) COMMENT '支付方式编码',
    paid_at Nullable(DateTime('Asia/Shanghai')) COMMENT '支付时间',
    created_at Nullable(DateTime('Asia/Shanghai')) COMMENT '下单时间',
    updated_at Nullable(DateTime('Asia/Shanghai')) COMMENT '订单更新时间',
    order_status_code Nullable(String) COMMENT '商品订单状态编码',
    order_status_name Nullable(String) COMMENT '商品订单状态名称',
    main_status_code Nullable(String) COMMENT '主流程状态编码',
    main_status_name Nullable(String) COMMENT '主流程状态名称',
    room_attribution_quality_code UInt8 COMMENT '直播间归因质量码，0正常1缺失',
    author_attribution_quality_code UInt8 COMMENT '达人归因质量码，0正常1缺失',
    cleaning_contract_version String COMMENT '清洗契约版本，当前为1.2.0审阅版',
    source_task_instance_id String COMMENT '来源任务实例ID',
    etl_time DateTime('Asia/Shanghai') COMMENT '清洗处理时间'
)
ENGINE = MergeTree
PARTITION BY snapshot_date
ORDER BY (snapshot_date, shop_order_id, item_index);
