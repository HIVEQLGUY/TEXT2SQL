# 任务清单

- [x] 官方接口详情确认：`GET /open_api/v1.0/qianchuan/shop/get/`
- [x] 权限点确认：店铺账号管理 `20120000` / 获取店铺账户信息 `20121000`
- [x] 后台应用确认：`佑美巨量千川投放自助分析系统` 已上线，APP_ID `1868934661571884`
- [x] 后台授权确认：授权账号 `1324241103372126 / MaRay` 包含“获取店铺账户信息”
- [x] 频控确认：目标接口 `QPS: 10`，配额充足，不支持提频
- [x] 代码接入：客户端、适配器、统一 Runner 注册
- [x] Doris 表：`connect_qianchuan_shop_get_di`、`ods_qianchuan_shop_account_di`
- [x] 测试：全量 `pytest` 114 passed
- [ ] 凭据：补齐 `QIANCHUAN_OPENAPI_ACCESS_TOKEN`、`QIANCHUAN_OPENAPI_APP_SECRET`
- [ ] 真实采集：跑一次 `qianchuan_shop_get_daily` 并验证 CONNECT/ODS 行数
- [ ] 调度：真实采集通过后注册 DolphinScheduler 每日任务
