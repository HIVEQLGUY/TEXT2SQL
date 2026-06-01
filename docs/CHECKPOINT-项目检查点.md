# 项目检查点

本文件是固定检查点，不按会话新建。每次阶段性推进、资源变化、架构决策、风险发现，都更新这里。

## 使用规则

- 新会话接手时必须先读 `docs/HANDOFF-新会话接续说明.md`，再读本文件。
- 不要为每次对话新建单独交接文件。
- 重要信息只更新固定文件：
  - 资源索引：`docs/RESOURCE-资源登记.md`
  - 本地真实密钥：`local/SECRETS-实际账号.md`
  - 项目检查点：`docs/CHECKPOINT-项目检查点.md`
  - 长期沟通摘要：`docs/CHAT-沟通记录摘要.md`
  - 当前接续入口：`docs/HANDOFF-新会话接续说明.md`

## 检查点模板

```text
日期：
类型：资源 / 架构 / 开发 / 部署 / 风险 / 决策
摘要：
影响：
后续动作：
关联文件：
```

## 2026-05-31 资源记录机制

类型：决策

摘要：

- Git 不保存真实账号密码，但必须保存资源索引和凭证位置。
- 本地固定使用 `local/SECRETS-实际账号.md` 记录真实服务器、数据库、钉钉、大模型等敏感信息。
- `local/` 加入 `.gitignore`，只保存在本机。
- Git 固定使用 `docs/RESOURCE-资源登记.md` 记录资源登记、访问方式、账号用途和密钥文件位置。
- 后续开发途中重要信息默认更新固定记录文件，不再每次对话生成新的资源说明文件。

影响：

- 新会话可以从固定入口恢复上下文。
- 本地真实密码不进入 Git，但不会只存在聊天记录里。
- 后续若资源变化，需要同时更新资源登记和本地密钥文件。

后续动作：

