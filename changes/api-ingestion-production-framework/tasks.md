# 任务清单：API 接入生产级框架

## File Structure

- Create: `TEXT2SQL-codex-handoff/app/services/api_ingestion/models.py` - 定义 API 任务、运行、页面、质量门禁和结果模型。
- Create: `TEXT2SQL-codex-handoff/app/services/api_ingestion/registry.py` - 加载和校验任务定义，按任务编码返回连接器工厂。
- Create: `TEXT2SQL-codex-handoff/app/services/api_ingestion/runner.py` - 统一执行任务、记录状态、执行质量门禁并返回进程退出语义。
- Create: `TEXT2SQL-codex-handoff/app/repositories/api_ingestion_run_repository.py` - 将运行级和页面级状态写入 Doris。
- Create: `TEXT2SQL-codex-handoff/app/services/api_ingestion/scheduler.py` - 生成和发布 DolphinScheduler workflow，消除接口专用注册逻辑。
- Create: `TEXT2SQL-codex-handoff/app/services/api_ingestion/dwd_order_current.py` - 生成和验证抖店订单当前态 DWD SQL。
- Create: `TEXT2SQL-codex-handoff/config/api-ingestion-tasks.example.json` - 示例生产任务定义。
- Create: `TEXT2SQL-codex-handoff/sql/api_ingestion_runtime_tables.sql` - Doris 运行状态表 DDL。
- Create: `TEXT2SQL-codex-handoff/sql/dwd_douyin_shop_order_current_di.sql` - 抖店订单当前态 DWD DDL/DML/校验 SQL。
- Create: `TEXT2SQL-codex-handoff/scripts/api_ingestion.py` - 极薄 CLI 入口，只调用框架 runner 和 scheduler。
- Modify: `TEXT2SQL-codex-handoff/app/services/douyin_order_ingestion_job.py` - 适配统一 runner，返回结构化运行结果。
- Modify: `TEXT2SQL-codex-handoff/scripts/douyin_order_searchlist_ingest.py` - 降级为兼容入口，提示使用框架入口。
- Modify: `TEXT2SQL-codex-handoff/scripts/sync_dolphinscheduler_douyin_order_schedule.py` - 降级为兼容入口，调用框架 scheduler。
- Modify: `TEXT2SQL-codex-handoff/app/core/config.py` - 增加 API 任务配置文件和调度器凭据配置。
- Modify: `TEXT2SQL-codex-handoff/app/api/routers/integration.py` - 暴露 API 接入任务、最近运行和质量状态。
- Modify: `TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md` - 记录生产级 API 接入框架和迁移状态。
- Create: `TEXT2SQL-codex-handoff/tests/test_api_ingestion_models.py` - 覆盖任务定义和质量门禁模型。
- Create: `TEXT2SQL-codex-handoff/tests/test_api_ingestion_runner.py` - 覆盖成功、部分失败、非零退出和状态记录。
- Create: `TEXT2SQL-codex-handoff/tests/test_api_ingestion_scheduler.py` - 覆盖 DolphinScheduler rawScript 生成和去硬编码配置。
- Create: `TEXT2SQL-codex-handoff/tests/test_dwd_douyin_order_current.py` - 覆盖支付日期口径和当前态去重 SQL。

## Interfaces

### Batch 1 -> Batch 2
- **Produces**: `ApiIngestionTaskDefinition` and `ApiIngestionRunResult` - consumed by Batch 2 runner and Batch 3 scheduler.

### Batch 2 -> Batch 3
- **Produces**: `ApiIngestionRunner.run(task_code, mode, window)` - consumed by CLI and DolphinScheduler rawScript.

### Batch 2 -> Batch 4
- **Produces**: `connect_api_ingestion_run_di` and `connect_api_ingestion_page_di` records - consumed by integration API and production monitoring.

### Batch 4 -> Batch 5
- **Produces**: `dwd_douyin_shop_order_current_di` - consumed by business validation and later DWS modeling.

## Batch 1: Framework Contracts And Tests

Depends on: none

