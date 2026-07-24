## 2026-07-10 口径补充：影刀/text 账单表剔除

- 影刀数据库（source database = `text`）里的账单类表，除“运费险账单”外，本批不进入质量规则配置。
- 剔除原因：这些账单表属于月度数据处理、手动上传或手动执行性质，不是日常自动采集链路；即使存在下游依赖，也不代表需要每日 freshness 或行数波动校验。
- 判定证据需要同时看表名/中文名和任务性质：如果任务是手动上传、手动执行、月度处理或财务账单拆分，默认剔除；不要因为有数据集消费或下游任务就提升为 P0/P1。
- 保留例外：运费险账单类表仍可进入候选，因为它已被确认为需要关注的业务链路。
- 这条规则只约束账单类表，不影响仍有下游且近期活跃的影刀抓取表，例如评价有礼、红包、推广、流量、销售等明细/结果表。
# 第一批数据质量规则候选表重梳理

生成日期：2026-07-09

本版不是把所有表都交给人工确认，而是先自动剔除临时、测试、上传、长期固化且无强消费证据的表，再从 S/A 候选中挑出规则方向较明确的第一批候选。

## 总览

- S/A 候选总数：52
- 第一批可讨论配置候选：45
- 暂缓，需要补业务含义或口径证据：0
- 剔除/暂不治理：7
- 影刀/text 源库接入落表：176（按 source_id=iJuGP2i7Kk 识别）

## 影刀/text 源库识别口径

影刀数据库接入表不再按目标表名猜测。本版按 `ods_db_cube_work_table_info_f.source_id=iJuGP2i7Kk` 和调度任务参数中的 `srcDataSourceId` 识别，并按你确认的源库名标记为 `text`。

这类表的首要风险不是全表准确性扫描，而是接入静默缺失：任务成功但当日 0 行、缺分区/缺业务日期、字段变更、文本字段无法转数值或日期。

对这类源表，本版按三段式处理：没有下游任务数量的表，视为接入后当前链路未消费，默认暂不配置质量规则；有下游但长期不更新的表，先观察是否为固化周期数据；有下游且近期更新的表，纳入接入静默缺失候选，重点防任务成功但当日 0 行、缺天、字段变更和文本字段不可转换。影刀/text 里的账单类表按月度手动处理口径剔除，除运费险账单外暂不配置质量规则。

### text 源库账单表剔除清单（除运费险外）

以下表保留证据，但不进入规则配置、不进入 P0/P1/P2 人工确认；判断原因是月度数据处理、手动上传/手动执行任务或财务账单拆分，不是日常自动采集链路。

