# 新会话接续说明

## 1. 给新 Codex/API 的读取顺序

新会话接手后，请优先阅读以下文件：

1. `docs/NEXT-AI-切换API接续包.md`
2. `docs/CHECKPOINT-项目检查点.md`
3. `docs/RESOURCE-资源登记.md`
4. `docs/MEMORY-重要信息记录规范.md`
5. `docs/CHAT-沟通记录摘要.md`
6. `docs/PRD-智能问数项目概览.md`
7. `docs/ARCH-智能问数系统架构草案.md`
8. `docs/READING-教程阅读路线.md`
9. `docs/PLAN-第一阶段落地方案.md`
10. `docs/CHECKLIST-资源与权限确认.md`

这些文件包含本项目目前的上下文、教程阅读结论、业务差异、架构方向、第一阶段计划和资源需求。

`docs/NEXT-AI-切换API接续包.md` 是唯一固定接续包。后续开发只覆盖更新该文件，不创建多份会话归档，避免多头信息源。

如需登录服务器、连接数据库或调用外部服务，再读取本地文件：

```text
local/SECRETS-实际账号.md
.env
.env.admin
.env.reader
```

`local/` 和 `.env*` 不提交到 Git，用于保存真实账号密码。Git 中只保存资源索引和凭证位置。

## 2. 当前项目定位

本项目要搭建一个真实业务可用的智能问数系统，不是复刻教程里的电商 demo。

第一阶段目标：

- 跑通抖音主题域真实数据和元数据。
- 元数据入口使用钉钉 AI 表格，但钉钉到元数据库的定期写入已由用户自己的工具完成。
- 本项目当前不重复实现钉钉同步链路，优先读取和适配已写入元数据库的元数据。
- 用户自然语言问题经过元数据召回、上下文构建、SQL 生成、安全校验、执行和结果返回。

用户代码经验较弱，因此 Codex 需要主动承担工程判断，包括架构、配置、权限、安全、可维护性和实施步骤。

## 3. 已完成工作

已完成：

- 预读教程电商问数主线章节。
- 提炼教程中可复用的工程思想。
- 明确本项目和教程 demo 的差异。
- 建立项目 PRD、架构草案、阅读路线和第一阶段落地方案。
- 将旧测试原型归档到 `legacy/prototype-20260523/`。
- 当前正式代码目录尚未重新搭建，后续可从干净的 `app/` 结构开始。

旧原型只作参考，不应在其基础上继续堆正式功能。

## 4. 关键决策

架构方向：

- 后端：FastAPI。
- 流式协议：SSE。
- 工作流：保留 LangGraph 或至少保持同等节点化结构。
- 元数据入口：钉钉 AI 表格由用户已有工具写入元数据库。
- 运行元数据：项目自己的元数据库。
- 检索：字段语义检索 + 字段值检索 + 字段依赖/计算公式上下文。
- SQL：生成后必须经过安全审查、语法校验、风险校验，再执行。
- 日志：从第一阶段引入 `request_id`、`run_id`、`step_id`。

资源原则：

- 不为了省本地资源做临时架构。
- 可以使用云服务器和数据库管理员权限搭建长期架构。
- 应用运行仍应遵守最小权限原则，问数执行默认使用只读账号。

元数据原则：

- 产品概念上不强制区分指标和字段。
- 指标可视为带计算公式、业务口径和依赖关系的特殊字段元数据。
- 表元数据和字段元数据由钉钉 AI 表格协作维护，系统同步到元数据库。

## 5. 仓库状态

远程仓库：

`https://github.com/HIVEQLGUY/TEXT2SQL.git`

当前分支：

`codex/bootstrap-foundation`

最近关键提交：

`8a619c5 Document first-phase text2sql plan`

该提交已包含当前文档和旧原型归档。

## 6. 目录说明

当前重点目录：

- `docs/`：项目规划、架构、阅读路线、沟通摘要和资源清单。
- `local/`：本机真实账号密码和敏感信息，已被 `.gitignore` 忽略，不提交。
- `legacy/prototype-20260523/`：旧测试原型归档。
- `config/`：已有配置模板。

