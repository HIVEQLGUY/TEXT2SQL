# 当前状态

## 25. 发布器回滚门禁测试完成 2026-07-24

- 最新本地发布链路提交为 `23b00b6`（`test: cover rollback after postcheck failure`）；本地 `main` 相对缓存的 `origin/main` 领先 5 个提交，暂存区为空。
- 11 项发布器测试全部通过，覆盖成功发布、预推送失败后 `finalize`、`postcheck` 失败后 `rollback`、候选表保护、只读阶段和并发锁。
- 当前仍有 CH-UI/查询工作台相关未提交改动，未纳入上述 5 个发布链路提交。

## 24. 预推送失败可恢复性修正 2026-07-24

- 修复发布器失败路径：Git 预提交成功但预推送失败时，不再把报告留在不可 `finalize` 的 `blocked` 状态，而是落为 `version_record_pending`，并提交本地报告。
- `finalize` 现在可以接管该状态，补记报告、创建标签并重新推送；新增回归测试覆盖“预推送失败 -> 本地留痕 -> finalize 成功”。
- 发布器测试现为 11 项全部通过；当前抖店修正发布包 `plan` 和真实 `verify` 仍分别通过，未执行任何真实 `full` 写入。

## 23. CH-UI 现成 ClickHouse Web UI 试用安装包 2026-07-24

- 按用户要求保留此前自研 `ClickHouse 查询工作台`，并新增 CH-UI 现成工具试用安装包；二者当前并存，不互相覆盖。
- 已在 `tools/ch-ui` 固化 CH-UI Docker Compose 安装包、启动脚本、停止脚本、健康检查脚本和 README：
  - `tools/ch-ui/docker-compose.yml`
  - `tools/ch-ui/docker-compose.wsl.yml`
  - `tools/ch-ui/.env.example`
  - `tools/ch-ui/start-ch-ui.ps1`
  - `tools/ch-ui/start-ch-ui-wsl.ps1`
  - `tools/ch-ui/stop-ch-ui.ps1`
  - `tools/ch-ui/stop-ch-ui-wsl.ps1`
  - `tools/ch-ui/check-ch-ui.ps1`
  - `tools/ch-ui/README.md`
- CH-UI 官方推荐 Docker 镜像路径为 `ghcr.io/caioricciuti/ch-ui:latest`，默认容器端口 `3488`；本项目 Windows 侧实际可用访问地址为 `http://localhost:3488`，WSL 内健康检查地址为 `http://127.0.0.1:3488/health`。
- 当前 Windows 主机仍未发现 `docker`、Docker Desktop 或 `winget` 命令；实际使用 WSL `Ubuntu-24.04` 内 Docker 启动。`docker-compose.wsl.yml` 已按用户要求切回 `network_mode: host`，让 CH-UI 直接连接 WSL 内 ClickHouse 测试库 `http://127.0.0.1:8123`，避免 `host.docker.internal:8123` 解析到 Docker 网关后连接失败。
- 当前状态为：CH-UI 已通过 WSL Docker 启动，容器名 `youmei-ch-ui`，状态 `healthy`；`http://localhost:3488/health` 于 2026-07-24 16:09 +08:00 返回 200，WSL 内 `http://127.0.0.1:3488/health` 返回 200，ClickHouse 测试库 `http://127.0.0.1:8123/ping` 返回 `Ok.`。启动命令为 `powershell -ExecutionPolicy Bypass -File tools/ch-ui/start-ch-ui-wsl.ps1`。
- 边界：CH-UI 用于试用现成 ClickHouse Web UI 能力；项目内自研 `ClickHouse 查询工作台` 仍保留为受控只读验证网关，承担 SQL 白名单、默认 LIMIT、查询审计和 Git 发布包验证记录。

## 22. 发布链路本地提交与公开仓库推送门禁 2026-07-24

- 本次发布链路改造已形成本地 Git 提交 `2cd488b`（`chore: harden warehouse release workflow`），包含发布器、测试、流程文档、真实只读验证报告和状态台账；未提交的 ClickHouse 查询工作台改动未混入。
- 本地 `main` 当前相对缓存的 `origin/main` 领先 2 个提交：`f007765` 基线和 `2cd488b` 发布链路改造。当前 `.git` 暂存区为空，剩余工作区改动均为未提交的其他工作台文件。
- 已尝试普通快进推送 `origin/main`，但被公开仓库外发安全门禁拒绝；远程未发生变化，不能报告为 GitHub 已同步，也不得通过其他路径绕过该门禁。
- 真实只读验证、本地全流程集成验证和本地版本提交均已完成；剩余闭环只有公开仓库推送，以及物流快递单号影子契约审批后生成标准正式发布包并执行真实 `full`。

## 21. 发布链路本地闭环与真实只读验证 2026-07-24

