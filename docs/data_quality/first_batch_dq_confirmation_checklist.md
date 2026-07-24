# 第一批数据质量规则人工确认清单

生成时间：2026-07-10 14:28:08

用途：这份清单用于你最终确认哪些表进入正式配置。每张表已经对应到任务详情页的任务 code；确认后即可按 `first_batch_dq_configuration_plan.md` 逐表配置。

## 确认口径

- 默认建议确认通过：15 张重点表，以及影刀 text 中有下游、近期活跃、非手工月度账单的表。
- 默认暂不进入：无下游影刀表、长期固化观察表、除运费险外的手工月度账单表、归档订单表。
- 影刀/text 库账单类表除运费险账单外不需要人工确认；如果任务性质是手动上传、手动执行、月度处理或财务账单拆分，默认不进入规则配置。
- 第一阶段规则只预警不阻断。
- 大表按任务产出行数、昨天分区或昨天业务日期检查，不做全表扫描。

## 待确认清单

| 确认 | 范围 | 表 | 中文/业务名 | 任务 code | 任务名 | 建议规则方向 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 待确认 | core_15 | `dws_douyin_spu_sales_detail` | DWS_抖音_SPU销售明细 | `Ghu44PRchu` | 2.2抖音_销售经营数据综合表-抖音_销售经营综合表【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | core_15 | `ud_3418004512502203_spbmxssjllsj` | 商品编码销售数据、流量数据、推广数据 | `tCQHRUr2lz` | 3.dws_天猫销售经营综合数据清洗-商品编码销售数据、流量数据、推广数据【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负 |  |
| 待确认 | core_15 | `ud_3418004512502203_dxsthxqb` | dwd_销售退货详情表 | `WsaMDlzNGI` | 2.dwd_淘宝数据清洗-dwd_销售退货详情表【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负 | 需确认 S 级影响和告警人 |
| 待确认 | core_15 | `ud_3418004512502203_n23pddsjqx` | 2.3拼多多数据清洗 | `vTeCxTA2tz` | 2.2拼多多数据清洗-2.3拼多多数据清洗【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | core_15 | `ods_api_jstqm_sale_order_info_f` | ODS_销售订单信息表(聚水潭奇门API) | `9hARYiuSyx` | ods_api_jstqm_sale_order_info_f【EtlDevelop任务】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | core_15 | `ods_api_jstqm_sale_order_info_du` | ODS_销售订单信息表(聚水潭奇门API) | `MvuyryYfyY` | ODS_销售订单信息表(聚水潭奇门API)【连接器】（更新时间取数-可以补数据） | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | core_15 | `ud_3418004512502203_ddyxsjyzhb` | DWD_抖音_订单销售明细 | `lI6tx3AsC7` | 2.1 DWD_抖音数据清洗综合表-DWD_抖音销售经营综合表【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | core_15 | `ud_5179579576634064_tmxsjhzb` | 天猫-销售计划总表 | `s9Apa7nuXH` | 天猫销售计划-天猫-销售计划总表【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负 |  |
| 待确认 | core_15 | `ods_api_jstbz_product_sku_info_f` | ODS_商品SKU信息表(聚水潭标准API) | `4v6XI21730` | ods_api_jstbz_product_sku_info_f【EtlDevelop任务】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | core_15 | `ud_3418004512502203_n22jdymqjdzz` | 2.2京东佑美旗舰店总综合表 | `BRQxUQstRp` | 2.2京东佑美旗舰店_销售、售后、推广、流量综合表-2.2京东佑美旗舰店总综合表【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | core_15 | `ud_3418004512502203_n3jdzyhjzzhb` | 3.京东自营和京造综合表 | `7lAvjA2Tc5` | 3.DWD京东自营和京造销售流量推广数据综合表-3.京东自营和京造综合表【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负 |  |
| 待确认 | core_15 | `ud_3418004512502203_sxssjqx` | STD_抖音_订单销售明细 | `5aMpRAhBmy` | 1.1 STD_抖音销售清洗表-STD_销售数据清洗【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | core_15 | `ud_5179579576634064_tmtgzb` | 天猫-推广总表 | `tIae4qir6w` | 天猫-推广-天猫-推广总表【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负 |  |
| 待确认 | core_15 | `ods_api_dd_sale_order_list_info_du` | ODS_销售订单列表信息表(抖店API) | `mnMTqusbga` | ODS_销售订单列表信息表(抖店API)【连接器】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | core_15 | `ud_3418004512502203_sxsddxxb` | std_销售订单信息表 | `QUMvyo4abs` | 1.1std_淘宝销售和售后数据清洗-std_销售订单信息表【刷新】 | 昨天业务日期行数存在；主键非空/重复；核心字段空值；金额字段格式/非负；业务日期格式 |  |
| 待确认 | yingdao_text_active_downstream | `huizongbiao` | 天猫综合表 | `dd65mm262W` | 汇总表【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaoxiaoshoujihuabiao` | 天猫-销售计划表 | `2LqykyNRIR` | 天猫-销售计划表【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaobaozhengjinxiangmucahifen` | 天猫_保证金数据拆分 | `UHAP7pVbut` | 天猫_保证金数据拆分【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `pdd_tgzx_promotion_report_store_promotion_store_unit` | 拼多多推广中心推广报表店铺推广明星店铺单元 | `AIaML9Envt` | 拼多多推广中心推广报表店铺推广明星店铺单元【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaoshangpinIDcaigoufuzeren` | 天猫商品ID采购负责人综合表 | `ksgnfDHEJd` | 天猫商品ID采购负责人综合表【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `ODS_YOUMEIPDDxiaoshoudingdanbiao` | ODS_佑美拼多多销售订单数据 | `l0Koxecy0d` | ODS_佑美拼多多销售订单数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `shangpinpintuilv` | 天猫-商品品退率明细 | `2su02FO3o5` | 天猫-商品品退率明细【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `ODS_DOUYINZONGHEBIAO` | ODS_抖音综合表 | `mJ44GUeDiF` | ODS_抖音综合表【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `douyinyunfeixian` | ODS_抖音_运费险账单数据_RPA | `sXAhYSBWoO` | 抖音-运费险账单数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `shangpinchapinglv` | 天猫-商品差评率明细 | `9re4KEg377` | 天猫-商品差评率明细【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaokuaidilanshouxinxibiao` | 天猫快递揽收信息表 | `KFATFW5AWM` | 天猫快递揽收信息表【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `shoudanlijin` | 天猫-首单礼金 | `2BgNQLUOly` | 天猫-首单礼金【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `liuliangshuju` | 京东_商品明细sku流量数据 | `XOeOLYTRVz` | 京东_商品明细sku流量数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `xunicang_kc` | 虚拟仓库存数据 | `TycXab0KdW` | 虚拟仓库存数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `jingdongxiaohsoushuju` | 京东佑美旗舰店_销售数据 | `LgsTeae8S9` | 京东佑美旗舰店_销售数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `jingzaoxiaoshouliuliangshuju` | 京东京造_sku销售流量数据 | `qXaEHo33Z1` | 京东京造_sku销售流量数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `ods_dyyunfeixian` | ODS_抖音运费险_填报 | `dTuaRL2T1U` | ods-抖音运费险【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `pdd_sjzx_product_data_product_details` | 拼多多数据中心商品数据商品明细商品明细效果 | `QiasZaRhiR` | 拼多多数据中心商品数据商品明细商品明细效果【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `shangpinpaihang_liuliangdata_day` | 按日流量数据 | `4d6xB5qWaD` | 按日流量数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaopingjiayouli` | 天猫-评价有礼 | `FQsL4E0jwT` | 天猫-评价有礼【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaosixiaoshouxiaoshoushuju` | 天猫四小时_销售数据 | `hw6NL2SdrE` | 天猫四小时_销售数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmoyingxiaotuoguanjinshiwutiandierban` | 天猫-营销托管近十五天第二版 | `3D6d7Qe8iq` | 天猫-营销托管近十五天第二版【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `zhongdianpinpaimingtongji` | 天猫-重点品排名统计-日排名 | `kRaOyaiXTH` | 天猫-重点品排名统计-日排名【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `anrishoutaosousuo` | 按日手淘搜索_旧版 | `O8qSgo2Xqg` | 按日手淘搜索_旧版【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `damopanshujuxin` | 天猫-达摩盘数据新 | `S4OKHd96oN` | 天猫-达摩盘数据新【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `feiquanzhan_jjingdongziying` | 京东自营_非全站数据 | `0H6vA8a1eg` | 京东自营_非全站数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `jingdong_quanzhan` | 京东自营_全站 | `364O6KqVg7` | 京东自营_全站【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `jingdongfeiquanzhantuiguanghuafei` | 京东佑美旗舰店_推广花费 | `5wwtEDpPYu` | 京东佑美旗舰店_推广花费【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `jingdongquanzhantuiguanghuafei` | 京东佑美旗舰店_全站推广花费 | `kZKsV4jeZp` | 京东佑美旗舰店_全站推广花费【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `jingdongziyingxiaoshouliuliangshuju` | 京东自营_销售流量数据 | `uPw9lmKbzW` | 京东自营_销售流量数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `odsziyinghejingzaoshouhoushujubiao` | 京东售后数据 | `GwQTxmlYjX` | 京东售后数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `pdd_product_promotion_whole_store_hosting` | 拼多多-商品推广全店托管 | `ip8eDwje09` | 拼多多-商品推广全店托管【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `pdd_product_promotion_whole_store_hosting_overview` | 拼多多-商品推广概况全店托管 | `cTcFjycErR` | 拼多多-商品推广概况全店托管【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `pdd_promotion_reportproduct_promotion_dailyunit` | 拼多多推广报表商品推广日报单元 | `ZjaKsqKDhn` | 拼多多推广报表商品推广日报单元【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `pinduoduoshoushoushuju` | ODS_拼多多售后数据 | `q340kVIT8D` | ODS_拼多多售后数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `shangpinlanshoumingxi` | 天猫-商品揽收明细 | `noeqZ7sy6C` | 天猫-商品揽收明细【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `shangpintiyanfen` | 天猫-商品体验分 | `oUuexw03Jd` | 天猫-商品体验分【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `shipingid` | 视频id | `z0aIrIlDAx` | 视频id【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复 |  |
| 待确认 | yingdao_text_active_downstream | `shoutaosousuo_liuliangdata_day` | 按日手淘搜索流量数据 | `eJaaISZlhL` | 按日手淘搜索流量数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `taobaoke_liuliangdata_day` | 按日淘宝客流量数据 | `d3QZcR5SPj` | 按日淘宝客流量数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `taobaokejiuban` | 按日淘宝客_旧版 | `VDaIPYslyR` | 按日淘宝客_旧版【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaochaipinlvdingdanmingxibiao` | 天猫_商品差评订单明细 | `aKuSZUh727` | 天猫_商品差评订单明细【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaodamopanguanjianci` | 天猫-达摩盘-关键词 | `774aE1672V` | 天猫-达摩盘-关键词【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaohongbaohexiao` | 天猫-红包核销 | `8da46yam1L` | 天猫-红包核销【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaoliuliangzhengti` | 天猫-生意参谋-流量整体 | `jcwfnDZ1gc` | 天猫-生意参谋-流量整体【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaopeifudakuan` | 天猫-赔付打款 | `KK69MCzfVu` | 天猫-赔付打款【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaopinzhituikuan` | 品质退款 | `hwuwGnqt3o` | 品质退款【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaoshengyicanmouliuliangxinban` | 天猫-生意参谋-流量来源-新版 | `9UcdbFLDbK` | 天猫-生意参谋-流量来源-新版【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaosixiaohouhuopinyunying` | 天猫佑美_四小时_货品运营主体列表 | `AdAXlr6bdI` | 天猫佑美_四小时_货品运营主体列表【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaosixiaoquanzhanjihuanliebiao` | 天猫佑美_四小时_全站计划列表 | `FRcHsNnaPc` | 天猫佑美_四小时_全站计划列表【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaosixiaoshiguanjianci` | 天猫佑美_四小时_关键词单元列表 | `8Iw51FobWo` | 天猫佑美_四小时_关键词单元列表【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaosixiaoshoujingzhunrenqun` | 天猫佑美_四小时_精准人群主体列表 | `ZFgRwt8pwx` | 天猫佑美_四小时_精准人群主体列表【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaosixiaoshoushouhoushuju` | 天猫四小时_售后数据 | `MrgTBqP3OZ` | 天猫四小时_售后数据【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaotaokeyongjin` | 天猫-淘客佣金 | `mXemzumUf5` | 天猫-淘客佣金【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaotuiguangduanzhiliandong` | 天猫推广-短直联动 | `ETeKlnHukA` | 天猫推广-短直联动【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaoyingxiaofeiyongjinshitian` | 天猫-营销托管近十天 | `theaP49FvI` | 天猫-营销托管近十天【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tianmaoyingxiaotuoguanfeiyong` | 天猫-营销托管 | `EIQDTb55i2` | 天猫-营销托管【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `tuiguanghongbaofanhuan` | 拼多多-推广红包返还 | `ufakHsRsfg` | 拼多多-推广红包返还【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `xhsjg_global_ad_creative` | 小红书聚光-全局报表广告创意分日 | `d786YokWIk` | 小红书聚光-全局报表广告创意分日【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |
| 待确认 | yingdao_text_active_downstream | `xhspgy_data_center_export` | 小红书蒲公英-数据中心导出 | `MKq88uhasI` | 小红书蒲公英-数据中心导出【迁移】 | 任务产出行数/自定义SQL；任务产出行数波动；字段结构变化；主键非空/重复；核心字段空值 |  |