| 表名 | 中文/来源线索 | 剔除原因 |
| --- | --- | --- |
| `caiwuzhifubaozhangdanshuju` | 财务_支付宝账单 | 月度手工账单/手动执行，不配置日常质量规则 |
| `pinduoduozhifubaozhangdanshuju` | 拼多多-支付宝账单数据 | 月度手工账单/手动执行，不配置日常质量规则 |
| `tianmaoweixinzhangdan` | 天猫_微信账单 | 月度手工账单/手动执行，不配置日常质量规则 |
| `tmall_wechat_billing` | 天猫_微信账单_聚合账户 | 月度手工账单/手动执行，不配置日常质量规则 |
| `pdd_reconciliation_center_payment_details` | 拼多多对账中心货款明细 | 月度手工账单/手动执行，不配置日常质量规则 |
| `ods_douyinzijinzhangdanchaifen` | ODS_抖音资金账单拆分_填报 | 月度手工账单/手动执行，不配置日常质量规则 |
| `caiwuzhangdanchaifen` | 包材账单拆分 | 月度手工账单/手动执行，不配置日常质量规则 |
| `taogongchangzhifubaozhangdanshuju` | 淘工厂_支付宝账单明细 | 月度手工账单/手动执行，不配置日常质量规则 |
| `caiwukustianmaoweixinzhangdan` | 财务天猫kus微信账单 | 月度手工账单/手动执行，不配置日常质量规则 |
| `caiwukustianmaozhifubaochengyuyou` | 财务天猫kus支付宝账单-橙与柚 | 月度手工账单/手动执行，不配置日常质量规则 |
| `caiwutianmaokusbaozhengjin` | 财务天猫kus保证金账单 | 月度手工账单/手动执行，不配置日常质量规则 |
| `caiwutianmaokuszhifubaozhangdan` | 财务天猫kus支付宝账单-官方旗舰店 | 月度手工账单/手动执行，不配置日常质量规则 |
| `caiwutianmaokuszhifubaozhangdanhanbo` | 财务天猫kus支付宝账单-翰博 | 月度手工账单/手动执行，不配置日常质量规则 |
| `weixinhuiyuanzhongxinzhangdan` | 财务账单拆分_ods_微信会员中心 | 月度手工账单/手动执行，不配置日常质量规则 |
| `freight_bill_detail` | 运费账单明细（抖音财务对账后） | 运费账单不是运费险账单；按月度手工账单剔除 |
| `freight_bill_exception` | 运费账单问题件及冲回扣减明细（抖音财务对账后） | 运费账单不是运费险账单；按月度手工账单剔除 |
| `hangzhoumaizhuandianzhifubaozhangdnachaifen` | 杭州专卖店_支付宝账单拆分 | 月度手工账单/手动执行，不配置日常质量规则 |
| `tianmaobaozhengjinrpaapi` | 天猫-保证金账单 | 月度手工账单/手动执行，不配置日常质量规则 |
| `yuantongyuncangbaocaizhangdanchaifen` | 圆通云仓包材账单拆分 | 月度手工账单/手动执行，不配置日常质量规则 |

### text 源库治理候选（优先展示有下游且近期更新的前 30 张）

