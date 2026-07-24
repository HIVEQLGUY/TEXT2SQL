# Skill 循环治理系统任务

## File Structure

- Create: `TEXT2SQL-codex-handoff/app/services/skill_governance/models.py` — 定义 skill 注册、场景、路由、运行记录和审计模型。
- Create: `TEXT2SQL-codex-handoff/app/services/skill_governance/router.py` — 根据任务文本和注册表生成 skill 路由决策。
- Create: `TEXT2SQL-codex-handoff/app/services/skill_governance/evaluator.py` — 读取场景集和 OPSE 记录，生成场景评估和架构审计。
- Create: `TEXT2SQL-codex-handoff/app/services/skill_governance/workspace.py` — 投影 `.codex/skills` 到工作空间可见目录。
- Create: `TEXT2SQL-codex-handoff/scripts/skill_governance.py` — CLI 入口，提供 route、post-use、evaluate-skill、audit、project-skills。
- Create: `TEXT2SQL-codex-handoff/config/skill-governance.registry.json` — 数仓 agent 层 skill 路由注册表。
- Create: `TEXT2SQL-codex-handoff/skill-governance/datasets/warehouse-agent-skill-evals.json` — 每个核心 skill 的正常/边缘/故障测试场景。
- Create: `TEXT2SQL-codex-handoff/tests/test_skill_governance.py` — 覆盖路由、场景完整性、post-use、审计和投影行为。
- Modify: `AGENTS.md` — 强制关键 skill 使用前后走治理 hook。
- Modify: `TEXT2SQL-codex-handoff/docs/CONTEXT-长期前置上下文.md` — 记录跨项目 skill 循环治理原则。

## Interfaces

### Batch 1 → Batch 2

- **Produces**: `SkillGovernanceRegistry`、`SkillEvalDataset` — 供路由和评估服务使用。

### Batch 2 → Batch 3

- **Produces**: `route_task()`、`record_skill_use()`、`audit_skill_architecture()` — 供 CLI 和测试使用。

## Batch 1: 数据模型和测试

Depends on: none

1.1 Create `tests/test_skill_governance.py`。
- RED: 写测试要求 API 任务路由到 `api-doris-ingestion` 和 `agent-eval`。
- GREEN: 创建模型和路由服务。

1.2 Create `skill-governance/datasets/warehouse-agent-skill-evals.json`。
- RED: 写测试要求每个注册 skill 至少有 normal、edge、failure 三类场景。
- GREEN: 创建数据集。

## Batch 2: CLI 和持久化

Depends on: Batch 1

2.1 Create `scripts/skill_governance.py`。
- RED: 写测试调用 post-use 后同时写入 skill-runs 和 agent-evals。
- GREEN: 实现 CLI 和服务。

2.2 Create workspace projection。
- RED: 写测试要求投影后存在 skill 的 SKILL.md。
- GREEN: 实现投影服务。

## Batch 3: 规则和验证

Depends on: Batch 2

3.1 Modify `AGENTS.md` 和长期上下文。
- RED: 检查缺少 skill hook 规则。
- GREEN: 写入中文规则。

3.2 Run full tests and record OPSE。
- 运行全量 pytest。
- 用 `agent-eval` 记录本次 skill 循环系统升级。
