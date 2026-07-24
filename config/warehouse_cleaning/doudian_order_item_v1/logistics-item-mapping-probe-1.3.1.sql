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
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'order_id'), '"', ''), '') AS item_order_id,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'master_sku_order_id'), '"', ''), '') AS master_sku_order_id,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'product_id'), '"', ''), '') AS product_id,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'sku_id'), '"', ''), '') AS sku_id
    FROM source_items
), package_rows AS
(
    SELECT DISTINCT
        shop_id,
        order_id AS shop_order_id,
        toUInt16(pkg_tuple.2) AS package_index,
        nullIf(JSONExtractString(pkg_tuple.1, 'delivery_id'), '') AS package_id,
        nullIf(JSONExtractString(pkg_tuple.1, 'tracking_no'), '') AS tracking_no,
        pkg_tuple.1 AS package_json
    FROM
    (
        SELECT
            shop_id,
            order_id,
            arrayJoin(arrayZip(JSONExtractArrayRaw(logistics_info), arrayEnumerate(JSONExtractArrayRaw(logistics_info)))) AS pkg_tuple
        FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
        WHERE dt = '2026-07-22'
    )
), package_product_rows AS
(
    SELECT DISTINCT
        shop_id,
        shop_order_id,
        package_index,
        package_id,
        tracking_no,
        toUInt16(product_tuple.2) AS package_product_index,
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_order_id'), '"', ''), '') AS logistics_sku_order_id,
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'product_id'), '"', ''), '') AS logistics_product_id,
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_id'), '"', ''), '') AS logistics_sku_id
    FROM package_rows
    ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
)
SELECT
    'logistics_to_item_mapping' AS check_name,
    (SELECT count() FROM package_product_rows) AS package_product_rows,
    (SELECT count() FROM package_product_rows p INNER JOIN item_rows i ON p.shop_id = i.shop_id AND p.shop_order_id = i.shop_order_id AND p.logistics_sku_order_id = i.item_order_id) AS matched_by_item_order_id,
    (SELECT count() FROM package_product_rows p LEFT JOIN item_rows i ON p.shop_id = i.shop_id AND p.shop_order_id = i.shop_order_id AND p.logistics_sku_order_id = i.item_order_id WHERE i.item_order_id IS NULL) AS unmatched_by_item_order_id,
    (SELECT count() FROM package_product_rows p INNER JOIN item_rows i ON p.shop_id = i.shop_id AND p.shop_order_id = i.shop_order_id AND p.logistics_sku_order_id = i.master_sku_order_id) AS matched_by_master_sku_order_id,
    (SELECT count() FROM package_product_rows p INNER JOIN item_rows i ON p.shop_id = i.shop_id AND p.shop_order_id = i.shop_order_id AND p.logistics_product_id = i.product_id AND p.logistics_sku_id = i.sku_id) AS matched_by_product_sku
;
