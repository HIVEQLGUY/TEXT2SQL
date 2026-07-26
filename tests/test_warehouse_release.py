from __future__ import annotations

import os
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.warehouse_release import (  # noqa: E402
    build_context,
    clickhouse_config,
    git_push,
    git_runtime_environment,
    release_lock,
    run_cleanup_full,
    run_verify,
    run_finalize,
    run_full,
    validate_context,
)


GIT_EXECUTABLE = shutil.which("git") or str(
    Path.home()
    / ".cache"
    / "codex-runtimes"
    / "codex-primary-runtime"
    / "dependencies"
    / "native"
    / "git"
    / "cmd"
    / "git.exe"
)


def run_git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        [GIT_EXECUTABLE, *args],
        cwd=str(cwd),
        env={**os.environ, **git_runtime_environment(GIT_EXECUTABLE)},
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


PHASE_SQL = {
    "preflight": "SELECT currentDatabase();",
    "build": "CREATE TABLE youmei_sandbox.dwd_demo__candidate__1_0_0 (id UInt64) ENGINE = MergeTree ORDER BY id; INSERT INTO youmei_sandbox.dwd_demo__candidate__1_0_0 SELECT number FROM numbers(1);",
    "quality": "SELECT throwIf((SELECT count() FROM youmei_sandbox.dwd_demo__candidate__1_0_0) = 0, 'empty');",
    "swap": "RENAME TABLE youmei_sandbox.dwd_demo TO youmei_sandbox.dwd_demo__previous__1_0_0, youmei_sandbox.dwd_demo__candidate__1_0_0 TO youmei_sandbox.dwd_demo;",
    "postcheck": "SELECT count() FROM youmei_sandbox.dwd_demo;",
    "rollback": "RENAME TABLE youmei_sandbox.dwd_demo TO youmei_sandbox.dwd_demo__candidate__1_0_0, youmei_sandbox.dwd_demo__previous__1_0_0 TO youmei_sandbox.dwd_demo;",
    "cleanup": "DROP TABLE IF EXISTS youmei_sandbox.dwd_demo__candidate__1_0_0; DROP TABLE IF EXISTS youmei_sandbox.dwd_demo__previous__1_0_0;",
}


def create_package(root: Path, *, duplicate_phase: bool = False, direct_production_write: bool = False, readonly_mutation: bool = False) -> Path:
    package = root / "release"
    package.mkdir()
    for phase, sql in PHASE_SQL.items():
        if direct_production_write and phase == "build":
            sql = "INSERT INTO youmei_sandbox.dwd_demo SELECT number FROM numbers(1);"
        if readonly_mutation and phase == "preflight":
            sql = "CREATE TABLE youmei_sandbox.bad_table (id UInt64) ENGINE = MergeTree ORDER BY id;"
        (package / f"{phase}.sql").write_text(sql, encoding="utf-8")
    if duplicate_phase:
        (package / "quality.sql").write_text(PHASE_SQL["preflight"], encoding="utf-8")
    (package / "metadata.yaml").write_text(
        "status: approved\n"
        "table:\n"
        "  fully_qualified_name: youmei_clickhouse.default.youmei_sandbox.dwd_demo\n",
        encoding="utf-8",
    )
    release = package / "release.yaml"
    release.write_text(
        "release_api_version: warehouse-release/v1\n"
        "release_id: test_release_1_0_0\n"
        "version: 1.0.0\n"
        "release_type: formal\n"
        "environment: test\n"
        "status: approved\n"
        "source:\n"
        "  database: youmei_sandbox\n"
        "  partitions: ['2026-07-22']\n"
        "targets:\n"
        "  - chinese_name: 测试事实表\n"
        "    physical_name: dwd_demo\n"
        "    production_physical_name: dwd_demo\n"
        "    candidate_physical_name: dwd_demo__candidate__1_0_0\n"
        "    previous_physical_name: dwd_demo__previous__1_0_0\n"
        "    database: youmei_sandbox\n"
        "    grain: 测试粒度\n"
        "    key: [id]\n"
        "publish:\n"
        "  strategy: candidate_swap\n"
        "  phases:\n"
        + "".join(
            f"    {phase}: {'preflight.sql' if duplicate_phase and phase == 'quality' else phase + '.sql'}\n"
            for phase in PHASE_SQL
        )
        + "openmetadata:\n"
        "  contracts: [metadata.yaml]\n"
        "approval:\n"
        "  status: approved\n"
        "  formal_publish_authorized: true\n"
        "git:\n"
        "  required: true\n"
        "  auto_commit: true\n"
        "  auto_push: true\n"
        "  remote: origin\n"
        "  branch: main\n"
        "  tag: warehouse/test-release-1.0.0\n",
        encoding="utf-8",
    )
    return release


