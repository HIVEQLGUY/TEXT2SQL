# 数据质量治理元数据底表使用说明 v1

更新时间：2026-07-09

## 1. 使用边界

本说明用于第一阶段梳理 `cubeappdata` 中可支撑数据资产目录、数据质量优先级和第一版表级质量规则建议的元数据底表。当前阶段只使用元数据、任务、血缘、SQL 审计、报表/数据集关系和物理统计信息，不扫描敏感业务明细数据，不修改业务 SQL，不配置任务运行告警。

任务失败、取消、超时、未运行等运行态问题由 BI/调度平台自身能力处理。本轮只把任务相关元数据作为证据，用于判断表的上游、下游、产出任务、消费任务、使用价值和治理优先级。

注意：部分表注释和字段注释在当前 StarRocks 连接下存在中文编码显示问题，因此本文以英文物理字段名和表关系为主，中文用途按字段结构和上下文推断。

## 2. 推荐证据链

后续给每张表判断治理优先级时，不应只看表名或数仓分层。建议按以下证据链综合评分：

1. 资产身份：`std_data_government_meta_table`、`ods_db_cube_work_table_info_f`、`ods_db_cube_tables`。
2. 字段字典：`ods_db_cube_work_table_field_info_f`。
3. 物理健康：`ods_db_cube_tables_config`、`ods_db_cube_partitions_meta`、`ods_db_cube_be_tablets`。
4. 产出任务：`std_data_government_meta_task`、`ods_db_cube_yuce_schedule_task_info_f`。
5. 任务产出和最近实例：`std_data_government_meta_task_instance`、`ods_db_cube_yuce_schedule_instance_exec_status`。
6. 上下游和血缘：`std_data_government_meta_data_resource`、`dwd_data_government_meta_sql_related_resource`、`ods_db_cube_yuce_schedule_task_dependency_info_f`、`ods_db_cube_yuce_schedule_task_related_object_info_f`。
7. 使用热度和成本：`std_data_government_meta_fast_engine_audit_mv`、`dwd_data_government_meta_sql_related_resource`。
8. BI 消费：`ods_db_cube_table_data_collection`、`ods_db_cube_schedule_persist_info`、`ods_db_cube_report_form_item`、`ods_db_cube_report_form_distribution`、`ods_db_cube_report_form`、`ods_db_cube_user_analysis_project`。
9. 资产目录归属：`ods_db_cube_asset_node`。

## 3. 总览

| 表 | 行数证据 | 推荐优先级 | 核心用途 | 敏感性 |
| --- | ---: | --- | --- | --- |
| `std_data_government_meta_table` | 1,026,645 | P0 | 表治理汇总、表画像主事实 | owner/link 低敏 |
| `ods_db_cube_work_table_info_f` | 808 | P0 | BI 工作表/业务表注册信息 | owner/source_sql 中敏 |
| `ods_db_cube_work_table_field_info_f` | 22,811 | P0 | 字段字典和字段质量规则候选 | attrs 中敏 |
| `ods_db_cube_tables` | 5,411 | P0 | StarRocks 表级统计快照 | 低 |
| `ods_db_cube_tables_config` | 5,415 | P0 | 表模型、主键、分区、分桶 | 低 |
| `ods_db_cube_partitions_meta` | 40,495 | P1 | 分区行数、大小、版本、存储路径 | storage_path 中敏 |
| `ods_db_cube_be_tablets` | 85,484 | P2 | tablet/桶级倾斜和存储健康 | data_dir 中敏 |
| `std_data_government_meta_task` | 104,991 | P0 | 表到产出任务、任务治理汇总 | owner/link 低敏 |
| `std_data_government_meta_task_instance` | 221,866 | P1 | 任务实例产出行数和耗时证据 | owner/link 低敏 |
| `dwd_data_government_meta_sql_related_resource` | 3,013,625 | P0 | SQL 审计、资源使用、血缘证据 | SQL/user/clientIp 中高敏 |
| `std_data_government_meta_data_resource` | 8,790 | P0 | 对象-资源关系 | owner/link 低敏 |
| `std_data_government_meta_fast_engine_audit_mv` | 777,396 | P1 | 查询审计、热度、成本 | SQL/user/clientIp 中高敏 |
| `ods_db_cube_yuce_schedule_task_info_f` | 3,656 | P0 | 原始调度任务定义 | task_params 中敏 |
| `ods_db_cube_yuce_schedule_task_instance_info_f` | 226,443 | P1 | 原始调度实例 | task_params/ext 中敏 |
| `ods_db_cube_yuce_schedule_instance_exec_status` | 225,956 | P1 | 执行 SQL、影响行数、异常 | exec_sql/exception 中敏 |
| `ods_db_cube_yuce_schedule_task_dependency_info_f` | 3,749 | P1 | 任务依赖边 | 低 |
| `ods_db_cube_yuce_schedule_task_related_object_info_f` | 6,114 | P0 | 任务关联对象，找表任务入口 | 低 |
| `ods_db_cube_yuce_schedule_triggle_config_info_f` | 3,119 | P2 | 调度触发配置 | trigger_config 中敏 |
| `ods_db_cube_etl_schedule_config` | 1,388 | P1 | ETL 映射、迁移、分区策略 | config 中敏 |
| `ods_db_etl_develop_node_info` | 142 | P2 | ETL 节点和上下游 JSON | JSON 中敏 |
| `ods_db_etl_develop_project` | 22 | P3 | ETL 项目目录 | 低 |
| `ods_db_cube_table_data_collection` | 7,388 | P0 | BI 数据集/collection | order_fields 中敏 |
| `ods_db_cube_schedule_persist_info` | 5,228 | P0 | 物化表、数据集持久化关系 | columns/view_info 中敏 |
| `ods_db_cube_user_analysis_project` | 391 | P1 | 分析项目/看板项目 | user_id 低敏 |
| `ods_db_cube_analysis_project_with_collection_relation` | 6,559 | P0 | 项目-数据集关系 | 低 |
| `ods_db_cube_report_form` | 58 | P1 | 报表/看板主体 | user_id/url 中敏 |
| `ods_db_cube_report_form_item` | 834 | P0 | 图表卡片和数据集引用 | config_json 中敏 |
| `ods_db_cube_report_form_distribution` | 954 | P2 | 报表布局、联动、跳转 | JSON 中敏 |
| `ods_db_cube_asset_node` | 974 | P1 | 资产目录树 | user_id 低敏 |