- 用户重新提供新数据库和云服务器信息。
- Codex 更新 `local/SECRETS-实际账号.md` 的真实值。
- Codex 更新 `docs/RESOURCE-资源登记.md` 的脱敏资源索引。
- 完成连通性测试后，在本文件追加测试结果检查点。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`

## 2026-06-01 RDS 新账号连接成功

类型：测试

摘要：

- 本地密钥文件已更新为新账号 `chat_ai_duckdb_2`。
- 从云服务器 `114.55.148.140` 使用新账号连接 RDS `rm-2zea6b6dcxxq17753zo.mysql.rds.aliyuncs.com:3306` 成功。
- 连接库：`chatsql_ai`。
- 执行 `SELECT 1` 返回 `1`。
- MySQL 客户端需要加 `--get-server-public-key` 以支持 `caching_sha2_password` 非 SSL 认证。
- 尝试 `--ssl-mode=REQUIRED` 时，RDS 返回服务端不支持 SSL。

影响：

- 云服务器 SSH 和 RDS 连接链路已打通。
- 第一阶段资源确认中，数据库连接已可作为 M1/M2 后续开发依据。
- 后续应用配置需支持 MySQL `caching_sha2_password`，Python 驱动连接时可能需要等价参数，例如允许获取服务端公钥或改用兼容认证插件。

后续动作：

- 更新后续 `.env` 或正式配置模板时使用 `chat_ai_duckdb_2`。
- 进入 M1 前仍需确认该账号权限边界：是否只读、是否能建/写元数据库表。如果这是问数执行账号，应保持只读；元数据写入应另建应用写账号。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `docs/PLAN-第一阶段落地方案.md`

## 2026-06-01 M1 工程骨架启动

类型：开发

摘要：

- 正式代码从干净的根目录 `app/` 开始搭建，不复用旧原型目录。
- 新增 FastAPI 应用入口 `app/api/main.py`。
- 新增健康检查路由 `GET /api/health` 和准备检查 `GET /api/ready`。
- 新增标准库配置加载 `app/core/config.py`，支持 `META_DB_*`、`DW_DB_*` 和兼容旧 `DB_*`。
- 新增 request_id 上下文 `app/core/request_context.py`。
- 新增标准库日志配置 `app/core/logging.py`，日志格式包含 `request_id`。
- 迁移旧原型 SQL 审查思想到正式服务位置 `app/services/sql_safety_service.py`。
- 新增 `pyproject.toml` 声明 FastAPI、Uvicorn 和 PyMySQL 依赖。
- 新增 `.env.example`，并清理 `config/database.example.env` 中旧 RDS 示例。

本地配置：

- `.env` 已根据 `local/SECRETS-实际账号.md` 更新为新 RDS。
- `.env.reader` 已根据新 RDS 更新。
- `.env.admin` 已删除，避免旧 RDS 管理账号误导。
- 当前新 RDS 账号：`chat_ai_duckdb_2`。
- 当前本地配置开启 MySQL 服务端公钥获取参数：`*_MYSQL_GET_SERVER_PUBLIC_KEY=true`。

验证：

- `python -m compileall app` 通过。
- `app.core.config.get_settings()` 可读取新 RDS 配置，缺失项为空。
- SQL 审查服务基础导入与阻断验证通过。

影响：

- M1 的工程骨架、配置加载和 request_id 日志基础已开始落地。
- 本机尚未安装 FastAPI/Uvicorn/PyMySQL，因此还未启动实际 API 服务。

后续动作：

- 安装项目依赖或建立虚拟环境。
- 增加数据库连接客户端/Repository 层，注意 PyMySQL 需要支持 `caching_sha2_password` 获取服务端公钥。
- 确认 `chat_ai_duckdb_2` 权限边界，决定是否另建 `meta_app` 写账号。

关联文件：

- `pyproject.toml`
- `.env.example`
- `config/database.example.env`
- `app/api/main.py`
- `app/api/routers/health.py`
- `app/core/config.py`
- `app/core/logging.py`
- `app/core/request_context.py`
- `app/services/sql_safety_service.py`

## 2026-06-01 M1 本地 API 与数据库健康检查通过

类型：开发 / 测试

摘要：

- 已创建本地虚拟环境 `.venv/`，并加入 `.gitignore`。
- 已安装项目依赖：FastAPI、Uvicorn、PyMySQL 等。
- 修复 `pyproject.toml` 包发现配置，只打包 `app*`，避免把 `web/`、`local/`、`legacy/` 等目录当成 Python 包。
- 新增 MySQL 客户端 `app/clients/mysql.py`。
- 新增数据库健康检查接口 `GET /api/health/db`。
- PyMySQL 已能直连阿里云 RDS，支持当前账号的 `caching_sha2_password` 认证。
- 本地 Uvicorn 已启动：`http://127.0.0.1:8000`。

验证：

- `python -m compileall app` 通过。
- `GET /api/health` 返回 `ok=true`，并返回脱敏后的元数据库和数仓库配置。
- `GET /api/ready` 返回 `ok=true`，配置缺失项为空。
- `GET /api/health/db` 返回 `ok=true`，`metadata_db` 和 `warehouse_db` 均连接成功。
- RDS 返回版本：MySQL `8.0.36`。
- 当前用户：`chat_ai_duckdb_2@%`。

运行方式：

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

当前后台进程：

- PID 记录在 `.runtime/uvicorn.pid`。
- 日志记录在 `.runtime/uvicorn.err.log` 和 `.runtime/uvicorn.out.log`。

影响：

- M1 的 FastAPI 骨架、配置加载、request_id、健康检查和 RDS 连接已跑通。
- 后续可以进入 M2 元数据库表结构与 Repository。

后续动作：

- 确认 `chat_ai_duckdb_2` 是否允许写入元数据库表。
- 若它应作为问数只读账号，建议另建 `meta_app` 写账号。
- 设计并初始化 `meta_table`、`meta_field`、`meta_field_dependency`、`query_run`、`query_step` 等表。

关联文件：

- `.gitignore`
- `pyproject.toml`
- `app/clients/mysql.py`
- `app/api/routers/health.py`
- `app/core/config.py`
- `.runtime/uvicorn.pid`

## 2026-06-01 元数据库改用旧 RDS

类型：资源 / 决策

摘要：

