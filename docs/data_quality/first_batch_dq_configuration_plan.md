## 2026-07-10 口径补充：影刀/text 账单表剔除

- 影刀数据库（source database = `text`）里的账单类表，除“运费险账单”外，本批不进入质量规则配置。
- 剔除原因：这些账单表属于月度数据处理、手动上传或手动执行性质，不是日常自动采集链路；即使存在下游依赖，也不代表需要每日 freshness 或行数波动校验。
- 判定证据需要同时看表名/中文名和任务性质：如果任务是手动上传、手动执行、月度处理或财务账单拆分，默认剔除；不要因为有数据集消费或下游任务就提升为 P0/P1。
- 保留例外：运费险账单类表仍可进入候选，因为它已被确认为需要关注的业务链路。
- 这条规则只约束账单类表，不影响仍有下游且近期活跃的影刀抓取表，例如评价有礼、红包、推广、流量、销售等明细/结果表。
# 第一批数据质量检查规则配置方案

生成时间：2026-07-10 14:28:08

## 范围

- 第一批重点表：15 张。
- 影刀 text 活跃且有下游的接入表：60 张。
- 不包含：无下游影刀表、长期固化观察表、除运费险外的月度手工账单表、归档订单表。

## 配置原则

1. 前期只配置不依赖复杂业务口径的规则：行数非空、任务产出行数非零、主键非空/重复、核心字段空值、日期/数值格式可转换、字段结构变化。
2. 大表不做全表扫描，优先按昨天分区、昨天业务日期或任务产出行数检查。
3. 影刀/text 源表多数是文本字段，先做格式可转换和静默缺失检查，不直接配置复杂金额波动阈值。
4. 所有规则先预警不阻断；金额波动、上下游对账、复杂枚举合法性等进入第二批。
5. 预策 BI 已支持表规则和字段规则，第一批配置优先使用内置规则模板；SQL 规则只用于组合主键、跨表对账、字段结构变化、文本数值转换等内置模板无法覆盖的场景。
6. 内置规则映射详见：[yuce_bi_quality_rule_setting_logic.md](C:/Users/24796/Documents/TEXT2SQL/docs/data_quality/yuce_bi_quality_rule_setting_logic.md)。

## 汇总清单

| 范围 | 表 | 中文/业务名 | 重要性 | 角色 | 行数 | 最近更新 | 规则数 |
| --- | --- | --- | --- | --- | ---: | --- | ---: |
| core_15 | `dws_douyin_spu_sales_detail` | DWS_抖音_SPU销售明细 | A | result_like | 94013 | 2026-07-09 13:46:24 | 5 |
| core_15 | `ud_3418004512502203_spbmxssjllsj` | 商品编码销售数据、流量数据、推广数据 | A | result_like | 618104 | 2026-07-09 15:13:24 | 4 |
| core_15 | `ud_3418004512502203_dxsthxqb` | dwd_销售退货详情表 | S | result_like | 24816626 | 2026-07-09 15:07:16 | 4 |
| core_15 | `ud_3418004512502203_n23pddsjqx` | 2.3拼多多数据清洗 | A | result_like | 969324 | 2026-07-09 13:47:32 | 5 |
| core_15 | `ods_api_jstqm_sale_order_info_f` | ODS_销售订单信息表(聚水潭奇门API) | A | result_like | 23312740 | 2026-07-09 03:49:20 | 5 |
| core_15 | `ods_api_jstqm_sale_order_info_du` | ODS_销售订单信息表(聚水潭奇门API) | A | result_like | 25408030 | 2026-07-09 03:33:13 | 5 |
| core_15 | `ud_3418004512502203_ddyxsjyzhb` | DWD_抖音_订单销售明细 | A | result_like | 761271 | 2026-07-09 13:44:01 | 5 |
| core_15 | `ud_5179579576634064_tmxsjhzb` | 天猫-销售计划总表 | A | result_like | 14890 | 2026-07-09 15:15:05 | 4 |
| core_15 | `ods_api_jstbz_product_sku_info_f` | ODS_商品SKU信息表(聚水潭标准API) | A | detail_like | 49492 | 2026-07-09 02:03:09 | 5 |
| core_15 | `ud_3418004512502203_n22jdymqjdzz` | 2.2京东佑美旗舰店总综合表 | A | result_like | 112068 | 2026-07-09 13:41:58 | 5 |
| core_15 | `ud_3418004512502203_n3jdzyhjzzhb` | 3.京东自营和京造综合表 | A | result_like | 65696 | 2026-07-09 13:39:24 | 4 |
| core_15 | `ud_3418004512502203_sxssjqx` | STD_抖音_订单销售明细 | A | result_like | 824838 | 2026-07-09 05:34:26 | 5 |
| core_15 | `ud_5179579576634064_tmtgzb` | 天猫-推广总表 | A | result_like | 281713 | 2026-07-09 14:09:52 | 4 |
| core_15 | `ods_api_dd_sale_order_list_info_du` | ODS_销售订单列表信息表(抖店API) | A | result_like | 3226101 | 2026-07-09 05:00:00 | 5 |
| core_15 | `ud_3418004512502203_sxsddxxb` | std_销售订单信息表 | A | result_like | 24884809 | 2026-07-09 06:35:34 | 5 |
| yingdao_text_active_downstream | `huizongbiao` | 天猫综合表 | A | source_like | 9832.0 | 2026-07-10 00:30:18 | 5 |
| yingdao_text_active_downstream | `tianmaoxiaoshoujihuabiao` | 天猫-销售计划表 | B | source_like | 15695.0 | 2026-07-06 16:29:26 | 5 |
| yingdao_text_active_downstream | `tianmaobaozhengjinxiangmucahifen` | 天猫_保证金数据拆分 | B | source_like | 12845.0 | 2026-07-06 15:04:20 | 5 |
| yingdao_text_active_downstream | `pdd_tgzx_promotion_report_store_promotion_store_unit` | 拼多多推广中心推广报表店铺推广明星店铺单元 | C | detail_like | 495.0 | 2026-07-10 11:35:19 | 5 |
| yingdao_text_active_downstream | `tianmaoshangpinIDcaigoufuzeren` | 天猫商品ID采购负责人综合表 | B | source_like | 2032.0 | 2026-07-07 11:05:48 | 5 |
| yingdao_text_active_downstream | `ODS_YOUMEIPDDxiaoshoudingdanbiao` | ODS_佑美拼多多销售订单数据 | REVIEW | detail_like | 6961206.0 | 2026-07-10 08:23:33 | 5 |
| yingdao_text_active_downstream | `shangpinpintuilv` | 天猫-商品品退率明细 | B | detail_like | 216243.0 | 2026-07-10 12:00:57 | 5 |
| yingdao_text_active_downstream | `ODS_DOUYINZONGHEBIAO` | ODS_抖音综合表 | C | source_like | 1428.0 | 2026-07-07 08:58:46 | 5 |
| yingdao_text_active_downstream | `douyinyunfeixian` | ODS_抖音_运费险账单数据_RPA | B | detail_like | 1305051.0 | 2026-07-10 01:02:52 | 5 |
| yingdao_text_active_downstream | `shangpinchapinglv` | 天猫-商品差评率明细 | C | detail_like | 115721.0 | 2026-07-10 12:00:57 | 5 |
| yingdao_text_active_downstream | `tianmaokuaidilanshouxinxibiao` | 天猫快递揽收信息表 | C | result_like | 395247.0 | 2026-07-09 09:40:10 | 5 |
| yingdao_text_active_downstream | `shoudanlijin` | 天猫-首单礼金 | C | detail_like | 672804.0 | 2026-07-10 12:01:07 | 5 |
| yingdao_text_active_downstream | `liuliangshuju` | 京东_商品明细sku流量数据 | C | detail_like | 108055.0 | 2026-07-10 08:23:34 | 5 |
| yingdao_text_active_downstream | `xunicang_kc` | 虚拟仓库存数据 | C | detail_like | 332726.0 | 2026-07-10 08:04:19 | 5 |
| yingdao_text_active_downstream | `jingdongxiaohsoushuju` | 京东佑美旗舰店_销售数据 | C | detail_like | 115777.0 | 2026-07-10 08:23:19 | 5 |
| yingdao_text_active_downstream | `jingzaoxiaoshouliuliangshuju` | 京东京造_sku销售流量数据 | C | detail_like | 14423.0 | 2026-07-10 08:49:34 | 5 |
| yingdao_text_active_downstream | `ods_dyyunfeixian` | ODS_抖音运费险_填报 | C | source_like | 190.0 | 2026-07-08 15:06:26 | 5 |
| yingdao_text_active_downstream | `pdd_sjzx_product_data_product_details` | 拼多多数据中心商品数据商品明细商品明细效果 | C | detail_like | 741630.0 | 2026-07-10 11:36:50 | 5 |
| yingdao_text_active_downstream | `shangpinpaihang_liuliangdata_day` | 按日流量数据 | C | detail_like | 450685.0 | 2026-07-10 08:19:06 | 5 |
| yingdao_text_active_downstream | `tianmaopingjiayouli` | 天猫-评价有礼 | C | detail_like | 74610.0 | 2026-07-10 12:01:49 | 5 |
| yingdao_text_active_downstream | `tianmaosixiaoshouxiaoshoushuju` | 天猫四小时_销售数据 | B | detail_like | 2618588.0 | 2026-07-10 09:42:00 | 5 |
| yingdao_text_active_downstream | `tianmoyingxiaotuoguanjinshiwutiandierban` | 天猫-营销托管近十五天第二版 | C | detail_like | 9374.0 | 2026-07-10 12:00:47 | 5 |
| yingdao_text_active_downstream | `zhongdianpinpaimingtongji` | 天猫-重点品排名统计-日排名 | C | detail_like | 111113.0 | 2026-07-10 11:14:13 | 5 |
| yingdao_text_active_downstream | `anrishoutaosousuo` | 按日手淘搜索_旧版 | C | detail_like | 80686.0 | 2026-07-10 08:19:06 | 5 |
| yingdao_text_active_downstream | `damopanshujuxin` | 天猫-达摩盘数据新 | C | detail_like | 557525.0 | 2026-07-10 12:01:17 | 5 |
| yingdao_text_active_downstream | `feiquanzhan_jjingdongziying` | 京东自营_非全站数据 | C | detail_like | 28647.0 | 2026-07-10 08:49:22 | 5 |
| yingdao_text_active_downstream | `jingdong_quanzhan` | 京东自营_全站 | C | detail_like | 1653.0 | 2026-07-10 08:49:43 | 5 |
| yingdao_text_active_downstream | `jingdongfeiquanzhantuiguanghuafei` | 京东佑美旗舰店_推广花费 | C | detail_like | 45596.0 | 2026-07-10 08:23:36 | 5 |
| yingdao_text_active_downstream | `jingdongquanzhantuiguanghuafei` | 京东佑美旗舰店_全站推广花费 | C | detail_like | 3748.0 | 2026-07-10 08:23:19 | 5 |
| yingdao_text_active_downstream | `jingdongziyingxiaoshouliuliangshuju` | 京东自营_销售流量数据 | C | detail_like | 163496.0 | 2026-07-10 08:49:10 | 5 |
| yingdao_text_active_downstream | `odsziyinghejingzaoshouhoushujubiao` | 京东售后数据 | C | detail_like | 214052.0 | 2026-07-10 08:49:56 | 5 |
| yingdao_text_active_downstream | `pdd_product_promotion_whole_store_hosting` | 拼多多-商品推广全店托管 | C | detail_like | 95664.0 | 2026-07-10 11:35:51 | 5 |
| yingdao_text_active_downstream | `pdd_product_promotion_whole_store_hosting_overview` | 拼多多-商品推广概况全店托管 | C | detail_like | 2560.0 | 2026-07-10 11:35:31 | 5 |
| yingdao_text_active_downstream | `pdd_promotion_reportproduct_promotion_dailyunit` | 拼多多推广报表商品推广日报单元 | C | detail_like | 628026.0 | 2026-07-10 11:36:48 | 5 |
| yingdao_text_active_downstream | `pinduoduoshoushoushuju` | ODS_拼多多售后数据 | C | detail_like | 2223875.0 | 2026-07-10 08:12:33 | 5 |
| yingdao_text_active_downstream | `shangpinlanshoumingxi` | 天猫-商品揽收明细 | C | detail_like | 15385.0 | 2026-07-10 12:01:49 | 5 |
| yingdao_text_active_downstream | `shangpintiyanfen` | 天猫-商品体验分 | C | detail_like | 446200.0 | 2026-07-10 12:00:57 | 5 |
| yingdao_text_active_downstream | `shipingid` | 视频id | C | detail_like | 1183360.0 | 2026-07-10 08:19:11 | 4 |
| yingdao_text_active_downstream | `shoutaosousuo_liuliangdata_day` | 按日手淘搜索流量数据 | C | source_like | 29626.0 | 2026-07-10 08:30:31 | 5 |
| yingdao_text_active_downstream | `taobaoke_liuliangdata_day` | 按日淘宝客流量数据 | C | source_like | 19503.0 | 2026-07-10 08:30:18 | 5 |
| yingdao_text_active_downstream | `taobaokejiuban` | 按日淘宝客_旧版 | C | detail_like | 62184.0 | 2026-07-10 08:19:01 | 5 |
| yingdao_text_active_downstream | `tianmaochaipinlvdingdanmingxibiao` | 天猫_商品差评订单明细 | C | detail_like | 774417.0 | 2026-07-10 12:01:17 | 5 |
| yingdao_text_active_downstream | `tianmaodamopanguanjianci` | 天猫-达摩盘-关键词 | C | detail_like | 22018.0 | 2026-07-10 09:03:22 | 5 |
| yingdao_text_active_downstream | `tianmaohongbaohexiao` | 天猫-红包核销 | C | detail_like | 804456.0 | 2026-07-10 12:01:07 | 5 |
| yingdao_text_active_downstream | `tianmaoliuliangzhengti` | 天猫-生意参谋-流量整体 | C | detail_like | 423064.0 | 2026-07-10 10:03:08 | 5 |
| yingdao_text_active_downstream | `tianmaopeifudakuan` | 天猫-赔付打款 | C | detail_like | 10258.0 | 2026-07-10 12:00:19 | 5 |
| yingdao_text_active_downstream | `tianmaopinzhituikuan` | 品质退款 | C | detail_like | 812568.0 | 2026-07-10 12:00:59 | 5 |
| yingdao_text_active_downstream | `tianmaoshengyicanmouliuliangxinban` | 天猫-生意参谋-流量来源-新版 | C | detail_like | 5948900.0 | 2026-07-10 10:04:52 | 5 |
| yingdao_text_active_downstream | `tianmaosixiaohouhuopinyunying` | 天猫佑美_四小时_货品运营主体列表 | C | detail_like | 0.0 | 2026-07-10 09:51:07 | 5 |
| yingdao_text_active_downstream | `tianmaosixiaoquanzhanjihuanliebiao` | 天猫佑美_四小时_全站计划列表 | C | detail_like | 826281.0 | 2026-07-10 09:51:58 | 5 |
| yingdao_text_active_downstream | `tianmaosixiaoshiguanjianci` | 天猫佑美_四小时_关键词单元列表 | C | detail_like | 1330487.0 | 2026-07-10 09:51:47 | 5 |
| yingdao_text_active_downstream | `tianmaosixiaoshoujingzhunrenqun` | 天猫佑美_四小时_精准人群主体列表 | C | detail_like | 207095.0 | 2026-07-10 09:51:46 | 5 |
| yingdao_text_active_downstream | `tianmaosixiaoshoushouhoushuju` | 天猫四小时_售后数据 | C | detail_like | 1795774.0 | 2026-07-10 09:39:59 | 5 |
| yingdao_text_active_downstream | `tianmaotaokeyongjin` | 天猫-淘客佣金 | C | detail_like | 1146098.0 | 2026-07-10 12:02:05 | 5 |
| yingdao_text_active_downstream | `tianmaotuiguangduanzhiliandong` | 天猫推广-短直联动 | C | detail_like | 723.0 | 2026-07-10 08:41:21 | 5 |
| yingdao_text_active_downstream | `tianmaoyingxiaofeiyongjinshitian` | 天猫-营销托管近十天 | C | detail_like | 35572.0 | 2026-07-10 12:01:09 | 5 |
| yingdao_text_active_downstream | `tianmaoyingxiaotuoguanfeiyong` | 天猫-营销托管 | C | detail_like | 391957.0 | 2026-07-10 08:30:05 | 5 |
| yingdao_text_active_downstream | `tuiguanghongbaofanhuan` | 拼多多-推广红包返还 | C | detail_like | 76126.0 | 2026-07-10 01:03:02 | 5 |
| yingdao_text_active_downstream | `xhsjg_global_ad_creative` | 小红书聚光-全局报表广告创意分日 | B | detail_like | 49011498.0 | 2026-07-09 14:55:54 | 5 |
| yingdao_text_active_downstream | `xhspgy_data_center_export` | 小红书蒲公英-数据中心导出 | C | export_like | 967071.0 | 2026-07-09 15:00:19 | 5 |