- 发布器已优化 Git 运行时封装：自动发现随附 Git 后，会为所有 Git 子进程补齐 HTTPS、receive-pack 等辅助程序路径；不再依赖调用方临时设置 `PATH` 或 `GIT_EXEC_PATH`。
- 发布锁生命周期已固化：锁只在发布进程持有期间存在，释放后自动清理；新增的本地集成测试覆盖锁文件不残留。
- 发布器单元/集成测试现为 9 项全部通过，集成测试在临时 Git 工作树和裸仓库中验证健康检查、preflight、build、quality、swap、postcheck、OpenMetadata、cleanup、最终提交、分支推送和标签。
- `warehouse-release.cmd` 当前抖店修正包 `corrective-release-tracking-no-shadow-1.3.2.yaml` 的 `plan` 已通过，且 Git 只读预检结果已写入计划报告；此前 Git 路径对象无法 JSON 序列化的问题已修复。
- 真实 ClickHouse 只读健康检查已通过，版本 `26.6.1.1193`；真实 OpenMetadata `verify` 已通过，版本 `1.12.11`，读取 2 份契约并生成回读报告。当前真实验证命令为 `warehouse-release.cmd --release ...corrective-release-tracking-no-shadow-1.3.2.yaml --mode verify`。
- 真实 ClickHouse 当前源表 `ODS_销售订单列表信息表(抖店API)(ods_api_dd_sale_order_list_info_f)` 仅有分区 `2026-07-23`、45,140 行；现有正式 DWD 仍为此前 `2026-07-22` 快照口径：订单主单 49,695 行、商品明细 85,770 行。当前修正包仍引用 `2026-07-22`，因此不能把只读验证误报为可重建的正式发布。
- 当前仍未执行真实 `full`、生产表切换或 GitHub 推送。原因分别是：物流快递单号影子契约仍待用户审阅批准；现有修正包是历史兼容结构，只允许 `plan/verify`；GitHub 公开仓库首次推送还未获得可验证的网络/推送结果。

## 20. Git 版本与发布链路现状 2026-07-24

- 当前版本源规则已生效：Git 托管清洗契约、建模 SQL、发布 YAML、质量 SQL、OpenMetadata 契约、发布报告和回滚依据；ClickHouse 只保留当前正式对象，OpenMetadata 只保留当前元数据结果，二者都不是版本源头，也不会因人工改表自动回写 Git。
- 本地项目 `C:\Users\24796\Documents\TEXT2SQL` 已有基线提交 `f007765`（`chore: establish warehouse release baseline`），当前分支为 `main`，基线包含 1088 个项目文件；当前缓存的 `origin/main` 仍为 `62f0a7f`，本地领先 1 个提交，首次推送尚未完成。
- GitHub 远程为 `https://github.com/HIVEQLGUY/TEXT2SQL.git`，最近一次实时 `ls-remote` 复查于 2026-07-24 14:35 因网络无法连接 `github.com:443` 失败；因此当前不能宣称远程已同步。此前只读分支确认结果仍保留为历史证据。
- 工作区当前不是干净状态：存在 `.gitignore`、修正发布计划报告、发布器测试和 ClickHouse 查询工作台相关未提交改动，以及工作台检查脚本/包管理文件等未跟踪文件；这些改动尚未统一归属，不能直接全部纳入一次发布提交。
- 发布器 `tests/test_warehouse_release.py` 已补齐远程分支推送测试，使用项目随附 Git 运行时的 `mingw64/bin` 辅助程序路径；在设置 `PATH` 与 `GIT_EXEC_PATH` 后，7 项单元测试全部通过。
- 当前抖店修正发布包 `corrective-release-tracking-no-shadow-1.3.2.yaml` 的 `plan` 已通过，指纹为 `577c68dfeebae749282074f899c8c3e395b41e9731578b99c88e9adbc5867229`；`plan` 只完成发布包、指纹、阶段、Git 预检，不写 ClickHouse、不写 OpenMetadata、不推送 GitHub。
- 本次尚未执行正式 `full`、候选表切换、正式 OpenMetadata 发布或远程 Git 推送；该修正包本身仍是影子验证后待用户审阅状态，不能绕过粒度契约批准直接 `full`。因此端到端链路当前为“实现并通过计划/单测，未完成生产闭环”。
- 下一道门禁：先分类并处理工作区未提交改动；用户明确授权向当前公开 GitHub 仓库推送或改用私有仓库后，推送本地基线；正式清洗契约获批后再按 `verify -> full -> finalize（如需）` 执行并保留报告。

## 17. 数仓显性发布与 Git 版本规则确认 2026-07-23

- 最新用户规则：发布动作必须显性化；任何正式 SQL 变更都必须形成发布动作，发布后生成或切换到最新版本生产表；历史口径、历史字段、历史枚举、历史 OpenMetadata 元数据契约和发布报告必须作为版本信息进入 Git。
- 已更新项目强规则 `AGENTS.md` 和 `data-warehouse-cleaning` Skill：Git 是清洗和建模版本的权威来源，ClickHouse 和 OpenMetadata 是发布结果，不是版本源头。
- 当前已有能力：发布 YAML、ClickHouse SQL 文件、质量 SQL、OpenMetadata 契约、OpenMetadata 固定同步入口 `sync-openmetadata.cmd`，以及项目级显性发布总控 `warehouse-release.cmd`。
- 发布总控固定执行：发布包校验与指纹 -> Git 预提交 -> ClickHouse 健康检查 -> preflight/build/quality/swap/postcheck -> OpenMetadata `plan -> apply -> verify` -> cleanup -> Git 报告与标签。
- 发布总控已覆盖重复 release_id、规则指纹漂移、SQL 阶段复用、候选表/正式表重名、只读阶段写入、构建直写正式表、OpenMetadata 契约重复、Git 暂存区污染、并发发布锁、失败回滚、临时对象清理和最终 Git 留痕失败等情况。
- 当前环境限制仍存在：命令行当前找不到 `git` 可执行文件；因此本次只完成发布流程代码、计划验证和单元测试，未执行正式 `full` 发布。
- 本次新增固定资产：`scripts/warehouse_release.py`、`warehouse-release.cmd`、`docs/warehouse-release-process.md`、`config/warehouse-release-template.yaml` 和 `tests/test_warehouse_release.py`。
- 已验证：发布器 `plan` 可通过现有抖店修正发布文件；候选表切换、阶段 SQL 重复、直写正式表、只读阶段写入和并发锁测试通过；四个相关 Skill 的 UTF-8 校验通过。

## 16. OpenMetadata 固定同步入口落地 2026-07-23

