from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from forgeloop.cli import main
from forgeloop.opencli import (
    CommandRun,
    _display_command,
    _plugin_source_status,
    _run_fixed,
    fetch_opencli_npm_metadata,
    format_opencli_install_result,
    opencli_status,
    run_opencli_install,
)


class CliBranchTests(unittest.TestCase):
    def test_validate_json_returns_failure_for_error_findings(self) -> None:
        finding = SimpleNamespace(level="error", as_dict=lambda _root: {"level": "error"})
        output = StringIO()
        with patch("forgeloop.cli.validate_repo", return_value=[finding]), redirect_stdout(output):
            result = main(["validate", ".", "--json"])
        self.assertEqual(1, result)
        self.assertEqual([{"level": "error"}], json.loads(output.getvalue()))

    def test_index_check_reports_stale_index(self) -> None:
        output = StringIO()
        result = SimpleNamespace(changed=True)
        with patch("forgeloop.cli.build_memory_index", return_value=result), redirect_stdout(output):
            code = main(["index", ".", "--check"])
        self.assertEqual(1, code)
        self.assertIn("out of date", output.getvalue())

    def test_pack_reports_invalid_query_to_stderr(self) -> None:
        error = StringIO()
        with patch("forgeloop.cli.build_context_pack", side_effect=ValueError("query rejected")), redirect_stderr(error):
            code = main(["pack", "secret-value", "."])
        self.assertEqual(1, code)
        self.assertIn("query rejected", error.getvalue())

    def test_compat_and_doctor_use_report_health_for_exit_status(self) -> None:
        output = StringIO()
        compat = {"targets": [{"profile_files_present": False}]}
        doctor = {"ok": False}
        with (
            patch("forgeloop.cli.compatibility_report", return_value=compat),
            patch("forgeloop.cli.format_compatibility_report", return_value="missing profile"),
            redirect_stdout(output),
        ):
            self.assertEqual(1, main(["compat", "."]))
        with (
            patch("forgeloop.cli.doctor_report", return_value=doctor),
            patch("forgeloop.cli.format_doctor_report", return_value="not healthy"),
            redirect_stdout(output),
        ):
            self.assertEqual(1, main(["doctor", "."]))
        self.assertIn("missing profile", output.getvalue())
        self.assertIn("not healthy", output.getvalue())

    def test_tokens_and_setup_errors_are_user_facing_and_nonzero(self) -> None:
        error = StringIO()
        with patch("forgeloop.cli.build_token_report", side_effect=ValueError("bad query")), redirect_stderr(error):
            self.assertEqual(1, main(["tokens", "bad", "."]))
        with patch("forgeloop.cli.run_setup", side_effect=ValueError("unknown tool")), redirect_stderr(error):
            self.assertEqual(1, main(["setup", ".", "--tool", "codex"]))
        self.assertIn("bad query", error.getvalue())
        self.assertIn("unknown tool", error.getvalue())

    def test_hook_simulate_rejects_invalid_json_and_non_object_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "input.json"
            source.write_text("[]", encoding="utf-8")
            error = StringIO()
            with redirect_stderr(error):
                code = main(["hook-simulate", "Stop", ".", "--input", str(source)])
        self.assertEqual(1, code)
        self.assertIn("must be an object", error.getvalue())

    def test_secrets_check_returns_nonzero_when_repo_env_files_exist(self) -> None:
        status = SimpleNamespace(
            as_dict=lambda _root: {"repo_env_files": [".env"], "warnings": ["remove local secrets"]},
            exists=False,
            keys=[],
            repo_env_files=[Path.cwd() / ".env"],
            warnings=["remove local secrets"],
        )
        output = StringIO()
        with patch("forgeloop.cli.check_secrets", return_value=status), redirect_stdout(output):
            result = main(["secrets", "check", "."])
        self.assertEqual(1, result)
        self.assertIn(".env", output.getvalue())

    def test_governance_audit_and_verify_reflect_invalid_reports(self) -> None:
        output = StringIO()
        with (
            patch("forgeloop.cli.audit_governed_memory", return_value={"errors": ["bad metadata"]}),
            patch("forgeloop.cli.format_governance_audit", return_value="bad metadata"),
            redirect_stdout(output),
        ):
            self.assertEqual(1, main(["governance", "audit", "."]))
        with (
            patch("forgeloop.cli.verify_audit_log", return_value={"valid": False}),
            patch("forgeloop.cli.format_governance_log_status", return_value="invalid chain"),
            redirect_stdout(output),
        ):
            self.assertEqual(1, main(["governance", "verify", "."]))
        self.assertIn("bad metadata", output.getvalue())
        self.assertIn("invalid chain", output.getvalue())

    def test_opencli_install_cli_clamps_timeout_and_reports_failure(self) -> None:
        output = StringIO()
        with (
            patch("forgeloop.cli.run_opencli_install", return_value={"status": "failed", "executed": True}),
            patch("forgeloop.cli.format_opencli_install_result", return_value="install failed") as formatter,
            redirect_stdout(output),
        ):
            result = main(["opencli", "install", ".", "--execute", "--timeout", "1"])
        self.assertEqual(1, result)
        self.assertEqual(30, formatter.call_args.args[0].get("timeout", 30))
        self.assertIn("install failed", output.getvalue())

    def test_cli_returns_usage_error_for_missing_nested_command(self) -> None:
        error = StringIO()
        with redirect_stderr(error), self.assertRaises(SystemExit) as raised:
            main(["opencli"])
        self.assertEqual(2, raised.exception.code)
        self.assertIn("usage:", error.getvalue())


