# Skill 循环治理系统规格

## ADDED Requirements

### Requirement: 任务前 Skill 路由

系统 MUST 根据任务文本、项目路由规则和 skill 注册表输出候选 skill、必选 skill、执行顺序和是否需要 OPSE。

#### Scenario: API 接入任务

WHEN 任务文本包含 API、接口、Doris、CONNECT 或 ODS  
THEN 路由结果 MUST 包含 `api-doris-ingestion` 和 `agent-eval`。

#### Scenario: 数仓 DWD 任务

WHEN 任务文本包含 DWD、DIM、DWS、ADS、指标、口径或建模  
THEN 路由结果 MUST 先包含 `data-warehouse-modeling`，再包含 `doris-sql-dev`。

### Requirement: Skill 使用后自评

系统 MUST 支持在 skill 使用后记录 task_id、skill、场景、证据、问题和 OPSE 分数，并写入统一 JSONL。

#### Scenario: 使用后评分

WHEN 调用 post-use 记录  
THEN 系统 MUST 追加 `local/evals/agent-evals.jsonl` 和 `local/skill-governance/skill-runs.jsonl`。

### Requirement: Skill 专属测试场景集

每个数仓 agent 层核心 skill MUST 有自己的 eval 场景，且至少包含正常、边缘、故障三类。

#### Scenario: 场景完整性检查

WHEN 运行 skill 架构审计  
THEN 缺少正常、边缘或故障场景的 skill MUST 被标记为问题。

### Requirement: Skill 架构审计

系统 MUST 汇总 eval 记录、场景集和 changelog，输出每个 skill 的治理状态、低分原因和建议动作。

#### Scenario: 低分记录存在

WHEN 某 skill 最近 OPSE 低于 80  
THEN 审计报告 MUST 标记该 skill 需要优化，但不得自动修改 skill 内容。

### Requirement: 工作空间可见投影

系统 MUST 支持将本机 `.codex/skills` 的 SKILL.md、CHANGELOG.md 和 references 目录投影到项目工作空间。

#### Scenario: 投影 skill

WHEN 运行投影命令  
THEN 工作空间 MUST 出现 `skill-governance/skills/<skill-name>/`，供用户直接查看。
