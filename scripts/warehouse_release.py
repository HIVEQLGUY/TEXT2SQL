#!/usr/bin/env python3
"""Run a deterministic ClickHouse warehouse release.

The release manifest is the only input that may cause a formal publish.  The
runner validates the complete artifact set, executes ClickHouse in phases,
syncs OpenMetadata through the project entry point, writes an audit report and
records the release in Git.  It deliberately does not keep versioned formal
tables in ClickHouse; candidate and previous objects are temporary publish
objects and are cleaned only after the postcheck succeeds.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OM_SYNC = PROJECT_ROOT / "scripts" / "sync_openmetadata_release.py"
DEFAULT_OM_ENV = PROJECT_ROOT / "local" / "credentials" / "openmetadata.env"
DEFAULT_CH_EXECUTOR = (
    Path.home()
    / ".codex"
    / "skills"
    / "data-warehouse-cleaning"
    / "scripts"
    / "execute_clickhouse_sql.py"
)
DEFAULT_CH_QUERY = (
    Path.home()
    / ".codex"
    / "skills"
    / "clickhouse-sql-dev"
    / "scripts"
    / "run_clickhouse_sql.py"
)
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.-]{2,127}$")
VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
MUTATING_SQL_PATTERN = re.compile(
    r"\b(?:CREATE|INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|RENAME|OPTIMIZE|SYSTEM)\b",
    re.IGNORECASE,
)
MAX_OUTPUT = 20000


class ReleaseError(RuntimeError):
    """A user-actionable release validation or execution error."""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise ReleaseError("当前 Python 环境缺少 PyYAML，无法读取发布文件") from exc
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            value = yaml.safe_load(handle)
    except OSError as exc:
        raise ReleaseError(f"无法读取发布文件: {path}") from exc
    if not isinstance(value, dict):
        raise ReleaseError(f"发布文件根节点必须是 YAML 对象: {path}")
    return value


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def now_local() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def short_output(value: str, limit: int = MAX_OUTPUT) -> str:
    value = value or ""
    if len(value) <= limit:
        return value
    return value[:limit] + f"\n...[输出已截断，原始长度 {len(value)} 字符]"


def scrub_output(value: str) -> str:
    """Remove common credential-shaped values before writing an audit report."""
    value = re.sub(r"(?i)(password|token|secret|cookie)=([^\s&]+)", r"\1=***", value)
    value = re.sub(r"(?i)(password|token|secret)\s*[:=]\s*[^,\s}]+", r"\1=***", value)
    return short_output(value)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def unique_preserving(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReleaseError(f"{label} 必须是 YAML 对象")
    return value


def relative_to(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise ReleaseError(f"文件必须位于允许的目录内: {path}") from exc


def resolve_package_file(package_dir: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ReleaseError(f"{label} 必须是非空文件路径")
    candidate = Path(value.strip())
    if not candidate.is_absolute():
        candidate = package_dir / candidate
    candidate = candidate.resolve()
    relative_to(package_dir, candidate)
    return candidate


def strip_sql_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    sql = re.sub(r"--[^\r\n]*", " ", sql)
    return sql


def sql_has_mutation(sql: str) -> bool:
    return bool(MUTATING_SQL_PATTERN.search(strip_sql_comments(sql)))


def sql_mentions_identifier(sql: str, name: str) -> bool:
    return bool(re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", sql))


def phase_path_map(raw: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    """Normalize new publish.phases and the previous execution shape."""
    publish = raw.get("publish")
    if isinstance(publish, dict):
        phases = publish.get("phases")
        if isinstance(phases, dict):
            return phases, False
        aliases = {
            "preflight": "preflight_sql",
            "build": "build_sql",
            "quality": "quality_sql",
            "swap": "swap_sql",
            "postcheck": "postcheck_sql",
            "rollback": "rollback_sql",
            "cleanup": "cleanup_sql",
        }
        result = {key: publish.get(alias) for key, alias in aliases.items() if publish.get(alias)}
        if result:
            return result, False
    execution = raw.get("execution")
    if isinstance(execution, dict):
        aliases = {
            "preflight": "preflight_sql_file",
            "build": "sql_file",
            "quality": "quality_file",
            "swap": "swap_sql_file",
            "postcheck": "postcheck_sql_file",
            "rollback": "rollback_sql_file",
            "cleanup": "cleanup_sql_file",
        }
        result = {key: execution.get(alias) for key, alias in aliases.items() if execution.get(alias)}
        return result, True
    return {}, False


@dataclass
class ReleaseContext:
    release_file: Path
    package_dir: Path
    raw: dict[str, Any]
    normalized: dict[str, Any]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    artifact_paths: list[Path] = field(default_factory=list)
    artifact_hashes: dict[str, str] = field(default_factory=dict)
    manifest_fingerprint: str = ""
    report_path: Path | None = None
    steps: list[dict[str, Any]] = field(default_factory=list)

    @property
    def release_id(self) -> str:
        return str(self.normalized["release_id"])

    @property
    def mode(self) -> str:
        return str(self.normalized.get("release_type", "formal"))

    def add_step(self, name: str, status: str, **details: Any) -> None:
        item = {"name": name, "status": status, "at": now_local()}
        item.update(details)
        self.steps.append(item)


def normalize_manifest(raw: dict[str, Any], release_file: Path, package_dir: Path) -> tuple[dict[str, Any], list[str]]:
    release_id = str(raw.get("release_id", "")).strip()
    raw_contract = raw.get("contract") if isinstance(raw.get("contract"), dict) else {}
    version = str(raw.get("version", raw_contract.get("version", ""))).strip()
    release_type = str(raw.get("release_type", "formal")).strip().lower()
    environment = str(raw.get("environment", raw.get("target_environment", ""))).strip().lower()
    source = raw.get("source") if isinstance(raw.get("source"), dict) else {}
    partitions = source.get("partitions", source.get("source_partitions", []))
    if not partitions and source.get("source_partition") not in (None, ""):
        partitions = [source.get("source_partition")]
    if not partitions and source.get("snapshot_partition") not in (None, ""):
        partitions = [source.get("snapshot_partition")]

    targets_raw = raw.get("targets", [])
    targets: list[dict[str, Any]] = []
    for item in as_list(targets_raw):
        target = require_mapping(item, "targets 中的目标")
        physical = str(target.get("physical_name", target.get("production_physical_name", ""))).strip()
        database = str(target.get("database", source.get("database", ""))).strip()
        production = str(target.get("production_physical_name", physical)).strip()
        candidate = str(target.get("candidate_physical_name", target.get("candidate_table", ""))).strip()
        previous = str(target.get("previous_physical_name", "")).strip()
        targets.append({
            "chinese_name": str(target.get("chinese_name", "")).strip(),
            "physical_name": physical,
            "production_physical_name": production,
            "candidate_physical_name": candidate,
            "previous_physical_name": previous,
            "database": database,
            "grain": str(target.get("grain", "")).strip(),
            "key": target.get("key", []),
        })

    phases, legacy = phase_path_map(raw)
    legacy = legacy or not bool(str(raw.get("release_api_version", "")).strip())
    openmetadata = raw.get("openmetadata") if isinstance(raw.get("openmetadata"), dict) else {}
    contracts = [str(item).strip() for item in as_list(openmetadata.get("contracts")) if str(item).strip()]
    contract = raw.get("contract") if isinstance(raw.get("contract"), dict) else {}
    artifact_section = raw.get("artifacts") if isinstance(raw.get("artifacts"), dict) else {}
    for key in ("cleaning_contract", "modeling_contract", "contract", "cleaning", "modeling"):
        value = artifact_section.get(key, contract.get(key) if isinstance(contract, dict) else None)
        if isinstance(value, str) and value.strip():
            artifact_section[key] = value.strip()
    metadata_contracts = artifact_section.get("metadata_contracts", [])
    if not metadata_contracts and isinstance(raw.get("execution"), dict):
        metadata_contracts = raw["execution"].get("metadata_contract_files", [])
    for item in as_list(metadata_contracts):
        if str(item).strip():
            contracts.append(str(item).strip())
    contracts = unique_preserving(contracts)

    approval = raw.get("approval") if isinstance(raw.get("approval"), dict) else {}
    git = raw.get("git") if isinstance(raw.get("git"), dict) else {}
    publish = raw.get("publish") if isinstance(raw.get("publish"), dict) else {}
    strategy = str(publish.get("strategy", "")).strip().lower()
    if not strategy and not legacy:
        strategy = "candidate_swap"
    if legacy:
        strategy = strategy or "legacy_direct"

    normalized = {
        "release_api_version": str(raw.get("release_api_version", "warehouse-release/v1")),
        "release_id": release_id,
        "version": version,
        "release_type": release_type,
        "environment": environment,
        "status": str(raw.get("status", "")).strip().lower(),
        "source": {
            "database": str(source.get("database", "")).strip(),
            "partitions": [str(item).strip() for item in as_list(partitions) if str(item).strip()],
            "chinese_name": str(source.get("chinese_name", "")).strip(),
            "physical_name": str(source.get("physical_name", "")).strip(),
        },
        "targets": targets,
        "publish": {
            "strategy": strategy,
            "temporary_tables": [str(item).strip() for item in as_list(publish.get("temporary_tables")) if str(item).strip()],
            "previous_table_names": [str(item).strip() for item in as_list(publish.get("previous_table_names")) if str(item).strip()],
            "cleanup_on_success": bool(publish.get("cleanup_on_success", True)),
            "keep_candidate_on_failure": bool(publish.get("keep_candidate_on_failure", True)),
            "phases": phases,
        },
        "openmetadata": {
            "contracts": contracts,
            "mode": str(openmetadata.get("mode", "full")).strip().lower(),
            "env_file": str(openmetadata.get("env_file", "")).strip(),
        },
        "approval": approval,
        "git": {
            "required": bool(git.get("required", release_type in {"formal", "corrective", "rollback"})),
            "auto_commit": bool(git.get("auto_commit", True)),
            "auto_push": bool(git.get("auto_push", release_type in {"formal", "corrective", "rollback"})),
            "remote": str(git.get("remote", "origin")).strip(),
            "branch": str(git.get("branch", "main")).strip(),
            "tag": str(git.get("tag", f"warehouse/{release_id}")).strip(),
            "include_paths": [str(item).strip() for item in as_list(git.get("include_paths")) if str(item).strip()],
            "executable": str(git.get("executable", "")).strip(),
        },
        "artifacts": artifact_section,
        "legacy_manifest": legacy,
    }
    return normalized, ["旧 execution 结构已兼容读取，正式新发布请使用 release_api_version + publish.phases"] if legacy else []


def validate_context(ctx: ReleaseContext, requested_mode: str) -> None:
    n = ctx.normalized
    legacy = bool(n.get("legacy_manifest"))
    legacy_read_only = legacy and requested_mode in {"plan", "verify"}
    if not ID_PATTERN.fullmatch(ctx.release_id):
        ctx.errors.append("release_id 必须是 3-128 位小写字母、数字、点、下划线或短横线")
    version = str(n.get("version", ""))
    if not VERSION_PATTERN.fullmatch(version):
        if legacy_read_only:
            ctx.warnings.append("旧发布文件未声明标准 version；仅允许只读审阅")
        else:
            ctx.errors.append("version 必须使用类似 1.3.0 的版本格式")
    if n.get("environment") not in {"test", "staging", "production"}:
        if legacy_read_only:
            ctx.warnings.append("旧发布文件未声明 environment；仅允许只读审阅")
        else:
            ctx.errors.append("environment 必须明确为 test、staging 或 production")
    if not n.get("source", {}).get("database"):
        if legacy_read_only:
            ctx.warnings.append("旧发布文件未声明 source.database；仅允许只读审阅")
        else:
            ctx.errors.append("source.database 未声明")
    if not n.get("source", {}).get("partitions"):
        if legacy_read_only:
            ctx.warnings.append("旧发布文件未声明 source.partitions；仅允许只读审阅")
        else:
            ctx.errors.append("source.partitions 未声明，不能确认本次发布输入快照")
    if not n.get("targets"):
        if legacy_read_only:
            ctx.warnings.append("旧发布文件未声明 targets；仅允许只读审阅")
        else:
            ctx.errors.append("targets 不能为空")

    production_names: set[str] = set()
    candidate_names: set[str] = set()
    for index, target in enumerate(n.get("targets", []), start=1):
        prefix = f"targets[{index}]"
        for key in ("physical_name", "production_physical_name", "candidate_physical_name"):
            value = str(target.get(key, ""))
            if key == "candidate_physical_name" and not value and requested_mode == "plan":
                ctx.warnings.append(f"{prefix}.{key} 未声明，正式候选切换会被阻断")
                continue
            if not value or not IDENTIFIER_PATTERN.fullmatch(value):
                ctx.errors.append(f"{prefix}.{key} 不是合法 ClickHouse 表名")
        production = str(target.get("production_physical_name", ""))
        candidate = str(target.get("candidate_physical_name", ""))
        if not target.get("database"):
            if not legacy_read_only:
                ctx.errors.append(f"{prefix}.database 未声明")
            else:
                ctx.warnings.append(f"{prefix}.database 未声明，旧发布仅允许只读审阅")
        if requested_mode in {"full", "finalize"} and n.get("release_type") != "shadow" and not target.get("previous_physical_name"):
            ctx.errors.append(f"{prefix}.previous_physical_name 未声明，无法定义切换后的回滚对象")
        if production in production_names:
            ctx.errors.append(f"目标生产表重复声明: {production}")
        production_names.add(production)
        if candidate:
            if candidate == production:
                ctx.errors.append(f"候选表不能与生产表同名: {production}")
            if candidate in candidate_names:
                ctx.errors.append(f"候选表重复声明: {candidate}")
            candidate_names.add(candidate)
        if not target.get("grain"):
            ctx.warnings.append(f"{prefix}.grain 未声明，元数据和发布审计不完整")

    phases = n.get("publish", {}).get("phases", {})
    phase_files: dict[str, Path] = {}
    for phase, value in phases.items():
        if value in (None, ""):
            continue
        if isinstance(value, list):
            ctx.errors.append(f"publish.phases.{phase} 只能登记一个固定 SQL 文件")
            continue
        try:
            path = resolve_package_file(ctx.package_dir, value, f"publish.phases.{phase}")
        except ReleaseError as exc:
            ctx.errors.append(str(exc))
            continue
        if not path.exists():
            ctx.errors.append(f"SQL 文件不存在: {relative_to(ctx.package_dir, path)}")
            continue
        phase_files[phase] = path

    repeated_paths: dict[str, list[str]] = {}
    for phase, path in phase_files.items():
        repeated_paths.setdefault(str(path), []).append(phase)
    for path, phases_for_path in repeated_paths.items():
        if len(phases_for_path) > 1:
            ctx.errors.append(f"同一个 SQL 文件被多个发布阶段重复使用: {path} -> {phases_for_path}")

    formal_modes = {"full", "rollback"}
    if requested_mode in formal_modes:
        required_phases = {"preflight", "build", "quality", "swap", "postcheck", "rollback", "cleanup"}
        missing = sorted(required_phases - set(phase_files))
        if n.get("release_type") != "shadow" and missing:
            ctx.errors.append(f"正式发布缺少固定阶段 SQL: {', '.join(missing)}")
        if n.get("publish", {}).get("strategy") != "candidate_swap" and n.get("release_type") != "shadow":
            ctx.errors.append("正式发布必须使用 publish.strategy=candidate_swap，禁止直接写生产表")
        approval = n.get("approval", {})
        if str(approval.get("status", "")).lower() not in {"approved", "active"}:
            ctx.errors.append("approval.status 必须是 approved 或 active")
        if not bool(approval.get("formal_publish_authorized", approval.get("formal_dwd_authorized", False))):
            ctx.errors.append("approval 未明确授权 formal_publish_authorized")
        if not bool(n.get("git", {}).get("required", False)):
            ctx.errors.append("正式发布必须设置 git.required=true")
        if not n.get("openmetadata", {}).get("contracts"):
            ctx.errors.append("正式发布必须登记 openmetadata.contracts")
        if not n.get("git", {}).get("auto_commit", False):
            ctx.errors.append("正式发布必须开启 git.auto_commit")
        if not n.get("git", {}).get("auto_push", False):
            ctx.errors.append("正式发布必须开启 git.auto_push")
        if not n.get("git", {}).get("remote"):
            ctx.errors.append("正式发布必须声明 git.remote")
        if not n.get("git", {}).get("branch"):
            ctx.errors.append("正式发布必须声明 git.branch")
    elif requested_mode == "verify":
        for phase in ("preflight", "postcheck"):
            if phase not in phase_files:
                ctx.warnings.append(f"verify 未提供 {phase} SQL")

    readonly_phases = {"preflight", "quality", "postcheck"}
    for phase, path in phase_files.items():
        try:
            sql = path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            ctx.errors.append(f"无法读取 SQL 文件: {path}: {exc}")
            continue
        if phase in readonly_phases and sql_has_mutation(sql):
            ctx.errors.append(f"{phase} 阶段必须只读，但检测到写入/DDL 关键字: {relative_to(ctx.package_dir, path)}")
        if phase == "build" and n.get("publish", {}).get("strategy") == "candidate_swap":
            if candidate_names and not any(sql_mentions_identifier(sql, name) for name in candidate_names):
                ctx.errors.append("build SQL 未出现任何候选表名，无法证明构建不会直写生产表")
            for production in production_names:
                if re.search(rf"\b(?:INSERT\s+INTO|DROP\s+TABLE|TRUNCATE\s+TABLE)\s+(?:IF\s+EXISTS\s+)?(?:[A-Za-z0-9_]+\.)?{re.escape(production)}\b", sql, re.IGNORECASE):
                    ctx.errors.append(f"build SQL 直接操作生产表: {production}")
        if phase == "cleanup":
            for production in production_names:
                if re.search(rf"\b(?:DROP\s+TABLE|TRUNCATE\s+TABLE)\s+(?:IF\s+EXISTS\s+)?(?:[A-Za-z0-9_]+\.)?{re.escape(production)}\b", sql, re.IGNORECASE):
                    ctx.errors.append(f"cleanup SQL 不得删除当前生产表: {production}")
        if phase in {"swap", "rollback"} and n.get("publish", {}).get("strategy") == "candidate_swap":
            required_names = production_names | candidate_names
            missing_names = sorted(name for name in required_names if not sql_mentions_identifier(sql, name))
            if missing_names:
                ctx.errors.append(f"{phase} SQL 未覆盖声明的生产/候选表: {', '.join(missing_names)}")

    contract_paths: list[Path] = []
    for name in n.get("openmetadata", {}).get("contracts", []):
        try:
            path = resolve_package_file(ctx.package_dir, name, "openmetadata.contracts")
        except ReleaseError as exc:
            ctx.errors.append(str(exc))
            continue
        if not path.exists():
            ctx.errors.append(f"OpenMetadata 契约不存在: {relative_to(ctx.package_dir, path)}")
            continue
        contract_paths.append(path)
    fqn_by_path: dict[str, str] = {}
    fqn_seen: dict[str, str] = {}
    for path in contract_paths:
        try:
            contract = load_yaml(path)
            fqn = str(contract.get("table", {}).get("fully_qualified_name", "")).strip()
            fqn_by_path[str(path)] = fqn
            if fqn and fqn in fqn_seen and fqn_seen[fqn] != str(path):
                ctx.errors.append(f"多个 OpenMetadata 契约指向同一表，可能发生顺序覆盖: {fqn}")
            if fqn:
                fqn_seen[fqn] = str(path)
        except (ReleaseError, OSError) as exc:
            ctx.errors.append(f"无法读取 OpenMetadata 契约 {path}: {exc}")

    ctx.artifact_paths = []
    for path in [ctx.release_file, *phase_files.values(), *contract_paths]:
        if path not in ctx.artifact_paths:
            ctx.artifact_paths.append(path)
    for key in ("cleaning_contract", "modeling_contract", "contract"):
        value = n.get("artifacts", {}).get(key)
        if isinstance(value, str) and value.strip():
            try:
                path = resolve_package_file(ctx.package_dir, value, f"artifacts.{key}")
                if not path.exists():
                    ctx.errors.append(f"发布契约文件不存在: {relative_to(ctx.package_dir, path)}")
                elif path not in ctx.artifact_paths:
                    ctx.artifact_paths.append(path)
            except ReleaseError as exc:
                ctx.errors.append(str(exc))

    include_paths = n.get("git", {}).get("include_paths", [])
    for name in include_paths:
        try:
            path = resolve_package_file(ctx.package_dir, name, "git.include_paths")
            if not path.exists():
                ctx.errors.append(f"Git 清单文件不存在: {relative_to(ctx.package_dir, path)}")
            elif path not in ctx.artifact_paths:
                ctx.artifact_paths.append(path)
        except ReleaseError as exc:
            ctx.errors.append(str(exc))

    if not ctx.errors:
        ctx.artifact_hashes = {
            relative_to(ctx.package_dir, path): sha256_file(path)
            for path in sorted(ctx.artifact_paths, key=lambda item: relative_to(ctx.package_dir, item))
        }
        digest = hashlib.sha256()
        for name, file_hash in ctx.artifact_hashes.items():
            digest.update(name.encode("utf-8"))
            digest.update(b"\0")
            digest.update(file_hash.encode("ascii"))
            digest.update(b"\n")
        ctx.manifest_fingerprint = digest.hexdigest()

    ctx.warnings.extend(ctx.normalized.get("legacy_manifest") and [
        "旧发布文件只允许用于 plan/verify；未显式声明候选表切换、清理和回滚门禁时不得 full"
    ] or [])


def report_base(ctx: ReleaseContext, requested_mode: str, status: str) -> dict[str, Any]:
    n = ctx.normalized
    return {
        "report_version": "warehouse-release-report/v1",
        "status": status,
        "release_id": ctx.release_id,
        "version": n.get("version"),
        "release_type": n.get("release_type"),
        "environment": n.get("environment"),
        "requested_mode": requested_mode,
        "started_at": now_local(),
        "package_dir": relative_to(PROJECT_ROOT, ctx.package_dir),
        "release_file": relative_to(PROJECT_ROOT, ctx.release_file),
        "source": n.get("source"),
        "targets": n.get("targets"),
        "manifest_fingerprint": ctx.manifest_fingerprint,
        "artifact_hashes": ctx.artifact_hashes,
        "warnings": ctx.warnings,
        "validation_errors": ctx.errors,
        "steps": ctx.steps,
        "git": {
            "required": n.get("git", {}).get("required"),
            "auto_push": n.get("git", {}).get("auto_push"),
            "remote": n.get("git", {}).get("remote"),
            "branch": n.get("git", {}).get("branch"),
            "tag": n.get("git", {}).get("tag"),
        },
    }


def run_command(
    label: str,
    command: list[str],
    cwd: Path,
    timeout: int = 180,
    env_overrides: dict[str, str] | None = None,
) -> dict[str, Any]:
    safe_command = [str(item) for item in command]
    environment = os.environ.copy()
    if env_overrides:
        environment.update(env_overrides)
    try:
        completed = subprocess.run(
            safe_command,
            cwd=str(cwd),
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        return {"label": label, "ok": False, "returncode": None, "error": f"命令不存在: {safe_command[0]}", "exception": str(exc)}
    except subprocess.TimeoutExpired as exc:
        return {"label": label, "ok": False, "returncode": None, "error": f"执行超时({timeout}s)", "stdout": scrub_output(str(exc.stdout or "")), "stderr": scrub_output(str(exc.stderr or ""))}
    return {
        "label": label,
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": scrub_output(completed.stdout),
        "stderr": scrub_output(completed.stderr),
        "command": safe_command,
    }


def clickhouse_config(ctx: ReleaseContext) -> tuple[str, str]:
    config = ctx.raw.get("clickhouse") if isinstance(ctx.raw.get("clickhouse"), dict) else {}
    base_url = str(
        config.get("base_url")
        or os.getenv("CLICKHOUSE_BASE_URL")
        or "http://127.0.0.1:8123"
    ).strip()
    database = str(
        config.get("database")
        or ctx.normalized.get("source", {}).get("database")
        or os.getenv("CLICKHOUSE_DATABASE")
        or "youmei_sandbox"
    ).strip()
    return base_url, database


def execute_clickhouse_phase(ctx: ReleaseContext, phase: str, path: Path, executor: Path) -> dict[str, Any]:
    base_url, database = clickhouse_config(ctx)
    command = [
        sys.executable,
        str(executor),
        "--sql-file",
        str(path),
        "--base-url",
        base_url,
        "--database",
        database,
        "--print-results",
    ]
    return run_command(f"clickhouse:{phase}", command, PROJECT_ROOT)


def execute_clickhouse_health(ctx: ReleaseContext, query_runner: Path) -> dict[str, Any]:
    base_url, database = clickhouse_config(ctx)
    parsed = re.match(r"^https?://([^:/]+)(?::([0-9]+))?", base_url)
    if not parsed:
        return {"label": "clickhouse:health", "ok": False, "returncode": None, "error": f"无法解析 ClickHouse base_url: {base_url}"}
    host = parsed.group(1)
    port = parsed.group(2) or ("443" if base_url.startswith("https://") else "8123")
    command = [
        sys.executable,
        str(query_runner),
        "--host",
        host,
        "--port",
        port,
        "--database",
        database,
        "--query",
        "SELECT currentDatabase() AS database, version() AS version",
        "--format",
        "JSONEachRow",
    ]
    return run_command("clickhouse:health", command, PROJECT_ROOT, timeout=60)


def resolve_git(ctx: ReleaseContext, cli_value: str | None) -> str | None:
    configured = cli_value or str(ctx.normalized.get("git", {}).get("executable", "")).strip()
    candidates = [configured] if configured else []
    which = shutil.which("git")
    if which:
        candidates.append(which)
    candidates.extend([
        Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "native" / "git" / "cmd" / "git.exe",
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files\Git\bin\git.exe",
    ])
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def git_command(git: str, args: list[str]) -> list[str]:
    return [git, *args]


def git_runtime_environment(git: str) -> dict[str, str]:
    """Make bundled Git helpers available to all release subprocesses."""
    git_path = Path(git).resolve()
    runtime_root: Path | None = None
    for candidate in [git_path.parent, *git_path.parents]:
        if (candidate / "mingw64" / "bin" / "git-remote-https.exe").exists():
            runtime_root = candidate
            break
    if runtime_root is None:
        return {}

    path_entries = [
        runtime_root / "cmd",
        runtime_root / "mingw64" / "bin",
        runtime_root / "usr" / "bin",
    ]
    current_path = os.environ.get("PATH", "")
    merged_path = [str(path) for path in path_entries if path.exists()]
    if current_path:
        merged_path.append(current_path)
    environment = {"PATH": os.pathsep.join(merged_path)}

    bundled_receive_pack = runtime_root / "mingw64" / "bin" / "git-receive-pack.exe"
    default_receive_pack = runtime_root / "mingw64" / "libexec" / "git-core" / "git-receive-pack.exe"
    if bundled_receive_pack.exists() and not default_receive_pack.exists():
        environment["GIT_EXEC_PATH"] = str(runtime_root / "mingw64" / "bin")
    return environment


def run_git_command(
    label: str,
    git: str,
    args: list[str],
    cwd: Path,
    timeout: int = 180,
) -> dict[str, Any]:
    return run_command(
        label,
        git_command(git, args),
        cwd,
        timeout=timeout,
        env_overrides=git_runtime_environment(git),
    )


def git_preflight(ctx: ReleaseContext, git: str | None) -> dict[str, Any]:
    if not git:
        return {"ok": False, "error": "找不到 Git 可执行文件；正式发布必须先恢复 Git 可用性"}
    root_result = run_git_command("git:repo-root", git, ["rev-parse", "--show-toplevel"], PROJECT_ROOT, timeout=30)
    if not root_result.get("ok"):
        return {"ok": False, "git": git, "root_result": root_result, "error": "当前项目不是可用的 Git 工作树"}
    repo_root = Path(str(root_result.get("stdout", "")).strip()).resolve()
    try:
        relative_to(repo_root, ctx.package_dir)
        relative_to(repo_root, PROJECT_ROOT)
    except ReleaseError as exc:
        return {"ok": False, "git": git, "error": str(exc)}
    status_result = run_git_command("git:status", git, ["status", "--porcelain=v1"], repo_root, timeout=30)
    cached_result = run_git_command("git:cached-status", git, ["diff", "--cached", "--name-only"], repo_root, timeout=30)
    if not status_result.get("ok") or not cached_result.get("ok"):
        return {"ok": False, "git": git, "error": "无法读取 Git 工作区状态", "status": status_result, "cached": cached_result}
    cached = [line.strip() for line in str(cached_result.get("stdout", "")).splitlines() if line.strip()]
    if cached:
        return {"ok": False, "git": git, "repo_root": str(repo_root), "error": "Git 暂存区已有未归属本次发布的变更，请先处理", "cached_paths": cached}
    return {"ok": True, "git": git, "repo_root": str(repo_root), "worktree_status": str(status_result.get("stdout", ""))}


def git_allowed_paths(ctx: ReleaseContext, report_path: Path, metadata_report: Path | None = None) -> list[Path]:
    paths = list(ctx.artifact_paths) + [report_path]
    if metadata_report and metadata_report.exists():
        paths.append(metadata_report)
    result: list[Path] = []
    for path in paths:
        if path not in result:
            result.append(path)
    return result


def git_stage_commit(ctx: ReleaseContext, git_info: dict[str, Any], paths: list[Path], message: str) -> dict[str, Any]:
    git = git_info.get("git")
    repo_root = Path(git_info.get("repo_root", PROJECT_ROOT))
    relative_paths: list[str] = []
    for path in paths:
        try:
            relative_paths.append(relative_to(repo_root, path))
        except ReleaseError as exc:
            return {"ok": False, "error": str(exc)}
    add = run_git_command("git:add", git, ["add", "--", *relative_paths], repo_root, timeout=30)
    if not add.get("ok"):
        return {"ok": False, "add": add, "error": "Git stage 失败"}
    cached = run_git_command("git:cached-paths", git, ["diff", "--cached", "--name-only"], repo_root, timeout=30)
    if not cached.get("ok"):
        return {"ok": False, "cached": cached, "error": "无法读取 Git 暂存区"}
    allowed = set(relative_paths)
    actual = {line.strip() for line in str(cached.get("stdout", "")).splitlines() if line.strip()}
    unexpected = sorted(actual - allowed)
    if unexpected:
        return {"ok": False, "unexpected_staged_paths": unexpected, "error": "发布器发现非本次发布文件进入暂存区，已阻断提交"}
    if not actual:
        return {"ok": True, "no_changes": True, "message": "没有需要提交的新内容"}
    commit = run_git_command("git:commit", git, ["commit", "-m", message], repo_root, timeout=60)
    if not commit.get("ok"):
        return {"ok": False, "commit": commit, "error": "Git commit 失败"}
    head = run_git_command("git:head", git, ["rev-parse", "HEAD"], repo_root, timeout=30)
    return {"ok": True, "commit": commit, "head": str(head.get("stdout", "")).strip()}


def git_push(ctx: ReleaseContext, git_info: dict[str, Any], *, follow_tags: bool = False) -> dict[str, Any]:
    git = git_info.get("git")
    repo_root = Path(git_info.get("repo_root", PROJECT_ROOT))
    git_config = ctx.normalized.get("git", {})
    if not bool(git_config.get("auto_push", False)):
        return {"ok": True, "skipped": True, "reason": "git.auto_push=false"}

    remote = str(git_config.get("remote", "")).strip()
    branch = str(git_config.get("branch", "")).strip()
    if not remote or not branch:
        return {"ok": False, "error": "Git 推送缺少 git.remote 或 git.branch"}

    current = run_git_command(
        "git:current-branch",
        git,
        ["symbolic-ref", "--quiet", "--short", "HEAD"],
        repo_root,
        timeout=30,
    )
    current_branch = str(current.get("stdout", "")).strip()
    if not current.get("ok") or current_branch != branch:
        return {
            "ok": False,
            "error": f"当前分支 `{current_branch or 'detached'}` 与发布分支 `{branch}` 不一致，已阻断推送",
            "current_branch": current_branch,
            "expected_branch": branch,
        }

    args = ["push", "--porcelain"]
    if follow_tags:
        args.append("--follow-tags")
    args.extend([remote, f"HEAD:{branch}"])
    pushed = run_git_command("git:push", git, args, repo_root, timeout=120)
    return {
        "ok": pushed.get("ok", False),
        "remote": remote,
        "branch": branch,
        "follow_tags": follow_tags,
        "result": pushed,
        "error": None if pushed.get("ok") else "Git 远程推送失败，需修复远程状态后运行 finalize",
    }


def git_tag(ctx: ReleaseContext, git_info: dict[str, Any]) -> dict[str, Any]:
    tag = str(ctx.normalized.get("git", {}).get("tag", "")).strip()
    if not tag:
        return {"ok": True, "skipped": True, "reason": "未配置 Git 标签"}
    git = git_info.get("git")
    repo_root = Path(git_info.get("repo_root", PROJECT_ROOT))
    existing = run_git_command("git:tag-resolve", git, ["rev-parse", "--verify", f"refs/tags/{tag}"], repo_root, timeout=30)
    head = run_git_command("git:head", git, ["rev-parse", "HEAD"], repo_root, timeout=30)
    head_value = str(head.get("stdout", "")).strip()
    if existing.get("ok"):
        existing_value = str(existing.get("stdout", "")).strip()
        if existing_value == head_value:
            return {"ok": True, "tag": tag, "already_exists": True, "commit": head_value}
        return {"ok": False, "tag": tag, "error": "同名 Git 标签已指向其他提交，禁止覆盖"}
    created = run_git_command("git:tag", git, ["tag", "-a", tag, "-m", f"warehouse release {ctx.release_id}"], repo_root, timeout=30)
    return {"ok": created.get("ok", False), "tag": tag, "create": created, "commit": head_value}


def metadata_report_path(ctx: ReleaseContext) -> Path:
    return ctx.package_dir / f"openmetadata-sync-report-{ctx.release_file.stem}.json"


def run_openmetadata(ctx: ReleaseContext, sync_script: Path, mode: str) -> dict[str, Any]:
    env_file_value = str(ctx.normalized.get("openmetadata", {}).get("env_file", "")).strip()
    env_file = resolve_package_file(ctx.package_dir, env_file_value, "openmetadata.env_file") if env_file_value else DEFAULT_OM_ENV
    report_path = metadata_report_path(ctx)
    command = [
        sys.executable,
        str(sync_script),
        "--package-dir",
        str(ctx.package_dir),
        "--release",
        str(ctx.release_file),
        "--env-file",
        str(env_file),
        "--mode",
        mode,
        "--report",
        str(report_path),
    ]
    result = run_command(f"openmetadata:{mode}", command, PROJECT_ROOT, timeout=300)
    result["report_path"] = str(report_path)
    return result


def write_release_report(ctx: ReleaseContext, requested_mode: str, status: str, extra: dict[str, Any] | None = None) -> Path:
    if ctx.report_path is None:
        stem = f"release-plan-{ctx.release_id}.json" if requested_mode == "plan" else f"release-report-{ctx.release_id}.json"
        ctx.report_path = ctx.package_dir / stem
    report = report_base(ctx, requested_mode, status)
    if extra:
        report.update(extra)
    report["finished_at"] = now_local()
    write_json_atomic(ctx.report_path, report)
    return ctx.report_path


def existing_report(ctx: ReleaseContext) -> dict[str, Any] | None:
    path = ctx.package_dir / f"release-report-{ctx.release_id}.json"
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


@contextmanager
def release_lock(ctx: ReleaseContext):
    """Prevent two agents/processes from publishing the same release at once."""
    lock_path = ctx.package_dir / f".warehouse-release-{ctx.release_id}.lock"
    handle = lock_path.open("a+", encoding="utf-8")
    try:
        if os.name == "nt":
            import msvcrt

            if handle.tell() == 0:
                handle.write("0")
                handle.flush()
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise ReleaseError(f"相同发布正在运行，无法取得发布锁: {lock_path}") from exc
        else:
            import fcntl

            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise ReleaseError(f"相同发布正在运行，无法取得发布锁: {lock_path}") from exc
        yield
    finally:
        try:
            if os.name == "nt":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            handle.close()
            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                # A concurrent process may still hold the path briefly on Windows.
                # The release result remains valid; the next run can remove it.
                pass


def phase_paths(ctx: ReleaseContext) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for phase, value in ctx.normalized.get("publish", {}).get("phases", {}).items():
        if value:
            result[phase] = resolve_package_file(ctx.package_dir, value, f"publish.phases.{phase}")
    return result


def run_plan(ctx: ReleaseContext, requested_mode: str, git_executable: str | None) -> int:
    git = resolve_git(ctx, git_executable)
    git_info = git_preflight(ctx, git) if git else {
        "ok": False,
        "error": "找不到 Git 可执行文件；正式发布必须先恢复 Git 可用性",
    }
    if not git_info.get("ok") and ctx.normalized.get("git", {}).get("required", False):
        ctx.errors.append(str(git_info.get("error", "Git 预检失败")))
    ctx.add_step("validation", "passed" if not ctx.errors else "blocked", error_count=len(ctx.errors))
    ctx.add_step(
        "git_preflight",
        "passed" if git_info.get("ok") else "blocked",
        checked_only=True,
        result=git_info,
    )
    ctx.add_step("clickhouse", "planned", phases=list(phase_paths(ctx)))
    ctx.add_step("openmetadata", "planned", contracts=ctx.normalized.get("openmetadata", {}).get("contracts", []))
    report_path = write_release_report(ctx, requested_mode, "planned")
    print(json.dumps({
        "ok": not ctx.errors,
        "status": "planned" if not ctx.errors else "blocked",
        "release_id": ctx.release_id,
        "manifest_fingerprint": ctx.manifest_fingerprint,
        "report": str(report_path),
        "warnings": ctx.warnings,
        "errors": ctx.errors,
    }, ensure_ascii=False, indent=2))
    return 0 if not ctx.errors else 2


def run_verify(ctx: ReleaseContext, query_runner: Path, executor: Path, sync_script: Path) -> int:
    if ctx.errors:
        write_release_report(ctx, "verify", "blocked")
        return 2
    health = execute_clickhouse_health(ctx, query_runner)
    ctx.add_step("clickhouse_health", "passed" if health.get("ok") else "failed", result=health)
    phases = phase_paths(ctx)
    for phase in ("preflight", "postcheck"):
        if phase in phases:
            result = execute_clickhouse_phase(ctx, phase, phases[phase], executor)
            ctx.add_step(f"clickhouse_{phase}", "passed" if result.get("ok") else "failed", result=result)
            if not result.get("ok"):
                write_release_report(ctx, "verify", "failed")
                return 1
    metadata = None
    if ctx.normalized.get("openmetadata", {}).get("contracts"):
        metadata = run_openmetadata(ctx, sync_script, "verify")
        ctx.add_step("openmetadata_verify", "passed" if metadata.get("ok") else "failed", result=metadata)
    status = "verified" if health.get("ok") and (metadata is None or metadata.get("ok")) else "failed"
    write_release_report(ctx, "verify", status)
    return 0 if status == "verified" else 1


def git_prepare(ctx: ReleaseContext, git_executable: str | None, report_path: Path) -> tuple[dict[str, Any], dict[str, Any] | None]:
    git = resolve_git(ctx, git_executable)
    info = git_preflight(ctx, git)
    ctx.add_step("git_preflight", "passed" if info.get("ok") else "blocked", result=info)
    if not info.get("ok"):
        return info, None
    prepared = git_stage_commit(
        ctx,
        info,
        git_allowed_paths(ctx, report_path),
        f"warehouse release {ctx.release_id} prepare",
    )
    ctx.add_step("git_prepare_commit", "passed" if prepared.get("ok") else "failed", result=prepared)
    if prepared.get("ok"):
        pushed = git_push(ctx, info)
        prepared["push"] = pushed
        ctx.add_step("git_prepare_push", "passed" if pushed.get("ok") else "failed", result=pushed)
        if not pushed.get("ok"):
            prepared["ok"] = False
            prepared["error"] = "Git 预提交已完成，但远程推送失败"
    return info, prepared


def run_full(ctx: ReleaseContext, query_runner: Path, executor: Path, sync_script: Path, git_executable: str | None, rerun: bool) -> int:
    old_report = existing_report(ctx)
    if old_report and old_report.get("manifest_fingerprint") == ctx.manifest_fingerprint and old_report.get("status") == "succeeded" and not rerun:
        ctx.add_step("idempotency", "no_op", reason="相同发布指纹已成功发布")
        report_path = write_release_report(ctx, "full", "succeeded", {"idempotent_reuse": True, "previous_report": old_report})
        print(json.dumps({"ok": True, "status": "succeeded", "idempotent_reuse": True, "report": str(report_path)}, ensure_ascii=False, indent=2))
        return 0
    if old_report and old_report.get("manifest_fingerprint") and old_report.get("manifest_fingerprint") != ctx.manifest_fingerprint:
        ctx.errors.append("同一 release_id 已存在不同发布指纹，必须使用新的 release_id")
    if ctx.errors:
        report_path = write_release_report(ctx, "full", "blocked")
        print(json.dumps({"ok": False, "status": "blocked", "report": str(report_path), "errors": ctx.errors}, ensure_ascii=False, indent=2))
        return 2

    report_path = ctx.package_dir / f"release-report-{ctx.release_id}.json"
    ctx.report_path = report_path
    write_release_report(ctx, "full", "prepared")
    git_info, prepared = git_prepare(ctx, git_executable, report_path)
    if not prepared or not prepared.get("ok"):
        write_release_report(ctx, "full", "blocked", {"failure_reason": "Git 预提交失败"})
        return 2

    health = execute_clickhouse_health(ctx, query_runner)
    ctx.add_step("clickhouse_health", "passed" if health.get("ok") else "failed", result=health)
    if not health.get("ok"):
        write_release_report(ctx, "full", "failed", {"failure_reason": "ClickHouse 健康检查失败"})
        finalize_failure = git_stage_commit(ctx, git_info, [report_path], f"warehouse release {ctx.release_id} failed")
        ctx.add_step("git_failure_report", "passed" if finalize_failure.get("ok") else "failed", result=finalize_failure)
        return 1

    phases = phase_paths(ctx)
    swapped = False
    failure_reason = ""
    rollback_result: dict[str, Any] | None = None
    try:
        for phase in ("preflight", "build", "quality"):
            result = execute_clickhouse_phase(ctx, phase, phases[phase], executor)
            ctx.add_step(f"clickhouse_{phase}", "passed" if result.get("ok") else "failed", result=result)
            if not result.get("ok"):
                raise ReleaseError(f"ClickHouse {phase} 阶段失败")
        result = execute_clickhouse_phase(ctx, "swap", phases["swap"], executor)
        ctx.add_step("clickhouse_swap", "passed" if result.get("ok") else "failed", result=result)
        if not result.get("ok"):
            raise ReleaseError("ClickHouse swap 阶段失败")
        swapped = True
        result = execute_clickhouse_phase(ctx, "postcheck", phases["postcheck"], executor)
        ctx.add_step("clickhouse_postcheck", "passed" if result.get("ok") else "failed", result=result)
        if not result.get("ok"):
            raise ReleaseError("ClickHouse postcheck 质量门禁失败")

        metadata = run_openmetadata(ctx, sync_script, "full")
        ctx.add_step("openmetadata_full", "passed" if metadata.get("ok") else "failed", result=metadata)
        if not metadata.get("ok"):
            raise ReleaseError("OpenMetadata plan/apply/verify 未全部通过")

        result = execute_clickhouse_phase(ctx, "cleanup", phases["cleanup"], executor)
        ctx.add_step("clickhouse_cleanup", "passed" if result.get("ok") else "failed", result=result)
        if not result.get("ok"):
            failure_reason = "正式表已切换，但临时对象清理失败，需要人工清理"
            status = "cleanup_pending"
        else:
            status = "succeeded"
    except (ReleaseError, KeyError) as exc:
        failure_reason = str(exc)
        status = "failed"
        if swapped:
            rollback_result = execute_clickhouse_phase(ctx, "rollback", phases["rollback"], executor)
            ctx.add_step("clickhouse_rollback", "passed" if rollback_result.get("ok") else "failed", result=rollback_result)
            status = "failed_rolled_back" if rollback_result.get("ok") else "rollback_failed"

    extra: dict[str, Any] = {"failure_reason": failure_reason} if failure_reason else {}
    if rollback_result is not None:
        extra["rollback"] = rollback_result
    write_release_report(ctx, "full", status, extra)
    final_paths = [report_path]
    metadata_report = metadata_report_path(ctx)
    if metadata_report.exists():
        final_paths.append(metadata_report)
    final_git = git_stage_commit(ctx, git_info, final_paths, f"warehouse release {ctx.release_id} {status}")
    ctx.add_step("git_finalize_commit", "passed" if final_git.get("ok") else "failed", result=final_git)
    tag: dict[str, Any] | None = None
    if final_git.get("ok") and status == "succeeded":
        tag = git_tag(ctx, git_info)
        ctx.add_step("git_tag", "passed" if tag.get("ok") else "failed", result=tag)
        if not tag.get("ok"):
            status = "version_record_pending"
            failure_reason = "生产表和元数据已完成，但 Git 标签未成功创建"
            write_release_report(ctx, "full", status, {"failure_reason": failure_reason, "tag_result": tag})
    if final_git.get("ok"):
        pushed = git_push(ctx, git_info, follow_tags=bool(tag and tag.get("ok")))
        ctx.add_step("git_finalize_push", "passed" if pushed.get("ok") else "failed", result=pushed)
        if not pushed.get("ok"):
            status = "version_record_pending"
            failure_reason = "平台结果和本地 Git 留痕已产生，但远程 Git 推送失败，需要运行 finalize"
            write_release_report(ctx, "full", status, {"failure_reason": failure_reason, "push_result": pushed})
    else:
        status = "version_record_pending"
        failure_reason = "平台执行结果已产生，但 Git 最终留痕失败，需要运行 finalize"
        write_release_report(ctx, "full", status, {"failure_reason": failure_reason})

    print(json.dumps({
        "ok": status == "succeeded",
        "status": status,
        "release_id": ctx.release_id,
        "report": str(report_path),
        "failure_reason": failure_reason,
    }, ensure_ascii=False, indent=2))
    return 0 if status == "succeeded" else 1


def run_finalize(ctx: ReleaseContext, git_executable: str | None) -> int:
    report = existing_report(ctx)
    if not report:
        raise ReleaseError("找不到可 finalize 的 release-report 文件")
    if report.get("manifest_fingerprint") != ctx.manifest_fingerprint:
        raise ReleaseError("发布报告与当前发布文件指纹不一致，禁止 finalize")
    if report.get("status") not in {"succeeded", "cleanup_pending", "version_record_pending"}:
        raise ReleaseError(f"当前报告状态不允许 finalize: {report.get('status')}")
    ctx.report_path = ctx.package_dir / f"release-report-{ctx.release_id}.json"
    git = resolve_git(ctx, git_executable)
    info = git_preflight(ctx, git)
    if not info.get("ok"):
        raise ReleaseError(str(info.get("error", "Git preflight failed")))
    paths = [ctx.report_path, metadata_report_path(ctx)]
    result = git_stage_commit(ctx, info, [path for path in paths if path.exists()], f"warehouse release {ctx.release_id} finalize")
    if not result.get("ok"):
        raise ReleaseError(str(result.get("error", "Git finalize failed")))
    tag: dict[str, Any] | None = None
    if report.get("status") != "cleanup_pending":
        tag = git_tag(ctx, info)
        if not tag.get("ok"):
            raise ReleaseError(str(tag.get("error", "Git tag failed")))
    pushed = git_push(ctx, info, follow_tags=bool(tag and tag.get("ok")))
    if not pushed.get("ok"):
        raise ReleaseError(str(pushed.get("error", "Git push failed")))
    if report.get("status") == "cleanup_pending":
        print(json.dumps({"ok": False, "status": "cleanup_pending", "report": str(ctx.report_path), "push": pushed, "message": "已补记报告并推送，但清理门禁仍未完成，暂不创建正式发布标签"}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True, "status": "finalized", "report": str(ctx.report_path), "tag": tag}, ensure_ascii=False, indent=2))
    return 0


def build_context(release_file: Path) -> ReleaseContext:
    release_file = release_file.resolve()
    if not release_file.exists():
        raise ReleaseError(f"发布文件不存在: {release_file}")
    package_dir = release_file.parent.resolve()
    raw = load_yaml(release_file)
    normalized, warnings = normalize_manifest(raw, release_file, package_dir)
    ctx = ReleaseContext(release_file, package_dir, raw, normalized, warnings=warnings)
    return ctx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="显式发布 ClickHouse 数仓版本包")
    parser.add_argument("--release", type=Path, required=True, help="发布 YAML 路径")
    parser.add_argument("--mode", choices=("plan", "verify", "full", "finalize"), default="plan")
    parser.add_argument("--git-executable", help="Git 可执行文件路径；默认自动发现")
    parser.add_argument("--clickhouse-executor", type=Path, default=DEFAULT_CH_EXECUTOR)
    parser.add_argument("--clickhouse-query", type=Path, default=DEFAULT_CH_QUERY)
    parser.add_argument("--openmetadata-sync", type=Path, default=DEFAULT_OM_SYNC)
    parser.add_argument("--rerun", action="store_true", help="允许相同成功指纹重新执行；候选对象仍须符合清理门禁")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        ctx = build_context(args.release)
        validate_context(ctx, args.mode)
        if args.mode == "plan":
            return run_plan(ctx, args.mode, args.git_executable)
        if args.mode == "verify":
            if not args.clickhouse_executor.resolve().exists():
                raise ReleaseError(f"ClickHouse 执行器不存在: {args.clickhouse_executor}")
            return run_verify(ctx, args.clickhouse_query.resolve(), args.clickhouse_executor.resolve(), args.openmetadata_sync.resolve())
        if args.mode == "finalize":
            with release_lock(ctx):
                return run_finalize(ctx, args.git_executable)
        if not args.clickhouse_executor.resolve().exists():
            raise ReleaseError(f"ClickHouse 执行器不存在: {args.clickhouse_executor}")
        if not args.clickhouse_query.resolve().exists():
            raise ReleaseError(f"ClickHouse 查询器不存在: {args.clickhouse_query}")
        if not args.openmetadata_sync.resolve().exists():
            raise ReleaseError(f"OpenMetadata 同步入口不存在: {args.openmetadata_sync}")
        with release_lock(ctx):
            return run_full(
                ctx,
                args.clickhouse_query.resolve(),
                args.clickhouse_executor.resolve(),
                args.openmetadata_sync.resolve(),
                args.git_executable,
                args.rerun,
            )
    except ReleaseError as exc:
        print(json.dumps({"ok": False, "status": "blocked", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
