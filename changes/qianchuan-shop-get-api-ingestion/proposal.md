# 巨量千川店铺账户接口接入

## 背景

接入巨量千川开放平台 `/qianchuan/shop/get/`，先落到 Doris CONNECT/ODS 层，不直接进入 DWD/DIM/DWS/ADS。

## 范围

- 官方文档、权限点、后台授权和频控确认。
- 标准 API Runner 下新增 `qianchuan_shop_get` 连接器。
- Doris 新增 CONNECT/ODS 表。
- 单元测试和 SQL 验证探针。

## 非范围

- 不在缺少真实 `QIANCHUAN_OPENAPI_ACCESS_TOKEN` 的情况下上线 DolphinScheduler 每日调度。
- 不建设 DWD/DIM/DWS/ADS 语义模型。
- 不把 token、secret 或授权码写入代码和公开文档。

## 当前门禁

- 后台应用已确认具备“获取店铺账户信息”权限。
- 目标接口开发者频控为 QPS 10，代码默认配置 QPS 5。
- 真实采集和调度上线等待 `.env` 补齐巨量千川 token/secret 后执行。