## 4. 表/字段资产目录

### `std_data_government_meta_table`

- 用途：表治理汇总主表，适合作为数据资产目录和治理优先级评分的主事实表。
- 可支撑治理指标：表行数、存储大小、未使用天数、小文件数量、分区数量、资产分类、数仓分层、owner 覆盖、表链接可达性、冷表/热表判断。
- 关键字段：`calculated_date`、`table_id`、`table_name`、`alias_table_name`、`table_owner`、`main_category`、`sub_category`、`partition_count`、`datafile_count`、`tiny_datafile_count`、`data_size`、`row_count`、`unused_days`、`create_time`、`update_time`、`table_schema`、`data_warehouse_layering`、`asset_class`、`table_link`。
- 可能关联键：`table_id` -> `std_data_government_meta_task.table_id`；`table_name` + `table_schema` -> `ods_db_cube_tables`、`ods_db_cube_tables_config`、`ods_db_cube_partitions_meta`；`table_name` -> SQL 审计表 `table_name`。
- 敏感字段：`table_owner`、`table_link` 属低敏。可用于 owner 统计和跳转，不应公开到外部。
- 推荐优先级：P0。
- 谨慎点：该表像治理汇总表，可能按日期累积快照；使用时要按最新 `calculated_date` 去重，不要直接把 100 万行当作当前表数量。

### `ods_db_cube_work_table_info_f`

- 用途：BI 工具注册的工作表/业务表信息，适合补充表中文别名、来源表、来源 SQL、owner、数据更新时间。
- 可支撑治理指标：业务名覆盖、owner 覆盖、源 SQL 是否存在、直接数据源或魔方数据源、总记录数、最近数据更新时间、来源文件名、表类型。
- 关键字段：`id`、`source_id`、`creator_id`、`owner_id`、`table_type`、`table_name`、`table_schema`、`src_table_name`、`alias_table_name`、`comment`、`source_collection_id`、`source_sql`、`uniq_field_name`、`use_raw_data_source`、`data_last_update_time`、`total_row_number`、`source_file_name`、`namespace`。
- 可能关联键：`id` -> `ods_db_cube_work_table_field_info_f.table_id`、`ods_db_cube_table_data_collection.table_id`、`std_data_government_meta_task.table_id`；`source_collection_id` -> `ods_db_cube_table_data_collection.id`；`table_name` -> 物理表。
- 敏感字段：`source_sql` 可能包含业务逻辑和字段；`owner_id`、`creator_id` 低敏。
- 推荐优先级：P0。
- 谨慎点：表名和别名可能不规范；表角色不能只按 `table_type` 或名称判断，应结合任务、报表和审计证据。

