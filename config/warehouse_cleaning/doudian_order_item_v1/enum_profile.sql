WITH items AS
(
    SELECT arrayJoin(JSONExtractArrayRaw(sku_order_list)) AS sku_item
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE sku_order_list != ''
), values AS
(
    SELECT 'payment_type_code' AS field_name, nullIf(replaceAll(JSONExtractRaw(sku_item, 'pay_type'), '"', ''), '') AS field_value FROM items
    UNION ALL SELECT 'order_entry_code', nullIf(replaceAll(JSONExtractRaw(sku_item, 'b_type'), '"', ''), '') FROM items
    UNION ALL SELECT 'order_scene_code', nullIf(replaceAll(JSONExtractRaw(sku_item, 'sub_b_type'), '"', ''), '') FROM items
    UNION ALL SELECT 'ad_environment_type', nullIf(replaceAll(JSONExtractRaw(sku_item, 'ad_env_type'), '"', ''), '') FROM items
    UNION ALL SELECT 'order_status_code', nullIf(replaceAll(JSONExtractRaw(sku_item, 'order_status'), '"', ''), '') FROM items
    UNION ALL SELECT 'main_status_code', nullIf(replaceAll(JSONExtractRaw(sku_item, 'main_status'), '"', ''), '') FROM items
    UNION ALL SELECT 'order_type_code', nullIf(replaceAll(JSONExtractRaw(sku_item, 'order_type'), '"', ''), '') FROM items
)
SELECT field_name, field_value, count() AS row_count
FROM values
WHERE field_value IS NOT NULL
GROUP BY field_name, field_value
ORDER BY field_name, field_value;