## 逐表方案

### DWS_抖音_SPU销售明细（`dws_douyin_spu_sales_detail`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：94013 / 2026-07-09 13:46:24
- 任务：2.2抖音_销售经营数据综合表-抖音_销售经营综合表【刷新】（Ghu44PRchu）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：pay_time
- 核心字段候选：__id, spbm, pay_time, account_amount, bhstghf, cgje, cgjejbm, cgjexbm

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `dws_douyin_spu_sales_detail__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | pay_time | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `dws_douyin_spu_sales_detail__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `dws_douyin_spu_sales_detail__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, spbm, pay_time, account_amount, bhstghf, cgje, cgjejbm, cgjexbm | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `dws_douyin_spu_sales_detail__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | sjssje, zyf, cgje, dyyfysjlhtxhd, account_amount, cwsdkcje | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `dws_douyin_spu_sales_detail__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | pay_time | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `sfaz`：是
- `xfzsfje`：499.0, 957.0, 2578.16, 389.93, 2373.4, 3872.0, 1257.94, 397.26


### 商品编码销售数据、流量数据、推广数据（`ud_3418004512502203_spbmxssjllsj`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：618104 / 2026-07-09 15:13:24
- 任务：3.dws_天猫销售经营综合数据清洗-商品编码销售数据、流量数据、推广数据【刷新】（tCQHRUr2lz）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：未识别
- 核心字段候选：__id, spbmpjmll, spbmpjmll1, bhscgje, cgje, cgjejbm, cgjexbm, je

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_3418004512502203_spbmxssjllsj__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | - | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_3418004512502203_spbmxssjllsj__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `ud_3418004512502203_spbmxssjllsj__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, spbmpjmll, spbmpjmll1, bhscgje, cgje, cgjejbm, cgjexbm, je | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_3418004512502203_spbmxssjllsj__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | je, ygsjxsje, yf, yfrgtmx, cgje, yyfzr | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |

枚举/状态字段样例：
- `sfbaz`：不包


### dwd_销售退货详情表（`ud_3418004512502203_dxsthxqb`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：S / result_like
- 行数/最近更新：24816626 / 2026-07-09 15:07:16
- 任务：2.dwd_淘宝数据清洗-dwd_销售退货详情表【刷新】（WsaMDlzNGI）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：未识别
- 核心字段候选：__id, spbmkcs, bhscgje, cgje, dgcb, fhcbh, je, yf

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_3418004512502203_dxsthxqb__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | - | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_3418004512502203_dxsthxqb__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `ud_3418004512502203_dxsthxqb__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, spbmkcs, bhscgje, cgje, dgcb, fhcbh, je, yf | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_3418004512502203_dxsthxqb__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | fhcbh, je, yyfzr, cgje, yf, thhxsje | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |

枚举/状态字段样例：
- `sfwljcp`：两季产品, 否
- `sfbaz`：不包, 否
- `question_type`：不想要了, 尺码没选对, 质量问题


### 2.3拼多多数据清洗（`ud_3418004512502203_n23pddsjqx`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：969324 / 2026-07-09 13:47:32
- 任务：2.2拼多多数据清洗-2.3拼多多数据清洗【刷新】（vTeCxTA2tz）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：pay_date
- 核心字段候选：__id, pay_date, cgje, cgjejbm, cgjexbm, je, sjtghf, transaction_amount_yuan

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_3418004512502203_n23pddsjqx__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | pay_date | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_3418004512502203_n23pddsjqx__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `ud_3418004512502203_n23pddsjqx__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, pay_date, cgje, cgjejbm, cgjexbm, je, sjtghf, transaction_amount_yuan | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_3418004512502203_n23pddsjqx__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | zfje, je, cgje, yf, transaction_amount_yuan, zgyf | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `ud_3418004512502203_n23pddsjqx__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | pay_date | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `sfcjbybt`：是
- `sfaz`：否, 是


### ODS_销售订单信息表(聚水潭奇门API)（`ods_api_jstqm_sale_order_info_f`）

- 范围：core_15
- 来源类型：api_ingestion；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：23312740 / 2026-07-09 03:49:20
- 任务：ods_api_jstqm_sale_order_info_f【EtlDevelop任务】（9hARYiuSyx）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, l_id, wms_co_id, as_id；业务日期：dt, send_date, pay_date
- 核心字段候选：__id, l_id, wms_co_id, as_id, outer_pay_id, so_id, shop_buyer_id, open_id

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ods_api_jstqm_sale_order_info_f__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | dt | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ods_api_jstqm_sale_order_info_f__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, l_id, wms_co_id, as_id | 检查候选主键非空和重复。 |
| `ods_api_jstqm_sale_order_info_f__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, l_id, wms_co_id, as_id, outer_pay_id, so_id, shop_buyer_id, open_id | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ods_api_jstqm_sale_order_info_f__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | free_amount, pay_amount, paid_amount, buyer_paid_amount, seller_income_amount, cb_finances | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `ods_api_jstqm_sale_order_info_f__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | dt | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `is_cod`：false
- `status`：Sent, Cancelled
- `shop_status`：TRADE_FINISHED, TRADE_CLOSED_BY_TAOBAO


### ODS_销售订单信息表(聚水潭奇门API)（`ods_api_jstqm_sale_order_info_du`）

- 范围：core_15
- 来源类型：api_ingestion；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：25408030 / 2026-07-09 03:33:13
- 任务：ODS_销售订单信息表(聚水潭奇门API)【连接器】（更新时间取数-可以补数据）（MvuyryYfyY）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：dt, __id, l_id, wms_co_id；业务日期：dt, send_date, pay_date
- 核心字段候选：dt, __id, l_id, wms_co_id, as_id, outer_pay_id, so_id, shop_buyer_id

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ods_api_jstqm_sale_order_info_du__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | dt | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ods_api_jstqm_sale_order_info_du__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | dt, __id, l_id, wms_co_id | 检查候选主键非空和重复。 |
| `ods_api_jstqm_sale_order_info_du__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | dt, __id, l_id, wms_co_id, as_id, outer_pay_id, so_id, shop_buyer_id | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ods_api_jstqm_sale_order_info_du__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | free_amount, pay_amount, paid_amount, buyer_paid_amount, seller_income_amount, cb_finances | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `ods_api_jstqm_sale_order_info_du__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | dt | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `is_cod`：false
- `status`：Split
- `shop_status`：TRADE_FINISHED


### DWD_抖音_订单销售明细（`ud_3418004512502203_ddyxsjyzhb`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：761271 / 2026-07-09 13:44:01
- 任务：2.1 DWD_抖音数据清洗综合表-DWD_抖音销售经营综合表【刷新】（lI6tx3AsC7）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, order_id, skuid, doudian_open_id；业务日期：pay_time, create_time
- 核心字段候选：__id, order_id, skuid, spbm, doudian_open_id, open_address_id, yuce_cube_shop_id, wms_co_id

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_3418004512502203_ddyxsjyzhb__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | pay_time | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_3418004512502203_ddyxsjyzhb__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, order_id, skuid, doudian_open_id | 检查候选主键非空和重复。 |
| `ud_3418004512502203_ddyxsjyzhb__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, order_id, skuid, spbm, doudian_open_id, open_address_id, yuce_cube_shop_id, wms_co_id | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_3418004512502203_ddyxsjyzhb__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | cgje, sjssje, nxyf, yf, dyyfysjlhtxhd, account_amount | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `ud_3418004512502203_ddyxsjyzhb__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | pay_time | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `xfzsfje`：89.9, 0.0, 380.0, 97.4, 2324.64, 1953.27
- `sfpj`：0
- `sfwljcp`：是, 否


### 天猫-销售计划总表（`ud_5179579576634064_tmxsjhzb`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：14890 / 2026-07-09 15:15:05
- 任务：天猫销售计划-天猫-销售计划总表【刷新】（s9Apa7nuXH）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：未识别
- 核心字段候选：__id, ygsjxsje, yyfzr, zgcb, zjcjje

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_5179579576634064_tmxsjhzb__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | - | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_5179579576634064_tmxsjhzb__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `ud_5179579576634064_tmxsjhzb__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, ygsjxsje, yyfzr, zgcb, zjcjje | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_5179579576634064_tmxsjhzb__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | zgcb, yyfzr, zjcjje, ygsjxsje | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |


### ODS_商品SKU信息表(聚水潭标准API)（`ods_api_jstbz_product_sku_info_f`）

- 范围：core_15
- 来源类型：api_ingestion；源表：
- 重要性/角色：A / detail_like
- 行数/最近更新：49492 / 2026-07-09 02:03:09
- 任务：ods_api_jstbz_product_sku_info_f【EtlDevelop任务】（4v6XI21730）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, sku_id, i_id, c_id；业务日期：dt, modified, created
- 核心字段候选：__id, sku_id, i_id, c_id, supplier_id, sku_code, supplier_sku_id, supplier_i_id

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ods_api_jstbz_product_sku_info_f__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | dt | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ods_api_jstbz_product_sku_info_f__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, sku_id, i_id, c_id | 检查候选主键非空和重复。 |
| `ods_api_jstbz_product_sku_info_f__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, sku_id, i_id, c_id, supplier_id, sku_code, supplier_sku_id, supplier_i_id | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ods_api_jstbz_product_sku_info_f__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | sale_price, cost_price, market_price, other_price_1, other_price_2, other_price_3 | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `ods_api_jstbz_product_sku_info_f__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | dt | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `enabled`：1, -1
- `is_series_number`：false
- `batch_enabled`：


### 2.2京东佑美旗舰店总综合表（`ud_3418004512502203_n22jdymqjdzz`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：112068 / 2026-07-09 13:41:58
- 任务：2.2京东佑美旗舰店_销售、售后、推广、流量综合表-2.2京东佑美旗舰店总综合表【刷新】（BRQxUQstRp）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：paymentconfirmtime
- 核心字段候选：__id, spbm, spbm1, paymentconfirmtime, cgje, sjysje, tkje, yf

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_3418004512502203_n22jdymqjdzz__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | paymentconfirmtime | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_3418004512502203_n22jdymqjdzz__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `ud_3418004512502203_n22jdymqjdzz__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, spbm, spbm1, paymentconfirmtime, cgje, sjysje, tkje, yf | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_3418004512502203_n22jdymqjdzz__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | paymentconfirmtime, sjysje, tkje, cgje, yf, zfje | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `ud_3418004512502203_n22jdymqjdzz__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | paymentconfirmtime | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `是否安装`：是


### 3.京东自营和京造综合表（`ud_3418004512502203_n3jdzyhjzzhb`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：65696 / 2026-07-09 13:39:24
- 任务：3.DWD京东自营和京造销售流量推广数据综合表-3.京东自营和京造综合表【刷新】（7lAvjA2Tc5）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, sku；业务日期：未识别
- 核心字段候选：__id, sku, cgje1, cjje, cjje1, dgcb, dgcb1, ghje

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_3418004512502203_n3jdzyhjzzhb__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | - | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_3418004512502203_n3jdzyhjzzhb__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, sku | 检查候选主键非空和重复。 |
| `ud_3418004512502203_n3jdzyhjzzhb__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, sku, cgje1, cjje, cjje1, dgcb, dgcb1, ghje | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_3418004512502203_n3jdzyhjzzhb__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | cjje, cjje1, dgcb, cgje1, ghje, yf | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |

枚举/状态字段样例：
- `sfqc`：清仓


### STD_抖音_订单销售明细（`ud_3418004512502203_sxssjqx`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：824838 / 2026-07-09 05:34:26
- 任务：1.1 STD_抖音销售清洗表-STD_销售数据清洗【刷新】（5aMpRAhBmy）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, order_id, skuid, doudian_open_id；业务日期：pay_time, create_time
- 核心字段候选：__id, order_id, spbm, skuid, doudian_open_id, open_address_id, yuce_cube_shop_id, pay_time

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_3418004512502203_sxssjqx__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | pay_time | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_3418004512502203_sxssjqx__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, order_id, skuid, doudian_open_id | 检查候选主键非空和重复。 |
| `ud_3418004512502203_sxssjqx__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, order_id, spbm, skuid, doudian_open_id, open_address_id, yuce_cube_shop_id, pay_time | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_3418004512502203_sxssjqx__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | xfzsfje, cjje, sjssje, promotion_talent_amount, promotion_pay_amount, promotion_redpack_amount | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `ud_3418004512502203_sxssjqx__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | pay_time | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `xfzsfje`：0.0, 406.0, 89.9, 376.89, 74.93, 385.0, 411.16
- `sfpj`：0
- `sfwljcp`：是, 否


### 天猫-推广总表（`ud_5179579576634064_tmtgzb`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：281713 / 2026-07-09 14:09:52
- 任务：天猫-推广-天猫-推广总表【刷新】（tIae4qir6w）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：未识别
- 核心字段候选：__id, bdyf, cgje, qztghf, zcjje, zgcb, zjcjje, zjjgcb

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_5179579576634064_tmtgzb__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | - | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_5179579576634064_tmtgzb__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `ud_5179579576634064_tmtgzb__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, bdyf, cgje, qztghf, zcjje, zgcb, zjcjje, zjjgcb | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_5179579576634064_tmtgzb__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | zgcb, zcjje, zjjgcb, zjcjje, bdyf, yyfzr | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |


### ODS_销售订单列表信息表(抖店API)（`ods_api_dd_sale_order_list_info_du`）

- 范围：core_15
- 来源类型：api_ingestion；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：3226101 / 2026-07-09 05:00:00
- 任务：ODS_销售订单列表信息表(抖店API)【连接器】（mnMTqusbga）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：dt, __id, accept_order_status, shop_id；业务日期：dt, pay_time, order_expire_time
- 核心字段候选：dt, __id, shop_id, open_id, order_id, app_id, sku_order_list, doudian_open_id

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ods_api_dd_sale_order_list_info_du__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | dt | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ods_api_dd_sale_order_list_info_du__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | dt, __id, accept_order_status, shop_id | 检查候选主键非空和重复。 |
| `ods_api_dd_sale_order_list_info_du__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | dt, __id, shop_id, open_id, order_id, app_id, sku_order_list, doudian_open_id | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ods_api_dd_sale_order_list_info_du__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | channel_payment_no, order_amount, pay_amount, post_amount, post_insurance_amount, modify_amount | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `ods_api_dd_sale_order_list_info_du__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | dt | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `accept_order_status`：2
- `order_status`：4
- `order_status_desc`：已关闭


### std_销售订单信息表（`ud_3418004512502203_sxsddxxb`）

- 范围：core_15
- 来源类型：bi_or_unknown；源表：
- 重要性/角色：A / result_like
- 行数/最近更新：24884809 / 2026-07-09 06:35:34
- 任务：1.1std_淘宝销售和售后数据清洗-std_销售订单信息表【刷新】（QUMvyo4abs）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, l_id, wms_co_id, so_id；业务日期：modified, send_date, pay_date
- 核心字段候选：__id, l_id, wms_co_id, so_id, open_id, o_id, shop_id, co_id

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ud_3418004512502203_sxsddxxb__yesterday_biz_date_row_count_nonzero` | 昨天业务日期行数存在 | 优先使用 BI 表规则「单日行数，固定值」，日期参数传昨天业务日期；无日期字段时退化为任务产出行数 > 0。SQL 仅兜底。 | modified | 检查昨天业务日期是否有数据，避免结果表空跑。 |
| `ud_3418004512502203_sxsddxxb__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, l_id, wms_co_id, so_id | 检查候选主键非空和重复。 |
| `ud_3418004512502203_sxsddxxb__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | __id, l_id, wms_co_id, so_id, open_id, o_id, shop_id, co_id | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |
| `ud_3418004512502203_sxsddxxb__amount_fields_format_and_non_negative` | 金额字段格式/非负 | 数值字段优先使用 BI 字段规则「最小值/最大值」及波动类规则；文本金额字段先做空值/格式确认，数值可转换性用 SQL 兜底。 | free_amount, pay_amount, paid_amount, buyer_paid_amount, seller_income_amount, khbjyf | 检查金额、成本、推广费字段是否可转数字，以及一般金额是否出现负数。 |
| `ud_3418004512502203_sxsddxxb__biz_date_castable` | 业务日期格式 | 字段日期格式内置规则或自定义 SQL。 | modified | 检查业务日期字段非空且可作为日期使用。 |

枚举/状态字段样例：
- `status`：Sent
- `shop_status`：TRADE_FINISHED
- `receiver_state`：广东省, 河南省, 四川省, 湖南省, 浙江省, 广西壮族自治区, 山东省


### 天猫综合表（`huizongbiao`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：汇总表
- 重要性/角色：A / source_like
- 行数/最近更新：9832.0 / 2026-07-10 00:30:18
- 任务：汇总表【迁移】（dd65mm262W）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID；业务日期：未识别
- 核心字段候选：店铺名称, 商品ID

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `huizongbiao__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `huizongbiao__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `huizongbiao__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 店铺名称, 商品ID | 检查字段数量和关键字段是否发生变化。 |
| `huizongbiao__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID | 检查候选主键非空和重复。 |
| `huizongbiao__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 店铺名称, 商品ID | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-销售计划表（`tianmaoxiaoshoujihuabiao`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-销售计划表
- 重要性/角色：B / source_like
- 行数/最近更新：15695.0 / 2026-07-06 16:29:26
- 任务：天猫-销售计划表【迁移】（2LqykyNRIR）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 宝贝ID；业务日期：当月日期, 下周日期
- 核心字段候选：当月日期, 下周日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaoxiaoshoujihuabiao__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaoxiaoshoujihuabiao__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaoxiaoshoujihuabiao__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 当月日期, 下周日期 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaoxiaoshoujihuabiao__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 宝贝ID | 检查候选主键非空和重复。 |
| `tianmaoxiaoshoujihuabiao__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 当月日期, 下周日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫_保证金数据拆分（`tianmaobaozhengjinxiangmucahifen`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫_保证金数据拆分
- 重要性/角色：B / source_like
- 行数/最近更新：12845.0 / 2026-07-06 15:04:20
- 任务：天猫_保证金数据拆分【迁移】（UHAP7pVbut）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 业务订单号, 订单id/处罚id；业务日期：时间
- 核心字段候选：时间, 金额元, 业务订单号, 订单id/处罚id

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaobaozhengjinxiangmucahifen__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaobaozhengjinxiangmucahifen__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaobaozhengjinxiangmucahifen__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 时间, 金额元, 业务订单号, 订单id/处罚id | 检查字段数量和关键字段是否发生变化。 |
| `tianmaobaozhengjinxiangmucahifen__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 业务订单号, 订单id/处罚id | 检查候选主键非空和重复。 |
| `tianmaobaozhengjinxiangmucahifen__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 时间, 金额元, 业务订单号, 订单id/处罚id | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 拼多多推广中心推广报表店铺推广明星店铺单元（`pdd_tgzx_promotion_report_store_promotion_store_unit`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：pdd_tgzx_promotion_report_store_promotion_store_unit
- 重要性/角色：C / detail_like
- 行数/最近更新：495.0 / 2026-07-10 11:35:19
- 任务：拼多多推广中心推广报表店铺推广明星店铺单元【迁移】（AIaML9Envt）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, id, corp_id, shop_no；业务日期：business_date, gather_time, insert_time
- 核心字段候选：product_collection_quantity, store_followers, store_name, shop_no, each_transaction_amount, business_date, gather_time

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `pdd_tgzx_promotion_report_store_promotion_store_unit__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `pdd_tgzx_promotion_report_store_promotion_store_unit__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `pdd_tgzx_promotion_report_store_promotion_store_unit__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | product_collection_quantity, store_followers, store_name, shop_no, each_transaction_amount | 检查字段数量和关键字段是否发生变化。 |
| `pdd_tgzx_promotion_report_store_promotion_store_unit__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, id, corp_id, shop_no | 检查候选主键非空和重复。 |
| `pdd_tgzx_promotion_report_store_promotion_store_unit__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | product_collection_quantity, store_followers, store_name, shop_no, each_transaction_amount, business_date, gather_time | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `has_it_been_deleted`：


