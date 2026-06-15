# 项目检查点

本文件是固定检查点，不按会话新建。每次阶段性推进、资源变化、架构决策、风险发现，都更新这里。

## 使用规则

- 新会话接手时必须先读 `docs/HANDOFF-新会话接续说明.md`，再读本文件。
- 不要为每次对话新建单独交接文件。
- 重要信息只更新固定文件：
  - 资源索引：`docs/RESOURCE-资源登记.md`
  - 本地真实密钥：`local/SECRETS-实际账号.md`
  - 项目检查点：`docs/CHECKPOINT-项目检查点.md`
  - 长期沟通摘要：`docs/CHAT-沟通记录摘要.md`
  - 当前接续入口：`docs/HANDOFF-新会话接续说明.md`

## 检查点模板

```text
日期：
类型：资源 / 架构 / 开发 / 部署 / 风险 / 决策
摘要：
影响：
后续动作：
关联文件：
```

## 2026-05-31 资源记录机制

类型：决策

摘要：

- Git 不保存真实账号密码，但必须保存资源索引和凭证位置。
- 本地固定使用 `local/SECRETS-实际账号.md` 记录真实服务器、数据库、钉钉、大模型等敏感信息。
- `local/` 加入 `.gitignore`，只保存在本机。
- Git 固定使用 `docs/RESOURCE-资源登记.md` 记录资源登记、访问方式、账号用途和密钥文件位置。
- 后续开发途中重要信息默认更新固定记录文件，不再每次对话生成新的资源说明文件。

影响：

- 新会话可以从固定入口恢复上下文。
- 本地真实密码不进入 Git，但不会只存在聊天记录里。
- 后续若资源变化，需要同时更新资源登记和本地密钥文件。

后续动作：

- 用户重新提供新数据库和云服务器信息。
- Codex 更新 `local/SECRETS-实际账号.md` 的真实值。
- Codex 更新 `docs/RESOURCE-资源登记.md` 的脱敏资源索引。
- 完成连通性测试后，在本文件追加测试结果检查点。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`

## 2026-06-01 M2 元数据字典关联键确认与只读 API 初版

类型：开发 / 测试

摘要：

- 用户重新调整了元数据库中的两张字典表结构，新增/修正了可稳定关联的内部标识。
- `table_dictionary` 当前 41 行，核心表标识列为 `bbs`。
- `metric_dictionary` 当前 1394 行，核心字段标识列为 `zdbs`，所属表标识列为 `ssscb`。
- 已确认主关联关系：`metric_dictionary.ssscb = table_dictionary.bbs`。
- 带非空 `ssscb` 的字段共 1261 条，按上述主关联可全部匹配，未匹配数为 0。
- `table_dictionary.bhzd` 中也包含字段标识列表，可用 `FIND_IN_SET(metric_dictionary.zdbs, table_dictionary.bhzd)` 辅助校验，但不作为主关联键。
- 问数执行库 `chatsql_ai` 中存在测试表 `dws_douyin_spu_sales_detail`，元数据库中对应表元数据为：
  - `table_id = hKrBQ2zwwG`
  - `table_name = ud_3418004512502203_dyxsjyzhb`
  - `table_display_name = DWS_抖音_SPU销售明细`

已落地代码：

- 新增 `app/repositories/metadata_repository.py`，封装现有元数据字典表的只读访问和字段名适配。
- 新增 `app/api/routers/metadata.py`。
- 新增接口：
  - `GET /api/metadata/summary`
  - `GET /api/metadata/tables?q=&limit=`
  - `GET /api/metadata/fields?q=&table_id=&table_name=&limit=`
  - `GET /api/metadata/tables/{table_id}/fields`
- `app/api/main.py` 已挂载 metadata router。

验证：

- `python -m compileall app` 通过。
- 本地 Uvicorn 已重启并加载新路由。
- `GET /api/metadata/summary` 返回：
  - `table_count = 41`
  - `field_count = 1394`
  - `associated_field_count = 1261`
- `GET /api/metadata/tables?q=SPU&limit=5` 可返回 `hKrBQ2zwwG / ud_3418004512502203_dyxsjyzhb / DWS_抖音_SPU销售明细`。
- `GET /api/metadata/fields?table_id=hKrBQ2zwwG&limit=3` 可返回该表字段。

影响：

- M2 的第一阶段可以继续基于现有元数据表做召回上下文构建，不再阻塞于字典关联键。
- 后续检索层、ES/OpenSearch/向量索引层应优先依赖 API 层归一化后的字段名，而不是在多处硬编码上游中文缩写列名。

后续动作：

- 基于元数据 Repository 增加召回服务，先支持关键词召回表和字段。
- 建立自然语言问题到候选表/候选字段的上下文构建结构。
- 在进入 SQL 生成前，补充问数执行库真实表名和元数据库表名之间的映射策略；当前 `DWS_抖音_SPU销售明细` 的元数据英文名与执行库物理表名不完全一致，需要后续确认映射来源或规则。

关联文件：

- `app/repositories/metadata_repository.py`
- `app/api/routers/metadata.py`
- `app/api/main.py`
- `docs/NEXT-AI-切换API接续包.md`

## 2026-06-01 M2 元数据召回服务初版

类型：开发 / 测试

摘要：

- 新增 `app/services/metadata_retrieval_service.py`，提供从自然语言问题到候选表、候选字段和上下文片段的轻量召回服务。
- 新增接口 `GET /api/metadata/retrieve`。
- 当前实现先使用元数据库 LIKE 检索 + 服务层打分，不引入 ES/OpenSearch/向量库；后续可以替换服务内部实现，保持 API 形状稳定。
- 召回服务会抽取问题中的英文/数字 token 和中文 ngram，分别检索表字典、字段/指标字典。
- 已优化为批量检索：一次查候选表、一次查候选字段、一次批量补候选表字段，避免按关键词或按表循环建立 RDS 连接。
- 明确表名词权重更高，例如问题中出现 `SPU` 时，`DWS_抖音_SPU销售明细` 会优先排在相关字段命中表之前。
- metadata API 已对 PyMySQL 异常做 503 包装，避免 RDS 外网抖动时裸抛内部堆栈。

接口：

```text
GET /api/metadata/retrieve?question=&table_limit=&field_limit=&fields_per_table=
```

返回结构：

```text
question
terms
candidate_tables[]:
  table
  score
  fields[]
