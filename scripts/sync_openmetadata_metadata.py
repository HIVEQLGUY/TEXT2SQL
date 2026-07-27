#!/usr/bin/env python3
"""Synchronize the approved minimal warehouse metadata contract to OpenMetadata."""
from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


TABLE_EXTENSION_KEYS = {"composite_key_fields", "refresh_mode", "upstream_tables", "warehouse_layer"}
COLUMN_EXTENSION_KEYS = {"source_fields", "calculation_logic", "enum_values", "field_logic_version", "field_logic_updated_at"}
PROPERTY_LABELS = {
    "composite_key_fields": ("联合主键", "构成业务联合主键的中文名和物理字段名"),
    "refresh_mode": ("刷新模式", "full_snapshot、window_full_snapshot 或 incremental"),
    "upstream_tables": ("上游表", "直接上游正式表的中文名、物理名和FQN"),
    "warehouse_layer": ("数仓层级", "ODS、DWD、DIM、DWS 或 ADS"),
    "source_fields": ("来源字段", "字段的上游字段或JSON路径"),
    "calculation_logic": ("计算逻辑", "字段转换、单位、精度、聚合和空值策略"),
    "enum_values": ("枚举值", "枚举字段的取值定义；非枚举为空列表"),
    "field_logic_version": ("字段逻辑版本", "只在字段计算逻辑变化时递增"),
    "field_logic_updated_at": ("字段逻辑最近更新时间", "新字段逻辑正式生效时间"),
}


def load_yaml(path: Path) -> dict[str, Any]:
    import yaml
    value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("元数据契约根节点必须是对象")
    return value


def ch_type_to_om(value: str) -> str:
    value = str(value or "String").strip()
    while value.startswith(("Nullable(", "LowCardinality(")) and value.endswith(")"):
        value = value[value.index("(") + 1:-1].strip()
    base = value.split("(", 1)[0].upper()
    if base in {"STRING", "FIXEDSTRING"}: return "STRING"
    if base == "DATE": return "DATE"
    if base in {"DATETIME", "DATETIME64"}: return "DATETIME"
    if base.startswith(("INT8", "INT16", "INT32", "UINT8", "UINT16", "UINT32")): return "INT"
    if base.startswith(("INT64", "INT128", "INT256", "UINT64", "UINT128", "UINT256")): return "BIGINT"
    if base.startswith("DECIMAL"): return "DECIMAL"
    if base.startswith("FLOAT"): return "DOUBLE"
    if base in {"BOOL", "BOOLEAN"}: return "BOOLEAN"
    if base.startswith("ARRAY"): return "ARRAY"
    if base.startswith("MAP"): return "MAP"
    if base.startswith("TUPLE"): return "STRUCT"
    return "STRING"


