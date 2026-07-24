#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path("/mnt/c/Users/24796/Documents/TEXT2SQL/TEXT2SQL-codex-handoff")
BASE = "http://127.0.0.1:8585/api/v1"
CREDENTIALS = REPO / "web/data-agent-workspace/credentials.local.json"


def request(method: str, path: str, body: dict | None = None, token: str = "") -> dict:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def login() -> str:
    credentials = json.loads(CREDENTIALS.read_text(encoding="utf-8-sig"))["openmetadata"]
    body = {
        "email": credentials["username"],
        "password": base64.b64encode(credentials["password"].encode()).decode(),
    }
    return request("POST", "/users/login", body)["accessToken"]


def main() -> int:
    token = login()
    service = request("GET", "/services/databaseServices/name/youmei_clickhouse", token=token)
    print(json.dumps({
        "service": service.get("name"),
        "serviceType": service.get("serviceType"),
        "hasConnection": bool(service.get("connection")),
    }, ensure_ascii=False))

    database = "youmei_clickhouse.default"
    schemas = request(
        "GET",
        "/databaseSchemas?database=" + urllib.parse.quote(database, safe=""),
        token=token,
    ).get("data", [])
    print(json.dumps({
        "database": database,
        "schemas": [schema.get("fullyQualifiedName") for schema in schemas],
    }, ensure_ascii=False))

    for schema in schemas:
        schema_fqn = schema.get("fullyQualifiedName")
        tables = request(
            "GET",
            "/tables?databaseSchema="
            + urllib.parse.quote(schema_fqn, safe="")
            + "&limit=100",
            token=token,
        ).get("data", [])
        print(json.dumps({
            "schema": schema_fqn,
            "tables": [
                {
                    "name": table.get("name"),
                    "fullyQualifiedName": table.get("fullyQualifiedName"),
                    "columns": [column.get("name") for column in table.get("columns", [])],
                }
                for table in tables
            ],
        }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