- 已补充项目级固定入口 `sync-openmetadata.cmd`，内部调用 `scripts/sync_openmetadata_release.py`，用于从发布文件自动读取 `openmetadata.contracts` 中登记的 `metadata-contract-*.yaml`。
- 固定执行路径为：发布文件 -> 元数据契约列表 -> `plan -> apply -> verify` -> `openmetadata-sync-report-<发布文件名>.json`。
- 默认凭据读取入口为 `local/credentials/openmetadata.env`，不输出密码、Token 或密钥正文。
- 已用当前抖店订单物流快递单号粒度影子修正发布文件 `corrective-release-tracking-no-shadow-1.3.2.yaml` 执行 `--mode plan` 验证通过，自动识别 2 份 OpenMetadata 契约，并生成计划报告 `config/warehouse_cleaning/doudian_order_item_v1/openmetadata-sync-report-corrective-release-tracking-no-shadow-1.3.2.json`。
- 已更新项目强规则 `AGENTS.md` 和 `data-warehouse-cleaning` Skill：后续 ClickHouse 表结构、字段中文名、字段注释、业务口径、枚举、标签、粒度、血缘或清洗契约发生变化时，正式发布必须走该固定入口；探索期允许只执行 `--mode plan`。

## 15. 抖店订单物流粒度影子验证修正 2026-07-23

- 最新用户规则：粒度对齐阶段本质是重写清洗契约，验证结果如需落表必须先落影子表/探查表，不得直接开发或切换正式 DWD；只有用户审阅影子结果并明确批准正式契约后，才能晋级正式 DWD。
- 已更新项目强规则 `AGENTS.md` 和 `data-warehouse-cleaning` Skill：粒度对齐和清洗契约重写阶段只允许创建影子表/探查表并输出质量报告；快递单号用于运费匹配时，以快递单号作为物流业务粒度；包裹ID无业务价值时，不作为目标粒度字段保留；包裹ID粒度下的数值字段按快递单号汇总，平均型指标按快递单号取平均。
- 已撤回 1.3.1 直接正式 DWD 变更：`DWD_抖店订单商品明细事实全量快照表(dwd_trade_order_item_df)` 已恢复到 1.3.0 稳定口径，85,770 行，37 字段；1.3.1 直接商品明细表留存为 `dwd_trade_order_item_df_direct_logistics_backup_1_3_1`。
- 1.3.1 物流直建表已撤出正式 DWD：`dwd_trade_order_logistics_package_df` 改名为 `dwd_trade_order_logistics_package_validation_1_3_1`；`dwd_trade_order_logistics_package_item_df` 改名为 `dwd_trade_order_logistics_package_item_validation_1_3_1`。
- 当前正式 DWD：`DWD_抖店订单主单事实全量快照表(dwd_trade_order_df)` 49,695 行、82 字段；`DWD_抖店订单商品明细事实全量快照表(dwd_trade_order_item_df)` 85,770 行、37 字段；物流正式 DWD 直建表数量为 0。
- 已创建 `DWD_抖店订单物流快递单号粒度影子表(dwd_trade_order_logistics_tracking_no_shadow_1_3_2)`：42,838 行，18 字段；粒度为店铺ID(shop_id) + 店铺订单号(shop_order_id) + 快递单号(tracking_no)；快递单号键唯一，空值 0；包裹ID字段数 0。
- 快递单号影子表汇总结果：包裹数汇总 42,839；物流商品关系行数汇总 73,934；商品子单数汇总 73,934；发货商品数量汇总 74,275。
- OpenMetadata 已同步并回读验证：`dwd_trade_order_item_df` 当前正式口径 37 字段；`dwd_trade_order_logistics_tracking_no_shadow_1_3_2` 影子表 18 字段。
- 固化文件位于 `config/warehouse_cleaning/doudian_order_item_v1`：`formal-revert-logistics-direct-dwd-stepwise-1.3.2.sql`、`shadow-logistics-tracking-no-execution-1.3.2.sql`、`shadow-logistics-tracking-no-quality-checks-1.3.2.sql`、`metadata-contract-formal-item-1.3.2.yaml`、`metadata-contract-shadow-logistics-tracking-no-1.3.2.yaml`、`corrective-release-tracking-no-shadow-1.3.2.yaml`。

## 14. 抖店订单 DWD 物流履约粒度修正 2026-07-23

- 已按用户最新确认修正建模判断：物流单号/包裹粒度具有独立业务价值，不能按“无业务价值明细项”规则压回订单粒度。
- 已更新项目强规则 `AGENTS.md` 和 `data-warehouse-cleaning` Skill：订单类接口中，金额明细项、优惠明细项、标签项等解释型数组继续值转列或汇总回父粒度；物流信息、履约包裹、快递单号、发货商品关系、退款、结算、费用等独立业务过程必须先验证关系基数，再决定独立事实表或桥接关系表。
- 已完成粒度验证：
  - 订单商品明细中的明细订单号 `sku_order_list.order_id` 与物流商品信息中的商品子单号 `logistics_info.product_info.sku_order_id` 语义一致，73,934 条物流商品关系全部匹配商品明细，未匹配 0 条。
  - 包裹ID(package_id) 在 `店铺ID + 店铺订单号 + 包裹ID` 下唯一：42,839 行 / 42,839 个键。
  - 快递单号(tracking_no) 不完全唯一：42,839 行 / 42,838 个键，存在 1 个重复快递单号对应多个包裹ID的情况。
  - 包裹与商品子单不是一对一：12,087 个包裹只含 1 个商品子单，30,752 个包裹含多个商品子单，单包裹最多 6 个商品子单；73,924 个商品子单对应 1 个包裹，5 个商品子单拆到多个包裹，最多 2 个包裹。
