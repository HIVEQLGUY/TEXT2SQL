# TEXT2SQL / Youmei 当前 Codex 规则

更新时间：2026-07-23

## 1. 当前方向

本项目后续不再推进旧的 Text2SQL、DataAgent、自研 API 接入层、Doris CONNECT/ODS、DataX-Web、旧 RDS 问数执行链路。

当前有效方向：

1. 数据接入未来通过“预策”作为统一接入层。
2. 数据进入 ClickHouse 后，在 ClickHouse 中做数仓可行性测试和后续建模验证。
3. 旧接口接入代码和经验只作为历史留存，不再作为当前实现基础。
4. Superset 和 DolphinScheduler 仍需保留，不能作为 Doris 附带项删除。
5. Doris 已按用户要求删除；后续不得恢复为默认建模或接入引擎，除非用户明确要求。

## 2. 上下文加载规则

本文件是项目级强规则文件，作为 always-on 操作规则，而不是项目状态日志。

当前状态读取入口：

- 当前项目方向：`TEXT2SQL-codex-handoff/docs/STATE-CURRENT.md`
- 当前资源访问状态：`TEXT2SQL-codex-handoff/docs/RESOURCE-资源登记.md`
- 信息边界：`TEXT2SQL-codex-handoff/docs/AGENT-CONTEXT.md`
- 长期原则：`TEXT2SQL-codex-handoff/docs/CONTEXT-长期前置上下文.md`

在任何实质项目任务、新会话开始、资源状态不确定、或用户询问“现在还能访问什么/当前状态”时，先读取上述入口。

不要把旧 handoff、checkpoint、历史聊天、旧 RDS、旧 DataAgent、旧 Doris、旧接口接入记录当作当前事实，除非当前状态文档或用户最新确认明确要求。

## 3. 新规范分类规则

当用户提出新的长期要求时，必须立即分类并更新对应文件：

- 强制 recurring 行为 -> 更新 `AGENTS.md`
- 长期协作/产品/工程原则 -> 更新 `CONTEXT-长期前置上下文.md`
- 当前状态/资源可达性 -> 更新 `STATE-CURRENT.md` 或 `RESOURCE-资源登记.md`
- 信息结构或过期/当前边界 -> 更新 `AGENT-CONTEXT.md`
- 业务规则/指标/表契约 -> 更新对应领域文档或 ClickHouse 建模材料

## 4. 资源状态维护规则

`RESOURCE-资源登记.md` 是当前唯一资源状态台账。

本地账号、密码、Token、Cookie、私钥等敏感凭据的统一入口是：

```text
C:\Users\24796\Documents\TEXT2SQL\local\credentials\
```

后续新增平台账号、数据库账号、API 凭据、浏览器登录说明、申请应用资质说明、登录校验结果，都必须围绕该目录和 `RESOURCE-资源登记.md` 维护：凭据正文放在 `local/credentials/`，资源状态和凭据位置写在 `RESOURCE-资源登记.md`。旧兼容文件 `.env`、`.env.reader`、`local/SECRETS-实际账号.md` 可以保留，但不得作为新的分散入口。

资源访问和登录校验的默认一键入口是：

```text
C:\Users\24796\Documents\TEXT2SQL\check-resource.cmd --list
C:\Users\24796\Documents\TEXT2SQL\check-resource.cmd --all
C:\Users\24796\Documents\TEXT2SQL\check-resource.cmd <资源别名>
```

资源别名、凭据文件、env 键、SSH 私钥、自动启动命令统一登记在 `local/credentials/resources.json`。后续会话不得再人工翻多个凭据文件猜测连接方式；除非用户明确要求看明文，否则只运行统一校验入口并汇报校验结果。

每一次资源查询都代表一次新的状态确认。查询后必须更新对应资源的：

- 最近确认时间
- 最近状态
- 确认方式
- 备注

如果资源已释放、下线或不再管理，应删除连接地址，不保留会误导后续 agent 的旧连接信息。

敏感信息不写入文档：密码、Token、Cookie、私钥正文、真实账号密钥只能留在本机安全位置。

## 5. 当前架构边界

未来默认链路：

```text
预策数据接入层 -> ClickHouse -> 数仓可行性测试/建模验证 -> 必要时 Superset/DolphinScheduler/OpenMetadata 辅助
```

不再作为未来方向推进：

- 旧 Text2SQL/RDS 问数链路
- DataAgent API 统一访问层
- 自研 API ingestion 写 Doris CONNECT/ODS
- Doris 作为默认数仓引擎
- DataX-Web 新增同步
- SeaTunnel 作为本项目默认接入路径

仍需保留：

- ClickHouse
- Superset
- DolphinScheduler
- OpenMetadata 是否继续使用由 ClickHouse 元数据测试需要决定
- 历史接口接入留存包，仅作参考

