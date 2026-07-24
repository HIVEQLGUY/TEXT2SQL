DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_df_rebuild_1_3_0;
DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0;

CREATE TABLE youmei_sandbox.dwd_trade_order_df_rebuild_1_3_0
(
    snapshot_date Date COMMENT '数据快照日期',
    shop_id String COMMENT '店铺ID',
    shop_name Nullable(String) COMMENT '店铺名称',
    shop_order_id String COMMENT '店铺订单号',
    order_level_code Nullable(String) COMMENT '订单层级编码',
    business_source_code Nullable(String) COMMENT '业务来源编码',
    business_source_name Nullable(String) COMMENT '业务来源名称',
    order_type_code Nullable(String) COMMENT '订单类型编码',
    order_type_name Nullable(String) COMMENT '订单类型名称',
    trade_type_code Nullable(String) COMMENT '交易类型编码',
    trade_type_name Nullable(String) COMMENT '交易类型名称',
    order_status_code Nullable(String) COMMENT '订单状态编码',
    order_status_name Nullable(String) COMMENT '订单状态名称',
    main_status_code Nullable(String) COMMENT '主流程状态编码',
    main_status_name Nullable(String) COMMENT '主流程状态名称',
    order_entry_code Nullable(String) COMMENT '下单端编码',
    order_entry_name Nullable(String) COMMENT '下单端名称',
    order_scene_code Nullable(String) COMMENT '下单场景编码',
    order_scene_name Nullable(String) COMMENT '下单场景名称',
    payment_type_code Nullable(String) COMMENT '支付方式编码',
    channel_payment_no Nullable(String) COMMENT '支付渠道流水号',
    app_id Nullable(String) COMMENT '小程序ID',
    paid_at Nullable(DateTime('Asia/Shanghai')) COMMENT '支付时间',
    order_expired_at Nullable(DateTime('Asia/Shanghai')) COMMENT '订单过期时间',
    finished_at Nullable(DateTime('Asia/Shanghai')) COMMENT '订单完成时间',
    created_at Nullable(DateTime('Asia/Shanghai')) COMMENT '下单时间',
    updated_at Nullable(DateTime('Asia/Shanghai')) COMMENT '订单更新时间',
    expected_ship_at Nullable(DateTime('Asia/Shanghai')) COMMENT '预计发货时间',
    shipped_at Nullable(DateTime('Asia/Shanghai')) COMMENT '发货时间',
    cancel_reason Nullable(String) COMMENT '取消原因',
    buyer_words Nullable(String) COMMENT '买家留言',
    seller_words Nullable(String) COMMENT '商家备注',
    encrypted_post_phone Nullable(String) COMMENT '加密收件人电话',
    encrypted_post_receiver Nullable(String) COMMENT '加密收件人姓名',
    post_address Nullable(String) COMMENT '收件人地址',
    masked_post_receiver Nullable(String) COMMENT '脱敏收件人姓名',
    masked_post_phone Nullable(String) COMMENT '脱敏收件人电话',
    masked_post_address Nullable(String) COMMENT '脱敏收件人地址',
    pay_phone Nullable(String) COMMENT '下单人手机号',
    post_receiver Nullable(String) COMMENT '收件人姓名',
    post_phone Nullable(String) COMMENT '收件人电话',
    open_address_id Nullable(String) COMMENT '收件人地址ID',
    greet_words Nullable(String) COMMENT '贺卡文字',
    order_amount Nullable(Decimal128(2)) COMMENT '订单金额，源单位分，清洗后单位元',
    paid_amount Nullable(Decimal128(2)) COMMENT '支付金额，源单位分，清洗后单位元',
    freight_amount Nullable(Decimal128(2)) COMMENT '快递费，源单位分，清洗后单位元',
    freight_insurance_amount Nullable(Decimal128(2)) COMMENT '运费险金额，源单位分，清洗后单位元',
    price_adjust_amount Nullable(Decimal128(2)) COMMENT '改价金额变化量，源单位分，清洗后单位元',
    freight_adjust_amount Nullable(Decimal128(2)) COMMENT '改价运费金额变化量，源单位分，清洗后单位元',
    promotion_amount Nullable(Decimal128(2)) COMMENT '订单优惠总金额，源单位分，清洗后单位元',
    shop_promotion_amount Nullable(Decimal128(2)) COMMENT '店铺优惠金额，源单位分，清洗后单位元',
    platform_promotion_amount Nullable(Decimal128(2)) COMMENT '平台优惠金额，源单位分，清洗后单位元',
    talent_promotion_amount Nullable(Decimal128(2)) COMMENT '达人优惠金额，源单位分，清洗后单位元',
    payment_promotion_amount Nullable(Decimal128(2)) COMMENT '支付优惠金额，源单位分，清洗后单位元',
    redpack_promotion_amount Nullable(Decimal128(2)) COMMENT '红包优惠金额，源单位分，清洗后单位元',
    redpack_platform_promotion_amount Nullable(Decimal128(2)) COMMENT '平台红包优惠金额，源单位分，清洗后单位元',
    redpack_talent_promotion_amount Nullable(Decimal128(2)) COMMENT '达人红包优惠金额，源单位分，清洗后单位元',
    shop_cost_amount Nullable(Decimal128(2)) COMMENT '商家承担金额，源单位分，清洗后单位元',
    platform_cost_amount Nullable(Decimal128(2)) COMMENT '平台承担金额，源单位分，清洗后单位元',
    only_platform_cost_amount Nullable(Decimal128(2)) COMMENT '仅平台承担金额，源单位分，清洗后单位元',
    author_cost_amount Nullable(Decimal128(2)) COMMENT '达人承担金额，源单位分，清洗后单位元',
    post_origin_amount Nullable(Decimal128(2)) COMMENT '运费原价，源单位分，清洗后单位元',
    post_promotion_amount Nullable(Decimal128(2)) COMMENT '运费优惠金额，源单位分，清洗后单位元',
    total_promotion_amount Nullable(Decimal128(2)) COMMENT '总优惠金额，源单位分，清洗后单位元',
    packing_amount Nullable(Decimal128(2)) COMMENT '打包费，源单位分，清洗后单位元',
    actual_receive_amount Nullable(Decimal128(2)) COMMENT '商家实收金额，源单位分，清洗后单位元',
    consumer_paid_receive_amount Nullable(Decimal128(2)) COMMENT '消费者实付收入金额，商家收入明细项类型1，源单位分，清洗后单位元',
    platform_discount_receive_amount Nullable(Decimal128(2)) COMMENT '平台承担优惠收入金额，商家收入明细项类型2，源单位分，清洗后单位元',
    talent_discount_receive_amount Nullable(Decimal128(2)) COMMENT '达人承担优惠收入金额，商家收入明细项类型3，源单位分，清洗后单位元',
    third_party_discount_receive_amount Nullable(Decimal128(2)) COMMENT '三方平台承担优惠收入金额，商家收入明细项类型4，源单位分，清洗后单位元',
    service_provider_discount_receive_amount Nullable(Decimal128(2)) COMMENT '服务商承担优惠收入金额，商家收入明细项类型5，源单位分，清洗后单位元',
    unknown_receive_amount Nullable(Decimal128(2)) COMMENT '未知类型商家收入金额，源单位分，清洗后单位元',
    unknown_receive_type_codes Nullable(String) COMMENT '未知商家收入金额类型编码列表',
    logistics_package_count UInt16 COMMENT '物流包裹数',
    logistics_company_names Nullable(String) COMMENT '物流公司名称列表，按订单粒度去重拼接',
    tracking_numbers Nullable(String) COMMENT '物流单号列表，按订单粒度去重拼接',
    first_logistics_shipped_at Nullable(DateTime('Asia/Shanghai')) COMMENT '最早物流发货时间',
    latest_logistics_shipped_at Nullable(DateTime('Asia/Shanghai')) COMMENT '最晚物流发货时间',
    logistics_guarantee_amount Nullable(Decimal128(2)) COMMENT '物流保价金额合计，源单位分，清洗后单位元',
    platform_delivery_discount_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送优惠金额合计，源单位分，清洗后单位元',
    platform_delivery_paid_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送实付金额合计，源单位分，清洗后单位元',
    platform_delivery_payable_amount Nullable(Decimal128(2)) COMMENT '即时零售平台运力配送应付金额合计，源单位分，清洗后单位元'
)
ENGINE = MergeTree
PARTITION BY snapshot_date
ORDER BY (snapshot_date, shop_id, shop_order_id);

