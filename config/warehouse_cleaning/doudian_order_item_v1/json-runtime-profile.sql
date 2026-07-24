/* READ ONLY: profile JSON field presence without emitting raw JSON values. */
WITH item_rows AS
(
    SELECT
        arrayJoin(JSONExtractArrayRaw(sku_order_list)) AS item_json
    FROM youmei_sandbox.ods_api_dd_sale_order_list_info_f
    WHERE sku_order_list != ''
), field_observations AS
(
    SELECT arrayJoin(JSONExtractKeys(item_json)) AS field_name
    FROM item_rows
)
SELECT
    uniqExact(field_name) AS actual_item_top_level_field_count,
    count() AS item_field_observations
FROM field_observations;

/* The detailed field tree is frozen in json-expansion-inventory.yaml, sourced
   from the official interface response schema. */
