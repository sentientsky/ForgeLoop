from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from forgeloop.banner import ASCII_BANNER, ORANGE, RESET, is_ascii, render_intro
from forgeloop.cli import main
from forgeloop.compat import compatibility_report
from forgeloop.context import build_context_pack, render_context_pack
from forgeloop.core import (
    build_memory_index,
    collect_memory_records,
    create_note,
    parse_frontmatter,
    simulate_hook_event,
    slugify,
    validate_repo,
)
from forgeloop.doctor import doctor_report
from forgeloop.governance import audit_governed_memory, record_audit_event, verify_audit_log
from forgeloop.opencli import (
    CommandRun,
    opencli_plan,
    opencli_status,
    parse_node_engine_major,
    parse_node_major,
    run_opencli_install,
)
from forgeloop.secrets import check_secrets, external_secrets_path, init_external_secrets, parse_env_keys
from forgeloop.setup import ALL_SUPPORTED_ID, SUPPORTED_TOOLS, run_setup, setup_menu_text
from forgeloop.tokens import build_token_report, format_token_report


class FrontmatterTests(unittest.TestCase):
    def test_parse_frontmatter_extracts_simple_values_and_lists(self) -> None:
        text = "---\ntype: capture\nstatus: current\ntags: [memory, safety]\n---\n# Title\n"
        data, body = parse_frontmatter(text)

        self.assertEqual(data["type"], "capture")
        self.assertEqual(data["status"], "current")
        self.assertEqual(data["tags"], ["memory", "safety"])
        self.assertIn("# Title", body)


class GovernanceTests(unittest.TestCase):
    def test_governed_memory_audit_accepts_external_personal_data_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / "docs/captures/governed-pointer.md"
            note.parent.mkdir(parents=True)
            note.write_text(
                "---\n"
                "type: capture\n"
                "status: current\n"
                "data_classification: internal\n"
                "governed_content_classification: personal\n"
                "subject_ref: SUBJ-EXAMPLE-001\n"
                "jurisdiction: GB\n"
                "purpose: support\n"
                "lawful_basis: contract\n"
                "provenance_source: user-provided\n"
                "provenance_recorded_at: 2026-08-23\n"
                "retention_until: 2027-08-23\n"
                "storage_ref: STORE-EXTERNAL-001\n"
                "tags: [governed-memory]\n"
                "---\n"
                "# External pointer\n\nOnly an opaque external reference is stored here.\n",
                encoding="utf-8",
            )

            report = audit_governed_memory(root, today=date(2026, 8, 23))

        self.assertTrue(report["ok"])
        self.assertEqual(1, report["governed_records"])

    def test_governed_memory_audit_rejects_personal_data_in_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / "docs/captures/unsafe-memory.md"
            note.parent.mkdir(parents=True)
            note.write_text(
                "---\n"
                "type: capture\n"
                "data_classification: personal\n"
                "tags: [governed-memory]\n"
                "---\n"
                "# Unsafe record\n",
                encoding="utf-8",
            )

            report = audit_governed_memory(root)

        self.assertFalse(report["ok"])
        self.assertIn("personal-data-in-repository", {item["code"] for item in report["errors"]})
        self.assertEqual("docs/captures/unsafe-memory.md", report["errors"][0]["path"])

    def test_governance_audit_log_hashes_references_and_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repository"
            root.mkdir()
            governance_home = Path(tmp) / "governance-home"
            with patch.dict(os.environ, {"FORGELOOP_GOVERNANCE_HOME": str(governance_home)}):
                result = record_audit_event(
                    root,
                    action="collect",
                    actor_ref="OPERATOR-001",
                    record_ref="STORE-EXTERNAL-001",
                    subject_ref="SUBJ-EXAMPLE-001",
                )
                valid_status = verify_audit_log(root)
                audit_log = next((governance_home / "governance/audit").glob("*.jsonl"))
                raw_log = audit_log.read_text(encoding="utf-8")
                audit_log.write_text(raw_log.replace("collect", "erase"), encoding="utf-8")
                invalid_status = verify_audit_log(root)

        self.assertTrue(result["recorded"])
        self.assertTrue(valid_status["valid"])
        self.assertEqual(1, valid_status["event_count"])
        self.assertNotIn("SUBJ-EXAMPLE-001", raw_log)
        self.assertFalse(invalid_status["valid"])

    def test_governance_log_refuses_personal_identifiers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                record_audit_event(
                    Path(tmp),
                    action="access",
                    actor_ref="OPERATOR-001",
                    record_ref="STORE-EXTERNAL-001",
                    subject_ref="person@example.com",
                )

    def test_governance_log_refuses_storage_inside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.dict(os.environ, {"FORGELOOP_GOVERNANCE_HOME": str(root)}):
                with self.assertRaises(ValueError):
                    record_audit_event(
                        root,
                        action="access",
                        actor_ref="OPERATOR-001",
                        record_ref="STORE-EXTERNAL-001",
                    )

    def test_secrets_init_cli_does_not_echo_external_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repository"
            root.mkdir()
            (root / ".env.example").write_text("FORGELOOP_TEST_KEY=\n", encoding="utf-8")
            output = StringIO()
            with patch.dict(os.environ, {"FORGELOOP_CONFIG_HOME": str(Path(tmp) / "config-home")}), redirect_stdout(output):
                self.assertEqual(0, main(["secrets", "init", str(root), "--json"]))

        self.assertIn('"external": true', output.getvalue())
        self.assertNotIn("external_path", output.getvalue())
        self.assertNotIn(str(root), output.getvalue())


