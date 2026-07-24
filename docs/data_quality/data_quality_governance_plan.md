## 2026-07-10 口径补充：影刀/text 账单表剔除

- 影刀数据库（source database = `text`）里的账单类表，除“运费险账单”外，本批不进入质量规则配置。
- 剔除原因：这些账单表属于月度数据处理、手动上传或手动执行性质，不是日常自动采集链路；即使存在下游依赖，也不代表需要每日 freshness 或行数波动校验。
- 判定证据需要同时看表名/中文名和任务性质：如果任务是手动上传、手动执行、月度处理或财务账单拆分，默认剔除；不要因为有数据集消费或下游任务就提升为 P0/P1。
- 保留例外：运费险账单类表仍可进入候选，因为它已被确认为需要关注的业务链路。
- 这条规则只约束账单类表，不影响仍有下游且近期活跃的影刀抓取表，例如评价有礼、红包、推广、流量、销售等明细/结果表。
# 数据质量治理方案 v1

生成日期：2026-07-09

本文档汇总本轮基于 BI/StarRocks 元数据的数据质量治理方案。本轮只做证据化资产识别、优先级判断、规则模板设计和规则建议沉淀，不直接配置 BI 质量规则，不修改生产库，不删除任何表。

## 1. 本次治理目标

本次治理目标不是把所有 StarRocks 物理表都配置质量规则，而是建立一套可复用的证据化治理方法：

- 从 BI 工具和 StarRocks 元数据中识别表资产、使用关系、任务关系、字段风险和物理状态。
- 区分生产业务资产、BI 上传表、测试/临时表、静态/周期固化表、疑似废弃表。
- 建立表资产画像、治理优先级、风险标签和规则模板体系。
- 输出第一版规则建议，但所有待人工确认的表暂不进入规则配置。
- 为后续 AI 每日巡查元数据异常提供结构化输入。

本轮最终边界：

- `manual_confirm_required=true` 的表：全部暂不治理，不进入 BI 规则配置。
- `IGNORE`、Excel/upload/test-like、静态/周期固化依赖表：不生成强规则，只保留原因和证据。
- 当前第一批可直接上线规则的 P0/P1 表：暂为空。

## 2. 为什么不能只按 ODS/DWD/DWS/ADS 命名分层判断

BI 底层 StarRocks 表并不是一个严格受控的传统数仓分层环境，不能只按表名或 `ods/dwd/dws/ads` 判断治理优先级，原因如下：

- 表名可能是平台生成名，例如 `UD_...`、`ud_...`、`_cube_persist_...`，业务方通常不会按物理名搜索。
- 同一层级下同时存在正式业务表、Excel 上传表、测试表、持久化数据集表、临时过程表。
- `warehouse_layer_raw` 是元数据线索，不一定是可信业务分层。
- DWS/ADS 命名不一定代表正在被业务使用；ODS 命名也可能是核心报表或外部系统直接依赖的结果。
- 有下游依赖但长期未更新，不一定是异常，可能是周期性数据、配置表、历史快照或固化口径表。
- 命名像临时表的表，如果被核心报表、数据集、AI 或外部系统使用，仍可能是重点治理对象。

因此，本轮采用“证据优先”的判断方式：表名和分层只作为弱证据，不能单独决定角色、优先级或是否配置规则。

## 3. 本次采用的证据化判断方法

每张表综合以下证据判断：

| 证据类型 | 判断用途 |
| --- | --- |
| 物理存在证据 | 判断表是否真实存在于 StarRocks、行数、大小、创建时间、更新时间 |
| BI 资产证据 | 判断是否是 BI 工作表、数据集、Excel 上传表、资产目录节点 |
| 报表/数据集消费证据 | 判断是否被报表、分析项目、数据集使用 |
| 任务证据 | 判断是否有产出任务、任务类型、调度周期、下游任务数量 |
| SQL/查询证据 | 判断是否近期被查询、是否出现在 SQL 资源引用中 |
| 血缘证据 | 判断上游表、下游表、上游任务、下游任务 |
| 字段语义证据 | 判断主键、业务日期、金额、成本价、推广费、商品、店铺、订单、状态字段 |
| 资产目录证据 | 判断是否位于临时、测试、Excel 上传、业务目录等位置 |
| 冲突证据 | 判断是否需要 `REVIEW`，例如临时命名但有核心消费、长期未更新但近期查询 |

