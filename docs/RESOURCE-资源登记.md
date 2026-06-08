# 资源登记

本文件是项目固定资源索引，允许提交到 Git。这里只记录资源位置、用途、账号类型和本地密钥保存位置，不记录真实密码、Token、私钥正文。

真实账号密码固定记录在本地文件：

```text
local/SECRETS-实际账号.md
```

`local/` 已加入 `.gitignore`，不会提交到 Git。

## 1. 云服务器

状态：SSH v2 key 登录成功。

| 项目 | 内容 |
| --- | --- |
| 公网 IP | `114.55.148.140` |
| 内网 IP | 待填写 |
| 云厂商 / 区域 | 阿里云，区域待确认 |
| 操作系统 | 待填写 |
| CPU / 内存 / 磁盘 | 待填写 |
| SSH 用户 | `root` |
| 登录方式 | SSH 公钥，私钥见 `local/ssh/text2sql_codex_ed25519_v2` |
| sudo/root 权限 | root |
| Docker 是否允许安装 | 待确认 |
| 防火墙 / 安全组 | 待确认 |

说明：

- 服务器管理入口默认不直接暴露调试面板公网访问。
- Qdrant Dashboard、Kibana、Embedding docs 等管理入口优先通过内网、VPN 或 SSH 隧道访问。

## 2. 元数据库

状态：改用旧 RDS 作为元数据库；服务器端使用 `baoyan` 已通过 `SELECT 1` 测试。

| 项目 | 内容 |
| --- | --- |
| 数据库类型 | 阿里云 RDS MySQL |
| host | `rm-bp1mx4778wjne596xko.mysql.rds.aliyuncs.com` |
| port | `3306` |
| database / schema | `youmei_ai` |
| 网络访问方式 | 已从云服务器端测试 |
| 管理员账号 | `baoyan`，密码见本地密钥文件 |
| 应用账号 | 待创建，建议 `meta_app` |
| 只读账号 | 待创建，建议 `meta_readonly` |
| 密钥保存位置 | `local/SECRETS-实际账号.md` |

账号原则：

- 管理员账号只用于初始化、建库、授权、迁移和排障。
- 应用账号用于读写项目元数据。
- 问数执行 SQL 默认使用只读账号。

## 3. 问数执行数据库

状态：新 RDS 作为高读写问数执行数据库，当前用于测试流程，不强制只读账号。

| 项目 | 内容 |
| --- | --- |
| 数据库类型 | 阿里云 RDS MySQL |
| host | `rm-2zea6b6dcxxq17753zo.mysql.rds.aliyuncs.com` |
| port | `3306` |
| database / schema | `chatsql_ai` |
| 第一批表清单 | 待填写 |
| 当前测试账号 | `chat_ai_duckdb_2`，密码见本地密钥文件 |
| 是否需要白名单 | 已加入服务器公网 IP |
| 分区字段 / 大表限制 | 待确认 |

说明：

- 用户说明该新 RDS 是高读写 DB，适合作为问数执行数据库。
- 当前阶段为了测试流程，暂不强制单独创建只读账号。
- 后续进入健壮性和安全收敛阶段时，再配置只读执行账号。

## 3.1 抖音主题域数据源

状态：尚未接入元数据表，等元数据库连接稳定后再导入/接入。

## 4. 钉钉 AI 表格

状态：待确认。

| 项目 | 内容 |
| --- | --- |
| 开放平台应用类型 | 待填写 |
| app_key | 可脱敏填写 |
| app_secret | 真实值见本地密钥文件 |
| AI 表格 / 多维表格标识 | 待填写 |
| 表元数据 sheet/table 标识 | 待填写 |
| 字段元数据 sheet/table 标识 | 待填写 |
| 字段映射文档 | 待设计 |

## 5. 大模型服务

状态：待确认。

| 项目 | 内容 |
| --- | --- |
| 服务商 | 待填写 |
| base URL | 待填写 |
| API Key | 真实值见本地密钥文件 |
| 默认模型 | 待填写 |
| JSON/schema 输出支持 | 待确认 |
| 并发 / 速率 / 费用限制 | 待确认 |

## 6. 检索服务

状态：待确认。

| 项目 | 内容 |
| --- | --- |
| 向量检索 | Qdrant / pgvector / 其他，待确认 |
| 全文检索 | Elasticsearch / OpenSearch / 数据库全文索引，待确认 |
| Embedding 服务 | 云 API / 本地服务 / TEI，待确认 |
| Dashboard 访问方式 | 内网 / SSH 隧道，待确认 |

## 7. 当前已知本地凭证文件

以下文件存在于本地，且不会提交到 Git：

```text
.env
.env.reader
```

当前状态：

- `.env` 已更新为新 RDS，并同时包含 `META_DB_*`、`DW_DB_*` 和兼容旧原型的 `DB_*` 配置。
- `.env` 需要调整为：`META_DB_*` 指向旧 RDS 元数据库，`DW_DB_*` 指向新 RDS 问数执行数据库。
- `.env.reader` 已更新为新 RDS 问数执行数据库。
- `.env.admin` 已删除，避免旧 RDS 管理账号误导后续会话。
- 如需元数据库写账号或管理员账号，应重新创建并记录到 `local/SECRETS-实际账号.md`。
- `.venv/` 已创建并被 `.gitignore` 忽略。