class BannerTests(unittest.TestCase):
    def test_banner_is_ascii_and_reads_forgeloop(self) -> None:
        self.assertTrue(is_ascii(ASCII_BANNER))
        self.assertIn("########", ASCII_BANNER)
        self.assertEqual(7, len(ASCII_BANNER.splitlines()))

    def test_render_intro_wraps_orange_when_requested(self) -> None:
        coloured = render_intro(colour=True)
        plain = render_intro(colour=False)

        self.assertTrue(coloured.startswith(ORANGE))
        self.assertTrue(coloured.endswith(RESET))
        self.assertNotIn(ORANGE, plain)
        self.assertIn("Discover. Frame. Build. Check. Capture.", plain)

    def test_intro_cli_plain_mode(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(0, main(["intro", "--plain", "--no-tagline"]))
        self.assertIn("########", output.getvalue())


class ValidationTests(unittest.TestCase):
    def test_current_repository_has_no_validation_errors(self) -> None:
        root = Path(__file__).resolve().parents[1]
        findings = validate_repo(root)
        errors = [finding for finding in findings if finding.level == "error"]

        self.assertEqual([], errors)

    def test_validation_catches_risky_hooks_and_bad_skill_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in [
                ".claude/skills/discover",
                ".claude/skills/frame",
                ".claude/skills/build",
                ".claude/skills/check",
                ".claude/skills/capture",
                ".claude/agents",
                ".claude/hooks",
                "docs/discoveries",
                "docs/frames",
                "docs/builds",
                "docs/checks",
                "docs/captures",
                "docs/solutions",
                "docs/standards",
                "docs/palace/indexes",
                "memory",
                "templates",
                "examples",
            ]:
                (root / rel).mkdir(parents=True, exist_ok=True)
            for name in ["README.md", "CLAUDE.md", "LICENSE", "CONTRIBUTING.md"]:
                (root / name).write_text("# ok\n", encoding="utf-8")
            (root / ".env.example").write_text("FORGELOOP_TEST_KEY=\n", encoding="utf-8")
            (root / "pyproject.toml").write_text('[project]\nversion = "0.1.0"\n', encoding="utf-8")
            (root / ".claude/skills/discover/SKILL.md").write_text(
                "---\nname: wrong\ndescription: bad\n---\n# Skill\n",
                encoding="utf-8",
            )
            (root / ".claude/hooks/unsafe.md").write_text("eval $(cat input)\n", encoding="utf-8")
            (root / ".env").write_text("REAL_SECRET=do-not-commit-this-value\n", encoding="utf-8")
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/risky.yml").write_text(
                "on:\n  pull_request_target:\npermissions: write-all\njobs:\n"
                "  risky:\n    steps:\n      - uses: actions/checkout@v7\n",
                encoding="utf-8",
            )
            (root / ".github/workflows/missing-permissions.yml").write_text(
                "on:\n  push:\njobs:\n  test:\n    steps:\n"
                "      - uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0\n",
                encoding="utf-8",
            )

            findings = validate_repo(root)
            codes = {finding.code for finding in findings}

            self.assertIn("skill-name", codes)
            self.assertIn("risky-hook", codes)
            self.assertIn("env-file-in-repo", codes)
            self.assertIn("risky-workflow-trigger", codes)
            self.assertIn("workflow-write-all", codes)
            self.assertIn("workflow-permissions", codes)
            self.assertIn("unpinned-action", codes)

    def test_validation_catches_public_url_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "Source: https://github.com/<YOUR_ACCOUNT>/ForgeLoop\n",
                encoding="utf-8",
            )

            findings = validate_repo(root)

        self.assertIn("public-url-placeholder", {finding.code for finding in findings})


