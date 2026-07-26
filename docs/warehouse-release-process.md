# ClickHouse 数仓显性发布流程

本项目的版本源是 Git，ClickHouse 和 OpenMetadata 是发布结果。任何正式 SQL、字段、粒度、枚举、清洗契约或血缘变化，都必须生成一个发布 YAML，并通过项目发布入口执行；手工执行 SQL 不算完成发布。

## 一条固定路径

```text
发布 YAML
  -> 版本包校验与指纹
  -> Git 工作区和工具预检
  -> Git 预提交（记录待发布版本）
  -> ClickHouse 健康检查
  -> preflight（只读）
  -> build（只写候选表）
  -> quality（阻断门禁）
  -> swap（候选表切换为唯一正式表）
  -> postcheck（切换后门禁）
  -> OpenMetadata plan/apply/verify
  -> cleanup（删除临时候选表和旧表名）
  -> Git 发布报告提交与版本标签
  -> Git 远程推送（分支与标签）
```

正式发布必须使用候选表切换策略。候选表、旧表临时名和回滚对象只在发布期间存在；成功后不在 ClickHouse 保留 `backup_版本号` 形式的正式历史表。历史版本依赖 Git 中的 SQL、契约、元数据契约和报告按原规则重建。

影子表是业务方与建模助手交互期间的验证产物，不是第二套长期生产表。影子生命周期固定为：

```text
契约确认 -> 影子发布 -> 业务审阅
  -> 批准：正式发布候选表切换 -> OpenMetadata 更新 -> 删除影子表
  -> 退回/过期：清理发布 -> 删除影子表
```

影子晋级必须重新按正式契约构建正式候选表并切换，不直接把影子表改名为正式表，避免绕过正式质量和元数据门禁。影子发布成功后只保留当前待审阅影子表；已晋级或已被新版本替代的影子表必须通过清理发布删除。历史备份表不作为回滚机制，回滚统一从 Git 发布包重建。

对于已确认废弃的影子表、验证表和历史备份表，使用 `release_type: cleanup` 的清理发布：

```text
清理发布 YAML
  -> Git 预提交
  -> ClickHouse preflight / quality
  -> OpenMetadata plan（只读，未通过则不删除 ClickHouse 对象）
  -> DROP 已授权废弃对象
  -> postcheck
  -> OpenMetadata apply / verify（退休并回读）
  -> Git 报告、标签和远程推送
```

入口：

```powershell
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd --release <发布YAML> --mode plan
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd --release <发布YAML> --mode verify
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd --release <发布YAML> --mode full
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd --release <发布YAML> --mode finalize
```

## 影子晋级一键入口

影子表完成业务审阅并且影子发布报告为 `succeeded` 或 `finalized` 后，不再需要 AI 重新寻找正式 SQL、核对字段或逐步执行命令。影子发布 YAML 在 `promotion.formal_release` 中登记预先固化的正式发布 YAML，然后直接运行：

```powershell
C:\Users\24796\Documents\TEXT2SQL\warehouse-promote.cmd <影子发布YAML>
```

该入口自动完成：影子报告和发布指纹校验、正式发布包定位、来源表/分区/粒度/主键一致性校验、正式 `full` 发布、ClickHouse 候选切换与质量门禁、OpenMetadata `plan -> apply -> verify`、影子清理、Git 提交/标签/远程同步。正式发布包已存在但影子包尚未补充 `promotion.formal_release` 时，只有目录内存在唯一匹配的正式发布包才允许自动发现；发现多个候选或无法匹配时直接阻断，避免静默选错版本。

正式平台步骤完成后，Git 推送由发布器在同一进程内按配置自动重试；仍失败时自动进入 `finalize` 补记路径，网络恢复时再次重试，不需要用户继续和 AI 往返。失败仍会留下 `version_record_pending` 报告，不能伪造完成状态。

`plan` 只校验文件、版本指纹、阶段顺序和门禁，并执行 Git 工作树/暂存区只读预检，不写 ClickHouse、OpenMetadata 或 Git。发布器会自动补齐随附 Git 运行时的 HTTPS、receive-pack 等辅助程序路径，不要求调用方手工设置环境变量。`verify` 执行健康检查和只读前置 SQL；正式发布检查目标表和元数据，清理发布检查待清理对象并执行 OpenMetadata 退休计划。`full` 才是正式发布动作，成功收尾后自动提交并推送 Git 分支和标签。`finalize` 用于平台已经完成但 Git 最终提交、标签或远程同步遇到临时故障后的显式补记，不会重新执行数据写入。

## 发布包最小要求

发布文件必须声明：

- `release_id`、`version`、`release_type`、`environment`、`status`。
- `source.database` 和不可为空的输入分区列表。
- 每张目标表的中文业务名、物理名、粒度、主键、唯一候选表名和临时旧表名。
- 正式/影子发布使用 `publish.strategy: candidate_swap` 与七个阶段 SQL：`preflight`、`build`、`quality`、`swap`、`postcheck`、`rollback`、`cleanup`。
- 清理发布使用 `publish.strategy: cleanup_only`、`cleanup.objects` 和四个阶段 SQL：`preflight`、`quality`、`cleanup`、`postcheck`。
- `approval.status: approved`；正式发布必须有 `approval.formal_publish_authorized: true`，影子发布必须有 `approval.shadow_publish_authorized: true`，清理发布必须有 `approval.cleanup_authorized: true`。
- 正式/影子发布登记 `openmetadata.contracts`；清理发布登记保留表契约和 `openmetadata.retire`，由固定同步入口执行 `plan -> apply -> verify`。
- `git.required: true`、`git.auto_commit: true`、`git.auto_push: true`、`git.remote`、`git.branch` 和发布标签；`full`、`rollback`、`finalize` 均不得关闭远程同步，`plan`/`verify` 只读阶段不触发推送。

