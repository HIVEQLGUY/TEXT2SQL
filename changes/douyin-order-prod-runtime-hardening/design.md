# 抖店订单采集生产运行环境硬化设计

## Context

当前 `/order/searchList` 已经接入 Doris CONNECT/ODS，并完成 2026 年 6 月两家店铺回灌。每日调度已经注册到 DolphinScheduler，但用户关心实际执行是否依赖 Codex 当前桌面网络，以及迁到本地服务器侧是否更稳定。DolphinScheduler 容器 `youmei-dolphinscheduler` 运行在 WSL/Docker host networking 下，项目挂载在 `/workspace/TEXT2SQL/TEXT2SQL-codex-handoff`。

约束：
- API 采集必须保持 code connector -> Doris CONNECT/ODS。
- 凭据不能写入代码或输出日志。
- 生产调度必须通过 DolphinScheduler 官方 API 和 worker 执行证据确认。

## Goals

- 明确当前每日采集由 DolphinScheduler worker 执行，而不是 Codex 会话执行。
- 验证 worker 侧网络出口和 Doris 写入链路。
- 留下可重复验证入口，后续换服务器时直接运行同一检查。

## Decisions

### Decision 1: 使用 worker 内部 probe 作为生产运行环境门禁

Choice: 新增轻量验证脚本，从 worker 容器中检查 Python、项目挂载、外网出口、Doris HTTP/MySQL 连通性和抖店配置存在性。

Rationale: 这能直接回答运行环境是否可独立工作，不需要触发大窗口采集，也不会依赖 Codex 当前进程。

Alternatives: 只看 schedule ONLINE 状态。这个方式不足，因为 ONLINE 不能证明 worker 能访问外网和 Doris。

### Decision 2: 每日正式采集仍使用现有 ingestion CLI

Choice: DolphinScheduler shell command 继续调用 `scripts/douyin_order_searchlist_ingest.py daily`。

Rationale: 核心采集能力已经验证，生产化重点是执行环境和证据，不再复制采集逻辑。

Alternatives: 把采集逻辑写进 DolphinScheduler 任务脚本。这个方式会产生双份逻辑，后续维护风险更高。

## Risks And Trade-Offs

- 外网出口 IP 可能随代理、VPN 或服务器迁移变化；如果变更，需要同步更新抖店开放平台 IP 白名单。
- 非 mutating probe 不能证明 Stream Load 全链路写入；必要时使用极小窗口采集作为补充证据。
- 当前 ODS 表是源形态记录表，不是最终唯一化服务表；重复窗口采集后的下游唯一化仍应在 DWD/DIM/DWS 侧处理。