1.1 Create `TEXT2SQL-codex-handoff/tests/test_api_ingestion_models.py`.
- RED: Add a test that constructing a task without task code, source platform, schedule cron, connector type, target tables, window field, and quality gates raises validation errors.
- Run the test and confirm it fails because `app.services.api_ingestion.models` does not exist.
- GREEN: Create `TEXT2SQL-codex-handoff/app/services/api_ingestion/models.py` with dataclasses for task definition, window config, target tables, quality gate, run result and page result.
- Run `pytest tests/test_api_ingestion_models.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

1.2 Create `TEXT2SQL-codex-handoff/tests/test_api_ingestion_models.py`.
- RED: Add a test that a task definition rejects cron, window size, page size, workers, and target table values that are empty or outside approved ranges.
- Run the test and confirm it fails for missing validation.
- GREEN: Add validation methods on `ApiIngestionTaskDefinition`.
- Run `pytest tests/test_api_ingestion_models.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

1.3 Create `TEXT2SQL-codex-handoff/config/api-ingestion-tasks.example.json`.
- RED: Add a test that example config contains `douyin_order_searchlist_daily` and maps it to `/order/searchList`.
- Run the test and confirm it fails because the config file does not exist.
- GREEN: Create the example config with `/order/searchList` daily and backfill defaults.
- Run `pytest tests/test_api_ingestion_models.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

## Batch 2: Runner And Status Closure

Depends on: Batch 1

2.1 Create `TEXT2SQL-codex-handoff/tests/test_api_ingestion_runner.py`.
- RED: Add a fake connector test where all pages succeed and the runner returns `success` with exit code `0`.
- Run the test and confirm it fails because `ApiIngestionRunner` does not exist.
- GREEN: Create `TEXT2SQL-codex-handoff/app/services/api_ingestion/runner.py` and `registry.py` with a fake-connector friendly execution path.
- Run `pytest tests/test_api_ingestion_runner.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

2.2 Modify `TEXT2SQL-codex-handoff/tests/test_api_ingestion_runner.py`.
- RED: Add a fake connector test where one page fails and assert runner status is `partial_failed` with exit code `1`.
- Run the test and confirm it fails because the runner does not yet propagate partial failures.
- GREEN: Implement quality gate evaluation and non-zero exit mapping.
- Run `pytest tests/test_api_ingestion_runner.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

2.3 Create `TEXT2SQL-codex-handoff/app/repositories/api_ingestion_run_repository.py`.
- RED: Add a test repository double asserting the runner writes one run record and page records for every connector page.
- Run the test and confirm it fails because repository integration is missing.
- GREEN: Add repository protocol calls in the runner and a Doris repository implementation using Stream Load.
- Run `pytest tests/test_api_ingestion_runner.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

## Batch 3: Scheduler Integration

Depends on: Batch 2

3.1 Create `TEXT2SQL-codex-handoff/tests/test_api_ingestion_scheduler.py`.
- RED: Add a test that generated DolphinScheduler rawScript calls `scripts/api_ingestion.py run --task-code douyin_order_searchlist_daily`.
- Run the test and confirm it fails because scheduler service does not exist.
- GREEN: Create `TEXT2SQL-codex-handoff/app/services/api_ingestion/scheduler.py` and `TEXT2SQL-codex-handoff/scripts/api_ingestion.py`.
- Run `pytest tests/test_api_ingestion_scheduler.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

3.2 Modify `TEXT2SQL-codex-handoff/scripts/sync_dolphinscheduler_douyin_order_schedule.py`.
- RED: Add a test that scheduler credentials are read from environment or config and are not hardcoded in the scheduler service.
- Run the test and confirm it fails against the existing hardcoded path.
- GREEN: Move DolphinScheduler username, password, base URL and project code into settings/config; keep old script as a compatibility wrapper.
- Run `pytest tests/test_api_ingestion_scheduler.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

3.3 Modify `TEXT2SQL-codex-handoff/scripts/sync_dolphinscheduler_douyin_order_schedule.py`.
- RED: Add a test that publishing a workflow uses update or versioned replacement semantics and records old/new process code instead of unconditional delete.
- Run the test and confirm it fails.
- GREEN: Implement safe publish result objects with old/new schedule and process metadata.
- Run `pytest tests/test_api_ingestion_scheduler.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

## Batch 4: Doris Runtime Tables And DWD Current State

Depends on: Batch 2

4.1 Create `TEXT2SQL-codex-handoff/sql/api_ingestion_runtime_tables.sql`.
- RED: Add a test that the SQL file defines `connect_api_ingestion_run_di` and `connect_api_ingestion_page_di`.
- Run the test and confirm it fails because the SQL file does not exist.
- GREEN: Create Doris DDL with Duplicate Key evidence tables and explicit columns for task code, run id, scheduler instance id, shop id, window, page, status, counts and errors.
- Run `pytest tests/test_api_ingestion_runner.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