- 已完成正式 DWD 1.3.1 修正：
  - `DWD_抖店订单主单事实全量快照表(dwd_trade_order_df)`：49,695 行，82 字段，粒度为店铺ID(shop_id) + 店铺订单号(shop_order_id)，本次未重建。
  - `DWD_抖店订单商品明细事实全量快照表(dwd_trade_order_item_df)`：85,770 行，38 字段，新增商品子单号(sku_order_id)，粒度修正为店铺ID(shop_id) + 店铺订单号(shop_order_id) + 商品子单号(sku_order_id)；1.3.0 旧表保留为 `dwd_trade_order_item_df_backup_1_3_0`。
  - `DWD_抖店订单物流包裹事实全量快照表(dwd_trade_order_logistics_package_df)`：42,839 行，21 字段，粒度为店铺ID(shop_id) + 店铺订单号(shop_order_id) + 包裹ID(package_id)。
  - `DWD_抖店订单物流包裹商品子单关系事实全量快照表(dwd_trade_order_logistics_package_item_df)`：73,934 行，19 字段，粒度为店铺ID(shop_id) + 店铺订单号(shop_order_id) + 包裹ID(package_id) + 商品子单号(sku_order_id)，用于处理合包和拆包履约分析。
- 质量门禁已通过：
  - 商品明细商品子单键唯一：85,770 行 / 85,770 个键，商品子单号空值 0。
  - 物流包裹键唯一：42,839 行 / 42,839 个包裹键，包裹ID空值 0，快递单号空值 0。
  - 物流包裹商品子单关系键唯一：73,934 行 / 73,934 个键，商品子单号空值 0。
  - 物流包裹均可回连订单主单，未匹配 0。
  - 物流包裹商品子单关系均可回连商品明细和物流包裹，未匹配 0。
- OpenMetadata 已完成 `plan -> apply -> verify`：
  - `dwd_trade_order_item_df` 回读验证 38 字段。
  - `dwd_trade_order_logistics_package_df` 回读验证 21 字段。
  - `dwd_trade_order_logistics_package_item_df` 回读验证 19 字段。
- 固化文件位于 `config/warehouse_cleaning/doudian_order_item_v1`：
  - `logistics-grain-probe-1.3.1-fixed.sql`
  - `logistics-item-key-probe-1.3.1.sql`
  - `logistics-item-mapping-probe-1.3.1.sql`
  - `logistics-cardinality-probe-1.3.1.sql`
  - `logistics-cardinality-examples-1.3.1.sql`
  - `formal-logistics-refactor-execution-1.3.1.sql`
  - `formal-logistics-refactor-quality-checks-1.3.1.sql`
  - `formal-logistics-refactor-swap-1.3.1.sql`
  - `formal-logistics-refactor-postcheck-1.3.1.sql`
  - `metadata-contract-formal-item-1.3.1.yaml`
  - `metadata-contract-formal-logistics-package-1.3.1.yaml`
  - `metadata-contract-formal-logistics-package-item-1.3.1.yaml`
更新时间：2026-07-23 16:26 +08:00

## 1. 当前项目方向

项目方向已收敛：

- 数据接入未来只通过“预策”作为接入层推进。
- ClickHouse 是当前数仓可行性测试和后续建模验证方向。
- 旧 RDS、Text2SQL、DataAgent、自研 API ingestion、Doris CONNECT/ODS、DataX-Web、SeaTunnel 接入链路均不再作为未来推进方向。

## 2. 当前有效资源

当前资源访问状态统一维护在：

```text
TEXT2SQL-codex-handoff/docs/RESOURCE-资源登记.md
```

每一次资源查询都视为新的状态确认，必须同步更新该文件。

本地账号、密码、Token、私钥、网页登录说明等敏感凭据统一保存在：

```text
C:\Users\24796\Documents\TEXT2SQL\local\credentials\
```

资源登记表只写凭据位置和最近验证状态，不写密码正文。

## 3. 历史留存

历史接口接入代码、SDK bridge、接口契约、调度和注意事项已压缩留存在桌面：

```text
C:\Users\24796\Desktop\youmei-api-ingestion-archive-20260719.zip
```

该压缩包仅作后续参考，不代表当前架构继续推进。

## 4. 已停止推进的方向

- Doris 本地数仓与 CONNECT/ODS 接入层。
- DataAgent API 作为统一访问层。
- Text2SQL/RDS 问数执行链路。
- DataX-Web 新增同步。
- SeaTunnel 作为本项目后续默认接入路径。
- DolphinScheduler 不再承载本项目自研接口采集，但服务需要保留。
- Superset 服务需要保留；旧 Doris 看板数据不再作为当前方向。
- 已释放的旧问数 RDS 不再登记连接信息。

## 5. 后续工作原则

1. 任何新数据接入需求先问：预策是否能提供、以什么表/文件/接口交付、交付到哪里。
2. 任何建模验证默认进入 ClickHouse。
3. 历史 Doris/接口探查结果只能作为字段线索，不能作为当前建模事实。
4. 项目文档保持轻量；过期历史、临时说明和旧框架文档不再保留为当前入口。

## 6. ClickHouse 抖店订单 ODS 初始确认 2026-07-22