### 天猫商品ID采购负责人综合表（`tianmaoshangpinIDcaigoufuzeren`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫商品ID采购负责人综合表
- 重要性/角色：B / source_like
- 行数/最近更新：2032.0 / 2026-07-07 11:05:48
- 任务：天猫商品ID采购负责人综合表【迁移】（ksgnfDHEJd）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品编码；业务日期：未识别
- 核心字段候选：商品编码

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaoshangpinIDcaigoufuzeren__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaoshangpinIDcaigoufuzeren__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaoshangpinIDcaigoufuzeren__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品编码 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaoshangpinIDcaigoufuzeren__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品编码 | 检查候选主键非空和重复。 |
| `tianmaoshangpinIDcaigoufuzeren__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品编码 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### ODS_佑美拼多多销售订单数据（`ODS_YOUMEIPDDxiaoshoudingdanbiao`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：ODS_佑美拼多多销售订单数据
- 重要性/角色：REVIEW / detail_like
- 行数/最近更新：6961206.0 / 2026-07-10 08:23:33
- 任务：ODS_佑美拼多多销售订单数据【迁移】（l0Koxecy0d）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品编码, 线上订单号, 店铺款式编码；业务日期：付款日期, 发货日期, 下单时间
- 核心字段候选：付款日期, 抵扣金额, 商品金额, 商品编码, 线上订单号, 店铺款式编码, 商品名称, 店铺名称

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ODS_YOUMEIPDDxiaoshoudingdanbiao__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `ODS_YOUMEIPDDxiaoshoudingdanbiao__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `ODS_YOUMEIPDDxiaoshoudingdanbiao__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 付款日期, 抵扣金额, 商品金额, 商品编码, 线上订单号 | 检查字段数量和关键字段是否发生变化。 |
| `ODS_YOUMEIPDDxiaoshoudingdanbiao__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品编码, 线上订单号, 店铺款式编码 | 检查候选主键非空和重复。 |
| `ODS_YOUMEIPDDxiaoshoudingdanbiao__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 付款日期, 抵扣金额, 商品金额, 商品编码, 线上订单号, 店铺款式编码, 商品名称, 店铺名称 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `订单类型`：普通订单
- `状态`：已发货
- `店铺状态`：交易成功


### 天猫-商品品退率明细（`shangpinpintuilv`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-商品品退率明细
- 重要性/角色：B / detail_like
- 行数/最近更新：216243.0 / 2026-07-10 12:00:57
- 任务：天猫-商品品退率明细【迁移】（2su02FO3o5）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品编码/名称, 签收订单量；业务日期：日期
- 核心字段候选：商品编码/名称, 商品销量, 商品销售金额/元, 首次品退金额/元, 日期, 签收订单量

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `shangpinpintuilv__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `shangpinpintuilv__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `shangpinpintuilv__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品编码/名称, 商品销量, 商品销售金额/元, 首次品退金额/元, 日期 | 检查字段数量和关键字段是否发生变化。 |
| `shangpinpintuilv__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品编码/名称, 签收订单量 | 检查候选主键非空和重复。 |
| `shangpinpintuilv__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品编码/名称, 商品销量, 商品销售金额/元, 首次品退金额/元, 日期, 签收订单量 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### ODS_抖音综合表（`ODS_DOUYINZONGHEBIAO`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：ODS_抖音综合表
- 重要性/角色：C / source_like
- 行数/最近更新：1428.0 / 2026-07-07 08:58:46
- 任务：ODS_抖音综合表【迁移】（mJ44GUeDiF）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品编码；业务日期：未识别
- 核心字段候选：店铺名称, 商品编码

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ODS_DOUYINZONGHEBIAO__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `ODS_DOUYINZONGHEBIAO__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `ODS_DOUYINZONGHEBIAO__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 店铺名称, 商品编码 | 检查字段数量和关键字段是否发生变化。 |
| `ODS_DOUYINZONGHEBIAO__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品编码 | 检查候选主键非空和重复。 |
| `ODS_DOUYINZONGHEBIAO__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 店铺名称, 商品编码 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### ODS_抖音_运费险账单数据_RPA（`douyinyunfeixian`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：抖音-运费险账单数据
- 重要性/角色：B / detail_like
- 行数/最近更新：1305051.0 / 2026-07-10 01:02:52
- 任务：抖音-运费险账单数据【迁移】（sXAhYSBWoO）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 订单编号；业务日期：下单时间, 动账时间
- 核心字段候选：订单编号, 下单时间, 动账时间

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `douyinyunfeixian__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `douyinyunfeixian__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `douyinyunfeixian__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 订单编号, 下单时间, 动账时间 | 检查字段数量和关键字段是否发生变化。 |
| `douyinyunfeixian__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 订单编号 | 检查候选主键非空和重复。 |
| `douyinyunfeixian__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 订单编号, 下单时间, 动账时间 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-商品差评率明细（`shangpinchapinglv`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-商品差评率明细
- 重要性/角色：C / detail_like
- 行数/最近更新：115721.0 / 2026-07-10 12:00:57
- 任务：天猫-商品差评率明细【迁移】（9re4KEg377）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品名称/编码, 确认收货订单量；业务日期：日期
- 核心字段候选：商品名称/编码, 商品销量, 商品销售金额/元, 商品差评率, 商品差评量, 确认收货订单量, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `shangpinchapinglv__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `shangpinchapinglv__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `shangpinchapinglv__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品名称/编码, 商品销量, 商品销售金额/元, 商品差评率, 商品差评量 | 检查字段数量和关键字段是否发生变化。 |
| `shangpinchapinglv__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品名称/编码, 确认收货订单量 | 检查候选主键非空和重复。 |
| `shangpinchapinglv__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品名称/编码, 商品销量, 商品销售金额/元, 商品差评率, 商品差评量, 确认收货订单量, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫快递揽收信息表（`tianmaokuaidilanshouxinxibiao`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫快递揽收信息表
- 重要性/角色：C / result_like
- 行数/最近更新：395247.0 / 2026-07-09 09:40:10
- 任务：天猫快递揽收信息表【迁移】（KFATFW5AWM）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 内部订单号, 订单类型, 线上订单号；业务日期：最新物流时间, 平台付款时间, 计划发货时间
- 核心字段候选：内部订单号, 订单类型, 线上订单号, 店铺, 订单状态, 最新物流时间, 平台付款时间, 计划发货时间

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaokuaidilanshouxinxibiao__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaokuaidilanshouxinxibiao__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaokuaidilanshouxinxibiao__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 内部订单号, 订单类型, 线上订单号, 店铺, 订单状态 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaokuaidilanshouxinxibiao__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 内部订单号, 订单类型, 线上订单号 | 检查候选主键非空和重复。 |
| `tianmaokuaidilanshouxinxibiao__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 内部订单号, 订单类型, 线上订单号, 店铺, 订单状态, 最新物流时间, 平台付款时间, 计划发货时间 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `订单类型`：普通订单
- `订单状态`：已发货
- `包裹状态`：运输中


### 天猫-首单礼金（`shoudanlijin`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-首单礼金
- 重要性/角色：C / detail_like
- 行数/最近更新：672804.0 / 2026-07-10 12:01:07
- 任务：天猫-首单礼金【迁移】（2BgNQLUOly）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 父订单ID, 商品ID；业务日期：日期
- 核心字段候选：商品名称, 父订单ID, 商品ID, 支付金额, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `shoudanlijin__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `shoudanlijin__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `shoudanlijin__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品名称, 父订单ID, 商品ID, 支付金额, 日期 | 检查字段数量和关键字段是否发生变化。 |
| `shoudanlijin__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 父订单ID, 商品ID | 检查候选主键非空和重复。 |
| `shoudanlijin__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品名称, 父订单ID, 商品ID, 支付金额, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 京东_商品明细sku流量数据（`liuliangshuju`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：京东_商品明细sku流量数据
- 重要性/角色：C / detail_like
- 行数/最近更新：108055.0 / 2026-07-10 08:23:34
- 任务：京东_商品明细sku流量数据【迁移】（XOeOLYTRVz）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID；业务日期：最近上架时间, 日期
- 核心字段候选：商品ID, 商品名称, 商品关注数, 加购商品件数, 成交商品件数, 成交金额, 最近上架时间, 下单商品件数

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `liuliangshuju__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `liuliangshuju__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `liuliangshuju__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品ID, 商品名称, 商品关注数, 加购商品件数, 成交商品件数 | 检查字段数量和关键字段是否发生变化。 |
| `liuliangshuju__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID | 检查候选主键非空和重复。 |
| `liuliangshuju__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品ID, 商品名称, 商品关注数, 加购商品件数, 成交商品件数, 成交金额, 最近上架时间, 下单商品件数 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 虚拟仓库存数据（`xunicang_kc`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：虚拟仓库存数据
- 重要性/角色：C / detail_like
- 行数/最近更新：332726.0 / 2026-07-10 08:04:19
- 任务：虚拟仓库存数据【迁移】（TycXab0KdW）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品编码, 款式编码, 订单占有数；业务日期：更新时间
- 核心字段候选：商品名称, 商品编码, 款式编码, 订单占有数, 虚拟仓库存金额, 更新时间

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `xunicang_kc__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `xunicang_kc__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `xunicang_kc__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品名称, 商品编码, 款式编码, 订单占有数, 虚拟仓库存金额 | 检查字段数量和关键字段是否发生变化。 |
| `xunicang_kc__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品编码, 款式编码, 订单占有数 | 检查候选主键非空和重复。 |
| `xunicang_kc__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品名称, 商品编码, 款式编码, 订单占有数, 虚拟仓库存金额, 更新时间 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `状态`：生效