### `ods_db_cube_work_table_field_info_f`

- 用途：BI 工作表字段字典，是字段级质量规则候选的重要来源。
- 可支撑治理指标：字段数量、字段中文名/别名覆盖、字段类型、分区字段、原始字段映射、字段状态、字段顺序、字段扩展属性。
- 关键字段：`id`、`table_id`、`pos`、`field_name`、`alias_field_name`、`comment`、`field_type`、`field_type_enum`、`status`、`source_field_id`、`orig_field_type`、`attrs`、`partition_key`、`orig_field_name`。
- 可能关联键：`table_id` -> `ods_db_cube_work_table_info_f.id`、`ods_db_cube_table_data_collection.table_id`；`field_name`/`orig_field_name` -> 质量规则字段候选。
- 敏感字段：`attrs` 可能包含扩展配置，不应整段外发。
- 推荐优先级：P0。
- 谨慎点：字段规则配置前要确认字段是否在当前任务质量页面可选；若 UI 字段下拉不可用，可转成 SQL 规则。

### `ods_db_cube_tables`

- 用途：StarRocks `information_schema.tables` 风格表级快照。
- 可支撑治理指标：表是否存在、表类型、行数估算、数据大小、创建/更新时间、表注释、空表和长期未更新表识别。
- 关键字段：`TABLE_SCHEMA`、`TABLE_NAME`、`TABLE_TYPE`、`ENGINE`、`TABLE_ROWS`、`DATA_LENGTH`、`INDEX_LENGTH`、`CREATE_TIME`、`UPDATE_TIME`、`TABLE_COMMENT`。
- 可能关联键：`TABLE_SCHEMA` + `TABLE_NAME` -> `ods_db_cube_tables_config`、`ods_db_cube_partitions_meta`、业务表名。
- 敏感字段：低。
- 推荐优先级：P0。
- 谨慎点：`TABLE_ROWS` 和 `DATA_LENGTH` 是统计口径，适合优先级和波动规则建议，不宜单独作为精确审计结果。

### `ods_db_cube_tables_config`

- 用途：物理表模型配置，补充主键、分区、分桶、排序和属性。
- 可支撑治理指标：是否有主键、主键质量规则候选、分区字段识别、分桶合理性、表模型识别、属性缺失检查。
- 关键字段：`TABLE_SCHEMA`、`TABLE_NAME`、`TABLE_ENGINE`、`TABLE_MODEL`、`PRIMARY_KEY`、`PARTITION_KEY`、`DISTRIBUTE_KEY`、`DISTRIBUTE_TYPE`、`DISTRIBUTE_BUCKET`、`SORT_KEY`、`PROPERTIES`、`TABLE_ID`。
- 可能关联键：`TABLE_SCHEMA` + `TABLE_NAME` -> `ods_db_cube_tables`、`ods_db_cube_partitions_meta`；`TABLE_ID` -> `ods_db_cube_be_tablets.TABLE_ID`。
- 敏感字段：低。
- 推荐优先级：P0。
- 谨慎点：主键配置不等于业务唯一键成立，后续规则建议中应把主键重复检查列为候选，而不是默认通过。

### `ods_db_cube_partitions_meta`

- 用途：分区级物理元数据。
- 可支撑治理指标：最新分区是否生成、分区行数/大小波动、空分区、分区过多、分区版本滞后、冷热存储、数据缓存、分区存储路径。
- 关键字段：`DB_NAME`、`TABLE_NAME`、`PARTITION_NAME`、`PARTITION_ID`、`VISIBLE_VERSION`、`VISIBLE_VERSION_TIME`、`PARTITION_KEY`、`PARTITION_VALUE`、`DISTRIBUTION_KEY`、`BUCKETS`、`REPLICATION_NUM`、`STORAGE_MEDIUM`、`DATA_SIZE`、`ROW_COUNT`、`STORAGE_PATH`。
- 可能关联键：`DB_NAME` + `TABLE_NAME` -> `ods_db_cube_tables`；`PARTITION_ID` -> `ods_db_cube_be_tablets.PARTITION_ID`。
- 敏感字段：`STORAGE_PATH` 暴露物理路径，中敏。
- 推荐优先级：P1。
- 谨慎点：`DATA_SIZE`、`ROW_COUNT` 是字符串字段，使用前要规范化单位和类型。

### `ods_db_cube_be_tablets`

