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
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_order_id'), '"', ''), '') AS sku_order_id
    FROM package_rows
    ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
), by_package AS
(
    SELECT
        shop_id,
        shop_order_id,
        package_id,
        tracking_no,
        groupArray(sku_order_id) AS sku_order_ids,
        uniqExact(sku_order_id) AS sku_order_count
    FROM package_product_rows
    GROUP BY shop_id, shop_order_id, package_id, tracking_no
), by_sku_order AS
(
    SELECT
        shop_id,
        shop_order_id,
        sku_order_id,
        groupArray(tracking_no) AS tracking_nos,
        groupArray(package_id) AS package_ids,
        uniqExact(tracking_no) AS tracking_no_count
    FROM package_product_rows
    GROUP BY shop_id, shop_order_id, sku_order_id
), by_tracking AS
(
    SELECT
        shop_id,
        shop_order_id,
        tracking_no,
        groupArray(package_id) AS package_ids,
        uniqExact(package_id) AS package_id_count
    FROM package_rows
    GROUP BY shop_id, shop_order_id, tracking_no
)
SELECT
    'multi_sku_order_package_example' AS check_name,
    shop_id,
    shop_order_id,
    package_id,
    tracking_no,
    sku_order_count,
    arrayStringConcat(sku_order_ids, ',') AS sku_order_ids
FROM by_package
WHERE sku_order_count > 1
ORDER BY sku_order_count DESC, shop_order_id
LIMIT 5;

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
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_order_id'), '"', ''), '') AS sku_order_id
    FROM package_rows
    ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
), by_sku_order AS
(
    SELECT
        shop_id,
        shop_order_id,
        sku_order_id,
        groupArray(tracking_no) AS tracking_nos,
        groupArray(package_id) AS package_ids,
        uniqExact(tracking_no) AS tracking_no_count
    FROM package_product_rows
    GROUP BY shop_id, shop_order_id, sku_order_id
)
SELECT
    'split_sku_order_example' AS check_name,
    shop_id,
    shop_order_id,
    sku_order_id,
    tracking_no_count,
    arrayStringConcat(tracking_nos, ',') AS tracking_nos,
    arrayStringConcat(package_ids, ',') AS package_ids
FROM by_sku_order
WHERE tracking_no_count > 1
ORDER BY shop_order_id, sku_order_id
LIMIT 5;

WITH package_rows AS
(
    SELECT DISTINCT
        shop_id,
        order_id AS shop_order_id,
        toUInt16(pkg_tuple.2) AS package_index,
        nullIf(JSONExtractString(pkg_tuple.1, 'delivery_id'), '') AS package_id,
        nullIf(JSONExtractString(pkg_tuple.1, 'tracking_no'), '') AS tracking_no
    FROM
    (
        SELECT
            shop_id,
            order_id,
            arrayJoin(arrayZip(JSONExtractArrayRaw(logistics_info), arrayEnumerate(JSONExtractArrayRaw(logistics_info)))) AS pkg_tuple
        FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
        WHERE dt = '2026-07-22'
    )
), by_tracking AS
(
    SELECT
        shop_id,
        shop_order_id,
        tracking_no,
        groupArray(package_id) AS package_ids,
        uniqExact(package_id) AS package_id_count
    FROM package_rows
    GROUP BY shop_id, shop_order_id, tracking_no
)
SELECT
    'duplicate_tracking_no_example' AS check_name,
    shop_id,
    shop_order_id,
    tracking_no,
    package_id_count,
    arrayStringConcat(package_ids, ',') AS package_ids
FROM by_tracking
WHERE package_id_count > 1
ORDER BY shop_order_id, tracking_no
LIMIT 5;
