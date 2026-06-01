# 重要信息记录规范

本项目不依赖聊天记录保存关键上下文。后续 Codex 在开发过程中发现、确认或改变重要信息时，默认更新固定记录文件。

## 1. 固定记录文件

| 信息类型 | 固定位置 | 是否提交 Git |
| --- | --- | --- |
| 切换 API 时给下一个 AI 的完整接续包 | `docs/NEXT-AI-切换API接续包.md` | 是 |
| 新会话入口、读取顺序、下一步 | `docs/HANDOFF-新会话接续说明.md` | 是 |
| 长期沟通摘要和项目共识 | `docs/CHAT-沟通记录摘要.md` | 是 |
| 资源索引、账号用途、密钥位置 | `docs/RESOURCE-资源登记.md` | 是 |
| 阶段检查点、关键决策、测试结论 | `docs/CHECKPOINT-项目检查点.md` | 是 |
| 真实密码、Token、私钥路径或正文 | `local/SECRETS-实际账号.md` | 否 |
| 环境变量格式样例 | `.env.example` 或 `config/*.example.env` | 是 |
| 本机真实环境变量 | `.env`, `.env.admin`, `.env.reader`, `.env.*` | 否 |

## 2. 默认要记录的重要信息

Codex 在后续工作中遇到以下信息，应主动更新对应固定文件：

- 新服务器、新数据库、新数据源、新钉钉应用、新模型服务。
- 账号权限变化，例如创建只读账号、应用账号、同步账号。
- 安全边界变化，例如开放端口、白名单、只读限制、敏感字段限制。
- 架构决策变化，例如 MySQL 改 PostgreSQL、Qdrant 改 pgvector。
- 部署方式变化，例如本地开发、云服务器 Docker Compose、HTTPS 域名。
- 关键测试结论，例如 SSH 登录成功、数据库连接成功、钉钉接口可读。
- 阶段里程碑完成，例如 M1 工程骨架、M2 元数据库适配、M3 元数据索引刷新。
- 重要风险和阻塞，例如账号缺失、网络不通、权限不足、密钥失效。

## 3. 记录规则

- 不新建“本次对话记录”“会话总结 2”这类临时文件，除非用户明确要求。
- `docs/NEXT-AI-切换API接续包.md` 是唯一切换 API 接续包，后续只覆盖更新这个文件，不新建同类副本。
- 真实密钥只写入 `local/SECRETS-实际账号.md` 或 `.env.*`。
- Git 文档中可以写账号名、资源名、host、port、库名、用途和脱敏标识，但不写真实密码。
- 每次完成资源测试或阶段任务后，在 `docs/CHECKPOINT-项目检查点.md` 追加一条检查点。
- 每次完成关键开发进展、资源变更或下一步计划变化后，同步覆盖更新 `docs/NEXT-AI-切换API接续包.md`。
- 每次改变新会话读取顺序或下一步动作后，同步更新 `docs/HANDOFF-新会话接续说明.md`。
- 每次确认新资源后，同步更新 `docs/RESOURCE-资源登记.md`。

## 4. 新会话恢复流程

新会话按以下顺序恢复：

1. `docs/NEXT-AI-切换API接续包.md`
2. `docs/HANDOFF-新会话接续说明.md`
3. `docs/CHECKPOINT-项目检查点.md`
4. `docs/RESOURCE-资源登记.md`
5. `docs/CHAT-沟通记录摘要.md`
6. `docs/PRD-智能问数项目概览.md`
7. `docs/ARCH-智能问数系统架构草案.md`
8. `docs/PLAN-第一阶段落地方案.md`
9. 如需登录或连接，再读取本地 `local/SECRETS-实际账号.md` 和 `.env.*`

## 5. 切换 API / 新 Codex 的恢复方法

如果后续切换 API、模型或新会话导致聊天历史不可见，按以下方法恢复项目上下文：

1. 克隆或进入仓库 `https://github.com/HIVEQLGUY/TEXT2SQL.git`。
2. 切到分支 `codex/bootstrap-foundation`。
3. 先读 `docs/NEXT-AI-切换API接续包.md`。
4. 再读 `docs/HANDOFF-新会话接续说明.md`。
5. 再读 `docs/CHECKPOINT-项目检查点.md`，确认最新资源、风险和下一步。
6. 再读 `docs/RESOURCE-资源登记.md`，确认服务器、RDS、钉钉、大模型等资源索引。
7. 需要真实登录或连接时，读取本机 `local/SECRETS-实际账号.md` 和 `.env.*`。
8. 如 `local/` 不存在，说明真实密钥未随 Git 同步，需要用户重新提供或从本机备份恢复。
9. 恢复后若发现资源、密钥、测试结论变化，必须立即更新固定文件，不要只写在聊天里。

当前 SSH 注意事项：

- 云服务器 `114.55.148.140` 使用 v2 key。
- 当前私钥路径：`local/ssh/text2sql_codex_ed25519_v2`。
- 第一版 key 已作废，不应继续使用。