- 用途：BE tablet/桶级物理明细。
- 可支撑治理指标：tablet 状态、行数和数据大小倾斜、rowset 数量、segment 数量、版本异常、数据目录分布。
- 关键字段：`BE_ID`、`TABLE_ID`、`PARTITION_ID`、`TABLET_ID`、`NUM_VERSION`、`MAX_VERSION`、`MIN_VERSION`、`NUM_ROWSET`、`NUM_ROW`、`DATA_SIZE`、`INDEX_MEM`、`STATE`、`TYPE`、`DATA_DIR`、`SHARD_ID`、`INDEX_DISK`、`MEDIUM_TYPE`、`NUM_SEGMENT`。
- 可能关联键：`TABLE_ID` -> `ods_db_cube_tables_config.TABLE_ID`；`PARTITION_ID` -> `ods_db_cube_partitions_meta.PARTITION_ID`。
- 敏感字段：`DATA_DIR` 暴露服务器路径，中敏。
- 推荐优先级：P2。
- 谨慎点：用于物理治理和性能治理，不是第一版表级数据质量规则的主入口。

## 5. 任务、血缘和使用关系

### `std_data_government_meta_task`

- 用途：任务治理汇总表，适合从表反查产出任务、owner、任务类型和血缘入口。
- 可支撑治理指标：是否有产出任务、任务 owner、任务状态、下游数量、写入模式、期望周期、最近实例、成功实例、任务产出行数。
- 关键字段：`calculated_date`、`task_code`、`task_name`、`task_owner`、`task_type`、`write_mode`、`expect_interval`、`task_status`、`last_instance_id`、`success_instance_id`、`duration`、`single_influence_num`、`downstream_count`、`table_name`、`table_id`、`data_lineage_link`。
- 可能关联键：`task_code` -> 调度任务表和实例表；`table_name`/`table_id` -> 表资产；`data_lineage_link` -> BI 页面。
- 敏感字段：`task_owner`、链接低敏。
- 推荐优先级：P0。
- 谨慎点：本轮不做任务失败告警；只用任务状态和产出行数判断表是否重要、是否需要数据结果质量规则。

### `std_data_government_meta_task_instance`

- 用途：任务实例治理汇总。
- 可支撑治理指标：实例产出行数、耗时分布、最近成功实例、任务产出波动基线、产出后数据静默缺失风险。
- 关键字段：`instance_id`、`task_code`、`task_name`、`task_owner`、`task_type`、`write_mode`、`expect_interval`、`status`、`start_time`、`end_time`、`duration`、`single_influence_num`、`downstream_count`、`table_name`、`table_id`、`instance_link`。
- 可能关联键：`task_code` -> `std_data_government_meta_task.task_code`；`table_name`/`table_id` -> 表资产。
- 敏感字段：`task_owner`、`instance_link` 低敏。
- 推荐优先级：P1。
- 谨慎点：可用于给表级规则设置初始阈值，但任务失败本身不在本次质量规则范围。

### `dwd_data_government_meta_sql_related_resource`

- 用途：SQL 审计和资源关联明细，适合识别表使用热度、被哪些 SQL/任务/对象消费、扫描成本和血缘。
- 可支撑治理指标：表被查询次数、最近使用时间、扫描行数/扫描量、返回行数、CPU/内存成本、错误 SQL、下游对象、任务和资源链接、AI/写出/报表使用痕迹。
- 关键字段：`calculated_date`、`queryId`、`timestamp`、`queryType`、`clientIp`、`user`、`authorizedUser`、`catalog`、`db`、`state`、`errorCode`、`queryTime`、`scanVolume`、`scanRows`、`returnRows`、`cpuCost`、`memCost`、`stmt`、`digest`、`sql_id`、`sql_type`、`task_code`、`task_name`、`task_owner`、`object_id`、`object_name`、`object_type`、`resource_id`、`resource_name`、`resource_type`、`table_name`。
- 可能关联键：`table_name` -> 表资产；`task_code` -> 任务；`object_id`/`resource_id` -> `std_data_government_meta_data_resource`、BI 对象。
- 敏感字段：`stmt`、`clientIp`、`user`、`authorizedUser`、`profile_*` 中高敏；默认只做聚合统计，不导出原始 SQL。
- 推荐优先级：P0。
- 谨慎点：行数较大，后续查询必须限定日期窗口、字段和聚合粒度。

### `std_data_government_meta_data_resource`