candidate_fields[]
```

验证：

- `python -m compileall app` 通过。
- 本地 `GET /api/health/db` 通过，但 RDS 外网连接耗时约 3-4 秒，偶发连接超时需后续关注。
- `GET /api/metadata/retrieve?question=SPU 销售金额 店铺&table_limit=3&field_limit=8&fields_per_table=5` 返回：
  - 第一候选表：`hKrBQ2zwwG / ud_3418004512502203_dyxsjyzhb / DWS_抖音_SPU销售明细`
  - 后续候选包括订单销售明细、小件销售经营综合表等相关表。

影响：

- M2 已从“元数据读取 API”推进到“可用于 SQL 生成前置上下文的召回雏形”。
- 后续可以在此基础上继续做上下文压缩、候选字段去重、物理表名映射和 SQL 生成节点。

后续动作：

- 等用户明天更新元数据表名后，复测元数据表名与问数执行库物理表名的一致性。
- 增加上下文构建服务，将候选表/字段整理成 LLM prompt 可直接消费的短文本或结构化 schema。
- 后续接 ES/OpenSearch/向量库时，优先替换 `MetadataRetrievalService` 内部召回实现。

关联文件：

- `app/services/metadata_retrieval_service.py`
- `app/repositories/metadata_repository.py`
- `app/api/routers/metadata.py`
- `docs/NEXT-AI-切换API接续包.md`

## 2026-06-01 M2 问数上下文构建服务初版

类型：开发 / 测试

摘要：

- 新增 `app/services/metadata_context_service.py`，在元数据召回结果之上构建 SQL 生成前可消费的上下文。
- 新增接口 `GET /api/metadata/context`。
- 当前上下文输出包含：
  - `tables`：压缩后的候选表、候选字段、粒度、主键、说明、注意事项。
  - `candidate_fields`：召回层的字段候选，供调试或后续二次选择。
  - `prompt_context`：可直接喂给后续 LLM/SQL 生成节点的短文本上下文。
  - `warnings`：元数据缺失或映射风险提示。
- 该服务不直接生成 SQL，只负责把元数据整理成下一节点可用的输入。

接口：

```text
GET /api/metadata/context?question=&table_limit=&field_limit=&fields_per_table=
```

验证：

- `python -m compileall app` 通过。
- 本地 Uvicorn 已重启并加载新路由。
- `GET /api/metadata/context?question=SPU 销售金额 店铺&table_limit=2&field_limit=8&fields_per_table=5` 返回：
  - 第一候选表：`hKrBQ2zwwG / ud_3418004512502203_dyxsjyzhb / DWS_抖音_SPU销售明细`
  - 第一候选表字段数：5
  - `warnings` 为空
  - `prompt_context` 包含候选表、表名、字段英文名、字段中文名和类型。

部署判断：

- 当前本地测试直连阿里云外网 RDS 偶发较慢，不代表最终服务链路。
- 用户确认后续服务部署在阿里云云服务器上，从云服务器发起查询；当前无需因本地测试延迟改变架构。
- 后续部署到云服务器后，应复测 API 到 metadata DB 和 warehouse DB 的实际延迟。

后续动作：

- 用户明天更新元数据表名后，复测 `table_name` 与问数执行库物理表名的映射。
- 下一步进入 SQL 生成前的工作流节点设计：把 `metadata/context` 输出作为 SQL 生成输入。
- 同时补齐 SQL 执行前的物理表白名单、只读 SQL 安全校验和 LIMIT 策略。

关联文件：

- `app/services/metadata_context_service.py`
- `app/services/metadata_retrieval_service.py`
- `app/api/routers/metadata.py`
- `docs/NEXT-AI-切换API接续包.md`

## 2026-06-02 元数据表名映射修复与 SQL 草稿节点

类型：开发 / 测试

摘要：

- 用户已更新元数据表名。
- 已确认 `table_dictionary` 中 `hKrBQ2zwwG / DWS_抖音_SPU销售明细` 的 `bywm` 已更新为 `dws_douyin_spu_sales_detail`。
- 问数执行库 `chatsql_ai` 中同名物理表 `dws_douyin_spu_sales_detail` 已存在。
- 该表当前执行库结构可读，约 111 列；`information_schema.TABLES.TABLE_ROWS` 当前估算为 0，因此后续执行 SQL 可能能验证结构但不一定返回真实数据。

新增代码：

- 新增 `app/repositories/warehouse_repository.py`，读取执行库物理表和字段结构。
- 新增 `app/services/query_planning_service.py`，把元数据上下文和执行库 schema 做匹配，输出 SQL-ready 计划。
- 新增 `app/services/sql_draft_service.py`，基于 SQL-ready 计划生成只读 SELECT 草稿，并调用 `review_sql` 做安全审查。
- 新增 `app/api/routers/query.py`。
- `app/api/main.py` 已挂载 query router。
- `app/clients/mysql.py` 增加轻量建连重试，用于缓解本地外网 RDS 偶发 2003/2013/packet sequence 类临时断连。

新增接口：

```text
GET /api/query/prepare?question=&table_limit=&field_limit=&fields_per_table=
GET /api/query/draft-sql?question=&table_limit=&field_limit=&fields_per_table=&limit=
```

验证：

- `python -m compileall app` 通过。
- `GET /api/query/prepare?question=SPU 销售金额 店铺` 返回：
  - `ready_for_sql = true`
  - `selected_table.table_name = dws_douyin_spu_sales_detail`
  - 执行库物理列数约 111
- `GET /api/query/draft-sql?question=SPU 销售金额 店铺&table_limit=2&field_limit=30&fields_per_table=20&limit=100` 返回：

```sql
SELECT `bhssjxsje`, `shop_name1`, `bhsdrsjxsje`, `sjxsje`, `sjxsjexbm`, `sjxsjejbm`, `drsjxsje`, `ygsjxsje`, `bhssjssjeqtqs`, `qtfyje`, `sjssje`, `zje` FROM `dws_douyin_spu_sales_detail` LIMIT 100
```

- SQL safety review 返回 `allowed = true`，无 hard blocks，无 risks。
- 当前 warnings 包括：
  - 次候选表 `ud_5179579576634064_dyxjxsjyzhb` 在执行库中未找到物理表，不阻塞首选表。
  - 首选物理表 `dws_douyin_spu_sales_detail` 当前估算行数为 0。

影响：

- M2/M3 之间的前置链路已经从“元数据召回”推进到“元数据上下文 -> 执行库 schema 匹配 -> SQL 草稿 -> SQL 安全审查”。
- 当前 SQL 草稿仍是确定性占位能力，不等同最终大模型 SQL 生成；它用于先验证字段映射、表白名单、安全审查和执行链路。

后续动作：

- 下一步增加 SQL 执行节点：仅执行 `review_sql.allowed = true` 的 SELECT，默认 LIMIT，记录结果摘要。
- 再接入 LLM SQL 生成节点时，应把 `/api/query/prepare` 或 `/api/metadata/context` 输出作为 prompt 输入，并继续复用 `review_sql` 和执行库 schema 校验。
- 后续部署到阿里云服务器后，复测服务端到两个 RDS 的真实延迟。

关联文件：

- `app/repositories/warehouse_repository.py`
- `app/services/query_planning_service.py`
- `app/services/sql_draft_service.py`
- `app/api/routers/query.py`
- `app/clients/mysql.py`
- `docs/NEXT-AI-切换API接续包.md`

## 2026-06-02 SQL 执行闭环初版

类型：开发 / 测试

摘要：

- 新增 `app/services/sql_execution_service.py`。
- `WarehouseRepository` 新增 `execute_select`，用于执行只读 SELECT 并返回结构化结果。
- `GET /api/query/execute-draft` 已新增。
- 执行边界会对最终 SQL 再次调用 `review_sql`，只有 `allowed = true` 才执行。
- 当前执行节点复用 `draft-sql` 的确定性 SELECT 草稿，后续接入 LLM SQL 生成后也应复用同一安全执行边界。

新增接口：

```text
GET /api/query/execute-draft?question=&table_limit=&field_limit=&fields_per_table=&limit=
```

验证：

- `python -m compileall app` 通过。
- 本地 Uvicorn 已重启并加载新路由。
- `GET /api/query/execute-draft?question=SPU 销售金额 店铺&table_limit=2&field_limit=30&fields_per_table=20&limit=100` 执行成功。
- 执行 SQL：

```sql
SELECT `bhssjxsje`, `shop_name1`, `bhsdrsjxsje`, `sjxsje`, `sjxsjexbm`, `sjxsjejbm`, `drsjxsje`, `ygsjxsje`, `bhssjssjeqtqs`, `qtfyje`, `sjssje`, `zje` FROM `dws_douyin_spu_sales_detail` LIMIT 100
```

- 返回：
  - `executed = true`
  - `execution_review.allowed = true`
  - `row_count = 100`
  - `elapsed_ms ~= 3560.94`
  - `columns = bhssjxsje, shop_name1, bhsdrsjxsje, sjxsje, sjxsjexbm, sjxsjejbm, drsjxsje, ygsjxsje, bhssjssjeqtqs, qtfyje, sjssje, zje`

重要发现：

- `information_schema.TABLES.TABLE_ROWS` 对 `dws_douyin_spu_sales_detail` 的估算为 0，但实际 SELECT 能返回 100 行，说明该估算不可靠，不能作为是否有数据的硬判断。
- 当前 warning 中“Physical table has no estimated rows” 只是统计信息提示，不代表真实无数据。

影响：

- 第一阶段最小闭环已经形成：

```text
自然语言问题
-> 元数据召回
-> 上下文构建
-> 执行库 schema 匹配
-> SELECT 草稿
-> SQL 安全审查
-> SQL 执行
-> 结构化结果返回
```

后续动作：

- 增加正式 `query/run` 工作流接口，整合 prepare/draft/execute，返回面向前端的一体化结果。
- 接入 LLM SQL 生成节点时，仍必须复用当前执行边界的 `review_sql`。
- 优化 warning：把 `TABLE_ROWS=0` 改为弱提示，避免误导为真实无数据。
- 后续部署到阿里云服务器后复测端到端延迟。

关联文件：

- `app/services/sql_execution_service.py`
- `app/repositories/warehouse_repository.py`
- `app/api/routers/query.py`
- `docs/NEXT-AI-切换API接续包.md`

## 2026-06-07 M2 query/run 一体化问数入口

类型：开发 / 测试

摘要：

- 新增 `app/services/query_run_service.py`，提供面向前端/后续 agent 的一体化问数入口。
- 新增 `GET /api/query/run`。
- 该接口整合：
  - 元数据召回
  - 上下文构建
  - 执行库 schema 匹配
  - SELECT 草稿
  - SQL safety review
  - SQL 执行
  - 结构化结果返回
- 返回结构更适合前端消费：
  - `answer_status`
  - `sql`
  - `selected_table`
  - `columns`
  - `rows`
  - `row_count`
  - `elapsed_ms`
  - `warnings`
  - `trace`

性能/稳定性调整：

- `query/run` 默认 `table_limit=1`、`field_limit=20`，优先跑首选 SQL-ready 路径，减少本地直连 RDS 时的多余 schema 查询。
- `QueryPlanningService.prepare` 新增 `stop_after_first_ready`，当首个候选表已可执行时可停止检查后续候选表。
- `WarehouseRepository` 增加进程内 schema cache，避免同一进程内重复查询同一张表的 `information_schema`。
- 当元数据字段候选未能匹配物理列，但物理表存在时，`QueryPlanningService` 会使用执行库 `information_schema.COLUMNS` 作为字段候选兜底，避免 SQL-ready 表因为元数据字段召回为空而失败。

验证：

- `python -m compileall app` 通过。
- 本地 Uvicorn 已重启并加载新路由。
- `GET /api/query/run?question=SPU 销售金额 店铺&limit=10` 返回：
  - `answer_status = ok`
  - `selected_table.table_name = dws_douyin_spu_sales_detail`
  - `row_count = 10`
  - `column_count = 12`
  - `elapsed_ms ~= 6069.75`
  - `warnings = []`

执行 SQL：

```sql
SELECT `bhssjxsje`, `shop_name1`, `bhsdrsjxsje`, `sjxsje`, `sjxsjexbm`, `sjxsjejbm`, `drsjxsje`, `ygsjxsje`, `bhssjssjeqtqs`, `qtfyje`, `sjssje`, `zje` FROM `dws_douyin_spu_sales_detail` LIMIT 10
```

影响：

- M2 已形成可由前端或 agent 直接调用的最小问数入口。
- 当前仍是确定性 SQL 草稿，不是 LLM SQL 生成；但执行边界、安全审查和结构化结果返回已可复用。

后续动作：

- 下一步可以开始接入 LLM SQL 生成节点，但必须复用当前 `review_sql` 和执行边界。
- 也可以先补 `POST /api/query/run`，把 GET 参数改成请求体，便于复杂问题和后续会话上下文传入。
- 后续部署到阿里云服务器后复测端到端延迟，本地直连 RDS 仍有波动。

关联文件：

- `app/services/query_run_service.py`
- `app/services/query_planning_service.py`
- `app/repositories/warehouse_repository.py`
- `app/api/routers/query.py`
- `docs/NEXT-AI-切换API接续包.md`

## 2026-06-07 M2 query/run POST 正式入口

类型：开发 / 测试

摘要：

- `app/api/routers/query.py` 新增 `POST /api/query/run`。
- GET `/api/query/run` 保留为快速调试入口。
- POST 请求体使用 Pydantic 模型 `QueryRunRequest`，当前字段：
  - `question`
  - `table_limit`
  - `field_limit`
  - `fields_per_table`
  - `limit`
  - `mode`
  - `conversation_context`
- 当前仅支持 `mode = draft`，为后续 LLM SQL 生成模式预留扩展位。
- `conversation_context` 当前透传返回，用于后续多轮问数上下文。

验证：

- `python -m compileall app` 通过。
- 本地 Uvicorn 已重启。
- `POST /api/query/run` 使用 JSON body 验证通过：

```json
{
  "question": "SPU 销售金额 店铺",
  "limit": 5,
  "mode": "draft",
  "conversation_context": {
    "source": "codex_validation"
  }
}
```

返回摘要：

```text
answer_status = ok
mode = draft
selected_table.table_name = dws_douyin_spu_sales_detail
row_count = 5
column_count = 12
warnings = []
```

执行 SQL：

```sql
SELECT `bhssjxsje`, `shop_name1`, `bhsdrsjxsje`, `sjxsje`, `sjxsjexbm`, `sjxsjejbm`, `drsjxsje`, `ygsjxsje`, `bhssjssjeqtqs`, `qtfyje`, `sjssje`, `zje` FROM `dws_douyin_spu_sales_detail` LIMIT 5
```

影响：

- M2 已具备一个更适合前端和后续 agent 调用的一体化问数入口。
- 后续接入 LLM SQL 生成时，可以在该入口中扩展 `mode`，但仍必须复用当前 SQL safety review 和执行边界。

后续动作：

- 接入 LLM SQL 生成节点，先作为 `mode = llm_draft` 或类似模式，不直接替换当前 draft 模式。
- 增加运行记录模型：`run_id`、节点耗时、候选表字段、SQL review、执行摘要。
- 部署到云服务器后复测 POST `/api/query/run` 的真实链路延迟。

关联文件：

- `app/api/routers/query.py`
- `docs/NEXT-AI-切换API接续包.md`

## 2026-06-07 M2 query/run 运行记录结构

类型：开发 / 测试

摘要：

- `QueryRunService.run` 已新增运行记录结构。
- 每次 `GET/POST /api/query/run` 响应都会包含：
  - `run_id`
  - `started_at`
  - `trace.run_id`
  - `trace.started_at`
  - `trace.finished_at`
  - `trace.total_elapsed_ms`
  - `trace.steps`
- 当前 step 结构先覆盖：
  - `draft_and_execute`
  - `sql_execution`
- 该结构暂不落库，先固化响应契约；后续可按此结构设计 `query_run` 和 `query_step` 表。

验证：

- `python -m compileall app` 通过。
- 本地 Uvicorn 已重启。
- `POST /api/query/run` 使用 `SPU 销售金额 店铺`、`limit=3` 验证通过：
  - `answer_status = ok`
  - `row_count = 3`
  - `run_id = ddfd8cbd-cdf2-4311-bfe8-abf780a9ba96`
  - `trace.run_id` 与顶层 `run_id` 一致
  - `trace.total_elapsed_ms ~= 33861.48`
  - `trace.steps = draft_and_execute:ok, sql_execution:ok`
  - `trace.execution_review.allowed = true`

影响：

- M2 问数入口具备了最小可观测结构。
- 后续接入 LLM SQL 生成时，可以继续往 `trace.steps` 增加 `metadata_retrieval`、`context_build`、`llm_sql_generation`、`sql_review`、`sql_execution` 等节点。

后续动作：

- 将当前内存响应结构落到运行记录表或日志 sink。
- 接入 LLM SQL 生成节点时，必须写入对应 step 状态、耗时、输入输出摘要。

关联文件：

- `app/services/query_run_service.py`
- `docs/NEXT-AI-切换API接续包.md`

## 2026-06-08 M2 LLM SQL 生成节点初版

类型：开发 / 测试

摘要：

- 已接入 DeepSeek / OpenAI-compatible LLM client。
- Git 中新增 `.env.example` 的 LLM 配置模板。
- 本地 `.env` 和 `local/SECRETS-实际账号.md` 已记录真实 DeepSeek key，不提交 Git。
- 用户提供的 `https://platform.deepseek.com/api_keys` 是控制台 API key 页面；实际调用 base URL 已按官方 OpenAI-compatible API 使用 `https://api.deepseek.com`。
- `app/clients/llm.py` 新增 `OpenAICompatibleClient`。
- `app/services/llm_sql_generation_service.py` 新增 LLM SQL 生成服务。
- `POST /api/query/run` 已支持 `mode = llm_draft`。
- `mode = draft` 保留为确定性 fallback。
- LLM SQL 执行前新增 schema 白名单校验：LLM 输出 SQL 中反引号标识符必须属于选中物理表或字段，否则不执行。
- LLM SQL 仍必须通过 `review_sql`，并在执行边界再次审查。