## 6. 生产级交付规则

所有代码和数据平台交付默认按生产级要求处理。不得把一次性脚本、手工命令、notebook 式探查、聊天说明当成完成实现。

生产级交付至少要求：

- 能被框架或平台重复执行
- 配置在源码之外
- 有测试或验证证据
- 有运行状态、失败暴露和回滚/重跑语义
- 不硬编码凭据
- 不依赖脆弱临时参数

接口接入历史只保存在桌面留存包中。若未来确需重新接入外部接口，优先确认预策是否支持；不在本项目内恢复旧自研 API ingestion 链路。

## 7. 交付汇报规则

汇报平台、接入、调度、资源、数仓或生产状态时，必须分清：

- 已完成
- 部分完成
- 未运行
- 失败
- 已下线
- 已释放
- 阻塞待确认

不能只说“成功/完成”。资源汇报必须包含最近确认时间和确认方式。

## 8. 文档维护规则

优先维护现有权威文件，不新增 handoff、checkpoint、memory、summary 这类平行入口。

当前保留入口：

- `AGENTS.md`
- `STATE-CURRENT.md`
- `RESOURCE-资源登记.md`
- `AGENT-CONTEXT.md`
- `CONTEXT-长期前置上下文.md`
- `RUNBOOK-组件启停与稳定性.md`
- `PROJECT-FILE-STRUCTURE-20260628.md`

过期、不重要、临时和历史误导性材料可以删除；有长期价值的内容应提炼进上述入口。

## 9. 建模确认规则

后续数仓建模默认使用 ClickHouse。

当缺少源数据、权威字段、业务逻辑、指标口径或粒度确认时，必须停在问题清单并询问用户，不得自造临时业务规则。

DWD 粒度必须服务业务分析。订单类源表默认保留订单粒度和商品明细/商品子单粒度等有业务意义的父实体粒度；金额明细项、优惠明细项、标签项、状态明细项等键值型/解释型数组，不能默认建成独立 DWD 事实表，必须值转列、按类型聚合或确定性汇总回订单或商品明细粒度。物流信息、履约包裹、快递单号、发货商品关系、退款、结算、费用等有独立业务过程和分析价值的数组，必须先验证与订单、商品子单、包裹/快递单号之间的关系基数，再决定独立事实表或桥接关系表；不得被解释型明细项规则强行归一到订单或商品粒度。粒度对齐和清洗契约重写阶段只能创建影子表/探查表并输出质量报告，不得直接创建、替换或切换正式 DWD；只有用户审阅影子结果并明确批准正式契约后，才能晋级正式 DWD。如果用户确认快递单号用于运费匹配、包裹ID无业务价值，则以快递单号为业务粒度，包裹ID不作为目标粒度字段；包裹ID粒度下的数值字段按快递单号汇总或按指标类型取平均。

旧 Doris 探查结果、旧接口 ODS、旧 DWS/ADS 结果表只能作为历史线索，不能直接作为当前 ClickHouse 建模结论。

DWS/ADS 结果表不能反向当作 DWD/DIM 上游来源，除非用户明确批准临时分析。

## 10. 中文业务命名规则

与用户沟通仓库模型、源发现、SQL 验证、数据契约、BI 数据集、平台资产时，默认先写中文业务名，再在括号里补物理名。

例如：

```text
商品编码(spbm)
ClickHouse 测试库(youmei_sandbox)
```

如果只有物理名，说明“中文名未知，暂用物理名”。

## 10.2 前端中文化规则

本项目自研前端默认使用中文界面。页面标题、导航、按钮、表单占位、提示、状态、错误、表格列头、空值和布尔值展示都必须合理中文化。

技术品牌、SQL 关键字、物理库名、物理表名、物理字段名、环境变量、命令和代码片段不强行翻译；展示业务数据时优先显示中文业务名或字段注释，并在需要追溯时用括号保留物理名。

现成第三方封闭前端（例如 CH-UI Docker 镜像）如果没有语言配置，不作为“已中文化”的交付口径；应明确说明边界，并优先提供项目自研中文前端作为默认工作入口。

## 10.1 业务字段保留规则

本项目业务数据清洗和建模不设置安全、保密、脱敏或敏感字段筛选规则。收件人、电话、地址、买家留言、加密业务标识等字段按普通业务字段处理；是否进入 DWD/DIM/DWS/ADS 只由业务语义、粒度、类型契约、质量结果和下游用途决定。

平台登录凭据不是业务数据，不进入清洗契约、SQL 或业务模型。

## 11. 平台和删除安全规则

删除或卸载任何服务、容器、镜像、目录、数据前，必须确认：