- 用途：对象和资源关系表，可把报表/任务/数据集/表等对象关联起来。
- 可支撑治理指标：资源被哪些对象引用、资源 owner、资源类型分布、下游影响面、孤儿资源识别。
- 关键字段：`object_id`、`object_name`、`object_owner`、`object_type`、`object_create_time`、`object_update_time`、`object_link`、`resource_id`、`resource_name`、`resource_owner`、`resource_type`、`resource_link`。
- 可能关联键：`object_id`/`resource_id` -> BI 项目、数据集、报表、任务对象；`resource_name` -> 表名或资源名。
- 敏感字段：owner 和链接低敏。
- 推荐优先级：P0。
- 谨慎点：对象类型枚举需要后续用样本脱敏确认，不应猜测全部含义。

### `std_data_government_meta_fast_engine_audit_mv`

- 用途：查询审计宽表或物化视图，偏查询性能和使用热度。
- 可支撑治理指标：查询次数、最近访问、查询失败率、扫描行数/扫描量、慢查询、命中物化视图、成本高表。
- 关键字段：`calculated_date`、`queryId`、`timestamp`、`queryType`、`clientIp`、`user`、`authorizedUser`、`db`、`state`、`errorCode`、`queryTime`、`scanVolume`、`scanRows`、`returnRows`、`cpuCost`、`memCost`、`stmt`、`digest`、`candidateMVs`、`hitMvs`、`sql_id`、`task_type`、`object_id`、`object_type`、`instance_id`。
- 可能关联键：`queryId`/`sql_id` -> SQL 审计；`object_id` -> 数据资源关系。
- 敏感字段：`stmt`、用户、IP 中高敏；默认聚合使用。
- 推荐优先级：P1。
- 谨慎点：没有直接 `table_name` 字段，做表级治理时优先用 `dwd_data_government_meta_sql_related_resource`。

### `ods_db_cube_yuce_schedule_task_info_f`

- 用途：原始调度任务定义，能找到任务 code、任务名、任务类型、状态和参数。
- 可支撑治理指标：表是否有刷新任务、任务类型、任务状态、任务参数中的目标表/源表/字段映射。
- 关键字段：`id`、`code`、`task_name`、`task_type`、`priority`、`status`、`task_template_code`、`task_queue_name`、`task_params`、`group_params`、`last_instance_id`、`admin_id`、`create_time`、`update_time`。
- 可能关联键：`code` -> `std_data_government_meta_task.task_code`、实例表、质量页面 `/#/task_detail/{code}`。
- 敏感字段：`task_params`、`group_params` 可能包含 SQL、字段映射或数据源配置，中敏。
- 推荐优先级：P0。
- 谨慎点：解析 `task_params` 需要结构化处理，不要把整段参数直接展示给业务用户。

### `ods_db_cube_yuce_schedule_task_instance_info_f`

- 用途：原始调度任务实例信息。
- 可支撑治理指标：实例状态、失败次数、调度地址、业务日期、实例分组、依赖关系。
- 关键字段：`code`、`dag_instance_id`、`task_name`、`task_type`、`task_params`、`ext_params`、`related_instance_ids`、`status`、`fail_count`、`scheduling_address`、`dependencies`、`ext`、`instance_group_id`、`biz_date`、`create_time`、`update_time`。
- 可能关联键：`code` -> 任务 code；`dag_instance_id` -> 执行状态表。
- 敏感字段：`task_params`、`ext_params`、`dependencies`、`ext` 中敏。
- 推荐优先级：P1。
- 谨慎点：本轮不做运行告警；只用它补充表的任务活跃度和最近实例证据。

### `ods_db_cube_yuce_schedule_instance_exec_status`

- 用途：任务执行状态和执行 SQL 明细。
- 可支撑治理指标：任务影响行数、业务日期、执行 SQL、异常签名、最近写入量基线、静默缺失初筛。
- 关键字段：`task_code`、`task_queue_name`、`schedule_time`、`start_time`、`end_time`、`expect_exec_time`、`influence_num`、`single_influence_num`、`exception`、`exec_sql`、`status`、`biz_date`、`retry_times`、`dag_instance_id`、`last_queue_time`。
- 可能关联键：`task_code` -> 任务表；`dag_instance_id` -> 实例表。
- 敏感字段：`exec_sql`、`exception` 中敏。
- 推荐优先级：P1。
- 谨慎点：可以辅助生成“任务成功后产出行数异常”规则，但不能替代真实表级数据结果检查。

### `ods_db_cube_yuce_schedule_task_dependency_info_f`