| 优先级 | 角色 | 表名 | 源表/中文线索 | 行数 | 最新更新时间 | 使用证据 | 治理建议 |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| A | source_like | `huizongbiao` | 天猫综合表 | 9832.0 | 2026-07-10 00:30:18 | 数据集34 / 查询0 / 下游任务20 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| B | source_like | `tianmaoxiaoshoujihuabiao` | 天猫-销售计划表 | 15695.0 | 2026-07-06 16:29:26 | 数据集13 / 查询0 / 下游任务5 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| B | source_like | `tianmaobaozhengjinxiangmucahifen` | 天猫_保证金数据拆分 | 12845.0 | 2026-07-06 15:04:20 | 数据集4 / 查询0 / 下游任务4 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `pdd_tgzx_promotion_report_store_promotion_store_unit` | 拼多多推广中心推广报表店铺推广明星店铺单元 | 495.0 | 2026-07-10 11:35:19 | 数据集2 / 查询0 / 下游任务4 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| B | source_like | `tianmaoshangpinIDcaigoufuzeren` | 天猫商品ID采购负责人综合表 | 2032.0 | 2026-07-07 11:05:48 | 数据集8 / 查询0 / 下游任务3 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| REVIEW | detail_like | `ODS_YOUMEIPDDxiaoshoudingdanbiao` | ODS_佑美拼多多销售订单数据 | 6961206.0 | 2026-07-10 08:23:33 | 数据集6 / 查询0 / 下游任务3 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| B | detail_like | `shangpinpintuilv` | 天猫-商品品退率明细 | 216243.0 | 2026-07-10 12:00:57 | 数据集6 / 查询0 / 下游任务2 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | source_like | `ODS_DOUYINZONGHEBIAO` | ODS_抖音综合表 | 1428.0 | 2026-07-07 08:58:46 | 数据集4 / 查询0 / 下游任务2 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| B | detail_like | `douyinyunfeixian` | ODS_抖音_运费险账单数据_RPA | 1305051.0 | 2026-07-10 01:02:52 | 数据集4 / 查询0 / 下游任务2 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `shangpinchapinglv` | 天猫-商品差评率明细 | 115721.0 | 2026-07-10 12:00:57 | 数据集4 / 查询0 / 下游任务2 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | result_like | `tianmaokuaidilanshouxinxibiao` | 天猫快递揽收信息表 | 395247.0 | 2026-07-09 09:40:10 | 数据集4 / 查询0 / 下游任务2 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `shoudanlijin` | 天猫-首单礼金 | 672804.0 | 2026-07-10 12:01:07 | 数据集2 / 查询0 / 下游任务2 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `liuliangshuju` | 京东_商品明细sku流量数据 | 108055.0 | 2026-07-10 08:23:34 | 数据集6 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `xunicang_kc` | 虚拟仓库存数据 | 332726.0 | 2026-07-10 08:04:19 | 数据集6 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `jingdongxiaohsoushuju` | 京东佑美旗舰店_销售数据 | 115777.0 | 2026-07-10 08:23:19 | 数据集4 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `jingzaoxiaoshouliuliangshuju` | 京东京造_sku销售流量数据 | 14423.0 | 2026-07-10 08:49:34 | 数据集4 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | source_like | `ods_dyyunfeixian` | ODS_抖音运费险_填报 | 190.0 | 2026-07-08 15:06:26 | 数据集4 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `pdd_sjzx_product_data_product_details` | 拼多多数据中心商品数据商品明细商品明细效果 | 741630.0 | 2026-07-10 11:36:50 | 数据集4 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `shangpinpaihang_liuliangdata_day` | 按日流量数据 | 450685.0 | 2026-07-10 08:19:06 | 数据集4 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `tianmaopingjiayouli` | 天猫-评价有礼 | 74610.0 | 2026-07-10 12:01:49 | 数据集4 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| B | detail_like | `tianmaosixiaoshouxiaoshoushuju` | 天猫四小时_销售数据 | 2618588.0 | 2026-07-10 09:42:00 | 数据集4 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `tianmoyingxiaotuoguanjinshiwutiandierban` | 天猫-营销托管近十五天第二版 | 9374.0 | 2026-07-10 12:00:47 | 数据集4 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `zhongdianpinpaimingtongji` | 天猫-重点品排名统计-日排名 | 111113.0 | 2026-07-10 11:14:13 | 数据集3 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `anrishoutaosousuo` | 按日手淘搜索_旧版 | 80686.0 | 2026-07-10 08:19:06 | 数据集2 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `damopanshujuxin` | 天猫-达摩盘数据新 | 557525.0 | 2026-07-10 12:01:17 | 数据集2 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `feiquanzhan_jjingdongziying` | 京东自营_非全站数据 | 28647.0 | 2026-07-10 08:49:22 | 数据集2 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `jingdong_quanzhan` | 京东自营_全站 | 1653.0 | 2026-07-10 08:49:43 | 数据集2 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `jingdongfeiquanzhantuiguanghuafei` | 京东佑美旗舰店_推广花费 | 45596.0 | 2026-07-10 08:23:36 | 数据集2 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `jingdongquanzhantuiguanghuafei` | 京东佑美旗舰店_全站推广花费 | 3748.0 | 2026-07-10 08:23:19 | 数据集2 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |
| C | detail_like | `jingdongziyingxiaoshouliuliangshuju` | 京东自营_销售流量数据 | 163496.0 | 2026-07-10 08:49:10 | 数据集2 / 查询0 / 下游任务1 | source_silent_missing_candidate：silent_missing, row_count_anomaly, schema_change, text_format_castability |

## 第一批建议先对口径的表

这 15 张不是最终自动上线清单，而是建议优先和业务核对中文含义、字段口径和规则方向的第一批 S/A 候选。确认后再进入 BI 规则配置。

