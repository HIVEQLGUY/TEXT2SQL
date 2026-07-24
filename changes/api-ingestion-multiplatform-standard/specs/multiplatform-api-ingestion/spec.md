# 多平台 API 接入标准化规格

## ADDED Requirements

### Requirement: 平台 connector 标准接口

系统 MUST 提供平台无关的 connector 抽象，使新平台只需要实现平台客户端、接口 adapter 和主体解析，不需要重写 Runner、调度和 Doris 状态流转。

#### Scenario: 注册新平台接口

WHEN 新接口提供 `platform_code`、`connector_type`、`endpoint_key` 和 adapter 工厂  
THEN registry MUST 能创建对应 connector 并交给统一 Runner 执行。

#### Scenario: 未注册接口

WHEN 任务引用未注册的 `connector_type`  
THEN Runner MUST 返回明确错误，不得静默跳过或 fallback 到其他平台。

### Requirement: 接口接入契约

系统 MUST 提供接口接入契约模板，覆盖鉴权、分页、限流、增量字段、主键、CONNECT/ODS 表、调度、回灌和故障处理。

#### Scenario: 新平台接入前

WHEN 新平台接口准备开发  
THEN 必须先填写接口接入契约，且契约中 MUST 声明 CONNECT/ODS 表名和质量门禁。

#### Scenario: 缺少 ODS 证据

WHEN 接口契约缺少 ODS 表或主键字段  
THEN 该接口 MUST 不能进入 DWD/DIM/DWS/ADS 建模任务。

### Requirement: CONNECT/ODS 标准审计字段

系统 MUST 为 API 接入任务定义标准审计字段要求，包括平台、接口、主体、批次、请求、分页、游标、采集时间、源更新时间、schema 版本和 connector 版本。

#### Scenario: 任务定义加载

WHEN 加载 API 接入任务配置  
THEN 任务定义 MUST 校验平台编码、主体类型、主键字段、增量字段、目标表和审计字段配置。

### Requirement: 调度命令标准化

系统 MUST 使用平台无关的调度命令生成器创建 DolphinScheduler rawScript。

#### Scenario: 生成每日任务命令

WHEN 任务定义含有 `task_code` 和 `schedule_cron`  
THEN rawScript MUST 调用 `scripts/api_ingestion.py run --task-code <task_code>`，不得调用平台专用脚本。

### Requirement: 质量门禁标准化

系统 MUST 对每次 API 接入运行应用统一质量门禁。

#### Scenario: 页失败

WHEN 失败页数超过 `max_failed_pages`  
THEN 运行结果 MUST 是非零退出，并且不得刷新下游 DWD 当前态。

#### Scenario: 主体缺跑

WHEN `require_all_subjects` 为真且某个授权主体没有成功页面  
THEN 运行结果 MUST 是质量失败。

#### Scenario: ODS 主键重复

WHEN 质量门禁收到主键重复证据  
THEN 运行结果 MUST 是质量失败，并在运行状态中记录失败原因。

### Requirement: 抖店样例兼容

系统 MUST 保持现有抖店订单任务编码、调度命令和 Doris 表名兼容。

#### Scenario: 抖店订单任务加载

WHEN 加载示例任务配置  
THEN `douyin_order_searchlist_daily` MUST 仍指向 `/order/searchList`、CONNECT 表和 ODS 表。

#### Scenario: 抖店订单 Runner 执行

WHEN Runner 执行 `douyin_order_searchlist_daily`  
THEN 它 MUST 仍使用现有抖店订单采集逻辑，并返回页面级 CONNECT/ODS 证据。