- 用户说明旧 RDS 可作为元数据库。
- 新 RDS `chatsql_ai` 是高读写 DB，更适合作为问数执行数据库。
- 当前测试流程阶段暂不强制只读账号；后续健壮性和安全收敛阶段再重新配置账号。
- 旧 RDS 连接信息来自历史配置：`rm-bp1mx4778wjne596xko.mysql.rds.aliyuncs.com:3306/youmei_ai`，用户 `baoyan`。
- Codex 使用当前已知密码从云服务器端连接旧 RDS 并执行 `SELECT 1` 成功。

影响：

- `META_DB_*` 应指向旧 RDS。
- `DW_DB_*` 应指向新 RDS。
- M2 元数据库表结构应建在旧 RDS `youmei_ai` 中。
- 新 RDS `chatsql_ai` 保持为问数执行数据库。

后续动作：

- 更新本地 `local/SECRETS-实际账号.md` 和 `.env`。
- 复测本地 FastAPI `GET /api/health/db` 是否两组 DB 都通过。
- 进入 M2 元数据库表结构设计和初始化。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `.env`

## 2026-06-01 本地 API 双库配置验证通过

类型：资源 / 测试

摘要：

- 本地 `local/SECRETS-实际账号.md` 已更新：
  - 元数据库：旧 RDS `youmei_ai`，用户 `baoyan`。
  - 问数执行数据库：新 RDS `chatsql_ai`，用户 `chat_ai_duckdb_2`。
- 本地 `.env` 已更新：
  - `META_DB_*` 指向旧 RDS。
  - `DW_DB_*` 指向新 RDS。
  - 兼容旧原型的 `DB_*` 指向新 RDS。
- 本地 `.env.reader` 指向新 RDS。
- 已重启 Uvicorn。
- `GET /api/health/db` 验证通过：
  - `metadata_db.database_name = youmei_ai`
  - `metadata_db.current_user = baoyan@%`
  - `warehouse_db.database_name = chatsql_ai`
  - `warehouse_db.current_user = chat_ai_duckdb_2@%`

影响：

- 本地 API 已按“旧 RDS 元数据库 + 新 RDS 问数执行库”运行。
- 下一步可以在旧 RDS `youmei_ai` 中推进 M2 元数据库表结构。

后续动作：

- 设计 M2 表结构。
- 建初始化脚本和 Repository。
- 当前测试阶段新 RDS 不强制只读账号；后续安全收敛再配置。

关联文件：

- `docs/NEXT-AI-切换API接续包.md`
- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `.env`

## 2026-06-01 钉钉同步职责调整

类型：决策 / 架构

摘要：

- 用户确认：钉钉上维护的数仓元数据已经可以通过用户自己的工具定期写入元数据库。
- 因此项目内原计划 M3“接入钉钉开放平台并同步表/字段元数据”不再需要作为主要开发任务。
- 本项目应把元数据库视为已由外部工具供数的上游，优先读取和适配已有元数据表结构。
- 后续“同步”相关工作应转为元数据库到 ES/OpenSearch/向量库的索引刷新，而不是钉钉 API 接入。

影响：

- M2 从“从零设计并创建元数据库表”调整为“发现现有元数据表结构、字段映射和 Repository”。
- 原 M3 改为“元数据索引刷新/检索索引构建”。
- 不要重复实现钉钉同步链路，避免和用户已有工具职责重叠。

后续动作：

- 读取旧 RDS `youmei_ai` 中现有表清单和字段结构。
- 识别哪些表是用户工具写入的数仓元数据表。
- 基于现有表结构建立 Repository 和 API。
- 如果字段名与项目标准模型不同，优先做适配层。

关联文件：

- `docs/NEXT-AI-切换API接续包.md`
- `docs/PLAN-第一阶段落地方案.md`
- `docs/RESOURCE-资源登记.md`

## 2026-06-01 元数据字典表初步探查

类型：资源 / 分析

摘要：

- 用户确认数仓元数据已经由自己的工具写入元数据库。
- 当前核心元数据表为两张：
  - `table_dictionary`：数仓字典 / 表字典。
  - `metric_dictionary`：指标字典 / 字段指标字典。