## 8. SSH 公钥

云服务器当前绑定的 Codex 专用 v2 公钥文件：

```text
local/ssh/text2sql_codex_ed25519_v2.pub
```

私钥文件：

```text
local/ssh/text2sql_codex_ed25519_v2
```

私钥只保存在本地 `local/` 下，不提交 Git。

历史说明：

- 第一版 key `text2sql_codex_ed25519` 因沙箱用户创建导致沙箱外 `ssh` 无法读取，已作废并从本地清理。

## 9. 连通性测试结果

最近测试日期：2026-06-01

| 项目 | 结果 |
| --- | --- |
| SSH `root@114.55.148.140` | 成功 |
| 服务器主机名 | `iZbp13rcbr61o2rxnxa8rzZ` |
| 服务器系统 | Linux `6.8.0-111-generic x86_64` |
| 服务器到 RDS 3306 TCP | 成功 |
| 服务器 MySQL 客户端 | 已安装，MySQL 8.0.45 |
| RDS 账号登录 | 失败：`Access denied for user 'chat_ai_duckdb_1'@'114.55.148.140'` |

待确认：

- RDS 账号 `chat_ai_duckdb_1` 的密码是否正确。
- RDS 是否限制账号来源 host，需要允许 `114.55.148.140` 或 `%`。
- RDS 白名单/安全组已允许 TCP，但 MySQL 账号授权仍需检查。

补充测试：

- 2026-06-01 用户确认 RDS 白名单已加入服务器公网 IP，密码为本地已记录值。
- Codex 从服务器端复测登录仍返回 `Access denied for user 'chat_ai_duckdb_1'@'114.55.148.140'`。
- 已排除 Windows PowerShell 管道传密码时尾部 `CRLF` 导致密码多出回车字符的问题。
- 当前更可能是 RDS 账号状态、密码实际值、账号 host 授权或账号权限配置问题。

账号变更：

- 2026-06-01 用户新创建数据库账号 `chat_ai_duckdb_2`，密码不变。
- 后续 RDS 连接测试改用 `chat_ai_duckdb_2`。
- 2026-06-01 使用 `chat_ai_duckdb_2` 从云服务器端连接 `chatsql_ai` 成功，执行 `SELECT 1` 返回 `1`。
- MySQL 8 `caching_sha2_password` 连接需使用客户端参数 `--get-server-public-key`，当前 RDS 不支持 `--ssl-mode=REQUIRED`。
- 本地 `.env` 已设置 `META_DB_MYSQL_GET_SERVER_PUBLIC_KEY=true` 和 `DW_DB_MYSQL_GET_SERVER_PUBLIC_KEY=true`。
- 本地 FastAPI `GET /api/health/db` 已通过 PyMySQL 直连 RDS 验证。

## 10. 元数据库调整记录

最近调整日期：2026-06-01

- 用户决定旧 RDS 用作元数据库。
- 旧 RDS：`rm-bp1mx4778wjne596xko.mysql.rds.aliyuncs.com:3306/youmei_ai`。
- 旧 RDS 账号：`baoyan`，真实密码见 `local/SECRETS-实际账号.md`。
- Codex 从云服务器端使用旧 RDS 执行 `SELECT 1` 成功。
- 新 RDS `chatsql_ai` 继续作为问数执行数据库。
- 本地 FastAPI `GET /api/health/db` 已验证双库配置：
  - `metadata_db` -> `youmei_ai` / `baoyan@%`
  - `warehouse_db` -> `chatsql_ai` / `chat_ai_duckdb_2@%`

## 11. 元数据库字典表关联

元数据库：旧 RDS `youmei_ai`。

当前核心字典表：

```text
table_dictionary: 数仓表字典
metric_dictionary: 字段/指标字典
```

当前稳定关联键：

```text
table_dictionary.bbs = 表标识
metric_dictionary.zdbs = 字段标识
metric_dictionary.ssscb = 所属表标识
主关联：metric_dictionary.ssscb = table_dictionary.bbs
辅助校验：metric_dictionary.zdbs 可出现在 table_dictionary.bhzd 的逗号分隔字段标识列表中
```

当前样例：

```text
table_id: hKrBQ2zwwG
table_name: ud_3418004512502203_dyxsjyzhb
table_display_name: DWS_抖音_SPU销售明细
```

## 12. LLM 资源登记

用途：Text2SQL 的 LLM SQL 生成节点。

```text
provider: deepseek
base_url: https://api.deepseek.com
local model setting: DEEPSEEK
actual compatible model: 由 DeepSeek API 返回为准，当前验证返回 deepseek-v4-flash
```

注意：

- 用户提供的 `https://platform.deepseek.com/api_keys` 是控制台 API key 页面，不是调用 API 的 base URL。
- OpenAI-compatible 调用地址使用 `https://api.deepseek.com`。
- 代码中会将本地 `LLM_MODEL=DEEPSEEK` 别名映射为官方当前模型 `deepseek-v4-flash`。
- 真实 API key 只记录在本地 `.env` 和 `local/SECRETS-实际账号.md`，不提交 Git。
