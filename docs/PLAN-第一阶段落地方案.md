# 第一阶段落地方案

## 1. 阶段目标

第一阶段目标不是复刻教程 demo，而是跑通一个可长期演进的抖音主题域智能问数闭环。

阶段完成标准：

- 抖音主题域真实数据源可连接、可读取、可安全查询。
- 钉钉 AI 表格中的表元数据和字段元数据已由用户自己的工具定期写入项目元数据库，本项目负责读取和适配。
- 元数据库可以支撑字段理解、计算公式、直接依赖、业务含义和使用注意事项。
- 用户输入自然语言问题后，系统能完成召回、上下文构建、SQL 生成、SQL 校验、SQL 执行和结果返回。
- 每次问数都有运行记录、节点耗时、生成 SQL、校验结果、执行结果和错误信息。
- 第一阶段架构不阻碍后续扩展到更多主题域、更多数据源和更复杂的权限控制。

## 2. 当前仓库基础

当前仓库已经有一个轻量原型，主要包括：

- `app/server.py`：基于标准库 HTTP server 的本地接口和静态页面服务。
- `app/db.py`：数据库连接和查询执行。
- `app/config.py`：本地数据库配置加载。
- `app/metadata.py`：从 `information_schema` 扫描表和字段。
- `app/query_planner.py`：基于规则的简单 SQL 规划。
- `agent/sql_guard.py`：SQL 只读审查和风险识别。
- `app/log_store.py`：本地 SQLite 运行记录。
- `web/agent.html`、`web/app.js`、`web/styles.css`：本地测试页面。

这些能力可以作为迁移基础，但不建议继续在当前结构上无限堆功能。第一阶段正式化时，应逐步迁移到分层后端结构。

当前需要注意的技术债：

- 部分中文字符串在代码和文档中出现编码乱码，正式化前需要统一 UTF-8。
- `query_planner.py` 目前是规则式、单表倾向的临时规划器，不适合作为长期智能问数核心。
- 当前服务基于标准库 HTTP server，后续应切换到 FastAPI。
- 当前元数据主要来自 `information_schema`，缺少业务描述、公式、依赖和使用注意事项。

## 3. 第一阶段架构

建议第一阶段采用以下结构：

```text
抖音主题域数据源
        |
        | 只读查询
        v
问数执行层

钉钉 AI 表格
        |
        | 用户已有工具定期写入
        v
元数据数据库
        |
        | 构建检索上下文
        v
问数智能体
        |
        | 生成/校验/执行 SQL
        v
SSE API -> 前端测试台
```

核心服务：

- 后端 API：FastAPI。
- 流式协议：SSE。
- 元数据库：MySQL 或 PostgreSQL，优先根据现有云资源确认。
- 业务数据源：抖音主题域所在数据库。
- 检索服务：第一阶段建议保留可插拔接口，可按资源确认后选择 Qdrant + Elasticsearch/OpenSearch，或 PostgreSQL pgvector + 全文检索。
- 大模型：通过配置注入模型名、API Key、base URL。
- 运行日志：先入数据库，保留本地 SQLite 作为开发模式兜底。

## 4. 代码结构建议

建议逐步调整为：

```text
app/
  api/
    main.py
    routers/
      query.py
      metadata.py
      index.py
    schemas/
  core/
    config.py
    logging.py
    request_context.py
  clients/
    dingding.py
    llm.py
    embedding.py
    vector_store.py
    search_store.py
  models/
    meta_table.py
    meta_field.py
    meta_field_dependency.py
    metadata_source.py
    query_run.py
  entities/
    metadata.py
    query.py
  repositories/
    meta_repository.py
    dw_repository.py
    vector_repository.py
    value_search_repository.py
    run_repository.py
  services/
    metadata_index_service.py
    metadata_index_service.py
    query_service.py
    sql_safety_service.py
  agent/
    state.py
    context.py
    graph.py
    nodes/
  scripts/
    inspect_meta_db.py
    init_meta_db.py
config/
  app.example.yaml
  database.example.env
web/
```

迁移原则：

- 当前 `agent/sql_guard.py` 可以迁移为 `app/services/sql_safety_service.py` 或被其调用。
- 当前 `app/metadata.py` 的 `information_schema` 扫描能力保留，用于补充字段类型、示例值和校验真实表结构。
- 当前 `app/log_store.py` 的运行记录思想保留，但正式运行记录建议写入元数据库。
- 当前前端页面保留为测试台，后续接 SSE。

## 5. 元数据库第一版表

### 5.1 meta_table

表级元数据，来源于钉钉 AI 表格。

建议字段：

- `id`
- `domain`
- `warehouse_layer`
- `database_name`
- `table_name`
- `table_cn_name`
- `description`
- `business_object`
- `grain`
- `primary_key`
- `update_frequency`
- `partition_field`
- `source_system`
- `owner`
- `suitable_scenarios`
- `unsuitable_scenarios`
- `usage_notes`
- `enabled`
- `source_version`
- `created_at`
- `updated_at`

### 5.2 meta_field

字段级元数据，包含原子字段和计算字段。

建议字段：

- `id`：建议格式 `database_name.table_name.field_name`
- `database_name`
- `table_name`
- `field_name`
- `field_cn_name`
- `description`
- `data_type`
- `semantic_type`：标识字段、属性字段、度量字段、时间字段、技术字段
- `calculation_formula`
- `direct_dependency`
- `business_meaning`
- `usage_notes`
- `examples`
- `is_physical`
- `is_filterable`
- `is_groupable`
- `is_aggregatable`
- `enabled`
- `source_version`
- `created_at`
- `updated_at`

### 5.3 meta_field_dependency

字段依赖和血缘。

建议字段：

