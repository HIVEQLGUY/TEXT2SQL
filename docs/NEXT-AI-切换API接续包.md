# 切换 API 接续包

用途：当用户切换 API、模型或新会话时，可以把本文件内容直接发给下一个 AI，让它快速接手本项目。本文不包含真实密码、Token、私钥正文。

维护规则：

- 本文件是切换 API 时的唯一固定接续包，应提交到 Git。
- 后续开发中只更新本文件，不新建 `NEXT-AI-xxx`、`handoff-2`、`会话总结-日期` 等平行归档。
- 每次完成关键资源确认、架构决策、阶段开发、测试验证或阻塞解除后，都要同步覆盖更新本文件。
- 如果额度突然耗尽，用户可以让下一个 AI 登录 Git、读取本文件和 `docs/HANDOFF-新会话接续说明.md` 来恢复最新上下文。
- 真实密码、Token、私钥正文仍只保存在本地 `local/` 或 `.env*`，不进入本文件。

## 1. 项目定位

本项目仓库：

```text
https://github.com/HIVEQLGUY/TEXT2SQL.git
```

当前分支：

```text
codex/bootstrap-foundation
```

项目目标是建设一个真实业务可用的智能问数系统，不是复刻教程里的电商 demo。

第一阶段优先跑通抖音主题域：

- 用户自然语言提问。
- 系统基于元数据、字段含义、计算口径、字段依赖和真实字段值召回上下文。
- 大模型生成 SQL。
- SQL 经过安全审查、语法/执行计划校验和风险校验。
- 使用只读账号执行 SQL。
- 返回结构化结果、图表建议和完整运行记录。

## 2. 必读文件顺序

新 AI 接手后，先读这些文件：

1. `docs/HANDOFF-新会话接续说明.md`
2. `docs/CHECKPOINT-项目检查点.md`
3. `docs/RESOURCE-资源登记.md`
4. `docs/MEMORY-重要信息记录规范.md`
5. `docs/CHAT-沟通记录摘要.md`
6. `docs/PRD-智能问数项目概览.md`
7. `docs/ARCH-智能问数系统架构草案.md`
8. `docs/PLAN-第一阶段落地方案.md`
9. `docs/CHECKLIST-资源与权限确认.md`

如果需要登录服务器或连接数据库，再读取本机文件：

```text
local/SECRETS-实际账号.md
.env
.env.reader
local/ssh/text2sql_codex_ed25519_v2
```

注意：`local/`、`.env*`、`.venv/`、`.runtime/` 都被 `.gitignore` 忽略，不提交 Git。

## 3. 资源状态

云服务器：

```text
IP: 114.55.148.140
SSH 用户: root
SSH 私钥: local/ssh/text2sql_codex_ed25519_v2
状态: SSH 登录成功
```

RDS：

```text
类型: 阿里云 RDS MySQL
host: rm-2zea6b6dcxxq17753zo.mysql.rds.aliyuncs.com
port: 3306
database: chatsql_ai
账号: chat_ai_duckdb_2
密码: 见 local/SECRETS-实际账号.md
状态: 从本地 FastAPI/PyMySQL 和云服务器 mysql 客户端均已连接成功
```

MySQL 认证注意事项：

- RDS 使用 MySQL 8。
- 当前账号涉及 `caching_sha2_password`。
- 命令行客户端从服务器端连接时需要 `--get-server-public-key`。
- 本地 `.env` 已设置：

```text
META_DB_MYSQL_GET_SERVER_PUBLIC_KEY=true
DW_DB_MYSQL_GET_SERVER_PUBLIC_KEY=true
DB_MYSQL_GET_SERVER_PUBLIC_KEY=true
```

## 4. 当前代码状态

正式代码已从干净的 `app/` 目录开始搭建。

已完成 M1 的主要基础：

- `pyproject.toml`：声明项目依赖。
- `.env.example`：本地配置模板。
- `config/database.example.env`：旧 RDS 示例已清理为占位模板。
- `app/api/main.py`：FastAPI 应用入口。
- `app/api/routers/health.py`：健康检查接口。
- `app/core/config.py`：标准库配置加载，支持 `META_DB_*`、`DW_DB_*`、兼容 `DB_*`。
- `app/core/request_context.py`：`request_id` 上下文。
- `app/core/logging.py`：日志中带 `request_id`。
- `app/clients/mysql.py`：PyMySQL 数据库连接和 ping。
- `app/services/sql_safety_service.py`：SQL 只读安全审查，迁移自旧原型思想。

已验证：

```text
python -m compileall app 通过
GET /api/ready 返回 ok=true
GET /api/health/db 返回 ok=true
metadata_db 和 warehouse_db 均连接 RDS 成功
```

本地 API：

```text
http://127.0.0.1:8000
```

启动方式：

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

当前后台运行信息：

```text
.runtime/uvicorn.pid
.runtime/uvicorn.err.log
.runtime/uvicorn.out.log
```

## 5. 重要约定

- 不要把真实密码、Token、私钥正文提交到 Git。
- 真实密钥只写入 `local/SECRETS-实际账号.md` 或 `.env*`。
- 切换 API 的最新接续信息只更新本文件，不创建多份接续包。
- 资源索引写入 `docs/RESOURCE-资源登记.md`。
- 阶段结论写入 `docs/CHECKPOINT-项目检查点.md`。
- 新会话入口写入 `docs/HANDOFF-新会话接续说明.md`。
- 重要信息不要只留在聊天里。
- 不要继续在 `legacy/prototype-20260523/` 上堆正式功能，只作参考。
- `web/` 和 `.tmp-data-analysis-agent/` 当前是未跟踪目录，之前未处理，接手时不要误删。

## 6. 架构方向

已确认方向：

- 后端：FastAPI。
- 流式协议：SSE。
- 工作流：LangGraph 或至少保持同等节点化结构。
- 元数据入口：钉钉 AI 表格。
- 运行时元数据：项目自己的元数据库。
- 检索：字段语义检索 + 字段值检索 + 字段依赖/计算公式上下文。
- 未来可接 Elasticsearch/OpenSearch 或 Qdrant/pgvector，第一阶段先保留可插拔接口。
- SQL：生成后必须经过安全审查、语法校验、风险校验，再执行。
- 日志：从第一阶段引入 `request_id`、`run_id`、`step_id`。

关于 ES/OpenSearch：

- 元数据未来可能写入 ES/OpenSearch，用于字段值检索、关键词检索或混合检索。
- 这不阻塞当前 M1/M2。
- 当前应先把关系型元数据库表结构、Repository 和同步边界建好。

## 7. 下一步该做什么

下一步进入 M2：元数据库表结构与 Repository。

建议顺序：

1. 确认 `chat_ai_duckdb_2` 的权限边界。
   - 如果它是问数执行账号，应保持只读。
   - 如果需要写元数据库，建议另建 `meta_app` 写账号。
2. 设计第一版元数据库表结构：
   - `meta_table`
   - `meta_field`
   - `meta_field_dependency`
   - `meta_field_value`
   - `meta_sync_job`
   - `meta_sync_change_log`
   - `query_run`
   - `query_step`
3. 建立初始化脚本。
4. 建立 Repository 层。
5. 增加 `GET /api/metadata/tables` 和 `GET /api/metadata/fields` 的空实现或数据库实现。
6. 后续再进入 M3：钉钉 AI 表格同步。

建议不要现在直接做大模型 SQL 生成。当前优先级是：

```text
资源与连接稳定
-> 元数据库结构
-> 元数据同步
-> 检索上下文
-> 问数工作流
-> SQL 生成与执行闭环
```
