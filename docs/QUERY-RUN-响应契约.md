# query/run 响应契约

用途：固定第一版问数入口 `GET/POST /api/query/run` 的响应形状，供前端、后续 agent 和新会话接手时对齐。

## 入口

```text
GET /api/query/run
POST /api/query/run
```

`POST /api/query/run` 是正式入口，`GET /api/query/run` 保留为快速调试入口。

当前支持模式：

```text
draft      确定性 SQL 草稿模式，作为 fallback
llm_draft  DeepSeek / OpenAI-compatible LLM SQL 生成模式
```

## 顶层响应

接口外层由 FastAPI router 包一层：

```json
{
  "ok": true,
  "request_id": "string",
  "data": {}
}
```

`data` 是问数运行结果。

## data 稳定字段

```text
run_id            本次问数运行 ID
question          用户原始问题
mode              draft 或 llm_draft
started_at        UTC ISO 时间
answer_status     ok / not_ready / blocked
sql               最终候选 SQL；失败时可为 null
selected_table    选中的业务/物理表摘要；未选中时为 null
columns           执行结果列名数组
rows              执行结果行数组
row_count         返回行数
elapsed_ms        SQL 执行耗时；未执行时为 0
warnings          可展示的非致命提示
error             失败/阻断原因；成功时为 null
trace             运行过程追踪信息
```

`answer_status` 语义：

```text
ok         已生成 SQL 且执行成功
not_ready  资源或配置尚不满足执行条件，例如 LLM 未配置
blocked    生成、审查、schema 校验或执行前边界阻断
```

## selected_table

```text
table_id             元数据表 ID
table_name           执行库物理表名
table_display_name   业务展示名
```

## error

成功时：

```json
null
```

失败或阻断时：

```text
code       机器可读错误码
message    可展示/可记录的错误信息
stage      出错阶段
status     对应 answer_status
retryable  是否适合重试
```

当前错误码：

```text
llm_not_configured         LLM 未配置
llm_request_failed         LLM 请求失败
llm_sql_empty              LLM 未返回可执行 SQL
sql_safety_blocked         SQL safety review 阻断
schema_validation_failed   SQL 引用了选中 schema 之外的标识符
```

## trace

```text
trace.run_id
trace.started_at
trace.finished_at
trace.total_elapsed_ms
trace.steps
trace.draft_ready_to_execute
trace.draft_review
trace.execution_review
trace.executed
trace.llm
trace.error
```

`trace.steps[]`：

```text
step_id
status
elapsed_ms
error_code  可选，仅失败/阻断节点需要
```

`draft` 模式当前步骤：

```text
draft_and_execute
sql_execution
```

`llm_draft` 模式当前步骤：

```text
llm_sql_generation
sql_review
schema_validation
sql_execution
```

## 第一版前端消费建议

- 默认展示 `answer_status`、`selected_table`、`sql`、`columns`、`rows`、`warnings`。
- 成功时展示结果表格；`row_count=0` 也应作为成功空结果，不等同失败。
- `error != null` 时展示 `error.message`，并记录 `error.code` 和 `trace.steps`。
- `trace` 默认进入开发/管理员视图，不必在普通用户首屏完全展开。
- `llm.raw_content` 仅用于调试，前端不要作为稳定展示字段依赖。

## 当前测试集方向

M2 收尾阶段应继续补真实问题测试，优先覆盖：

```text
金额
数量
店铺
品牌
时间条件
排序
聚合
```

已拆出固定测试集：

```text
docs/QUERY-RUN-真实问题测试集.md
```

离线测试覆盖：

```text
tests/test_query_run_contract.py
tests/test_question_field_selection.py
```
