# 多平台 API 接入标准化

## Why

当前 API 接入框架已经能承接抖店 `/order/searchList`，并通过统一 Runner 写入 Doris CONNECT/ODS、注册 DolphinScheduler、刷新 DWD 当前态。但这套能力仍带有首个平台的实现痕迹：平台鉴权、主体解析、接口分页、接入契约、调度命令和质量门禁没有形成平台无关模板。继续接其他平台时，如果每次都复制抖店代码，会产生多套小差异，后续补数、重跑、排障、权限轮换、限流处理和 ODS 质量判断都会难以治理。

本变更要把已有统一接入骨架升级为多平台标准接入能力。目标不是重写框架，而是在现有 `api_ingestion` 层补齐平台 connector 抽象、接口契约模板、通用质量门禁和调度命令生成规则，让后续平台只新增平台客户端、接口 adapter 和表契约。

## What Changes

- 新增平台无关 connector 抽象，明确 `PlatformClient`、`EndpointAdapter`、`SubjectResolver`、`LandingWriter` 的职责边界。
- 扩展 API 任务定义，支持平台编码、主体类型、接口分类、增量字段、分页模式、限流策略、主键字段和 CONNECT/ODS 标准审计字段。
- 新增接口接入契约模板，后续新平台在写代码前必须声明鉴权、分页、限流、增量、主键、表名、调度、回灌和故障处理。
- 标准化 DolphinScheduler rawScript 生成，不让新接口各自拼命令。
- 标准化质量门禁场景，覆盖页失败、空窗口、主键重复、主体缺跑、CONNECT/ODS 批次不一致、半批失败禁止刷新下游。
- 将抖店订单接口注册到新抽象上，作为多平台模板样例。

## Scope

### In Scope

- `api_ingestion` 服务层的多平台抽象和配置模型。
- 接口接入契约模板和任务定义示例。
- 调度 rawScript 生成标准化。
- 质量门禁模型和测试场景补充。
- 抖店 `/order/searchList` 的兼容迁移，保证现有生产入口不变。
- 当前状态文档和 skill/eval 治理记录。

### Out of Scope

- 不接入新的第三方平台业务接口。
- 不重建抖店订单 CONNECT/ODS/DWD 表。
- 不设计 DWD/DIM/DWS/ADS 业务模型。
- 不替换 DolphinScheduler。
- 不引入 MySQL 作为 API 原始 JSON 中转层。

## Impact

- 代码：`TEXT2SQL-codex-handoff/app/services/api_ingestion/`
- 配置：`TEXT2SQL-codex-handoff/config/api-ingestion-tasks.example.json`
- 文档模板：`TEXT2SQL-codex-handoff/docs/templates/`
- 测试：`TEXT2SQL-codex-handoff/tests/`
- 项目状态：`TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md`
- Skill/eval：`TEXT2SQL-codex-handoff/skill-governance/` 和本机 skill 投影

## Capabilities

### New Capabilities

- 多平台 API connector 标准接口。
- 平台主体解析和接口 adapter 标准模型。
- 接口接入契约模板。
- 平台无关调度命令生成。
- 接口级质量门禁标准场景。

### Modified Capabilities

- 抖店订单接口从平台专用 connector 迁移为标准 `EndpointAdapter` 样例。
- API 任务定义从单接口运行配置扩展为多平台接入契约的一部分。
- 后续新接口默认先完成 CONNECT/ODS，不直接进入 DWD 以上建模。