- ClickHouse 测试库：`youmei_sandbox`。
- 已确认正式候选源表：`ODS_销售订单列表信息表(抖店API)`（`ods_api_dd_sale_order_list_info_f`），当前 52,431 行，店铺订单号 52,431 个，店铺 5 个，日分区为 2026-07-21。
- 同名增量表 `ODS_销售订单列表信息表(抖店API)`（`ods_api_dd_sale_order_list_info_du`）已按用户要求于 2026-07-22 删除；删除后查询 `system.tables` 无结果。后续不得再把该 DU 表作为候选上游。
- 临时表 `临时建模测试表：STD_抖音_订单销售明细，可删除`（`tmp_ud_3418004512502203_sxssjqx_model_test`）已按用户要求于 2026-07-22 删除；删除后查询 `system.tables` 无结果。后续不得再把该表作为候选上游或历史线索入口。
- 正式候选源表是订单主单层，`订单详情信息(sku_order_list)` 为订单商品明细 JSON 数组。展开后有 90,279 行订单商品明细，覆盖 52,431 个店铺订单号。
- 展开后的订单商品明细中，商品ID和SKU字段当前均无空值；直播间ID空值或 0 值 51,936 行，直播间ID数（含空/0）390；达人ID字段空值或 0 值 45,840 行。后续 DWD 设计必须基于 JSON 展开和字段语义验证，不能直接用主单表行作为商品明细粒度。
- 相关只读探查 SQL 位于 `TEXT2SQL-codex-handoff/tmp/probe_clickhouse_doudian_order_*_20260722.sql`。

## 7. 数据清洗 Skill 与 ODS 实践 2026-07-22

- 已生成并安装 `data-warehouse-cleaning` Skill：源目录为 `C:\Users\24796\Documents\skill创建\data-warehouse-cleaning`，可路由目录为 `C:\Users\24796\.codex\skills\data-warehouse-cleaning`；`quick_validate.py` 通过。
- 已将 ODS 到 DWD 清洗设为 `data-warehouse-modeling` 的强制前置步骤；默认 ClickHouse，不再以 Doris 作为建模引擎。
- 已固化实践包：`config/warehouse_cleaning/doudian_order_item_v1`，包括源画像、机器可读清洗契约、中文版契约说明、枚举字典、质量 SQL、清洗 SQL 草案、执行计划、审批记录和 ODS 元数据契约。
- 当前清洗契约版本为 `1.2.0`，商品支付金额（`pay_amount`）按分转元，商品原价（`goods_price`）按用户确认的元处理，目标金额统一保留两位小数；未创建正式 DWD 表。
- 接口文档字段树已固化 622 个路径：502 个标量字段全部纳入展开契约，51 个业务数组全部纳入关系契约；根传输容器 `shop_order_list` 因 ODS 已一行一单而不重复落表。
- JSON 展开目标按粒度拆分为订单主单（`dwd_trade_order_df`）、订单商品明细（`dwd_trade_order_item_df`）和 51 个数组子关系；接口响应页 `page`、`size`、`total` 在当前 ODS 不可观测，已登记为待接入元数据而非伪造值。
- 已确认金额公共规则：金额按字段单位证据处理、目标保留两位小数、负数保留符号、空值转 NULL、非空非法值进入异常统计、零值保留为零。
- 当前 ODS 技术结论：窗口全量快照；订单商品明细粒度为店铺订单号 + 商品明细数组序号；当前快照技术主键唯一性通过。
- 已按用户确认执行 ClickHouse 影子清洗表 `dwd_trade_order_item_shadow_1_2_0`：90,279 行、技术主键 90,279 个、商品ID/SKU/数量/金额解析异常均为 0，原始 JSON 列数量为 0。
- 当时正式 DWD 尚未创建；截至 2026-07-23 14:28 已创建订单主单和商品明细核心字段阶段性正式 DWD，完整 502 个标量字段的最终物理类型契约仍需逐字段完成。
- 影子表已在 OpenMetadata 注册并回读验证 36 个字段和 25 个表级属性；复合技术键以 `technical_key_fields=shop_order_id,item_index` 登记。
- 已生成 `json-type-candidates.yaml`：502 个字段中 243 个可按接口逻辑类型处理，218 个需要字段级语义确认，41 个阻断；候选不直接作为正式 DWD 类型。

## 8. OpenMetadata ODS 同步 2026-07-22

- 已在 OpenMetadata `1.12.11` 注册稳定表级自定义属性，并完成 ODS 和影子表契约的 `dry-run -> diff -> apply -> read-back verify`。
- 已写入并回读验证：ODS 表 92 个字段、中文显示名、字段注释、ClickHouse 类型映射、主键标识、25 个表级自定义属性和枚举结构化内容；新增 JSON 全字段展开策略、字段树版本、标量字段数、业务关系数和关系契约版本。2026-07-23 后业务字段不再按安全、保密、脱敏或敏感性生成排除/打标规则。
- 枚举属性当前写为 `enum_dictionary_version=pending`；内容状态为 `reviewed`，未知编码保留并标记，未将未审批枚举字典伪装成正式版本。
- 后续金额规则审批后，必须增加清洗契约版本，重新生成 DWD 元数据契约并沿用同一 OpenMetadata 同步脚本。

## 9. 当前数仓架构展示页 2026-07-23

- 已生成本地 HTML 架构展示页：`docs/youmei-warehouse-architecture-20260723.html`。
- 页面覆盖当前主链路、抖店订单主题进度、ClickHouse 分层、OpenMetadata 治理、Superset/DolphinScheduler 保留状态、Git 可重建型版本管理方案、业务分析流和后续落地路径。
- 页面明确区分已完成、部分完成、未运行、已下线、阻塞待确认和待落地状态；该页面生成时 Git 可重建型版本管理、ClickHouse 元数据控制库、正式 DWD 仍为待落地。正式 DWD 核心版的最新状态以本文件第 11 节为准。

## 10. 抖店订单主单影子清洗 2026-07-23