class Client:
    def __init__(self, base_url: str, username: str, password: str) -> None:
        self.base = base_url.rstrip("/") + "/api/v1"
        self.username, self.password, self.token = username, password, ""

    def request(self, method: str, path: str, body: Any = None) -> dict[str, Any]:
        headers = {"Content-Type": "application/json-patch+json" if method == "PATCH" else "application/json"}
        if self.token: headers["Authorization"] = f"Bearer {self.token}"
        payload = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
        request = urllib.request.Request(self.base + path, data=payload, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                raw = response.read().decode("utf-8", "replace")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            raise RuntimeError(f"{method} {path} 失败: HTTP {exc.code}: {detail[:1000]}") from exc

    def login(self) -> None:
        encoded = base64.b64encode(self.password.encode()).decode()
        self.token = str(self.request("POST", "/users/login", {"email": self.username, "password": encoded})["accessToken"])


def text_value(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if isinstance(value, (dict, list)) else str(value)


def column_payload(column: dict[str, Any], ordinal: int) -> dict[str, Any]:
    ext = {key: text_value(column.get(key, [] if key in {"source_fields", "enum_values"} else {})) for key in COLUMN_EXTENSION_KEYS}
    return {"name": column["physical_name"], "displayName": column["chinese_name"],
            "description": column["business_meaning"], "dataType": ch_type_to_om(column["data_type"]),
            "dataTypeDisplay": column.get("data_type_display", column["data_type"]), "ordinalPosition": ordinal,
            "tags": [], "extension": ext}


def payload(contract: dict[str, Any]) -> dict[str, Any]:
    table, metadata = contract["table"], contract["table_metadata"]
    extension = {key: text_value(metadata[key]) for key in TABLE_EXTENSION_KEYS}
    return {"name": table["name"], "displayName": table["display_name"], "description": "",
            "databaseSchema": table["database_schema_fqn"], "tableType": "Regular", "tags": [],
            "columns": [column_payload(c, i) for i, c in enumerate(contract["columns"], 1)], "extension": extension}


def read_table(client: Client, fqn: str) -> dict[str, Any] | None:
    try: return client.request("GET", "/tables/name/" + urllib.parse.quote(fqn, safe="") + "?fields=extension,tags,columns")
    except RuntimeError as exc:
        if "HTTP 404" in str(exc): return None
        raise


def ensure_custom_properties(client: Client) -> None:
    """Register the fixed minimal property vocabulary once, before table updates."""
    table_type = client.request("GET", "/metadata/types/name/table")
    types = client.request("GET", "/metadata/types?limit=100").get("data", [])
    string_type = next((item for item in types if item.get("name") == "string"), None)
    if not string_type: raise RuntimeError("OpenMetadata 未提供 string 自定义属性类型")
    existing_result = client.request("GET", "/metadata/types/name/table/customProperties")
    existing = existing_result if isinstance(existing_result, list) else existing_result.get("customProperties", [])
    names = {str(item.get("name")) for item in existing}
    for name, (display_name, description) in PROPERTY_LABELS.items():
        if name in names: continue
        client.request("PUT", f"/metadata/types/{table_type['id']}", {
            "name": name, "displayName": display_name, "description": description,
            "propertyType": {"id": string_type.get("id"), "type": "type", "name": "string", "fullyQualifiedName": "string"},
        })


def clear_entity_tags(client: Client, entity_id: str) -> None:
    """Tags are outside the approved minimum metadata set and must not linger."""
    client.request("PATCH", f"/tables/{urllib.parse.quote(entity_id, safe='')}", [
        {"op": "replace", "path": "/tags", "value": []},
    ])


def verify(client: Client, contract: dict[str, Any]) -> dict[str, Any]:
    expected, fqn = payload(contract), contract["table"]["fully_qualified_name"]
    actual = read_table(client, fqn)
    if not actual: return {"ok": False, "table_exists": False, "table_fqn": fqn}
    actual_columns = {c.get("name"): c for c in actual.get("columns", [])}
    expected_columns = {c["name"]: c for c in expected["columns"]}
    mismatches: list[dict[str, Any]] = []
    for name in sorted(set(actual_columns) & set(expected_columns)):
        got, want = actual_columns[name], expected_columns[name]
        # Column tags can be inherited from the OpenMetadata service hierarchy.
        # They are not part of the approved field metadata contract and cannot
        # be cleared safely at individual-column level without changing parent assets.
        checks = {"displayName": got.get("displayName") == want["displayName"], "description": got.get("description", "") == want["description"],
                  "dataType": got.get("dataType") == want["dataType"], "extension": (got.get("extension") or {}) == want["extension"]}
        if not all(checks.values()): mismatches.append({"name": name, "failed_checks": [k for k,v in checks.items() if not v]})
    extension = actual.get("extension") or {}
    table_checks = {"displayName": actual.get("displayName") == expected["displayName"], "description": actual.get("description", "") == "",
                    "tags": not actual.get("tags", []), "extension": extension == expected["extension"]}
    missing, unexpected = sorted(set(expected_columns)-set(actual_columns)), sorted(set(actual_columns)-set(expected_columns))
    return {"ok": not missing and not unexpected and not mismatches and all(table_checks.values()), "table_exists": True, "table_fqn": fqn,
            "expected_column_count": len(expected_columns), "actual_column_count": len(actual_columns), "missing_columns": missing,
            "unexpected_columns": unexpected, "column_mismatches": mismatches, "table_failed_checks": [k for k,v in table_checks.items() if not v],
            "actual_table_extension_keys": sorted(extension)}


def validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("status") not in {"approved", "active"}: raise ValueError("元数据契约未获批准")
    metadata = contract.get("table_metadata", {})
    if set(metadata) != TABLE_EXTENSION_KEYS: raise ValueError("表级元数据必须且只能包含四项扩展属性")
    for column in contract.get("columns", []):
        if set(COLUMN_EXTENSION_KEYS) - set(column): raise ValueError(f"字段缺少最小元数据: {column.get('physical_name')}")
        fingerprint = column.get("logic_fingerprint", "")
        if not fingerprint or len(str(fingerprint)) != 64: raise ValueError(f"字段逻辑指纹无效: {column.get('physical_name')}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("plan", "apply", "verify"), required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--base-url", default=os.getenv("OPENMETADATA_BASE_URL", "http://127.0.0.1:8585"))
    parser.add_argument("--username", default=os.getenv("OPENMETADATA_USERNAME", "admin@open-metadata.org"))
    parser.add_argument("--password-env", default="OPENMETADATA_PASSWORD")
    args = parser.parse_args()
    password = os.getenv(args.password_env, "")
    if not password: raise SystemExit("缺少 OpenMetadata 密码环境变量")
    contract = load_yaml(args.contract); validate_contract(contract)
    client = Client(args.base_url, args.username, password); client.login()
    fqn = contract["table"]["fully_qualified_name"]
    existing = read_table(client, fqn)
    if args.mode == "plan":
        print(json.dumps({"ok": True, "mode": "plan", "table_fqn": fqn, "exists": bool(existing), "columns": len(contract["columns"]), "table_extension_keys": sorted(TABLE_EXTENSION_KEYS), "column_extension_keys": sorted(COLUMN_EXTENSION_KEYS)}, ensure_ascii=False)); return 0
    if args.mode == "verify":
        print(json.dumps({"ok": True, "mode": "verify", "verification": verify(client, contract)}, ensure_ascii=False)); return 0
    if not existing: raise SystemExit("正式表未在 OpenMetadata 发现，禁止本次元数据修订创建新资产")
    ensure_custom_properties(client)
    result = client.request("PUT", "/tables", payload(contract))
    clear_entity_tags(client, str(result.get("id") or existing.get("id")))
    outcome = verify(client, contract)
    print(json.dumps({"ok": outcome["ok"], "mode": "apply", "table_fqn": fqn, "entity_id": result.get("id"), "verification": outcome}, ensure_ascii=False)); return 0 if outcome["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