4.2 Create `TEXT2SQL-codex-handoff/tests/test_dwd_douyin_order_current.py`.
- RED: Add a test that DWD SQL uses `shop_id + order_id` as the current-state key and orders by `update_time` then `collected_at`.
- Run the test and confirm it fails because the SQL file does not exist.
- GREEN: Create `TEXT2SQL-codex-handoff/sql/dwd_douyin_shop_order_current_di.sql`.
- Run `pytest tests/test_dwd_douyin_order_current.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

4.3 Modify `TEXT2SQL-codex-handoff/sql/dwd_douyin_shop_order_current_di.sql`.
- RED: Add a test that payment-date order count filters `pay_time > 0` and excludes `main_status_desc = '未支付取消'`.
- Run the test and confirm it fails if the SQL lacks the payment-date quality query.
- GREEN: Add validation SQL for daily paid order count by shop.
- Run `pytest tests/test_dwd_douyin_order_current.py` and confirm it passes.
- Commit step: record changed files because this workspace has no active git metadata.

## Batch 5: Migrate `/order/searchList`

Depends on: Batch 3 and Batch 4

5.1 Modify `TEXT2SQL-codex-handoff/app/services/douyin_order_ingestion_job.py`.
- RED: Add a runner integration test that task code `douyin_order_searchlist_daily` uses the existing Douyin connector and writes run status.
- Run the test and confirm it fails because adapter registration is missing.
- GREEN: Register `/order/searchList` as a framework task adapter.
- Run targeted API ingestion tests and existing Douyin tests.
- Commit step: record changed files because this workspace has no active git metadata.

5.2 Modify `TEXT2SQL-codex-handoff/scripts/douyin_order_searchlist_ingest.py`.
- RED: Add a compatibility test that old CLI emits a deprecation note and delegates to framework runner.
- Run the test and confirm it fails.
- GREEN: Replace internal orchestration with a call into `ApiIngestionRunner`.
- Run existing Douyin tests and CLI smoke.
- Commit step: record changed files because this workspace has no active git metadata.

5.3 Execute Doris migration SQL.
- RED: Run read-only existence checks and confirm runtime tables or DWD table are absent.
- GREEN: Execute `sql/api_ingestion_runtime_tables.sql` and `sql/dwd_douyin_shop_order_current_di.sql` against Doris.
- Run validation SQL for DWD current-state row counts and paid-date daily counts.
- Confirm no existing CONNECT/ODS data was deleted.
- Commit step: record execution evidence in `STATE-CURRENT.md`.

5.4 Publish DolphinScheduler workflow through framework scheduler.
- RED: Run dry-run publish and confirm rawScript uses `scripts/api_ingestion.py`.
- GREEN: Publish or update workflow `ODS_抖店订单列表接口采集__0715` through framework scheduler.
- Run worker-side dry-run and one narrow live window.
- Confirm DolphinScheduler schedule is ONLINE and run status appears in Doris.
- Commit step: record execution evidence in `STATE-CURRENT.md`.

## Batch 6: Verification And Governance

Depends on: Batch 5

6.1 Modify `TEXT2SQL-codex-handoff/app/api/routers/integration.py`.
- RED: Add API test that integration overview returns API ingestion task definitions and recent run status.
- Run the test and confirm it fails.
- GREEN: Expose task and run status through existing integration router.
- Run integration router tests.
- Commit step: record changed files because this workspace has no active git metadata.

6.2 Modify `TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md`.
- RED: Check that current state lacks the API production framework section.
- GREEN: Add current operational truth: framework task code, runtime tables, DWD current table, scheduler workflow, quality gates and known limits.
- Verify the file is readable as UTF-8.
- Commit step: record changed file in final summary.

6.3 Record OPSE evaluation.
- RED: Confirm no `api-ingestion-production-framework` OPSE record exists.
- GREEN: Append OPSE evaluation after tests, Doris validation and scheduler validation pass.
- Verify JSONL parses.
- Commit step: report OPSE score and evidence.