核心原则：

- 多证据一致时才提升治理优先级。
- 证据不足时不强行配置规则。
- 所有阈值缺少历史 profiling 时标记 `TODO`，不假装确定。
- 所有人工确认项暂不进入规则配置。

## 4. 元数据表使用说明

本轮主要使用以下元数据表：

| 元数据表 | 用途 |
| --- | --- |
| `std_data_government_meta_table` | 表治理汇总、表别名、owner、资产分类、行数、大小、未使用天数、表链接 |
| `ods_db_cube_work_table_info_f` | BI 工作表注册信息、中文名、来源文件、来源 SQL、上传表识别 |
| `ods_db_cube_work_table_field_info_f` | 字段字典、字段中文名、字段类型、字段注释、分区字段线索 |
| `ods_db_cube_tables` / `information_schema.tables` | 物理表是否存在、行数、大小、创建/更新时间、表注释 |
| `ods_db_cube_tables_config` | 主键、分区键、分桶键、表模型 |
| `ods_db_cube_partitions_meta` | 分区数量、最新分区、分区行数和大小 |
| `std_data_government_meta_task` | 表产出任务、任务 owner、任务类型、下游数量、任务链接 |
| `std_data_government_meta_task_instance` | 任务实例、产出行数、耗时、最近运行证据 |
| `dwd_data_government_meta_sql_related_resource` | SQL 审计、查询引用、任务资源引用、近期使用证据 |
| `ods_db_cube_table_data_collection` | BI 数据集 collection 关系 |
| `ods_db_cube_schedule_persist_info` | 数据集持久化表关系 |
| `ods_db_cube_report_form_item` | 报表卡片对数据集的引用 |
| `ods_db_cube_analysis_project_with_collection_relation` | 分析项目和数据集关系 |
| `ods_db_cube_asset_node` | BI 资产目录、临时/测试/上传目录识别 |

注意：当前部分中文表注释和字段注释存在编码显示问题，因此中文名只作为辅助证据；必要时需要从 BI 页面或用户确认中补正。

## 5. 表资产画像字段说明

表资产画像文件：[table_asset_profile.yml](C:/Users/24796/Documents/TEXT2SQL/config/dq/table_asset_profile.yml)

画像覆盖 984 张 StarRocks 物理表。核心字段分为以下几类：

| 字段组 | 说明 |
| --- | --- |
| 基础信息 | `table_name`、`database_name`、`schema_name`、`table_comment`、`owner_candidate`、`asset_category_candidate`、`warehouse_layer_raw`、`table_link` |
| 物理状态 | `row_count`、`data_size`、`partition_count`、`latest_partition`、`latest_update_time`、`create_time`、`unused_days`、`physical_status` |
| 字段画像 | `field_count`、`partition_field_candidate`、`biz_date_field_candidate`、`primary_key_candidate`、`unique_key_candidate`、日期/金额/成本价/推广费/指标/维度/状态/关联键字段 |
| 使用情况 | 报表、数据集、任务、查询、上下游任务、上下游表数量，以及 `usage_status` |
| 血缘状态 | `producing_tasks`、`consuming_tasks`、`upstream_tables`、`downstream_tables`、`lineage_status` |
| 候选角色 | `data_role_candidate` |
| 治理优先级 | `importance_candidate` |
| 规则建议 | `quality_rule_needed`、`recommended_rule_groups`、`risk_tags` |
| 证据 | `evidence_items`、`metadata_conflicts` |

画像不是最终事实表清单。它是治理候选池，包含正式表、上传表、测试表、临时表、静态固化表和疑似废弃表。

## 6. 表角色候选判断逻辑

