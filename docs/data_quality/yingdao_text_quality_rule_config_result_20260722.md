# 影刀/text 源接入专项质量规则配置结果

更新时间：2026-07-22

## 配置口径

- 本批范围：`first_batch_dq_configuration_plan.yml` 中 `yingdao_text_active_downstream` 的 60 张表。
- 适用场景：影刀/text 源表有下游依赖，需发现“任务执行成功但本次接入 0 行”的静默缺失。
- 规则类型：任务规则。
- 规则模板：单次执行成功数据条数，固定值。
- 异常条件：`计算值 <= 0`。
- 异常阻断：否，仅预警。
- 告警渠道：IM 个人消息，接收人包含包彦。
- 告警配置同时写入任务对象和表对象；当任务 ID 与表 ID 相同时只写一次。
- 本批不使用业务日期字段、不扫全表，避免对大表造成额外负担。

## 复核结果

- 配置表数：60。
- 复核通过：60。
- 缺失或失败：0。

## 已完成配置明细

| 中文业务名 | 物理表名 | 任务 ID | 表 ID | 规则 ID | 规则口径 |
| --- | --- | --- | --- | --- | --- |
| 天猫综合表 | huizongbiao | dd65mm262W | dd65mm262W | sCs7jJFU3r | 单次执行成功数据条数 <= 0 |
| 天猫-销售计划表 | tianmaoxiaoshoujihuabiao | 2LqykyNRIR | fgqg5oHIc8 | Mwc7VDomcw | 单次执行成功数据条数 <= 0 |
| 天猫_保证金数据拆分 | tianmaobaozhengjinxiangmucahifen | UHAP7pVbut | FusnsJo9eb | hZ6DohxmJG | 单次执行成功数据条数 <= 0 |
| 拼多多推广中心推广报表店铺推广明星店铺单元 | pdd_tgzx_promotion_report_store_promotion_store_unit | AIaML9Envt | VMAjLCBroB | DEgHtz75iN | 单次执行成功数据条数 <= 0 |
| 天猫商品ID采购负责人综合表 | tianmaoshangpinIDcaigoufuzeren | ksgnfDHEJd | 5Lslf3fO4f | c0sXoduAKp | 单次执行成功数据条数 <= 0 |
| ODS_佑美拼多多销售订单数据 | ODS_YOUMEIPDDxiaoshoudingdanbiao | l0Koxecy0d | APg16Xm9uD | rX6tPzYW8g | 单次执行成功数据条数 <= 0 |
| 天猫-商品品退率明细 | shangpinpintuilv | 2su02FO3o5 | Ti6B9Jue0w | iLKGS0uPO8 | 单次执行成功数据条数 <= 0 |
| ODS_抖音综合表 | ODS_DOUYINZONGHEBIAO | mJ44GUeDiF | FbQbJfyXzD | U0eM6Y8RVC | 单次执行成功数据条数 <= 0 |
| ODS_抖音_运费险账单数据_RPA | douyinyunfeixian | sXAhYSBWoO | NccHkKZD8B | i5auAxb6sK | 单次执行成功数据条数 <= 0 |
| 天猫-商品差评率明细 | shangpinchapinglv | 9re4KEg377 | XY8kIkSC8O | NCeWRuRabX | 单次执行成功数据条数 <= 0 |
| 天猫快递揽收信息表 | tianmaokuaidilanshouxinxibiao | KFATFW5AWM | W0ual0amDe | 4g4oRQUCz7 | 单次执行成功数据条数 <= 0 |
| 天猫-首单礼金 | shoudanlijin | 2BgNQLUOly | q0A5nBK3Gc | n1qwFwvbI4 | 单次执行成功数据条数 <= 0 |
| 京东_商品明细sku流量数据 | liuliangshuju | XOeOLYTRVz | 8sgB8D8d4F | RTgBq7WOfH | 单次执行成功数据条数 <= 0 |
| 虚拟仓库存数据 | xunicang_kc | TycXab0KdW | TycXab0KdW | 9xe2p915VU | 单次执行成功数据条数 <= 0 |
| 京东佑美旗舰店_销售数据 | jingdongxiaohsoushuju | LgsTeae8S9 | HwMtlpnDKL | GaeY4zeFZ4 | 单次执行成功数据条数 <= 0 |
| 京东京造_sku销售流量数据 | jingzaoxiaoshouliuliangshuju | qXaEHo33Z1 | uRgxSDx277 | 7pAnxp9YTg | 单次执行成功数据条数 <= 0 |
| ODS_抖音运费险_填报 | ods_dyyunfeixian | dTuaRL2T1U | OwuEOi1uOy | K7c9uxQtNS | 单次执行成功数据条数 <= 0 |
| 拼多多数据中心商品数据商品明细商品明细效果 | pdd_sjzx_product_data_product_details | QiasZaRhiR | 0XMZFAEKpj | iuemlaX7HR | 单次执行成功数据条数 <= 0 |
| 按日流量数据 | shangpinpaihang_liuliangdata_day | 4d6xB5qWaD | 4d6xB5qWaD | 4vwdSqzEu6 | 单次执行成功数据条数 <= 0 |
| 天猫-评价有礼 | tianmaopingjiayouli | FQsL4E0jwT | LwQHlGDWn3 | 8esN5FJLUb | 单次执行成功数据条数 <= 0 |
| 天猫四小时_销售数据 | tianmaosixiaoshouxiaoshoushuju | hw6NL2SdrE | y5Ax6qrJ5i | WEuAghRZOi | 单次执行成功数据条数 <= 0 |
| 天猫-营销托管近十五天第二版 | tianmoyingxiaotuoguanjinshiwutiandierban | 3D6d7Qe8iq | iVuA6kZmYf | YiMnMIjcqs | 单次执行成功数据条数 <= 0 |
| 天猫-重点品排名统计-日排名 | zhongdianpinpaimingtongji | kRaOyaiXTH | 58OckSpkkv | KN8UQ2p79V | 单次执行成功数据条数 <= 0 |
| 按日手淘搜索_旧版 | anrishoutaosousuo | O8qSgo2Xqg | BjeQqI5HVF | UN82RJy8eO | 单次执行成功数据条数 <= 0 |
| 天猫-达摩盘数据新 | damopanshujuxin | S4OKHd96oN | W2Og2IFsnB | YS4klHV07z | 单次执行成功数据条数 <= 0 |
| 京东自营_非全站数据 | feiquanzhan_jjingdongziying | 0H6vA8a1eg | Iqs1BE0ySa | TDac7gntdn | 单次执行成功数据条数 <= 0 |
| 京东自营_全站 | jingdong_quanzhan | 364O6KqVg7 | wwKwZyiYQ3 | 9VuyHiXk1k | 单次执行成功数据条数 <= 0 |
| 京东佑美旗舰店_推广花费 | jingdongfeiquanzhantuiguanghuafei | 5wwtEDpPYu | 8jcB35whfQ | SG8sUAzuw4 | 单次执行成功数据条数 <= 0 |
| 京东佑美旗舰店_全站推广花费 | jingdongquanzhantuiguanghuafei | kZKsV4jeZp | b9wh2yfSnp | zJQv9A9U66 | 单次执行成功数据条数 <= 0 |
| 京东自营_销售流量数据 | jingdongziyingxiaoshouliuliangshuju | uPw9lmKbzW | hfeYQdyZ6a | cks1GRrqvz | 单次执行成功数据条数 <= 0 |
| 京东售后数据 | odsziyinghejingzaoshouhoushujubiao | GwQTxmlYjX | B5KmwnVTo8 | KbeKHYP8HU | 单次执行成功数据条数 <= 0 |
| 拼多多-商品推广全店托管 | pdd_product_promotion_whole_store_hosting | ip8eDwje09 | BOQF6BQaTU | 4Q8EGSF9W0 | 单次执行成功数据条数 <= 0 |
| 拼多多-商品推广概况全店托管 | pdd_product_promotion_whole_store_hosting_overview | cTcFjycErR | mDMviBaCJs | tAayqDFMJE | 单次执行成功数据条数 <= 0 |
| 拼多多推广报表商品推广日报单元 | pdd_promotion_reportproduct_promotion_dailyunit | ZjaKsqKDhn | XNAt653aOf | XIq0VsOxQ7 | 单次执行成功数据条数 <= 0 |
| ODS_拼多多售后数据 | pinduoduoshoushoushuju | q340kVIT8D | X96vA8u2de | hHOuXTJBTM | 单次执行成功数据条数 <= 0 |
| 天猫-商品揽收明细 | shangpinlanshoumingxi | noeqZ7sy6C | r9awd7jp1Y | gRMraKttpn | 单次执行成功数据条数 <= 0 |
| 天猫-商品体验分 | shangpintiyanfen | oUuexw03Jd | Kg6ln4cD6l | jsw3fiiu5Y | 单次执行成功数据条数 <= 0 |
| 视频id | shipingid | z0aIrIlDAx | z0aIrIlDAx | Vja6j7aYyV | 单次执行成功数据条数 <= 0 |
| 按日手淘搜索流量数据 | shoutaosousuo_liuliangdata_day | eJaaISZlhL | eJaaISZlhL | ma8A2Yi2Lj | 单次执行成功数据条数 <= 0 |
| 按日淘宝客流量数据 | taobaoke_liuliangdata_day | d3QZcR5SPj | d3QZcR5SPj | i4MRvui8p3 | 单次执行成功数据条数 <= 0 |
| 按日淘宝客_旧版 | taobaokejiuban | VDaIPYslyR | ZswfjzEN7V | OKg7M67FOs | 单次执行成功数据条数 <= 0 |
| 天猫_商品差评订单明细 | tianmaochaipinlvdingdanmingxibiao | aKuSZUh727 | TG6B9rsPl1 | 2VcRDr68xO | 单次执行成功数据条数 <= 0 |
| 天猫-达摩盘-关键词 | tianmaodamopanguanjianci | 774aE1672V | Azc9w2fYt4 | ofuYUJEeFi | 单次执行成功数据条数 <= 0 |
| 天猫-红包核销 | tianmaohongbaohexiao | 8da46yam1L | wIczqOxqOH | DMctDo2x0F | 单次执行成功数据条数 <= 0 |
| 天猫-生意参谋-流量整体 | tianmaoliuliangzhengti | jcwfnDZ1gc | G6wtsQlSPl | pveICia5mC | 单次执行成功数据条数 <= 0 |
| 天猫-赔付打款 | tianmaopeifudakuan | KK69MCzfVu | kHqqU2wujg | TfAjLVzD43 | 单次执行成功数据条数 <= 0 |
| 品质退款 | tianmaopinzhituikuan | hwuwGnqt3o | UkcLgEeuYj | f0KwZWphKp | 单次执行成功数据条数 <= 0 |
| 天猫-生意参谋-流量来源-新版 | tianmaoshengyicanmouliuliangxinban | 9UcdbFLDbK | nluazvOrDX | Qrc5GLDFkp | 单次执行成功数据条数 <= 0 |
| 天猫佑美_四小时_货品运营主体列表 | tianmaosixiaohouhuopinyunying | AdAXlr6bdI | 2fsTWtN6c2 | HFgJoh5jLY | 单次执行成功数据条数 <= 0 |
| 天猫佑美_四小时_全站计划列表 | tianmaosixiaoquanzhanjihuanliebiao | FRcHsNnaPc | hKcBdPPBZN | BIAhgE4d99 | 单次执行成功数据条数 <= 0 |
| 天猫佑美_四小时_关键词单元列表 | tianmaosixiaoshiguanjianci | 8Iw51FobWo | 59ALbptKKF | fs67VZ77zn | 单次执行成功数据条数 <= 0 |
| 天猫佑美_四小时_精准人群主体列表 | tianmaosixiaoshoujingzhunrenqun | ZFgRwt8pwx | G48MqYGBXv | tHK0b2o1JO | 单次执行成功数据条数 <= 0 |
| 天猫四小时_售后数据 | tianmaosixiaoshoushouhoushuju | MrgTBqP3OZ | GC4opW64wy | rlcddHeSy7 | 单次执行成功数据条数 <= 0 |
| 天猫-淘客佣金 | tianmaotaokeyongjin | mXemzumUf5 | ZRQLNLNKCE | Rs4kb1dmrv | 单次执行成功数据条数 <= 0 |
| 天猫推广-短直联动 | tianmaotuiguangduanzhiliandong | ETeKlnHukA | FqeU2ZMc8V | pe6ZBXS6mj | 单次执行成功数据条数 <= 0 |
| 天猫-营销托管近十天 | tianmaoyingxiaofeiyongjinshitian | theaP49FvI | ekuAi3cNSo | DUaQTsWerk | 单次执行成功数据条数 <= 0 |
| 天猫-营销托管 | tianmaoyingxiaotuoguanfeiyong | EIQDTb55i2 | JwsFZnU8CB | lU4asivAQs | 单次执行成功数据条数 <= 0 |
| 拼多多-推广红包返还 | tuiguanghongbaofanhuan | ufakHsRsfg | C5qMdS7wWB | sGsFlY49v8 | 单次执行成功数据条数 <= 0 |
| 小红书聚光-全局报表广告创意分日 | xhsjg_global_ad_creative | d786YokWIk | k1s7J9am6x | r1uIAHXUBw | 单次执行成功数据条数 <= 0 |
| 小红书蒲公英-数据中心导出 | xhspgy_data_center_export | MKq88uhasI | OFakvvVr0S | Z5Kc5sR9Cc | 单次执行成功数据条数 <= 0 |
