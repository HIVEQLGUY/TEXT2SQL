# Agent 上下文与信息结构

更新时间：2026-07-19

## 当前信息入口

- 强规则：`C:\Users\24796\Documents\TEXT2SQL\AGENTS.md`
- 当前状态：`TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md`
- 当前资源：`TEXT2SQL-codex-handoff/docs/RESOURCE-资源登记.md`
- 统一凭据：`C:\Users\24796\Documents\TEXT2SQL\local\credentials\`
- 当前运行说明：`TEXT2SQL-codex-handoff/docs/RUNBOOK-组件启停与稳定性.md`

## 当前事实边界

未来方向是：

```text
预策数据接入层 -> ClickHouse -> 数仓可行性测试/建模验证
```

以下内容只作为历史，不再作为当前事实：

- 旧 RDS / Text2SQL 问数链路。
- DataAgent API 统一访问层。
- Doris `agent_warehouse`。
- Doris CONNECT/ODS 自研接口接入。
- DataX-Web、SeaTunnel、DolphinScheduler 在本项目内承载接入任务。
- 旧 Superset/Doris 演示看板。

## 历史资料位置

历史接口接入代码与说明已单独留存在桌面压缩包：

```text
C:\Users\24796\Desktop\youmei-api-ingestion-archive-20260719.zip
```

后续不要再依赖旧 `CHECKPOINT`、旧 handoff 或历史临时文档判断当前方向。
