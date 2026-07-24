# 执行契约：抖店订单采集生产运行环境硬化

## Intent Lock

把抖店订单每日采集从“可由 Codex 临时执行”提升为“本地 DolphinScheduler worker 侧可独立执行并可验证”的生产运行链路。

## Scope Fence

包含：
- worker 侧运行环境 probe。
- DolphinScheduler 每日任务状态和命令验证。
- 必要时更新调度注册脚本。
- 状态文档和 OPSE 记录。

不包含：
- 重新设计 CONNECT/ODS 表。
- 新增其他抖店接口。
- 改走 MySQL、DataX 或 SeaTunnel。
- DWD/DIM/DWS/ADS 建模。

## Approved Behavior

- Runtime probe MUST not print secrets.
- Runtime probe MUST run inside `youmei-dolphinscheduler`.
- DolphinScheduler workflow `ODS_抖店订单列表接口采集__0715` MUST remain ONLINE.
- The scheduled shell command MUST call `scripts/douyin_order_searchlist_ingest.py daily`.
- Verification MUST include platform health, worker-side egress IP, Doris connectivity, and schedule state.

## Test Obligations

- Run runtime probe locally and inside worker.
- Run DolphinScheduler schedule API inspection.
- Run at least targeted Python tests if code changes are made.
- Validate no plaintext app secret or token is printed.

## Execution Batches

### Batch 1: Runtime Probe

Done when `verify_douyin_order_runtime.py` exists, returns JSON, hides secrets, and runs inside worker.

### Batch 2: Scheduler Verification

Done when workflow state, cron, and command are verified through DolphinScheduler API.

### Batch 3: Documentation And Evaluation

Done when `STATE-CURRENT.md` records the worker-side production evidence and OPSE is recorded if production readiness changed.

## Review Gates

- After Batch 1, review probe output for secret leakage before sharing or documenting it.
- After Batch 2, verify schedule evidence through API rather than UI-only observation.
- After Batch 3, run final tests and report residual risks.

## Rewind Triggers

- Worker egress IP differs from the抖店白名单 and API requests fail because of IP restriction.
- Worker cannot access `.env`, Doris, or project files.
- DolphinScheduler command points to a Codex-only or Windows-only path.

## Approval Gate

DP-3: 用户已批准按“落到本地服务器/调度器侧运行并验证稳定性”的方案继续执行。