当前角色枚举：

| 角色 | 判断逻辑 |
| --- | --- |
| `source_like` | 更像来源表或接入表，有下游任务，但不一定有上游 |
| `detail_like` | 明细表，通常行数较大、字段较多、有交易/订单/商品/金额等字段 |
| `dimension_like` | 维表或字典表，字段较少，包含商品、店铺、组织、人员、渠道等维度键 |
| `summary_like` | 汇总表，包含指标字段，有聚合或分析消费线索 |
| `result_like` | 结果表，被数据集、报表、持久化或核心分析使用 |
| `export_like` | 写出、下载、外部消费相关表 |
| `temp_or_intermediate_like` | 临时、持久化中间过程、工作表过程产物 |
| `stale_or_unused_like` | 长期无使用、空表或无消费证据的疑似废弃表 |
| `unknown` | 证据不足，暂不强行归类 |

关键修正：

- `UD_...`、Excel 上传、`test`、临时目录表，不能只因存在物理表就当成生产业务资产。
- 有下游引用但长期未更新，不自动视为 freshness 风险；如果无报表、无查询、无核心字段、无 S/A 影响，则按静态/周期固化候选处理。
- 只有影响 S/A 表或被核心消费的中间表，才进入规则候选。

## 7. 治理优先级判断逻辑

优先级枚举：

| 优先级 | 判断逻辑 |
| --- | --- |
| `S` | 核心业务决策、核心报表/数据集、AI/外部直接使用、关键结果表 |
| `A` | 重要报表/数据集/任务链路、核心指标字段、重要维表或核心中间表 |
| `B` | 有下游任务或常规中间/明细/汇总作用，但直接业务影响有限 |
| `C` | 低频使用、单任务内部使用、影响范围小、无核心字段 |
| `IGNORE` | 长期无使用、无下游、无报表、无查询、空表或废弃临时表候选 |
| `REVIEW` | 元数据冲突、来源不明、命名和使用矛盾、关键元数据缺失 |

本轮新增治理口径：

- 下游依赖只说明“链路引用过”，不等于必须持续更新。
- 周期性、配置型、历史快照型、固化口径型表，如果长期未更新但没有强消费证据，默认不配置规则。
- 所有 `manual_confirm_required=true` 的表，本轮不进入规则配置。

## 8. 风险标签体系

风险标签不按分层硬套，而按风险类型设计：

| 风险标签 | 适用场景 |
| --- | --- |
| `freshness_risk` | 活跃日更/小时更表、核心报表/数据集/任务链路使用表 |
| `silent_missing_risk` | API、影刀、ERP、钉钉、外部接入表，尤其是可能静默缺分区的表 |
| `row_count_anomaly_risk` | 活跃表、结果表、接入表的行数波动 |
| `primary_key_duplicate_risk` | 明细表、维表、结果表、写出表的候选主键重复 |
| `core_field_null_risk` | 主键、业务日期、店铺、商品、SKU、订单、金额等核心字段空值 |
| `amount_abnormal_risk` | 金额、销售额、退款额、库存金额等字段异常 |
| `cost_price_abnormal_risk` | 成本价、采购价异常 |
| `promotion_fee_abnormal_risk` | 推广费、广告费、投放费用异常 |
| `referential_integrity_risk` | 事实表和商品、店铺、成本、渠道、组织等维表关联失败 |
| `downstream_consistency_risk` | 结果表、汇总表、写出表、AI 使用表上下游对账 |
| `schema_change_risk` | API、影刀、DB 同步等外部来源 schema 漂移 |
| `stale_table_risk` | 疑似废弃、上传测试、静态固化或观察-only 表 |

## 9. 质量规则模板体系

规则模板文件：[rule_templates.yml](C:/Users/24796/Documents/TEXT2SQL/config/dq/rule_templates.yml)

预策 BI 规则配置逻辑参考：[yuce_bi_quality_rule_setting_logic.md](C:/Users/24796/Documents/TEXT2SQL/docs/data_quality/yuce_bi_quality_rule_setting_logic.md)

