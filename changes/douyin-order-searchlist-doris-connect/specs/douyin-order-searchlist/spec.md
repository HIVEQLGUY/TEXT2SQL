# 能力规格：抖店订单列表接口 Doris 接入

## ADDED Requirements

### Requirement: 官方接口契约

连接器 SHALL 使用抖店开放平台 `/order/searchList` API，方法名为 `order.searchList`，API 协议版本为 `2`。

#### Scenario: 构造公共参数

WHEN 连接器准备一次请求
THEN 请求 SHALL 包含 `method`、`app_key`、`access_token`、`param_json`、`timestamp`、`v`、`sign` 和 `sign_method`。

#### Scenario: 业务参数排序

WHEN 连接器为请求签名
THEN 连接器 SHALL 按参数名排序业务参数后生成 `param_json`，再参与签名。

### Requirement: 查询窗口门禁

连接器 SHALL 在调用 API 前执行 `/order/searchList` 官方查询限制。

#### Scenario: 缺少时间条件时拒绝请求

WHEN 请求中既没有 `create_time_start` 也没有 `update_time_start`
THEN 连接器 SHALL 在发送 API 前拒绝该请求。

#### Scenario: 单页大小受控

WHEN 请求要求单页超过 100 条
THEN 连接器 SHALL 限制或拒绝该请求，确保发给 API 的 `size <= 100`。

#### Scenario: 大结果窗口自动切分

WHEN 查询窗口可能超过 5 万条翻页上限
THEN 连接器 SHALL 切分时间窗口，并把每个子窗口写入 CONNECT 元数据。

#### Scenario: 近 90 天下单时间限制

WHEN 使用 `create_time_start` 查询
THEN 连接器 SHALL 不发送早于运行日期前 90 天的下单时间下界。

### Requirement: Doris CONNECT 落地

连接器 SHALL 先把 API 采集证据写入 Doris CONNECT 表，再做 ODS 解析。

#### Scenario: 成功页面写入 CONNECT

WHEN API 页面成功返回
THEN CONNECT 行 SHALL 包含来源系统、接口地址、方法名、批次 ID、请求 ID、页码、单页大小、查询窗口、HTTP 状态、API 状态码、采集时间、原始请求参数、原始响应、连接器版本和加载状态。

#### Scenario: 失败页面可见

WHEN API 页面重试后仍失败
THEN CONNECT 行 SHALL 包含错误码、错误消息、重试次数、请求元数据，并设置 `load_status = 'failed'`。

### Requirement: Doris ODS 源形态表

连接器 SHALL 把成功 CONNECT 记录解析为 ODS 表，同时保留源系统语义。

#### Scenario: 解析店铺订单

WHEN 成功响应中包含 `shop_order_list`
THEN ODS 行 SHALL 包含稳定的订单主字段，例如 店铺ID(`shop_id`)、店铺名称(`shop_name`)、店铺订单号(`order_id`)、订单状态(`order_status`)、主流程状态(`main_status`)、支付时间(`pay_time`)、下单时间(`create_time`)、更新时间(`update_time`)、订单金额(`order_amount`)、支付金额(`pay_amount`)、快递费(`post_amount`)、运费险金额(`post_insurance_amount`)、优惠金额相关字段和来源批次元数据。

#### Scenario: 保留嵌套对象

WHEN 响应中包含 商品单信息(`sku_order_list`)、物流信息(`logistics_info`)、优惠信息(`promotion_detail`) 或 商家收入金额信息(`actual_receive_amount_info`) 等嵌套对象
THEN ODS 行 SHALL 以 JSON 字符串保留这些对象，除非某字段被明确提升为稳定 ODS 顶层字段。

### Requirement: 框架集成

连接器 SHALL 能通过现有 DataAgent integration 框架发现。

#### Scenario: integration overview 展示连接器

WHEN 读取 `/api/integration/overview` 和 `/api/integration/sync-jobs`
THEN 抖店订单列表连接器 SHALL 作为 API/Doris 连接器展示，并显示目标 CONNECT 和 ODS 表。

#### Scenario: 凭据脱敏

WHEN 列出数据源
THEN `app_secret`、`access_token` 以及 token 类字段 SHALL 被脱敏。

### Requirement: 验证证据

实现 SHALL 提供自动化测试和运行时 Doris 校验 SQL。

#### Scenario: 单元测试覆盖连接器行为

WHEN 测试套件运行
THEN 测试 SHALL 覆盖签名、参数校验、重试处理、CONNECT 行构造、ODS 映射、Stream Load payload 构造和 integration 脱敏。

#### Scenario: 运行时校验可用

WHEN 使用真实凭据运行连接器
THEN 校验结果 SHALL 报告 CONNECT 行数、ODS 行数、失败页面数、重复 店铺订单号(`order_id`) 数量和最新 更新时间(`update_time`)。
