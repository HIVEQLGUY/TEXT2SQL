# 抖店订单列表接口接入 Doris CONNECT/ODS

## Why

这次要解决的问题是：把抖店开放平台订单列表接口 `/order/searchList` 正式接入当前 Youmei DataAgent 架构，让订单 API 数据直接进入 Doris 的 CONNECT/ODS 层，并能被后续数仓建模、问数和治理链路复用。

当前项目已经明确：新 API / 原始 JSON 数据不再默认先进 MySQL，也不再为了迁就 SeaTunnel 新增 MySQL 中转。正确路径是：

```text
抖店开放平台 API -> 代码连接器 -> Doris CONNECT/ODS -> DWD/DIM/DWS/ADS
```

所以本变更不是写一个临时采集脚本，而是在 DataAgent 的连接器层补齐一个可复用的抖店订单接口接入能力。

## What Changes

- 新增抖店开放平台 `/order/searchList` 连接器，支持公共参数、签名、分页、时间窗口、重试和限流退避。
- 新增 Doris Stream Load 写入能力，用于 API 连接器把数据写入 Doris。
- 新增 CONNECT 层订单接口落地表，保存请求批次、分页、窗口、状态、错误、原始响应和连接器诊断。
- 新增 ODS 层订单源形态表，保存订单主记录关键字段，并保留 商品单信息(`sku_order_list`) 等嵌套对象的原始 JSON。
- 把该接口登记到现有 data integration 配置，使 DataAgent 框架入口能看到这个接入任务。
- 增加测试覆盖签名、分页窗口、重试策略、Stream Load payload、ODS 映射和 integration 展示。

## Scope

### In Scope

- 接口：抖店开放平台 `/order/searchList`，方法名 `order.searchList`。
- 官方文档页：`https://op.jinritemai.com/docs/api-docs/15/1342`。
- 应用权限页：`https://op.jinritemai.com/app-back/7651957715719177771/permission`。
- 数据库：Doris `agent_warehouse`。
- 数据层：CONNECT 和 ODS。
- 凭据来源：本地环境变量或本地 secrets 文件，代码和公开文档不保存明文密钥。
- 运行入口：DataAgent 连接器/service 层和 integration 配置。
- 允许保留一个极薄的本地触发入口，但主逻辑必须在框架层，不写成散落脚本。
- 官方限制：近 90 天创建订单、单页最大 100、翻页最多 5 万、时间条件必传、系统繁忙时按官方建议重试。

### Out of Scope

- 不做 DWD/DIM/DWS/ADS 业务建模。
- 不创建 Superset 图表或 BI 看板。
- 不把原始 API JSON 写入 MySQL 或 `youmei_ai`。
- 不绕过抖店登录、验证码、权限审批或店铺授权。
- 不接入除 `/order/searchList` 之外的订单详情、售后、结算或商品接口。
- 不处理超过官方 90 天窗口之外的后台手工导出订单。

## Impact

- 代码影响范围：
  - `TEXT2SQL-codex-handoff/app/clients/`
  - `TEXT2SQL-codex-handoff/app/services/`
  - `TEXT2SQL-codex-handoff/app/repositories/`
  - `TEXT2SQL-codex-handoff/config/data-integration.example.json`
  - `TEXT2SQL-codex-handoff/tests/`
- 运行依赖：
  - Doris FE HTTP `8030`，用于 Stream Load。
  - Doris MySQL `9030`，用于 DDL、校验和 DataAgent 读取。
  - 本地抖店 `app_key`、`app_secret`、`access_token`，以及可选 `shop_id`。
- 权限依赖：
  - 公共文档只能证明接口定义，不能证明应用 `7651957715719177771` 已有权限。
  - 实际权限状态需要登录抖店开放平台权限页确认。

## Capabilities

### New Capabilities

- 抖店订单列表接口代码连接器。
- Doris Stream Load 客户端，可复用于后续 API / 原始 JSON 接口。
- API 源进入 Doris CONNECT/ODS 的落地模式。
- DataAgent integration 入口对 API 连接器任务的展示。

### Modified Capabilities

- data integration 配置可以表示“API 连接器直接写 Doris”的任务，不再只围绕 DataX/MySQL/SeaTunnel。
- 本接口明确执行新的源架构边界：API -> 代码连接器 -> Doris CONNECT/ODS。
