# Generated Data Quality Rule Suggestions v1

Generated at: 2026-07-09

This file summarizes suggested rules generated from `config/dq/table_asset_profile.yml` and `config/dq/rule_templates.yml`.
No BI configuration or production data was modified.

## Coverage

- Generated table config files: 887
- Tables requiring manual confirmation: 782
- Total suggested rules: 1800

## Importance Distribution

| importance | table_count |
| --- | ---: |
| S | 1 |
| A | 51 |
| B | 129 |
| C | 313 |
| REVIEW | 1 |
| IGNORE | 392 |

## Role Distribution

| role | table_count |
| --- | ---: |
| detail_like | 101 |
| dimension_like | 91 |
| export_like | 2 |
| result_like | 123 |
| source_like | 251 |
| summary_like | 10 |
| temp_or_intermediate_like | 103 |
| unknown | 206 |

## Rule Group Distribution

| rule_group | rule_count |
| --- | ---: |
| amount_abnormal | 195 |
| core_field_null | 253 |
| cost_price_abnormal | 125 |
| downstream_consistency | 133 |
| freshness | 307 |
| primary_key_unique | 202 |
| promotion_fee_abnormal | 107 |
| referential_integrity | 176 |
| row_count_anomaly | 184 |
| schema_change | 59 |
| silent_missing | 59 |

## Suppressed Or Observation-Only Tables

| reason | table_count |
| --- | ---: |
| Excel/upload/test-like isolated table without report/query/downstream evidence: no strong rule generated. | 75 |
| IGNORE/stale candidate: only observation reason is generated. | 392 |
| Static/periodic fixed downstream dependency with no direct business consumption or core risk evidence: no rule and no manual confirmation needed. | 105 |

## Manual Review Snapshot

| priority | checklist_items_in_output | total_candidates_before_limit |
| --- | ---: | ---: |
| P0 | 50 | 196 |
| P1 | 40 | 453 |
| P2 | 30 | 88 |

## Top Suggested Rule Files

