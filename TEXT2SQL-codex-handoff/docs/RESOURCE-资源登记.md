# 资源登记与最近状态

## 2026-07-26 11:17 +08:00 DWD 清理发布前资源复核

- ClickHouse 测试库(youmei_sandbox)：2026-07-26 10:54 通过 `check-resource.cmd clickhouse-local` 确认 HTTP 200；11:04 的只读 DWD 盘点继续确认 ClickHouse 版本 `26.6.1.1193`，当前 `dwd_` 对象为 13 张。
- OpenMetadata：2026-07-26 10:54 通过 `check-resource.cmd openmetadata-local` 复核失败，`127.0.0.1:8585` 连接被拒绝；因此本轮清理发布只能停在 OpenMetadata 只读计划门禁之前，未删除 ClickHouse 对象。
- GitHub `HIVEQLGUY/TEXT2SQL`：2026-07-26 10:54 只读远程校验失败；本地 Git 仍可用，正式发布的远程同步状态不能据此汇报为完成。

## 2026-07-23 17:00 +08:00 资源确认补充

- ClickHouse 测试库(youmei_sandbox)：2026-07-24 15:50 的纠正影子发布已通过 ClickHouse 全阶段质量、切换和回读；16:04 曾短暂连接拒绝，16:09 已通过 Windows 回退资源入口和只读 SQL 恢复确认。
- 本次 `check-resource.cmd clickhouse-local` 触发脚本路径编码异常，未作为成功校验记录；后续需要修复该资源别名脚本。OpenMetadata 资源别名(openmetadata-local)在 2026-07-23 16:58 +08:00 已通过统一入口登录校验，版本 `1.12.11`。
- 上述旧记录中的物流包裹正式表已被后续粒度规则撤回；当前表清单以本文件最新 DWD 复核和 `STATE-CURRENT.md` 为准。
更新时间：2026-07-26 12:06 +08:00

本文件是当前唯一资源状态入口。每一次资源查询都代表一次新的状态确认，查询后必须更新本文件的“最近确认时间、最近状态、确认方式、备注”。

## 凭据统一入口

账号、密码、Token、Cookie、私钥等敏感凭据统一保存在本机：

```text
C:\Users\24796\Documents\TEXT2SQL\local\credentials\
```

当前统一凭据说明文件：

```text
C:\Users\24796\Documents\TEXT2SQL\local\credentials\README-凭据统一管理.md
```

机器可读资源映射：

```text
C:\Users\24796\Documents\TEXT2SQL\local\credentials\resources.json
```

统一校验入口：

```text
C:\Users\24796\Documents\TEXT2SQL\check-resource.cmd --list
C:\Users\24796\Documents\TEXT2SQL\check-resource.cmd --all
C:\Users\24796\Documents\TEXT2SQL\check-resource.cmd <资源别名>
```

资源登记表只记录凭据位置、最近校验时间、校验方式和校验状态，不记录密码正文。后续新增平台账号、API 资质、数据库账号、网页登录态或校验结果，都必须同步维护本节和对应资源行。

## 当前有效资源

