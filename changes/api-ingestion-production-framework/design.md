# Design: API 接入生产级框架

## Context

当前 `/order/searchList` 通过专用 Python 脚本采集抖店订单，DolphinScheduler 每天触发 shell 命令，数据写入 Doris CONNECT/ODS。链路已经可运行，但存在生产级缺口：脚本参数分散、调度注册硬编码、任务状态只在日志和 CONNECT 层间接体现、部分失败不会稳定反映到 DolphinScheduler、ODS 追加层容易被业务误用、后续新接口缺少统一扩展路径。

约束：

- API/raw JSON 接入必须走 code connector -> Doris CONNECT/ODS。
- 不使用 MySQL 作为 API 原始 JSON 中转层。
- DolphinScheduler 是正式调度层。
- 脚本只能作为薄入口，生产逻辑必须进入 `app/` 框架层。
- 当前 Doris 数据不得破坏。

## Goals

- 所有未来 API 接入都有统一任务定义、统一执行入口、统一状态表、统一调度注册和统一质量门禁。
- `/order/searchList` 成为框架中的一个任务，而不是孤立脚本。
- 操作人在 DolphinScheduler 上的上线、下线、重跑、失败查看能真实对应代码执行和运行状态。
- Doris 层级边界清晰：CONNECT/ODS 保留证据，DWD/DWS 提供业务查询。
- 新接口接入时只新增适配器和配置，不复制调度和状态代码。

## Decisions

### Decision 1: 新增框架任务定义模型

Choice: 在 `app/services/api_ingestion` 中引入 `ApiIngestionTaskDefinition`、`ApiIngestionRuntimeConfig` 和 `ApiIngestionQualityGate`。

Rationale: 当前 CLI 参数无法承载生产任务元数据。框架模型可以统一描述接口、窗口、分页、限流、目标表、调度 cron 和质量门禁。

Alternatives: 继续给每个接口写脚本参数。该方案会让接口规模扩大后不可维护。

### Decision 2: 新增统一执行服务

Choice: 新增 `ApiIngestionRunner`，由任务编码选择连接器，执行窗口采集、Doris 写入、状态落库和质量门禁。

Rationale: DolphinScheduler 应该调用稳定框架入口，而不是绑定某个具体接口脚本。

Alternatives: 让 DolphinScheduler 直接调每个接口脚本。该方案无法形成统一状态和重跑机制。

### Decision 3: 状态表作为生产闭环中心

Choice: 在 Doris 新增 `connect_api_ingestion_run_di` 和 `connect_api_ingestion_page_di`，分别记录运行级状态和页面级状态。

Rationale: CONNECT 原始页表只知道接口页面，不知道一次生产运行的整体状态、调度器实例、质量门禁结果和重跑关系。

Alternatives: 只依赖 DolphinScheduler 日志。该方案不利于数据侧排查和 BI 监控。

### Decision 4: ODS 保留源形态，DWD 提供当前态

Choice: 保留 `ods_douyin_shop_order_search_list_di` 作为追加源形态表，新增 `dwd_douyin_shop_order_current_di` 作为按 `shop_id + order_id` 去重后的订单当前态。

Rationale: 48 小时回看增量天然会重复返回订单。让 ODS 去重会损失采集证据；让业务直接查 ODS 会产生重复。

Alternatives: 把 ODS 改成 UNIQUE KEY。该方案会破坏源证据层，且可能影响已采数据。

### Decision 5: DolphinScheduler 发布从脚本转为服务化注册

Choice: 保留极薄 CLI 入口，但把注册策略、任务定义读取、rawScript 生成、更新而非删除重建等逻辑放入框架服务。

Rationale: 调度器发布是生产能力，不应散在一次性脚本里。

Alternatives: 继续用 `sync_dolphinscheduler_douyin_order_schedule.py`。该方案硬编码多、扩展差。

### Decision 6: 失败门禁必须让调度器失败

Choice: `failed_pages > 0`、授权主体缺跑、Doris 写入异常、质量门禁失败时，框架进程必须非零退出。

Rationale: 操作人要能在 DolphinScheduler 第一眼看到失败，不能只在 Doris 状态表里隐藏。

Alternatives: 采集完成后只写失败状态但进程返回成功。该方案会制造生产误判。

## Risks And Trade-Offs

- 新增 DWD 当前态需要明确支付日期业务口径；本变更将先固化订单量口径为支付时间且排除未支付取消，其他经营指标继续进入后续建模合同。
- 调度器 update-in-place 需要兼容 DolphinScheduler API 行为；如果 API 不支持安全更新，框架必须先离线旧版本再创建新版本，并记录替换关系。
- 运行状态表会增加 Doris 写入量，但能换来可观测性和重跑证据。
- 统一框架会比单接口脚本更复杂，但后续新增接口成本会降低。

## Verification Strategy

- 单元测试：任务定义解析、runner 状态流转、失败门禁、DWD 去重 SQL 生成、DolphinScheduler rawScript 生成。
- 集成测试：用 fake connector 模拟成功、部分失败、重复重跑。
- Doris 校验：运行状态表行数、失败页数、ODS 与 DWD 去重关系、支付日期订单口径。
- 调度器校验：workflow ONLINE、rawScript 调用框架入口、手动重跑生成新 run 记录、失败时 DolphinScheduler task 失败。