- 用户明确要求物理 DWD 不保留治理字段；后续治理信息放在运行清单、发布记录、质量结果和 OpenMetadata 中，不塞入业务表字段。
- 用户进一步明确：本项目不存在业务字段安全风险考虑，后续数据清洗 Skill 不需要按“敏感字段”排除字段。业务字段是否进入 DWD/DIM/DWS/ADS 只由业务语义、粒度、类型契约、质量结果和下游用途决定；平台账号、密码、Token、Cookie、私钥等凭据仍按资源凭据规则处理。
- 已生成订单主单清洗增补契约：`config/warehouse_cleaning/doudian_order_item_v1/order-cleaning-contract-addendum.yaml`。
- 当前 `ODS_销售订单列表信息表(抖店API)`（`ods_api_dd_sale_order_list_info_f`）最新可见分区为 `2026-07-22`，当前行数 51,878，`店铺ID + 店铺订单号` 去重后 49,695 个键。
- 发现 2,183 个重复订单主单键、4,366 行重复记录；重复键最大重复 2 行；整行哈希冲突数为 0，判断为完全相同行重复装载。订单主单影子清洗采用 `DISTINCT` 折叠完全重复行；若后续出现同键不同内容，质量门禁阻断，不自动覆盖。
- 已创建并重建 `DWD_抖店订单主单影子清洗表`（`dwd_trade_order_shadow_1_2_0`）：49,695 行、复合键 49,695 个，字段数 65 个，磁盘占用约 46.03 MiB。
- 订单主单影子表只排除原始 JSON 和本轮未定型字段；已纳入收件人、电话、地址、加密/脱敏联系信息、地址ID、买家留言、商家备注、支付渠道流水号等订单业务字段。表内不保留清洗批次、质量状态、契约版本等治理字段。
- 已执行订单主单影子质量门禁：通过。支付时间空值 1,110 行，完成时间空值 37,842 行；订单金额范围 0 到 15,780 元，支付金额范围 0 到 15,759 元，支付金额合计 6,070,022.38 元。
- 已生成订单主单影子 OpenMetadata 契约：`metadata-contract-order-shadow.yaml`，包含 65 个字段；当时因 OpenMetadata 凭据未纳入统一资源目录，影子表元数据未写入。该资源目录问题已在正式 DWD 阶段修复，正式 DWD 元数据写入状态见第 11 节。
- 商品明细影子表仍是此前 `2026-07-21` 分区结果；订单主单影子表是 `2026-07-22` 分区结果，影子表之间不能直接进行跨表精确对账。正式 DWD 核心版已统一使用 `2026-07-22` 来源分区，见第 11 节。
- 已按用户要求使用 `next-ai-drawio` 重画目标态逻辑架构图：`docs/youmei-warehouse-architecture.drawio`。该图包含 4 个页签：`01 目标总体架构`、`02 数据流架构`、`03 控制流与治理架构`、`04 业务流与主题模型`，并导出对应 SVG 预览文件：`docs/youmei-warehouse-architecture-01-target-overall.svg`、`docs/youmei-warehouse-architecture-02-data-flow.svg`、`docs/youmei-warehouse-architecture-03-control-governance.svg`、`docs/youmei-warehouse-architecture-04-business-model.svg`。该版本以目标架构为主，不再把历史链路、组件启停状态、具体源表实例或单次建模进度作为架构主体。
- 已根据用户反馈修正 draw.io 图可读性：压缩节点文字、使用 draw.io 原生换行、减少边标签、删除总图中干扰阅读的治理长线，并重新导出 4 张 SVG 预览。

## 11. 抖店订单正式 DWD 核心版 2026-07-23

- 已按用户“继续下一步”确认，将订单主单和商品明细核心字段从影子验证推进为阶段性正式 DWD；截至第 12 节，51 个业务数组子关系中已正式落地2个，完整 502 个接口标量字段和剩余49个业务数组子关系仍需继续逐字段类型契约和质量门禁。
- 正式来源分区统一为 `2026-07-22`：`ODS_销售订单列表信息表(抖店API)`（`ods_api_dd_sale_order_list_info_f`）源行数 51,878，店铺ID+店铺订单号去重后 49,695 个主单键，展开商品明细 89,561 行，店铺ID+店铺订单号+商品明细序号去重后 85,770 个商品明细键。
- 正式发布前冲突检查通过：主单重复行 2,183 行、商品明细重复行 3,791 行，均为完全重复装载；同键不同内容冲突数为 0。正式清洗采用目标字段 `DISTINCT` 折叠，若后续出现同键不同内容则阻断。
- 已创建并写入 `DWD_抖店订单主单事实全量快照表`（`dwd_trade_order_df`）：49,695 行、复合键 49,695 个、字段数 65 个、磁盘占用约 46.03 MiB、支付金额合计 6,070,022.38 元。
- 已创建并写入 `DWD_抖店订单商品明细事实全量快照表`（`dwd_trade_order_item_df`）：85,770 行、复合键 85,770 个、字段数 29 个、磁盘占用约 4.57 MiB；直播间ID为空 49,537 行，达人ID为空 43,563 行。
- 正式质量门禁通过：主单复合键唯一、商品明细复合键唯一、商品ID/SKU/数量无空、正式 DWD 无原始 JSON 列、商品明细均能匹配到订单主单。
- 固化文件位于 `config/warehouse_cleaning/doudian_order_item_v1`：`formal-conflict-checks.sql`、`formal-execution.sql`、`formal-quality-checks.sql`、`formal-postcheck.sql`、`formal-release-core-1.2.0.yaml`、`metadata-contract-formal-order.yaml`、`metadata-contract-formal-item.yaml`，并已更新 `approval.yaml` 和 `run-manifest.json`。
- OpenMetadata 资源目录问题已修复：新增统一凭据文件 `local/credentials/openmetadata.env`，新增统一资源别名 `openmetadata-local`，`check-resource.cmd openmetadata-local` 登录校验通过，版本 `1.12.11`。
- OpenMetadata 正式 DWD 元数据已完成 `plan -> apply -> verify`：`DWD_抖店订单主单事实全量快照表`（`dwd_trade_order_df`）回读验证 65 个字段、26 个表级自定义属性；`DWD_抖店订单商品明细事实全量快照表`（`dwd_trade_order_item_df`）回读验证 29 个字段、26 个表级自定义属性。复合技术键通过 `technical_key_fields` 表级属性登记，不再使用多列列级主键约束。
- 同步脚本已修复两类 OpenMetadata API 适配问题：ClickHouse 原生类型 `Nullable(...)`、`Decimal128(2)`、`DateTime('Asia/Shanghai')` 映射为 OpenMetadata 标准类型；复合键不再对多个字段同时写列级 `PRIMARY_KEY`。