本地配置：

```text
LLM_PROVIDER=deepseek
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=DEEPSEEK（代码映射为 deepseek-v4-flash）
LLM_TIMEOUT_SECONDS=60
LLM_API_KEY=见 local/SECRETS-实际账号.md
```

验证：

- `python -m compileall app` 通过。
- `GET /api/health` 返回 LLM 配置已读取，且只显示 `api_key_configured = true`，不泄露 key。
- `POST /api/query/run` 使用 `mode = llm_draft` 验证通过。

验证请求摘要：

```json
{
  "question": "SPU 销售金额 店铺",
  "limit": 3,
  "mode": "llm_draft",
  "table_limit": 1,
  "field_limit": 20,
  "fields_per_table": 20
}
```

返回摘要：

```text
answer_status = ok
selected_table.table_name = dws_douyin_spu_sales_detail
row_count = 3
executed = true
execution_review.allowed = true
llm_model = deepseek-v4-flash
warnings = []
```

LLM 生成并执行的 SQL（初次验证）：

```sql
SELECT `yjlm`, `sjlm`, `bhsqtfy` FROM `dws_douyin_spu_sales_detail` LIMIT 3
```

随后优化：

- `QueryPlanningService` 会在物理表存在时合并执行库字段候选，避免只传入少量元数据命中字段。
- LLM prompt 已增加 question-focused recommended columns。
- 复测后 LLM SQL 已能覆盖店铺和销售金额相关字段：