`build` 只能创建并写入候选表；`swap` 负责原子切换；`cleanup` 不得删除当前正式表；`rollback` 必须能把切换前对象恢复为正式对象。只读阶段如果出现 DDL/DML 关键字会直接阻断。`release_type: shadow` 可在测试库执行同样的候选切换和 OpenMetadata 登记，但必须声明 `approval.shadow_publish_authorized: true`，目标只能是影子表；完成 `full` 后同样自动同步 Git 远程。

清理发布的 `cleanup.sql` 只能删除 YAML 中逐项声明并经过授权的对象，发布器会逐项校验 SQL 覆盖范围；`postcheck.sql` 必须证明当前正式表仍存在、待清理对象已不存在。清理前先执行 OpenMetadata 只读计划，服务不可达或计划失败时直接阻断删除；ClickHouse 清理通过后，再由固定同步器对 `openmetadata.retire` 中的表资产执行退休删除并回读确认。清理发布不创建物理回滚备份，失败后的恢复依据是 Git 中对应历史发布包；若元数据应用阶段临时失败，保留不完整状态并在服务恢复后重跑同一清理发布。

## 冗余和重跑处理

- 同一 `release_id` 的发布指纹发生变化时直接阻断，必须新建版本号，避免同名规则漂移。
- 相同指纹已经成功发布时默认幂等返回，不重复写入；只有显式 `--rerun` 才允许重新执行。
- 发布阶段 SQL 文件重复使用会阻断，防止重复插入或重复切换。
- OpenMetadata 契约路径自动去重；不同文件指向同一表会阻断，防止后写契约覆盖先写契约。
- 暂存区已有未归属本次发布的内容时阻断，发布器不会把无关改动一起提交。
- 失败发生在 `swap` 前时，生产表不变，候选表默认保留供诊断；不得自动删除后重跑。
- `swap` 后的质量、元数据或清理失败时，优先执行固定 `rollback`；回滚失败必须明确标记 `rollback_failed`，不得报告为成功。
- 清理失败但正式表和元数据已经正确时，标记 `cleanup_pending`，不得为了清理临时对象再破坏正式表。
- Git 最终留痕失败时标记 `version_record_pending`，使用 `finalize` 补记；不能把平台成功当成完整发布成功。
- Git 最终推送失败标记 `version_record_pending`；ClickHouse 和 OpenMetadata 结果不回滚，仅保留本地版本记录并阻断“完整发布成功”状态，`finalize` 必须补记报告、标签和远程推送。发布前不再把远程推送作为数据写入前置条件。
- Git 推送固定使用非交互模式和 60 秒超时；网络、凭据或超时失败都必须快速落为 `version_record_pending`，不得留下等待输入的后台推送进程，恢复后仍通过同一发布的 `finalize` 重试。
- Git 推送默认自动重试 3 次，退避间隔由 `git.push_retry_backoff_seconds` 控制；同一 `full` 进程在远程失败后自动尝试 `finalize`，只有重试仍失败才等待后续人工/调度补偿。
- 版本历史不通过 ClickHouse 多套正式表保存；成功发布后只保留当前正式表和必要的运行态/审计报告。
- 影子表、验证表和历史备份表不因“发布成功”自动全部保留；已确认晋级、退回或过期的对象必须另行生成清理发布。候选表和 `__previous__` 临时名仍由正式发布成功后的 `cleanup` 自动清理。
- 清理发布优先保护数据对象：OpenMetadata 只读计划是删除前置门禁；清理 SQL 只允许操作 `cleanup.objects`，`DROP/TRUNCATE` 未声明对象或漏删声明对象都会阻断。
- 发布锁文件只在进程持有期间存在，释放后自动清理；若 Windows 仍有并发句柄，报告保留清理异常但不影响已完成发布状态。

## 失败恢复

发布报告位于发布包目录的 `release-report-<release_id>.json`。报告记录阶段状态、SQL/契约哈希、ClickHouse 返回、OpenMetadata 同步报告、回滚结果和 Git 提交结果，不记录密码、Token 或 Cookie。

回滚不是直接改历史正式表，而是从 Git 取上一版完整发布包，复制为一个新的回滚发布包，声明新的 `release_id` 和 `release_type: rollback`，再走同一条候选构建、校验、切换、元数据同步和 Git 留痕流程。这样回滚本身也可审计、可重跑、可再次回滚。

## 与清洗和建模 Skill 的关系

ODS 到 DWD 仍先由 `data-warehouse-cleaning` 固化字段、粒度、金额、JSON、枚举和质量契约；DWS/ADS 仍由 `data-warehouse-modeling` 先声明粒度和指标。发布器只负责把已经审批的契约和固定 SQL 按顺序交付，不替代建模决策，也不允许绕过影子表审批直接发布。

## 本地闭环验证

发布器单元和本地候选切换集成测试统一运行：

```powershell
C:\Users\24796\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest -v tests\test_warehouse_release.py
```

该测试使用临时 Git 工作树、裸仓库和模拟 ClickHouse/OpenMetadata 执行器，不写真实数仓；真实环境仍必须通过 `verify` 后再经用户批准执行 `full`。
