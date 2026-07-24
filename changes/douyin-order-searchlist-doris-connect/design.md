# 设计：抖店订单列表接口接入 Doris CONNECT/ODS

## Context

当前项目已经把 API / 原始 JSON 数据源定位为代码连接器数据源，默认直接落 Doris CONNECT/ODS。MySQL `youmei_ai` 只保留为历史表、兼容迁移和已确认对账来源，不再作为新 API 的默认落地层。

用户本次明确要求：在之前项目架构的 connect 层写入 `/order/searchList` 接入能力，并和当前项目架构融合；数据存放和读取都在 Doris；减少脚本生成，多用框架本身能力。

### 官方接口事实

- 接口路径：`/order/searchList`。
- 方法名：`order.searchList`。
- 协议版本：`2`。
- 官方 demo endpoint：`https://openapi-fxg.jinritemai.com/order/searchList`。
- 公共参数：`method`、`app_key`、`access_token`、`param_json`、`timestamp`、`v`、`sign`；`sign_method` 可选但推荐 `hmac-sha256`。
- 业务参数：`size`、`page` 必传；`create_time_start` 或 `update_time_start` 至少传一个。
- 页码从 `0` 开始。
- 单页大小必须 `<= 100`。
- 翻页最多支持 5 万条结果，因此大范围必须切分。
- 订单列表最多支持查询近 90 天创建的订单。
- 系统繁忙类错误按官方建议在 30 秒内重试 3 到 5 次。
- 授权主体：店铺。
- 收费类型：免费 API。
- 具体应用权限状态必须登录权限页确认，公共文档不能证明应用已授权。

## Goals

- 实现可复用的 API -> Doris CONNECT/ODS 连接器模式。
- 保留原始 API 证据，支持审计和重放。
- ODS 只做源形态保留，不提前做业务口径建模。
- 把连接器登记进 DataAgent integration 入口。
- 凭据不进入代码和公开文档。
- 在声明可生产使用前提供测试和校验 SQL。

## Decisions

### Decision 1: 使用 DataAgent 连接器代码和 Doris Stream Load

选择：在 `app/clients/` 下新增 Doris Stream Load 客户端，在 `app/services/` 或 app 内连接器包中新增抖店订单连接器。

理由：现有应用已经有 clients、repositories、services、integration API、配置加载和测试结构。Stream Load 是 Doris 原生 HTTP 写入方式，适合 API JSON 直接落 Doris。

备选方案：
- SeaTunnel：不选。当前规则把 SeaTunnel 留给结构化批量源和历史数据库迁移。
- DataX-Web：不选。DataX-Web 已经是历史/legacy。
- 纯脚本采集：不选。用户明确要求减少脚本，多用框架能力。

### Decision 2: 使用 CONNECT 和 ODS 两张 Doris 表

选择：
- CONNECT 表：`connect_douyin_order_search_list_di`。
- ODS 表：`ods_douyin_order_search_list_di`。

理由：CONNECT 保存请求/响应证据和失败诊断；ODS 提供源形态订单记录，方便 DataAgent 查询、验证和后续建模。

备选方案：
- 只建 raw 表：不够，后续问数和校验难以直接使用。
- ODS 全量扁平化：过早。`/order/searchList` 嵌套字段多且可能变化，深度扁平化应放到后续建模阶段。

### Decision 3: ODS 初始粒度为店铺订单号

选择：ODS 一行代表一个 店铺订单号(`order_id`) 的当前源形态记录，保留来源批次和嵌套 JSON。

理由：接口顶层返回 `shop_order_list`。商品单信息(`sku_order_list`) 属于嵌套结构，本次保留为 JSON，避免混合店铺订单和 SKU 商品单粒度。

备选方案：
- 商品单/SKU 粒度：后续 DWD 订单商品事实表可能需要，但不应混入 API 落地变更。
- 每次观测 append-only：CONNECT 已保存页面级证据，ODS 需要面向读取的当前源形态记录。

### Decision 4: 时间窗口切分由连接器负责

选择：连接器负责按 `update_time` 或 `create_time` 切分窗口、分页迭代，并记录子窗口元数据。

理由：接口有 90 天和 5 万翻页上限。连接器必须阻止非法请求，并记录实际采集范围。

备选方案：
- 让操作人手工选择窗口：不选。可重复接入应由框架管理。
- 只依赖分页：不选。官方错误明确限制最多翻页 5 万。

## Risks And Trade-Offs

- 应用权限状态还未验证，因为权限页需要登录态。
- 真实 API 和 Doris 端到端验证需要本地凭据。
- 接口包含收件人等敏感字段，本变更默认不提升加密/明文 PII 到分析字段。
- 签名算法要严格按官方调用指南实现，并用确定性测试覆盖。
- 高订单量店铺可能需要更小的窗口切分，窗口大小需要可配置。

## Data Model

### CONNECT 表

表名：`connect_douyin_order_search_list_di`

关键字段：
- `batch_id`
- `request_id`
- `endpoint`
- `method`
- `query_mode`
- `window_start`
- `window_end`
- `page`
- `size`
- `total`
- `http_status`
- `api_code`
- `api_sub_code`
- `api_message`
- `retry_count`
- `load_status`
- `raw_request_json`
- `raw_response_json`
- `collected_at`
- `connector_version`

### ODS 表

表名：`ods_douyin_order_search_list_di`

关键字段：
- `shop_id`
- `shop_name`
- `order_id`
- `order_level`
- `biz`
- `biz_desc`
- `order_type`
- `order_type_desc`
- `order_status`
- `order_status_desc`
- `main_status`
- `main_status_desc`
- `pay_time`
- `create_time`
- `update_time`
- `finish_time`
- `cancel_reason`
- `b_type`
- `b_type_desc`
- `sub_b_type`
- `sub_b_type_desc`
- `pay_type`
- `channel_payment_no`
- `order_amount`
- `pay_amount`
- `post_amount`
- `post_insurance_amount`
- `promotion_amount`
- `promotion_shop_amount`
- `promotion_platform_amount`
- `promotion_talent_amount`
- `promotion_pay_amount`
- `shop_cost_amount`
- `platform_cost_amount`
- `author_cost_amount`
- `only_platform_cost_amount`
- `sku_order_list_json`
- `logistics_info_json`
- `promotion_detail_json`
- `actual_receive_amount_info_json`
- `raw_shop_order_json`
- `batch_id`
- `request_id`
- `source_page`
- `collected_at`

## Validation

- DDL 校验：两张表存在于 Doris `agent_warehouse`。
- 加载校验：报告 CONNECT 成功页面数和失败页面数。
- ODS 校验：ODS 订单行数等于成功 CONNECT 页面中解析出的 `shop_order_list` 条数。
- 幂等校验：同一批次或窗口重跑后，不按 店铺订单号(`order_id`) 产生重复当前记录。
- 新鲜度校验：报告最大 更新时间(`update_time`)。