```sql
SELECT `shop_name1`, `sjxsje`, `bhssjxsje`, `bhsdrsjxsje`, `drsjxsje` FROM `dws_douyin_spu_sales_detail` LIMIT 3
```

影响：

- M2 已从确定性问数闭环推进到 LLM SQL 生成闭环。
- 当前安全边界仍然保留：LLM 输出必须过 SQL review、schema 白名单和执行边界。

后续动作：

- 已补充 `mode=llm_draft` 的细粒度 trace step：`llm_sql_generation`、`sql_review`、`schema_validation`、`sql_execution`。
- 已补充 LLM 失败/SQL 被拦截时的统一 `error` 对象，包含 `code`、`message`、`stage`、`status`、`retryable`。
- 下一步继续扩展更多真实问题测试集，并开始整理前端/agent 消费的问数响应契约。

补充验证：

- `python -m compileall app` 通过。
- `POST /api/query/run` 使用 `mode=draft` 验证通过：
  - `answer_status = ok`
  - `row_count = 3`
  - `trace.steps = draft_and_execute:ok, sql_execution:ok`
- `POST /api/query/run` 使用 `mode=llm_draft` 验证通过：
  - `answer_status = ok`
  - `row_count = 3`
  - `error = null`
  - `trace.steps = llm_sql_generation:ok, sql_review:ok, schema_validation:ok, sql_execution:ok`