## 12. 抖店订单正式 DWD 子关系增补 2026-07-23

- 已按用户当时要求，将 `物流信息(logistics_info)` 和 `商家收入金额明细项(actual_receive_amount_info.actual_receive_amount_details)` 两个业务数组子关系正式落地；发布版本为 `1.2.1`。该阶段已被第 13 节 `1.3.0` 父粒度归一化重构取代，原子表不再作为当前正式 DWD 口径来源。
- 固化文件位于 `config/warehouse_cleaning/doudian_order_item_v1`：`formal-child-execution-1.2.1.sql`、`formal-child-quality-checks-1.2.1.sql`、`formal-release-child-1.2.1.yaml`、`metadata-contract-formal-actual-receive-detail.yaml`、`metadata-contract-formal-logistics.yaml`。
- 已创建并写入 `DWD_抖店订单商家收入金额明细项事实全量快照表`（`dwd_json_actual_receive_amount_info_actual_receive_amount_details_df`）：72,575 行，复合键为 `店铺ID(shop_id) + 店铺订单号(shop_order_id) + 商家收入金额明细项序号(json_item_index)`，字段数 8，商家收入明细项金额合计 6,352,569.57 元。
- 已创建并写入 `DWD_抖店订单物流信息事实全量快照表`（`dwd_json_logistics_info_df`）：42,839 行，复合键为 `店铺ID(shop_id) + 店铺订单号(shop_order_id) + 物流信息序号(json_item_index)`，字段数 20，物流单号空值 0，发货时间空值 0。
- 正式质量门禁通过：两张子表复合键唯一、目标表同键不同内容冲突为 0、均可匹配订单主单、无原始 JSON 列、金额和时间解析异常为 0。
- 商家收入金额明细项类型编码发现接口文档未列出的编码 `6`，当前 1,110 行；已按既有枚举策略保留编码并标记为 `未知类型:6`，不丢弃记录。
- OpenMetadata 元数据已完成 `plan -> apply -> verify`：`DWD_抖店订单商家收入金额明细项事实全量快照表`（`dwd_json_actual_receive_amount_info_actual_receive_amount_details_df`）回读验证 8 个字段、26 个表级自定义属性；`DWD_抖店订单物流信息事实全量快照表`（`dwd_json_logistics_info_df`）回读验证 20 个字段、26 个表级自定义属性。

## 13. 抖店订单 DWD 父粒度归一化重构 2026-07-23

- 已按用户明确要求优化建模规则：当前抖店订单 DWD 只保留订单粒度和商品明细粒度；金额明细项、优惠明细项、标签项等无独立业务价值的明细项数组，必须值转列或确定性汇总回父粒度，后续类似订单主表均按该规则处理。
- 已更新项目强规则 `AGENTS.md` 和 `data-warehouse-cleaning` Skill；Skill 校验通过。
- 已完成 `1.3.0` 正式重构，固化文件位于 `config/warehouse_cleaning/doudian_order_item_v1`：`formal-refactor-probe-1.3.0.sql`、`formal-refactor-execution-1.3.0.sql`、`formal-refactor-quality-checks-1.3.0.sql`、`formal-refactor-swap-1.3.0.sql`、`formal-release-refactor-1.3.0.yaml`、`metadata-contract-formal-order-1.3.0.yaml`、`metadata-contract-formal-item-1.3.0.yaml`。
- `DWD_抖店订单主单事实全量快照表`（`dwd_trade_order_df`）已切换为 1.3.0：49,695 行，复合键 49,695 个，82 字段；订单主单级商家收入金额明细项已按类型值转列，物流信息已按订单粒度汇总；商家实收金额合计 6,352,569.57 元，物流包裹数合计 42,839。
- `DWD_抖店订单商品明细事实全量快照表`（`dwd_trade_order_item_df`）已切换为 1.3.0：85,770 行，复合键 85,770 个，37 字段；商品明细级商家收入金额明细项已按类型值转列；商品商家实收金额合计 6,352,569.57 元。
- 原 `DWD_抖店订单商家收入金额明细项事实全量快照表`（`dwd_json_actual_receive_amount_info_actual_receive_amount_details_df`）已改名为废弃备份表 `dwd_deprecated_actual_receive_amount_detail_backup_1_2_1`；原 `DWD_抖店订单物流信息事实全量快照表`（`dwd_json_logistics_info_df`）已改名为废弃备份表 `dwd_deprecated_logistics_info_backup_1_2_1`；二者不再作为正式 DWD 口径来源。
- 正式质量门禁通过：订单主单复合键唯一、商品明细复合键唯一、商品明细均可匹配订单主单、正式 DWD 不保留原始 JSON 列、不保留明细项子粒度键 `json_item_index`，订单级和商品级商家实收金额均与明细项合计对账一致。
- OpenMetadata 元数据已完成 `plan -> apply -> verify`：`DWD_抖店订单主单事实全量快照表`（`dwd_trade_order_df`）回读验证 82 个字段、26 个表级自定义属性；`DWD_抖店订单商品明细事实全量快照表`（`dwd_trade_order_item_df`）回读验证 37 个字段、26 个表级自定义属性。