| 分数 | 优先级 | 角色 | 表名 | 中文/别名线索 | 来源 | 行数 | 文本字段占比 | 执行策略 | 使用证据 | 易丢/易错点 | 建议规则方向 |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| 237 | A | result_like | `dws_douyin_spu_sales_detail` | DWS_抖音_SPU销售明细 | bi_or_unknown | 94013 | 0.2016 | latest_partition_or_limited_scan | 数据集37 / 查询322 / 下游任务38 | 业务日期/分区断档、分区为空、行数突降；主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing |
| 232.8 | A | result_like | `ud_3418004512502203_spbmxssjllsj` | 商品编码销售数据、流量数据、推广数据 | bi_or_unknown | 618104 | 0.1439 | latest_partition_or_limited_scan | 数据集54 / 查询288 / 下游任务58 | 主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空；销售额/退款额/库存金额等金额异常或口径突变 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, primary_key_unique, promotion_fee_abnormal, referential_integrity |
| 227.6 | S | result_like | `ud_3418004512502203_dxsthxqb` | dwd_销售退货详情表 | bi_or_unknown | 24816626 | 0.451 | partition_or_metadata_only | 数据集147 / 查询196 / 下游任务16 | 主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空；销售额/退款额/库存金额等金额异常或口径突变 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, primary_key_unique, referential_integrity |
| 218.4 | A | result_like | `ud_3418004512502203_n23pddsjqx` | 2.3拼多多数据清洗 | bi_or_unknown | 969324 | 0.2 | latest_partition_or_limited_scan | 数据集33 / 查询154 / 下游任务39 | 业务日期/分区断档、分区为空、行数突降；主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing |
| 208.9 | A | result_like | `ods_api_jstqm_sale_order_info_f` | ODS_销售订单信息表(聚水潭奇门API) | api_ingestion | 23312740 | 0.9877 | partition_or_metadata_only | 数据集55 / 查询9 / 下游任务13 | 业务日期/分区断档、分区为空、行数突降；源表字段多为文本，数字/日期字段可能出现空串、脏值、不可转换；主键重复或主键为空 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 199.0 | A | result_like | `ods_api_jstqm_sale_order_info_du` | ODS_销售订单信息表(聚水潭奇门API) | api_ingestion | 25408030 | 0.988 | partition_or_metadata_only | 数据集52 / 查询0 / 下游任务4 | 业务日期/分区断档、分区为空、行数突降；源表字段多为文本，数字/日期字段可能出现空串、脏值、不可转换；主键重复或主键为空 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 197 | A | result_like | `ud_3418004512502203_ddyxsjyzhb` | DWD_抖音_订单销售明细 | bi_or_unknown | 761271 | 0.3269 | latest_partition_or_limited_scan | 数据集15 / 查询308 / 下游任务12 | 业务日期/分区断档、分区为空、行数突降；主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing |
| 194.8 | A | result_like | `ud_5179579576634064_tmxsjhzb` | 天猫-销售计划总表 | bi_or_unknown | 14890 | 0.3158 | latest_partition_or_limited_scan | 数据集27 / 查询238 / 下游任务22 | 主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空；销售额/退款额/库存金额等金额异常或口径突变 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, primary_key_unique, referential_integrity |
| 187.7 | A | detail_like | `ods_api_jstbz_product_sku_info_f` | ODS_商品SKU信息表(聚水潭标准API) | api_ingestion | 49492 | 0.9833 | latest_partition_or_limited_scan | 数据集46 / 查询7 / 下游任务24 | 业务日期/分区断档、分区为空、行数突降；源表字段多为文本，数字/日期字段可能出现空串、脏值、不可转换；主键重复或主键为空 | amount_abnormal, core_field_null, cost_price_abnormal, freshness, primary_key_unique, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 186.6 | A | result_like | `ud_3418004512502203_n22jdymqjdzz` | 2.2京东佑美旗舰店总综合表 | bi_or_unknown | 112068 | 0.275 | latest_partition_or_limited_scan | 数据集16 / 查询126 / 下游任务32 | 业务日期/分区断档、分区为空、行数突降；主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, referential_integrity, row_count_anomaly, silent_missing |
| 183.6 | A | result_like | `ud_3418004512502203_n3jdzyhjzzhb` | 3.京东自营和京造综合表 | bi_or_unknown | 65696 | 0.2419 | latest_partition_or_limited_scan | 数据集23 / 查询126 / 下游任务26 | 主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空；销售额/退款额/库存金额等金额异常或口径突变 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, primary_key_unique, referential_integrity |
| 182.0 | A | result_like | `ud_3418004512502203_sxssjqx` | STD_抖音_订单销售明细 | bi_or_unknown | 824838 | 0.5357 | latest_partition_or_limited_scan | 数据集7 / 查询280 / 下游任务7 | 业务日期/分区断档、分区为空、行数突降；主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing |
| 181.2 | A | result_like | `ud_5179579576634064_tmtgzb` | 天猫-推广总表 | bi_or_unknown | 281713 | 0.1154 | latest_partition_or_limited_scan | 数据集13 / 查询252 / 下游任务9 | 主键重复或主键为空；商品/店铺/订单/日期/金额等核心字段为空；销售额/退款额/库存金额等金额异常或口径突变 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, primary_key_unique, promotion_fee_abnormal, referential_integrity |
| 181.0 | A | result_like | `ods_api_dd_sale_order_list_info_du` | ODS_销售订单列表信息表(抖店API) | api_ingestion | 3226101 | 0.9892 | partition_or_metadata_only | 数据集20 / 查询0 / 下游任务6 | 业务日期/分区断档、分区为空、行数突降；源表字段多为文本，数字/日期字段可能出现空串、脏值、不可转换；主键重复或主键为空 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 177.8 | A | result_like | `ud_3418004512502203_sxsddxxb` | std_销售订单信息表 | bi_or_unknown | 24884809 | 0.9167 | partition_or_metadata_only | 数据集30 / 查询98 / 下游任务20 | 业务日期/分区断档、分区为空、行数突降；源表字段多为文本，数字/日期字段可能出现空串、脏值、不可转换；主键重复或主键为空 | amount_abnormal, core_field_null, downstream_consistency, freshness, primary_key_unique, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |

## 其他可讨论候选

| 分数 | 优先级 | 角色 | 表名 | 中文/别名线索 | 来源 | 使用证据 | 建议规则方向 |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 177 | A | result_like | `ud_3418004512502203_ssxszb` | std_四小时总表 | bi_or_unknown | 数据集8 / 查询378 / 下游任务5 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, primary_key_unique, promotion_fee_abnormal, referential_integrity |
| 175.4 | A | result_like | `ods_api_tb_trades_sold_increment_info_f` | ODS_更新时间交易订单信息表(淘宝API) | api_ingestion | 数据集16 / 查询14 / 下游任务3 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 174.8 | A | result_like | `ud_3418004512502203_qjspzlb` | 全局_商品资料表 | bi_or_unknown | 数据集27 / 查询98 / 下游任务16 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, primary_key_unique, referential_integrity |
| 172.2 | A | result_like | `ud_3418004512502203_n22pddsjqx` | 2.2拼多多数据清洗 | bi_or_unknown | 数据集20 / 查询182 / 下游任务6 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, referential_integrity, row_count_anomaly, silent_missing |
| 172.0 | A | result_like | `ud_5179579576634064_tmsptyfzb` | 天猫-综合体验分 | bi_or_unknown | 数据集20 / 查询140 / 下游任务16 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, promotion_fee_abnormal, referential_integrity |
| 170.0 | A | source_like | `huizongbiao` | 天猫综合表 | yingdao_db_text | 数据集34 / 查询0 / 下游任务20 | core_field_null, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, schema_change, silent_missing, text_format_castability |
| 167.8 | A | result_like | `ud_1_swxtgdptghfx` | std_万相台各店铺推广花费详细数据 | bi_or_unknown | 数据集11 / 查询98 / 下游任务7 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing |
| 166.7 | A | detail_like | `ods_api_jstbz_suite_product_info_f` | ODS_组合商品信息表(聚水潭标准API) | api_ingestion | 数据集26 / 查询7 / 下游任务17 | amount_abnormal, core_field_null, cost_price_abnormal, freshness, primary_key_unique, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 165.6 | A | result_like | `ud_3418004512502203_dzxmxb` | dwd_滞销明细表 | bi_or_unknown | 数据集21 / 查询196 / 下游任务3 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, primary_key_unique, referential_integrity |
| 165.6 | A | result_like | `ud_5179579576634064_tmll` | 天猫-流量 | bi_or_unknown | 数据集24 / 查询196 / 下游任务12 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, referential_integrity |
| 163.0 | A | result_like | `ud_3418004512502203_n12ztzhkbdj` | 1.2总体综合看板搭建 | bi_or_unknown | 数据集13 / 查询140 / 下游任务14 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, promotion_fee_abnormal, referential_integrity |
| 161.4 | A | result_like | `ud_3418004512502203_n21xhsztsjkb` | 2.1小红书整体数据宽表 | bi_or_unknown | 数据集18 / 查询84 / 下游任务25 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, referential_integrity |
| 159.0 | A | result_like | `ud_3418004512502203_n11gptsjzh` | 1.1各平台数据整合 | bi_or_unknown | 数据集13 / 查询140 / 下游任务10 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, promotion_fee_abnormal, referential_integrity |
| 155.0 | A | source_like | `peijian` | 配件 | yingdao_db_text | 数据集22 / 查询0 / 下游任务29 | core_field_null, primary_key_unique, referential_integrity, row_count_anomaly, schema_change, silent_missing, text_format_castability |
| 153.8 | A | result_like | `ud_3418004512502203_n1gygddxqb` | 1.各员工钉钉详情表 | dingtalk_or_form | 数据集19 / 查询98 / 下游任务10 | core_field_null, downstream_consistency, primary_key_unique, referential_integrity, text_format_castability |
| 153.8 | A | result_like | `ud_3418004512502203_yyglqtb` | dwd_仓库大屏 | bi_or_unknown | 数据集8 / 查询98 / 下游任务6 | amount_abnormal, core_field_null, downstream_consistency, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 149.8 | A | result_like | `ud_3418004512502203_n12addshlsjq` | 1.2按订单售后率数据清洗综合表 | bi_or_unknown | 数据集16 / 查询98 / 下游任务6 | amount_abnormal, core_field_null, downstream_consistency, freshness, primary_key_unique, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 149.7 | A | detail_like | `ods_api_jstqm_sale_outstock_info_f` | ODS_销售出库信息表(聚水潭奇门API) | api_ingestion | 数据集20 / 查询7 / 下游任务6 | amount_abnormal, core_field_null, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 148.8 | A | result_like | `ud_3418004512502203_n21qnhtshlzh` | 2.1千牛后台售后率综合表 | bi_or_unknown | 数据集13 / 查询168 / 下游任务9 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, referential_integrity |
| 146.2 | A | result_like | `ud_3418004512502203_n21tmxjyfjs` | 2.1天猫小件运费计算 | bi_or_unknown | 数据集3 / 查询112 / 下游任务10 | amount_abnormal, core_field_null, cost_price_abnormal, downstream_consistency, primary_key_unique, referential_integrity |
| 146.0 | A | source_like | `ods_api_jstbz_sale_order_info_du` | ODS_销售订单信息表(聚水潭标准API) | api_ingestion | 数据集10 / 查询0 / 下游任务1 | amount_abnormal, core_field_null, cost_price_abnormal, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 145.0 | A | result_like | `ud_3418004512502203_tmpddjdpkdyf` | 天猫、拼多多、京东pop快递运费 | bi_or_unknown | 数据集11 / 查询140 / 下游任务10 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, referential_integrity |
| 144.7 | A | detail_like | `ods_api_jstqm_sale_order_info_f_ss` | ODS_销售订单信息表_实时(聚水潭奇门API) | api_ingestion | 数据集8 / 查询7 / 下游任务1 | amount_abnormal, core_field_null, cost_price_abnormal, freshness, primary_key_unique, promotion_fee_abnormal, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 144.0 | A | result_like | `ud_3418004512502203_n3tmspqkxgsj` | 3.天猫商品情况相关数据 | bi_or_unknown | 数据集8 / 查询210 / 下游任务5 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, referential_integrity |
| 143.8 | A | result_like | `ud_1_sthtkxxb` | std_退货退款信息表 | bi_or_unknown | 数据集11 / 查询98 / 下游任务5 | amount_abnormal, core_field_null, downstream_consistency, freshness, primary_key_unique, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 143.8 | A | result_like | `ud_3418004512502203_n11xsckxxb` | 1.1销售出库信息表 | bi_or_unknown | 数据集11 / 查询98 / 下游任务5 | amount_abnormal, core_field_null, downstream_consistency, freshness, primary_key_unique, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |
| 143.2 | A | result_like | `ud_5179579576634064_tmdmpsjzb` | 天猫-达摩盘数据总表 | bi_or_unknown | 数据集11 / 查询112 / 下游任务11 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, referential_integrity |
| 141.8 | A | result_like | `ud_5179579576634064_xypmzb` | 行业排名总表 | bi_or_unknown | 数据集13 / 查询98 / 下游任务9 | amount_abnormal, core_field_null, downstream_consistency, primary_key_unique, referential_integrity |
| 141.6 | A | result_like | `ud_3418004512502203_dgxnckcsj` | dwd_各虚拟仓库存数据 | bi_or_unknown | 数据集18 / 查询196 / 下游任务6 | core_field_null, downstream_consistency, primary_key_unique, referential_integrity |
| 123.0 | A | source_like | `ods_api_jstbz_refund_info_du` | ODS_退货退款信息表(聚水潭标准API) | api_ingestion | 数据集10 / 查询0 / 下游任务2 | amount_abnormal, core_field_null, freshness, primary_key_unique, referential_integrity, row_count_anomaly, silent_missing, text_format_castability |