本次 LLM 复测 SQL：

```sql
SELECT `shop_name1`, `sjxsje` FROM `dws_douyin_spu_sales_detail` LIMIT 3
```

## 2026-06-15 M2 query/run 响应契约与离线测试

类型：开发 / 测试 / 文档

摘要：

- 新增 `docs/QUERY-RUN-响应契约.md`，固定 `GET/POST /api/query/run` 第一版响应形状。
- 契约明确 `data` 稳定字段、`answer_status` 语义、`selected_table`、`error`、`trace` 和 `trace.steps`。
- 新增 `tests/test_query_run_contract.py`，使用 fake executor/repository，不访问真实 RDS 或 LLM。
- 测试覆盖：
  - `draft` 成功响应的顶层字段和 trace。
  - `llm_draft` 未配置 LLM 时的 `not_ready` 和统一 `error`。
  - LLM SQL schema 白名单允许/阻断行为。

影响：

- M2 的问数入口不再只靠手工接口验证，开始具备可离线回归的响应契约。
- 后续前端和 agent 可以先按 `docs/QUERY-RUN-响应契约.md` 消费 `query/run`。

后续动作：

- 扩展真实问题测试集，覆盖金额、数量、店铺、品牌、时间条件、排序和聚合。
- 在真实测试集稳定后，再推进多轮问数上下文、聚合 SQL 和云服务器部署复测。

关联文件：

- `docs/QUERY-RUN-响应契约.md`
- `tests/test_query_run_contract.py`
- `app/services/query_run_service.py`

关联文件：

- `app/clients/llm.py`
- `app/services/llm_sql_generation_service.py`
- `app/services/query_planning_service.py`
- `app/services/query_run_service.py`
- `app/api/routers/query.py`
- `.env.example`
- `docs/NEXT-AI-切换API接续包.md`

## 2026-06-01 RDS 新账号连接成功

类型：测试

摘要：

- 本地密钥文件已更新为新账号 `chat_ai_duckdb_2`。
- 从云服务器 `114.55.148.140` 使用新账号连接 RDS `rm-2zea6b6dcxxq17753zo.mysql.rds.aliyuncs.com:3306` 成功。
- 连接库：`chatsql_ai`。
- 执行 `SELECT 1` 返回 `1`。
- MySQL 客户端需要加 `--get-server-public-key` 以支持 `caching_sha2_password` 非 SSL 认证。
- 尝试 `--ssl-mode=REQUIRED` 时，RDS 返回服务端不支持 SSL。