| importance | role | table | manual_confirm_required | rule_count | reason |
| --- | --- | --- | --- | ---: | --- |
| S | result_like | `ud_3418004512502203_dxsthxqb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `dws_douyin_spu_sales_detail` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ods_api_dd_sale_order_list_info_du` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ods_api_jstqm_archive_sale_order_info_du` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ods_api_jstqm_archive_sale_order_info_f` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ods_api_jstqm_sale_order_info_du` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ods_api_jstqm_sale_order_info_f` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ods_api_tb_trades_sold_increment_info_f` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_1_swxtgdptghfx` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_ddyxsjyzhb` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_n23pddsjqx` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_spbmxssjllsj` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_ssxszb` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_sxssjqx` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_5179579576634064_tmtgzb` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | source_like | `ods_api_jstbz_archive_sale_order_info_du` | true | 8 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Cost or purchase price field |
| A | source_like | `ods_api_jstbz_sale_order_info_du` | true | 8 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Cost or purchase price field |
| A | result_like | `ud_3418004512502203_dzxmxb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_n11gptsjzh` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Promo |
| A | result_like | `ud_3418004512502203_n12ztzhkbdj` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Promo |
| A | result_like | `ud_3418004512502203_n21tmxjyfjs` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_n22jdymqjdzz` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_n22pddsjqx` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_n3jdzyhjzzhb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_qjspzlb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | result_like | `ud_3418004512502203_yyglqtb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Promo |
| A | result_like | `ud_5179579576634064_tmsptyfzb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Promo |
| A | result_like | `ud_5179579576634064_tmxsjhzb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| A | detail_like | `ods_api_jstqm_sale_order_info_f_ss` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Cost or purchase price fields detecte |
| A | source_like | `ods_db_cube_dc_auth_api_config_detail_info_f` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; External source-like table req |
| A | result_like | `ud_1_sthtkxxb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_3418004512502203_n11xsckxxb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_3418004512502203_n12addshlsjq` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_3418004512502203_n21qnhtshlzh` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_3418004512502203_n21xhsztsjkb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_3418004512502203_n3tmspqkxgsj` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_3418004512502203_sxsddxxb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_3418004512502203_tmpddjdpkdyf` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_5179579576634064_tmdmpsjzb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_5179579576634064_tmll` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | result_like | `ud_5179579576634064_xypmzb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| A | detail_like | `dwd_data_government_meta_sql_related_resource` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Cost or purchase price fields detecte |
| A | detail_like | `ods_api_jstbz_product_sku_info_f` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Cost or purchase price fields detecte |
| A | source_like | `ods_api_jstbz_refund_info_du` | true | 6 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected. |
| A | detail_like | `ods_api_jstbz_suite_product_info_f` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Cost or purchase price fields detecte |
| A | detail_like | `ods_api_jstqm_sale_outstock_info_f` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Promotion or ad fee fields detected.; |
| A | result_like | `ud_3418004512502203_dgxnckcsj` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Join key fields detected on fa |
| A | result_like | `ud_3418004512502203_n1gygddxqb` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Join key fields detected on fa |
| A | source_like | `peijian` | true | 5 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules. |
| A | detail_like | `std_data_government_meta_table` | true | 5 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Promotion or ad fee fields detected.; Join key fields detected |
| A | source_like | `UD_5179579576634064_MH19B_tmzhbxhzb` | true | 2 | Table is active or consumed by report/dataset/downstream task.; Amount fields detected. |
| A | source_like | `huizongbiao` | true | 2 | Table is active or consumed by report/dataset/downstream task.; Promotion or ad fee fields detected. |
| REVIEW | detail_like | `ODS_YOUMEIPDDxiaoshoudingdanbiao` | true | 4 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Join key fields detected on fact/result-like table. |
| B | source_like | `ods_api_dd_product_detail_info_du` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; External source-like table req |
| B | source_like | `ods_api_dd_settle_bill_detail_info_du` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; External source-like table req |
| B | source_like | `ods_api_jstbz_product_history_cost_price_info_du` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; External source-like table req |
| B | result_like | `ud_3418004512502203_dgspbmtghfxq` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_dyyspfl` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_mzjzfxsjqx` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_n1stmxssjqx` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_sdytgsj` | true | 9 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ods_api_jingdong_order_info_f` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | source_like | `ods_api_jlqc_live_list_info_du` | true | 8 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Cost or purchase price field |
| B | source_like | `ods_api_jlqc_uni_promition_root_report_info_du` | true | 8 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Cost or purchase price field |
| B | result_like | `ods_api_tb_item_sku_info_f` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | source_like | `ods_api_tb_trades_sold_increment_info_du` | true | 8 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Cost or purchase price field |
| B | source_like | `ods_api_xhsjg_report_offline_note_info_du_xhsjg` | true | 8 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Cost or purchase price field |
| B | result_like | `ud_3418004512502203_ddyxjkdyfjs` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_dwxttghfxqb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Promo |
| B | result_like | `ud_3418004512502203_n21jdzhsj` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_n21zxzhb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_n2tmxjyfjs` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_pdddjyfjs` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_sdyshsjqx` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Promo |
| B | result_like | `ud_3418004512502203_tmrb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_3418004512502203_ykddhd` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_4971200913022541_ddyzbjrlcb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Cost  |
| B | result_like | `ud_5179579576634064_tmrbgptzb` | true | 8 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Promo |
| B | source_like | `ods_api_dd_shop_account_item_info_du` | true | 7 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Promotion or ad fee fields d |
| B | source_like | `ods_api_jingdong_order_info_du` | true | 7 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Cost or purchase price field |
| B | source_like | `ods_api_jstbz_product_sku_info_du` | true | 7 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Cost or purchase price field |
| B | source_like | `ods_api_jstbz_sale_outstock_info_du` | true | 7 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Promotion or ad fee fields d |
| B | detail_like | `ods_api_jstqm_refund_info_f` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Detail/dimension-like table re |
| B | source_like | `ods_api_jstqm_sale_outstock_info_du` | true | 7 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected.; Promotion or ad fee fields d |
| B | source_like | `ods_api_tb_wxtwjb_campaign_report_info_du` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; External source-like table req |
| B | source_like | `ods_api_tb_wxtwjb_item_promotion_report_info_du` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; External source-like table req |
| B | detail_like | `tianmaosixiaoshouxiaoshoushuju` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Detail/dimension-like table re |
| B | result_like | `ud_3418004512502203_dhpbhjhb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_dspbmllsj2` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_dtmsxsllsj` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_dyyryksjdjs` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_n11cgrkxxb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_n11djdzyhjzx` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_n12ahpbmshsj` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_n12jdzyhjzsh` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_n12spddthtkx` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_n14jdjzhzysp` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_n15pddxjkdyf` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_n21ryhjcbzhb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Cost or purchase price fields  |
| B | result_like | `ud_3418004512502203_sjdzyhjzxsdd` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_3418004512502203_spddxsddxxb` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | result_like | `ud_5179579576634064_tmllsjbcss` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected.; Join  |
| B | detail_like | `xhsjg_global_ad_creative` | true | 7 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Cost or purchase price fields detecte |
| B | source_like | `UD_5179579576634064_47ARJ_jdzyhjzzhbxj` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Amount fields detected. |
| B | source_like | `ods_api_jlqc_douyin_account_info_du` | true | 6 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Promotion or ad fee fields detected. |
| B | source_like | `ods_api_jstbz_archive_refund_info_du` | true | 6 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected. |
| B | source_like | `ods_api_jstbz_logistic_order_info_du` | true | 6 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected. |
| B | detail_like | `ods_api_jstbz_sale_outstock_info_f` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Promotion or ad fee fields detected.; |
| B | result_like | `ods_api_jstbz_virtualwh_stock_info_f` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Join key fields detected on fa |
| B | source_like | `ods_api_jstqm_archive_refund_info_du` | true | 6 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected. |
| B | source_like | `ods_api_jstqm_refund_info_du` | true | 6 | Table is active or consumed by report/dataset/downstream task.; External source-like table requires silent missing, row anomaly, schema change, and core field rules.; Amount fields detected. |
| B | detail_like | `std_api_jstbz_product_history_cost_info_f` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Cost or purchase price fields detecte |
| B | dimension_like | `std_api_tb_wxtwjb_adv_release_effect_info_f` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Cost or purchase price fields detecte |
| B | detail_like | `std_data_government_meta_fast_engine_audit_mv` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Detail/dimension-like table requires key uniqueness and core field completeness suggestions.; Amount fields detected.; Cost or purchase price fields detecte |
| B | result_like | `ud_3418004512502203_ddydjkdyfjs` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Join key fields detected on fa |
| B | result_like | `ud_3418004512502203_dljlx` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Join key fields detected on fa |
| B | result_like | `ud_3418004512502203_n11addlshsjq` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Join key fields detected on fa |
| B | result_like | `ud_3418004512502203_n21qnhtcpsjq` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Join key fields detected on fa |
| B | result_like | `ud_3418004512502203_n21qnhtsjqx` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Join key fields detected on fa |
| B | result_like | `ud_3418004512502203_spddsdsj` | true | 6 | Table is active or consumed by report/dataset/downstream task.; Result/export/AI-or-external-use candidate requires freshness, row count, core field, key, and downstream consistency rules.; Join key fields detected on fa |
