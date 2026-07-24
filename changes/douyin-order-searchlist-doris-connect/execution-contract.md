# 执行契约：抖店订单列表接口接入 Doris CONNECT/ODS

## Intent Lock

在 DataAgent 的 connect 层实现抖店开放平台 `/order/searchList` 订单连接器，使订单 API 数据直接写入 Doris CONNECT/ODS，并能通过现有 integration 框架被发现和验证。

## Scope Fence

本次包含：
- `order.searchList` OpenAPI 请求签名、参数校验、重试、分页和时间窗口切分。
- Doris JSON Stream Load 客户端。
- CONNECT 表 `connect_douyin_order_search_list_di`。
- ODS 表 `ods_douyin_order_search_list_di`。
- integration 配置登记和测试。
- 运行时校验 SQL 与接入结果报告。

本次不包含：
- DWD/DIM/DWS/ADS 建模。
- Superset 资产。
- MySQL 或 `youmei_ai` 中转。
- 其他抖店 API。
- 绕过登录、验证码、权限审批或后台手工导出。

## Approved Behavior

- 连接器必须使用方法 `order.searchList` 和协议版本 `2`。
- 连接器必须包含官方公共参数，并支持 `hmac-sha256` 签名。
- 连接器必须要求 `create_time_start` 或 `update_time_start` 至少存在一个。
- 连接器发给 API 的单页大小必须 `<= 100`。
- 使用下单时间查询时，连接器必须保护官方近 90 天限制。
- 当查询结果可能超过 5 万翻页上限时，连接器必须切分时间窗口。
- 成功和失败的页面都必须写入 CONNECT 层，失败不能静默丢弃。
- ODS 层必须保留源形态订单记录；嵌套对象默认以 JSON 保存，不提前做业务建模。
- integration 视图和 safe info 不能暴露 `app_secret`、`access_token` 等敏感值。

## Test Obligations

实现生产代码前，必须先写失败测试覆盖：
- OpenAPI 签名和公共参数构造。
- `/order/searchList` 参数门禁。
- Doris Stream Load 请求构造。
- CONNECT 行构造和重试策略。
- 分页与时间窗口切分。
- ODS 行映射。
- integration 元数据加载和密钥脱敏。

## Architecture Constraints

- API / 原始 JSON 数据走：代码连接器 -> Doris CONNECT/ODS。
- 不用 SeaTunnel、DataX-Web 或 MySQL 作为这个 API 的默认接入路径。
- 使用 `TEXT2SQL-codex-handoff/app` 下既有 app/client/service/repository/test 结构。
- 凭据只从环境变量或本地 secrets 读取。
- Doris SQL 使用显式字段清单和校验 SQL。
- 未经明确确认，不执行破坏性 Doris SQL。

## Execution Batches

### Batch 1: 客户端基础能力

完成条件：
- `DouyinOpenApiClient` 能签名并校验参数，且测试通过。
- `DorisStreamLoadClient` 能构造安全的 JSON Stream Load 请求，且测试通过。

### Batch 2: 订单连接器和 Doris 表

完成条件：
- `DouyinOrderSearchListConnector` 支持重试、分页、窗口切分、CONNECT 行和 ODS 映射，且测试通过。
- Doris DDL 和校验 SQL 存在，并使用显式字段。
- repository 默认只做幂等建表和校验，不做破坏性覆盖。

### Batch 3: 配置和框架可见性

完成条件：
- settings 和 example integration metadata 包含抖店订单列表连接器，且不含真实密钥。
- `/api/integration/*` 能看到该连接器元数据。
- 密钥脱敏测试通过。

### Batch 4: 验证和交付

完成条件：
- 新增测试和全量测试通过。
- 平台健康确认 Doris 与 DataAgent 可用。
- 如果凭据和权限可用，完成一个小窗口真实接入并校验 CONNECT/ODS 行数。
- 如果权限或凭据缺失，明确报告“代码完成，但真实接入受权限/凭据阻塞”。

## Review Gates

- Batch 1 后复核客户端接口，再让连接器依赖它。
- Batch 2 后复核 DDL 与连接器行为，再尝试任何真实 Doris 写入。
- Batch 3 后复核框架展示，再声明 integration 已接入。
- Batch 4 后做最终复核，再关闭 change。

## Rewind Triggers

以下情况必须回到规格/设计阶段：
- 权限页显示应用 `7651957715719177771` 没有 `/order/searchList` 权限，且需要改变接入策略。
- 官方文档展示出不同的签名、限流或分页规则。
- 实现需要新增调度器或 UI 工作流，超出 integration 登记范围。
- ODS 粒度从 店铺订单号(`order_id`) 改为 商品单/SKU 粒度。
- 需要把敏感收件人字段暴露到 ODS 之上。

## Coverage Gaps

没有故意遗漏的规格需求。唯一外部门禁是：应用权限状态必须通过已登录的抖店开放平台权限页确认，公共文档本身不能证明具体应用已授权。

## Approval Gate

DP-3：契约批准。只有在用户明确批准本 `execution-contract.md` 后，才能进入实现阶段。