影响：

- 云服务器 SSH 和 RDS 连接链路已打通。
- 第一阶段资源确认中，数据库连接已可作为 M1/M2 后续开发依据。
- 后续应用配置需支持 MySQL `caching_sha2_password`，Python 驱动连接时可能需要等价参数，例如允许获取服务端公钥或改用兼容认证插件。

后续动作：

- 更新后续 `.env` 或正式配置模板时使用 `chat_ai_duckdb_2`。
- 进入 M1 前仍需确认该账号权限边界：是否只读、是否能建/写元数据库表。如果这是问数执行账号，应保持只读；元数据写入应另建应用写账号。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `docs/PLAN-第一阶段落地方案.md`

## 2026-06-01 M1 工程骨架启动

类型：开发

摘要：

- 正式代码从干净的根目录 `app/` 开始搭建，不复用旧原型目录。
- 新增 FastAPI 应用入口 `app/api/main.py`。
- 新增健康检查路由 `GET /api/health` 和准备检查 `GET /api/ready`。
- 新增标准库配置加载 `app/core/config.py`，支持 `META_DB_*`、`DW_DB_*` 和兼容旧 `DB_*`。
- 新增 request_id 上下文 `app/core/request_context.py`。
- 新增标准库日志配置 `app/core/logging.py`，日志格式包含 `request_id`。
- 迁移旧原型 SQL 审查思想到正式服务位置 `app/services/sql_safety_service.py`。
- 新增 `pyproject.toml` 声明 FastAPI、Uvicorn 和 PyMySQL 依赖。
- 新增 `.env.example`，并清理 `config/database.example.env` 中旧 RDS 示例。

本地配置：

- `.env` 已根据 `local/SECRETS-实际账号.md` 更新为新 RDS。
- `.env.reader` 已根据新 RDS 更新。
- `.env.admin` 已删除，避免旧 RDS 管理账号误导。
- 当前新 RDS 账号：`chat_ai_duckdb_2`。
- 当前本地配置开启 MySQL 服务端公钥获取参数：`*_MYSQL_GET_SERVER_PUBLIC_KEY=true`。

验证：

- `python -m compileall app` 通过。
- `app.core.config.get_settings()` 可读取新 RDS 配置，缺失项为空。
- SQL 审查服务基础导入与阻断验证通过。

影响：

- M1 的工程骨架、配置加载和 request_id 日志基础已开始落地。
- 本机尚未安装 FastAPI/Uvicorn/PyMySQL，因此还未启动实际 API 服务。

后续动作：

- 安装项目依赖或建立虚拟环境。
- 增加数据库连接客户端/Repository 层，注意 PyMySQL 需要支持 `caching_sha2_password` 获取服务端公钥。
- 确认 `chat_ai_duckdb_2` 权限边界，决定是否另建 `meta_app` 写账号。

关联文件：

- `pyproject.toml`
- `.env.example`
- `config/database.example.env`
- `app/api/main.py`
- `app/api/routers/health.py`
- `app/core/config.py`
- `app/core/logging.py`
- `app/core/request_context.py`
- `app/services/sql_safety_service.py`

## 2026-06-01 M1 本地 API 与数据库健康检查通过

类型：开发 / 测试

摘要：

- 已创建本地虚拟环境 `.venv/`，并加入 `.gitignore`。
- 已安装项目依赖：FastAPI、Uvicorn、PyMySQL 等。
- 修复 `pyproject.toml` 包发现配置，只打包 `app*`，避免把 `web/`、`local/`、`legacy/` 等目录当成 Python 包。
- 新增 MySQL 客户端 `app/clients/mysql.py`。
- 新增数据库健康检查接口 `GET /api/health/db`。
- PyMySQL 已能直连阿里云 RDS，支持当前账号的 `caching_sha2_password` 认证。
- 本地 Uvicorn 已启动：`http://127.0.0.1:8000`。

验证：

- `python -m compileall app` 通过。
- `GET /api/health` 返回 `ok=true`，并返回脱敏后的元数据库和数仓库配置。
- `GET /api/ready` 返回 `ok=true`，配置缺失项为空。
- `GET /api/health/db` 返回 `ok=true`，`metadata_db` 和 `warehouse_db` 均连接成功。
- RDS 返回版本：MySQL `8.0.36`。
- 当前用户：`chat_ai_duckdb_2@%`。

运行方式：

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

当前后台进程：

- PID 记录在 `.runtime/uvicorn.pid`。
- 日志记录在 `.runtime/uvicorn.err.log` 和 `.runtime/uvicorn.out.log`。

影响：

- M1 的 FastAPI 骨架、配置加载、request_id、健康检查和 RDS 连接已跑通。
- 后续可以进入 M2 元数据库表结构与 Repository。

后续动作：

- 确认 `chat_ai_duckdb_2` 是否允许写入元数据库表。
- 若它应作为问数只读账号，建议另建 `meta_app` 写账号。
- 设计并初始化 `meta_table`、`meta_field`、`meta_field_dependency`、`query_run`、`query_step` 等表。

关联文件：

- `.gitignore`
- `pyproject.toml`
- `app/clients/mysql.py`
- `app/api/routers/health.py`
- `app/core/config.py`
- `.runtime/uvicorn.pid`

## 2026-06-01 元数据库改用旧 RDS

类型：资源 / 决策

摘要：

- 用户说明旧 RDS 可作为元数据库。
- 新 RDS `chatsql_ai` 是高读写 DB，更适合作为问数执行数据库。
- 当前测试流程阶段暂不强制只读账号；后续健壮性和安全收敛阶段再重新配置账号。
- 旧 RDS 连接信息来自历史配置：`rm-bp1mx4778wjne596xko.mysql.rds.aliyuncs.com:3306/youmei_ai`，用户 `baoyan`。
- Codex 使用当前已知密码从云服务器端连接旧 RDS 并执行 `SELECT 1` 成功。

