WITH source_items AS
(
    SELECT
        shop_id,
        order_id AS shop_order_id,
        arrayJoin(arrayZip(JSONExtractArrayRaw(sku_order_list), arrayEnumerate(JSONExtractArrayRaw(sku_order_list)))) AS item_tuple
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
), item_rows AS
(
    SELECT DISTINCT
        shop_id,
        shop_order_id,
        toUInt16(item_tuple.2) AS item_index,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'order_id'), '"', ''), '') AS item_order_id,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'parent_order_id'), '"', ''), '') AS item_parent_order_id,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'master_sku_order_id'), '"', ''), '') AS master_sku_order_id
    FROM source_items
)
SELECT
    'item_candidate_keys' AS check_name,
    count() AS item_rows,
    uniqExact(tuple(shop_id, shop_order_id, item_index)) AS item_index_keys,
    uniqExact(tuple(shop_id, shop_order_id, item_order_id)) AS item_order_id_keys,
    countIf(item_order_id IS NULL) AS item_order_id_null_count,
    uniqExact(tuple(shop_id, shop_order_id, master_sku_order_id)) AS master_sku_order_id_keys,
    countIf(master_sku_order_id IS NULL OR master_sku_order_id = '0') AS master_sku_order_id_blank_count,
    uniqExact(tuple(shop_id, item_order_id)) AS global_item_order_id_keys
FROM item_rows;
