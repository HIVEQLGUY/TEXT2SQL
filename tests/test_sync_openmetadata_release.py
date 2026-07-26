from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts import sync_openmetadata_release as sync_release  # noqa: E402


class OpenMetadataReleaseFlowTests(unittest.TestCase):
    def test_full_runs_global_plan_apply_verify_for_contracts_and_retirements(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            package = Path(temporary_directory)
            release = package / "release.yaml"
            contract_a = package / "contract-a.yaml"
            contract_b = package / "contract-b.yaml"
            contract_a.write_text("contract_id: a\n", encoding="utf-8")
            contract_b.write_text("contract_id: b\n", encoding="utf-8")
            release.write_text(
                "openmetadata:\n"
                "  contracts:\n"
                "    - contract-a.yaml\n"
                "    - contract-b.yaml\n"
                "  retire:\n"
                "    - fully_qualified_name: old_table\n",
                encoding="utf-8",
            )
            report = package / "sync-report.json"
            calls: list[tuple[str, str, str]] = []

            def fake_contract(sync_script: Path, contract: Path, mode: str) -> dict:
                calls.append(("contract", contract.name, mode))
                return {"contract": str(contract), "mode": mode, "ok": True, "returncode": 0}

            def fake_retirement(items: list[dict[str, str]], mode: str) -> list[dict]:
                calls.append(("retire", items[0]["fully_qualified_name"], mode))
                return [
                    {
                        "fully_qualified_name": items[0]["fully_qualified_name"],
                        "mode": mode,
                        "ok": True,
                        "action": "deleted" if mode == "apply" else "verified_absent",
                    }
                ]

            argv = [
                "sync_openmetadata_release.py",
                "--package-dir",
                str(package),
                "--release",
                str(release),
                "--sync-script",
                str(Path(__file__)),
                "--mode",
                "full",
                "--report",
                str(report),
            ]
            with (
                mock.patch.object(sys, "argv", argv),
                mock.patch.object(sync_release, "load_env_file", return_value={}),
                mock.patch.object(sync_release, "run_contract", side_effect=fake_contract),
                mock.patch.object(sync_release, "run_retirement", side_effect=fake_retirement),
            ):
                self.assertEqual(sync_release.main(), 0)

            self.assertEqual(
                calls,
                [
                    ("contract", "contract-a.yaml", "plan"),
                    ("contract", "contract-b.yaml", "plan"),
                    ("retire", "old_table", "plan"),
                    ("contract", "contract-a.yaml", "apply"),
                    ("contract", "contract-b.yaml", "apply"),
                    ("retire", "old_table", "apply"),
                    ("contract", "contract-a.yaml", "verify"),
                    ("contract", "contract-b.yaml", "verify"),
                    ("retire", "old_table", "verify"),
                ],
            )
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["mode"], "full")
            self.assertNotIn("full", [item.get("mode") for item in payload["results"]])


if __name__ == "__main__":
    unittest.main()
