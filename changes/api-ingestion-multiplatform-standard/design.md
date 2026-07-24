# 多平台 API 接入标准化设计

## Context

当前 `api_ingestion` 已有任务模型、连接器 registry、统一 Runner、Doris 运行状态 repository、调度 rawScript 生成和抖店订单 adapter。项目规则要求后续外部平台先落 CONNECT/ODS，再进入 DWD/DIM/DWS/ADS；并要求减少脚本，使用框架自身能力。

约束：

- 不能引入 MySQL 作为 API JSON 中转。
- DolphinScheduler 仍是生产调度层。
- 抖店订单现有生产任务编码和表名必须兼容。
- DWD 以上建模不在本变更中展开。
- 密钥仍放在本地环境或未来 secret store，不进入代码和公开文档。

## Goals

- 让新平台接口只实现平台差异，不复制 Runner、调度和状态逻辑。
- 让每个接口开发前都有接入契约。
- 让 CONNECT/ODS 审计字段和质量门禁成为默认规则。
- 保持抖店订单现有生产链路不回归。

## Decisions

### Decision 1: 在现有 `api_ingestion` 内补抽象，不新建框架

Choice：新增 `platform.py`、`contracts.py` 等小模块，复用现有 Runner 和 registry。

Rationale：现有 Runner 已经处理状态、质量门禁、DWD 刷新和调度入口，重建框架会扩大风险。

Alternatives：新建完整 connector 框架。该方案会重复已有能力，不符合“减少脚本和重复框架”的要求。

### Decision 2: 任务定义承载多平台元数据

Choice：扩展 `ApiIngestionTaskDefinition`，加入 `platform_code`、`subject_type`、`endpoint_key`、`primary_keys`、`incremental_fields`、`audit_fields`。

Rationale：任务定义是 Runner、调度、质量门禁和文档契约的共同入口，放在这里能让接入可检查。

Alternatives：只在文档里描述。该方案无法被测试和运行时校验。

### Decision 3: 接口 adapter 输出页面级证据

Choice：标准 `EndpointAdapter.collect(task, run_id)` 返回 `ApiIngestionPageResult` 列表，继续由 Runner 聚合和判定。

Rationale：页面级证据是重试、补数、失败定位和 DWD 刷新边界的基础。

Alternatives：adapter 直接写状态表。该方案会让每个平台重复状态逻辑。

### Decision 4: 质量门禁先做运行级，不直接查 Doris 全表

Choice：本变更先标准化运行结果层的失败页、主体覆盖、行数和重复证据字段；Doris 全表 SQL 探针作为后续接口契约补充。

Rationale：不同接口主键和表结构不同，先把证据接口固定，再让具体接口补 SQL 探针。

Alternatives：一次性做全接口 SQL 质量引擎。该方案需要更多表元数据，不适合作为接其他平台前的前置收口。

## Risks And Trade-Offs

- 任务定义字段增加会影响现有测试和配置；通过向后兼容默认值控制风险。
- 抽象过早可能变复杂；本变更只抽最小稳定接口，保留抖店 adapter 作为样例。
- 质量门禁无法替代所有 Doris SQL 校验；接口契约必须继续声明接口级 SQL 探针。
