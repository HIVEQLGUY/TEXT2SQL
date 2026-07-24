# Spec: API 接入生产级框架

## ADDED Requirements

### Requirement: 统一任务定义

所有生产 API 采集任务 SHALL 由框架任务定义描述，不得只依赖散落脚本参数。

#### Scenario: 注册新接口任务

WHEN 开发者为一个新 API 接口创建采集任务  
THEN 任务定义 MUST 包含任务编码、来源平台、接口方法、调度 cron、窗口字段、分页策略、限流策略、授权主体、目标 CONNECT/ODS 表、质量门禁和重跑策略。

#### Scenario: 禁止硬编码生产参数

WHEN 框架加载任务定义  
THEN 调度器账号、接口密钥、店铺 token、cron、窗口大小、并发数 MUST 从配置或环境变量读取，不得硬编码在业务脚本中。

### Requirement: 统一执行入口

DolphinScheduler SHALL 调用框架级执行入口，而不是直接绑定具体接口脚本。

#### Scenario: 每日自动采集

WHEN DolphinScheduler 定时触发 API 采集 workflow  
THEN workflow MUST 调用统一入口并传入任务编码、运行模式和窗口参数，框架 MUST 根据任务定义执行具体连接器。

#### Scenario: 手动重跑

WHEN 操作人在 DolphinScheduler 重跑 workflow 或使用框架重跑入口  
THEN 框架 MUST 重新执行对应任务窗口，并在运行状态表中生成新的运行记录。

### Requirement: 状态闭环

API 采集运行状态 SHALL 同时在 Doris 运行状态表和 DolphinScheduler 任务结果中可见。

#### Scenario: 全部成功

WHEN 所有店铺、窗口和页面采集成功并写入 Doris  
THEN 运行状态 MUST 记录为 `success`，DolphinScheduler task MUST 成功结束。

#### Scenario: 部分失败

WHEN 任一店铺、窗口或页面采集失败  
THEN 运行状态 MUST 记录为 `failed` 或 `partial_failed`，失败详情 MUST 写入 Doris，框架进程 MUST 以非零退出码结束，使 DolphinScheduler 显示失败。

### Requirement: Doris 层级边界

API 原始采集 SHALL 保留在 CONNECT/ODS，业务查询 MUST 使用 DWD 或更高层，不得直接把追加型 ODS 当作最终事实表。

#### Scenario: 增量回看产生重复 ODS 行

WHEN 每日增量按更新时间回看并重复采集同一订单  
THEN ODS MAY 保留多条源形态记录，DWD 当前态表 MUST 按业务主键去重。

#### Scenario: 订单业务口径查询

WHEN 用户查询每日订单数  
THEN 框架提供的 DWD/校验 SQL MUST 使用支付时间、排除未支付取消订单，并按店铺维度给出可复核结果。

### Requirement: 可重跑和幂等

API 采集任务 SHALL 支持窗口级重跑，并明确 CONNECT、ODS、DWD 三层幂等策略。

#### Scenario: 同窗口重跑

WHEN 使用相同任务编码、店铺、query_mode、窗口和页码重跑  
THEN CONNECT/ODS 写入 MUST 可识别重复 Doris label 或批次，并且 DWD 当前态结果 MUST 保持稳定。

#### Scenario: 不同窗口重复覆盖同一订单

WHEN 不同增量窗口返回同一订单  
THEN ODS MAY 追加证据记录，DWD MUST 保留最新有效版本。

### Requirement: 可扩展连接器接口

框架 SHALL 支持未来多个平台和接口接入，而不复制整套调度、状态和 Doris 写入代码。

#### Scenario: 接入第二个抖店接口

WHEN 新增另一个抖店接口  
THEN 开发者 MUST 只新增接口适配器、字段映射和任务定义，复用调度注册、运行状态、Doris 写入、质量门禁和 OPSE 评估。

#### Scenario: 接入其他平台 API

WHEN 新增非抖店平台 API  
THEN 框架 MUST 允许平台客户端和鉴权方式替换，同时复用统一运行状态、调度器注册和 Doris CONNECT/ODS 写入契约。

### Requirement: 生产质量门禁

每个生产 API 任务 SHALL 有自动质量校验。

#### Scenario: 行数异常

WHEN 采集结果低于任务定义中的最小行数规则或缺少授权主体  
THEN 框架 MUST 将运行标记为失败或需人工确认，并将原因写入状态表。

#### Scenario: OPSE 评估

WHEN 一个 API 任务被标记为生产可用  
THEN 必须存在 OPSE 评估记录，包含 Outcome、Process、Style、Efficiency 得分和验证证据。

## MODIFIED Requirements

### Requirement: `/order/searchList` 生产迁移

现有 `/order/searchList` 接入 MUST 迁移到统一 API 接入框架，并保留当前已采集数据。

#### Scenario: 保留历史数据

WHEN 迁移 `/order/searchList` 执行入口  
THEN 已有 CONNECT/ODS 表和数据 MUST 保留，不得清空或破坏。

#### Scenario: 当前调度升级

WHEN 发布新的 `/order/searchList` 生产 workflow  
THEN DolphinScheduler 中的每日任务 MUST 使用框架入口，且原专用注册脚本不得继续作为生产发布路径。