def create_cleanup_package(root: Path, *, authorized: bool = True, missing_object_in_sql: bool = False) -> Path:
    package = root / "cleanup"
    package.mkdir()
    (package / "preflight.sql").write_text(
        "SELECT count() FROM system.tables WHERE database = 'youmei_sandbox';\n",
        encoding="utf-8",
    )
    (package / "quality.sql").write_text(
        "SELECT count() FROM system.tables WHERE database = 'youmei_sandbox' AND name = 'dwd_old_shadow';\n",
        encoding="utf-8",
    )
    cleanup_sql = "DROP TABLE IF EXISTS youmei_sandbox.dwd_old_shadow;\n"
    if missing_object_in_sql:
        cleanup_sql = "DROP TABLE IF EXISTS youmei_sandbox.dwd_other_shadow;\n"
    (package / "cleanup.sql").write_text(cleanup_sql, encoding="utf-8")
    (package / "postcheck.sql").write_text(
        "SELECT count() FROM system.tables WHERE database = 'youmei_sandbox' AND name = 'dwd_demo';\n",
        encoding="utf-8",
    )
    (package / "metadata.yaml").write_text(
        "status: approved\n"
        "table:\n"
        "  fully_qualified_name: youmei_clickhouse.default.youmei_sandbox.dwd_demo\n",
        encoding="utf-8",
    )
    release = package / "release.yaml"
    release.write_text(
        "release_api_version: warehouse-release/v1\n"
        "release_id: test_cleanup_1_0_0\n"
        "version: 1.0.0\n"
        "release_type: cleanup\n"
        "environment: test\n"
        "status: approved\n"
        "source:\n"
        "  database: youmei_sandbox\n"
        "  partitions: ['2026-07-22']\n"
        "cleanup:\n"
        "  objects:\n"
        "    - database: youmei_sandbox\n"
        "      physical_name: dwd_old_shadow\n"
        "publish:\n"
        "  strategy: cleanup_only\n"
        "  phases:\n"
        "    preflight: preflight.sql\n"
        "    quality: quality.sql\n"
        "    cleanup: cleanup.sql\n"
        "    postcheck: postcheck.sql\n"
        "openmetadata:\n"
        "  contracts: [metadata.yaml]\n"
        "  retire:\n"
        "    - fully_qualified_name: youmei_clickhouse.default.youmei_sandbox.dwd_old_shadow\n"
        "approval:\n"
        "  status: approved\n"
        f"  cleanup_authorized: {'true' if authorized else 'false'}\n"
        "git:\n"
        "  required: true\n"
        "  auto_commit: true\n"
        "  auto_push: true\n"
        "  remote: origin\n"
        "  branch: main\n"
        "  tag: warehouse/test-cleanup-1.0.0\n",
        encoding="utf-8",
    )
    return release


