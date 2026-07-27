#!/usr/bin/env python3
"""Create immutable v2 minimal OpenMetadata contracts from approved legacy contracts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

PACKAGE = Path(__file__).resolve().parents[1] / "config" / "warehouse_cleaning" / "doudian_order_item_v1"
ODS_FQN = "youmei_clickhouse.default.youmei_sandbox.ods_api_dd_sale_order_list_info_f"
SOURCE_ALIAS = {"snapshot_date": "dt", "shop_order_id": "order_id", "paid_at": "pay_time", "created_at": "create_time", "updated_at": "update_time", "finished_at": "finish_time", "order_expired_at": "order_expire_time", "expected_ship_at": "exp_ship_time", "shipped_at": "ship_time"}


def read(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict): raise ValueError(f"无效契约: {path}")
    return value


def logic(column: dict[str, Any], source: str) -> dict[str, Any]:
    description, data_type = str(column.get("description", "")), str(column.get("data_type", ""))
    is_amount = "金额" in description or "费用" in description
    is_fen = "源单位分" in description or "单位为分" in description
    aggregation = "average" if "平均" in description else "sum" if "合计" in description else "none"
    operation = "direct_mapping"
    formula = f"{source} 直接映射"
    if is_fen:
        operation, formula = "unit_conversion", f"toDecimal({source}) / 100"
    elif is_amount:
        operation, formula = "decimal_standardization", f"toDecimal({source})"
    elif "DateTime" in data_type:
        operation, formula = "time_standardization", f"parse {source} as Asia/Shanghai datetime"
    elif data_type.startswith(("UInt", "Int", "Float")):
        operation, formula = "numeric_standardization", f"cast {source} to {data_type}"
    result: dict[str, Any] = {"operation": operation, "formula": formula, "aggregation": aggregation,
        "null_policy": "空值转NULL", "invalid_policy": "非空非法值进入异常统计"}
    if is_amount:
        result.update({"source_unit": "分" if is_fen else "元", "target_unit": "元", "precision": 2})
    if "DateTime" in data_type: result["timezone"] = "Asia/Shanghai"
    return result


def sources_for(table_name: str, column: dict[str, Any]) -> list[str]:
    physical = str(column["physical_name"])
    source = SOURCE_ALIAS.get(physical, str(column.get("source_field", physical)))
    if table_name.startswith("dwd_"):
        return [f"{ODS_FQN}.{source}"]
    return [source]


def convert(source_path: Path, output_name: str, changed_at: str, upstream: list[dict[str, str]]) -> Path:
    old, table = read(source_path), read(source_path).get("table", {})
    old_table = old["table"]
    columns = []
    for old_column in old.get("columns", []):
        sources = sources_for(old_table["name"], old_column)
        calculation = logic(old_column, sources[0])
        enum = old_column.get("enum_definition") or {}
        enum_values = enum if enum else []
        fingerprint_source = {"source_fields": sources, "calculation_logic": calculation, "enum_values": enum_values, "data_type": old_column["data_type"]}
        columns.append({"chinese_name": old_column["chinese_name"], "physical_name": old_column["physical_name"], "data_type": old_column["data_type"],
            "data_type_display": old_column.get("data_type_display", old_column["data_type"]), "business_meaning": old_column["description"],
            "source_fields": sources, "calculation_logic": calculation, "enum_values": enum_values,
            "field_logic_version": "1.0.0", "field_logic_updated_at": changed_at,
            "logic_fingerprint": hashlib.sha256(json.dumps(fingerprint_source, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()})
    key_columns = [c for c in old.get("columns", []) if c.get("is_primary_key")]
    output = {"contract_id": f"openmetadata_minimal_{old_table['name']}", "contract_version": "2.0.0", "status": "approved",
        "table": {"name": old_table["name"], "display_name": old_table["display_name"], "database_schema_fqn": old_table["database_schema_fqn"], "fully_qualified_name": old_table["fully_qualified_name"]},
        "table_metadata": {"composite_key_fields": [{"chinese_name": c["chinese_name"], "physical_name": c["physical_name"]} for c in key_columns],
            "refresh_mode": {"code": "window_full_snapshot", "chinese_name": "窗口全量快照"}, "upstream_tables": upstream,
            "warehouse_layer": str(old.get("custom_properties", {}).get("warehouse_layer", ""))}, "columns": columns}
    path = PACKAGE / output_name
    path.write_text(yaml.safe_dump(output, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    upstream = [{"chinese_name": "ODS_销售订单列表信息表(抖店API)", "physical_name": "ods_api_dd_sale_order_list_info_f", "fully_qualified_name": ODS_FQN}]
    specs = [("metadata-contract-ods.yaml", "metadata-contract-minimal-ods-2.0.0.yaml", "2026-07-22T00:00:00+08:00", []),
        ("metadata-contract-formal-order-1.3.0.yaml", "metadata-contract-minimal-formal-order-2.0.0.yaml", "2026-07-23T00:00:00+08:00", upstream),
        ("metadata-contract-formal-item-1.3.0.yaml", "metadata-contract-minimal-formal-item-2.0.0.yaml", "2026-07-23T00:00:00+08:00", upstream),
        ("metadata-contract-formal-logistics-tracking-no-1.4.3.yaml", "metadata-contract-minimal-formal-logistics-tracking-no-2.0.0.yaml", "2026-07-26T00:00:00+08:00", upstream)]
    paths = [convert(PACKAGE / old, new, timestamp, parents) for old, new, timestamp, parents in specs]
    print(json.dumps({"ok": True, "contracts": [str(p) for p in paths]}, ensure_ascii=False)); return 0


if __name__ == "__main__": raise SystemExit(main())