- 用途：任务依赖关系边。
- 可支撑治理指标：上游依赖数量、下游任务数量、关键链路识别、表治理优先级加权。
- 关键字段：`id`、`task_code`、`depend_code`、`create_time`、`update_time`。
- 可能关联键：`task_code`、`depend_code` -> 调度任务 code。
- 敏感字段：低。
- 推荐优先级：P1。
- 谨慎点：只描述任务依赖，不一定等价于字段级血缘。

### `ods_db_cube_yuce_schedule_task_related_object_info_f`

- 用途：任务关联对象表，是从表/报表/数据集定位任务的关键桥表。
- 可支撑治理指标：任务产出或消费的对象、任务和表/分析项目/卡片的关联、同对象互斥任务。
- 关键字段：`id`、`task_code`、`related_object_id`、`related_object_type`、`related_object_name`、`task_mutual_with_same_object`、`create_time`、`update_time`。
- 可能关联键：`task_code` -> 任务；`related_object_id` -> 工作表、collection、分析项目、报表卡片等对象。
- 敏感字段：低。
- 推荐优先级：P0。
- 谨慎点：`related_object_type` 枚举需要后续脱敏样本确认。

### `ods_db_cube_yuce_schedule_triggle_config_info_f`

- 用途：调度触发配置。
- 可支撑治理指标：期望调度周期、动态触发、触发类型、任务模板，用于判断表更新频率和规则基线窗口。
- 关键字段：`id`、`schedule_type`、`schedule_code`、`trigger_type`、`trigger_config`、`expect_interval`、`enable_dynamic_trigger`、`task_template_code`、`mix_interval_tag`。
- 可能关联键：`schedule_code` -> 任务 code 或调度 code；`task_template_code` -> 任务模板。
- 敏感字段：`trigger_config` 中敏。
- 推荐优先级：P2。
- 谨慎点：只用于规则窗口建议；不在本轮做任务运行告警。

### `ods_db_cube_etl_schedule_config`

- 用途：ETL 调度配置，包含查询条件、字段映射、迁移策略、分区策略、分布策略。
- 可支撑治理指标：字段映射完整性、分区策略、增量条件、写入策略、规则适用粒度。
- 关键字段：`id`、`update_strategy`、`sql_query_condition_config`、`field_name_config`、`task_trigger_config`、`migrate_strategy_config`、`partition_strategy_config`、`field_mapping_config`、`distribution_strategy_config`、`advanced_query_condition`。
- 可能关联键：`id` 需与任务参数或配置对象进一步确认。
- 敏感字段：各类 `*_config` 可能包含 SQL、字段映射、条件，中敏。
- 推荐优先级：P1。
- 谨慎点：解析成本较高，适合作为第二阶段规则精细化证据。

### `ods_db_etl_develop_node_info`

- 用途：ETL 开发节点信息，含工作版本和生产版本上下游 JSON。
- 可支撑治理指标：ETL 节点活跃度、上下游关系、项目归属、发布状态。
- 关键字段：`id`、`name`、`type`、`creator_id`、`project_id`、`last_publish_time`、`prod_version_id`、`node_status`、`working_version_id`、`last_editor_id`、`working_version_down_stream_json`、`prod_version_down_stream_json`。
- 可能关联键：`project_id` -> `ods_db_etl_develop_project.id`。
- 敏感字段：上下游 JSON 中敏。
- 推荐优先级：P2。
- 谨慎点：只覆盖 ETL 开发侧，不一定覆盖全部 BI 刷新任务。

### `ods_db_etl_develop_project`

- 用途：ETL 项目目录。
- 可支撑治理指标：ETL 项目数量、项目 owner、项目更新时间、项目下节点分组。
- 关键字段：`id`、`name`、`creator_id`、`canvas`、`create_time`、`update_time`、`folder_id`。
- 可能关联键：`id` -> `ods_db_etl_develop_node_info.project_id`。
- 敏感字段：`canvas` 可能包含节点布局/配置，中敏。
- 推荐优先级：P3。
- 谨慎点：更偏资产导航，不是表级质量优先级的核心证据。

## 6. BI、报表和数据集资产

### `ods_db_cube_table_data_collection`