影响：

- `META_DB_*` 应指向旧 RDS。
- `DW_DB_*` 应指向新 RDS。
- M2 元数据库表结构应建在旧 RDS `youmei_ai` 中。
- 新 RDS `chatsql_ai` 保持为问数执行数据库。

后续动作：

- 更新本地 `local/SECRETS-实际账号.md` 和 `.env`。
- 复测本地 FastAPI `GET /api/health/db` 是否两组 DB 都通过。
- 进入 M2 元数据库表结构设计和初始化。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `.env`

## 2026-06-01 本地 API 双库配置验证通过

类型：资源 / 测试

摘要：

- 本地 `local/SECRETS-实际账号.md` 已更新：
  - 元数据库：旧 RDS `youmei_ai`，用户 `baoyan`。
  - 问数执行数据库：新 RDS `chatsql_ai`，用户 `chat_ai_duckdb_2`。
- 本地 `.env` 已更新：
  - `META_DB_*` 指向旧 RDS。
  - `DW_DB_*` 指向新 RDS。
  - 兼容旧原型的 `DB_*` 指向新 RDS。
- 本地 `.env.reader` 指向新 RDS。
- 已重启 Uvicorn。
- `GET /api/health/db` 验证通过：
  - `metadata_db.database_name = youmei_ai`
  - `metadata_db.current_user = baoyan@%`
  - `warehouse_db.database_name = chatsql_ai`
  - `warehouse_db.current_user = chat_ai_duckdb_2@%`

影响：

- 本地 API 已按“旧 RDS 元数据库 + 新 RDS 问数执行库”运行。
- 下一步可以在旧 RDS `youmei_ai` 中推进 M2 元数据库表结构。

后续动作：

- 设计 M2 表结构。
- 建初始化脚本和 Repository。
- 当前测试阶段新 RDS 不强制只读账号；后续安全收敛再配置。

关联文件：

- `docs/NEXT-AI-切换API接续包.md`
- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `.env`

## 2026-06-01 钉钉同步职责调整

类型：决策 / 架构

摘要：

- 用户确认：钉钉上维护的数仓元数据已经可以通过用户自己的工具定期写入元数据库。
- 因此项目内原计划 M3“接入钉钉开放平台并同步表/字段元数据”不再需要作为主要开发任务。
- 本项目应把元数据库视为已由外部工具供数的上游，优先读取和适配已有元数据表结构。
- 后续“同步”相关工作应转为元数据库到 ES/OpenSearch/向量库的索引刷新，而不是钉钉 API 接入。

影响：

- M2 从“从零设计并创建元数据库表”调整为“发现现有元数据表结构、字段映射和 Repository”。
- 原 M3 改为“元数据索引刷新/检索索引构建”。
- 不要重复实现钉钉同步链路，避免和用户已有工具职责重叠。

后续动作：

- 读取旧 RDS `youmei_ai` 中现有表清单和字段结构。
- 识别哪些表是用户工具写入的数仓元数据表。
- 基于现有表结构建立 Repository 和 API。
- 如果字段名与项目标准模型不同，优先做适配层。

关联文件：

- `docs/NEXT-AI-切换API接续包.md`
- `docs/PLAN-第一阶段落地方案.md`
- `docs/RESOURCE-资源登记.md`

## 2026-06-01 元数据字典表初步探查

类型：资源 / 分析

摘要：

- 用户确认数仓元数据已经由自己的工具写入元数据库。
- 当前核心元数据表为两张：
  - `table_dictionary`：数仓字典 / 表字典。
  - `metric_dictionary`：指标字典 / 字段指标字典。
- 元数据库 `youmei_ai` 当前表：
  - `table_dictionary`：41 行。
  - `metric_dictionary`：1394 行。
  - `dws_tmall_sales_link_summary`：约 549633 行，看起来像旧/示例数据表，不是当前核心元数据字典。
- 问数执行库 `chatsql_ai` 当前测试表：
  - `dws_douyin_spu_sales_detail`：约 87579 行，表结构已存在。

字段理解：

- `table_dictionary.bywm`：表英文名。
- `table_dictionary.bzwm`：表中文名。
- `table_dictionary.bhzd`：包含字段，当前表现为逗号分隔内部标识。
- `metric_dictionary.zdywmc`：字段英文名称。
- `metric_dictionary.zdzwmc`：字段中文名称。
- `metric_dictionary.ssscb`：注释为“所属数仓表”，但当前值表现为内部标识。
- `metric_dictionary.jsgs`：计算公式。
- `metric_dictionary.ywdy`：业务定义。
- `metric_dictionary.syzysx`：使用注意事项。

关键发现：

- 尝试 `metric_dictionary.ssscb = table_dictionary.bywm`，匹配数为 0。
- 尝试 `FIND_IN_SET(metric_dictionary.ssscb, table_dictionary.bhzd)`，匹配数为 0。
- 因此两张字典可以作为召回基础，但真实关联键尚未确认。

影响：

- M2 应先做“现有表结构适配和关联键确认”，而不是从零设计新元数据表。
- 在关联键确认前，可以先做表字典和指标字典的独立关键词召回。
- SQL 生成需要可靠地从指标/字段定位到实际执行表，因此关联键是 M2 的第一优先级。

后续动作：

- 请用户确认 `metric_dictionary.ssscb` 应该关联 `table_dictionary` 的哪一列，或是否存在未导入的 ID 映射字段。
- 如果现有结构无法稳定关联，建议在上游工具中补充稳定字段，例如 `table_name` 或 `table_id`。
- 建立 Repository 时先保留适配层，不直接绑定死字段名。

关联文件：

- `docs/NEXT-AI-切换API接续包.md`
- `docs/RESOURCE-资源登记.md`
- `app/clients/mysql.py`

## 2026-06-01 RDS 新账号

类型：资源

