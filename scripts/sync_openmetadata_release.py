#!/usr/bin/env python3
"""Run OpenMetadata sync for every metadata contract in a release package.

This is the project-level wrapper around the deterministic skill script:
  data-warehouse-cleaning/scripts/sync_openmetadata_metadata.py

It discovers metadata contracts from a release YAML, loads the local
OpenMetadata credential env file, then runs plan/apply/verify in a fixed order
and writes a JSON report back to the package directory.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKAGE_DIR = PROJECT_ROOT / "config" / "warehouse_cleaning" / "doudian_order_item_v1"
DEFAULT_ENV_FILE = PROJECT_ROOT / "local" / "credentials" / "openmetadata.env"
DEFAULT_SYNC_SCRIPT = (
    PROJECT_ROOT / "scripts" / "sync_openmetadata_metadata.py"
)


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit("PyYAML is required. Use the bundled Codex Python runtime.") from exc
    with path.open("r", encoding="utf-8-sig") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise SystemExit(f"YAML root must be an object: {path}")
    return value


def load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"OpenMetadata env file not found: {path}")
    loaded: dict[str, str] = {}
    pattern = re.compile(r"^\s*([^#][^=]+)=(.*)$")
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        match = pattern.match(raw_line)
        if not match:
            continue
        key = match.group(1).strip()
        value = match.group(2).strip().strip('"').strip("'")
        os.environ[key] = value
        loaded[key] = "***" if "PASSWORD" in key or "TOKEN" in key or "SECRET" in key else value
    return loaded


def latest_release_file(package_dir: Path) -> Path:
    candidates = sorted(
        package_dir.glob("*release*.yaml"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise SystemExit(f"No release YAML found in package: {package_dir}")
    return candidates[0]


def discover_contracts(package_dir: Path, release_file: Path) -> list[Path]:
    release = load_yaml(release_file)
    openmetadata = release.get("openmetadata") or {}
    names = openmetadata.get("contracts") or openmetadata.get("metadata_contracts") or []
    contracts: list[Path] = []
    for name in names:
        contract = (package_dir / str(name)).resolve()
        if not contract.exists():
            raise SystemExit(f"Metadata contract not found: {contract}")
        contracts.append(contract)
    retire = openmetadata.get("retire") or []
    if not contracts and not retire:
        raise SystemExit(f"Release file does not define openmetadata.contracts or openmetadata.retire: {release_file}")
    return contracts


def discover_retire_objects(release_file: Path) -> list[dict[str, str]]:
    release = load_yaml(release_file)
    openmetadata = release.get("openmetadata") or {}
    raw = openmetadata.get("retire") or []
    result: list[dict[str, str]] = []
    for item in raw:
        if isinstance(item, dict):
            fqn = str(item.get("fully_qualified_name", item.get("fqn", ""))).strip()
            reason = str(item.get("reason", "")).strip()
        else:
            fqn = str(item).strip()
            reason = ""
        if fqn:
            result.append({"fully_qualified_name": fqn, "reason": reason})
    return result


def run_contract(sync_script: Path, contract: Path, mode: str) -> dict[str, Any]:
    command = [
        sys.executable,
        str(sync_script),
        "--mode",
        mode,
        "--contract",
        str(contract),
    ]
    completed = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    parsed_stdout: Any = None
    if completed.stdout.strip():
        try:
            parsed_stdout = json.loads(completed.stdout)
        except json.JSONDecodeError:
            parsed_stdout = completed.stdout.strip()
    return {
        "contract": str(contract),
        "mode": mode,
        "returncode": completed.returncode,
        "ok": completed.returncode == 0,
        "stdout": parsed_stdout,
        "stderr": completed.stderr.strip(),
    }


def metadata_request(base_url: str, method: str, path: str, token: str, body: object | None = None) -> dict[str, Any] | None:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    request = urllib.request.Request(base_url.rstrip("/") + "/api/v1" + path, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed HTTP {exc.code}: {detail[:1000]}") from exc


def metadata_login(base_url: str, username: str, password: str) -> str:
    encoded = base64.b64encode(password.encode("utf-8")).decode("ascii")
    result = metadata_request(base_url, "POST", "/users/login", "", {"email": username, "password": encoded})
    if not result or not result.get("accessToken"):
        raise RuntimeError("OpenMetadata 登录未返回 accessToken")
    return str(result["accessToken"])


def retire_table(base_url: str, token: str, item: dict[str, str], mode: str) -> dict[str, Any]:
    fqn = item["fully_qualified_name"]
    encoded = urllib.parse.quote(fqn, safe="")
    current = metadata_request(base_url, "GET", f"/tables/name/{encoded}", token)
    if current is None:
        return {"fully_qualified_name": fqn, "mode": mode, "ok": True, "action": "already_absent", "reason": item.get("reason", "")}
    if mode == "plan":
        return {"fully_qualified_name": fqn, "mode": mode, "ok": True, "action": "planned_retire", "entity_id": current.get("id"), "reason": item.get("reason", "")}
    if mode == "apply":
        entity_id = str(current.get("id", "")).strip()
        if not entity_id:
            return {"fully_qualified_name": fqn, "mode": mode, "ok": False, "error": "OpenMetadata 表资产缺少 id"}
        deleted = metadata_request(base_url, "DELETE", f"/tables/{urllib.parse.quote(entity_id, safe='')}?hardDelete=true&recursive=true", token)
        return {"fully_qualified_name": fqn, "mode": mode, "ok": True, "action": "deleted", "entity_id": entity_id, "response": deleted or {}}
    verified = metadata_request(base_url, "GET", f"/tables/name/{encoded}", token)
    return {"fully_qualified_name": fqn, "mode": mode, "ok": verified is None, "action": "verified_absent" if verified is None else "still_present", "reason": item.get("reason", "")}


def run_retirement(items: list[dict[str, str]], mode: str) -> list[dict[str, Any]]:
    if not items:
        return []
    base_url = os.getenv("OPENMETADATA_BASE_URL", "http://127.0.0.1:8585")
    username = os.getenv("OPENMETADATA_USERNAME", "admin@open-metadata.org")
    password = os.getenv("OPENMETADATA_PASSWORD", "")
    if not password:
        raise RuntimeError("missing password environment variable: OPENMETADATA_PASSWORD")
    token = metadata_login(base_url, username, password)
    return [retire_table(base_url, token, item, mode) for item in items]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_PACKAGE_DIR)
    parser.add_argument("--release", type=Path)
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--sync-script", type=Path, default=DEFAULT_SYNC_SCRIPT)
    parser.add_argument("--mode", choices=("plan", "apply", "verify", "full"), default="plan")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    package_dir = args.package_dir.resolve()
    if args.release:
        release_file = args.release if args.release.is_absolute() else package_dir / args.release
        release_file = release_file.resolve()
    else:
        release_file = latest_release_file(package_dir)
    if not release_file.exists():
        raise SystemExit(f"Release file not found: {release_file}")
    if not args.sync_script.exists():
        raise SystemExit(f"OpenMetadata sync script not found: {args.sync_script}")

    env_summary = load_env_file(args.env_file)
    contracts = discover_contracts(package_dir, release_file)
    retire_objects = discover_retire_objects(release_file)
    mode_sequence = ["plan", "apply", "verify"] if args.mode == "full" else [args.mode]

    results: list[dict[str, Any]] = []
    blocked = False

    # A full sync is a release-wide transaction: every contract and every
    # retirement target must pass plan before any apply starts. This also
    # ensures `full` never reaches retire_table(), which only accepts the
    # explicit plan/apply/verify operations.
    for mode in mode_sequence:
        for contract in contracts:
            if blocked:
                results.append({
                    "contract": str(contract),
                    "mode": mode,
                    "returncode": None,
                    "ok": False,
                    "skipped": True,
                    "stderr": "Skipped after previous failure.",
                })
                continue
            result = run_contract(args.sync_script, contract, mode)
            results.append(result)
            if not result["ok"]:
                blocked = True

        if retire_objects:
            if blocked:
                results.extend({
                    "retire": item,
                    "mode": mode,
                    "returncode": None,
                    "ok": False,
                    "skipped": True,
                    "stderr": "Skipped after previous failure.",
                } for item in retire_objects)
                continue
            try:
                retire_results = run_retirement(retire_objects, mode)
            except Exception as exc:  # noqa: BLE001
                retire_results = [{"mode": mode, "ok": False, "error": str(exc)}]
            results.extend({"retire": item, "mode": mode, "returncode": 0 if item.get("ok") else 1, **item} for item in retire_results)
            if any(not item.get("ok") for item in retire_results):
                blocked = True

    report = {
        "ok": all(item.get("ok") for item in results),
        "run_time": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "package_dir": str(package_dir),
        "release_file": str(release_file),
        "mode": args.mode,
        "contract_count": len(contracts),
        "contracts": [str(item) for item in contracts],
        "retire_count": len(retire_objects),
        "retire_objects": retire_objects,
        "env_file": str(args.env_file.resolve()),
        "env_loaded_keys": sorted(env_summary.keys()),
        "results": results,
    }
    report_path = args.report
    if report_path is None:
        release_stem = release_file.stem
        report_path = package_dir / f"openmetadata-sync-report-{release_stem}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "ok": report["ok"],
        "release_file": str(release_file),
        "contract_count": len(contracts),
        "mode": args.mode,
        "report": str(report_path),
    }, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