| 资源 | 当前用途 | 地址/入口 | 最近确认时间 | 最近状态 | 确认方式 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| ClickHouse 测试库 | 当前数仓可行性测试与建模验证 | `youmei_sandbox`，本机 `127.0.0.1:8123/9000` | 2026-07-26 11:31 +08:00 | HTTP 200 可访问，耗时 0.04s | GET `http://127.0.0.1:8123/ping` | 当前 ClickHouse 建模验证默认入口。 |
| DBeaver Community | Windows 桌面 ClickHouse 查询工具 | `C:\Users\24796\AppData\Local\DBeaver\dbeaver.exe`；预配置连接 `ClickHouse 测试库(youmei_sandbox)` | 2026-07-24 17:38 +08:00 | 已安装并已打开；DBeaver 工作区已写入 ClickHouse 连接；ClickHouse `/ping` 返回 `Ok.` | 安装 DBeaver Community 26.1.3；写入 `%APPDATA%\DBeaverData\workspace6\General\.dbeaver\data-sources.json`；HTTP 健康检查 `127.0.0.1:8123/ping` | 连接参数：`jdbc:clickhouse://127.0.0.1:8123/youmei_sandbox`，用户 `default`，密码为空；首次连接如提示下载 ClickHouse JDBC 驱动，按 DBeaver 提示下载。 |
| ClickHouse 外部工具代理 | 供外部工具/魔方访问本机 ClickHouse | `120.26.202.216:28123` | 2026-07-22 09:41 +08:00 | 代理通道可用 | WSL 内启动 `clickhouse_tool_tunnel.sh supervise`；`clickhouse_tool_tunnel.sh status` 返回 healthy：`root@120.26.202.216 127.0.0.1:18123 -> local 127.0.0.1:8123` | 本机直连 `/ping` 超时符合白名单设计，公网入口主要给魔方出口 IP 使用；该通道为轻量 SSH 反向通道，不启动 OpenMetadata/Superset/DolphinScheduler。 |
| 工具服务器 | ClickHouse 公网代理承载机 | `120.26.202.216` | 2026-07-26 11:31 +08:00 | 不可用/待处理：未找到可用 SSH 私钥候选 | 检查 key_candidates 文件是否存在 | ClickHouse 公网代理/隧道承载机；使用本机 SSH 私钥做 BatchMode 登录验证。 |
| 预策/魔方源库 `cubeappdata` | 抖店订单基础表等预策侧源表的只读候选来源 | `127.0.0.1:19030`，默认库 `cubeappdata`，用户 `ro1` | 2026-07-26 11:31 +08:00 | 登录成功；当前用户 `'ro1'@'%'`，版本 `5.1.0`，`cubeappdata` 表数量 `995` | Windows Python 读取 `local/credentials/sr.env` 的 `SR_*` 并通过本机隧道执行只读查询 | 凭据映射：`local/credentials/sr.env` / `SR_*`；`120.26.202.216:9030` 不作为本机登录入口。 |
| 阿里云生产 ECS | 历史生产/公网资源与备份管理入口 | `114.55.148.140` | 2026-07-26 11:31 +08:00 | 不可用/待处理：未找到可用 SSH 私钥候选 | 检查 key_candidates 文件是否存在 | 使用本机 SSH 私钥做 BatchMode 登录验证；不会展示私钥内容。 |
| 旧 RDS `youmei_ai` | 历史业务源/RDS 资源，当前不作为未来默认链路 | `rm-bp1mx4778wjne596xko.mysql.rds.aliyuncs.com:3306` | 2026-07-26 11:31 +08:00 | 不可用/待处理：校验失败：(2003, "Can't connect to MySQL server on 'rm-bp1mx4778wjne596xko.mysql.rds.aliyuncs.com' ([WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试。)") | mysql_env 校验 | 凭据映射：`local/credentials/project.env` / `META_DB_*`；历史业务源/RDS 资源；当前不作为未来默认链路，但可用统一脚本做只读登录验证。 |
| Superset | BI 服务保留 | `http://127.0.0.1:8088` | 2026-07-26 11:31 +08:00 | 不可用/待处理：校验失败：<urlopen error [WinError 10061] 由于目标计算机积极拒绝，无法连接。> | http 校验 | BI 服务保留；仅验证 HTTP 可访问，不打印管理员密码。 |
| DolphinScheduler | 调度服务保留 | `http://127.0.0.1:12345/dolphinscheduler/ui/` | 2026-07-26 11:31 +08:00 | 不可用/待处理：校验失败：<urlopen error [WinError 10061] 由于目标计算机积极拒绝，无法连接。> | http 校验 | 调度服务保留；仅验证 UI 可访问。 |
| OpenMetadata | ClickHouse 数仓表、字段和清洗契约元数据登记 | `127.0.0.1:8585/8586` | 2026-07-26 12:06 +08:00 | 登录成功，版本 `1.12.11`，耗时 0.56s | 读取 `local/credentials/openmetadata.env` 的 `OPENMETADATA_*` 并调用 OpenMetadata 登录和版本接口 | ClickHouse 数仓表、字段和清洗契约元数据登记。 |
| OpenMetadata 到 ClickHouse bridge | OpenMetadata 访问本机 ClickHouse 的桥接 | `172.16.240.1:18124` | 2026-07-19 15:51 +08:00 | 可用 | `/ping` 返回 `Ok.` | 仅服务本机 Docker/WSL 内部链路 |
| 历史接口接入留存包 | 旧 API ingestion 代码、契约、SDK bridge、隐性经验留存 | `C:\Users\24796\Desktop\youmei-api-ingestion-archive-20260719.zip` | 2026-07-19 15:51 +08:00 | 文件存在 | 文件大小 995,237 bytes | 仅供历史参考，不代表当前架构继续推进 |
| GitHub `HIVEQLGUY/TEXT2SQL` | 数仓 SQL、清洗契约、发布报告和版本记录的 Git 权威来源 | `https://github.com/HIVEQLGUY/TEXT2SQL.git` | 2026-07-26 12:06 +08:00 | 不可用/待处理：Git 远程访问失败（凭据或网络校验未通过） | Git 只读检查 `https://github.com/HIVEQLGUY/TEXT2SQL.git` 的远程分支 | Git 版本源；只读校验远程分支可访问性，不记录密码或 Token。 |

