# 抖店订单采集生产运行环境硬化

## Why

6 月订单回灌已经证明 `/order/searchList` 接口和 Doris CONNECT/ODS 落库链路可用，但长时间回灌暴露了运行环境风险：如果采集由 Codex 当前桌面会话直接执行，网络出口、连接稳定性、进程生命周期和调度证据都不够生产化。这个变更要把抖店订单采集的日常运行责任明确落到本地 DolphinScheduler worker 侧，并验证 worker 环境可以独立访问抖店开放平台、读取本地凭据、写入 Doris，并留下可复核证据。

## What Changes

- 验证 DolphinScheduler worker 容器的 Python 运行时、项目挂载、`.env` 读取、外网出口和 Doris 访问能力。
- 验证现有 `ODS_抖店订单列表接口采集__0715` 每日任务确实从 DolphinScheduler worker 侧执行采集命令。
- 如发现调度命令缺少生产参数，更新注册脚本并重新注册。
- 增加一份生产运行检查脚本或验证入口，用于以后快速判断“采集是否在本地调度侧可运行”。
- 更新当前状态文档，记录生产运行入口、网络出口判断、调度状态和剩余风险。

## Scope

### In Scope

- 抖店订单 `/order/searchList` 已有采集链路的运行环境验证。
- DolphinScheduler workflow `ODS_抖店订单列表接口采集__0715`。
- 本地 Docker/WSL/DolphinScheduler worker 到抖店 OpenAPI 和 Doris 的连通性。
- 最小量真实采集或非破坏性 probe，用于证明 worker 侧链路可用。

### Out of Scope

- 不重新设计订单 CONNECT/ODS 表。
- 不新增其他抖店接口。
- 不调整 DWD/DIM/DWS/ADS 建模。
- 不把 API JSON 改走 MySQL、DataX 或 SeaTunnel。
- 不绕过抖店开放平台 IP 白名单、权限或店铺授权。

## Impact

- `TEXT2SQL-codex-handoff/scripts/sync_dolphinscheduler_douyin_order_schedule.py`
- `TEXT2SQL-codex-handoff/scripts/douyin_order_searchlist_ingest.py`
- 可选新增 `TEXT2SQL-codex-handoff/scripts/verify_douyin_order_runtime.py`
- `TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md`
- DolphinScheduler schedule id `51`

## Capabilities

### New Capabilities

- 一键验证抖店订单采集是否可由本地 DolphinScheduler worker 侧运行。
- 明确区分 Codex 桌面临时执行和 DolphinScheduler 生产执行。

### Modified Capabilities

- 每日采集调度从“已注册”升级为“worker 侧运行环境已验证”。
