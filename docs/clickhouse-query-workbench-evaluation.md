# ClickHouse 查询工作台产品和技术评估

更新时间：2026-07-24

## 1. 目标判断

当前需求不是做 AI 对话工具，而是给数仓清洗、建模和 SQL 生成结果提供一个可靠的人工验证工作台。核心链路是：查看数据库、查看表、查看字段、查看建表语句、查看样例数据、粘贴 SQL、执行只读查询、查看结果、保存查询、记录验证备注。

结论：建议进入分支 C，开发轻量自定义工具第一版。原因不是现成工具完全不可用，而是当前项目的关键要求包括后端只读白名单、禁止多语句、默认 LIMIT、查询审计、验证备注、前端不保存 ClickHouse 密码、后续与 Git 发布包衔接。这些要求已经超出普通 SQL Web UI 的默认边界。

## 2. 工具评估

| 工具 | 覆盖能力 | 不足 | 当前适配度 |
| --- | --- | --- | --- |
| ClickHouse 自带 SQL Console / Web UI | ClickHouse Cloud 的 SQL Console 适合云上浏览表、运行 SQL、看结果；自建 ClickHouse 的 HTTP 接口和 `/play` 更偏基础查询入口 | 对自建本地 ClickHouse 的团队化查询历史、收藏、审计、验证备注、统一只读网关支持不足 | 中 |
| Tabix | 面向 ClickHouse 的 SQL 编辑和表浏览，轻量，适合个人快速查询 | 项目维护活跃度和安全治理能力需要谨慎；通常更像前端 SQL 客户端，不适合作为本项目唯一审计入口 | 中低 |
| Apache Superset | SQL Lab、保存查询、图表、权限和 BI 协作较强；项目已要求保留 Superset | 偏 BI 平台；查看建表语句、验证备注、SQL 白名单、默认 LIMIT 和模型发布关联需要额外流程；当前本地 Superset 最近状态为不可用 | 中 |
| Metabase | 面向业务分析和图表，交互友好，适合看板和轻量自助分析 | ClickHouse 支持依赖驱动/版本适配；SQL 工程验证、DDL 查看、发布关联和严格只读网关不是强项 | 中低 |
| CH-UI 等 ClickHouse Web UI | 更贴近 ClickHouse 查询工作台，表浏览和 SQL 执行体验更好 | 仍需确认密码保存位置、审计、默认 LIMIT、风险 SQL 拦截和验证备注；不能替代项目级发布流程 | 中 |

参考来源：

- ClickHouse 官方文档：`https://clickhouse.com/docs/`
- ClickHouse HTTP 接口：`https://clickhouse.com/docs/interfaces/http`
- ClickHouse Cloud SQL Console：`https://clickhouse.com/docs/cloud/get-started/sql-console`
- Apache Superset 官方文档：`https://superset.apache.org/docs/`
- Metabase 官方文档：`https://www.metabase.com/docs/`
- Tabix GitHub：`https://github.com/tabixio/tabix`
- CH-UI GitHub：`https://github.com/caioricciuti/ch-ui`

## 3. 需求归类

属于 SQL 查询工具的需求：

- 查看数据库、表、字段、字段类型。
- 查看建表语句和样例数据。
- 手写、粘贴和执行只读 SQL。
- 查看查询结果、耗时、行数和错误。
- 复制 SQL 和结果。
- 保存常用查询和查看查询历史。

属于数仓工程和版本管理的需求：

- 验证 AI 生成的数据清洗和建模 SQL。
- 将验证结论关联到 Git 发布包、清洗契约、质量门禁和 OpenMetadata。
- DDL、DWD 发布、回滚、元数据同步必须继续走 `warehouse-release.cmd` 和 `sync-openmetadata.cmd`，不能放进查询工作台默认模式。

不应该放进第一版工作台的需求：

- AI 对话、AI 自动生成 SQL。
- 自动清洗、自动建模、自动发布。
- 复杂血缘图和多角色审批。
- 默认 DDL 或写入操作。若以后需要，必须做独立管理模式，不能混入只读查询模式。

## 4. 分支选择

选择分支 C：开发轻量自定义工具。

最小不可替代功能：

- 后端统一代理 ClickHouse，前端不保存密码、不直连 ClickHouse。
- SQL 只读白名单：只允许 `SELECT`、`WITH ... SELECT`、`SHOW`、`DESCRIBE`、`EXPLAIN`。
- 禁止多语句和危险关键字。
- 默认 LIMIT 和最大返回行数。
- 查询超时。
- 错误信息脱敏。
- 查询历史、收藏和验证备注落本地审计文件。
- Demo 模式，ClickHouse 不可用时仍可打开界面验证主链路。

## 5. 与 Git / dbt / SQLMesh 的衔接

第一版只做“验证工作台”，不做版本发布器。

- AI 生成或人工确认的正式 SQL 继续进入 Git 发布包。
- 工作台查询历史可记录 `发布版本`、`验证对象`、`验证备注`，作为后续发布报告或问题定位证据。
- 后续接 dbt 或 SQLMesh 时，工作台只负责读取模型 SQL、执行只读验证和记录结果；模型编排、依赖解析、环境切换、发布和回滚仍由 Git + 发布工具负责。