## 已下线的本机历史组件

| 组件 | 最近确认时间 | 最近状态 |
| --- | --- | --- |
| Doris `8030/9030` | 2026-07-19 15:45 +08:00 | 容器、镜像、数据目录已删除，端口关闭 |
| CH-UI `3488` | 2026-07-24 17:20 +08:00 | 已按用户要求删除：容器 `youmei-ch-ui`、镜像 `ghcr.io/caioricciuti/ch-ui:latest`、项目目录 `tools/ch-ui` 已删除；Docker 卷 `ch-ui_ch-ui-data` 因 Docker 元数据坏引用残留，不能作为服务可用证据。 |
| DataAgent API `8877` | 2026-07-19 15:45 +08:00 | 旧进程停止，端口关闭 |
| DataX-Web `9528/19528/9504/9999` | 2026-07-19 15:45 +08:00 | 旧容器、镜像、代理进程、目录已删除，端口关闭 |
| SeaTunnel 接入调度 | 2026-07-19 15:45 +08:00 | 旧容器、镜像、目录已删除 |

## 敏感信息规则

- 不在本文档写真实密码、Token、Cookie、私钥正文。
- 如果未来恢复某个资源的真实账号，应记录“凭据保存在何处”，不记录凭据值。
- 已释放资源删除连接地址，避免后续误连或误判。

## 本地凭据恢复记录

2026-07-19 17:05 +08:00：已从回收站备份包 `TEXT2SQL-codex-handoff.zip` 恢复以下凭据/账号相关文件到项目原路径：`.env`、`.env.reader`、`local/SECRETS-实际账号.md`、`local/tmp_remote_patch_doris_service_password.py`、`config/database.example.env`、`config/datax-sync.example.env`。恢复过程未打印密码正文；后续每个资源仍需按访问动作单独验证状态。

2026-07-19 17:20 +08:00：已建立统一凭据目录 `C:\Users\24796\Documents\TEXT2SQL\local\credentials\`，并复制恢复文件为 `SECRETS-统一凭据.md`、`project.env`、`reader.env`、`tmp_remote_patch_doris_service_password.py`。旧路径保留用于兼容，不作为后续新增凭据的分散入口。

2026-07-19 18:05 +08:00：已建立一键资源校验入口 `check-resource.cmd` 与机器可读资源映射 `local/credentials/resources.json`。当前默认启用资源 `old-rds-youmei-ai`、`yuce-cubeappdata`、`clickhouse-local`、`superset-local`、`dolphinscheduler-local`、`aliyun-ecs-prod`、`tool-server` 全量校验通过；校验结果已自动写回本资源登记表。

2026-07-23：完成 Git/GitHub 资源状态确认。本机 Git 可执行文件为 `C:\Users\24796\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe`，版本 `2.53.0.windows.3`；Git Credential Manager 版本文件信息为 `2.7.3`，全局凭据助手为 `manager`。当前项目已初始化本地 Git 仓库，但尚未配置远程 URL、提交作者信息和可用 GitHub 凭据。GitHub 连接器查询因传输层失败未完成；已打开 GitHub 登录页面，待用户完成交互式登录后再次验证。

2026-07-24：GitHub 登录已确认。GitHub 账号为 `HIVEQLGUY`，已确认绑定邮箱；本地项目提交身份已配置，远程 `origin` 已绑定 `https://github.com/HIVEQLGUY/TEXT2SQL.git`，`git ls-remote --heads origin` 只读验证通过。未执行首次提交、拉取或推送。

2026-07-24 14:35：复查 Git 版本链路。本地已有基线提交 `f007765`，缓存的 `origin/main` 为 `62f0a7f`，本地领先 1 个提交；实时远程检查因 `github.com:443` 网络连接失败，未确认远程已接收基线，也未执行推送。