- 元数据库 `youmei_ai` 当前表：
  - `table_dictionary`：41 行。
  - `metric_dictionary`：1394 行。
  - `dws_tmall_sales_link_summary`：约 549633 行，看起来像旧/示例数据表，不是当前核心元数据字典。
- 问数执行库 `chatsql_ai` 当前测试表：
  - `dws_douyin_spu_sales_detail`：约 87579 行，表结构已存在。

字段理解：

- `table_dictionary.bywm`：表英文名。
- `table_dictionary.bzwm`：表中文名。
- `table_dictionary.bhzd`：包含字段，当前表现为逗号分隔内部标识。
- `metric_dictionary.zdywmc`：字段英文名称。
- `metric_dictionary.zdzwmc`：字段中文名称。
- `metric_dictionary.ssscb`：注释为“所属数仓表”，但当前值表现为内部标识。
- `metric_dictionary.jsgs`：计算公式。
- `metric_dictionary.ywdy`：业务定义。
- `metric_dictionary.syzysx`：使用注意事项。

关键发现：

- 尝试 `metric_dictionary.ssscb = table_dictionary.bywm`，匹配数为 0。
- 尝试 `FIND_IN_SET(metric_dictionary.ssscb, table_dictionary.bhzd)`，匹配数为 0。
- 因此两张字典可以作为召回基础，但真实关联键尚未确认。

影响：

- M2 应先做“现有表结构适配和关联键确认”，而不是从零设计新元数据表。
- 在关联键确认前，可以先做表字典和指标字典的独立关键词召回。
- SQL 生成需要可靠地从指标/字段定位到实际执行表，因此关联键是 M2 的第一优先级。

后续动作：

- 请用户确认 `metric_dictionary.ssscb` 应该关联 `table_dictionary` 的哪一列，或是否存在未导入的 ID 映射字段。
- 如果现有结构无法稳定关联，建议在上游工具中补充稳定字段，例如 `table_name` 或 `table_id`。
- 建立 Repository 时先保留适配层，不直接绑定死字段名。

关联文件：

- `docs/NEXT-AI-切换API接续包.md`
- `docs/RESOURCE-资源登记.md`
- `app/clients/mysql.py`

## 2026-06-01 RDS 新账号

类型：资源

摘要：

- 用户已新创建 RDS 数据库账号：`chat_ai_duckdb_2`。
- 密码不变，仍使用本地 `local/SECRETS-实际账号.md` 已记录值。
- 后续连接 `chatsql_ai` 改用 `chat_ai_duckdb_2`。

后续动作：

- 更新本地密钥文件中的应用账号和只读账号。
- 从云服务器端使用 `chat_ai_duckdb_2` 复测 RDS 登录和 `SELECT 1`。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `.gitignore`

## 2026-05-31 新服务器与 RDS 资源登记

类型：资源

摘要：

- 用户提供新的云服务器公网 IP：`114.55.148.140`，SSH 用户：`root`。
- 登录方式改为 Codex 生成 SSH 公钥，由用户配置到阿里云实例。
- Codex 已生成专用 SSH key，私钥路径：`local/ssh/text2sql_codex_ed25519`。
- 用户提供新的阿里云 RDS MySQL 外网地址、库名和账号，真实密码已记录到本地密钥文件。
- 数据库连接策略：先登录云服务器，再从服务器端测试 RDS 连接。

影响：

- 当前资源确认进入“待 SSH 公钥配置、待连通性测试”状态。
- 旧 `.env`、`.env.admin`、`.env.reader` 仍指向旧 RDS，不再作为新资源依据。

后续动作：

- 用户将 `local/ssh/text2sql_codex_ed25519.pub` 的内容配置到云服务器 `root` 用户授权密钥。
- Codex 使用沙箱外 SSH 测试登录 `root@114.55.148.140`。
- SSH 登录成功后，从服务器端测试 RDS `rm-2zea6b6dcxxq17753zo.mysql.rds.aliyuncs.com:3306` 连接。
- 测试结果继续追加到本检查点文件。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `local/ssh/text2sql_codex_ed25519`
- `local/ssh/text2sql_codex_ed25519.pub`

## 2026-06-01 SSH v2 key 重新绑定

类型：资源 / 风险

摘要：