class OpenCliFailurePathTests(unittest.TestCase):
    def _plan(self, *, node: bool = True, npm: bool = True, plugin: bool = True) -> dict:
        return {
            "status": {
                "node": {"ready": node},
                "npm": {"ready": npm, "path": "npm" if npm else ""},
                "plugin_source": {
                    "ready": plugin,
                    "path": "integrations/opencli",
                    "reason": "plugin source unsafe",
                },
            }
        }

    def test_install_blocks_before_execution_for_each_missing_prerequisite(self) -> None:
        for plan, message in (
            (self._plan(node=False), "Node.js >= 21"),
            (self._plan(npm=False), "npm is required"),
            (self._plan(plugin=False), "plugin source unsafe"),
        ):
            with (
                self.subTest(message=message),
                patch("forgeloop.opencli.opencli_plan", return_value=plan),
                patch("forgeloop.opencli._run_fixed") as runner,
            ):
                result = run_opencli_install(Path("."), execute=True)
            self.assertEqual("blocked", result["status"])
            self.assertIn(message, result["results"][0]["reason"])
            runner.assert_not_called()

    def test_install_blocks_when_binary_does_not_appear_after_npm(self) -> None:
        with (
            patch("forgeloop.opencli.opencli_plan", return_value=self._plan()),
            patch("forgeloop.opencli._run_fixed", return_value=CommandRun(["npm"], 0, "", "")),
            patch("forgeloop.opencli.shutil.which", return_value=None),
        ):
            result = run_opencli_install(Path("."), execute=True)
        self.assertEqual("blocked", result["status"])
        self.assertIn("not found on PATH", result["results"][-1]["reason"])

    def test_install_stops_after_each_failed_verification_command(self) -> None:
        for failed_args in (["plugin", "install"], ["--version"], ["list", "-f", "json"]):
            calls: list[list[str]] = []

            def runner(
                executable: str,
                args: list[str],
                timeout: int,
                expected_args: list[str] = failed_args,
                recorded_calls: list[list[str]] = calls,
            ) -> CommandRun:
                recorded_calls.append(args)
                failed = args[: len(expected_args)] == expected_args
                return CommandRun([executable, *args], 1 if failed else 0, "", "")

            with (
                self.subTest(failed_args=failed_args),
                patch("forgeloop.opencli.opencli_plan", return_value=self._plan()),
                patch("forgeloop.opencli._run_fixed", side_effect=runner),
                patch("forgeloop.opencli.shutil.which", return_value="opencli"),
            ):
                result = run_opencli_install(Path("."), execute=True)
            self.assertEqual("failed", result["status"])
            self.assertEqual(failed_args, calls[-1][: len(failed_args)])

    def test_optional_doctor_and_skills_are_run_and_failure_is_not_hidden(self) -> None:
        calls: list[list[str]] = []

        def runner(executable: str, args: list[str], timeout: int) -> CommandRun:
            calls.append([executable, *args])
            failed = args == ["doctor"]
            return CommandRun([executable, *args], 1 if failed else 0, "", "")

        with (
            patch("forgeloop.opencli.opencli_plan", return_value=self._plan()),
            patch("forgeloop.opencli._run_fixed", side_effect=runner),
            patch("forgeloop.opencli.shutil.which", side_effect=["opencli", "npx"]),
        ):
            result = run_opencli_install(Path("."), include_skills=True, run_doctor=True, execute=True)
        self.assertEqual("failed", result["status"])
        self.assertIn(["opencli", "doctor"], calls)
        self.assertIn(["npx", "skills", "add", "jackwener/opencli"], calls)

    def test_missing_npx_marks_optional_skill_install_failed(self) -> None:
        def runner(executable: str, args: list[str], timeout: int) -> CommandRun:
            return CommandRun([executable, *args], 0, "", "")

        with (
            patch("forgeloop.opencli.opencli_plan", return_value=self._plan()),
            patch("forgeloop.opencli._run_fixed", side_effect=runner),
            patch("forgeloop.opencli.shutil.which", side_effect=["opencli", None]),
        ):
            result = run_opencli_install(Path("."), include_skills=True, execute=True)
        self.assertEqual("failed", result["status"])
        self.assertTrue(result["results"][-1]["skipped"])
        self.assertIn("npx was not found", result["results"][-1]["reason"])

    def test_status_reports_missing_and_unparseable_toolchain(self) -> None:
        with (
            patch("forgeloop.opencli.shutil.which", return_value=None),
            patch("forgeloop.opencli._version_from_command", return_value=""),
        ):
            status = opencli_status(Path("."))
        self.assertFalse(status["node"]["ready"])
        self.assertFalse(status["npm"]["ready"])
        self.assertFalse(status["npx"]["ready"])
        self.assertTrue(any("Node.js was not found" in warning for warning in status["warnings"]))

    def test_npm_metadata_handles_missing_command_bad_json_and_non_object(self) -> None:
        with patch("forgeloop.opencli.shutil.which", return_value=None):
            missing = fetch_opencli_npm_metadata()
        self.assertTrue(missing["checked"])
        self.assertTrue(missing["warnings"])

        for stdout, expected in (("not json", "not valid JSON"), ("[]", "did not return an object")):
            with (
                self.subTest(stdout=stdout),
                patch("forgeloop.opencli.shutil.which", return_value="npm"),
                patch("forgeloop.opencli._run_fixed", return_value=CommandRun(["npm"], 0, stdout, "")),
            ):
                result = fetch_opencli_npm_metadata()
            self.assertIn(expected, result["warnings"][0])

    def test_npm_metadata_warns_when_registry_engine_is_below_supported_minimum(self) -> None:
        payload = {"version": "1.2.3", "engines": {"node": ">=20.0.0"}}
        with (
            patch("forgeloop.opencli.shutil.which", return_value="npm"),
            patch("forgeloop.opencli._run_fixed", return_value=CommandRun(["npm"], 0, json.dumps(payload), "")),
        ):
            metadata = fetch_opencli_npm_metadata()
        self.assertEqual(20, metadata["node_engine_major"])
        self.assertIn("stricter docs baseline", metadata["warnings"][0])

    def test_plugin_source_rejects_missing_manifest_and_path_resolution_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plugin = root / "integrations/opencli"
            plugin.mkdir(parents=True)
            missing_manifest = _plugin_source_status(root)
            self.assertFalse(missing_manifest["ready"])
            self.assertIn("manifest", missing_manifest["reason"])

            original_resolve = Path.resolve

            def fail_plugin_resolution(path: Path, *args, **kwargs) -> Path:
                if path == root:
                    return original_resolve(path, *args, **kwargs)
                raise OSError("unavailable")

            with patch.object(Path, "resolve", new=fail_plugin_resolution):
                failed_resolve = _plugin_source_status(root)
            self.assertFalse(failed_resolve["ready"])
            self.assertIn("resolved safely", failed_resolve["reason"])

            with patch.object(Path, "resolve", side_effect=OSError("unavailable")):
                failed_root = _plugin_source_status(root)
            self.assertFalse(failed_root["ready"])
            self.assertIn("repository root", failed_root["reason"])

    def test_fixed_runner_handles_timeout_oserror_and_truncation(self) -> None:
        import subprocess

        with patch("forgeloop.opencli.subprocess.run", side_effect=subprocess.TimeoutExpired("npm", 1, stderr="slow")):
            timed_out = _run_fixed("npm", ["view"], timeout=1)
        self.assertTrue(timed_out.timed_out)

        with patch("forgeloop.opencli.subprocess.run", side_effect=OSError("private path detail")):
            failed = _run_fixed("npm", ["view"], timeout=1)
        self.assertTrue(failed.skipped)
        self.assertEqual("", failed.stderr)

        output = format_opencli_install_result({
            "executed": True,
            "status": "failed",
            "results": [
                {"command": ["cmd", "has spaces"], "skipped": True, "reason": "missing"},
                {"command": ["cmd", "slow"], "skipped": False, "timed_out": True},
                {"command": ["cmd", "bad"], "skipped": False, "timed_out": False, "exit_code": 3},
            ],
        })
        self.assertIn('"has spaces" (missing)', output)
        self.assertIn("timed out", output)
        self.assertIn("exit 3", output)
        self.assertEqual("tool " + '"path with spaces"', _display_command(["tool", "path with spaces"]))


if __name__ == "__main__":
    unittest.main()