### 京东佑美旗舰店_销售数据（`jingdongxiaohsoushuju`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：京东佑美旗舰店_销售数据
- 重要性/角色：C / detail_like
- 行数/最近更新：115777.0 / 2026-07-10 08:23:19
- 任务：京东佑美旗舰店_销售数据【迁移】（LgsTeae8S9）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 订单号, SKU, 订单金额；业务日期：下单时间, 付款时间
- 核心字段候选：订单号, SKU, 商品名称, 优惠前金额, 成交商品件数, 优惠金额, 订单金额, 下单时间

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `jingdongxiaohsoushuju__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `jingdongxiaohsoushuju__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `jingdongxiaohsoushuju__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 订单号, SKU, 商品名称, 优惠前金额, 成交商品件数 | 检查字段数量和关键字段是否发生变化。 |
| `jingdongxiaohsoushuju__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 订单号, SKU, 订单金额 | 检查候选主键非空和重复。 |
| `jingdongxiaohsoushuju__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 订单号, SKU, 商品名称, 优惠前金额, 成交商品件数, 优惠金额, 订单金额, 下单时间 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 京东京造_sku销售流量数据（`jingzaoxiaoshouliuliangshuju`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：京东京造_sku销售流量数据
- 重要性/角色：C / detail_like
- 行数/最近更新：14423.0 / 2026-07-10 08:49:34
- 任务：京东京造_sku销售流量数据【迁移】（qXaEHo33Z1）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：日期
- 核心字段候选：商品信息, 成交金额, 加购商品件数, 成交商品件数, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `jingzaoxiaoshouliuliangshuju__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `jingzaoxiaoshouliuliangshuju__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `jingzaoxiaoshouliuliangshuju__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品信息, 成交金额, 加购商品件数, 成交商品件数, 日期 | 检查字段数量和关键字段是否发生变化。 |
| `jingzaoxiaoshouliuliangshuju__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `jingzaoxiaoshouliuliangshuju__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品信息, 成交金额, 加购商品件数, 成交商品件数, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### ODS_抖音运费险_填报（`ods_dyyunfeixian`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：ods-抖音运费险
- 重要性/角色：C / source_like
- 行数/最近更新：190.0 / 2026-07-08 15:06:26
- 任务：ods-抖音运费险【迁移】（dTuaRL2T1U）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 投保单号, 订单编号；业务日期：下单时间, 动账时间
- 核心字段候选：订单编号, 下单时间, 动账时间, 店铺名称

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `ods_dyyunfeixian__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `ods_dyyunfeixian__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `ods_dyyunfeixian__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 订单编号, 下单时间, 动账时间, 店铺名称 | 检查字段数量和关键字段是否发生变化。 |
| `ods_dyyunfeixian__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 投保单号, 订单编号 | 检查候选主键非空和重复。 |
| `ods_dyyunfeixian__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 订单编号, 下单时间, 动账时间, 店铺名称 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 拼多多数据中心商品数据商品明细商品明细效果（`pdd_sjzx_product_data_product_details`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：pdd_sjzx_product_data_product_details
- 重要性/角色：C / detail_like
- 行数/最近更新：741630.0 / 2026-07-10 11:36:50
- 任务：拼多多数据中心商品数据商品明细商品明细效果【迁移】（QiasZaRhiR）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, id, corp_id, commodity_id；业务日期：business_date, gather_time, insert_time
- 核心字段候选：commodity_id, product_information, number_of_users_who_collect_products, product_views, product_visitors_num, store_name, shop_no, completed_orders

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `pdd_sjzx_product_data_product_details__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `pdd_sjzx_product_data_product_details__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `pdd_sjzx_product_data_product_details__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | commodity_id, product_information, number_of_users_who_collect_products, product_views, product_visitors_num | 检查字段数量和关键字段是否发生变化。 |
| `pdd_sjzx_product_data_product_details__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, id, corp_id, commodity_id | 检查候选主键非空和重复。 |
| `pdd_sjzx_product_data_product_details__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | commodity_id, product_information, number_of_users_who_collect_products, product_views, product_visitors_num, store_name, shop_no, completed_orders | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 按日流量数据（`shangpinpaihang_liuliangdata_day`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：按日流量数据
- 重要性/角色：C / detail_like
- 行数/最近更新：450685.0 / 2026-07-10 08:19:06
- 任务：按日流量数据【迁移】（4d6xB5qWaD）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID, 商品ID1；业务日期：日期
- 核心字段候选：日期, 商品名称, 商品ID, 商品ID1, 商品状态, 支付金额, 退款金额, 老买家支付金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `shangpinpaihang_liuliangdata_day__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `shangpinpaihang_liuliangdata_day__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `shangpinpaihang_liuliangdata_day__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期, 商品名称, 商品ID, 商品ID1, 商品状态 | 检查字段数量和关键字段是否发生变化。 |
| `shangpinpaihang_liuliangdata_day__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID, 商品ID1 | 检查候选主键非空和重复。 |
| `shangpinpaihang_liuliangdata_day__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期, 商品名称, 商品ID, 商品ID1, 商品状态, 支付金额, 退款金额, 老买家支付金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `商品状态`：


### 天猫-评价有礼（`tianmaopingjiayouli`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-评价有礼
- 重要性/角色：C / detail_like
- 行数/最近更新：74610.0 / 2026-07-10 12:01:49
- 任务：天猫-评价有礼【迁移】（FQsL4E0jwT）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 活动id, 评价id, 商品id；业务日期：评价时间, 发放时间
- 核心字段候选：评价时间, 发放金额, 发放时间, 商品id, 订单id, 店铺名称

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaopingjiayouli__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaopingjiayouli__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaopingjiayouli__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 评价时间, 发放金额, 发放时间, 商品id, 订单id | 检查字段数量和关键字段是否发生变化。 |
| `tianmaopingjiayouli__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 活动id, 评价id, 商品id | 检查候选主键非空和重复。 |
| `tianmaopingjiayouli__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 评价时间, 发放金额, 发放时间, 商品id, 订单id, 店铺名称 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫四小时_销售数据（`tianmaosixiaoshouxiaoshoushuju`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫四小时_销售数据
- 重要性/角色：B / detail_like
- 行数/最近更新：2618588.0 / 2026-07-10 09:42:00
- 任务：天猫四小时_销售数据【迁移】（hw6NL2SdrE）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 内部订单号, 线上订单号, 快递单号；业务日期：下单时间, 付款日期, 发货日期
- 核心字段候选：内部订单号, 线上订单号, 店铺编号, 店铺名称, 店铺简称, 店铺分组, 店铺主账号, 下单时间

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaosixiaoshouxiaoshoushuju__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaosixiaoshouxiaoshoushuju__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaosixiaoshouxiaoshoushuju__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 内部订单号, 线上订单号, 店铺编号, 店铺名称, 店铺简称 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaosixiaoshouxiaoshoushuju__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 内部订单号, 线上订单号, 快递单号 | 检查候选主键非空和重复。 |
| `tianmaosixiaoshouxiaoshoushuju__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 内部订单号, 线上订单号, 店铺编号, 店铺名称, 店铺简称, 店铺分组, 店铺主账号, 下单时间 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `状态`：取消, 被拆分, 发货中
- `店铺状态`：
- `异常类型`：


### 天猫-营销托管近十五天第二版（`tianmoyingxiaotuoguanjinshiwutiandierban`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-营销托管近十五天第二版
- 重要性/角色：C / detail_like
- 行数/最近更新：9374.0 / 2026-07-10 12:00:47
- 任务：天猫-营销托管近十五天第二版【迁移】（3D6d7Qe8iq）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 预估成交订单量, 当日成交订单量, 周期累计成交订单量；业务日期：日期
- 核心字段候选：商品, 预估成交订单量, 当日成交订单量, 当日成交金额, 周期累计成交订单量, 周期累计成交金额, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmoyingxiaotuoguanjinshiwutiandierban__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmoyingxiaotuoguanjinshiwutiandierban__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmoyingxiaotuoguanjinshiwutiandierban__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品, 预估成交订单量, 当日成交订单量, 当日成交金额, 周期累计成交订单量 | 检查字段数量和关键字段是否发生变化。 |
| `tianmoyingxiaotuoguanjinshiwutiandierban__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 预估成交订单量, 当日成交订单量, 周期累计成交订单量 | 检查候选主键非空和重复。 |
| `tianmoyingxiaotuoguanjinshiwutiandierban__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品, 预估成交订单量, 当日成交订单量, 当日成交金额, 周期累计成交订单量, 周期累计成交金额, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-重点品排名统计-日排名（`zhongdianpinpaimingtongji`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-重点品排名统计-日排名
- 重要性/角色：C / detail_like
- 行数/最近更新：111113.0 / 2026-07-10 11:14:13
- 任务：天猫-重点品排名统计-日排名【迁移】（kRaOyaiXTH）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID；业务日期：日期-日, 日期-周, 日期-月
- 核心字段候选：商品ID, 商品名称, 日期-日, 日期-周, 日期-月

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `zhongdianpinpaimingtongji__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `zhongdianpinpaimingtongji__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `zhongdianpinpaimingtongji__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品ID, 商品名称, 日期-日, 日期-周, 日期-月 | 检查字段数量和关键字段是否发生变化。 |
| `zhongdianpinpaimingtongji__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID | 检查候选主键非空和重复。 |
| `zhongdianpinpaimingtongji__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品ID, 商品名称, 日期-日, 日期-周, 日期-月 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 按日手淘搜索_旧版（`anrishoutaosousuo`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：按日手淘搜索_旧版
- 重要性/角色：C / detail_like
- 行数/最近更新：80686.0 / 2026-07-10 08:19:06
- 任务：按日手淘搜索_旧版【迁移】（O8qSgo2Xqg）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID；业务日期：日期
- 核心字段候选：日期, 商品名称, 商品ID, 支付金额, 微详情引导支付金额, 店铺名称

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `anrishoutaosousuo__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `anrishoutaosousuo__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `anrishoutaosousuo__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期, 商品名称, 商品ID, 支付金额, 微详情引导支付金额 | 检查字段数量和关键字段是否发生变化。 |
| `anrishoutaosousuo__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID | 检查候选主键非空和重复。 |
| `anrishoutaosousuo__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期, 商品名称, 商品ID, 支付金额, 微详情引导支付金额, 店铺名称 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-达摩盘数据新（`damopanshujuxin`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-达摩盘数据新
- 重要性/角色：C / detail_like
- 行数/最近更新：557525.0 / 2026-07-10 12:01:17
- 任务：天猫-达摩盘数据新【迁移】（S4OKHd96oN）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 宝贝ID；业务日期：日期
- 核心字段候选：日期, 支付金额, 预售支付金额, 营销推广引导总成交金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `damopanshujuxin__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `damopanshujuxin__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `damopanshujuxin__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期, 支付金额, 预售支付金额, 营销推广引导总成交金额 | 检查字段数量和关键字段是否发生变化。 |
| `damopanshujuxin__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 宝贝ID | 检查候选主键非空和重复。 |
| `damopanshujuxin__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期, 支付金额, 预售支付金额, 营销推广引导总成交金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 京东自营_非全站数据（`feiquanzhan_jjingdongziying`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：京东自营_非全站数据
- 重要性/角色：C / detail_like
- 行数/最近更新：28647.0 / 2026-07-10 08:49:22
- 任务：京东自营_非全站数据【迁移】（0H6vA8a1eg）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, SKU ID, SKU 名称, 总订单行；业务日期：点击时间
- 核心字段候选：SKU ID, SKU 名称, 点击时间, 总订单行, 总订单金额, 平均订单成本, 直接订单行, 直接订单金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `feiquanzhan_jjingdongziying__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `feiquanzhan_jjingdongziying__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `feiquanzhan_jjingdongziying__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | SKU ID, SKU 名称, 点击时间, 总订单行, 总订单金额 | 检查字段数量和关键字段是否发生变化。 |
| `feiquanzhan_jjingdongziying__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, SKU ID, SKU 名称, 总订单行 | 检查候选主键非空和重复。 |
| `feiquanzhan_jjingdongziying__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | SKU ID, SKU 名称, 点击时间, 总订单行, 总订单金额, 平均订单成本, 直接订单行, 直接订单金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 京东自营_全站（`jingdong_quanzhan`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：京东自营_全站
- 重要性/角色：C / detail_like
- 行数/最近更新：1653.0 / 2026-07-10 08:49:43
- 任务：京东自营_全站【迁移】（364O6KqVg7）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, SPU ID, 全站订单行, 全站订单成本；业务日期：日期
- 核心字段候选：日期, 商品计划名称, 全站订单行, 全站订单成本

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `jingdong_quanzhan__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `jingdong_quanzhan__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `jingdong_quanzhan__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期, 商品计划名称, 全站订单行, 全站订单成本 | 检查字段数量和关键字段是否发生变化。 |
| `jingdong_quanzhan__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, SPU ID, 全站订单行, 全站订单成本 | 检查候选主键非空和重复。 |
| `jingdong_quanzhan__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期, 商品计划名称, 全站订单行, 全站订单成本 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 京东佑美旗舰店_推广花费（`jingdongfeiquanzhantuiguanghuafei`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：京东佑美旗舰店_推广花费
- 重要性/角色：C / detail_like
- 行数/最近更新：45596.0 / 2026-07-10 08:23:36
- 任务：京东佑美旗舰店_推广花费【迁移】（5wwtEDpPYu）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, SKU ID, SKU 名称, 总订单行；业务日期：点击时间, '当前时间'
- 核心字段候选：SKU ID, SKU 名称, 点击时间, '当前时间', 总订单行, 总订单金额, 平均订单成本, 直接订单行

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `jingdongfeiquanzhantuiguanghuafei__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `jingdongfeiquanzhantuiguanghuafei__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `jingdongfeiquanzhantuiguanghuafei__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | SKU ID, SKU 名称, 点击时间, '当前时间', 总订单行 | 检查字段数量和关键字段是否发生变化。 |
| `jingdongfeiquanzhantuiguanghuafei__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, SKU ID, SKU 名称, 总订单行 | 检查候选主键非空和重复。 |
| `jingdongfeiquanzhantuiguanghuafei__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | SKU ID, SKU 名称, 点击时间, '当前时间', 总订单行, 总订单金额, 平均订单成本, 直接订单行 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 京东佑美旗舰店_全站推广花费（`jingdongquanzhantuiguanghuafei`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：京东佑美旗舰店_全站推广花费
- 重要性/角色：C / detail_like
- 行数/最近更新：3748.0 / 2026-07-10 08:23:19
- 任务：京东佑美旗舰店_全站推广花费【迁移】（kZKsV4jeZp）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, SPU ID, 全站订单行, 全站订单成本；业务日期：日期, '当前时间'
- 核心字段候选：日期, '当前时间', 商品计划名称, 全站订单行, 全站订单成本

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `jingdongquanzhantuiguanghuafei__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `jingdongquanzhantuiguanghuafei__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `jingdongquanzhantuiguanghuafei__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期, '当前时间', 商品计划名称, 全站订单行, 全站订单成本 | 检查字段数量和关键字段是否发生变化。 |
| `jingdongquanzhantuiguanghuafei__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, SPU ID, 全站订单行, 全站订单成本 | 检查候选主键非空和重复。 |
| `jingdongquanzhantuiguanghuafei__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期, '当前时间', 商品计划名称, 全站订单行, 全站订单成本 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 京东自营_销售流量数据（`jingdongziyingxiaoshouliuliangshuju`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：京东自营_销售流量数据
- 重要性/角色：C / detail_like
- 行数/最近更新：163496.0 / 2026-07-10 08:49:10
- 任务：京东自营_销售流量数据【迁移】（uPw9lmKbzW）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, SKU；业务日期：时间
- 核心字段候选：时间, 商品名称, SKU, 店铺名称, 成交商品件数, 成交金额, 加购商品件数

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `jingdongziyingxiaoshouliuliangshuju__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `jingdongziyingxiaoshouliuliangshuju__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `jingdongziyingxiaoshouliuliangshuju__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 时间, 商品名称, SKU, 店铺名称, 成交商品件数 | 检查字段数量和关键字段是否发生变化。 |
| `jingdongziyingxiaoshouliuliangshuju__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, SKU | 检查候选主键非空和重复。 |
| `jingdongziyingxiaoshouliuliangshuju__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 时间, 商品名称, SKU, 店铺名称, 成交商品件数, 成交金额, 加购商品件数 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 京东售后数据（`odsziyinghejingzaoshouhoushujubiao`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：京东售后数据
- 重要性/角色：C / detail_like
- 行数/最近更新：214052.0 / 2026-07-10 08:49:56
- 任务：京东售后数据【迁移】（GwQTxmlYjX）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 采购单号, 订单号, sku编码；业务日期：业务日期
- 核心字段候选：订单号, sku编码, sku数量, 总金额, 业务日期, 店铺名称

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `odsziyinghejingzaoshouhoushujubiao__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `odsziyinghejingzaoshouhoushujubiao__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `odsziyinghejingzaoshouhoushujubiao__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 订单号, sku编码, sku数量, 总金额, 业务日期 | 检查字段数量和关键字段是否发生变化。 |
| `odsziyinghejingzaoshouhoushujubiao__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 采购单号, 订单号, sku编码 | 检查候选主键非空和重复。 |
| `odsziyinghejingzaoshouhoushujubiao__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 订单号, sku编码, sku数量, 总金额, 业务日期, 店铺名称 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `单据类型`：售后退货


### 拼多多-商品推广全店托管（`pdd_product_promotion_whole_store_hosting`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：pdd_product_promotion_whole_store_hosting
- 重要性/角色：C / detail_like
- 行数/最近更新：95664.0 / 2026-07-10 11:35:51
- 任务：拼多多-商品推广全店托管【迁移】（ip8eDwje09）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, id, corp_id, bidding_method；业务日期：business_date, gather_time, insert_time
- 核心字段候选：commodity_id, commodity_name, store_name, shop_no, each_transaction_amount, each_direct_transaction_amount, indirect_transaction_amount_per_transaction, business_date

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `pdd_product_promotion_whole_store_hosting__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `pdd_product_promotion_whole_store_hosting__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `pdd_product_promotion_whole_store_hosting__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | commodity_id, commodity_name, store_name, shop_no, each_transaction_amount | 检查字段数量和关键字段是否发生变化。 |
| `pdd_product_promotion_whole_store_hosting__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, id, corp_id, bidding_method | 检查候选主键非空和重复。 |
| `pdd_product_promotion_whole_store_hosting__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | commodity_id, commodity_name, store_name, shop_no, each_transaction_amount, each_direct_transaction_amount, indirect_transaction_amount_per_transaction, business_date | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `has_it_been_deleted`：已删除