- 用途：BI 数据集/collection 定义，是识别报表消费表和数据集资产的核心表。
- 可支撑治理指标：数据集数量、数据集状态、是否持久化、项目归属、来源、创建人、更新时间、是否替换数据集。
- 关键字段：`id`、`project_id`、`name`、`table_id`、`table_type`、`order_fields`、`persist_enable`、`persist_version`、`status`、`project_type`、`creator_id`、`replace_tag`、`collection_source`、`meta_version`、`sample_method`。
- 可能关联键：`table_id` -> `ods_db_cube_work_table_info_f.id`；`id` -> `ods_db_cube_analysis_project_with_collection_relation.collection_id`、`ods_db_cube_report_form_item.src_collection_id`、`ods_db_cube_schedule_persist_info.object_id`。
- 敏感字段：`order_fields` 可能包含字段配置，中敏。
- 推荐优先级：P0。
- 谨慎点：不要把 `_persist_COLLECTION_*` 直接当元数据主表，应通过本表和持久化信息识别。

### `ods_db_cube_schedule_persist_info`

- 用途：数据集/对象物化信息，连接 BI 对象和实际 `_persist_*` 物化表。
- 可支撑治理指标：物化表名、最后物化时间、物化状态、物化字段、存储介质、是否报表底表、物化版本。
- 关键字段：`id`、`object_id`、`object_type`、`object_name`、`version`、`mvcc_version`、`create_table_param`、`persist_table_name`、`last_persist_time`、`columns`、`view_info`、`status`、`python_exec_info`、`storage_medium`、`is_report_base_collection`、`ontology_object_type_relation_uniq_snapshot`。
- 可能关联键：`object_id` -> collection、报表卡片或分析对象；`persist_table_name` -> 物理 `_persist_*` 表；`version` -> 报表卡片 `persist_version`。
- 敏感字段：`create_table_param`、`columns`、`view_info`、`python_exec_info` 中敏。
- 推荐优先级：P0。
- 谨慎点：质量规则应优先作用于正式产出表或稳定物化表；临时物化表需通过状态和对象关系确认。

### `ods_db_cube_user_analysis_project`

- 用途：用户分析项目/BI 项目主体。
- 可支撑治理指标：项目状态、项目发布情况、是否启用刷新、项目更新时间、项目数量。
- 关键字段：`id`、`name`、`description`、`user_id`、`status`、`type`、`enable_refresh`、`last_publish_time`、`create_time`、`update_time`、`namespace`。
- 可能关联键：`id` -> `ods_db_cube_analysis_project_with_collection_relation.project_id`、`ods_db_cube_report_form.project_id`、`ods_db_cube_table_data_collection.project_id`。
- 敏感字段：`user_id` 低敏；`cover_img` 不建议读取。
- 推荐优先级：P1。
- 谨慎点：项目存在不代表实际活跃，应结合报表卡片、数据集和 SQL 审计。

### `ods_db_cube_analysis_project_with_collection_relation`

- 用途：分析项目和数据集关系桥表。
- 可支撑治理指标：数据集被多少项目使用、项目影响面、孤立数据集识别。
- 关键字段：`id`、`project_id`、`collection_id`、`create_time`、`update_time`。
- 可能关联键：`project_id` -> 分析项目；`collection_id` -> `ods_db_cube_table_data_collection.id`。
- 敏感字段：低。
- 推荐优先级：P0。
- 谨慎点：只反映项目-数据集关系，不一定反映每个图表实际使用。

### `ods_db_cube_report_form`

- 用途：报表/看板主体表。
- 可支撑治理指标：报表状态、负责人、可访问 URL、最近数据更新时间、发布时间、展示状态、是否移动布局。
- 关键字段：`id`、`project_id`、`form_name`、`user_id`、`liable_id`、`status`、`access_url`、`last_data_update_time`、`type`、`create_time`、`update_time`、`last_publish_time`、`display`、`namespace`。
- 可能关联键：`id` -> `ods_db_cube_report_form_distribution.form_id`；`project_id` -> 分析项目。
- 敏感字段：`user_id`、`liable_id`、`access_url`、`thumbnail`、`media_url` 中敏，默认只读必要字段。
- 推荐优先级：P1。
- 谨慎点：报表状态要结合卡片和数据集关系判断，不宜只看报表表本身。

### `ods_db_cube_report_form_item`