正式代码目录 `app/`、`web/`、`agent/`、`scripts/` 已从根目录移入 `legacy/`，后续正式实现可以重新创建。

## 7. 下一步建议

下一步不要直接写功能代码，应先完成新服务器和新 RDS 的连通性确认。

当前已提供的新资源见 `docs/RESOURCE-资源登记.md`：

- 云服务器公网 IP：`114.55.148.140`
- SSH 用户：`root`
- SSH 登录方式：Codex 本地生成 v2 公钥，用户已配置到阿里云实例，测试成功。
- SSH 私钥路径：`local/ssh/text2sql_codex_ed25519_v2`
- 元数据库：旧阿里云 RDS MySQL，`youmei_ai`，服务器端使用 `baoyan` 已连接成功。
- 问数执行数据库：新阿里云 RDS MySQL，`chatsql_ai`，服务器端和本地 API 均已连接成功。
- 真实密码记录在本地 `local/SECRETS-实际账号.md`，不要提交 Git。
- 本地 `.env` 应保持 `META_DB_*` 指向旧 RDS，`DW_DB_*` 指向新 RDS；`.env.reader` 指向新 RDS。
- M1 工程骨架已启动并通过本地 API/RDS 健康检查，详见 `docs/CHECKPOINT-项目检查点.md`。
- 本地 API 地址：`http://127.0.0.1:8000`。
- `GET /api/health/db` 已验证：`metadata_db=youmei_ai/baoyan@%`，`warehouse_db=chatsql_ai/chat_ai_duckdb_2@%`。

下一步动作：

1. 复测本地 `.env` 调整后 `GET /api/health/db` 是否元数据库和问数执行数据库都通过。
2. 进入 M2：读取旧 RDS `youmei_ai` 中现有元数据表结构，做字段映射和 Repository。
3. 原 M3 钉钉同步不再作为项目内任务；后续改做元数据库到 ES/OpenSearch/向量库的索引刷新。
4. 当前测试阶段新 RDS 暂不强制只读账号，后续健壮性阶段再收敛权限。
5. M2 第一优先级已完成：用户调整表结构后，已确认 `metric_dictionary.ssscb = table_dictionary.bbs` 是真实主关联键。
6. M2 初版只读 API 已新增并验证：`GET /api/metadata/summary`、`GET /api/metadata/tables`、`GET /api/metadata/fields`、`GET /api/metadata/tables/{table_id}/fields`。
7. M2 元数据召回服务初版已新增并验证：`GET /api/metadata/retrieve?question=...`。
8. M2 问数上下文构建服务初版已新增并验证：`GET /api/metadata/context?question=...`，输出 `tables`、`candidate_fields`、`prompt_context`、`warnings`。
9. 用户确认最终服务部署在阿里云云服务器上，本地直连 RDS 慢不作为当前架构阻塞；后续上云后复测真实延迟。
10. 下一步进入 SQL 生成前工作流节点设计，并在用户更新元数据表名后确认元数据库表名与问数执行库物理表名的映射策略。

连通性确认后，从 `docs/PLAN-第一阶段落地方案.md` 的 M1 开始：

1. 建立 FastAPI 后端结构。
2. 建立配置加载和环境变量模板。
3. 建立 request_id 日志。
4. 保留旧原型作为参考，不直接复用其目录结构。

## 8. 注意事项

- 不要提交 `.env`、`.env.admin`、`.env.reader` 或任何真实密钥。
- 真实账号密码固定记录在 `local/SECRETS-实际账号.md` 或 `.env.*`，不要只留在聊天记录里。
- Git 中的资源状态固定更新 `docs/RESOURCE-资源登记.md`，阶段结论固定更新 `docs/CHECKPOINT-项目检查点.md`。
- 后续开发途中确认的重要信息默认更新固定记录文件，不要为每次对话新建零散记录文件。
- 超级管理员账号只能用于初始化、建库、授权、排障和迁移。
- 问数执行 SQL 必须使用只读账号。
- 不要把教程里的电商教学表当作实际业务模型。
- 不要把旧原型恢复到根目录继续开发。
- 用户希望 Codex 从系统工程角度主动提建议，而不是只按教程逐步实现。
