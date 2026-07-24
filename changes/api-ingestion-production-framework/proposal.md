# API 接入生产级框架改造

## Why

当前抖店 `/order/searchList` 已经证明单接口可以通过代码连接器写入 Doris CONNECT/ODS，并由 DolphinScheduler 定时触发。但现状仍存在生产化缺口：调度器只执行一个 shell 命令，无法完整感知接口采集内部状态；后续新接口不会自动形成统一注册、运行、重跑、失败门禁和质量校验；ODS 追加表容易被误用为业务事实表；部分凭据、调度器账号、窗口参数仍分散在脚本和环境中。继续以这种方式扩展接口，会把每个接口做成孤立工程，后续维护、重跑、告警和口径治理都会失控。

本变更要把 API 接入从“单接口脚本能跑”升级为“生产级框架能力”：未来所有外部 API、RPA、Yingdao 或文件采集任务都必须通过统一任务定义、统一执行服务、统一 Doris CONNECT/ODS/DWD 流转、统一 DolphinScheduler 注册、统一运行状态和质量门禁。

## What Changes

- 新增框架级 API 接入任务定义，描述接口、平台、调度、窗口、分页、限流、目标表、质量门禁和重跑策略。
- 新增框架级运行状态表，记录每次采集运行、店铺/账号、窗口、页数、行数、失败页、异常、Doris label 和调度器实例信息。
- 新增统一执行入口，后续 DolphinScheduler 只调用框架入口和任务编码，不直接绑定具体接口脚本参数。
- 将 `/order/searchList` 迁移为首个框架任务，保留现有 CONNECT/ODS 数据，同时新增业务可用的 DWD 当前态表。
- 改造调度器注册逻辑：由配置化任务定义生成或更新 DolphinScheduler workflow，禁止硬编码账号密码，禁止无差别删除重建。
- 增加质量门禁：任何失败页、店铺缺跑、Doris 写入异常、关键行数异常必须让框架运行状态和 DolphinScheduler 结果同时可见。
- 增加重跑能力：支持按任务、店铺、时间窗口、query_mode 重跑，且重跑行为具有可解释的幂等策略。

## Scope

### In Scope

- API 接入框架层设计与首批实现。
- `/order/searchList` 迁移到框架运行方式。
- Doris 生产运行元数据表和 DWD 订单当前态表。
- DolphinScheduler 注册和重跑入口生产化。
- 配置去硬编码：调度器账号、任务参数、接口窗口、调度 cron、店铺列表进入配置或环境变量。
- 质量门禁与失败状态传播。
- 单元测试、集成测试、Doris 校验 SQL、OPSE 评估。

### Out of Scope

- 不在本变更中接入新的业务接口。
- 不在本变更中重建完整抖音 DWS/ADS 宽表。
- 不引入 MySQL 作为 API JSON 中转层。
- 不把 DolphinScheduler 替换为其他调度器。
- 不把所有历史 SeaTunnel/DataX 任务迁移到 API 框架。

## Impact

- 代码：`app/services`、`app/repositories`、`app/clients`、`app/core/config.py`、`app/api/routers/integration.py`。
- Doris：新增 API 运行状态表、任务配置可见表或本地配置映射、DWD 订单当前态表。
- 调度器：现有 `ODS_抖店订单列表接口采集__0715` workflow 将由框架注册逻辑管理。
- 测试：新增框架级单元测试、调度器注册测试、Doris 质量门禁测试。
- 文档：更新当前状态、资源登记、合同或运行手册。

## Capabilities

### New Capabilities

- 配置化 API 任务注册。
- 统一 API 任务执行器。
- 统一采集运行状态和失败门禁。
- DolphinScheduler workflow 生产级发布和重跑入口。
- DWD 当前态去重表。

### Modified Capabilities

- `/order/searchList` 从接口专用脚本迁移为框架任务。
- DolphinScheduler 注册从硬编码脚本转向配置化发布。
- ODS 从可查询数据源明确降级为源形态证据层，业务查询走 DWD/DWS。
