# Skill 循环治理系统

## Why

当前 skill 使用、评估、迭代和文档管理依赖规则与人工执行，缺少统一的可见工作空间、路由证据、使用后自评、skill 专属测试场景集，以及架构级审计。这样容易受到 Codex 上下文压缩、记忆遗漏、临时判断和单点修补影响。

## What Changes

- 建立工作空间可见的 skill 治理目录，集中保存 skill 投影、测试数据集、运行记录和治理报告。
- 增加统一 CLI，支持任务前 skill 路由、skill 使用后记录、skill 场景评估、skill 架构审计和 skill 投影。
- 为数仓 agent 层的每个核心 skill 建立专属 eval 场景数据集，覆盖正常、边缘、故障场景。
- 将 OPSE 四维作为统一评分纲领，场景按 skill 能力拆解生成，不再新增临时评测体系。
- 更新项目规则，要求生产流程在关键 skill 使用后执行 post-use eval，并把结果反馈给用户，用户确认后再迭代 skill。

## Scope

### In Scope

- `agent-eval` 作为唯一 OPSE 记录标准。
- 本项目工作空间中的 skill governance 可见资产。
- 数仓 agent 层核心 skill 的路由配置和 eval 场景集。
- 任务前路由、任务后记录、场景评估、架构审计的 CLI。
- 项目规则和长期原则更新。

### Out of Scope

- 不修改 Codex 产品内核。
- 不声称已经实现真正 runtime 自动 hook。
- 不替换 spec-superflow、数仓建模、Doris、接入、平台等领域 skill。

## Impact

- 新增 `TEXT2SQL-codex-handoff/app/services/skill_governance/`。
- 新增 `TEXT2SQL-codex-handoff/scripts/skill_governance.py`。
- 新增 `TEXT2SQL-codex-handoff/config/skill-governance.registry.json`。
- 新增 `TEXT2SQL-codex-handoff/skill-governance/` 可见工作区。
- 更新 `AGENTS.md` 和长期上下文。

## Capabilities

### New Capabilities

- skill 路由决策持久化。
- skill 使用后 OPSE 自评记录。
- 每个 skill 的正常/边缘/故障场景数据集。
- skill 架构审计，识别反复低分、缺少场景、缺少版本记录等问题。
- 将 `C:\Users\24796\.codex\skills` 投影到项目工作空间，便于查看。

### Modified Capabilities

- `agent-eval` 继续作为唯一 OPSE 标准，但增加使用约定和治理脚本入口。
