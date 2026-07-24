# 任务清单：抖店订单采集生产运行环境硬化

## File Structure

- Create: `TEXT2SQL-codex-handoff/scripts/verify_douyin_order_runtime.py` - 验证 worker 环境、Doris 连通、外网出口和抖店配置状态。
- Modify: `TEXT2SQL-codex-handoff/scripts/sync_dolphinscheduler_douyin_order_schedule.py` - 确认每日命令保持生产入口，并可复核注册状态。
- Modify: `TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md` - 记录生产运行验证结果和迁移注意事项。

## Interfaces

### Batch 1 -> Batch 2
- **Produces**: `verify_douyin_order_runtime.py` JSON output - consumed by Batch 2 to validate worker-side runtime.

### Batch 2 -> Batch 3
- **Produces**: DolphinScheduler schedule/API evidence - consumed by Batch 3 for state documentation.

## Batch 1: Runtime Probe

Depends on: none

1.1 Create `TEXT2SQL-codex-handoff/scripts/verify_douyin_order_runtime.py`. [done]
- [done] Write a failing test by running the script path before creation and confirm the file is missing.
- [done] Implement JSON output for `python_ok`, `project_root_exists`, `env_file_exists`, `doris_http_configured`, `doris_mysql_connectivity`, `external_egress_ip`, and `douyin_credentials_configured`.
- [done] Ensure secret values are represented only as booleans.
- [done] Run the script locally and confirm JSON output.
- [done] Commit step: record changed file in the final summary because this workspace has no active git metadata.

1.2 Run the probe inside `youmei-dolphinscheduler`. [done]
- [done] Execute `docker exec youmei-dolphinscheduler python3 /workspace/TEXT2SQL/TEXT2SQL-codex-handoff/scripts/verify_douyin_order_runtime.py`.
- [done] Confirm exit code 0.
- [done] Record external egress IP and Doris connectivity result.

## Batch 2: Scheduler Verification

Depends on: Batch 1

2.1 Inspect current DolphinScheduler schedule. [done]
- [done] Use official API helper from `sync_dolphinscheduler_douyin_order_schedule.py`.
- [done] Confirm schedule id `51` or replacement schedule is ONLINE.
- [done] Confirm cron is `0 15 7 * * ?`.
- [done] Confirm command calls `scripts/douyin_order_searchlist_ingest.py daily`.

2.2 Run a worker-side low-risk command. [done]
- [done] Prefer non-mutating probe from Batch 1.
- [done] If write proof is needed, use a narrow current-day window and validate failed pages equal to zero.
- [done] Avoid large backfills during this hardening change.

## Batch 3: Documentation And Evaluation

Depends on: Batch 2

3.1 Update `TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md`. [done]
- [done] Record worker-side probe results.
- [done] Record whether the egress IP matches the current抖店 IP 白名单.
- [done] Record schedule status.

3.2 Run verification. [done]
- [done] Run relevant script checks and `pytest`.
- [done] Record OPSE eval if production-readiness status changes.
