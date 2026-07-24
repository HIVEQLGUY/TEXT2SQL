# 执行契约：多平台 API 接入标准化

## Intent Lock

把现有抖店 API 接入骨架升级为多平台标准接入能力，让后续平台只新增平台客户端、接口 adapter 和表契约，不复制 Runner、调度、状态和质量门禁。

## Scope Fence

In scope:

- 新增平台无关 connector 抽象。
- 扩展 API 任务定义的多平台元数据。
- 新增接口接入契约模板。
- 标准化调度 rawScript。
- 标准化主体覆盖和重复证据质量门禁。
- 保持抖店 `/order/searchList` 兼容。

Out of scope:

- 不接入新第三方平台业务接口。
- 不重建现有 Doris 表。
- 不做 DWD/DIM/DWS/ADS 建模。
- 不替换 DolphinScheduler。
- 不引入 MySQL 作为 API JSON 中转。

## Approved Behavior

- 系统 MUST 提供 `EndpointAdapter` 和 `StandardApiConnector`，使平台 adapter 可插入统一 Runner。
- 任务定义 MUST 校验平台编码、主体类型、接口 key、主键、增量字段和审计字段。
- 新接口 MUST 先填写接口接入契约模板，并声明 CONNECT/ODS 表。
- 调度 rawScript MUST 调用 `scripts/api_ingestion.py run --task-code <task_code>`。
- 质量门禁 MUST 在失败页、主体缺跑、重复键证据出现时返回非零结果。
- 抖店订单任务编码、表名和现有采集逻辑 MUST 不回归。

## Test Obligations

- 先写 `tests/test_api_ingestion_platform.py`，证明标准 connector 委托 adapter。
- 扩展 `tests/test_api_ingestion_models.py`，证明多平台元数据校验。
- 扩展 `tests/test_api_ingestion_runner.py`，证明主体缺跑和重复证据触发 `quality_failed`。
- 扩展 `tests/test_api_ingestion_scheduler.py`，证明 rawScript 平台无关。
- 全量 `pytest` 必须通过后才记录完成状态。

## Execution Batches

1. 标准 connector 抽象。
2. 多平台任务定义与接口契约模板。
3. Runner 质量门禁和调度标准化。
4. 抖店样例兼容、状态文档和 OPSE 收口。

## Review Gates

- Batch 1 后检查抽象是否没有引入平台硬编码。
- Batch 2 后检查任务定义是否向后兼容抖店配置。
- Batch 3 后检查失败时不会刷新 DWD。
- Batch 4 后检查文档、测试和 OPSE 记录。

## Rewind Triggers

- 如果实现需要修改现有 Doris 表结构，返回规划。
- 如果实现需要 DolphinScheduler API 实际发布，返回规划。
- 如果任务定义破坏现有 `douyin_order_searchlist_daily`，先修复兼容性。
- 如果质量门禁需要接口级 SQL 探针才能判断，先记录为接口契约要求，不在本批次扩大为 SQL 引擎。

## Coverage Check

所有规格要求均映射到测试义务和执行批次，无未覆盖要求。
