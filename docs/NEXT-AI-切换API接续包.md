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
- 数仓元数据由用户已有工具从钉钉维护侧定期写入元数据库，本项目不再重复实现钉钉同步链路。
- 系统基于元数据库中的字段含义、计算口径、字段依赖和真实字段值召回上下文。
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
元数据库: 旧阿里云 RDS MySQL
host: rm-bp1mx4778wjne596xko.mysql.rds.aliyuncs.com
port: 3306
database: youmei_ai
账号: baoyan
密码: 见 local/SECRETS-实际账号.md
状态: 从云服务器 mysql 客户端已连接成功
```

问数执行数据库：

```text
类型: 新阿里云 RDS MySQL，高读写 DB
host: rm-2zea6b6dcxxq17753zo.mysql.rds.aliyuncs.com
port: 3306
database: chatsql_ai
账号: chat_ai_duckdb_2
密码: 见 local/SECRETS-实际账号.md
状态: 从本地 FastAPI/PyMySQL 和云服务器 mysql 客户端均已连接成功
```

账号策略：

- 当前只是测试流程，新 RDS 暂不强制单独只读账号。
- 后续进入健壮性和安全收敛阶段，再重新配置只读问数执行账号。
- M2 元数据库表结构应建在旧 RDS `youmei_ai` 中。

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
metadata_db 连接旧 RDS youmei_ai 成功，用户 baoyan@%
warehouse_db 连接新 RDS chatsql_ai 成功，用户 chat_ai_duckdb_2@%
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

当前本地 `.env` 状态：

```text
META_DB_* -> 旧 RDS youmei_ai
DW_DB_* -> 新 RDS chatsql_ai
DB_* -> 新 RDS chatsql_ai，兼容旧原型脚本
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
- 元数据入口：钉钉 AI 表格由用户已有工具负责维护和定期写入元数据库。
- 运行时元数据：项目自己的元数据库。
- 检索：字段语义检索 + 字段值检索 + 字段依赖/计算公式上下文。
- 未来可接 Elasticsearch/OpenSearch 或 Qdrant/pgvector，第一阶段先保留可插拔接口。
- SQL：生成后必须经过安全审查、语法校验、风险校验，再执行。
- 日志：从第一阶段引入 `request_id`、`run_id`、`step_id`。

关于元数据同步和 ES/OpenSearch：

- 钉钉到元数据库的定期写入已由用户自己的工具完成，本项目当前不实现 M3 钉钉同步。
- 元数据未来可能写入 ES/OpenSearch，用于字段值检索、关键词检索或混合检索。
- 这不阻塞当前 M1/M2。
- 当前应先读取/适配已有元数据库表结构，建立 Repository 和索引刷新边界。

## 7. 下一步该做什么

下一步进入 M2：现有元数据库结构发现、字段映射与 Repository。

建议顺序：

1. 复测本地 `.env` 中 `META_DB_*` 指向旧 RDS、`DW_DB_*` 指向新 RDS 后的 `GET /api/health/db`。
2. 读取旧 RDS `youmei_ai` 中现有元数据表清单和字段结构。
3. 判断已有工具写入的表是否已经覆盖：
   - `meta_table`
   - `meta_field`
   - `meta_field_dependency`
   - `meta_field_value`
   - `query_run`
   - `query_step`
4. 若已有表名/字段名和项目建议模型不同，优先做适配层，不急着改上游表。
5. 建立 Repository 层，先支持读取表元数据、字段元数据、字段依赖。
6. 增加 `GET /api/metadata/tables` 和 `GET /api/metadata/fields`。
7. 原 M3 改为“元数据索引刷新”：基于元数据库写入 ES/OpenSearch/向量库，而不是接钉钉 API。

建议不要现在直接做大模型 SQL 生成。当前优先级是：

```text
资源与连接稳定
-> 现有元数据库结构适配
-> 元数据读取 API
-> 检索上下文
-> 问数工作流
-> SQL 生成与执行闭环
```