## 18. Git 版本管理与 GitHub 登录状态 2026-07-23

- 已确认本机 Git 可用：`C:\Users\24796\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe`，版本 `2.53.0.windows.3`；此前“当前环境找不到 Git”的判断已纠正。
- 当前项目 `C:\Users\24796\Documents\TEXT2SQL` 已初始化本地 Git 仓库，默认分支为 `main`；截至本次确认尚无提交、远程地址、提交作者姓名和提交作者邮箱。
- Git Credential Manager 已随 Git 安装，版本文件信息为 `2.7.3`，全局凭据助手配置为 `manager`；针对 `github.com` 的本机凭据查询未发现可用凭据。
- GitHub 连接器本次查询登录态因传输层请求失败未完成，不能据此判定账号状态；已打开 GitHub 登录页面供用户完成交互式登录。
- 待完成：确认 GitHub 登录成功、取得本项目远程仓库 URL、确认提交作者姓名和邮箱，然后执行首次提交、远程绑定、推送和发布器 `plan` 验证。

## 19. GitHub 登录与远程绑定 2026-07-24

- GitHub 登录已确认：账号 `HIVEQLGUY`，GitHub 连接器回读用户 ID `95523358`；提交作者信息已按 GitHub 账号配置到本地仓库。
- 当前项目远程 `origin` 已绑定 `https://github.com/HIVEQLGUY/TEXT2SQL.git`；`git ls-remote --heads origin` 只读验证通过，远程存在 `main` 和 `codex/bootstrap-foundation` 两个分支。
- GitHub 已登记到统一资源校验入口，资源别名为 `github-text2sql`，后续可使用 `check-resource.cmd github-text2sql` 固定验证远程访问状态。
- 已补充发布器 Git 自动发现：默认可识别当前 Codex 缓存 Git，不再要求手工传 `--git-executable`；当前纠正发布包执行 `--mode plan` 通过，旧发布包仅产生兼容性警告，不允许直接 `full`。
- 发布器测试已用项目自带 `unittest` 执行，5 项全部通过；当前 Python 环境未安装 `pytest`，未将其缺失误判为代码失败。
- 当前仍未完成：本地初始提交、与远程 `main` 的内容对齐和首次推送；本次只完成登录、身份配置、远程绑定、资源校验和发布计划验证。
## 26. 物流快递单号影子发布与版本链路闭环 2026-07-24

- 已修复发布器首次发布验证缺口：当 ClickHouse 目标表尚不存在时，`verify` 不再把目标表 `postcheck` 和 OpenMetadata 回读误判为失败，改为通过健康检查和只读前置 SQL，并明确输出 `pre_publish_verified`；目标已存在时仍执行完整回读。
- 发布器回归测试已增至 14 项并全部通过；本次新增首次影子发布验证测试。
- 原 `doudian_order_tracking_no_shadow_1_3_3` 因 Git 暂存权限失败的报告保留为失败审计记录；未修改原发布编号指纹，新增纠正发布 `doudian_order_tracking_no_shadow_corrective_1_3_3`，复用同一目标影子表和候选 SQL，不新增正式历史表。
- 纠正发布包 `config/warehouse_cleaning/doudian_order_item_v1/corrective-release-tracking-no-shadow-1.3.3.yaml` 已完成真实 `full`：Git 预提交、ClickHouse 健康检查、前置检查、候选构建、质量门禁、候选切换、切换后检查、OpenMetadata `plan -> apply -> verify`、临时对象清理和 Git 标签均通过。
- `DWD_抖店订单物流快递单号粒度影子表`（`dwd_trade_order_logistics_tracking_no_shadow_1_3_3`）当前 41,140 行、复合键 41,140 个、空快递单号 0；目标粒度为 `店铺ID(shop_id) + 店铺订单号(shop_order_id) + 快递单号(tracking_no)`，包裹ID未作为字段或目标粒度，候选表和旧表已清理。
- OpenMetadata 已回读 18 个字段和 17 个表级自定义属性；中文表名、粒度、金额单位策略、清洗契约版本和数据质量状态已登记。
- 本地 Git 已形成发布提交 `3c1e3d9`、标签 `warehouse/doudian-order-tracking-shadow-corrective-1.3.3` 和流程修复提交 `7500650`；当前工作区仍有前次工具台、旧失败尝试和其他未分类改动，发布器未将其混入本次提交。当前本地 `main` 领先本地 `origin/main`，具体差异以实时 Git 检查为准，远程 GitHub 尚未确认同步。
- 当前正式订单主单、商品明细 DWD 未被本次物流影子发布替换；物流快递单号影子结果仍需用户审阅后，才能创建新的正式 DWD 晋级发布。

## 27. 发布后资源复核 2026-07-24

- 2026-07-24 15:50 的真实纠正影子发布报告仍为 `succeeded`，ClickHouse 全阶段质量、候选切换、切换后检查和清理均通过；目标表当时回读为 41,140 行、复合键唯一、快递单号空值 0。
- 2026-07-24 16:04 的补充只读复查无法连接本机 ClickHouse 8123；`wsl --list --verbose` 显示当前没有可用 Ubuntu-24.04 发行版，本机也未发现 ClickHouse 进程或 8123/9000 监听端口。
- 该断联发生在发布成功之后，未执行任何回滚或删除动作；当前状态为“发布结果已完成、运行资源当前不可达、待恢复后补做只读回读”，不能汇报为当前服务健康。
- 16:09 通过 Windows 回退资源检查和 ClickHouse 只读 SQL 复核，服务已恢复；目标表 41,140 行、复合键 41,140 个、候选/旧表不存在，当前不再处于不可达状态。
