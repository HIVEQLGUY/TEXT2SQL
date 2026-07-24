# DWS_抖音_SPU销售明细上游最上游源表目录

- 目标表：DWS_抖音_SPU销售明细（`dws_douyin_spu_sales_detail`）
- 目标刷新任务：2.2抖音_销售经营数据综合表-抖音_销售经营综合表【刷新】（`Ghu44PRchu`）
- 元数据快照：任务 2026-07-18 00:00:00，表 2026-07-18 00:00:00
- 只读递归任务数：519
- 血缘命中表数：118
- 最上游源表数：58
- 非运费最上游源表数：53
- 抖音主题/公共成本组织源表数：33
- 跨域公共源候选数：20
- 运费相关源表剔除数：5
- 剔除表数：20

## 本次口径

- `STD/DWD/DIM/DWS/ADS` 这类分析产出表继续向上穿透，不再按表名当源表。
- `*_du` 表不是一刀切剔除：如果有同名前缀 `*_f`，用 `*_f` 全量表替代；如果血缘真实只使用 `*_du` 且没有 `*_f` 证据，则保留 `*_du` 并标记原因。
- `dev` schema 视为测试环境，不进最终目录。
- 运费、运费险、快递运费、freight 等相关源表本次不进目录，后续单独处理。
- 中间表和剔除表保留在文档后面作为证据，方便核对。

## 抖音主题源表

