# ClickHouse 数仓显性发布流程

本项目的版本源是 Git，ClickHouse 和 OpenMetadata 是发布结果。任何正式 SQL、字段、粒度、枚举、清洗契约或血缘变化，都必须生成一个发布 YAML，并通过项目发布入口执行；手工执行 SQL 不算完成发布。

## 一条固定路径

```text
发布 YAML
  -> 版本包校验与指纹
  -> Git 工作区和工具预检
  -> Git 预提交（记录待发布版本）
  -> Git 预推送（远程版本先行登记，失败则不进入数据写入）
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

入口：

```powershell
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd --release <发布YAML> --mode plan
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd --release <发布YAML> --mode verify
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd --release <发布YAML> --mode full
C:\Users\24796\Documents\TEXT2SQL\warehouse-release.cmd --release <发布YAML> --mode finalize
```

`plan` 只校验文件、版本指纹、阶段顺序和门禁，并执行 Git 工作树/暂存区只读预检，不写 ClickHouse、OpenMetadata 或 Git。发布器会自动补齐随附 Git 运行时的 HTTPS、receive-pack 等辅助程序路径，不要求调用方手工设置环境变量。`verify` 只执行健康检查、只读 SQL 和 OpenMetadata 回读。`full` 才是正式发布动作。`finalize` 用于平台已经完成但 Git 最终提交或标签遇到临时故障后的显式补记，不会重新执行数据写入。

## 发布包最小要求

发布文件必须声明：

- `release_id`、`version`、`release_type`、`environment`、`status`。
- `source.database` 和不可为空的输入分区列表。
- 每张目标表的中文业务名、物理名、粒度、主键、唯一候选表名和临时旧表名。
- `publish.strategy: candidate_swap` 与七个阶段 SQL：`preflight`、`build`、`quality`、`swap`、`postcheck`、`rollback`、`cleanup`。
- `approval.status: approved` 和 `approval.formal_publish_authorized: true`。
- `openmetadata.contracts`，由固定同步入口执行 `plan -> apply -> verify`。
- `git.required: true`、`git.auto_commit: true`、`git.auto_push: true`、`git.remote`、`git.branch` 和发布标签。

`build` 只能创建并写入候选表；`swap` 负责原子切换；`cleanup` 不得删除当前正式表；`rollback` 必须能把切换前对象恢复为正式对象。只读阶段如果出现 DDL/DML 关键字会直接阻断。

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
- Git 预推送失败时阻断 ClickHouse 写入，并把已完成的本地预提交记录为 `version_record_pending`；Git 最终推送失败同样标记 `version_record_pending`，`finalize` 必须同时补记本地报告、标签和远程推送。
- 版本历史不通过 ClickHouse 多套正式表保存；成功发布后只保留当前正式表和必要的运行态/审计报告。
- 发布锁文件只在进程持有期间存在，释放后自动清理；若 Windows 仍有并发句柄，报告保留清理异常但不影响已完成发布状态。

## 失败恢复

发布报告位于发布包目录的 `release-report-<release_id>.json`。报告记录阶段状态、SQL/契约哈希、ClickHouse 返回、OpenMetadata 同步报告、回滚结果和 Git 提交结果，不记录密码、Token 或 Cookie。

回滚不是直接改历史正式表，而是从 Git 取上一版完整发布包，复制为一个新的回滚发布包，声明新的 `release_id` 和 `release_type: rollback`，再走同一条候选构建、校验、切换、元数据同步和 Git 留痕流程。这样回滚本身也可审计、可重跑、可再次回滚。

## 与清洗和建模 Skill 的关系

ODS 到 DWD 仍先由 `data-warehouse-cleaning` 固化字段、粒度、金额、JSON、枚举和质量契约；DWS/ADS 仍由 `data-warehouse-modeling` 先声明粒度和指标。发布器只负责把已经审批的契约和固定 SQL 按顺序交付，不替代建模决策，也不允许绕过影子表审批直接发布。

## 本地闭环验证

发布器单元和本地候选切换集成测试统一运行：

```powershell
C:\Users\24796\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe tests\test_warehouse_release.py
```

该测试使用临时 Git 工作树、裸仓库和模拟 ClickHouse/OpenMetadata 执行器，不写真实数仓；真实环境仍必须通过 `verify` 后再经用户批准执行 `full`。
