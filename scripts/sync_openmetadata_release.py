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
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKAGE_DIR = PROJECT_ROOT / "config" / "warehouse_cleaning" / "doudian_order_item_v1"
DEFAULT_ENV_FILE = PROJECT_ROOT / "local" / "credentials" / "openmetadata.env"
DEFAULT_SYNC_SCRIPT = (
    Path.home()
    / ".codex"
    / "skills"
    / "data-warehouse-cleaning"
    / "scripts"
    / "sync_openmetadata_metadata.py"
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
    if not names:
        raise SystemExit(f"Release file does not define openmetadata.contracts: {release_file}")
    contracts: list[Path] = []
    for name in names:
        contract = (package_dir / str(name)).resolve()
        if not contract.exists():
            raise SystemExit(f"Metadata contract not found: {contract}")
        contracts.append(contract)
    return contracts


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
    mode_sequence = ["plan", "apply", "verify"] if args.mode == "full" else [args.mode]

    results: list[dict[str, Any]] = []
    blocked = False
    for contract in contracts:
        for mode in mode_sequence:
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

    report = {
        "ok": all(item.get("ok") for item in results),
        "run_time": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "package_dir": str(package_dir),
        "release_file": str(release_file),
        "mode": args.mode,
        "contract_count": len(contracts),
        "contracts": [str(item) for item in contracts],
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