CREATE TABLE youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0
(
    snapshot_date Date COMMENT '数据快照日期',
    shop_id String COMMENT '店铺ID',
    shop_name Nullable(String) COMMENT '店铺名称',
    shop_order_id String COMMENT '店铺订单号',
    item_index UInt16 COMMENT '商品明细序号，源JSON数组位置',
    product_id Nullable(String) COMMENT '商品ID',
    product_name Nullable(String) COMMENT '商品名称',
    sku_id Nullable(String) COMMENT 'SKU ID',
    sku_specification Nullable(String) COMMENT 'SKU规格，已展开为名称和值',
    item_quantity Nullable(Int64) COMMENT '商品数量',
    goods_amount Nullable(Decimal128(2)) COMMENT '商品原价，单位为元，统一保留两位小数',
    item_paid_amount Nullable(Decimal128(2)) COMMENT '商品支付金额，接口文档单位为分，清洗后转为元并保留两位小数',
    item_actual_receive_amount Nullable(Decimal128(2)) COMMENT '商品商家实收金额，源单位分，清洗后单位元',
    item_consumer_paid_receive_amount Nullable(Decimal128(2)) COMMENT '商品消费者实付收入金额，商家收入明细项类型1，源单位分，清洗后单位元',
    item_platform_discount_receive_amount Nullable(Decimal128(2)) COMMENT '商品平台承担优惠收入金额，商家收入明细项类型2，源单位分，清洗后单位元',
    item_talent_discount_receive_amount Nullable(Decimal128(2)) COMMENT '商品达人承担优惠收入金额，商家收入明细项类型3，源单位分，清洗后单位元',
    item_third_party_discount_receive_amount Nullable(Decimal128(2)) COMMENT '商品三方平台承担优惠收入金额，商家收入明细项类型4，源单位分，清洗后单位元',
    item_service_provider_discount_receive_amount Nullable(Decimal128(2)) COMMENT '商品服务商承担优惠收入金额，商家收入明细项类型5，源单位分，清洗后单位元',
    item_unknown_receive_amount Nullable(Decimal128(2)) COMMENT '商品未知类型商家收入金额，源单位分，清洗后单位元',
    item_unknown_receive_type_codes Nullable(String) COMMENT '商品未知商家收入金额类型编码列表',
    room_id Nullable(String) COMMENT '直播间ID，空值和0统一为NULL',
    author_id Nullable(String) COMMENT '达人ID，空值和0统一为NULL',
    author_name Nullable(String) COMMENT '达人名称，接口返回值',
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
    main_status_name Nullable(String) COMMENT '主流程状态名称'
)
ENGINE = MergeTree
PARTITION BY snapshot_date
ORDER BY (snapshot_date, shop_id, shop_order_id, item_index);