- 用户明确要求删除的对象
- 容器名/目录名/端口属于本项目
- 是否会误删保留组件

特别规则：

- Superset 保留。
- DolphinScheduler 保留。
- 删除 Doris 不等于删除 Superset 或 DolphinScheduler。
- 只有用户明确点名删除 Superset 或 DolphinScheduler 时才允许下线。

## 12. 当前技能路由

- ClickHouse SQL、表设计、建模验证 -> `clickhouse-sql-dev`
- 正式数仓发布、候选表切换、回滚、发布报告和 Git 留痕 -> 项目 `warehouse-release.cmd`
- 已批准影子表晋级正式 DWD -> 项目 `warehouse-promote.cmd`；不得再依赖聊天逐步寻找正式包或手工重跑阶段
- ODS 到 DWD 清洗、字段语义统一、JSON 展开、金额/枚举/质量契约 -> `data-warehouse-cleaning`
- 数仓建模、粒度、指标、维度 -> `data-warehouse-modeling`；其中 ODS 到 DWD 必须先经过 `data-warehouse-cleaning`
- 平台/端口/WSL/Docker/Superset/DolphinScheduler/OpenMetadata 状态 -> `dataagent-platform-ops` 或更贴近的新脚本
- 资源状态盘点 -> 更新 `RESOURCE-资源登记.md`
- 旧接口经验查询 -> 查看桌面 `youmei-api-ingestion-archive-20260719.zip`
- 可复用结论、策略变更、清理/迁移结果 -> `agent-eval` 记录 OPSE

旧 `api-doris-ingestion`、`doris-sql-dev`、`seatunnel-agent`、`datax-web-agent` 只用于历史理解，不作为未来默认执行路径。

## 13. Skill 治理与评估规则

可复用工作、策略切换、生产可用结论、资源清理、平台变更必须进行 OPSE 评估：

- Outcome：目标是否完成并有证据
- Process：路线、工具、顺序和门禁是否正确
- Style：文档和用户汇报是否符合规则
- Efficiency：是否避免重复劳动、绕路和资源浪费

如果评估暴露反复问题，应更新本文件、资源台账、runbook 或相关脚本，而不是只留在聊天里。

## 14. 历史接口留存

旧接口接入代码、SDK bridge、接口契约、调度/回补脚本、测试和隐性经验已留存在：

```text
C:\Users\24796\Desktop\youmei-api-ingestion-archive-20260719.zip
```

该包仅供历史参考。后续如果需要接接口，先走预策能力确认，不默认恢复本项目旧接入框架。

## 15. PowerShell / WSL 执行规则

当前 shell 是 PowerShell。避免在 PowerShell 中直接拼复杂 Bash heredoc、多层引号、多行 SQL 或带管道的复杂命令。

优先使用：

- 固定 `.ps1`
- 固定 `.sh`
- 固定 `.sql`
- 固定 Python 脚本

任何递归删除必须先校验路径在项目目录或明确目标目录内。

## 16. OpenMetadata 固定同步规则

后续凡是 ClickHouse 表结构、字段中文名、字段注释、业务口径、枚举、标签、粒度、血缘或清洗契约发生变更，不能只在聊天或临时命令里补写 OpenMetadata。

固定路径如下：

```text
发布文件 release*.yaml / corrective-release*.yaml
  -> openmetadata.contracts 中登记 metadata-contract-*.yaml
  -> 清理发布另登记 openmetadata.retire 退休表资产
  -> sync-openmetadata.cmd --release <发布文件名> --mode full
  -> plan -> apply -> verify
  -> openmetadata-sync-report-<发布文件名>.json
```

默认入口：

```text
C:\Users\24796\Documents\TEXT2SQL\sync-openmetadata.cmd
```

脚本会读取：

```text
C:\Users\24796\Documents\TEXT2SQL\local\credentials\openmetadata.env
```

后续建模和清洗交付必须把 OpenMetadata 同步视为发布门禁的一部分：没有发布文件、没有元数据契约或退休清单、没有回读校验报告，不得汇报为“元数据已完成”。探索期允许只执行 `--mode plan`，正式发布必须执行 `--mode full` 并保留报告。

## 17. 数仓显性发布与 Git 版本规则

数仓版本管理以 Git 为权威来源，ClickHouse 和 OpenMetadata 是发布结果，不是版本源头。

任何正式 SQL 变更不得以“手工执行 SQL”视为完成，必须显性创建发布动作。正式发布至少包含：

- 发布文件：`release*.yaml` 或 `corrective-release*.yaml`
- 变更 SQL：建表、写入、校验、切换、回滚或重建 SQL
- 清洗/建模契约：字段、粒度、主键、枚举、口径、质量门禁
- OpenMetadata 契约：`metadata-contract-*.yaml`
- 执行报告：ClickHouse 执行结果、质量门禁结果、OpenMetadata 回读校验结果
- Git 版本记录：提交本次发布涉及的 SQL、契约、元数据契约、报告和发布清单