## 剔除/暂不治理

| 优先级 | 角色 | 表名 | 中文/别名线索 | 剔除原因 |
| --- | --- | --- | --- | --- |
| A | result_like | `ods_api_jstqm_archive_sale_order_info_du` | ODS_销售订单归档信息表(聚水潭奇门API) | 归档/历史/备份表，不做日常 freshness/行数规则，暂不进入第一批 |
| A | result_like | `ods_api_jstqm_archive_sale_order_info_f` | ODS_销售订单归档信息表(聚水潭奇门API) | 归档/历史/备份表，不做日常 freshness/行数规则，暂不进入第一批 |
| A | source_like | `ods_api_jstbz_archive_sale_order_info_du` | ODS_销售订单归档信息表(聚水潭标准API) | 归档/历史/备份表，不做日常 freshness/行数规则，暂不进入第一批 |
| A | detail_like | `dwd_data_government_meta_sql_related_resource` | 数据治理元数据_SQL关联资源表 | 平台/治理元数据表，不作为业务质量规则第一批 |
| A | source_like | `UD_5179579576634064_MH19B_tmzhbxhzb` | 天猫综合表.xlsx-汇总表 | Excel/upload/test-like，不作为第一批生产规则表 |
| A | detail_like | `std_data_government_meta_table` | 数据治理元数据_表 | 平台/治理元数据表，不作为业务质量规则第一批 |
| A | source_like | `ods_db_cube_dc_auth_api_config_detail_info_f` | api授权信息 | 平台/治理元数据表，不作为业务质量规则第一批 |

## 使用方式

建议先核对第一批 S/A 候选和 text 源库静默缺失候选。确认中文名、来源、字段含义和规则方向后，再进入 BI 数据质量规则配置。

完整逐表证据见 `config/dq/first_batch_rule_candidates.yml`，其中包含字段风险、少量样本、枚举样本和元数据证据。