class NewNoteTests(unittest.TestCase):
    def test_slugify_removes_path_traversal_characters(self) -> None:
        self.assertEqual("escape-token", slugify("../Escape Token"))

    def test_create_note_uses_template_and_refuses_overwrite(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root) as tmp:
            test_root = Path(tmp)
            (test_root / "templates").mkdir()
            (test_root / "docs/frames").mkdir(parents=True)
            (test_root / "templates/frame-template.md").write_text(
                "---\ntype: frame\ndate: YYYY-MM-DD\nstatus: draft\n---\n# Frame: Short Task Name\n",
                encoding="utf-8",
            )

            result = create_note(
                test_root,
                "frame",
                "Safe Test Note",
                note_date=date(2026, 4, 17),
            )
            text = result.path.read_text(encoding="utf-8")

            self.assertEqual(test_root / "docs/frames/2026-04-17-safe-test-note.md", result.path)
            self.assertIn("# Frame: Safe Test Note", text)
            with self.assertRaises(FileExistsError):
                create_note(test_root, "frame", "Safe Test Note", note_date=date(2026, 4, 17))

    def test_create_note_supports_release_polish_note_kinds(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root) as tmp:
            test_root = Path(tmp)
            (test_root / "templates").mkdir()
            (test_root / "docs/decisions").mkdir(parents=True)
            (test_root / "templates/decision-template.md").write_text(
                "---\ntype: decision\ndate: YYYY-MM-DD\nstatus: proposed\n---\n# Short Task Name\n",
                encoding="utf-8",
            )

            result = create_note(
                test_root,
                "decision",
                "Keep Local First",
                note_date=date(2026, 5, 18),
            )

            self.assertEqual(test_root / "docs/decisions/2026-05-18-keep-local-first.md", result.path)
            self.assertIn("# Keep Local First", result.path.read_text(encoding="utf-8"))


class HookSimulationTests(unittest.TestCase):
    def test_stop_hook_simulation_never_executes_commands(self) -> None:
        result = simulate_hook_event(
            Path(__file__).resolve().parents[1],
            "Stop",
            {
                "session_id": "abc; rm -rf /",
                "message_count": 15,
                "transcript_path": "../../outside.jsonl",
            },
        )

        self.assertEqual("remind-capture", result.action)
        self.assertFalse(result.details["executes_commands"])
        self.assertEqual("abc__rm_-rf__", result.details["session_id"])
        self.assertFalse(result.details["transcript_path_accepted"])


