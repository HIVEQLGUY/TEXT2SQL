# 组件启停与稳定性

更新时间：2026-07-19

## 当前运行口径

旧 DataAgent/Doris/DataX/SeaTunnel 演示栈不再作为未来方向维护。Superset 和 DolphinScheduler 仍需保留，不能作为 Doris 附带项删除。

当前只保留 ClickHouse 可行性测试相关运行口径：

```text
本机 WSL ClickHouse
  -> youmei_sandbox
  -> 必要时通过 120.26.202.216:28123 供外部工具/魔方访问
```

## ClickHouse 通道

本机入口：

```text
127.0.0.1:8123
127.0.0.1:9000
```

外部工具代理：

```text
120.26.202.216:28123
```

相关脚本：

```text
ops/devbox/clickhouse_tool_tunnel.sh
ops/devbox/clickhouse_tool_tunnel_supervisor.ps1
ops/devbox/clickhouse_openmetadata_bridge_proxy.py
```

## 历史组件

以下组件若仍残留，只作为待清理历史资源：

- Doris FE/BE
- DataAgent API
- DataX-Web
- SeaTunnel / SeaTunnel Web
- 旧 OpenMetadata 到 Doris 元数据链路

删除这些组件前，必须确认容器名、目录或端口属于本项目。

## 保留组件

- Superset：`http://127.0.0.1:8088`
- DolphinScheduler：`http://127.0.0.1:12345/dolphinscheduler/ui/`

这两个组件后续需要保留。除非用户明确点名删除，不得下线。