- 第一版 SSH key 由沙箱用户生成，沙箱外 `ssh` 无法读取私钥，登录测试失败在本地私钥权限阶段。
- Codex 使用沙箱外 Windows 用户重新生成 v2 key。
- v2 私钥路径：`local/ssh/text2sql_codex_ed25519_v2`。
- v2 公钥路径：`local/ssh/text2sql_codex_ed25519_v2.pub`。
- 用户已重新绑定 v2 公钥到云服务器。
- 旧 key `text2sql_codex_ed25519` 应作废，避免后续会话误用。

影响：

- 后续 SSH 登录必须使用 v2 私钥。
- Git 资源登记和本地密钥文件需要同步指向 v2。
- 切换 API 或新会话恢复时，应按 `docs/MEMORY-重要信息记录规范.md` 和 `docs/HANDOFF-新会话接续说明.md` 的固定路径读取，不依赖聊天历史。

后续动作：

- 删除本地旧 key 文件。
- 使用 v2 私钥测试 `root@114.55.148.140`。
- SSH 成功后，从服务器端测试 RDS 连接。
- 测试结论继续追加到本检查点。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `docs/MEMORY-重要信息记录规范.md`
- `docs/HANDOFF-新会话接续说明.md`
- `local/SECRETS-实际账号.md`
- `local/ssh/text2sql_codex_ed25519_v2`
- `local/ssh/text2sql_codex_ed25519_v2.pub`

## 2026-06-01 SSH 与 RDS 连通性测试

类型：资源 / 测试 / 阻塞

摘要：

- 使用 v2 私钥成功登录 `root@114.55.148.140`。
- 服务器主机名：`iZbp13rcbr61o2rxnxa8rzZ`。
- 服务器系统：Linux `6.8.0-111-generic x86_64`。
- 从服务器端测试 RDS `rm-2zea6b6dcxxq17753zo.mysql.rds.aliyuncs.com:3306`，TCP 连接成功。
- 服务器已安装 MySQL 客户端：MySQL 8.0.45。
- 使用账号 `chat_ai_duckdb_1` 连接库 `chatsql_ai` 执行 `SELECT 1` 时失败：`Access denied for user 'chat_ai_duckdb_1'@'114.55.148.140'`。

影响：

- 云服务器 SSH 通道已经可用。
- RDS 网络路径已经可用。
- 当前阻塞点不在网络，而在 MySQL 账号密码或账号 host 授权。

后续动作：

- 确认 `chat_ai_duckdb_1` 密码是否正确。
- 在 RDS 控制台或管理员账号中确认该账号是否允许从 `114.55.148.140` 登录。
- 如果账号 host 受限，需要授权服务器公网 IP 或合适的来源范围。
- 认证修复后重新执行服务器端 `SELECT 1` 测试。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
- `local/ssh/text2sql_codex_ed25519_v2`

## 2026-06-01 RDS 认证复测

类型：测试 / 阻塞

摘要：

- 用户确认 RDS 白名单已加入服务器公网 IP `114.55.148.140`。
- 用户确认数据库密码仍为本地 `local/SECRETS-实际账号.md` 已记录值。
- Codex 从云服务器端再次测试 `chat_ai_duckdb_1` 登录 `chatsql_ai`，仍返回 `Access denied for user 'chat_ai_duckdb_1'@'114.55.148.140'`。
- Codex 额外排除了 Windows PowerShell 管道传输密码时尾部 `CRLF` 造成密码多一个回车字符的可能。

影响：

- 网络、白名单和端口可达性不是当前阻塞点。
- 当前阻塞点仍在 MySQL 认证/授权层。

后续动作：

- 在阿里云 RDS 控制台确认账号 `chat_ai_duckdb_1` 是否启用、密码是否刚重置生效。
- 确认该账号是否有访问库 `chatsql_ai` 的权限。
- 如 RDS 控制台支持账号授权来源，确认允许 `114.55.148.140` 或合适来源。
- 可临时重置该账号密码后同步更新 `local/SECRETS-实际账号.md`，再复测。

关联文件：

- `docs/RESOURCE-资源登记.md`
- `local/SECRETS-实际账号.md`