class SecretsTests(unittest.TestCase):
    def test_parse_env_keys_reads_only_keys(self) -> None:
        keys = parse_env_keys("# comment\nFORGELOOP_ONE=value\n\nFORGELOOP_TWO=\n")

        self.assertEqual(["FORGELOOP_ONE", "FORGELOOP_TWO"], keys)

    def test_external_secrets_init_writes_outside_repo(self) -> None:
        previous = os.environ.get("FORGELOOP_CONFIG_HOME")
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as config_tmp:
            try:
                os.environ["FORGELOOP_CONFIG_HOME"] = config_tmp
                root = Path(tmp)
                (root / ".env.example").write_text(
                    "FORGELOOP_TEST_KEY=\nFORGELOOP_SECOND_KEY=\n",
                    encoding="utf-8",
                )

                path = init_external_secrets(root)
                status = check_secrets(root)

                self.assertFalse(root in path.resolve().parents)
                self.assertTrue(path.is_file())
                self.assertEqual(external_secrets_path(root), path)
                self.assertEqual(["FORGELOOP_TEST_KEY", "FORGELOOP_SECOND_KEY"], status.keys)
                self.assertEqual([], status.repo_env_files)
                self.assertIn("FORGELOOP_TEST_KEY=", path.read_text(encoding="utf-8"))
            finally:
                if previous is None:
                    os.environ.pop("FORGELOOP_CONFIG_HOME", None)
                else:
                    os.environ["FORGELOOP_CONFIG_HOME"] = previous

    def test_external_secrets_init_rejects_dangling_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repository"
            root.mkdir()
            (root / ".env.example").write_text("FORGELOOP_TEST_KEY=\n", encoding="utf-8")
            target = Path(tmp) / "external-secrets.env"
            target.symlink_to(Path(tmp) / "missing-target.env")

            with patch("forgeloop.secrets.external_secrets_path", return_value=target):
                with self.assertRaisesRegex(ValueError, "symlink"):
                    init_external_secrets(root)

    def test_external_secrets_path_must_be_a_regular_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repository"
            root.mkdir()
            (root / ".env.example").write_text("FORGELOOP_TEST_KEY=\n", encoding="utf-8")
            target = Path(tmp) / "external-secrets.env"
            target.mkdir()

            with patch("forgeloop.secrets.external_secrets_path", return_value=target):
                with self.assertRaisesRegex(ValueError, "regular file"):
                    init_external_secrets(root)
                status = check_secrets(root)

        self.assertFalse(status.exists)
        self.assertTrue(any("not a regular file" in warning for warning in status.warnings))

    def test_precompact_always_recommends_capture(self) -> None:
        result = simulate_hook_event(Path(__file__).resolve().parents[1], "PreCompact", {})

        self.assertEqual("remind-capture", result.action)


class MemoryIndexTests(unittest.TestCase):
    def test_memory_index_collects_records_and_writes_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/captures").mkdir(parents=True)
            (root / "docs/solutions").mkdir(parents=True)
            (root / "docs/palace/drawers").mkdir(parents=True)
            (root / "docs/palace/entities").mkdir(parents=True)
            (root / "docs/palace/timelines").mkdir(parents=True)
            (root / "docs/palace/indexes").mkdir(parents=True)
            (root / "docs/captures/2026-04-17-test.md").write_text(
                "---\ntype: capture\nstatus: current\nvalid_from: 2026-04-17\ntags: [test]\n---\n# Test Capture\n",
                encoding="utf-8",
            )

            records = collect_memory_records(root)
            result = build_memory_index(root)
            payload = json.loads(result.json_path.read_text(encoding="utf-8"))

            self.assertEqual(1, len(records))
            self.assertEqual(1, payload["record_count"])
            self.assertEqual("Test Capture", payload["records"][0]["title"])
            self.assertNotIn("generated_on", payload)
            self.assertEqual(1, payload["schema_version"])
            self.assertFalse(build_memory_index(root, check=True).changed)