- 用途：报表卡片/图表项，是识别数据集被最终消费的关键表。
- 可支撑治理指标：图表数量、图表类型、卡片状态、引用数据集、最近数据更新时间、是否允许探索、缓存设置、卡片业务类型。
- 关键字段：`id`、`alias_name`、`item_name`、`chart_type`、`src_collection_id`、`persist_version`、`config_json`、`status`、`order_params`、`is_drill_down`、`allow_exploration`、`last_data_update_time`、`project_type`、`creator_id`、`data_config_json`、`card_biz_type`、`cache_preheating`、`use_cache`。
- 可能关联键：`src_collection_id` -> `ods_db_cube_table_data_collection.id`；`persist_version` -> `ods_db_cube_schedule_persist_info.version`；`id` -> `ods_db_cube_report_form_distribution.form_object_id`。
- 敏感字段：`config_json`、`data_config_json`、`order_params` 中敏，可能包含字段、筛选、SQL 配置。
- 推荐优先级：P0。
- 谨慎点：图表配置 JSON 需要脱敏解析，不能直接外发。

### `ods_db_cube_report_form_distribution`

- 用途：报表布局、卡片位置、联动和跳转配置。
- 可支撑治理指标：卡片是否在报表中展示、报表联动依赖、页面布局影响面、移动端布局。
- 关键字段：`id`、`form_id`、`form_object_id`、`object_type`、`show_flag`、`card_index`、`linkage_json`、`jumping_json`、`x`、`y`、`width`、`height`、`ontology_linkage_json`、`mobile_layout_json`。
- 可能关联键：`form_id` -> `ods_db_cube_report_form.id`；`form_object_id` -> `ods_db_cube_report_form_item.id`。
- 敏感字段：`linkage_json`、`jumping_json`、`ontology_linkage_json`、`mobile_layout_json` 中敏。
- 推荐优先级：P2。
- 谨慎点：主要用于影响面排序，不是质量规则主依据。

### `ods_db_cube_asset_node`

- 用途：BI 资产目录树。
- 可支撑治理指标：资产目录归属、资产是否挂目录、目录层级、资产类型、资产 owner。
- 关键字段：`id`、`parent_id`、`name`、`pos`、`user_id`、`asset_type`、`obj_id`、`asset_class`、`create_time`、`update_time`。
- 可能关联键：`obj_id` -> 表、数据集、报表或项目对象；`parent_id` -> 本表 `id`。
- 敏感字段：`user_id` 低敏。
- 推荐优先级：P1。
- 谨慎点：目录结构不能证明表仍被使用，只能作为资产管理和展示维度。

## 7. 敏感字段使用规范

以下字段默认只用于本地聚合和规则推断，不进入用户可见明细：

- SQL 明文：`stmt`、`exec_sql`、`source_sql`、`view_info`、`config_json`、`data_config_json`。
- 用户和网络：`user`、`authorizedUser`、`user_id`、`creator_id`、`owner_id`、`clientIp`、`task_owner`。
- 链接和路径：`object_link`、`resource_link`、`table_link`、`instance_link`、`access_url`、`STORAGE_PATH`、`DATA_DIR`。
- 配置 JSON：`task_params`、`group_params`、`ext_params`、`trigger_config`、`field_mapping_config`、`create_table_param`、`columns`、`python_exec_info`。

## 8. 第一版可支撑的治理判断

基于以上元数据，第一版可以不扫描业务明细，先形成以下表级治理判断：

1. 高价值表：有报表卡片消费、有分析项目消费、有下游任务、有 SQL 查询热度、有 owner。
2. 高风险表：大表、分区异常、长期未更新但仍被使用、主键/分区配置缺失、物化状态异常、最近产出行数波动。
3. 沉默缺失风险：任务成功但 `single_influence_num` 异常偏低，或表/分区 `ROW_COUNT`、`TABLE_ROWS` 较历史基线异常。
4. 字段规则候选：字段字典中主键、分区字段、金额字段、日期字段、商品/店铺/订单字段、owner/负责人字段。
5. 成本治理候选：被高频 SQL 扫描、扫描量大、返回行数小、查询失败多、tablet/分区倾斜明显。
6. 使用价值下降候选：`unused_days` 高、没有报表/数据集/任务下游、SQL 审计低热度、仅存在历史备份或临时物化。

## 9. 后续阶段建议

第二阶段建议基于本文形成表级评分模型：

- `价值分`：报表消费、数据集消费、任务下游、SQL 热度、owner、资产目录。
- `风险分`：大表、分区多、小文件多、未更新、字段字典缺失、无主键、物化异常。
- `规则优先级`：价值分高且风险分高的表优先配置质量规则。
- `规则模板`：行数非零、行数波动、最新分区/日期、主键重复、关键字段空值率、金额非负、上下游行数一致、报表底表完整性。

第一阶段不建议直接配置异常阻断。初始策略应为“只预警、不阻断”，等规则稳定后再对少量核心链路启用阻断。
