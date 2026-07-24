WITH source_items AS
(
    SELECT
        shop_id,
        order_id,
        arrayJoin(arrayZip(JSONExtractArrayRaw(sku_order_list), arrayEnumerate(JSONExtractArrayRaw(sku_order_list)))) AS item_tuple
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
), item_rows AS
(
    SELECT DISTINCT
        shop_id,
        order_id,
        toUInt16(item_tuple.2) AS item_index,
        nullIf(JSONExtractString(item_tuple.1, 'sku_order_id'), '') AS sku_order_id,
        coalesce(
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'product_id_str'), '"', ''), ''),
            nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'product_id'), '"', ''), '')
        ) AS product_id,
        nullIf(replaceAll(JSONExtractRaw(item_tuple.1, 'sku_id'), '"', ''), '') AS sku_id
    FROM source_items
), package_rows AS
(
    SELECT DISTINCT
        shop_id,
        order_id,
        toUInt16(pkg_tuple.2) AS package_index,
        nullIf(JSONExtractString(pkg_tuple.1, 'delivery_id'), '') AS package_id,
        nullIf(JSONExtractString(pkg_tuple.1, 'tracking_no'), '') AS tracking_no,
        nullIf(JSONExtractString(pkg_tuple.1, 'company_name'), '') AS logistics_company_name,
        if(toInt64OrNull(JSONExtractRaw(pkg_tuple.1, 'ship_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(pkg_tuple.1, 'ship_time')), 'Asia/Shanghai')) AS shipped_at,
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
        order_id,
        package_index,
        package_id,
        tracking_no,
        logistics_company_name,
        shipped_at,
        toUInt16(product_tuple.2) AS package_product_index,
        nullIf(JSONExtractString(product_tuple.1, 'sku_order_id'), '') AS sku_order_id,
        coalesce(
            nullIf(JSONExtractString(product_tuple.1, 'product_id_str'), ''),
            nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'product_id'), '"', ''), '')
        ) AS product_id,
        nullIf(replaceAll(JSONExtractRaw(product_tuple.1, 'sku_id'), '"', ''), '') AS sku_id,
        toInt64OrNull(JSONExtractRaw(product_tuple.1, 'product_count')) AS shipped_product_count
    FROM package_rows
    ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
)
SELECT
    '商品明细来源粒度' AS check_name,
    count() AS row_count,
    uniqExact(tuple(shop_id, order_id, item_index)) AS item_index_key_count,
    uniqExact(tuple(shop_id, order_id, sku_order_id)) AS sku_order_id_key_count,
    countIf(sku_order_id IS NULL) AS sku_order_id_null_count
FROM item_rows;

WITH package_rows AS
(
    SELECT DISTINCT
        shop_id,
        order_id,
        toUInt16(pkg_tuple.2) AS package_index,
        nullIf(JSONExtractString(pkg_tuple.1, 'delivery_id'), '') AS package_id,
        nullIf(JSONExtractString(pkg_tuple.1, 'tracking_no'), '') AS tracking_no,
        nullIf(JSONExtractString(pkg_tuple.1, 'company_name'), '') AS logistics_company_name,
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
)
SELECT
    '物流包裹来源粒度' AS check_name,
    count() AS package_rows,
    uniqExact(tuple(shop_id, order_id, package_index)) AS package_index_key_count,
    uniqExact(tuple(shop_id, order_id, package_id)) AS package_id_key_count,
    uniqExact(tuple(shop_id, order_id, tracking_no)) AS tracking_no_key_count,
    countIf(package_id IS NULL) AS package_id_null_count,
    countIf(tracking_no IS NULL) AS tracking_no_null_count
FROM package_rows;

