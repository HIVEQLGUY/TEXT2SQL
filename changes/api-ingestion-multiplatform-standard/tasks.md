# 任务清单：多平台 API 接入标准化

## File Structure

- Create: `TEXT2SQL-codex-handoff/app/services/api_ingestion/platform.py` — 定义平台客户端、接口 adapter、主体解析和标准 connector 组合接口。
- Create: `TEXT2SQL-codex-handoff/app/services/api_ingestion/contracts.py` — 生成和校验接口接入契约数据结构。
- Modify: `TEXT2SQL-codex-handoff/app/services/api_ingestion/models.py` — 扩展任务定义的多平台元数据和质量门禁字段。
- Modify: `TEXT2SQL-codex-handoff/app/services/api_ingestion/registry.py` — 支持注册标准 EndpointAdapter connector 工厂。
- Modify: `TEXT2SQL-codex-handoff/app/services/api_ingestion/runner.py` — 增加主体覆盖和重复证据质量门禁。
- Modify: `TEXT2SQL-codex-handoff/app/services/api_ingestion/douyin_order_searchlist.py` — 让抖店订单 adapter 符合标准接口。
- Modify: `TEXT2SQL-codex-handoff/app/services/api_ingestion/scheduler.py` — 固化平台无关 rawScript 生成规则。
- Modify: `TEXT2SQL-codex-handoff/config/api-ingestion-tasks.example.json` — 补充平台、主体、主键、增量和审计字段示例。
- Create: `TEXT2SQL-codex-handoff/docs/templates/API-接口接入契约模板.md` — 新平台接口开发前必须填写的契约模板。
- Modify: `TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md` — 记录多平台标准化完成状态。
- Create: `TEXT2SQL-codex-handoff/tests/test_api_ingestion_platform.py` — 覆盖标准 connector 抽象。
- Modify: `TEXT2SQL-codex-handoff/tests/test_api_ingestion_models.py` — 覆盖扩展任务定义校验。
- Modify: `TEXT2SQL-codex-handoff/tests/test_api_ingestion_runner.py` — 覆盖主体缺跑和重复证据质量失败。
- Modify: `TEXT2SQL-codex-handoff/tests/test_api_ingestion_scheduler.py` — 覆盖平台无关 rawScript。

## Interfaces

### Batch 1 -> Batch 2
- **Produces**: `EndpointAdapter.collect(task: ApiIngestionTaskDefinition, run_id: str) -> list[ApiIngestionPageResult]` — consumed by registry and standard connector.
- **Produces**: `ApiConnectorContext` — consumed by platform connector factories.

### Batch 2 -> Batch 3
- **Produces**: Extended `ApiIngestionTaskDefinition` — consumed by runner, scheduler and config tests.

### Batch 3 -> Batch 4
- **Produces**: Standard quality failure statuses — consumed by DWD refresh guard and OPSE evidence.

## Batch 1: 标准 Connector 抽象

Depends on: none

1.1 Create `TEXT2SQL-codex-handoff/tests/test_api_ingestion_platform.py`.
- RED: Add a test that a standard connector delegates to an `EndpointAdapter.collect` method and returns page results.
- Run the test and confirm it fails because `platform.py` does not exist.
- GREEN: Create `TEXT2SQL-codex-handoff/app/services/api_ingestion/platform.py` with `EndpointAdapter`, `SubjectResolver`, `ApiConnectorContext`, and `StandardApiConnector`.
- Run `pytest tests/test_api_ingestion_platform.py` and confirm it passes.
- Commit step: record changed files in final summary because this workspace has no active git CLI.

1.2 Modify `TEXT2SQL-codex-handoff/tests/test_api_ingestion_platform.py`.
- RED: Add a test that an empty subject list fails before collection when the task requires all subjects.
- Run the test and confirm it fails for missing subject validation.
- GREEN: Add subject validation to `StandardApiConnector.collect`.
- Run `pytest tests/test_api_ingestion_platform.py` and confirm it passes.
- Commit step: record changed files in final summary.