每个规则组包含：

- `description`
- `applicable_risk_tags`
- `required_metadata`
- `default_threshold`
- `default_alert_level_by_importance`
- `rule_sql_template`
- `manual_review_required`

模板只定义规则形态，不代表可以直接上线。上线前必须满足：

- 表不是 `IGNORE`。
- 表不是观察-only。
- 表没有 `manual_confirm_required=true`。
- 关键字段、业务日期、主键、阈值、上下游口径已有证据。
- 对应 SQL 模板已按 StarRocks 方言和 BI 质量平台要求调整。
- 日更 T+1 表的日期类存在性、空值、主键重复、金额格式等第一版规则，统一只检查昨天业务日期或昨天分区；不得使用“最近 3 天有数据”替代缺失日检查。
- 无可靠业务日期字段的表，优先使用任务本次产出行数或任务实例行数，不做全表历史扫描。
- 能使用预策 BI 内置表规则/字段规则表达的检查，优先使用内置配置项；SQL 规则只作为组合主键、跨表对账、字段结构变化、文本数值转换等兜底。

## 10. 第一批建议上线的 P0/P1 表

当前第一批建议上线的 P0/P1 表：无。

原因：

- 当前生成的规则建议中，所有有规则的高优先级表仍包含 `manual_confirm_required=true`。
- 用户已确认：所有待人工确认表暂不进入规则配置，暂不治理。
- 当前缺少足够的历史 profiling 证据来确认行数波动、金额异常、成本价倍数、推广费倍数、上下游对账阈值。
- 当前部分中文名、owner、业务日期、主键和业务口径仍需要补证据。

因此，本轮不建议直接上线任何 P0/P1 质量规则。P0/P1 只作为候选池保留，待后续补齐证据后再进入配置。

当前候选概况：

| 项目 | 数量 |
| --- | ---: |
| 表级建议文件 | 913 |
| 建议规则 | 1852 |
| 需要人工确认的表 | 802 |
| 本轮可直接上线表 | 0 |
| 观察-only / no strong rule 表 | 589 |

## 11. 暂不治理或建议清理的表

本轮暂不治理的表包括：

| 类型 | 数量 | 处理方式 |
| --- | ---: | --- |
| `IGNORE` / stale 候选 | 397 | 不配置规则，只保留证据；不直接删除 |
| Excel/upload/test-like isolated 表 | 81 | 不配置规则；可进入上传表清理观察清单 |
| 静态/周期固化下游依赖表 | 111 | 不配置规则、不人工确认；除非后续发现强消费证据 |

建议清理不等于删除。清理流程应单独包括：

1. 确认 BI 页面是否仍可见、是否有人收藏或使用。
2. 确认是否有报表、数据集、SQL、任务、外部系统引用。
3. 确认 owner 或创建人。
4. 观察一段时间后再归档或下线。
5. 删除或清表必须由平台 owner 或业务 owner 单独确认。

## 12. 人工确认事项

用户已确认：当前人工确认清单中的表全部暂不进入规则配置，暂不治理。

因此，人工确认事项在本轮只作为后续补证据清单，不作为上线前置任务。

后续如果要重启人工确认，应优先确认：

- S/A 候选表的 owner、业务负责人、告警接收人。
- 核心结果表是否真实被核心报表、AI、外部系统或业务方直接消费。
- 成本价、推广费、销售额、退款额、库存金额等字段的业务含义和阈值。
- 主键是否全局唯一，还是按店铺、日期、渠道、平台组合唯一。
- 业务日期字段和期望更新频率。
- 上下游对账的可比粒度、过滤条件和指标公式。
- Excel/upload/test-like 表是否应归档、保留或升级为正式资产。

## 13. 后续如何把规则接入 BI/数据质量平台

建议分四步接入：

1. 规则候选转正式规则

   从 [generated_rules](C:/Users/24796/Documents/TEXT2SQL/config/dq/generated_rules) 中选择不需要人工确认的表，或对人工确认表补齐证据后解除 `manual_confirm_required`。

