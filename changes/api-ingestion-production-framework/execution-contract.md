# Execution Contract: API 接入生产级框架

## Intent Lock

把 API 接入从单接口脚本升级为生产级框架：所有未来 API 任务必须通过统一任务定义、统一执行入口、统一调度注册、统一运行状态、统一 Doris 层级边界和统一质量门禁；`/order/searchList` 是首个迁移对象。

## Scope Fence

In scope:

- API 任务定义、runner、registry、scheduler、运行状态 repository。
- Doris 运行状态表和抖店订单 DWD 当前态表。
- `/order/searchList` 从专用脚本迁移到框架任务。
- DolphinScheduler 发布逻辑去硬编码并由框架生成 rawScript。
- 失败页和质量门禁必须传播到 DolphinScheduler 失败状态。

Out of scope:

- 新增第二个业务接口。
- 完整 DWS/ADS 宽表重建。
- 使用 MySQL 作为 API 原始数据中转。
- 替换 DolphinScheduler。

## Approved Behavior

- 生产 API 任务 MUST 由任务定义描述，不能只由脚本参数决定。
- DolphinScheduler MUST 调用框架入口 `scripts/api_ingestion.py`。
- 运行状态 MUST 写入 Doris，且部分失败 MUST 使进程非零退出。
- CONNECT/ODS 保留证据，DWD 当前态提供业务查询口径。
- `/order/searchList` 当前态 MUST 按 `shop_id + order_id` 去重，支付日期订单数 MUST 使用 `pay_time > 0` 并排除 `未支付取消`。
- 调度器账号、密钥、cron、窗口和并发 MUST 来自配置或环境变量。

## Build Rules

- No production code without a failing test first.
- 脚本只能是薄入口，不得承载生产业务编排。
- 不得清空或破坏现有 `connect_douyin_order_search_list_di` 和 `ods_douyin_shop_order_search_list_di` 数据。
- 所有 Doris mutating SQL 必须先有只读存在性/影响面检查。
- 如果发现 DolphinScheduler API 无法安全 update workflow，必须记录旧/新 schedule/process 关系，不能静默删除。

## Test Obligations

- `test_api_ingestion_models.py` 覆盖任务定义和配置校验。
- `test_api_ingestion_runner.py` 覆盖成功、部分失败、非零退出和状态落库。
- `test_api_ingestion_scheduler.py` 覆盖 rawScript 生成、去硬编码配置和安全发布结果。
- `test_dwd_douyin_order_current.py` 覆盖当前态去重和支付日期订单口径。
- 现有 `test_douyin_order_connector.py` 和 `test_douyin_order_ingestion_job.py` 必须继续通过。

## Execution Batches

1. Framework contracts and tests.
2. Runner and status closure.
3. Scheduler integration.
4. Doris runtime tables and DWD current state.
5. Migrate `/order/searchList`.
6. Verification and governance.

## Review Gates

- Batch 2 后必须确认失败状态能让 runner 返回非零退出。
- Batch 3 后必须确认 DolphinScheduler rawScript 使用框架入口。
- Batch 4 后必须确认 DWD 当前态不会误用 ODS 追加记录。
- Batch 5 后必须在 worker 内跑窄窗口真实验证。
- Batch 6 后必须记录 OPSE。

## Rewind Triggers

- 任务定义无法表达某类 API 的分页、窗口或鉴权方式。
- DolphinScheduler API 不支持当前安全发布策略。
- Doris DWD 当前态 SQL 无法稳定表达订单最新版本。
- 任何实现需要引入 MySQL 作为 API 中转。
- 任何实现需要清空现有 CONNECT/ODS 数据。

## Approval Gate

DP-3: 本合同需要用户明确批准后进入 execution-governor 执行。批准后默认使用 SDD 模式，因为任务跨模型、runner、Doris、调度器和 API 多个模块。