### 拼多多-商品推广概况全店托管（`pdd_product_promotion_whole_store_hosting_overview`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：pdd_product_promotion_whole_store_hosting_overview
- 重要性/角色：C / detail_like
- 行数/最近更新：2560.0 / 2026-07-10 11:35:31
- 任务：拼多多-商品推广概况全店托管【迁移】（cTcFjycErR）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, id, corp_id, shop_no；业务日期：business_date, gather_time, insert_time
- 核心字段候选：store_name, shop_no, each_transaction_amount, business_date, gather_time

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `pdd_product_promotion_whole_store_hosting_overview__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `pdd_product_promotion_whole_store_hosting_overview__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `pdd_product_promotion_whole_store_hosting_overview__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | store_name, shop_no, each_transaction_amount, business_date, gather_time | 检查字段数量和关键字段是否发生变化。 |
| `pdd_product_promotion_whole_store_hosting_overview__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, id, corp_id, shop_no | 检查候选主键非空和重复。 |
| `pdd_product_promotion_whole_store_hosting_overview__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | store_name, shop_no, each_transaction_amount, business_date, gather_time | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 拼多多推广报表商品推广日报单元（`pdd_promotion_reportproduct_promotion_dailyunit`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：pdd_promotion_reportproduct_promotion_dailyunit
- 重要性/角色：C / detail_like
- 行数/最近更新：628026.0 / 2026-07-10 11:36:48
- 任务：拼多多推广报表商品推广日报单元【迁移】（ZjaKsqKDhn）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, id, corp_id, bidding_method；业务日期：business_date, gather_time, insert_time
- 核心字段候选：commodity_id, commodity_name, store_name, shop_no, each_transaction_amount, each_direct_transaction_amount, indirect_transaction_amount_per_transaction, business_date

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `pdd_promotion_reportproduct_promotion_dailyunit__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `pdd_promotion_reportproduct_promotion_dailyunit__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `pdd_promotion_reportproduct_promotion_dailyunit__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | commodity_id, commodity_name, store_name, shop_no, each_transaction_amount | 检查字段数量和关键字段是否发生变化。 |
| `pdd_promotion_reportproduct_promotion_dailyunit__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, id, corp_id, bidding_method | 检查候选主键非空和重复。 |
| `pdd_promotion_reportproduct_promotion_dailyunit__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | commodity_id, commodity_name, store_name, shop_no, each_transaction_amount, each_direct_transaction_amount, indirect_transaction_amount_per_transaction, business_date | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `keep_the_promotion`：原全站推广, 原标准推广
- `has_it_been_deleted`：已删除


