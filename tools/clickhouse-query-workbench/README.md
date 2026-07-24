# ClickHouse 查询工作台

这是项目内的最小自研查询工作台，用于人工验证 ClickHouse 数仓清洗、建模和 AI 生成 SQL 的结果。第一版不包含 AI 对话、自动建模、自动发布或管理模式。

## 当前边界

- 前端不保存 ClickHouse 密码。
- 前端不直连 ClickHouse，所有查询必须经过后端。
- 默认只允许 `SELECT`、`WITH ... SELECT`、`SHOW`、`DESCRIBE`、`EXPLAIN`。
- 默认禁止多语句和写入/管理类 SQL。
- 默认追加 `LIMIT`，并通过 ClickHouse 查询设置限制返回行数和执行时间。
- 查询历史、收藏和验证备注写入 `WORKBENCH_AUDIT_DIR`。
- 当前不适合公网直接暴露，只允许本机或内网受控访问。

## 本地启动

```powershell
cd C:\Users\24796\Documents\TEXT2SQL\tools\clickhouse-query-workbench
Copy-Item .env.example .env
npm install
npm run dev
```

访问：

```text
http://127.0.0.1:5177
```

Demo 模式默认开启。要连接真实 ClickHouse，将 `.env` 中的 `WORKBENCH_DEMO_MODE` 改成 `false`，并配置只读账号。

## 只读账号建议

不要把生产管理员账号配置给工作台。推荐使用 `config/clickhouse/query-workbench-readonly-user.template.sql` 作为模板，由人工替换密码后执行。

## 验证命令

```powershell
npm run typecheck
npm run lint
npm run test
npm run build
```

## 与发布流程的关系

工作台只负责查询验证和记录备注。正式 ClickHouse 表结构、字段、口径、发布、回滚和 OpenMetadata 同步仍必须走项目发布入口：

```powershell
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd --release <发布YAML> --mode full
```