class ContextPackTests(unittest.TestCase):
    def test_context_pack_returns_pointer_only_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/captures").mkdir(parents=True)
            (root / "docs/solutions").mkdir(parents=True)
            (root / "docs/palace/drawers").mkdir(parents=True)
            (root / "docs/palace/entities").mkdir(parents=True)
            (root / "docs/palace/timelines").mkdir(parents=True)
            (root / "docs/captures/2026-04-26-token-economy.md").write_text(
                "---\ntype: capture\nstatus: current\nvalid_from: 2026-04-26\n"
                "tags: [memory, token, compression]\n---\n"
                "# Token Economy\n\n"
                "Full detail that should not be copied into the compact packet.\n",
                encoding="utf-8",
            )

            payload = build_context_pack(root, "token memory compression", limit=1)
            text = render_context_pack(payload)

            self.assertEqual("FCP/1", payload["schema_version"])
            self.assertIn("measurement", payload)
            self.assertGreater(payload["measurement"]["packet_bytes"], 0)
            self.assertEqual(
                len(render_context_pack(payload).encode("utf-8")),
                payload["measurement"]["packet_bytes"],
            )
            self.assertEqual("utf8_bytes_measured_from_rendered_fcp", payload["measurement"]["method"])
            self.assertEqual(1, payload["returned"])
            self.assertIn("docs/captures/2026-04-26-token-economy.md", text)
            self.assertIn("LOSSLESS=BY_REFERENCE", text)
            self.assertIn("FCP_BYTES=", text)
            self.assertIn("SAVE_SELECTED=", text)
            self.assertNotIn("Full detail that should not be copied", text)
            self.assertTrue(is_ascii(text))

    def test_context_pack_cli_outputs_fcp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = StringIO()

        with redirect_stdout(output):
            self.assertEqual(0, main(["pack", "memory validation", str(root), "--limit", "2"]))

        text = output.getvalue()
        self.assertIn("FCP/1", text)
        self.assertIn("MODE=PTR", text)

    def test_context_pack_rejects_secret_like_queries(self) -> None:
        secret_like_query = "api_key=" + "super" + "secret" + "value" + "12345"
        with self.assertRaises(ValueError):
            build_context_pack(Path(__file__).resolve().parents[1], secret_like_query)