### ODS_拼多多售后数据（`pinduoduoshoushoushuju`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：ODS_拼多多售后数据
- 重要性/角色：C / detail_like
- 行数/最近更新：2223875.0 / 2026-07-10 08:12:33
- 任务：ODS_拼多多售后数据【迁移】（q340kVIT8D）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 线上订单号, 商品编码, 原订单下单金额；业务日期：申请日期, 影刀修改时间
- 核心字段候选：线上订单号, 商品编码, 店铺名称, 申请日期, 申请金额, 原订单下单金额, 原订单状态, 原订单类型

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `pinduoduoshoushoushuju__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `pinduoduoshoushoushuju__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `pinduoduoshoushoushuju__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 线上订单号, 商品编码, 店铺名称, 申请日期, 申请金额 | 检查字段数量和关键字段是否发生变化。 |
| `pinduoduoshoushoushuju__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 线上订单号, 商品编码, 原订单下单金额 | 检查候选主键非空和重复。 |
| `pinduoduoshoushoushuju__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 线上订单号, 商品编码, 店铺名称, 申请日期, 申请金额, 原订单下单金额, 原订单状态, 原订单类型 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `问题类型`：其他原因, 不想要了, 材质、面料与商品描述不符, 做工粗糙/有瑕疵
- `线上状态`：买家已经申请退款，等待卖家同意, 卖家已经同意退款，等待买家退货, 买家已经退货，等待卖家确认收货
- `状态`：已确认, 待确认


### 天猫-商品揽收明细（`shangpinlanshoumingxi`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-商品揽收明细
- 重要性/角色：C / detail_like
- 行数/最近更新：15385.0 / 2026-07-10 12:01:49
- 任务：天猫-商品揽收明细【迁移】（noeqZ7sy6C）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品编码/名称, 应揽收订单量, 超时揽收订单量；业务日期：日期
- 核心字段候选：商品编码/名称, 商品销量, 商品销售金额/元, 应揽收订单量, 超时揽收订单量, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `shangpinlanshoumingxi__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `shangpinlanshoumingxi__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `shangpinlanshoumingxi__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品编码/名称, 商品销量, 商品销售金额/元, 应揽收订单量, 超时揽收订单量 | 检查字段数量和关键字段是否发生变化。 |
| `shangpinlanshoumingxi__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品编码/名称, 应揽收订单量, 超时揽收订单量 | 检查候选主键非空和重复。 |
| `shangpinlanshoumingxi__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品编码/名称, 商品销量, 商品销售金额/元, 应揽收订单量, 超时揽收订单量, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-商品体验分（`shangpintiyanfen`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-商品体验分
- 重要性/角色：C / detail_like
- 行数/最近更新：446200.0 / 2026-07-10 12:00:57
- 任务：天猫-商品体验分【迁移】（oUuexw03Jd）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID, 问题订单数, 成交订单数；业务日期：日期
- 核心字段候选：商品ID, 商品名称, 问题订单数, 成交订单数, 商品体验分, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `shangpintiyanfen__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `shangpintiyanfen__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `shangpintiyanfen__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品ID, 商品名称, 问题订单数, 成交订单数, 商品体验分 | 检查字段数量和关键字段是否发生变化。 |
| `shangpintiyanfen__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID, 问题订单数, 成交订单数 | 检查候选主键非空和重复。 |
| `shangpintiyanfen__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品ID, 商品名称, 问题订单数, 成交订单数, 商品体验分, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 视频id（`shipingid`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：视频id
- 重要性/角色：C / detail_like
- 行数/最近更新：1183360.0 / 2026-07-10 08:19:11
- 任务：视频id【迁移】（z0aIrIlDAx）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 视频id, 宝贝id；业务日期：未识别
- 核心字段候选：未识别

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `shipingid__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `shipingid__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `shipingid__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | - | 检查字段数量和关键字段是否发生变化。 |
| `shipingid__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 视频id, 宝贝id | 检查候选主键非空和重复。 |


### 按日手淘搜索流量数据（`shoutaosousuo_liuliangdata_day`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：按日手淘搜索流量数据
- 重要性/角色：C / source_like
- 行数/最近更新：29626.0 / 2026-07-10 08:30:31
- 任务：按日手淘搜索流量数据【迁移】（eJaaISZlhL）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID；业务日期：日期
- 核心字段候选：日期, 商品名称, 商品ID, 支付金额, 微详情引导支付金额, 店铺名称

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `shoutaosousuo_liuliangdata_day__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `shoutaosousuo_liuliangdata_day__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `shoutaosousuo_liuliangdata_day__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期, 商品名称, 商品ID, 支付金额, 微详情引导支付金额 | 检查字段数量和关键字段是否发生变化。 |
| `shoutaosousuo_liuliangdata_day__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID | 检查候选主键非空和重复。 |
| `shoutaosousuo_liuliangdata_day__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期, 商品名称, 商品ID, 支付金额, 微详情引导支付金额, 店铺名称 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 按日淘宝客流量数据（`taobaoke_liuliangdata_day`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：按日淘宝客流量数据
- 重要性/角色：C / source_like
- 行数/最近更新：19503.0 / 2026-07-10 08:30:18
- 任务：按日淘宝客流量数据【迁移】（d3QZcR5SPj）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID；业务日期：日期
- 核心字段候选：日期, 商品名称, 商品ID, 支付金额, 微详情引导支付金额, 店铺名称

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `taobaoke_liuliangdata_day__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `taobaoke_liuliangdata_day__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `taobaoke_liuliangdata_day__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期, 商品名称, 商品ID, 支付金额, 微详情引导支付金额 | 检查字段数量和关键字段是否发生变化。 |
| `taobaoke_liuliangdata_day__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID | 检查候选主键非空和重复。 |
| `taobaoke_liuliangdata_day__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期, 商品名称, 商品ID, 支付金额, 微详情引导支付金额, 店铺名称 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 按日淘宝客_旧版（`taobaokejiuban`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：按日淘宝客_旧版
- 重要性/角色：C / detail_like
- 行数/最近更新：62184.0 / 2026-07-10 08:19:01
- 任务：按日淘宝客_旧版【迁移】（VDaIPYslyR）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID；业务日期：日期
- 核心字段候选：日期, 商品名称, 商品ID, 支付金额, 店铺名称

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `taobaokejiuban__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `taobaokejiuban__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `taobaokejiuban__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期, 商品名称, 商品ID, 支付金额, 店铺名称 | 检查字段数量和关键字段是否发生变化。 |
| `taobaokejiuban__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID | 检查候选主键非空和重复。 |
| `taobaokejiuban__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期, 商品名称, 商品ID, 支付金额, 店铺名称 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫_商品差评订单明细（`tianmaochaipinlvdingdanmingxibiao`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫_商品差评订单明细
- 重要性/角色：C / detail_like
- 行数/最近更新：774417.0 / 2026-07-10 12:01:17
- 任务：天猫_商品差评订单明细【迁移】（aKuSZUh727）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 订单编号, 商品名称/编码；业务日期：付款时间, 评价时间, 日期
- 核心字段候选：订单编号, 商品名称/编码, 付款时间, 评价时间, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaochaipinlvdingdanmingxibiao__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaochaipinlvdingdanmingxibiao__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaochaipinlvdingdanmingxibiao__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 订单编号, 商品名称/编码, 付款时间, 评价时间, 日期 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaochaipinlvdingdanmingxibiao__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 订单编号, 商品名称/编码 | 检查候选主键非空和重复。 |
| `tianmaochaipinlvdingdanmingxibiao__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 订单编号, 商品名称/编码, 付款时间, 评价时间, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-达摩盘-关键词（`tianmaodamopanguanjianci`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-达摩盘-关键词
- 重要性/角色：C / detail_like
- 行数/最近更新：22018.0 / 2026-07-10 09:03:22
- 任务：天猫-达摩盘-关键词【迁移】（774aE1672V）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：日期
- 核心字段候选：日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaodamopanguanjianci__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaodamopanguanjianci__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaodamopanguanjianci__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaodamopanguanjianci__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `tianmaodamopanguanjianci__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-红包核销（`tianmaohongbaohexiao`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-红包核销
- 重要性/角色：C / detail_like
- 行数/最近更新：804456.0 / 2026-07-10 12:01:07
- 任务：天猫-红包核销【迁移】（8da46yam1L）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 订单金额, 订单编号；业务日期：使用时间
- 核心字段候选：使用时间, 订单金额, 订单编号, 商家出资金额, 店铺名称

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaohongbaohexiao__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaohongbaohexiao__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaohongbaohexiao__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 使用时间, 订单金额, 订单编号, 商家出资金额, 店铺名称 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaohongbaohexiao__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 订单金额, 订单编号 | 检查候选主键非空和重复。 |
| `tianmaohongbaohexiao__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 使用时间, 订单金额, 订单编号, 商家出资金额, 店铺名称 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-生意参谋-流量整体（`tianmaoliuliangzhengti`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-生意参谋-流量整体
- 重要性/角色：C / detail_like
- 行数/最近更新：423064.0 / 2026-07-10 10:03:08
- 任务：天猫-生意参谋-流量整体【迁移】（jcwfnDZ1gc）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID；业务日期：统计日期
- 核心字段候选：统计日期, 店铺名称, 商品ID, 商品名称, 商品状态, 商品访客数, 下单金额, 支付金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaoliuliangzhengti__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaoliuliangzhengti__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaoliuliangzhengti__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 统计日期, 店铺名称, 商品ID, 商品名称, 商品状态 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaoliuliangzhengti__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID | 检查候选主键非空和重复。 |
| `tianmaoliuliangzhengti__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 统计日期, 店铺名称, 商品ID, 商品名称, 商品状态, 商品访客数, 下单金额, 支付金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `商品状态`：当前在线


### 天猫-赔付打款（`tianmaopeifudakuan`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-赔付打款
- 重要性/角色：C / detail_like
- 行数/最近更新：10258.0 / 2026-07-10 12:00:19
- 任务：天猫-赔付打款【迁移】（KK69MCzfVu）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品id, 违规赔付订单量；业务日期：日期
- 核心字段候选：商品id, 违规赔付订单量, 商品赔付金额, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaopeifudakuan__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaopeifudakuan__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaopeifudakuan__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品id, 违规赔付订单量, 商品赔付金额, 日期 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaopeifudakuan__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品id, 违规赔付订单量 | 检查候选主键非空和重复。 |
| `tianmaopeifudakuan__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品id, 违规赔付订单量, 商品赔付金额, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 品质退款（`tianmaopinzhituikuan`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：品质退款
- 重要性/角色：C / detail_like
- 行数/最近更新：812568.0 / 2026-07-10 12:00:59
- 任务：品质退款【迁移】（hwuwGnqt3o）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 订单编号；业务日期：买家退款时间
- 核心字段候选：商品, 订单编号, 买家退款时间

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaopinzhituikuan__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaopinzhituikuan__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaopinzhituikuan__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品, 订单编号, 买家退款时间 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaopinzhituikuan__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 订单编号 | 检查候选主键非空和重复。 |
| `tianmaopinzhituikuan__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品, 订单编号, 买家退款时间 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-生意参谋-流量来源-新版（`tianmaoshengyicanmouliuliangxinban`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-生意参谋-流量来源-新版
- 重要性/角色：C / detail_like
- 行数/最近更新：5948900.0 / 2026-07-10 10:04:52
- 任务：天猫-生意参谋-流量来源-新版【迁移】（9UcdbFLDbK）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID；业务日期：统计日期
- 核心字段候选：统计日期, 店铺名称, 商品ID, 商品收藏人数, 支付金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaoshengyicanmouliuliangxinban__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaoshengyicanmouliuliangxinban__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaoshengyicanmouliuliangxinban__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 统计日期, 店铺名称, 商品ID, 商品收藏人数, 支付金额 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaoshengyicanmouliuliangxinban__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID | 检查候选主键非空和重复。 |
| `tianmaoshengyicanmouliuliangxinban__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 统计日期, 店铺名称, 商品ID, 商品收藏人数, 支付金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫佑美_四小时_货品运营主体列表（`tianmaosixiaohouhuopinyunying`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫佑美_四小时_货品运营主体列表
- 重要性/角色：C / detail_like
- 行数/最近更新：0.0 / 2026-07-10 09:51:07
- 任务：天猫佑美_四小时_货品运营主体列表【迁移】（AdAXlr6bdI）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 主体ID, 宝贝ID；业务日期：日期
- 核心字段候选：商品成长, 总预售成交金额, 总成交金额, 直接成交金额, 间接成交金额, 新客成交金额贡献, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaosixiaohouhuopinyunying__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaosixiaohouhuopinyunying__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaosixiaohouhuopinyunying__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品成长, 总预售成交金额, 总成交金额, 直接成交金额, 间接成交金额 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaosixiaohouhuopinyunying__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 主体ID, 宝贝ID | 检查候选主键非空和重复。 |
| `tianmaosixiaohouhuopinyunying__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品成长, 总预售成交金额, 总成交金额, 直接成交金额, 间接成交金额, 新客成交金额贡献, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫佑美_四小时_全站计划列表（`tianmaosixiaoquanzhanjihuanliebiao`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫佑美_四小时_全站计划列表
- 重要性/角色：C / detail_like
- 行数/最近更新：826281.0 / 2026-07-10 09:51:58
- 任务：天猫佑美_四小时_全站计划列表【迁移】（FRcHsNnaPc）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 计划ID；业务日期：投放日期, 日期
- 核心字段候选：投放日期, 收藏店铺数, 店铺收藏成本, 总预售成交金额, 总成交金额, 直接成交金额, 间接成交金额, 新客成交金额贡献

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaosixiaoquanzhanjihuanliebiao__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaosixiaoquanzhanjihuanliebiao__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaosixiaoquanzhanjihuanliebiao__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 投放日期, 收藏店铺数, 店铺收藏成本, 总预售成交金额, 总成交金额 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaosixiaoquanzhanjihuanliebiao__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 计划ID | 检查候选主键非空和重复。 |
| `tianmaosixiaoquanzhanjihuanliebiao__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 投放日期, 收藏店铺数, 店铺收藏成本, 总预售成交金额, 总成交金额, 直接成交金额, 间接成交金额, 新客成交金额贡献 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `状态`：


### 天猫佑美_四小时_关键词单元列表（`tianmaosixiaoshiguanjianci`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫佑美_四小时_关键词单元列表
- 重要性/角色：C / detail_like
- 行数/最近更新：1330487.0 / 2026-07-10 09:51:47
- 任务：天猫佑美_四小时_关键词单元列表【迁移】（8Iw51FobWo）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 单元ID, 宝贝ID, 计划ID；业务日期：加入计划时间, 日期
- 核心字段候选：商品成长, 加入计划时间, 拍下订单笔数, 拍下订单金额, 总预售成交金额, 直接预售成交金额, 间接预售成交金额, 直接成交金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaosixiaoshiguanjianci__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaosixiaoshiguanjianci__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaosixiaoshiguanjianci__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品成长, 加入计划时间, 拍下订单笔数, 拍下订单金额, 总预售成交金额 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaosixiaoshiguanjianci__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 单元ID, 宝贝ID, 计划ID | 检查候选主键非空和重复。 |
| `tianmaosixiaoshiguanjianci__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品成长, 加入计划时间, 拍下订单笔数, 拍下订单金额, 总预售成交金额, 直接预售成交金额, 间接预售成交金额, 直接成交金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `状态`：