class WarehouseReleaseValidationTests(unittest.TestCase):
    def test_git_remote_push_settings_are_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = build_context(create_package(Path(directory)))
            self.assertTrue(context.normalized["git"]["auto_push"])
            self.assertEqual(context.normalized["git"]["remote"], "origin")
            self.assertEqual(context.normalized["git"]["branch"], "main")

    def test_shadow_full_requires_remote_push(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = create_package(Path(directory))
            text = release.read_text(encoding="utf-8")
            text = text.replace("release_type: formal", "release_type: shadow")
            text = text.replace("  formal_publish_authorized: true", "  shadow_publish_authorized: true")
            text = text.replace("  auto_push: true", "  auto_push: false")
            release.write_text(text, encoding="utf-8")
            context = build_context(release)
            validate_context(context, "full")
            self.assertTrue(any("git.auto_push" in item for item in context.errors))

    def test_verify_allows_first_publish_without_existing_target(self) -> None:
        import scripts.warehouse_release as release_runner

        with tempfile.TemporaryDirectory() as directory:
            release = create_package(Path(directory))
            text = release.read_text(encoding="utf-8")
            text = text.replace("release_type: formal", "release_type: shadow")
            text = text.replace("  formal_publish_authorized: true", "  shadow_publish_authorized: true")
            release.write_text(text, encoding="utf-8")
            context = build_context(release)
            original_root = release_runner.PROJECT_ROOT
            release_runner.PROJECT_ROOT = Path(directory)
            try:
                with (
                    mock.patch.object(release_runner, "execute_clickhouse_health", return_value={"ok": True}),
                    mock.patch.object(release_runner, "execute_clickhouse_phase", return_value={"ok": True}),
                    mock.patch.object(
                        release_runner,
                        "clickhouse_target_state",
                        return_value={"ok": True, "all_targets_exist": False, "targets": [{"exists": False}]},
                    ),
                    mock.patch.object(release_runner, "run_openmetadata") as metadata,
                ):
                    status = run_verify(context, Path("query.py"), Path("executor.py"), Path("metadata.py"))
            finally:
                release_runner.PROJECT_ROOT = original_root
            self.assertEqual(status, 0)
            metadata.assert_not_called()
            report = json.loads((context.package_dir / f"release-report-{context.release_id}.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "pre_publish_verified")

    def test_clickhouse_config_falls_back_from_empty_legacy_database(self) -> None:
        context = SimpleNamespace(
            raw={"clickhouse": {"base_url": "", "database": ""}},
            normalized={"source": {"database": ""}},
        )
        with mock.patch.dict(os.environ, {"CLICKHOUSE_BASE_URL": "", "CLICKHOUSE_DATABASE": ""}):
            self.assertEqual(
                clickhouse_config(context),
                ("http://127.0.0.1:8123", "youmei_sandbox"),
            )

    def test_full_release_runs_all_phases_and_records_git(self) -> None:
        import scripts.warehouse_release as release_runner

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            remote = root / "remote.git"
            repo.mkdir()
            remote.mkdir()
            run_git(remote, "init", "--bare")
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "test-user")
            run_git(repo, "config", "user.email", "test@example.invalid")
            (repo / "README.md").write_text("test\n", encoding="utf-8")
            run_git(repo, "add", "README.md")
            run_git(repo, "commit", "-m", "test baseline")
            run_git(repo, "remote", "add", "origin", str(remote))

            release = create_package(repo)
            log_path = root / "execution.log"
            query_runner = root / "query.py"
            executor = root / "executor.py"
            metadata_sync = root / "metadata_sync.py"
            query_runner.write_text(
                "from pathlib import Path\n"
                f"Path({str(log_path)!r}).open('a', encoding='utf-8').write('health\\n')\n",
                encoding="utf-8",
            )
            executor.write_text(
                "import sys\n"
                "from pathlib import Path\n"
                f"log = Path({str(log_path)!r})\n"
                "args = sys.argv\n"
                "sql_path = Path(args[args.index('--sql-file') + 1])\n"
                "with log.open('a', encoding='utf-8') as handle:\n"
                "    handle.write(sql_path.stem + '\\n')\n",
                encoding="utf-8",
            )
            metadata_sync.write_text(
                "import json\n"
                "import sys\n"
                "from pathlib import Path\n"
                f"log = Path({str(log_path)!r})\n"
                "args = sys.argv\n"
                "with log.open('a', encoding='utf-8') as handle:\n"
                "    handle.write('openmetadata\\n')\n"
                "report = Path(args[args.index('--report') + 1])\n"
                "report.write_text(json.dumps({'status': 'verified'}), encoding='utf-8')\n",
                encoding="utf-8",
            )

            original_root = release_runner.PROJECT_ROOT
            release_runner.PROJECT_ROOT = repo
            try:
                context = build_context(release)
                validate_context(context, "full")
                self.assertEqual(context.errors, [])
                push_observations: list[list[str]] = []
                real_git_push = release_runner.git_push

                def observe_push(*args, **kwargs):
                    push_observations.append(log_path.read_text(encoding="utf-8").splitlines())
                    return real_git_push(*args, **kwargs)

                with mock.patch.object(release_runner, "git_push", side_effect=observe_push):
                    with release_lock(context):
                        status = run_full(
                            context,
                            query_runner,
                            executor,
                            metadata_sync,
                            GIT_EXECUTABLE,
                            False,
                        )
                self.assertEqual(status, 0)
            finally:
                release_runner.PROJECT_ROOT = original_root

            self.assertFalse((release.parent / ".warehouse-release-test_release_1_0_0.lock").exists())
            self.assertEqual(
                log_path.read_text(encoding="utf-8").splitlines(),
                ["health", "preflight", "build", "quality", "swap", "postcheck", "openmetadata", "cleanup"],
            )
            self.assertEqual(
                push_observations,
                [["health", "preflight", "build", "quality", "swap", "postcheck", "openmetadata", "cleanup"]],
            )
            report = json.loads((release.parent / "release-report-test_release_1_0_0.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "succeeded")
            self.assertEqual(
                run_git(remote, "rev-parse", "refs/heads/main"),
                run_git(repo, "rev-parse", "HEAD"),
            )
            self.assertEqual(
                run_git(remote, "rev-parse", "refs/tags/warehouse/test-release-1.0.0^{}"),
                run_git(repo, "rev-parse", "HEAD"),
            )

    def test_final_push_failure_is_finalizeable(self) -> None:
        import scripts.warehouse_release as release_runner

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            remote = root / "remote.git"
            repo.mkdir()
            remote.mkdir()
            run_git(remote, "init", "--bare")
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "test-user")
            run_git(repo, "config", "user.email", "test@example.invalid")
            (repo / "README.md").write_text("test\n", encoding="utf-8")
            run_git(repo, "add", "README.md")
            run_git(repo, "commit", "-m", "test baseline")
            run_git(repo, "remote", "add", "origin", str(remote))

            release = create_package(repo)
            original_root = release_runner.PROJECT_ROOT
            release_runner.PROJECT_ROOT = repo
            try:
                context = build_context(release)
                validate_context(context, "full")
                self.assertEqual(context.errors, [])
                failed_push = {"ok": False, "error": "simulated public remote block"}
                with (
                    mock.patch.object(release_runner, "execute_clickhouse_health", return_value={"ok": True}),
                    mock.patch.object(release_runner, "execute_clickhouse_phase", return_value={"ok": True}),
                    mock.patch.object(release_runner, "run_openmetadata", return_value={"ok": True}),
                    mock.patch.object(release_runner, "git_push", return_value=failed_push),
                ):
                    with release_lock(context):
                        status = run_full(
                            context,
                            root / "unused-query.py",
                            root / "unused-executor.py",
                            root / "unused-metadata.py",
                            GIT_EXECUTABLE,
                            False,
                        )
                self.assertEqual(status, 1)
                report_path = release.parent / "release-report-test_release_1_0_0.json"
                report = json.loads(report_path.read_text(encoding="utf-8"))
                self.assertEqual(report["status"], "version_record_pending")
                self.assertEqual(
                    run_git(repo, "ls-files", "--error-unmatch", "release/release-report-test_release_1_0_0.json"),
                    "release/release-report-test_release_1_0_0.json",
                )

                with mock.patch.object(release_runner, "git_push", return_value={"ok": True}):
                    self.assertEqual(run_finalize(context, GIT_EXECUTABLE), 0)
                finalized_report = json.loads(report_path.read_text(encoding="utf-8"))
                self.assertEqual(finalized_report["status"], "finalized")
                tag_commit = run_git(repo, "rev-parse", "refs/tags/warehouse/test-release-1.0.0^{}")
                self.assertEqual(
                    run_git(repo, "merge-base", "--is-ancestor", tag_commit, run_git(repo, "rev-parse", "HEAD")),
                    "",
                )
            finally:
                release_runner.PROJECT_ROOT = original_root

    def test_postcheck_failure_rolls_back_and_records_failure(self) -> None:
        import scripts.warehouse_release as release_runner

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            remote = root / "remote.git"
            repo.mkdir()
            remote.mkdir()
            run_git(remote, "init", "--bare")
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "test-user")
            run_git(repo, "config", "user.email", "test@example.invalid")
            (repo / "README.md").write_text("test\n", encoding="utf-8")
            run_git(repo, "add", "README.md")
            run_git(repo, "commit", "-m", "test baseline")
            run_git(repo, "remote", "add", "origin", str(remote))

            release = create_package(repo)
            log_path = root / "execution.log"
            query_runner = root / "query.py"
            executor = root / "executor.py"
            query_runner.write_text("print('health')\n", encoding="utf-8")
            executor.write_text(
                "import sys\n"
                "from pathlib import Path\n"
                f"log = Path({str(log_path)!r})\n"
                "args = sys.argv\n"
                "phase = Path(args[args.index('--sql-file') + 1]).stem\n"
                "with log.open('a', encoding='utf-8') as handle:\n"
                "    handle.write(phase + '\\n')\n"
                "raise SystemExit(1 if phase == 'postcheck' else 0)\n",
                encoding="utf-8",
            )

            original_root = release_runner.PROJECT_ROOT
            release_runner.PROJECT_ROOT = repo
            try:
                context = build_context(release)
                validate_context(context, "full")
                self.assertEqual(context.errors, [])
                with release_lock(context):
                    status = run_full(
                        context,
                        query_runner,
                        executor,
                        root / "unused-metadata.py",
                        GIT_EXECUTABLE,
                        False,
                    )
                self.assertEqual(status, 1)
            finally:
                release_runner.PROJECT_ROOT = original_root

            self.assertEqual(
                log_path.read_text(encoding="utf-8").splitlines(),
                ["preflight", "build", "quality", "swap", "postcheck", "rollback"],
            )
            report = json.loads((release.parent / "release-report-test_release_1_0_0.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "failed_rolled_back")
            self.assertFalse(run_git(repo, "tag", "--list", "warehouse/test-release-1.0.0"))
            self.assertEqual(
                run_git(remote, "rev-parse", "refs/heads/main"),
                run_git(repo, "rev-parse", "HEAD"),
            )

    def test_git_push_uses_configured_remote_and_branch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            remote = root / "remote.git"
            source = root / "source"
            remote.mkdir()
            source.mkdir()
            run_git(remote, "init", "--bare")
            run_git(source, "init", "-b", "main")
            run_git(source, "config", "user.name", "test-user")
            run_git(source, "config", "user.email", "test@example.invalid")
            (source / "README.md").write_text("test\n", encoding="utf-8")
            run_git(source, "add", "README.md")
            run_git(source, "commit", "-m", "test commit")
            run_git(source, "remote", "add", "origin", str(remote))

            context = SimpleNamespace(
                normalized={
                    "git": {
                        "auto_push": True,
                        "remote": "origin",
                        "branch": "main",
                    }
                }
            )
            result = git_push(context, {"git": GIT_EXECUTABLE, "repo_root": str(source)})

            self.assertTrue(result["ok"], result)
            self.assertEqual(run_git(remote, "rev-parse", "refs/heads/main"), run_git(source, "rev-parse", "HEAD"))

    def test_git_runtime_environment_disables_interactive_prompts(self) -> None:
        environment = git_runtime_environment(GIT_EXECUTABLE)
        self.assertEqual(environment["GIT_TERMINAL_PROMPT"], "0")
        self.assertEqual(environment["GCM_INTERACTIVE"], "Never")

    def test_valid_candidate_swap_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = create_package(Path(directory))
            context = build_context(release)
            validate_context(context, "full")
            self.assertEqual(context.errors, [])
            self.assertTrue(context.manifest_fingerprint)
            with release_lock(context):
                self.assertTrue((Path(directory) / "release" / ".warehouse-release-test_release_1_0_0.lock").exists())
            self.assertFalse((Path(directory) / "release" / ".warehouse-release-test_release_1_0_0.lock").exists())

    def test_cleanup_manifest_requires_explicit_authorization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = create_cleanup_package(Path(directory), authorized=False)
            context = build_context(release)
            validate_context(context, "full")
            self.assertTrue(any("cleanup_authorized" in item for item in context.errors))

    def test_cleanup_manifest_validates_declared_objects(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = create_cleanup_package(Path(directory))
            context = build_context(release)
            validate_context(context, "full")
            self.assertEqual(context.errors, [])

    def test_cleanup_manifest_blocks_unlisted_drop_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = create_cleanup_package(Path(directory), missing_object_in_sql=True)
            context = build_context(release)
            validate_context(context, "full")
            self.assertTrue(any("未覆盖声明的清理对象" in item for item in context.errors))
            self.assertTrue(any("操作未声明的清理对象" in item for item in context.errors))

    def test_cleanup_requires_openmetadata_plan_before_drop(self) -> None:
        import scripts.warehouse_release as release_runner

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            remote = root / "remote.git"
            repo.mkdir()
            remote.mkdir()
            run_git(remote, "init", "--bare")
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "test-user")
            run_git(repo, "config", "user.email", "test@example.invalid")
            (repo / "README.md").write_text("test\n", encoding="utf-8")
            run_git(repo, "add", "README.md")
            run_git(repo, "commit", "-m", "test baseline")
            run_git(repo, "remote", "add", "origin", str(remote))

            release = create_cleanup_package(repo)
            context = build_context(release)
            validate_context(context, "full")
            self.assertEqual(context.errors, [])
            phase_calls: list[str] = []

            def fake_phase(*args, **kwargs):
                phase_calls.append(args[1])
                return {"ok": True}

            original_root = release_runner.PROJECT_ROOT
            release_runner.PROJECT_ROOT = repo
            try:
                with (
                    mock.patch.object(release_runner, "execute_clickhouse_health", return_value={"ok": True}),
                    mock.patch.object(release_runner, "execute_clickhouse_phase", side_effect=fake_phase),
                    mock.patch.object(release_runner, "run_openmetadata", return_value={"ok": False}),
                    mock.patch.object(release_runner, "git_push", return_value={"ok": True}),
                ):
                    with release_lock(context):
                        status = run_cleanup_full(
                            context,
                            root / "unused-query.py",
                            root / "unused-executor.py",
                            root / "unused-metadata.py",
                            GIT_EXECUTABLE,
                            False,
                        )
            finally:
                release_runner.PROJECT_ROOT = original_root

            self.assertEqual(status, 1)
            self.assertEqual(phase_calls, ["preflight", "quality"])
            report = json.loads((release.parent / "release-report-test_cleanup_1_0_0.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "failed")

    def test_duplicate_phase_file_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = create_package(Path(directory), duplicate_phase=True)
            context = build_context(release)
            validate_context(context, "full")
            self.assertTrue(any("重复使用" in item for item in context.errors))

    def test_direct_production_write_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = create_package(Path(directory), direct_production_write=True)
            context = build_context(release)
            validate_context(context, "full")
            self.assertTrue(any("直接操作生产表" in item for item in context.errors))

    def test_readonly_phase_mutation_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = create_package(Path(directory), readonly_mutation=True)
            context = build_context(release)
            validate_context(context, "full")
            self.assertTrue(any("必须只读" in item for item in context.errors))

    def test_readonly_system_table_query_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = create_package(Path(directory))
            quality = release.parent / "quality.sql"
            quality.write_text(
                "SELECT count() FROM system.columns WHERE database = 'youmei_sandbox';\n",
                encoding="utf-8",
            )
            context = build_context(release)
            validate_context(context, "full")
            self.assertFalse(any("quality 阶段必须只读" in item for item in context.errors))

    def test_legacy_manifest_is_read_only_compatible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "legacy"
            package.mkdir()
            release = package / "legacy.yaml"
            release.write_text(
                "release_id: legacy_release_1_0_0\n"
                "openmetadata:\n"
                "  contracts: []\n",
                encoding="utf-8",
            )
            context = build_context(release)
            validate_context(context, "plan")
            self.assertEqual(context.errors, [])
            self.assertTrue(context.warnings)


if __name__ == "__main__":
    unittest.main()
