# Test Bench

本地测试台用于验证数据库连接、元数据理解、取数 Agent 流程、SQL 审查、只读执行、结果展示和运行记录。

## Start

```powershell
python app/server.py
```

打开：

```text
http://127.0.0.1:8765
```

## Features

- 连接状态：显示 host、database、user、MySQL version、延迟。
- 心跳检测：网页每 10 秒调用一次 `/api/heartbeat`，断联会显示异常。
- 元数据：读取 `information_schema.tables` 和 `information_schema.columns`。
- 取数 Agent：支持元数据引导、SQL 审查、只读查询执行。
- 风险控制：硬拦截危险 SQL，风险 SQL 默认不执行。
- 图表：当结果包含维度列和数值列时自动绘制条形图。
- 记录：每次问题、SQL、审查、执行耗时、行数、结果预览会保存到本地 SQLite。

## Runtime Files

本地运行记录保存在：

```text
.runtime/text2sql_runs.sqlite3
```

该目录被 `.gitignore` 忽略，不会提交到 GitHub。

## Current Limitation

当前网页 Agent 尚未接入大模型 API。复杂自然语言到 SQL 的生成阶段先由 Codex 协助完成，网页负责审查、执行、可视化和记录。后续可接入 OpenAI API、本地模型或 MCP Server。