- `id`
- `field_id`
- `dependency_field_id`
- `dependency_type`
- `description`
- `created_at`

### 5.4 meta_field_value

字段真实值或候选值缓存。

建议字段：

- `id`
- `field_id`
- `value`
- `value_norm`
- `source`
- `hit_count`
- `updated_at`

### 5.5 metadata_source / sync_change_log

记录外部元数据写入来源、版本、变更和索引刷新状态。钉钉到元数据库的同步由用户已有工具负责，本项目当前不重复实现。

### 5.6 query_run / query_step

记录问数运行和节点过程。

## 6. 外部元数据接入方式

当前关键调整：

- 钉钉 AI 表格仍是元数据协作入口。
- 钉钉到元数据库的定期写入已由用户自己的工具完成。
- 本项目不再把“接入钉钉开放平台并同步元数据”作为第一阶段主任务。
- 本项目优先读取旧 RDS `youmei_ai` 中已有元数据表，建立适配层和 Repository。
- 后续如需检索，基于元数据库内容刷新 ES/OpenSearch、向量库或字段值索引。

第一阶段接入流程调整为：

1. 读取元数据库现有表清单和字段结构。
2. 识别用户工具写入的表元数据、字段元数据、字段依赖和字段值表。
3. 将现有表结构映射到项目内部统一实体。
4. 如果已有表结构和建议模型不一致，优先做适配层，不急于改上游。
5. 建立 Repository 层读取元数据。
6. 建立基础 metadata API。
7. 后续根据元数据库变更刷新检索索引。

## 7. 问数工作流

第一阶段建议节点：

1. `receive_question`：接收问题，生成 `request_id` 和 `run_id`。
2. `parse_question`：识别主题域、时间、维度、度量、筛选条件。
3. `recall_fields`：召回字段元数据。
4. `recall_formulas`：召回计算字段、业务口径和公式。
5. `recall_values`：召回字段真实值。
6. `recall_dependencies`：召回直接依赖、主键、分区字段、join 关系。
7. `merge_context`：合并成按库表字段组织的上下文。
8. `filter_context`：过滤与当前问题无关的上下文。
9. `add_runtime_context`：补充当前时间、数据库类型、权限边界。
10. `generate_sql`：生成 SQL。
11. `review_sql_safety`：静态安全审查。
12. `validate_sql`：数据库语法/执行计划校验。
13. `correct_sql`：必要时修正 SQL。
14. `execute_sql`：用只读账号执行。
15. `build_response`：返回表格、摘要和图表建议。
16. `save_run`：保存完整运行记录。

第 3、4、5、6 步可以并行。

## 8. API 设计

第一阶段接口：

- `POST /api/query`：提交自然语言问题，SSE 返回进度和结果。
- `POST /api/metadata/index/refresh`：手动触发元数据检索索引刷新，后续实现。
- `GET /api/metadata/tables`：查看已同步表元数据。
- `GET /api/metadata/fields`：查看已同步字段元数据。
- `GET /api/runs`：查看问数运行历史。
- `GET /api/runs/{run_id}`：查看单次问数详情。
- `GET /api/health`：服务健康检查。

SSE 消息类型：

- `progress`
- `sql`
- `result`
- `error`
- `trace`

## 9. 安全边界

第一阶段必须实现：

- 应用查询使用只读账号。
- 超级管理员账号只用于初始化和运维脚本。
- 只允许单条只读 SQL。
- 禁止多语句。
- 禁止写操作关键词。
- 禁止未授权库表。
- 禁止敏感字段。
- SQL 执行超时。
- 查询结果行数保护。
- 所有生成 SQL 和执行结果入日志。

## 10. 资源需求清单

需要项目负责人提供或确认：

- 云服务器 SSH 管理权限。
- 元数据库部署位置：新建 MySQL/PostgreSQL，或使用现有数据库。
- 抖音主题域数据源连接信息：host、port、database、只读账号、网络白名单。
- 抖音主题域第一批表清单。
- 钉钉开放平台应用凭证。
- 钉钉 AI 表格 app/token、表格 ID、字段映射。
- 大模型 API Key、base URL、模型偏好。
- 是否允许部署 Qdrant、Elasticsearch/OpenSearch、Kibana 等服务。
- 服务器内存、CPU、磁盘和操作系统信息。

## 11. 里程碑

### M1：工程骨架和配置

- 建立 FastAPI 后端结构。
- 建立配置加载和环境变量模板。
- 建立 request_id 日志。
- 保留当前原型可运行。

### M2：元数据库适配

- 读取旧 RDS `youmei_ai` 中现有元数据表结构。
- 梳理外部工具写入的表/字段/依赖/字段值。
- 建立字段映射和内部实体。
- 建立元数据 Repository。

### M3：元数据索引刷新

- 基于元数据库内容构建字段元数据检索。
- 基于元数据库内容构建字段值检索。
- 后续接 ES/OpenSearch、Qdrant 或 pgvector。
- 保留索引刷新记录和错误记录。

### M4：检索上下文

- 组装字段元数据检索结果。
- 组装字段值检索结果。
- 建立依赖和公式上下文组装。

### M5：问数闭环

- 实现节点化问数流程。
- 生成 SQL。
- 安全审查和数据库校验。
- 执行并返回结果。

### M6：前端测试台和可观测性

- 前端接 SSE。
- 展示节点进度、SQL、审查结果、查询结果。
- 展示运行历史。

## 12. 下一步动作

建议下一步先做资源确认和现有数据库梳理：

1. 确认抖音主题域数据源连接方式。
2. 读取旧 RDS `youmei_ai` 的现有元数据表结构。
3. 确认哪些表由用户已有工具定期写入。
4. 确认云服务器是否可部署 Docker 服务。
5. 进入 M2 元数据库适配和 Repository。