| 中文表名 | 英文表名 | schema | 业务域分类 | 来源系统候选 | 行数 | 更新时间 | 判断原因 | 产出任务 | 路径示例 |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| ODS_抖音综合表 | `ODS_DOUYINZONGHEBIAO` | cubeappdata | 抖音主题 | 库表迁移 | 1428.0 | 2026-07-07 08:58:39 | 产出任务类型为接入/迁移类：库表迁移 | ODS_抖音综合表【迁移】(mJ44GUeDiF, 库表迁移) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 6p4aMPhpIB -> dbcHW02Vp0 -> mJ44GUeDiF |
| ODS_抖音乘方推广花费表_填报 | `ODS_douyinchengfangtuiguanghuafei` | cubeappdata | 抖音主题 | 填报 | 64.0 | 2026-04-22 11:31:24 | 产出任务类型为接入/迁移类：库表迁移 | ODS_抖音乘方推广花费表【迁移】(OgqA3SQ6bT, 库表迁移) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> W5WDKhMdo4 -> sD6L0X74Ag -> srspReyO40 -> 3HaOI1YTSj -> sX484NOPO3 |
| ODS_抖音乘方计划id_链接id_映射_RPA | `ODS_jihuaidduiyingshangpinid` | cubeappdata | 抖音主题 | 影刀/RPA | 13.0 | 2026-01-20 16:51:47 | 产出任务类型为接入/迁移类：库表迁移 | ODS_抖音乘方计划id对应链接id表【迁移】(1beUE64XNH, 库表迁移) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> W5WDKhMdo4 -> sD6L0X74Ag -> srspReyO40 -> 3HaOI1YTSj -> sX484NOPO3 |
| ODS_抖音_部门每日人力成本_填报 | `UD_4971200913022541_BN8N5_dyrlcbtbxs1` | cubeappdata | 抖音主题 | 钉盘/Excel填报 | 3.0 | 2026-07-18 00:15:05 | 产出任务类型为接入/迁移类：钉盘接入 | 抖音人力成本填报.xlsx【钉盘接入】(9OsVTMiWWO, 钉盘接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_抖音_佑美运动户外_直播加热推广_填报 | `UD_5179579576634064_FTRED_dyzbjrtgymyd` | cubeappdata | 抖音主题 | 钉盘/Excel填报 | 31.0 | 2025-12-16 15:24:24 | 产出任务类型为接入/迁移类：excel更新 | 抖音直播加热推广-佑美运动户外【EXCEL】(lWKYjw3RvZ, excel更新) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> W5WDKhMdo4 -> sD6L0X74Ag -> srspReyO40 -> 3HaOI1YTSj -> 0C42m71eLb |
| ODS_抖音综合表_填报 | `UD_5179579576634064_XDLII_dyzhbxs1` | cubeappdata | 抖音主题 | 钉盘/Excel填报 | 1745.0 | 2026-07-18 11:00:07 | 产出任务类型为接入/迁移类：钉盘接入 | 抖音综合表.xlsx【钉盘接入】(LkqMfbyv8e, 钉盘接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 6p4aMPhpIB -> dbcHW02Vp0 -> nuSN8563RV -> LkqMfbyv8e |
| ODS_抖音_推广消耗流量表_RPA | `doutuiguangliuliangshuju` | cubeappdata | 抖音主题 | 影刀/RPA | 117790.0 | 2026-06-08 10:49:40 | 产出任务类型为接入/迁移类：库表迁移 | 抖音-推广消耗、流量表【迁移】(jowXVWAEml, 库表迁移) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> W5WDKhMdo4 -> sD6L0X74Ag -> srspReyO40 -> wHcpHrnPGx -> Xj4AfORj0h |
| 货品型号始发地 | `huopinxinghaoshifadi` | cubeappdata | 公共维表/成本/组织 | 库表迁移 | 1570.0 | 2026-04-13 17:08:09 | 产出任务类型为接入/迁移类：库表迁移 | 货品型号始发地【迁移】(wB80eUhvdf, 库表迁移) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_售后列表信息表(抖店API) | `ods_api_dd_after_sale_list_info_du` | cubeappdata | 抖音主题 | 抖店/API | 372328.0 | 2026-07-18 02:13:17 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_售后列表信息表(抖店API)【连接器】(teQTjNS2jo, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_查询店铺联盟订单信息表(抖店API) | `ods_api_dd_buyin_query_shop_alliance_order_info_du` | cubeappdata | 抖音主题 | 抖店/API | 339788.0 | 2026-07-18 02:24:12 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_查询店铺联盟订单信息表(抖店API)【连接器】(QqqmUEVmQ7, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_商品详情信息表(抖店API) | `ods_api_dd_product_detail_info_du` | cubeappdata | 抖音主题 | 抖店/API | 31294.0 | 2026-07-18 02:18:52 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_商品详情信息表(抖店API)【连接器】(7iATpCqsy1, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> 4sMhrTjpMW -> yhAjbzPaTp -> CTuKHcQM5w -> PmgpigAQRE -> qhv7swmY4l |
| ODS_商家结算账单信息表(抖店API) | `ods_api_dd_settle_bill_detail_info_du` | cubeappdata | 抖音主题 | 抖店/API | 537198.0 | 2026-07-18 10:04:33 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_商家结算账单信息表(抖店API)【连接器】(nn44PwEKsM, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_部门信息表(钉钉API) | `ods_api_dingtalk_dept_info_f` | cubeappdata | 公共维表/成本/组织 | 钉钉/API | 169.0 | 2026-07-18 02:14:56 | 尾部为 _f，全量表；按要求作为源表候选 | ods_api_dingtalk_dept_info_f【EtlDevelop任务】(TRAl2GEgxB, etl开发任务) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 6p4aMPhpIB -> dbcHW02Vp0 -> nuSN8563RV -> eAWHKCeJXl -> oi6J9yuQH8 -> t4O2bq0buA -> TRAl2GEgxB |
| ODS_用户信息表(钉钉API) | `ods_api_dingtalk_user_info_f` | cubeappdata | 公共维表/成本/组织 | 钉钉/API | 629.0 | 2026-07-18 02:32:12 | 尾部为 _f，全量表；按要求作为源表候选 | ods_api_dingtalk_user_info_f【EtlDevelop任务】(NWgJ6lDXr9, etl开发任务) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 6p4aMPhpIB -> dbcHW02Vp0 -> nuSN8563RV -> eAWHKCeJXl -> oi6J9yuQH8 -> t4O2bq0buA -> 1Semn2dteT -> NWgJ6lDXr9 |
| ODS_抖音账号信息表(巨量千川API) | `ods_api_jlqc_douyin_account_info_du` | cubeappdata | 抖音主题 | 巨量千川/投放 | 3956.0 | 2026-07-18 01:28:52 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_抖音账号信息表(巨量千川API)【连接器】(ahuGb3XnjE, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> qjk10d4W7h -> bI86bM7BvJ -> qBO2jNZBhK -> K1gH9SHZT5 -> 8iqyOpnfDY |
| ODS_直播间列表信息表(巨量千川API) | `ods_api_jlqc_live_list_info_du` | cubeappdata | 抖音主题 | 巨量千川/投放 | 1474.0 | 2026-07-18 02:04:52 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_直播间列表信息表(巨量千川API)【连接器】(2JAh8JnGKf, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> qjk10d4W7h -> bI86bM7BvJ -> qBO2jNZBhK -> K1gH9SHZT5 -> 8iqyOpnfDY |
| ODS_全域推广乘方直播间抖音号数据信息表(巨量千川API) | `ods_api_jlqc_uni_overall_roi_live_aweme_info_du` | cubeappdata | 抖音主题 | 巨量千川/投放 | 28.0 | 2026-07-17 05:02:52 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_全域推广乘方直播间抖音号数据信息表(巨量千川API)【连接器】(S7sbIPZs12, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> qjk10d4W7h -> bI86bM7BvJ -> qBO2jNZBhK -> K1gH9SHZT5 -> S7sbIPZs12 |
| ODS_全域推广乘方商品商品数据信息表(巨量千川API) | `ods_api_jlqc_uni_overall_roi_product_product_info_du` | cubeappdata | 抖音主题 | 巨量千川/投放 | 353.0 | 2026-07-06 05:00:48 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_全域推广乘方商品商品数据信息表(巨量千川API)【连接器】(tVwHPS1VgT, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> qjk10d4W7h -> bI86bM7BvJ -> qBO2jNZBhK -> K1gH9SHZT5 -> tVwHPS1VgT |
| ODS_全域推广报告信息表(巨量千川API)_旧 | `ods_api_jlqc_uni_promition_report_info_du_old` | cubeappdata | 抖音主题 | 巨量千川/投放 | 16588.0 | 2026-07-18 10:02:03 | 产出任务类型为接入/迁移类：连接器接入 | ODS_全域推广报告信息表(巨量千川API)【连接器】(MegrZkwZoP, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> W5WDKhMdo4 -> sD6L0X74Ag -> srspReyO40 -> 3HaOI1YTSj -> 0C42m71eLb |
| ODS_全域推广直播间维度信息表(巨量千川API) | `ods_api_jlqc_uni_promition_root_report_info_du` | cubeappdata | 抖音主题 | 巨量千川/投放 | 2324.0 | 2026-07-18 05:18:02 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_全域推广直播间维度信息表(巨量千川API)【连接器】(TJgtI2jvcD, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> qjk10d4W7h -> bI86bM7BvJ -> qBO2jNZBhK -> K1gH9SHZT5 -> TJgtI2jvcD |
| ODS_全域推广商品全域商品数据信息表(巨量千川API) | `ods_api_jlqc_uni_promotion_product_product_info_du` | cubeappdata | 抖音主题 | 巨量千川/投放 | 4249.0 | 2026-07-18 02:23:47 | 上游真实使用 _du，未找到可替代的 _f 全量表；产出任务类型为接入/迁移类：连接器接入 | ODS_全域推广商品全域商品数据信息表(巨量千川API)【连接器】(Jxeq32pjP3, 连接器接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> qjk10d4W7h -> bI86bM7BvJ -> qBO2jNZBhK -> K1gH9SHZT5 -> Jxeq32pjP3 |
| ODS_商品历史成本价信息表(聚水潭标准API) | `ods_api_jstbz_product_history_cost_price_info_f` | cubeappdata | 公共维表/成本/组织 | 聚水潭/ERP | 245.0 | 2026-07-18 02:24:54 | 尾部为 _f，全量表；按要求作为源表候选 | ods_api_jstbz_product_history_cost_price_info_f【EtlDevelop任务】(0ccP8y2dQJ, etl开发任务) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_商品SKU信息表(聚水潭标准API) | `ods_api_jstbz_product_sku_info_f` | cubeappdata | 公共维表/成本/组织 | 聚水潭/ERP | 49615.0 | 2026-07-18 02:30:23 | 尾部为 _f，全量表；按要求作为源表候选 | ods_api_jstbz_product_sku_info_f【EtlDevelop任务】(4v6XI21730, etl开发任务) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> 994SOzLTQV -> 5aMpRAhBmy -> M8qi0iwCWh -> pmMzApalZx -> N4uyZn2Brb |
| ODS_组合商品信息表(聚水潭标准API) | `ods_api_jstbz_suite_product_info_f` | cubeappdata | 公共维表/成本/组织 | 聚水潭/ERP | 11499.0 | 2026-07-18 01:00:30 | 尾部为 _f，全量表；按要求作为源表候选 | ods_api_jstbz_suite_product_info_f【EtlDevelop任务】(Qoa4SEgNmZ, etl开发任务) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> 994SOzLTQV -> 5aMpRAhBmy -> M8qi0iwCWh -> pmMzApalZx -> N4uyZn2Brb |
| ODS_销售订单归档信息表(聚水潭奇门API) | `ods_api_jstqm_archive_sale_order_info_f` | cubeappdata | 公共维表/成本/组织 | 聚水潭/ERP | 32511821.0 | 2026-05-06 19:01:51 | 尾部为 _f，全量表；按要求作为源表候选 | ods_api_jstqm_archive_sale_order_info_f【EtlDevelop任务】(RCAvJGRCIk, etl开发任务) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_退货退款信息表(聚水潭奇门API) | `ods_api_jstqm_refund_info_f` | cubeappdata | 公共维表/成本/组织 | 聚水潭/ERP | 3468402.0 | 2026-07-18 02:32:06 | 尾部为 _f，全量表；按要求作为源表候选 | ods_api_jstqm_refund_info_f【EtlDevelop任务】(mT4yyoaTaE, etl开发任务) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_销售订单信息表(聚水潭奇门API) | `ods_api_jstqm_sale_order_info_f` | cubeappdata | 公共维表/成本/组织 | 聚水潭/ERP | 23651665.0 | 2026-07-18 03:25:19 | 尾部为 _f，全量表；按要求作为源表候选 | ods_api_jstqm_sale_order_info_f【EtlDevelop任务】(9hARYiuSyx, etl开发任务) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_抖音_直播间人力成本支出_填报 | `ods_douyin_live_room_labor_cost_entry` | cubeappdata | 抖音主题 | 填报 | 276.0 | 2026-07-18 05:00:14 | 产出任务类型为接入/迁移类：在线表格接入 | 支出明细（钉钉表格）【在线表格接入】(xJeIQ69bSX, 在线表格接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_抖音_直播间主链接映射_填报 | `ods_douyin_live_room_main_link_detail_entry` | cubeappdata | 抖音主题 | 填报 | 20.0 | 2026-07-18 05:00:09 | 产出任务类型为接入/迁移类：在线表格接入 | 直播链接（钉钉表格）【在线表格接入】(pUeSXt1NWn, 在线表格接入) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> qjk10d4W7h -> bI86bM7BvJ -> qBO2jNZBhK -> K1gH9SHZT5 -> pUeSXt1NWn |
| ODS_抖音_全域投放推商品_RPA | `ods_douyinanshangpintuiguangshuju` | cubeappdata | 抖音主题 | 影刀/RPA | 85275.0 | 2026-04-22 11:31:00 | 产出任务类型为接入/迁移类：库表迁移 | ods-抖音全域按商品推广数据【迁移】(00uSPqQxB9, 库表迁移) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> nhgdWWKApC -> W5WDKhMdo4 -> sD6L0X74Ag -> srspReyO40 -> 3HaOI1YTSj -> sX484NOPO3 |
| ODS_抖音好评数据_填报 | `ods_dyhaopingshuju` | cubeappdata | 抖音主题 | 填报 | 1789.0 | 2025-11-14 19:32:13 | 产出任务类型为接入/迁移类：库表迁移 | ods_抖音好评数据【迁移】(Z3M1lFdITy, 库表迁移) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| ODS_抖音刷单数据_填报 | `ods_dyshuandanshuju` | cubeappdata | 抖音主题 | 填报 | 1222.0 | 2025-11-14 19:36:48 | 产出任务类型为接入/迁移类：库表迁移 | ods_抖音刷单数据【迁移】(JoeKH6qxcq, 库表迁移) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |
| STD_商品历史成本表(聚水潭标准API) | `std_api_jstbz_product_history_cost_info_f` | cubeappdata | 公共维表/成本/组织 | 聚水潭/ERP | 168166.0 | 2026-07-18 02:30:44 | 尾部为 _f，全量表；按要求作为源表候选 | std_api_jstbz_product_history_cost_info_f【EtlDevelop任务】(bT8csKdyGj, etl开发任务) | Ghu44PRchu -> PmOkCMF2rf -> ayK47N3cOU -> k5gRwv2JLE -> 5Mg7F1AfFT -> FpM1x7YM9G -> RggJA8Sv0l -> GKM7p7i4nh -> yZq4ZcYKSY -> lI6tx3AsC7 -> I3wRsmNT14 -> MUuQqC8Ik3 |

## 跨域公共源候选

这些表是递归血缘链路带入的最上游表，但业务域不是抖音主题主体，先不混入主目录。

| 中文表名 | 英文表名 | schema | 业务域分类 | 来源系统候选 | 判断原因 |
| --- | --- | --- | --- | --- | --- |
| ODS_佑美拼多多销售订单数据 | `ODS_YOUMEIPDDxiaoshoudingdanbiao` | cubeappdata | 跨域拼多多 | 库表迁移 | 产出任务类型为接入/迁移类：库表迁移 |
| 拼多多佑美助攻数据.xlsx-拼多多助攻数据 | `UD_5179579576634064_7K5LO_pddymzgsjxpd` | cubeappdata | 跨域拼多多 | 钉盘/Excel填报 | 产出任务类型为接入/迁移类：钉盘接入 |
| 拼多多KUS助攻数据.xlsx-拼多多助攻数据 | `UD_5179579576634064_89GSE_pddkzgsjxpdd` | cubeappdata | 跨域拼多多 | 钉盘/Excel填报 | 产出任务类型为接入/迁移类：钉盘接入 |
| 天猫综合表.xlsx-Sheet2 | `UD_5179579576634064_EB3YT_tmzhbxs2` | cubeappdata | 跨域天猫/淘宝 | 钉盘/Excel填报 | 产出任务类型为接入/迁移类：钉盘接入 |
| 京东综合表.xlsx-京东综合表 | `UD_5179579576634064_RAEGP_jdzhbxjdzhb` | cubeappdata | 跨域京东 | 钉盘/Excel填报 | 产出任务类型为接入/迁移类：钉盘接入 |
| 大件商品编码干线费保价费.xlsx-Sheet1 | `UD_6816162936700995_HP4G4_djspbmgxfbjf` | cubeappdata | 待确认域 | 钉盘/Excel填报 | 产出任务类型为接入/迁移类：钉盘接入 |
| 天猫综合表 | `huizongbiao` | cubeappdata | 跨域天猫/淘宝 | 库表迁移 | 产出任务类型为接入/迁移类：库表迁移 |
| 京东佑美旗舰店_刷单数据 | `jingdong_youmeiqijiandianshuandanshuju` | cubeappdata | 跨域京东 | 库表迁移 | 产出任务类型为接入/迁移类：库表迁移 |
| 京东佑美旗舰店_销售数据 | `jingdongxiaohsoushuju` | cubeappdata | 跨域京东 | 库表迁移 | 产出任务类型为接入/迁移类：库表迁移 |
| 京东综合表 | `jingdongzonghebiao` | cubeappdata | 跨域京东 | 库表迁移 | 产出任务类型为接入/迁移类：库表迁移 |
| 拼多多KUS助攻数据 | `kuszhugong` | cubeappdata | 跨域拼多多 | 库表迁移 | 产出任务类型为接入/迁移类：库表迁移 |
| ODS_退款审核单列表信息表(京东API) | `ods_api_jingdong_aftersale_apply_order_list_info_f` | cubeappdata | 跨域京东 | 京东/API | 尾部为 _f，全量表；按要求作为源表候选 |
| ODS_售后服务单列表信息表(京东API) | `ods_api_jingdong_asc_query_list_info_f` | cubeappdata | 跨域京东 | 京东/API | 尾部为 _f，全量表；按要求作为源表候选 |
| ODS_销售订单信息表(京东API) | `ods_api_jingdong_order_info_f` | cubeappdata | 跨域京东 | 京东/API | 尾部为 _f，全量表；按要求作为源表候选 |
| ODS_SKU信息表(京东API) | `ods_api_jingdong_sku_info_f` | cubeappdata | 跨域京东 | 京东/API | 尾部为 _f，全量表；按要求作为源表候选 |
| ODS_在售商品列表信息表(淘宝API) | `ods_api_tb_onsale_item_list_info_f` | cubeappdata | 跨域天猫/淘宝 | 淘宝/API | 尾部为 _f，全量表；按要求作为源表候选 |
| api授权信息 | `ods_db_cube_dc_auth_api_config_detail_info_f` | cubeappdata | 待确认域 | 库表迁移 | 尾部为 _f，全量表；按要求作为源表候选 |
| 拼多多2023助攻数据 | `pdd2023zhugongshuju` | cubeappdata | 跨域拼多多 | 库表迁移 | 产出任务类型为接入/迁移类：库表迁移 |
| ODS_拼多多售后数据 | `pinduoduoshoushoushuju` | cubeappdata | 跨域拼多多 | 库表迁移 | 产出任务类型为接入/迁移类：库表迁移 |
| 拼多多佑美助攻数据 | `youmeizhugong` | cubeappdata | 跨域拼多多 | 库表迁移 | 产出任务类型为接入/迁移类：库表迁移 |

## 本次排除的运费相关源表

| 中文表名 | 英文表名 | schema | 判断原因 |
| --- | --- | --- | --- |
| 202507大件逆向运费 | `dajiannixiangyunfei` | cubeappdata | 产出任务类型为接入/迁移类：库表迁移 |
| ODS_抖音_运费险账单数据_RPA | `douyinyunfeixian` | cubeappdata | 产出任务类型为接入/迁移类：库表迁移 |
| 运费账单明细（抖音财务对账后） | `freight_bill_detail` | cubeappdata | 产出任务类型为接入/迁移类：库表迁移 |
| 运费账单问题件及冲回扣减明细（抖音财务对账后） | `freight_bill_exception` | cubeappdata | 产出任务类型为接入/迁移类：库表迁移 |
| 天猫佑美大件运费综合表 | `tianmaoyoumeidajianyunfeizonghebiao` | cubeappdata | 产出任务类型为接入/迁移类：库表迁移 |

## 中间表证据

| 中文表名 | 英文表名 | schema | 判断原因 | 产出任务 |
| --- | --- | --- | --- | --- |
| dim_淘系商品链接属性 | `dim_tb_itm_link_attr` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 各渠道类目映射及大小件属性-dim_淘系链接基本属性【刷新】(1uqgfnY6lo, 分析存表刷新) |
| DWS_抖音_SPU销售明细 | `dws_douyin_spu_sales_detail` | cubeappdata | 目标结果表，不进入源表目录 | 2.2抖音_销售经营数据综合表-抖音_销售经营综合表【刷新】(Ghu44PRchu, 分析存表刷新) |
| ODS_退货退款信息表_实时(聚水潭奇门API) | `ods_api_jstqm_refund_info_f_ss` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | ods_api_jstqm_refund_info_f_ss【EtlDevelop任务】(BxO04KZGrR, etl开发任务) |
| std_退货退款信息表 | `ud_1_sthtkxxb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.1std_淘宝销售和售后数据清洗-std_退货退款信息表【刷新】(Wy8GHrifZz, 分析存表刷新) |
| DWD_抖音_订单结算账单明细 | `ud_3418004512502203_ddyddzdsjqx` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.3 STD_抖音账单流水数据清晰-DWD_抖音订单账单数据清晰【刷新】(E1OO104q1k, 分析存表刷新) |
| DWD_抖音_大件_订单运单号明细表 | `ud_3418004512502203_ddydjkdyfjs` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 2.1 DWD_抖音数据清洗综合表-DWD抖音—大件快递运费计算【刷新】(0M61hG2Q2i, 分析存表刷新) |
| DWD_抖音结算账单费用 | `ud_3418004512502203_ddyjszdfy` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.3 STD_抖音账单流水数据清晰-dwd_抖音结算账单费用【刷新】(AaQLxF82O1, 分析存表刷新) |
| DWD_抖音_小件_订单运单号明细表 | `ud_3418004512502203_ddyxjkdyfjs` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 2.1 DWD_抖音数据清洗综合表-DWD抖音_小件快递运费计算【刷新】(3FwNWleSV4, 分析存表刷新) |
| DWD_抖音_订单销售明细 | `ud_3418004512502203_ddyxsjyzhb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 2.1 DWD_抖音数据清洗综合表-DWD_抖音销售经营综合表【刷新】(lI6tx3AsC7, 分析存表刷新) |
| 京东佑美旗舰店大件运费清洗 | `ud_3418004512502203_jdymqjddjyfq` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 2.1京东销售和售后数据关联-京东佑美旗舰店大件运费清洗【刷新】(eM4kzPuhmy, 分析存表刷新) |
| 1.1std_京东销售数据 | `ud_3418004512502203_n11sjdxssj` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.1京东销售数据-1.1std_京东销售数据【刷新】(lpAdAWV47s, 分析存表刷新) |
| 1.2京东售后数据 | `ud_3418004512502203_n12jdshsj` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.2京东售后数据-1.2京东售后数据【刷新】(A3M3fv6cnX, 分析存表刷新) |
| 1.2京东自营和京造长值售后数据 | `ud_3418004512502203_n12jdzyhjzzz` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.2STD京东自营和京造厂直退货数据清洗-1.2京东自营和京造长值售后数据【刷新】(ZHATr0HJPU, 分析存表刷新) |
| 1.2std_拼多多退货退款信息表 | `ud_3418004512502203_n12spddthtkx` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.2拼多多退货数据清洗-1.2std_拼多多退货退款信息表【刷新】(WAoEq25uKD, 分析存表刷新) |
| 1.3京东京造和自营厂直运费计算 | `ud_3418004512502203_n13jdjzhzycz` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.3京东自营和京造厂直（运费计算）销售和售后数据-1.3京东京造和自营厂直运费计算【刷新】(K1wv3powHI, 分析存表刷新) |
| 1.5拼多多小件快递运费 | `ud_3418004512502203_n15pddxjkdyf` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.5,拼多多运费计算-1.5拼多多小件快递运费【刷新】(Daui5ReOky, 分析存表刷新) |
| 1.各员工钉钉详情表 | `ud_3418004512502203_n1gygddxqb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 钉钉用户信息表-1.各员工钉钉详情表【刷新】(oi6J9yuQH8, 分析存表刷新) |
| 2.2快递单号计算运费 | `ud_3418004512502203_n22kddhjsyf` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 2.1京东销售和售后数据关联-2.2快递单号计算运费【刷新】(czaWuc75Dm, 分析存表刷新) |
| 拼多多大件运费计算 | `ud_3418004512502203_pdddjyfjs` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 2.1拼多多数据清洗（人工扣点、退货、助攻、运费、采购、基础扣点）-拼多多大件运费计算【刷新】(ghuQO3FNsQ, 分析存表刷新) |
| 全局_商品资料表 | `ud_3418004512502203_qjspzlb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 全局_商品资料表-全局_商品资料表【刷新】(N4uyZn2Brb, 分析存表刷新) |
| STD_达人佣金预估 | `ud_3418004512502203_sdryjyg` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.3 STD_抖音账单流水数据清晰-STD_达人佣金预估【刷新】(kdqUt9TvHS, 分析存表刷新) |
| STD_抖音_售后单明细（抖店API） | `ud_3418004512502203_sdyshsjqx` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.2 STD_抖音售后数据清洗-STD_抖音售后数据清洗【刷新】(HdaYLSZ0jU, 分析存表刷新) |
| STD_抖音_推广消耗明细 | `ud_3418004512502203_sdytgsj` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.4抖音推广数据-std_抖音推广数据【刷新】(sD6L0X74Ag, 分析存表刷新) |
| std_京东自营和京造销售订单信息表 | `ud_3418004512502203_sjdzyhjzxsdd` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.1京东自营和京造厂直聚水潭销售数据-std_京东自营和京造销售订单信息表【刷新】(KFp53HHPrt, 分析存表刷新) |
| STD_抖音_ERP销售订单明细表 | `ud_3418004512502203_sjstdyxsddxx` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.11STD聚水潭抖音—销售数据清洗-std_聚水潭抖音销售订单信息表【刷新】(251Uny8XjY, 分析存表刷新) |
| std_拼多多刷单数据 | `ud_3418004512502203_spddsdsj` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.3拼多多刷单数据清洗-std_拼多多刷单数据【刷新】(21vCNM5Ybe, 分析存表刷新) |
| std_拼多多销售订单信息表 | `ud_3418004512502203_spddxsddxxb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.1.std_拼多多销售数据清洗-std_拼多多销售订单信息表【刷新】(GRSxAqsPjw, 分析存表刷新) |
| std_销售订单信息表 | `ud_3418004512502203_sxsddxxb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.1std_淘宝销售和售后数据清洗-std_销售订单信息表【刷新】(QUMvyo4abs, 分析存表刷新) |
| STD_抖音_订单销售明细 | `ud_3418004512502203_sxssjqx` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.1 STD_抖音销售清洗表-STD_销售数据清洗【刷新】(5aMpRAhBmy, 分析存表刷新) |
| 天猫大件运费数据清洗表 | `ud_3418004512502203_tmdjyfsjqxb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 2.dwd_淘宝数据清洗-天猫大件运费数据清洗表【刷新】(L6gpGlB7lA, 分析存表刷新) |
| 天猫、拼多多、京东pop快递运费 | `ud_3418004512502203_tmpddjdpkdyf` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | std_大件正向运费数据清洗-天猫、拼多多、京东pop快递运费【刷新】(f9Konlb2Nb, 分析存表刷新) |
| 1.5有快递单号（快递运费计算） | `ud_3418004512502203_ykddhd` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 2.1拼多多数据清洗（人工扣点、退货、助攻、运费、采购、基础扣点）-1.5有快递单号（快递运费计算）【刷新】(emuMgVsUcl, 分析存表刷新) |
| STD_抖音_链接直播间人力成本明细 | `ud_4971200913022541_ddyzbjrlcb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.5 抖音直播间人力成本清洗-dwd_抖音直播间人力成本【刷新】(2hsVfz4qE0, 分析存表刷新) |
| STD_抖音_推广消耗明细_巨量千川 | `ud_4971200913022541_sdytgxhmxjlq` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.6 千川推广数据清洗-STD_抖音_推广消耗明细_巨量千川【刷新】(bI86bM7BvJ, 分析存表刷新) |
| dwd_抖音直播间主链映射 | `ud_6816162936700995_ddyzbjzlys` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.5 抖音直播间人力成本清洗-dwd_抖音直播间主链映射【刷新】(qLMpV02KVt, 分析存表刷新) |
| DIM_商品历史成本表(聚水潭标准API) | `ud_6816162936700995_jgb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 商品历史成本价众数清洗-结果表【刷新】(YLclnZKfcH, 分析存表刷新) |
| 1.1.1 抖音销售订单实收info | `ud_6816162936700995_n111dyxsddss` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.1.1抖音销售清洗表订单实收info-1.1.1 抖音销售订单实收info【刷新】(XkOL49YYeW, 分析存表刷新) |
| 1.1.2 STD_抖音销售清洗表-货品详情 | `ud_6816162936700995_n112sdyxsqxb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.1.2 STD_抖音销售清洗表-货品详情-1.1.2 STD_抖音销售清洗表-货品详情【刷新】(XVR0tvuk7I, 分析存表刷新) |
| 1.1.3 STD_抖音销售清洗表运单号 | `ud_6816162936700995_n113sdyxsqxb` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 1.1.3 STD_抖音销售清洗表运单号-1.1.3 STD_抖音销售清洗表运单号【刷新】(jK2dakuj7Q, 分析存表刷新) |
| 2.2.1.1 抖音推广花费匹配订单 | `ud_6816162936700995_n2211dytghfp` | cubeappdata | 由分析/ETL任务产出且存在上游，继续穿透，不作为最上游源表 | 2.2.1.1 抖音推广花费匹配订单-2.2.1.1 抖音推广花费匹配订单【刷新】(nhgdWWKApC, 分析存表刷新) |

## 剔除表

| 中文表名 | 英文表名 | schema | 判断原因 |
| --- | --- | --- | --- |
| ODS_销售订单列表信息表(抖店API) | `ods_api_dd_sale_order_list_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_dd_sale_order_list_info_f，最终目录使用 _f |
| ODS_资金流水信息表(抖店API) | `ods_api_dd_shop_account_item_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_dd_shop_account_item_info_f，最终目录使用 _f |
| ODS_部门信息表(钉钉API) | `ods_api_dingtalk_dept_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_dingtalk_dept_info_f，最终目录使用 _f |
| ODS_用户信息表(钉钉API) | `ods_api_dingtalk_user_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_dingtalk_user_info_f，最终目录使用 _f |
| ODS_退款审核单列表信息表(京东API) | `ods_api_jingdong_aftersale_apply_order_list_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jingdong_aftersale_apply_order_list_info_f，最终目录使用 _f |
| ODS_售后服务单列表信息表(京东API) | `ods_api_jingdong_asc_query_list_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jingdong_asc_query_list_info_f，最终目录使用 _f |
| ODS_销售订单信息表(京东API) | `ods_api_jingdong_order_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jingdong_order_info_f，最终目录使用 _f |
| ODS_SKU信息表(京东API) | `ods_api_jingdong_sku_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jingdong_sku_info_f，最终目录使用 _f |
| ODS_退货退款归档信息表(聚水潭标准API) | `ods_api_jstbz_archive_refund_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstbz_archive_refund_info_f，最终目录使用 _f |
| ODS_销售订单归档信息表(聚水潭标准API) | `ods_api_jstbz_archive_sale_order_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstbz_archive_sale_order_info_f，最终目录使用 _f |
| ODS_商品历史成本价信息表(聚水潭标准API) | `ods_api_jstbz_product_history_cost_price_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstbz_product_history_cost_price_info_f，最终目录使用 _f |
| ODS_商品SKU信息表(聚水潭标准API) | `ods_api_jstbz_product_sku_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstbz_product_sku_info_f，最终目录使用 _f |
| ODS_退货退款信息表(聚水潭标准API) | `ods_api_jstbz_refund_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstbz_refund_info_f，最终目录使用 _f |
| ODS_组合商品信息表(聚水潭标准API) | `ods_api_jstbz_suite_product_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstbz_suite_product_info_f，最终目录使用 _f |
| ODS_退货退款归档信息表(聚水潭奇门API) | `ods_api_jstqm_archive_refund_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstqm_archive_refund_info_f，最终目录使用 _f |
| ODS_销售订单归档信息表(聚水潭奇门API) | `ods_api_jstqm_archive_sale_order_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstqm_archive_sale_order_info_f，最终目录使用 _f |
| ODS_退货退款信息表(聚水潭奇门API) | `ods_api_jstqm_refund_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstqm_refund_info_f，最终目录使用 _f |
| ODS_销售订单信息表(聚水潭奇门API) | `ods_api_jstqm_sale_order_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_jstqm_sale_order_info_f，最终目录使用 _f |
| ODS_类目列表信息表(淘宝API) | `ods_api_tb_itemcats_list_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_tb_itemcats_list_info_f，最终目录使用 _f |
| ODS_在售商品列表信息表(淘宝API) | `ods_api_tb_onsale_item_list_info_du` | cubeappdata | 尾部为 _du，且存在可替代的全量表 ods_api_tb_onsale_item_list_info_f，最终目录使用 _f |
