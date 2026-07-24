# 任务清单：抖店订单列表接口接入 Doris CONNECT/ODS

## 文件范围

- 新增：`TEXT2SQL-codex-handoff/app/clients/douyin_openapi.py`，抖店 OpenAPI 签名、公共参数、参数门禁和 HTTP 调用客户端。
- 新增：`TEXT2SQL-codex-handoff/app/clients/doris_stream_load.py`，Doris HTTP Stream Load JSON Lines 客户端。
- 新增：`TEXT2SQL-codex-handoff/app/services/douyin_order_connector.py`，`/order/searchList` 分页、重试、窗口切分、CONNECT 行构造、ODS 映射和写入编排。
- 新增：`TEXT2SQL-codex-handoff/app/repositories/doris_ingestion_repository.py`，CONNECT/ODS Stream Load 仓储封装。
- 新增：`TEXT2SQL-codex-handoff/sql/douyin_order_searchlist_connect_ods.sql`，Doris CONNECT/ODS 幂等 DDL。
- 修改：`TEXT2SQL-codex-handoff/app/core/config.py`，增加抖店 OpenAPI 和 Doris HTTP typed settings。
- 修改：`TEXT2SQL-codex-handoff/app/api/routers/health.py`，暴露脱敏后的连接器配置状态。
- 修改：`TEXT2SQL-codex-handoff/config/data-integration.example.json`，登记抖店开放平台 source/job 元数据。
- 修改：`TEXT2SQL-codex-handoff/config/database.example.env`，补充 Doris HTTP 与抖店 OpenAPI 环境变量示例。
- 新增/修改测试：覆盖 OpenAPI 签名、参数门禁、Stream Load、CONNECT/ODS 写入、配置加载、integration 脱敏。

## 执行批次

### Batch 1：客户端基础能力

- 已完成：`DouyinOpenApiClient` 按官方文档实现 `hmac-sha256` 签名，签名内容使用 `app_key`、`method`、`param_json`、`timestamp`、`v`，`param_json` 按 key 排序。
- 已完成：`DouyinOpenApiClient` 使用 POST，公共参数走 query，`param_json` 作为 JSON body。
- 已完成：`/order/searchList` 参数门禁覆盖开始时间、`page >= 0`、`size <= 100`、下单时间近 90 天限制。
- 已完成：`DorisStreamLoadClient` 使用 `PUT /api/{db}/{table}/_stream_load`、JSON Lines、Basic Auth、Doris JSON load headers。

### Batch 2：订单连接器和 Doris 表

- 已完成：`DouyinOrderSearchListConnector` 支持可重试错误 `isp.service-error:20004/20005`，失败页也写 CONNECT 证据。
- 已完成：分页从 `page=0` 开始，根据 `total` 停止翻页。
- 已完成：当接口总数达到官方 5 万限制时，支持按时间窗口二分。
- 已完成：ODS 映射保留稳定订单字段、嵌套 JSON 字符串、单个订单原始 JSON、批次号、请求号、来源页码和采集时间。
- 已完成：`DorisIngestionRepository` 将 CONNECT/ODS 行分别写入 `connect_douyin_order_search_list_di` 和 `ods_douyin_shop_order_search_list_di`。
- 已完成：Doris `agent_warehouse` 已幂等创建上述两张表，并通过 `SHOW TABLES` 验证。

### Batch 3：配置和框架可见性

- 已完成：`Settings` 增加 `douyin_openapi` 和 `doris_stream_load`。
- 已完成：`/api/health` 只返回凭据是否配置，不返回明文。
- 已完成：`DataIntegrationService` 的 source/job 列表可展示抖店开放平台连接器，且 `app_secret`、`access_token` 脱敏。
- 已完成：`data-integration.example.json` 登记抖店订单查询接口采集任务，状态为 `pending_credentials`。

### Batch 4：验证和交付

- 已完成：针对性测试通过。
- 已完成：全量测试通过，结果为 `59 passed`。
- 已完成：本地 Doris `127.0.0.1:9030` 连接验证通过，并完成幂等 DDL 落库。
- 未完成：真实小窗口采集未执行，因为抖店应用 `7651957715719177771` 的 `/order/searchList` 权限、店铺授权和 `app_key/app_secret/access_token` 仍待页面确认和配置。

## 当前阻塞

- 需要登录抖店开放平台权限页确认 `/order/searchList` 已授权。
- 需要配置真实 `DOUYIN_OPENAPI_APP_KEY`、`DOUYIN_OPENAPI_APP_SECRET`、`DOUYIN_OPENAPI_ACCESS_TOKEN`。
- 凭据配置后，再执行一个小时间窗口真实采集，并校验 CONNECT/ODS 行数和失败页记录。