class CompatibilityTests(unittest.TestCase):
    def test_current_repository_reports_core_tool_compatibility(self) -> None:
        root = Path(__file__).resolve().parents[1]
        report = compatibility_report(root)
        targets = {target["tool"]: target for target in report["targets"]}

        self.assertTrue(targets["Claude Code"]["ready"])
        self.assertTrue(targets["Codex"]["ready"])
        self.assertTrue(targets["Cursor"]["ready"])
        self.assertTrue(targets["GitHub Copilot"]["ready"])
        self.assertTrue(targets["Gemini CLI / Gemini Code Assist"]["ready"])
        self.assertTrue(targets["Windsurf"]["ready"])
        self.assertTrue(targets["Cline / Roo Code"]["ready"])
        self.assertTrue(targets["OpenCode"]["ready"])
        self.assertTrue(targets["OpenCLI integrated plugin"]["ready"])

    def test_compat_cli_outputs_report(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = StringIO()

        with redirect_stdout(output):
            self.assertEqual(0, main(["compat", str(root)]))

        self.assertIn("Claude Code", output.getvalue())
        self.assertIn("Codex", output.getvalue())


class DoctorTests(unittest.TestCase):
    def test_doctor_reports_no_errors_for_current_repository(self) -> None:
        root = Path(__file__).resolve().parents[1]
        report = doctor_report(root)
        errors = [check for check in report["checks"] if check["status"] == "error"]

        self.assertEqual([], errors)
        self.assertTrue(any(check["name"] == "opencli" for check in report["checks"]))
        self.assertTrue(any(check["name"] == "release-assets" for check in report["checks"]))

    def test_doctor_cli_outputs_health_report(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = StringIO()

        with redirect_stdout(output):
            self.assertEqual(0, main(["doctor", str(root)]))

        self.assertIn("ForgeLoop doctor", output.getvalue())
        self.assertIn("opencli", output.getvalue())


class OpenCLITests(unittest.TestCase):
    def test_parse_node_major_handles_standard_versions(self) -> None:
        self.assertEqual(21, parse_node_major("v21.0.0"))
        self.assertEqual(22, parse_node_major("22.3.1"))
        self.assertIsNone(parse_node_major("not-a-version"))

    def test_parse_node_engine_major_handles_engine_ranges(self) -> None:
        self.assertEqual(20, parse_node_engine_major(">=20.0.0"))
        self.assertEqual(21, parse_node_engine_major(">= 21.0.0"))
        self.assertIsNone(parse_node_engine_major("^20.0.0"))

    def test_opencli_plan_uses_latest_package_and_local_plugin(self) -> None:
        root = Path(__file__).resolve().parents[1]
        plan = opencli_plan(root, include_skills=True, run_doctor=True)
        commands = [step["command"] for step in plan["steps"]]

        self.assertIn(["npm", "install", "-g", "@jackwener/opencli@latest"], commands)
        self.assertTrue(any(command[:3] == ["opencli", "plugin", "install"] for command in commands))
        self.assertTrue(any(command == ["npx", "skills", "add", "jackwener/opencli"] for command in commands))
        self.assertTrue(plan["status"]["plugin_source"]["exists"])

    def test_opencli_install_without_execute_is_dry_run(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = run_opencli_install(root, execute=False)

        self.assertFalse(result["executed"])
        self.assertEqual("dry-run", result["status"])

    def test_opencli_install_verifies_plugin_command_list(self) -> None:
        root = Path(__file__).resolve().parents[1]
        plan = {
            "status": {
                "node": {"ready": True},
                "npm": {"ready": True, "path": "npm"},
                "plugin_source": {"ready": True, "reason": ""},
            }
        }
        calls: list[list[str]] = []

        def run(executable: str, args: list[str], timeout: int) -> CommandRun:
            calls.append([executable, *args])
            return CommandRun([executable, *args], 0, "", "")

        with (
            patch("forgeloop.opencli.opencli_plan", return_value=plan),
            patch("forgeloop.opencli.shutil.which", return_value="opencli"),
            patch("forgeloop.opencli._run_fixed", side_effect=run),
        ):
            result = run_opencli_install(root, execute=True)

        self.assertEqual("ok", result["status"])
        self.assertEqual(
            [
                ["npm", "install", "-g", "@jackwener/opencli@latest"],
                ["opencli", "plugin", "install", str(root / "integrations/opencli")],
                ["opencli", "--version"],
                ["opencli", "list", "-f", "json"],
            ],
            calls,
        )

    def test_opencli_install_stops_when_plugin_install_fails(self) -> None:
        root = Path(__file__).resolve().parents[1]
        plan = {
            "status": {
                "node": {"ready": True},
                "npm": {"ready": True, "path": "npm"},
                "plugin_source": {"ready": True, "reason": ""},
            }
        }
        calls: list[list[str]] = []

        def run(executable: str, args: list[str], timeout: int) -> CommandRun:
            calls.append([executable, *args])
            exit_code = 1 if args[:2] == ["plugin", "install"] else 0
            return CommandRun([executable, *args], exit_code, "", "")

        with (
            patch("forgeloop.opencli.opencli_plan", return_value=plan),
            patch("forgeloop.opencli.shutil.which", return_value="opencli"),
            patch("forgeloop.opencli._run_fixed", side_effect=run),
        ):
            result = run_opencli_install(root, execute=True)

        self.assertEqual("failed", result["status"])
        self.assertEqual(2, len(calls))

    def test_opencli_status_rejects_symlinked_plugin_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repository"
            source = Path(tmp) / "outside-plugin"
            (root / "integrations").mkdir(parents=True)
            source.mkdir()
            (source / "opencli-plugin.json").write_text("{}\n", encoding="utf-8")
            (root / "integrations/opencli").symlink_to(source, target_is_directory=True)

            with patch("forgeloop.opencli.shutil.which", return_value=None):
                status = opencli_status(root)

        self.assertFalse(status["plugin_source"]["ready"])
        self.assertIn("symlinks", status["plugin_source"]["reason"])

    def test_opencli_status_cli_outputs_package(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = StringIO()

        with redirect_stdout(output):
            self.assertEqual(0, main(["opencli", "status", str(root)]))

        self.assertIn("@jackwener/opencli@latest", output.getvalue())

    def test_opencli_status_default_does_not_fetch_registry_metadata(self) -> None:
        root = Path(__file__).resolve().parents[1]
        status = opencli_status(root)

        self.assertFalse(status["registry"]["checked"])

    def test_opencli_plan_cli_outputs_plan(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = StringIO()

        with redirect_stdout(output):
            self.assertEqual(0, main(["opencli", "plan", str(root), "--with-skills"]))

        self.assertIn("ForgeLoop OpenCLI integration plan", output.getvalue())
        self.assertIn("npx skills add jackwener/opencli", output.getvalue())


class SetupMenuTests(unittest.TestCase):
    def test_setup_menu_lists_supported_and_coming_soon_tools(self) -> None:
        menu = setup_menu_text()

        self.assertIn("Claude Code", menu)
        self.assertIn("Codex", menu)
        self.assertIn("Cursor", menu)
        self.assertIn("GitHub Copilot", menu)
        self.assertIn("Windsurf", menu)
        self.assertIn("OpenCode", menu)
        self.assertIn("Coming soon", menu)
        self.assertIn("Amazon Q", menu)

    def test_setup_cli_dry_run_selects_codex_without_writing(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = StringIO()

        with redirect_stdout(output):
            self.assertEqual(0, main(["setup", str(root), "--tool", "codex", "--dry-run"]))

        self.assertIn("Selected: Codex", output.getvalue())
        self.assertFalse((root / ".forgeloop.local.json").exists())

    def test_setup_interactive_selection_can_choose_all_supported(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = StringIO()
        all_choice = str(len(SUPPORTED_TOOLS) + 1)

        with redirect_stdout(output):
            result = run_setup(root, dry_run=True, input_func=lambda _prompt: all_choice)

        self.assertEqual(ALL_SUPPORTED_ID, result.selected_tool)
        self.assertFalse(result.missing_files)
        self.assertIn("All supported tools", output.getvalue())

    def test_setup_writes_local_profile_when_not_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
            (root / "README.md").write_text("# Readme\n", encoding="utf-8")
            (root / "docs/HOW_TO_USE.md").write_text("# How to use\n", encoding="utf-8")

            result = run_setup(root, tool_id="codex")
            payload = json.loads((root / ".forgeloop.local.json").read_text(encoding="utf-8"))

            self.assertTrue(result.wrote_config)
            self.assertEqual("codex", payload["selected_tool"])


class TokenReportTests(unittest.TestCase):
    def test_token_report_measures_packet_against_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/captures").mkdir(parents=True)
            (root / "docs/solutions").mkdir(parents=True)
            (root / "docs/palace/drawers").mkdir(parents=True)
            (root / "docs/palace/entities").mkdir(parents=True)
            (root / "docs/palace/timelines").mkdir(parents=True)
            (root / "docs/captures/2026-05-02-token.md").write_text(
                "---\ntype: capture\nstatus: current\nvalid_from: 2026-05-02\n"
                "tags: [token, report]\n---\n"
                "# Token Report\n\n"
                "A reusable token measurement note.\n",
                encoding="utf-8",
            )

            report = build_token_report(root, "token report", limit=1, tool_id="codex")
            text = format_token_report(report)

            self.assertEqual(1, report["returned_records"])
            self.assertEqual("codex", report["tool_reports"][0]["tool"])
            self.assertGreater(report["tool_reports"][0]["packet_tokens"], 0)
            self.assertIn("exact", report["tool_reports"][0])
            self.assertIn("ForgeLoop token report", text)

    def test_tokens_cli_outputs_report(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = StringIO()

        with redirect_stdout(output):
            self.assertEqual(0, main(["tokens", "memory validation", str(root), "--tool", "codex", "--limit", "2"]))

        text = output.getvalue()
        self.assertIn("ForgeLoop token report", text)
        self.assertIn("Codex", text)


if __name__ == "__main__":
    unittest.main()