### 天猫佑美_四小时_精准人群主体列表（`tianmaosixiaoshoujingzhunrenqun`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫佑美_四小时_精准人群主体列表
- 重要性/角色：C / detail_like
- 行数/最近更新：207095.0 / 2026-07-10 09:51:46
- 任务：天猫佑美_四小时_精准人群主体列表【迁移】（ZFgRwt8pwx）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 单元ID, 宝贝ID, 拍下订单笔数；业务日期：日期
- 核心字段候选：商品成长, 拍下订单笔数, 拍下订单金额, 总预售成交金额, 直接预售成交金额, 间接预售成交金额, 直接成交金额, 间接成交金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaosixiaoshoujingzhunrenqun__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaosixiaoshoujingzhunrenqun__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaosixiaoshoujingzhunrenqun__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品成长, 拍下订单笔数, 拍下订单金额, 总预售成交金额, 直接预售成交金额 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaosixiaoshoujingzhunrenqun__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 单元ID, 宝贝ID, 拍下订单笔数 | 检查候选主键非空和重复。 |
| `tianmaosixiaoshoujingzhunrenqun__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品成长, 拍下订单笔数, 拍下订单金额, 总预售成交金额, 直接预售成交金额, 间接预售成交金额, 直接成交金额, 间接成交金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `状态`：


### 天猫四小时_售后数据（`tianmaosixiaoshoushouhoushuju`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫四小时_售后数据
- 重要性/角色：C / detail_like
- 行数/最近更新：1795774.0 / 2026-07-10 09:39:59
- 任务：天猫四小时_售后数据【迁移】（MrgTBqP3OZ）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 售后单号, 内部订单号, 线上订单号；业务日期：登记时间, 申请日期, 最后确认日期
- 核心字段候选：内部订单号, 登记时间, 申请日期, 线上申请金额, 卖家应退金额, 买家应补偿金额, 实际应退金额, 店铺编号

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaosixiaoshoushouhoushuju__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaosixiaoshoushouhoushuju__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaosixiaoshoushouhoushuju__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 内部订单号, 登记时间, 申请日期, 线上申请金额, 卖家应退金额 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaosixiaoshoushouhoushuju__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 售后单号, 内部订单号, 线上订单号 | 检查候选主键非空和重复。 |
| `tianmaosixiaoshoushouhoushuju__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 内部订单号, 登记时间, 申请日期, 线上申请金额, 卖家应退金额, 买家应补偿金额, 实际应退金额, 店铺编号 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `线上类型`：仅退款
- `问题类型`：不想要了, 订单信息拍错（规格/尺码/颜色等）, 携带退款：赠品
- `原订单状态`：取消, 异常


### 天猫-淘客佣金（`tianmaotaokeyongjin`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-淘客佣金
- 重要性/角色：C / detail_like
- 行数/最近更新：1146098.0 / 2026-07-10 12:02:05
- 任务：天猫-淘客佣金【迁移】（mXemzumUf5）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 商品ID, 淘宝父订单编号, 淘宝子订单编号；业务日期：确认收货时间, 账户支出时间, 淘客结算时间
- 核心字段候选：确认收货时间, 账户支出时间, 淘客结算时间, 创建时间, 商品ID, 商品名称, 成交商品数, 服务费金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaotaokeyongjin__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaotaokeyongjin__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaotaokeyongjin__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 确认收货时间, 账户支出时间, 淘客结算时间, 创建时间, 商品ID | 检查字段数量和关键字段是否发生变化。 |
| `tianmaotaokeyongjin__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 商品ID, 淘宝父订单编号, 淘宝子订单编号 | 检查候选主键非空和重复。 |
| `tianmaotaokeyongjin__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 确认收货时间, 账户支出时间, 淘客结算时间, 创建时间, 商品ID, 商品名称, 成交商品数, 服务费金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `是否预售未付尾款订单`：


### 天猫推广-短直联动（`tianmaotuiguangduanzhiliandong`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫推广-短直联动
- 重要性/角色：C / detail_like
- 行数/最近更新：723.0 / 2026-07-10 08:41:21
- 任务：天猫推广-短直联动【迁移】（ETeKlnHukA）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 计划ID；业务日期：日期
- 核心字段候选：日期, 直接成交金额, 总成交金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaotuiguangduanzhiliandong__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaotuiguangduanzhiliandong__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaotuiguangduanzhiliandong__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 日期, 直接成交金额, 总成交金额 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaotuiguangduanzhiliandong__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 计划ID | 检查候选主键非空和重复。 |
| `tianmaotuiguangduanzhiliandong__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 日期, 直接成交金额, 总成交金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-营销托管近十天（`tianmaoyingxiaofeiyongjinshitian`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-营销托管近十天
- 重要性/角色：C / detail_like
- 行数/最近更新：35572.0 / 2026-07-10 12:01:09
- 任务：天猫-营销托管近十天【迁移】（theaP49FvI）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：日期
- 核心字段候选：商品名称, 成交金额, 日期

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaoyingxiaofeiyongjinshitian__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaoyingxiaofeiyongjinshitian__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaoyingxiaofeiyongjinshitian__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 商品名称, 成交金额, 日期 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaoyingxiaofeiyongjinshitian__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `tianmaoyingxiaofeiyongjinshitian__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 商品名称, 成交金额, 日期 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 天猫-营销托管（`tianmaoyingxiaotuoguanfeiyong`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：天猫-营销托管
- 重要性/角色：C / detail_like
- 行数/最近更新：391957.0 / 2026-07-10 08:30:05
- 任务：天猫-营销托管【迁移】（EIQDTb55i2）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, 订单日期, 交易主订单号, 交易子订单号；业务日期：扣费日期, 订单日期, 确认收货日期
- 核心字段候选：扣费日期, 扣费交易金额, 扣费金额, 订单日期, 交易主订单号, 交易子订单号, 扣费金额元, 退款金额元

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tianmaoyingxiaotuoguanfeiyong__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tianmaoyingxiaotuoguanfeiyong__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tianmaoyingxiaotuoguanfeiyong__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 扣费日期, 扣费交易金额, 扣费金额, 订单日期, 交易主订单号 | 检查字段数量和关键字段是否发生变化。 |
| `tianmaoyingxiaotuoguanfeiyong__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, 订单日期, 交易主订单号, 交易子订单号 | 检查候选主键非空和重复。 |
| `tianmaoyingxiaotuoguanfeiyong__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 扣费日期, 扣费交易金额, 扣费金额, 订单日期, 交易主订单号, 交易子订单号, 扣费金额元, 退款金额元 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |


### 拼多多-推广红包返还（`tuiguanghongbaofanhuan`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：拼多多-推广红包返还
- 重要性/角色：C / detail_like
- 行数/最近更新：76126.0 / 2026-07-10 01:03:02
- 任务：拼多多-推广红包返还【迁移】（ufakHsRsfg）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id；业务日期：时间
- 核心字段候选：时间, 店铺名称, 交易金额

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `tuiguanghongbaofanhuan__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `tuiguanghongbaofanhuan__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `tuiguanghongbaofanhuan__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | 时间, 店铺名称, 交易金额 | 检查字段数量和关键字段是否发生变化。 |
| `tuiguanghongbaofanhuan__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id | 检查候选主键非空和重复。 |
| `tuiguanghongbaofanhuan__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | 时间, 店铺名称, 交易金额 | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `资金类型`：现金, 红包
- `流水类型`：收入, 支出
- `是否计入`：


### 小红书聚光-全局报表广告创意分日（`xhsjg_global_ad_creative`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：xhsjg_global_ad_creative
- 重要性/角色：B / detail_like
- 行数/最近更新：49011498.0 / 2026-07-09 14:55:54
- 任务：小红书聚光-全局报表广告创意分日【迁移】（d786YokWIk）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, id, order_cost_7th, order_volume_placed_7th；业务日期：report_time_type, time, per_capita_stay_timelive_broadcast_room
- 核心字段候选：order_cost_7th, order_volume_placed_7th, seven_day_order_amount, seven_day_payment_order_cost, seven_day_payment_order_quantity, seven_day_payment_amount, seven_day_presale_order_volume, seven_day_presale_order_amount

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `xhsjg_global_ad_creative__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `xhsjg_global_ad_creative__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `xhsjg_global_ad_creative__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | order_cost_7th, order_volume_placed_7th, seven_day_order_amount, seven_day_payment_order_cost, seven_day_payment_order_quantity | 检查字段数量和关键字段是否发生变化。 |
| `xhsjg_global_ad_creative__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, id, order_cost_7th, order_volume_placed_7th | 检查候选主键非空和重复。 |
| `xhsjg_global_ad_creative__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | order_cost_7th, order_volume_placed_7th, seven_day_order_amount, seven_day_payment_order_cost, seven_day_payment_order_quantity, seven_day_payment_amount, seven_day_presale_order_volume, seven_day_presale_order_amount | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `advertising_type`：搜索广告, 信息流广告, 全站智投广告
- `report_time_type`：分日


### 小红书蒲公英-数据中心导出（`xhspgy_data_center_export`）

- 范围：yingdao_text_active_downstream
- 来源类型：yingdao_db_text；源表：xhspgy_data_center_export
- 重要性/角色：C / export_like
- 行数/最近更新：967071.0 / 2026-07-09 15:00:19
- 任务：小红书蒲公英-数据中心导出【迁移】（MKq88uhasI）
- 建议配置入口：表对应更新任务的任务详情 -> 数据质量检查规则
- 资源策略：大表只按昨天分区/昨天业务日期/任务产出行数检查，避免全表扫描。
- 候选主键：__id, id, star_task_main_task_id, note_id；业务日期：jd_cooperation_task_start_time, jd_cooperation_task_end_time, task_start_time
- 核心字段候选：jd_cooperation_task_start_time, jd_cooperation_task_end_time, task_start_time, task_end_time, starting_time_vipshop_collaboration_task, vipshop_collaboration_task_end_time, advertising_amount_effect_xiaohongshu_website, total_amountternal_effects_xiaohongshu_website

| 规则 | 类型 | 配置方式 | 字段 | 说明 |
| --- | --- | --- | --- | --- |
| `xhspgy_data_center_export__task_output_row_count_nonzero` | 任务产出行数/自定义SQL | 优先在任务详情中配置任务产出行数 > 0；如果只能写 SQL，则配置整表非空或按昨天业务日期非空。 | - | 检查本次更新任务是否真实产出数据，重点防任务成功但 0 行。 |
| `xhspgy_data_center_export__task_output_row_count_history_baseline` | 任务产出行数波动 | 在任务详情中配置任务产出行数历史对比；如果平台暂不支持历史基线，先记录为观察规则。 | - | 检查本次任务产出行数是否明显低于近 7 次成功任务的常规水平。 |
| `xhspgy_data_center_export__schema_field_count_stable` | 字段结构变化 | 优先配置字段存在/字段数规则；没有内置项时用自定义 SQL 查 information_schema.columns。 | jd_cooperation_task_start_time, jd_cooperation_task_end_time, task_start_time, task_end_time, starting_time_vipshop_collaboration_task | 检查字段数量和关键字段是否发生变化。 |
| `xhspgy_data_center_export__primary_key_null_and_duplicate` | 主键非空/重复 | 优先使用 BI 字段规则「空值个数，固定值」和「重复值个数，固定值」；大表必须配置昨天分区或昨天业务日期参数。组合主键无法表达时 SQL 兜底。 | __id, id, star_task_main_task_id, note_id | 检查候选主键非空和重复。 |
| `xhspgy_data_center_export__core_fields_null` | 核心字段空值 | 优先使用 BI 字段规则「空值个数，固定值」或「空值个数/总行数，固定值」；第一阶段只预警，不阻断。 | jd_cooperation_task_start_time, jd_cooperation_task_end_time, task_start_time, task_end_time, starting_time_vipshop_collaboration_task, vipshop_collaboration_task_end_time, advertising_amount_effect_xiaohongshu_website, total_amountternal_effects_xiaohongshu_website | 检查主键、业务日期、商品/店铺/订单/金额等核心字段空值。 |

枚举/状态字段样例：
- `interactive_component_types`：0.0
- `is_it_optimal_efficiency_mode`：否
- `body_component_type`：搜索组件, 0.0




