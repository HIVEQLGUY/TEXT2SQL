# Skill 循环治理系统设计

## Context

当前 OPSE 标准已经存在于 `agent-eval`，但缺少 skill 使用前路由、使用后自评、场景数据集、工作空间投影和架构审计。新设计必须复用 `agent-eval`，不能新增一套评测体系。

## Goals

- 所有治理结果持久化到工作空间，避免依赖上下文记忆。
- 每个核心 skill 都有可回放的 eval 场景。
- 每次关键 skill 使用后都能调用统一 post-use 入口记录 OPSE。
- skill 迭代必须先给出建议，等待用户确认后再修改。

## Decisions

### Decision 1: `agent-eval` 是唯一评分标准

Choice: 所有场景评分最终写入 `local/evals/agent-evals.jsonl`，字段沿用 OPSE。  
Rationale: 避免出现临时 eval 和多套口径。  
Alternatives: 给每个 skill 独立建 JSONL，被拒绝，因为会破坏统一治理。

### Decision 2: 工作空间保留 governance 镜像

Choice: 在 `TEXT2SQL-codex-handoff/skill-governance/` 保存数据集、报告、skill 投影和运行记录。  
Rationale: 用户可见，且不依赖 Codex 上下文。  
Alternatives: 只保存在 `.codex/skills`，被拒绝，因为用户不容易直接审查。

### Decision 3: Hook 先实现为可执行协议

Choice: 通过 `scripts/skill_governance.py route` 和 `post-use` 作为前后 hook。  
Rationale: 当前没有可用的 Codex runtime hook；先建立稳定脚本入口，后续可接入插件层。  
Alternatives: 声称自动运行，被拒绝，因为不真实。

## Risks And Trade-Offs

- 脚本 hook 需要执行者遵守 AGENTS 规则；还不是真正内核自动触发。
- 场景数据集初版是治理基线，后续需要用真实用户反馈迭代。
- 投影 skill 文件可能滞后，需要定期运行投影命令刷新。