WITH package_rows AS
(
    SELECT DISTINCT
        shop_id,
        order_id,
        toUInt16(pkg_tuple.2) AS package_index,
        nullIf(JSONExtractString(pkg_tuple.1, 'delivery_id'), '') AS package_id,
        nullIf(JSONExtractString(pkg_tuple.1, 'tracking_no'), '') AS tracking_no,
        nullIf(JSONExtractString(pkg_tuple.1, 'company_name'), '') AS logistics_company_name,
        if(toInt64OrNull(JSONExtractRaw(pkg_tuple.1, 'ship_time')) IN (0, NULL), NULL, toDateTime(toInt64OrZero(JSONExtractRaw(pkg_tuple.1, 'ship_time')), 'Asia/Shanghai')) AS shipped_at,
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
        order_id,
        package_index,
        package_id,
        tracking_no,
        toUInt16(product_tuple.2) AS package_product_index,
        nullIf(JSONExtractString(product_tuple.1, 'sku_order_id'), '') AS sku_order_id
    FROM package_rows
    ARRAY JOIN arrayZip(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')), arrayEnumerate(JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')))) AS product_tuple
)
SELECT
    '物流包裹商品关系粒度' AS check_name,
    count() AS package_product_rows,
    uniqExact(tuple(shop_id, order_id, package_index, package_product_index)) AS package_product_index_key_count,
    uniqExact(tuple(shop_id, order_id, tracking_no, sku_order_id)) AS tracking_no_sku_order_id_key_count,
    uniqExact(tuple(shop_id, order_id, package_id, sku_order_id)) AS package_id_sku_order_id_key_count,
    countIf(sku_order_id IS NULL) AS sku_order_id_null_count
FROM package_product_rows;

WITH package_rows AS
(
    SELECT DISTINCT
        shop_id,
        order_id,
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
        order_id,
        package_index,
        package_id,
        tracking_no,
        nullIf(JSONExtractString(product_tuple.1, 'sku_order_id'), '') AS sku_order_id
    FROM package_rows
    ARRAY JOIN JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')) AS product_tuple
), by_package AS
(
    SELECT
        shop_id,
        order_id,
        package_id,
        tracking_no,
        uniqExact(sku_order_id) AS sku_order_count
    FROM package_product_rows
    GROUP BY shop_id, order_id, package_id, tracking_no
), by_sku_order AS
(
    SELECT
        shop_id,
        order_id,
        sku_order_id,
        uniqExact(tracking_no) AS tracking_no_count
    FROM package_product_rows
    GROUP BY shop_id, order_id, sku_order_id
)
SELECT
    '包裹和子订单对应关系' AS check_name,
    countIf(sku_order_count = 1) AS one_sku_order_packages,
    countIf(sku_order_count > 1) AS multi_sku_order_packages,
    max(sku_order_count) AS max_sku_order_per_package,
    (SELECT countIf(tracking_no_count = 1) FROM by_sku_order) AS one_package_sku_orders,
    (SELECT countIf(tracking_no_count > 1) FROM by_sku_order) AS multi_package_sku_orders,
    (SELECT max(tracking_no_count) FROM by_sku_order) AS max_tracking_no_per_sku_order
FROM by_package;

WITH source_items AS
(
    SELECT
        shop_id,
        order_id,
        arrayJoin(arrayZip(JSONExtractArrayRaw(sku_order_list), arrayEnumerate(JSONExtractArrayRaw(sku_order_list)))) AS item_tuple
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE dt = '2026-07-22'
), item_rows AS
(
    SELECT DISTINCT
        shop_id,
        order_id,
        nullIf(JSONExtractString(item_tuple.1, 'sku_order_id'), '') AS sku_order_id
    FROM source_items
), package_rows AS
(
    SELECT DISTINCT
        shop_id,
        order_id,
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
        order_id,
        nullIf(JSONExtractString(product_tuple, 'sku_order_id'), '') AS sku_order_id
    FROM package_rows
    ARRAY JOIN JSONExtractArrayRaw(JSONExtractRaw(package_json, 'product_info')) AS product_tuple
)
SELECT
    '商品明细与物流商品sku_order_id覆盖关系' AS check_name,
    (SELECT count() FROM item_rows) AS item_sku_order_rows,
    (SELECT count() FROM package_product_rows) AS package_product_sku_order_rows,
    (SELECT count() FROM item_rows i LEFT JOIN package_product_rows p ON i.shop_id = p.shop_id AND i.order_id = p.order_id AND i.sku_order_id = p.sku_order_id WHERE p.sku_order_id IS NULL) AS item_not_in_package_product_count,
    (SELECT count() FROM package_product_rows p LEFT JOIN item_rows i ON i.shop_id = p.shop_id AND i.order_id = p.order_id AND i.sku_order_id = p.sku_order_id WHERE i.sku_order_id IS NULL) AS package_product_not_in_item_count;