2. SQL 模板实例化

   将规则模板中的占位符替换为实际字段：

   - `{database_name}`
   - `{table_name}`
   - `{biz_date_field}`
   - `{primary_key_fields}`
   - `{amount_field}`
   - `{cost_price_field}`
   - `{promotion_fee_field}`
   - `{upstream_table}`
   - `{downstream_table}`

   对日更 T+1 表，日期过滤统一实例化为：

   ```sql
   cast({biz_date_field} as date) = date_sub(current_date(), interval 1 day)
   ```

   该过滤用于定位“昨天应到但未到”的静默缺失问题；不要改成最近多天范围，否则某一天缺数会被其他日期的数据掩盖。

3. 在 BI 质量页面配置

   根据 `9.1.3.11 数据质量检查规则`，优先使用 BI 内置表规则和字段规则：

   - 昨天是否有数据：表规则 `单日行数，固定值`。
   - 行数波动：表规则 `单日行数，1、7、30 天波动率`。
   - 主键/核心字段非空：字段规则 `空值个数，固定值` 或 `空值个数/总行数，固定值`。
   - 单字段唯一/重复：字段规则 `重复值个数，固定值` 或 `重复值个数/总行数，固定值`。
   - 金额字段极值：字段规则 `最大值/最小值` 波动类规则。
   - 枚举合法性：字段规则 `枚举值异常值数量/占比`。

   只有当内置规则无法表达时，才使用 SQL 规则。

4. 上线后回写状态

   建议后续维护一个规则运行状态表或配置文件，记录：

   - 表名和中文名
   - 规则组
   - BI 规则 ID
   - 告警级别
   - 是否启用
   - 最近运行时间
   - 最近异常结果
   - owner
   - 变更记录

本轮不执行以上配置，只保留方案。

## 14. 后续如何每日让 AI 巡查元数据异常

建议每日 AI 巡查只看元数据，不扫描业务明细，重点发现“资产状态变化”和“治理证据变化”。

每日巡查输入：

- 最新 `std_data_government_meta_table`
- 最新 `std_data_government_meta_task`
- 最新 `dwd_data_government_meta_sql_related_resource`
- 最新 BI 数据集、报表、资产目录关系
- 最新 `information_schema.tables` 和分区元数据
- 上一日生成的 `table_asset_profile.yml`

每日巡查输出：

- 新增表、删除/消失表、重命名疑似表。
- 从无使用变为有报表/数据集/查询的表。
- 从普通表变为 S/A 候选的表。
- 原本观察-only 但出现强消费证据的表。
- 原本有规则候选但变成静态/固化的表。
- owner、主键、业务日期、字段结构发生变化的表。
- API/外部接入表 schema 变化。
- 大表行数、存储量、分区数异常变化。

每日巡查建议流程：

1. 重新生成表资产画像。
2. 与昨日画像做 diff。
3. 只输出变化清单，不重复输出全量表。
4. 对变化表重新计算角色、优先级、风险标签。
5. 只把“新增强证据”的表推入候选治理池。
6. 所有需要人工确认的表仍不自动配置规则。

建议每日巡查报告包括：

| 模块 | 内容 |
| --- | --- |
| 新增资产 | 新增物理表、BI 工作表、Excel 上传表 |
| 消失资产 | 昨日存在今日不存在的表或资产节点 |
| 使用变化 | 报表、数据集、查询、任务引用新增或消失 |
| 风险变化 | 新增金额字段、成本字段、推广费字段、schema 变化 |
| 优先级变化 | S/A/B/C/IGNORE/REVIEW 的变化原因 |
| 建议动作 | 观察、补证据、纳入候选、暂不治理、建议清理 |

短期建议：

- 保持当前全量画像和规则建议文件作为基线。
- 下一轮先做“画像 diff”和“BI 搜索可见性校验”，减少平台物理表误入业务资产。
- 等用户确认第一批真实核心表后，再进入 BI 质量规则配置。

