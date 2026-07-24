SELECT
    'order_header' AS relation_name,
    count() AS source_rows,
    uniqExact(tuple(shop_id, order_id)) AS key_count,
    count() - uniqExact(tuple(shop_id, order_id)) AS duplicate_rows
FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
WHERE dt = '2026-07-22';

WITH source_items AS
(
    SELECT
        shop_id,
        order_id,
        arrayJoin(arrayEnumerate(JSONExtractArrayRaw(sku_order_list))) AS item_index
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
)
SELECT
    'order_item_shop_order_index' AS relation_name,
    count() AS source_rows,
    uniqExact(tuple(shop_id, order_id, item_index)) AS key_count,
    count() - uniqExact(tuple(shop_id, order_id, item_index)) AS duplicate_rows
FROM source_items;

WITH source_items AS
(
    SELECT
        order_id,
        arrayJoin(arrayEnumerate(JSONExtractArrayRaw(sku_order_list))) AS item_index
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
)
SELECT
    'order_item_order_index' AS relation_name,
    count() AS source_rows,
    uniqExact(tuple(order_id, item_index)) AS key_count,
    count() - uniqExact(tuple(order_id, item_index)) AS duplicate_rows
FROM source_items;