正式发布的目标状态是：每一次 SQL 发布都会生成或切换到最新版本的生产表；历史口径、历史字段、历史枚举、历史 OpenMetadata 元数据契约和发布报告全部保存在 Git 中，用 Git 记录查询和回滚依据。

Git 远程同步必须由发布总控以非交互方式执行并设置有限超时；网络、凭据或超时失败统一记录为 `version_record_pending`，不得留下等待输入的后台推送进程，也不得以手工后台推送代替发布报告。恢复后必须继续使用同一发布包的 `finalize` 补记。

影子表只作为业务方与建模助手的交互验证产物。影子结果获批后，必须按同一清洗契约重新构建正式候选表、通过正式门禁并切换正式表，随后删除已晋级影子表；影子结果退回或被新版本替代时，也必须通过清理发布删除。清理发布使用 `release_type: cleanup`、`publish.strategy: cleanup_only`、`cleanup.objects` 和 `approval.cleanup_authorized: true`，不得手工执行删除 SQL。

不得依赖在 ClickHouse 或 OpenMetadata 中保留多张正式表来做版本管理。回滚默认依据 Git 中上一版可重建发布包重新执行并切换当前生产对象。

项目级一键发布总控入口为：

```text
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd
```

固定命令为：

```powershell
warehouse-release.cmd --release <发布YAML> --mode plan
warehouse-release.cmd --release <发布YAML> --mode verify
warehouse-release.cmd --release <发布YAML> --mode full
warehouse-release.cmd --release <发布YAML> --mode finalize
```

已批准影子表的正式晋级使用固定一键入口：

```powershell
C:\Users\24796\Documents\TEXT2SQL\warehouse-promote.cmd <影子发布YAML>
```

该入口只接受影子发布报告已为 `succeeded`/`finalized` 且指纹一致的结果，自动解析 `promotion.formal_release` 或唯一匹配的正式发布包，校验来源表、分区、粒度和主键后调用正式 `full` 发布。正式发布包仍必须通过 ClickHouse、OpenMetadata 和 Git 全部门禁；一键入口只是固化路由，不降低业务确认或生产质量门槛。Git 推送默认在发布进程内自动重试，并在必要时自动进入 `finalize`，不得要求 AI 或聊天继续接力。

发布总控已经固化以下门禁：发布指纹、同一 release_id 版本漂移、同一 SQL 多阶段复用、候选表与生产表重名、只读阶段出现 DDL/DML、构建阶段直写生产表、清理 SQL 未覆盖声明对象、OpenMetadata 契约重复指向同一表、Git 暂存区污染、重复发布幂等、并发发布锁、ClickHouse 阶段失败、切换后回滚、临时对象清理失败、Git 最终留痕失败和远程同步失败。

正式 `full` 发布必须使用 `candidate_swap`：先 Git 预提交发布包，再只写候选表，质量通过后切换唯一正式表，执行 OpenMetadata `plan -> apply -> verify`，最后清理候选/旧表临时对象并提交报告和标签；上述平台步骤成功后，发布总控必须自动推送 Git 远程分支和标签。`release_type: shadow` 的 `full` 发布同样必须自动同步；只有 `plan`/`verify` 只读阶段不触发推送。远程推送默认自动重试并在同一进程内自动补记 `finalize`；重试仍失败才标记 `version_record_pending`，不得汇报为完整发布成功。历史版本不在 ClickHouse 保留多张正式备份表，统一依据 Git 发布包重建。

清理 `full` 发布只允许执行 `preflight -> quality -> OpenMetadata plan -> cleanup -> postcheck -> OpenMetadata apply/verify 退休回读 -> Git 留痕`，不创建物理备份。OpenMetadata 只读计划未通过时不得删除 ClickHouse 对象；当前正式表必须在 `postcheck` 中确认仍存在，清理对象必须确认不存在；OpenMetadata 退休失败或 Git 远程同步失败时，发布报告必须明确标记未完成并支持重跑/补记。

自动同步使用发布包声明的 `git.remote`、`git.branch` 和标签，通过项目发布总控执行；不得依赖聊天后的手工推送。发布前只提交本次发布允许路径，不能把工作区其他未提交文件一并推送；发布后的远程同步必须是显性报告步骤并可由 `finalize` 重试。

旧结构 `execution.*` 发布文件只能通过 `plan/verify` 兼容读取，不得直接 `full`。具体发布包结构和冗余处理见 `docs/warehouse-release-process.md` 与 `config/warehouse-release-template.yaml`。
