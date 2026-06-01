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

用户已说明：

- 数仓元数据已经由用户自己的工具写入元数据库。
- 当前元数据核心表共两张：
  - `table_dictionary`：数仓字典 / 表字典。
  - `metric_dictionary`：指标字典 / 字段指标字典。
- 用户理解这两张表足够支撑召回，后续如不够再调整表结构。
- 问数执行数据库中已新增一张测试表，表结构已存在，数据可能不完整。

Codex 已初步读取到：

- 元数据库 `youmei_ai`：
  - `table_dictionary`：41 行。
  - `metric_dictionary`：1394 行。
  - 另有一张 `dws_tmall_sales_link_summary`，看起来是旧/示例数据表，不属于当前两张核心字典。
- 问数执行库 `chatsql_ai`：
  - `dws_douyin_spu_sales_detail`：表结构已存在，当前约 87579 行。

当前重要疑点：

- `table_dictionary.bywm` 是表英文名。
- `table_dictionary.bzwm` 是表中文名。
- `metric_dictionary.zdywmc` 是字段英文名称。
- `metric_dictionary.zdzwmc` 是字段中文名称。
- `metric_dictionary.ssscb` 字段注释为“所属数仓表”，但当前值看起来像内部标识，不直接等于 `table_dictionary.bywm`。
- 尝试 `metric_dictionary.ssscb = table_dictionary.bywm`，匹配数为 0。
- 尝试 `FIND_IN_SET(metric_dictionary.ssscb, table_dictionary.bhzd)`，匹配数也为 0。
- 因此 M2 第一件事不是写复杂代码，而是确认两张字典的真实关联键：`ssscb` 到底关联哪一列，或是否需要额外映射。

建议顺序：

1. 复测本地 `.env` 中 `META_DB_*` 指向旧 RDS、`DW_DB_*` 指向新 RDS 后的 `GET /api/health/db`。
2. 读取旧 RDS `youmei_ai` 中现有元数据表清单和字段结构。
3. 确认 `table_dictionary` 和 `metric_dictionary` 的真实关联键。
4. 若关联键不在现有字段中，先做文本召回适配，或请用户补充一个稳定关联字段。
5. 建立 Repository 层，先支持读取表字典、指标字典、按关键词检索。
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

## 8. 2026-06-01 最新进展：M2 元数据读取 API 已启动

用户已重新调整元数据库中的两张字典表，现在可以稳定关联：

```text
table_dictionary.bbs = 表标识
metric_dictionary.zdbs = 字段标识
metric_dictionary.ssscb = 所属表标识
主关联关系：metric_dictionary.ssscb = table_dictionary.bbs
```

当前探查结果：

```text
table_dictionary: 41 行
metric_dictionary: 1394 行
带非空所属表标识的字段: 1261 条
按 ssscb -> bbs 可匹配字段: 1261 条
未匹配字段: 0 条
```

当前可用于后续测试的抖音 SPU 销售明细元数据：

```text
table_id: hKrBQ2zwwG
table_name: ud_3418004512502203_dyxsjyzhb
table_display_name: DWS_抖音_SPU销售明细
```

已新增 M2 初版代码：

```text
app/repositories/metadata_repository.py
app/api/routers/metadata.py
```

已挂载接口：

```text
GET /api/metadata/summary
GET /api/metadata/tables?q=&limit=
GET /api/metadata/fields?q=&table_id=&table_name=&limit=
GET /api/metadata/tables/{table_id}/fields
```

已验证：

```text
python -m compileall app 通过
GET /api/metadata/summary 返回 table_count=41, field_count=1394, associated_field_count=1261
GET /api/metadata/tables?q=SPU&limit=5 能找到 DWS_抖音_SPU销售明细
GET /api/metadata/fields?table_id=hKrBQ2zwwG&limit=3 能返回该表字段
```

下一步建议：

1. 在 M2 内继续做元数据召回服务，输入自然语言问题，输出候选表、候选字段、业务定义、计算公式和注意事项。
2. 确认元数据库表名与问数执行库物理表名之间的映射策略。当前元数据中 `DWS_抖音_SPU销售明细` 的英文名是 `ud_3418004512502203_dyxsjyzhb`，问数执行库中测试物理表是 `dws_douyin_spu_sales_detail`，两者不完全一致。
3. 召回上下文稳定后，再进入 SQL 生成、SQL 安全校验和执行闭环。

## 9. 2026-06-01 最新进展：M2 元数据召回服务初版

已新增召回服务：

```text
app/services/metadata_retrieval_service.py
```

已新增接口：

```text
GET /api/metadata/retrieve?question=&table_limit=&field_limit=&fields_per_table=
```

当前实现：

- 从自然语言问题中抽取英文/数字 token 和中文 ngram。
- 使用元数据库 LIKE 检索表字典和字段/指标字典。
- 在服务层做轻量打分，输出候选表、候选字段和每张表的字段上下文。
- 明确表名词权重较高，例如问题中出现 `SPU` 时，`DWS_抖音_SPU销售明细` 会排在第一候选。
- 已优化为批量查询，避免按词或按表循环创建 RDS 连接。
- metadata API 已把 PyMySQL 异常包装成 HTTP 503，避免 RDS 外网抖动时裸抛内部堆栈。

验证样例：

```text
GET /api/metadata/retrieve?question=SPU 销售金额 店铺&table_limit=3&field_limit=8&fields_per_table=5
```

返回第一候选表：

```text
table_id: hKrBQ2zwwG
table_name: ud_3418004512502203_dyxsjyzhb
table_display_name: DWS_抖音_SPU销售明细
```

注意：

- 本地 PowerShell 输出中文 JSON 时可能显示乱码，但 API 实际返回为 UTF-8。
- RDS 外网连接偶发超时，健康检查中 metadata/warehouse DB 连接耗时约 3-4 秒，后续若变严重应考虑连接池、服务端部署或内网连接。
- 用户说明元数据表名明天会更新；当前“元数据表名与执行库物理表名不一致”暂不阻塞 M2 召回。

下一步建议：

1. 增加上下文构建服务，把候选表/字段整理成 LLM 生成 SQL 前可直接消费的结构。
2. 用户更新元数据表名后，复测物理表映射。
3. 在上下文稳定后进入 SQL 生成节点和 SQL 安全执行闭环。
