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
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_id'), '"', ''), '') AS logistics_sku_id,
        toInt64OrNull(JSONExtractRaw(product_tuple.1, 'product_count')) AS shipped_product_count
    FROM package_rows
    ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
)
SELECT
    'item_candidate_keys' AS check_name,
    count() AS item_rows,
    uniqExact(tuple(shop_id, shop_order_id, item_index)) AS item_index_keys,
    uniqExact(tuple(shop_id, shop_order_id, item_order_id)) AS item_order_id_keys,
    countIf(item_order_id IS NULL) AS item_order_id_null_count,
    uniqExact(tuple(shop_id, shop_order_id, master_sku_order_id)) AS master_sku_order_id_keys,
    countIf(master_sku_order_id IS NULL OR master_sku_order_id = '0') AS master_sku_order_id_blank_count
FROM item_rows;

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
    'logistics_sku_mapping' AS check_name,
    (SELECT count() FROM package_product_rows) AS package_product_rows,
    (SELECT count() FROM package_product_rows p INNER JOIN item_rows i ON p.shop_id = i.shop_id AND p.shop_order_id = i.shop_order_id AND p.logistics_sku_order_id = i.item_order_id) AS matched_by_item_order_id,
    (SELECT count() FROM package_product_rows p INNER JOIN item_rows i ON p.shop_id = i.shop_id AND p.shop_order_id = i.shop_order_id AND p.logistics_sku_order_id = i.master_sku_order_id) AS matched_by_master_sku_order_id,
    (SELECT count() FROM package_product_rows p INNER JOIN item_rows i ON p.shop_id = i.shop_id AND p.shop_order_id = i.shop_order_id AND p.logistics_product_id = i.product_id AND p.logistics_sku_id = i.sku_id) AS matched_by_product_sku,
    (SELECT count() FROM package_product_rows p LEFT JOIN item_rows i ON p.shop_id = i.shop_id AND p.shop_order_id = i.shop_order_id AND p.logistics_sku_order_id = i.item_order_id WHERE i.item_order_id IS NULL) AS unmatched_by_item_order_id;

WITH package_rows AS
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
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_order_id'), '"', ''), '') AS logistics_sku_order_id
    FROM package_rows
    ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
), by_package AS
(
    SELECT
        shop_id,
        shop_order_id,
        package_id,
        tracking_no,
        uniqExact(logistics_sku_order_id) AS sku_order_count
    FROM package_product_rows
    GROUP BY shop_id, shop_order_id, package_id, tracking_no
), by_sku_order AS
(
    SELECT
        shop_id,
        shop_order_id,
        logistics_sku_order_id,
        uniqExact(tracking_no) AS tracking_no_count,
        uniqExact(package_id) AS package_id_count
    FROM package_product_rows
    GROUP BY shop_id, shop_order_id, logistics_sku_order_id
)
SELECT
    'package_sku_cardinality' AS check_name,
    countIf(sku_order_count = 1) AS one_sku_order_packages,
    countIf(sku_order_count > 1) AS multi_sku_order_packages,
    max(sku_order_count) AS max_sku_order_per_package,
    (SELECT countIf(tracking_no_count = 1) FROM by_sku_order) AS one_tracking_no_sku_orders,
    (SELECT countIf(tracking_no_count > 1) FROM by_sku_order) AS multi_tracking_no_sku_orders,
    (SELECT max(tracking_no_count) FROM by_sku_order) AS max_tracking_no_per_sku_order,
    (SELECT countIf(package_id_count = 1) FROM by_sku_order) AS one_package_id_sku_orders,
    (SELECT countIf(package_id_count > 1) FROM by_sku_order) AS multi_package_id_sku_orders,
    (SELECT max(package_id_count) FROM by_sku_order) AS max_package_id_per_sku_order
FROM by_package;
