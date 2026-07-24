# Skill 循环治理系统执行契约

## Intent Lock

建立一个跨项目、工作空间可见、基于 `agent-eval` OPSE 的 skill 路由、使用后自评、测试场景和架构审计循环系统。

## Scope Fence

In scope:
- 新增 skill-governance 服务、CLI、注册表、场景数据集和工作空间投影。
- 更新项目规则，要求关键 skill 前后 hook。
- 用 `agent-eval` 记录本次治理系统升级。

Out of scope:
- 修改 Codex 内核。
- 声称 runtime hook 已自动触发。
- 自动修改任何 skill 内容；优化建议必须等待用户确认。

## Build Rules

- 所有新增规则和说明必须中文。
- 评估记录必须进入 `local/evals/agent-evals.jsonl`。
- 不新增临时评测文档。
- 测试先行，至少覆盖路由、场景完整性、post-use 持久化和投影。

## Test Obligations

- API 任务路由包含 `api-doris-ingestion` 和 `agent-eval`。
- DWD 任务路由顺序包含 `data-warehouse-modeling` 后接 `doris-sql-dev`。
- 每个核心 skill 都有 normal、edge、failure 场景。
- post-use 同时写入 `skill-runs.jsonl` 和 OPSE eval JSONL。
- project-skills 能把 skill 文件投影到工作空间。

## Approval

用户已要求“继续按照新范式升级这个 skill 循环系统”，本轮按该批准执行。
