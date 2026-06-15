# query/run 真实问题测试集

用途：作为 M2 收尾和后续 M3/M4 演进的固定测试清单，避免只用一个 `SPU 销售金额 店铺` 样例判断系统可用性。

当前测试表：

```text
dws_douyin_spu_sales_detail
```

当前入口：

```text
POST /api/query/run
```

当前模式：

```text
draft
llm_draft
```

## 分级

```text
P0  M2 必须稳定：能选中正确表、生成安全 SELECT、返回结构化结果
P1  LLM 优先验证：需要模型理解维度/指标/筛选，但仍可单表完成
P2  后续能力：聚合、排序、时间解析、多轮上下文或更复杂口径
```

## P0 当前闭环用例

| ID | 问题 | 覆盖点 | 期望表 | 期望字段线索 | 当前建议模式 |
| --- | --- | --- | --- | --- | --- |
| QR-P0-001 | SPU 销售金额 店铺 | 金额、店铺、SPU 表定位 | `dws_douyin_spu_sales_detail` | 店铺字段、销售金额字段 | `draft` + `llm_draft` |
| QR-P0-002 | 看一下 SPU 的店铺销售金额 | 店铺维度、金额指标 | `dws_douyin_spu_sales_detail` | 店铺字段、销售金额字段 | `draft` + `llm_draft` |
| QR-P0-003 | SPU 销售金额和当日销售金额 | 多个金额指标 | `dws_douyin_spu_sales_detail` | `sjxsje`、`drsjxsje` 或相关金额字段 | `draft` + `llm_draft` |
| QR-P0-004 | SPU 店铺销售金额返回 5 条 | LIMIT 传入和结果行数 | `dws_douyin_spu_sales_detail` | 店铺字段、销售金额字段 | `draft` + `llm_draft` |

P0 验收：

```text
answer_status = ok
selected_table.table_name = dws_douyin_spu_sales_detail
sql 只读且包含 LIMIT
error = null
trace.executed = true
```

## P1 语义覆盖用例

| ID | 问题 | 覆盖点 | 期望字段线索 | 当前说明 |
| --- | --- | --- | --- | --- |
| QR-P1-001 | 按品牌看 SPU 销售数量 | 品牌、数量 | 品牌字段、数量字段 | 需要真实字段名进一步从元数据确认 |
| QR-P1-002 | 按日期看 SPU 销售金额 | 时间字段、金额 | 日期/时间字段、销售金额字段 | `draft` 可能只选字段，不会自动按日期聚合 |
| QR-P1-003 | 最近 30 天店铺销售金额 | 时间条件、店铺、金额 | 日期/时间字段、店铺字段、金额字段 | 时间解析/WHERE 仍待增强 |
| QR-P1-004 | SPU 商品名称和销售金额 | 商品属性、金额 | 商品/SPU 名称字段、金额字段 | 需要确认商品名称字段口径 |

P1 验收：

```text
selected_table 正确
sql 安全可执行
llm_draft 字段选择能覆盖问题中的主要维度/指标
无法满足时间/聚合时，warnings 或后续 explain 不应误导用户
```

## P2 后续能力用例

| ID | 问题 | 需要能力 | 当前状态 |
| --- | --- | --- | --- |
| QR-P2-001 | 按店铺汇总 SPU 销售金额 Top 10 | GROUP BY、SUM、ORDER BY、LIMIT | 待 LLM 聚合 SQL 稳定验证 |
| QR-P2-002 | 最近 30 天每天的销售金额趋势 | 时间解析、日期聚合 | 待时间字段识别和聚合生成 |
| QR-P2-003 | 哪些品牌销售金额最高 | 品牌字段、聚合排序 | 待品牌字段确认和聚合生成 |
| QR-P2-004 | 和上一个问题一样，但只看某个店铺 | 多轮上下文 | 待 conversation_context 接入 |

## 离线回归覆盖

已新增离线单测：

```text
tests/test_query_run_contract.py
tests/test_question_field_selection.py
```

离线测试不访问 RDS、不访问 LLM，只锁住：

```text
query/run 响应契约
LLM schema 白名单校验
确定性字段选择的最低语义命中
```

## 后续执行记录规则

每次真实接口复测后，把结论追加到 `docs/CHECKPOINT-项目检查点.md`，不要新建临时测试总结文件。

记录至少包含：

```text
测试日期
请求问题
mode
answer_status
selected_table.table_name
SQL 摘要
row_count
trace.steps
问题或风险
```
