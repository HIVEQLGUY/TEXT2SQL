# 第一批数据质量规则配置结果

更新时间：2026-07-22

## 配置口径

- 本批只配置第一批核心候选表，不包含影刀/text 源接入专项表。
- 有可靠业务日期字段的表：配置「单日行数，固定值」，统计日期截止至 T-1，异常条件为 `计算值 <= 0`。
- 暂无可靠业务日期字段的表：配置「单次执行成功数据条数，固定值」，异常条件为 `计算值 <= 0`。
- 异常阻断：否，仅预警。
- 告警渠道：IM 个人消息，接收人包含包彦。
- 告警配置同时写入任务对象和表对象，避免任务详情入口和表详情入口展示不一致。
- 已有正常字段波动规则保留；未发现「最近 3 天」或「行数大于 0 报警」类错误规则残留。

## 已完成配置

| 中文业务名 | 物理表名 | 任务 ID | 表 ID | 规则 ID | 规则口径 |
| --- | --- | --- | --- | --- | --- |
| DWS_抖音_SPU销售明细 | dws_douyin_spu_sales_detail | Ghu44PRchu | nM34Tlww6y00 | 42Q35SSEyf | pay_time T-1 单日行数 <= 0 |
| 商品编码销售数据、流量数据、推广数据 | ud_3418004512502203_spbmxssjllsj | tCQHRUr2lz | kz8w04VU2r67 | mSKcfUt8y4 | zfsj T-1 单日行数 <= 0 |
| dwd_销售退货详情表 | ud_3418004512502203_dxsthxqb | WsaMDlzNGI | hQBX6TCHMM77 | 3Lg1E3adzH | 单次执行成功数据条数 <= 0 |
| 2.3拼多多数据清洗 | ud_3418004512502203_n23pddsjqx | vTeCxTA2tz | EkqHoEv25p00 | 7C4oBWo3mt | pay_date T-1 单日行数 <= 0 |
| ODS_销售订单信息表(聚水潭奇门API) | ods_api_jstqm_sale_order_info_f | 9hARYiuSyx | 06eMC7GyvQ | Z5AhCKGfzC | dt T-1 单日行数 <= 0 |
| ODS_销售订单信息表(聚水潭奇门API) DU | ods_api_jstqm_sale_order_info_du | MvuyryYfyY | 3g4MDp65Et | tpMf8VsRBs | dt T-1 单日行数 <= 0 |
| DWD_抖音_订单销售明细 | ud_3418004512502203_ddyxsjyzhb | lI6tx3AsC7 | K3stNj3df630 | qQquM6Bu7G | pay_time T-1 单日行数 <= 0 |
| 天猫-销售计划总表 | ud_5179579576634064_tmxsjhzb | s9Apa7nuXH | R0Psf66NwF00 | KNqSaP2M3d | 单次执行成功数据条数 <= 0 |
| ODS_商品SKU信息表(聚水潭标准API) | ods_api_jstbz_product_sku_info_f | 4v6XI21730 | XOOW9wgXwR | sJcD4KSFyP | dt T-1 单日行数 <= 0 |
| 2.2京东佑美旗舰店总综合表 | ud_3418004512502203_n22jdymqjdzz | BRQxUQstRp | cnO3uGGZim20 | 1EAPvHL9lm | paymentconfirmtime T-1 单日行数 <= 0 |
| 3.京东自营和京造综合表 | ud_3418004512502203_n3jdzyhjzzhb | 7lAvjA2Tc5 | h7D7bU64Nj00 | DXwpAf3OQp | 单次执行成功数据条数 <= 0 |
| STD_抖音_订单销售明细 | ud_3418004512502203_sxssjqx | 5aMpRAhBmy | dCvk1Epx0r67 | OK86ofR8A4 | pay_time T-1 单日行数 <= 0 |
| 天猫-推广总表 | ud_5179579576634064_tmtgzb | tIae4qir6w | 1qPZWo3lBp00 | QBcddM16Gn | 单次执行成功数据条数 <= 0 |
| std_销售订单信息表 | ud_3418004512502203_sxsddxxb | QUMvyo4abs | rTdWW1Z3q910 | rra4qiO7xm | pay_date T-1 单日行数 <= 0 |

## 跳过项

| 中文业务名 | 物理表名 | 原因 |
| --- | --- | --- |
| ODS_销售订单列表信息表(抖店API) DU | ods_api_dd_sale_order_list_info_du | 该 DU 表此前已按要求删除，后续不再作为候选表。 |

## 复核结果

- 上表 14 张已配置表均能通过接口读取到对应规则。
- 上表 14 张已配置表的任务对象告警均包含包彦。
- 上表 14 张已配置表的表对象告警均包含包彦。
- 第一批影刀/text 源接入专项表尚未批量配置，建议下一步单独按「任务产出行数 <= 0」和「历史基线波动」口径处理。