摘要：

- 用户已新创建 RDS 数据库账号：`chat_ai_duckdb_2`。
- 密码不变，仍使用本地 `local/SECRETS-实际账号.md` 已记录值。
- 后续连接 `chatsql_ai` 改用 `chat_ai_duckdb_2`。

后续动作：

- 更新本地密钥文件中的应用账号和只读账号。
- 从云服务器端使用 `chat_ai_duckdb_2` 复测 RDS 登录和 `SELECT 1`。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `.gitignore`

## 2026-05-31 新服务器与 RDS 资源登记

类型：资源

摘要：

- 用户提供新的云服务器公网 IP：`114.55.148.140`，SSH 用户：`root`。
- 登录方式改为 Codex 生成 SSH 公钥，由用户配置到阿里云实例。
- Codex 已生成专用 SSH key，私钥路径：`local/ssh/text2sql_codex_ed25519`。
- 用户提供新的阿里云 RDS MySQL 外网地址、库名和账号，真实密码已记录到本地密钥文件。
- 数据库连接策略：先登录云服务器，再从服务器端测试 RDS 连接。

影响：

- 当前资源确认进入“待 SSH 公钥配置、待连通性测试”状态。
- 旧 `.env`、`.env.admin`、`.env.reader` 仍指向旧 RDS，不再作为新资源依据。

后续动作：

- 用户将 `local/ssh/text2sql_codex_ed25519.pub` 的内容配置到云服务器 `root` 用户授权密钥。
- Codex 使用沙箱外 SSH 测试登录 `root@114.55.148.140`。
- SSH 登录成功后，从服务器端测试 RDS `rm-2zea6b6dcxxq17753zo.mysql.rds.aliyuncs.com:3306` 连接。
- 测试结果继续追加到本检查点文件。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `local/ssh/text2sql_codex_ed25519`
- `local/ssh/text2sql_codex_ed25519.pub`

## 2026-06-01 SSH v2 key 重新绑定

类型：资源 / 风险

摘要：

- 第一版 SSH key 由沙箱用户生成，沙箱外 `ssh` 无法读取私钥，登录测试失败在本地私钥权限阶段。
- Codex 使用沙箱外 Windows 用户重新生成 v2 key。
- v2 私钥路径：`local/ssh/text2sql_codex_ed25519_v2`。
- v2 公钥路径：`local/ssh/text2sql_codex_ed25519_v2.pub`。
- 用户已重新绑定 v2 公钥到云服务器。
- 旧 key `text2sql_codex_ed25519` 应作废，避免后续会话误用。

影响：

- 后续 SSH 登录必须使用 v2 私钥。
- Git 资源登记和本地密钥文件需要同步指向 v2。
- 切换 API 或新会话恢复时，应按 `docs/MEMORY-重要信息记录规范.md` 和 `docs/HANDOFF-新会话接续说明.md` 的固定路径读取，不依赖聊天历史。

后续动作：

- 删除本地旧 key 文件。
- 使用 v2 私钥测试 `root@114.55.148.140`。
- SSH 成功后，从服务器端测试 RDS 连接。
- 测试结论继续追加到本检查点。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `docs/MEMORY-重要信息记录规范.md`
- `docs/HANDOFF-新会话接续说明.md`
- `local/SECRETS-实际账号.md`
- `local/ssh/text2sql_codex_ed25519_v2`
- `local/ssh/text2sql_codex_ed25519_v2.pub`

## 2026-06-01 SSH 与 RDS 连通性测试

类型：资源 / 测试 / 阻塞

摘要：

- 使用 v2 私钥成功登录 `root@114.55.148.140`。
- 服务器主机名：`iZbp13rcbr61o2rxnxa8rzZ`。
- 服务器系统：Linux `6.8.0-111-generic x86_64`。
- 从服务器端测试 RDS `rm-2zea6b6dcxxq17753zo.mysql.rds.aliyuncs.com:3306`，TCP 连接成功。
- 服务器已安装 MySQL 客户端：MySQL 8.0.45。
- 使用账号 `chat_ai_duckdb_1` 连接库 `chatsql_ai` 执行 `SELECT 1` 时失败：`Access denied for user 'chat_ai_duckdb_1'@'114.55.148.140'`。

影响：

- 云服务器 SSH 通道已经可用。
- RDS 网络路径已经可用。
- 当前阻塞点不在网络，而在 MySQL 账号密码或账号 host 授权。

后续动作：

- 确认 `chat_ai_duckdb_1` 密码是否正确。
- 在 RDS 控制台或管理员账号中确认该账号是否允许从 `114.55.148.140` 登录。
- 如果账号 host 受限，需要授权服务器公网 IP 或合适的来源范围。
- 认证修复后重新执行服务器端 `SELECT 1` 测试。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `local/ssh/text2sql_codex_ed25519_v2`

## 2026-06-01 RDS 认证复测

类型：测试 / 阻塞

摘要：

- 用户确认 RDS 白名单已加入服务器公网 IP `114.55.148.140`。
- 用户确认数据库密码仍为本地 `local/SECRETS-实际账号.md` 已记录值。
- Codex 从云服务器端再次测试 `chat_ai_duckdb_1` 登录 `chatsql_ai`，仍返回 `Access denied for user 'chat_ai_duckdb_1'@'114.55.148.140'`。
- Codex 额外排除了 Windows PowerShell 管道传输密码时尾部 `CRLF` 造成密码多一个回车字符的可能。

影响：

- 网络、白名单和端口可达性不是当前阻塞点。
- 当前阻塞点仍在 MySQL 认证/授权层。

后续动作：

- 在阿里云 RDS 控制台确认账号 `chat_ai_duckdb_1` 是否启用、密码是否刚重置生效。
- 确认该账号是否有访问库 `chatsql_ai` 的权限。
- 如 RDS 控制台支持账号授权来源，确认允许 `114.55.148.140` 或合适来源。
- 可临时重置该账号密码后同步更新 `local/SECRETS-实际账号.md`，再复测。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