## Batch 2: 多平台任务定义与契约模板

Depends on: Batch 1

2.1 Modify `TEXT2SQL-codex-handoff/tests/test_api_ingestion_models.py`.
- RED: Add a test that task config accepts `platform_code`, `subject_type`, `endpoint_key`, `primary_keys`, `incremental_fields`, `audit_fields`, and rejects missing primary keys.
- Run the test and confirm it fails.
- GREEN: Extend `ApiIngestionTaskDefinition` and validation in `models.py`.
- Run `pytest tests/test_api_ingestion_models.py` and confirm it passes.
- Commit step: record changed files in final summary.

2.2 Create `TEXT2SQL-codex-handoff/docs/templates/API-接口接入契约模板.md`.
- RED: Add a test or grep check that the template contains sections for 鉴权、分页、限流、增量、主键、CONNECT/ODS、调度、回灌、故障处理.
- Run the check and confirm it fails because the template is absent.
- GREEN: Create the template with required sections and ODS-first gate.
- Run the check and confirm it passes.
- Commit step: record changed files in final summary.

2.3 Modify `TEXT2SQL-codex-handoff/config/api-ingestion-tasks.example.json`.
- RED: Add a config test asserting the抖店 task declares platform metadata, primary key and audit fields.
- Run the test and confirm it fails.
- GREEN: Update the example config.
- Run `pytest tests/test_api_ingestion_models.py` and confirm it passes.
- Commit step: record changed files in final summary.

## Batch 3: Runner 质量门禁和调度标准化

Depends on: Batch 2

3.1 Modify `TEXT2SQL-codex-handoff/tests/test_api_ingestion_runner.py`.
- RED: Add a test that missing required subject pages returns `quality_failed`.
- Run the test and confirm it fails.
- GREEN: Implement subject coverage quality gate in `runner.py`.
- Run `pytest tests/test_api_ingestion_runner.py` and confirm it passes.
- Commit step: record changed files in final summary.

3.2 Modify `TEXT2SQL-codex-handoff/tests/test_api_ingestion_runner.py`.
- RED: Add a test that duplicate key evidence returns `quality_failed`.
- Run the test and confirm it fails.
- GREEN: Add duplicate evidence fields to `ApiIngestionRunResult` and quality gate handling.
- Run `pytest tests/test_api_ingestion_runner.py` and confirm it passes.
- Commit step: record changed files in final summary.

3.3 Modify `TEXT2SQL-codex-handoff/tests/test_api_ingestion_scheduler.py`.
- RED: Add a test that scheduler rawScript never calls platform-specific scripts.
- Run the test and confirm it fails if rawScript is not standardized.
- GREEN: Keep scheduler rawScript generated as `python3 scripts/api_ingestion.py run --task-code <task_code>`.
- Run `pytest tests/test_api_ingestion_scheduler.py` and confirm it passes.
- Commit step: record changed files in final summary.

## Batch 4: 抖店样例迁移与治理收口

Depends on: Batch 3

4.1 Modify `TEXT2SQL-codex-handoff/app/services/api_ingestion/douyin_order_searchlist.py`.
- RED: Add a platform abstraction test using the抖店 adapter as a standard endpoint adapter.
- Run the test and confirm current behavior mismatch if any.
- GREEN: Adjust the adapter with minimal compatibility changes.
- Run targeted API ingestion tests and confirm they pass.
- Commit step: record changed files in final summary.

4.2 Modify `TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md`.
- RED: Confirm the state file lacks the multi-platform connector standard section.
- GREEN: Add the completed standardization state, template path, quality gates and remaining boundaries.
- Verify UTF-8 readability.
- Commit step: record changed files in final summary.

4.3 Record OPSE evaluation.
- RED: Confirm no `api-ingestion-multiplatform-standard` OPSE record exists.
- GREEN: Append OPSE record after tests pass.
- Verify JSONL parses.
- Commit step: report OPSE score and evidence.