INSERT INTO youmei_sandbox.dwd_trade_order_df_rebuild_1_3_0
WITH order_receive AS
(
    SELECT
        shop_id,
        order_id,
        any(actual_receive_amount) AS actual_receive_amount,
        sumIf(amount, type_code = '1') AS consumer_paid_receive_amount,
        sumIf(amount, type_code = '2') AS platform_discount_receive_amount,
        sumIf(amount, type_code = '3') AS talent_discount_receive_amount,
        sumIf(amount, type_code = '4') AS third_party_discount_receive_amount,
        sumIf(amount, type_code = '5') AS service_provider_discount_receive_amount,
        sumIf(amount, type_code NOT IN ('1', '2', '3', '4', '5') OR type_code IS NULL) AS unknown_receive_amount,
        nullIf(arrayStringConcat(arraySort(groupUniqArrayIf(assumeNotNull(type_code), type_code NOT IN ('1', '2', '3', '4', '5') AND type_code IS NOT NULL)), ','), '') AS unknown_receive_type_codes
    FROM
    (
        SELECT DISTINCT
            shop_id,
            order_id,
            if(nullIf(trim(JSONExtractRaw(JSONExtractRaw(origin_data, 'actual_receive_amount_info'), 'actual_receive_amount')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(JSONExtractRaw(origin_data, 'actual_receive_amount_info'), 'actual_receive_amount'), 2) / 100) AS actual_receive_amount,
            toUInt16(item_tuple.2) AS detail_index,
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'type'), '"', ''), '') AS type_code,
            if(nullIf(trim(JSONExtractRaw(item_tuple.1, 'amount')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'amount'), 2) / 100) AS amount
        FROM
        (
            SELECT
                shop_id,
                order_id,
                origin_data,
                arrayJoin(arrayZip(JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(origin_data, 'actual_receive_amount_info'), 'actual_receive_amount_details')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(origin_data, 'actual_receive_amount_info'), 'actual_receive_amount_details'))))) AS item_tuple
            FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
            WHERE dt = '2026-07-22'
        )
    )
    GROUP BY shop_id, order_id
), logistics_rollup AS
(
    SELECT
        shop_id,
        order_id,
        toUInt16(count()) AS logistics_package_count,
        nullIf(arrayStringConcat(arraySort(groupUniqArrayIf(assumeNotNull(logistics_company_name), logistics_company_name IS NOT NULL)), ','), '') AS logistics_company_names,
        nullIf(arrayStringConcat(arraySort(groupUniqArrayIf(assumeNotNull(tracking_no), tracking_no IS NOT NULL)), ','), '') AS tracking_numbers,
        min(shipped_at) AS first_logistics_shipped_at,
        max(shipped_at) AS latest_logistics_shipped_at,
        sum(guarantee_amount) AS logistics_guarantee_amount,
        sum(platform_delivery_discount_amount) AS platform_delivery_discount_amount,
        sum(platform_delivery_paid_amount) AS platform_delivery_paid_amount,
        sum(platform_delivery_payable_amount) AS platform_delivery_payable_amount
    FROM
    (
        SELECT DISTINCT
            shop_id,
            order_id,
            toUInt16(item_tuple.2) AS logistics_index,
            nullIf(JSONExtractString(item_tuple.1, 'company_name'), '') AS logistics_company_name,
            nullIf(JSONExtractString(item_tuple.1, 'tracking_no'), '') AS tracking_no,
            if(toInt64OrNull(JSONExtractRaw(item_tuple.1, 'ship_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(item_tuple.1, 'ship_time')), 'Asia/Shanghai')) AS shipped_at,
            if(nullIf(trim(JSONExtractRaw(item_tuple.1, 'guarantee_amount')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'guarantee_amount'), 2) / 100) AS guarantee_amount,
            if(nullIf(trim(JSONExtractRaw(item_tuple.1, 'sp_discount_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'sp_discount_price'), 2) / 100) AS platform_delivery_discount_amount,
            if(nullIf(trim(JSONExtractRaw(item_tuple.1, 'sp_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'sp_price'), 2) / 100) AS platform_delivery_paid_amount,
            if(nullIf(trim(JSONExtractRaw(item_tuple.1, 'sp_total_price')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(item_tuple.1, 'sp_total_price'), 2) / 100) AS platform_delivery_payable_amount
        FROM
        (
            SELECT
                shop_id,
                order_id,
                arrayJoin(arrayZip(JSONExtractArrayRaw(logistics_info), arrayEnumerate(JSONExtractArrayRaw(logistics_info)))) AS item_tuple
            FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
            WHERE dt = '2026-07-22'
        )
    )
    GROUP BY shop_id, order_id
), normalized AS
(
    SELECT DISTINCT
        toDate(s.dt) AS snapshot_date,
        nullIf(trim(s.shop_id), '') AS shop_id,
        nullIf(trim(s.shop_name), '') AS shop_name,
        nullIf(trim(s.order_id), '') AS shop_order_id,
        nullIf(trim(s.order_level), '') AS order_level_code,
        nullIf(trim(s.biz), '') AS business_source_code,
        nullIf(trim(s.biz_desc), '') AS business_source_name,
        nullIf(trim(s.order_type), '') AS order_type_code,
        nullIf(trim(s.order_type_desc), '') AS order_type_name,
        nullIf(trim(s.trade_type), '') AS trade_type_code,
        nullIf(trim(s.trade_type_desc), '') AS trade_type_name,
        nullIf(trim(s.order_status), '') AS order_status_code,
        nullIf(trim(s.order_status_desc), '') AS order_status_name,
        nullIf(trim(s.main_status), '') AS main_status_code,
        nullIf(trim(s.main_status_desc), '') AS main_status_name,
        nullIf(trim(s.b_type), '') AS order_entry_code,
        nullIf(trim(s.b_type_desc), '') AS order_entry_name,
        nullIf(trim(s.sub_b_type), '') AS order_scene_code,
        nullIf(trim(s.sub_b_type_desc), '') AS order_scene_name,
        nullIf(trim(s.pay_type), '') AS payment_type_code,
        nullIf(trim(s.channel_payment_no), '') AS channel_payment_no,
        nullIf(trim(s.app_id), '') AS app_id,
        if(toInt64OrNull(nullIf(s.pay_time, '')) IS NULL OR toInt64OrZero(s.pay_time) = 0, NULL, toDateTime(toInt64OrZero(s.pay_time), 'Asia/Shanghai')) AS paid_at,
        if(toInt64OrNull(nullIf(s.order_expire_time, '')) IS NULL OR toInt64OrZero(s.order_expire_time) = 0, NULL, toDateTime(toInt64OrZero(s.order_expire_time), 'Asia/Shanghai')) AS order_expired_at,
        if(toInt64OrNull(nullIf(s.finish_time, '')) IS NULL OR toInt64OrZero(s.finish_time) = 0, NULL, toDateTime(toInt64OrZero(s.finish_time), 'Asia/Shanghai')) AS finished_at,
        if(toInt64OrNull(nullIf(s.create_time, '')) IS NULL OR toInt64OrZero(s.create_time) = 0, NULL, toDateTime(toInt64OrZero(s.create_time), 'Asia/Shanghai')) AS created_at,
        if(toInt64OrNull(nullIf(s.update_time, '')) IS NULL OR toInt64OrZero(s.update_time) = 0, NULL, toDateTime(toInt64OrZero(s.update_time), 'Asia/Shanghai')) AS updated_at,
        if(toInt64OrNull(nullIf(s.exp_ship_time, '')) IS NULL OR toInt64OrZero(s.exp_ship_time) = 0, NULL, toDateTime(toInt64OrZero(s.exp_ship_time), 'Asia/Shanghai')) AS expected_ship_at,
        if(toInt64OrNull(nullIf(s.ship_time, '')) IS NULL OR toInt64OrZero(s.ship_time) = 0, NULL, toDateTime(toInt64OrZero(s.ship_time), 'Asia/Shanghai')) AS shipped_at,
        nullIf(trim(s.cancel_reason), '') AS cancel_reason,
        nullIf(trim(s.buyer_words), '') AS buyer_words,
        nullIf(trim(s.seller_words), '') AS seller_words,
        nullIf(trim(s.encrypt_post_tel), '') AS encrypted_post_phone,
        nullIf(trim(s.encrypt_post_receiver), '') AS encrypted_post_receiver,
        nullIf(trim(s.post_addr), '') AS post_address,
        nullIf(trim(s.mask_post_receiver), '') AS masked_post_receiver,
        nullIf(trim(s.mask_post_tel), '') AS masked_post_phone,
        nullIf(trim(s.mask_post_addr), '') AS masked_post_address,
        nullIf(trim(s.pay_tel), '') AS pay_phone,
        nullIf(trim(s.post_receiver), '') AS post_receiver,
        nullIf(trim(s.post_tel), '') AS post_phone,
        nullIf(trim(s.open_address_id), '') AS open_address_id,
        nullIf(trim(s.greet_words), '') AS greet_words,
        if(nullIf(trim(s.order_amount), '') IS NULL, NULL, toDecimal128OrNull(s.order_amount, 2) / 100) AS order_amount,
        if(nullIf(trim(s.pay_amount), '') IS NULL, NULL, toDecimal128OrNull(s.pay_amount, 2) / 100) AS paid_amount,
        if(nullIf(trim(s.post_amount), '') IS NULL, NULL, toDecimal128OrNull(s.post_amount, 2) / 100) AS freight_amount,
        if(nullIf(trim(s.post_insurance_amount), '') IS NULL, NULL, toDecimal128OrNull(s.post_insurance_amount, 2) / 100) AS freight_insurance_amount,
        if(nullIf(trim(s.modify_amount), '') IS NULL, NULL, toDecimal128OrNull(s.modify_amount, 2) / 100) AS price_adjust_amount,
        if(nullIf(trim(s.modify_post_amount), '') IS NULL, NULL, toDecimal128OrNull(s.modify_post_amount, 2) / 100) AS freight_adjust_amount,
        if(nullIf(trim(s.promotion_amount), '') IS NULL, NULL, toDecimal128OrNull(s.promotion_amount, 2) / 100) AS promotion_amount,
        if(nullIf(trim(s.promotion_shop_amount), '') IS NULL, NULL, toDecimal128OrNull(s.promotion_shop_amount, 2) / 100) AS shop_promotion_amount,
        if(nullIf(trim(s.promotion_platform_amount), '') IS NULL, NULL, toDecimal128OrNull(s.promotion_platform_amount, 2) / 100) AS platform_promotion_amount,
        if(nullIf(trim(s.promotion_talent_amount), '') IS NULL, NULL, toDecimal128OrNull(s.promotion_talent_amount, 2) / 100) AS talent_promotion_amount,
        if(nullIf(trim(s.promotion_pay_amount), '') IS NULL, NULL, toDecimal128OrNull(s.promotion_pay_amount, 2) / 100) AS payment_promotion_amount,
        if(nullIf(trim(s.promotion_redpack_amount), '') IS NULL, NULL, toDecimal128OrNull(s.promotion_redpack_amount, 2) / 100) AS redpack_promotion_amount,
        if(nullIf(trim(s.promotion_redpack_platform_amount), '') IS NULL, NULL, toDecimal128OrNull(s.promotion_redpack_platform_amount, 2) / 100) AS redpack_platform_promotion_amount,
        if(nullIf(trim(s.promotion_redpack_talent_amount), '') IS NULL, NULL, toDecimal128OrNull(s.promotion_redpack_talent_amount, 2) / 100) AS redpack_talent_promotion_amount,
        if(nullIf(trim(s.shop_cost_amount), '') IS NULL, NULL, toDecimal128OrNull(s.shop_cost_amount, 2) / 100) AS shop_cost_amount,
        if(nullIf(trim(s.platform_cost_amount), '') IS NULL, NULL, toDecimal128OrNull(s.platform_cost_amount, 2) / 100) AS platform_cost_amount,
        if(nullIf(trim(s.only_platform_cost_amount), '') IS NULL, NULL, toDecimal128OrNull(s.only_platform_cost_amount, 2) / 100) AS only_platform_cost_amount,
        if(nullIf(trim(s.author_cost_amount), '') IS NULL, NULL, toDecimal128OrNull(s.author_cost_amount, 2) / 100) AS author_cost_amount,
        if(nullIf(trim(s.post_origin_amount), '') IS NULL, NULL, toDecimal128OrNull(s.post_origin_amount, 2) / 100) AS post_origin_amount,
        if(nullIf(trim(s.post_promotion_amount), '') IS NULL, NULL, toDecimal128OrNull(s.post_promotion_amount, 2) / 100) AS post_promotion_amount,
        if(nullIf(trim(s.total_promotion_amount), '') IS NULL, NULL, toDecimal128OrNull(s.total_promotion_amount, 2) / 100) AS total_promotion_amount,
        if(nullIf(trim(s.packing_amount), '') IS NULL, NULL, toDecimal128OrNull(s.packing_amount, 2) / 100) AS packing_amount,
        r.actual_receive_amount,
        r.consumer_paid_receive_amount,
        r.platform_discount_receive_amount,
        r.talent_discount_receive_amount,
        r.third_party_discount_receive_amount,
        r.service_provider_discount_receive_amount,
        r.unknown_receive_amount,
        r.unknown_receive_type_codes,
        coalesce(l.logistics_package_count, toUInt16(0)) AS logistics_package_count,
        l.logistics_company_names,
        l.tracking_numbers,
        l.first_logistics_shipped_at,
        l.latest_logistics_shipped_at,
        l.logistics_guarantee_amount,
        l.platform_delivery_discount_amount,
        l.platform_delivery_paid_amount,
        l.platform_delivery_payable_amount
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f s
    LEFT JOIN order_receive r ON s.shop_id = r.shop_id AND s.order_id = r.order_id
    LEFT JOIN logistics_rollup l ON s.shop_id = l.shop_id AND s.order_id = l.order_id
    WHERE s.dt = '2026-07-22'
)
SELECT *
FROM normalized
WHERE shop_id IS NOT NULL
  AND shop_order_id IS NOT NULL;

INSERT INTO youmei_sandbox.dwd_trade_order_item_df_rebuild_1_3_0
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
), item_receive AS
(
    SELECT
        shop_id,
        order_id,
        item_index,
        any(item_actual_receive_amount) AS item_actual_receive_amount,
        sumIf(amount, type_code = '1') AS item_consumer_paid_receive_amount,
        sumIf(amount, type_code = '2') AS item_platform_discount_receive_amount,
        sumIf(amount, type_code = '3') AS item_talent_discount_receive_amount,
        sumIf(amount, type_code = '4') AS item_third_party_discount_receive_amount,
        sumIf(amount, type_code = '5') AS item_service_provider_discount_receive_amount,
        sumIf(amount, type_code NOT IN ('1', '2', '3', '4', '5') OR type_code IS NULL) AS item_unknown_receive_amount,
        nullIf(arrayStringConcat(arraySort(groupUniqArrayIf(assumeNotNull(type_code), type_code NOT IN ('1', '2', '3', '4', '5') AND type_code IS NOT NULL)), ','), '') AS item_unknown_receive_type_codes
    FROM
    (
        SELECT DISTINCT
            shop_id,
            order_id,
            toUInt16(item_tuple.2) AS item_index,
            if(nullIf(trim(JSONExtractRaw(JSONExtractRaw(item_tuple.1, 'actual_receive_amount_info'), 'actual_receive_amount')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(JSONExtractRaw(item_tuple.1, 'actual_receive_amount_info'), 'actual_receive_amount'), 2) / 100) AS item_actual_receive_amount,
            toUInt16(detail_tuple.2) AS detail_index,
            nullIf(replaceAll(JSONExtractRaw(detail_tuple.1, 'type'), '"', ''), '') AS type_code,
            if(nullIf(trim(JSONExtractRaw(detail_tuple.1, 'amount')), '') IS NULL, NULL, toDecimal128OrNull(JSONExtractRaw(detail_tuple.1, 'amount'), 2) / 100) AS amount
        FROM source_items
        ARRAY JOIN arrayZip(
            JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(item_tuple.1, 'actual_receive_amount_info'), 'actual_receive_amount_details')),
            arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(JSONExtractRaw(item_tuple.1, 'actual_receive_amount_info'), 'actual_receive_amount_details')))
        ) AS detail_tuple
    )
    GROUP BY shop_id, order_id, item_index
), normalized AS
(
    SELECT DISTINCT
        toDate(si.dt) AS snapshot_date,
        nullIf(trim(si.shop_id), '') AS shop_id,
        nullIf(trim(si.shop_name), '') AS shop_name,
        nullIf(trim(si.order_id), '') AS shop_order_id,
        toUInt16(si.item_tuple.2) AS item_index,
        coalesce(nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'product_id_str'), '"', ''), ''), nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'product_id'), '"', ''), '')) AS product_id,
        nullIf(JSONExtractString(si.item_tuple.1, 'product_name'), '') AS product_name,
        nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'sku_id'), '"', ''), '') AS sku_id,
        arrayStringConcat(arrayMap(x -> concat(JSONExtractString(x, 'name'), '=', JSONExtractString(x, 'value')), JSONExtractArrayRaw(JSONExtractRaw(si.item_tuple.1, 'spec'))), ';') AS sku_specification,
        toInt64OrNull(JSONExtractRaw(si.item_tuple.1, 'item_num')) AS item_quantity,
        toDecimal128OrNull(JSONExtractRaw(si.item_tuple.1, 'goods_price'), 2) AS goods_amount,
        if(nullIf(trim(JSONExtractRaw(si.item_tuple.1, 'pay_amount')), '') IS NULL, CAST(NULL AS Nullable(Decimal128(2))), toDecimal128OrNull(JSONExtractRaw(si.item_tuple.1, 'pay_amount'), 2) / 100) AS item_paid_amount,
        r.item_actual_receive_amount,
        r.item_consumer_paid_receive_amount,
        r.item_platform_discount_receive_amount,
        r.item_talent_discount_receive_amount,
        r.item_third_party_discount_receive_amount,
        r.item_service_provider_discount_receive_amount,
        r.item_unknown_receive_amount,
        r.item_unknown_receive_type_codes,
        nullIf(nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'room_id_str'), '"', ''), ''), '0') AS room_id,
        nullIf(nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'author_id'), '"', ''), ''), '0') AS author_id,
        nullIf(JSONExtractString(si.item_tuple.1, 'author_name'), '') AS author_name,
        nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'content_id'), '"', ''), '') AS content_id,
        nullIf(JSONExtractString(si.item_tuple.1, 'ad_env_type'), '') AS ad_environment_type,
        nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'b_type'), '"', ''), '') AS order_entry_code,
        nullIf(JSONExtractString(si.item_tuple.1, 'b_type_desc'), '') AS order_entry_name,
        nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'sub_b_type'), '"', ''), '') AS order_scene_code,
        nullIf(JSONExtractString(si.item_tuple.1, 'sub_b_type_desc'), '') AS order_scene_name,
        nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'pay_type'), '"', ''), '') AS payment_type_code,
        if(toInt64OrNull(JSONExtractRaw(si.item_tuple.1, 'pay_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(si.item_tuple.1, 'pay_time')), 'Asia/Shanghai')) AS paid_at,
        if(toInt64OrNull(JSONExtractRaw(si.item_tuple.1, 'create_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(si.item_tuple.1, 'create_time')), 'Asia/Shanghai')) AS created_at,
        if(toInt64OrNull(JSONExtractRaw(si.item_tuple.1, 'update_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(si.item_tuple.1, 'update_time')), 'Asia/Shanghai')) AS updated_at,
        nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'order_status'), '"', ''), '') AS order_status_code,
        nullIf(JSONExtractString(si.item_tuple.1, 'order_status_desc'), '') AS order_status_name,
        nullIf(replaceAll(JSONExtractRaw(si.item_tuple.1, 'main_status'), '"', ''), '') AS main_status_code,
        nullIf(JSONExtractString(si.item_tuple.1, 'main_status_desc'), '') AS main_status_name
    FROM source_items si
    LEFT JOIN item_receive r
      ON si.shop_id = r.shop_id
     AND si.order_id = r.order_id
     AND toUInt16(si.item_tuple.2) = r.item_index
)
SELECT *
FROM normalized
WHERE shop_id IS NOT NULL
  AND shop_order_id IS NOT NULL;
