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
        uniqExact(sku_order_id) AS sku_order_count
    FROM package_product_rows
    GROUP BY shop_id, shop_order_id, package_id, tracking_no
), by_sku_order AS
(
    SELECT
        shop_id,
        shop_order_id,
        sku_order_id,
        uniqExact(tracking_no) AS tracking_no_count,
        uniqExact(package_id) AS package_id_count
    FROM package_product_rows
    GROUP BY shop_id, shop_order_id, sku_order_id
)
SELECT
    'package_sku_cardinality' AS check_name,
    (SELECT count() FROM package_rows) AS package_rows,
    (SELECT uniqExact(tuple(shop_id, shop_order_id, package_id)) FROM package_rows) AS package_id_keys,
    (SELECT uniqExact(tuple(shop_id, shop_order_id, tracking_no)) FROM package_rows) AS tracking_no_keys,
    countIf(sku_order_count = 1) AS one_sku_order_packages,
    countIf(sku_order_count > 1) AS multi_sku_order_packages,
    max(sku_order_count) AS max_sku_order_per_package,
    (SELECT count() FROM by_sku_order) AS shipped_sku_order_keys,
    (SELECT countIf(tracking_no_count = 1) FROM by_sku_order) AS one_tracking_no_sku_orders,
    (SELECT countIf(tracking_no_count > 1) FROM by_sku_order) AS multi_tracking_no_sku_orders,
    (SELECT max(tracking_no_count) FROM by_sku_order) AS max_tracking_no_per_sku_order,
    (SELECT countIf(package_id_count = 1) FROM by_sku_order) AS one_package_id_sku_orders,
    (SELECT countIf(package_id_count > 1) FROM by_sku_order) AS multi_package_id_sku_orders,
    (SELECT max(package_id_count) FROM by_sku_order) AS max_package_id_per_sku_order
FROM by_package;
