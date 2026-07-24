SELECT
    'ods_api_dd_sale_order_list_info_f' AS source_table,
    'suffix_f' AS naming_signal,
    count() AS row_count,
    uniqExact(order_id) AS distinct_shop_order_count,
    uniqExact(dt) AS partition_count,
    groupUniqArray(dt) AS partitions,
    uniqExact(yuce_task_instance_id) AS task_instance_count,
    uniqExact(yuce_cube_shop_id) AS cube_shop_count,
    min(toDateTime(toInt64OrZero(create_time), 'Asia/Shanghai')) AS min_create_time,
    max(toDateTime(toInt64OrZero(create_time), 'Asia/Shanghai')) AS max_create_time,
    min(toDateTime(toInt64OrZero(update_time), 'Asia/Shanghai')) AS min_update_time,
    max(toDateTime(toInt64OrZero(update_time), 'Asia/Shanghai')) AS max_update_time,
    countIf(toInt64OrZero(pay_time) = 0) AS zero_pay_time_count
FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f;
