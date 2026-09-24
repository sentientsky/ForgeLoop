from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from zipfile import ZipFile

from forgeloop.adoption import _is_link_like, _validated_relative_path, adopt_into_repo
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
from forgeloop.governance import (
    audit_governed_memory,
    record_audit_event,
    verify_audit_log,
)
from forgeloop.opencli import (
    CommandRun,
    opencli_plan,
    opencli_status,
    parse_node_engine_major,
    parse_node_major,
    run_opencli_install,
)
from forgeloop.release_archive import forbidden_source_paths
from forgeloop.release_archive import main as check_release_archive
from forgeloop.secrets import (
    check_secrets,
    external_secrets_path,
    init_external_secrets,
    parse_env_keys,
)
from forgeloop.setup import (
    ALL_SUPPORTED_ID,
    SUPPORTED_TOOLS,
    run_setup,
    setup_menu_text,
)
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

    def test_governance_erase_requires_opaque_evidence_and_hashes_it(self) -> None:
        from forgeloop import governance

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repository"
            root.mkdir()
            with patch.dict(os.environ, {"FORGELOOP_GOVERNANCE_HOME": str(base / "config")}):
                with self.assertRaisesRegex(ValueError, "requires an opaque reference"):
                    record_audit_event(
                        root,
                        action="erase",
                        actor_ref="OPERATOR-001",
                        record_ref="STORE-EXTERNAL-001",
                    )
                with self.assertRaisesRegex(ValueError, "opaque upper-case identifier"):
                    record_audit_event(
                        root,
                        action="erase",
                        actor_ref="OPERATOR-001",
                        record_ref="STORE-EXTERNAL-001",
                        evidence_ref="evidence@example.com",
                    )
                with self.assertRaisesRegex(ValueError, "only accepted for an erase event"):
                    record_audit_event(
                        root,
                        action="access",
                        actor_ref="OPERATOR-001",
                        record_ref="STORE-EXTERNAL-001",
                        evidence_ref="EVIDENCE-PACKET-001",
                    )
                event = record_audit_event(
                    root,
                    action="erase",
                    actor_ref="OPERATOR-001",
                    record_ref="STORE-EXTERNAL-001",
                    evidence_ref="EVIDENCE-PACKET-001",
                )
                status = verify_audit_log(root)
                audit_log = next((base / "config/governance/audit").glob("*.jsonl"))
                raw_log = audit_log.read_text(encoding="utf-8")
                stored_event = json.loads(raw_log)

        self.assertTrue(event["recorded"])
        self.assertTrue(status["valid"])
        self.assertEqual(governance._hash_reference("evidence", "EVIDENCE-PACKET-001"), stored_event["evidence_ref_hash"])
        self.assertNotIn("EVIDENCE-PACKET-001", raw_log)

    def test_governance_log_verifies_legacy_events_before_appending_v2(self) -> None:
        from forgeloop import governance

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repository"
            root.mkdir()
            with patch.dict(os.environ, {"FORGELOOP_GOVERNANCE_HOME": str(base / "config")}):
                legacy_event = {
                    "schema_version": "FGA/1",
                    "event_id": "AUD-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "occurred_at": "2026-01-01T00:00:00Z",
                    "action": "collect",
                    "actor_ref_hash": governance._hash_reference("actor", "OPERATOR-001"),
                    "record_ref_hash": governance._hash_reference("record", "STORE-EXTERNAL-001"),
                    "subject_ref_hash": "",
                    "previous_event_hash": "",
                }
                legacy_event["event_hash"] = governance._hash_event(legacy_event)
                audit_log = governance._audit_log_path(root.resolve())
                audit_log.parent.mkdir(parents=True)
                audit_log.write_text(json.dumps(legacy_event) + "\n", encoding="utf-8")

                self.assertTrue(verify_audit_log(root)["valid"])
                record_audit_event(
                    root,
                    action="access",
                    actor_ref="OPERATOR-001",
                    record_ref="STORE-EXTERNAL-001",
                )
                status = verify_audit_log(root)

        self.assertTrue(status["valid"])
        self.assertEqual(2, status["event_count"])

    def test_governance_verifier_reports_malformed_action_type_without_crashing(self) -> None:
        from forgeloop import governance

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repository"
            root.mkdir()
            with patch.dict(os.environ, {"FORGELOOP_GOVERNANCE_HOME": str(base / "config")}):
                audit_log = governance._audit_log_path(root.resolve())
                audit_log.parent.mkdir(parents=True)
                malformed_event = {
                    "schema_version": "FGA/2",
                    "event_id": "AUD-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "occurred_at": "2026-01-01T00:00:00Z",
                    "action": [],
                    "actor_ref_hash": "a" * 64,
                    "record_ref_hash": "b" * 64,
                    "subject_ref_hash": "",
                    "evidence_ref_hash": "",
                    "previous_event_hash": "",
                    "event_hash": "c" * 64,
                }
                audit_log.write_text(json.dumps(malformed_event) + "\n", encoding="utf-8")

                status = verify_audit_log(root)

        self.assertFalse(status["valid"])
        self.assertIn("unsupported action", status["reason"])

    def test_governance_erase_cli_refuses_to_record_without_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repository"
            root.mkdir()
            output = StringIO()
            error = StringIO()
            with (
                patch.dict(os.environ, {"FORGELOOP_GOVERNANCE_HOME": str(base / "config")}),
                redirect_stdout(output),
                redirect_stderr(error),
            ):
                result = main(
                    [
                        "governance",
                        "log",
                        "erase",
                        str(root),
                        "--actor-ref",
                        "OPERATOR-001",
                        "--record-ref",
                        "STORE-EXTERNAL-001",
                    ]
                )

        self.assertEqual(1, result)
        self.assertIn("requires an opaque reference", error.getvalue())
        self.assertEqual("", output.getvalue())

    def test_governance_log_refuses_personal_identifiers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
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
            with (
                patch.dict(os.environ, {"FORGELOOP_GOVERNANCE_HOME": str(root)}),
                self.assertRaises(ValueError),
            ):
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

    def test_validation_requires_scorecard_write_permissions_at_job_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workflow = Path(tmp) / ".github/workflows/scorecard.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text(
                "name: Scorecard\n"
                "permissions:\n"
                "  contents: read\n"
                "  security-events: write\n"
                "  id-token: write\n"
                "jobs:\n"
                "  analysis:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps: []\n",
                encoding="utf-8",
            )

            findings = validate_repo(Path(tmp))

        self.assertIn(
            "scorecard-global-write-permissions",
            {finding.code for finding in findings},
        )

    def test_validation_requires_codeql_write_permissions_at_job_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workflow = Path(tmp) / ".github/workflows/codeql.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text(
                "name: CodeQL\n"
                "permissions:\n"
                "  contents: read\n"
                "  security-events: write\n"
                "jobs:\n"
                "  analyse:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps: []\n",
                encoding="utf-8",
            )

            findings = validate_repo(Path(tmp))

        self.assertIn(
            "codeql-global-write-permissions",
            {finding.code for finding in findings},
        )


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
            temp_root = Path(tmp).resolve()
            root = temp_root / "repository"
            root.mkdir()
            (root / ".env.example").write_text("FORGELOOP_TEST_KEY=\n", encoding="utf-8")
            target = temp_root / "external-secrets.env"
            target.symlink_to(temp_root / "missing-target.env")

            with (
                patch("forgeloop.secrets.external_secrets_path", return_value=target),
                self.assertRaisesRegex(ValueError, "symlink"),
            ):
                init_external_secrets(root)

    def test_external_secrets_path_must_be_a_regular_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp).resolve()
            root = temp_root / "repository"
            root.mkdir()
            (root / ".env.example").write_text("FORGELOOP_TEST_KEY=\n", encoding="utf-8")
            target = temp_root / "external-secrets.env"
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
    def test_missing_repository_profiles_are_not_reported_as_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = compatibility_report(Path(temp_dir))

        self.assertEqual(2, report["schema_version"])
        self.assertFalse(report["targets"][0]["profile_files_present"])

    def test_current_repository_reports_core_tool_compatibility(self) -> None:
        root = Path(__file__).resolve().parents[1]
        report = compatibility_report(root)
        targets = {target["tool"]: target for target in report["targets"]}

        self.assertTrue(targets["Claude Code"]["profile_files_present"])
        self.assertTrue(targets["Codex"]["profile_files_present"])
        self.assertTrue(targets["Cursor"]["profile_files_present"])
        self.assertTrue(targets["GitHub Copilot"]["profile_files_present"])
        self.assertTrue(targets["Gemini CLI / Gemini Code Assist"]["profile_files_present"])
        self.assertTrue(targets["Windsurf"]["profile_files_present"])
        self.assertTrue(targets["Cline / Roo Code"]["profile_files_present"])
        self.assertTrue(targets["OpenCode"]["profile_files_present"])
        self.assertTrue(targets["OpenCLI integrated plugin"]["profile_files_present"])

    def test_release_workflow_limits_tags_to_protected_main_history(self) -> None:
        workflow = Path(__file__).resolve().parents[1] / ".github/workflows/release.yml"
        text = workflow.read_text(encoding="utf-8")

        self.assertIn("fetch-depth: 0", text)
        self.assertIn('git merge-base --is-ancestor "$GITHUB_SHA" origin/main', text)
        self.assertIn("dist/*-source.zip.sha256", text)
        self.assertIn("sha256sum", text)

    def test_compat_cli_outputs_report(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = StringIO()

        with redirect_stdout(output):
            self.assertEqual(0, main(["compat", str(root)]))

        self.assertIn("Claude Code", output.getvalue())
        self.assertIn("Codex", output.getvalue())
        self.assertIn("does not verify behaviour inside the external tool", output.getvalue())


class ReleaseArchiveTests(unittest.TestCase):
    def test_source_archive_check_allows_example_env_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = Path(temp_dir) / "source.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("ForgeLoop/.env.example", "EXAMPLE=value\n")
                archive.writestr("ForgeLoop/README.md", "safe\n")

            self.assertEqual([], forbidden_source_paths(archive_path))

    def test_source_archive_check_rejects_local_secret_files_case_insensitively(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = Path(temp_dir) / "source.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("ForgeLoop/.ENV.production", "secret")
                archive.writestr("ForgeLoop/production.env", "secret")
                archive.writestr("ForgeLoop/.forgeloop.local.json", "{}")
                archive.writestr("ForgeLoop/.claude/settings.local.json", "{}")
                archive.writestr("ForgeLoop/.npmrc", "//registry.npmjs.org/:_authToken=secret")
                archive.writestr("ForgeLoop/.aws/credentials", "secret")
                archive.writestr("ForgeLoop/.ssh/id_ecdsa", "private key")
                archive.writestr("ForgeLoop/keys/deploy.PEM", "private key")

            self.assertEqual(
                [
                    "ForgeLoop/.ENV.production",
                    "ForgeLoop/production.env",
                    "ForgeLoop/.forgeloop.local.json",
                    "ForgeLoop/.claude/settings.local.json",
                    "ForgeLoop/.npmrc",
                    "ForgeLoop/.aws/credentials",
                    "ForgeLoop/.ssh/id_ecdsa",
                    "ForgeLoop/keys/deploy.PEM",
                ],
                forbidden_source_paths(archive_path),
            )

    def test_source_archive_cli_returns_nonzero_for_local_secret_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = Path(temp_dir) / "source.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("ForgeLoop/secrets.env", "secret")
            output = StringIO()
            with redirect_stdout(output):
                result = check_release_archive([str(archive_path)])

        self.assertEqual(1, result)
        self.assertIn("1 local-only file", output.getvalue())
        self.assertNotIn("secrets.env", output.getvalue())

    def test_source_archive_cli_rejects_invalid_zip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = Path(temp_dir) / "invalid.zip"
            archive_path.write_text("not a zip", encoding="utf-8")
            errors = StringIO()

            with redirect_stderr(errors), self.assertRaises(SystemExit) as error:
                check_release_archive([str(archive_path)])

        self.assertEqual(2, error.exception.code)
        self.assertIn("Could not read the source ZIP archive", errors.getvalue())


class DoctorTests(unittest.TestCase):
    def test_doctor_reports_no_errors_for_current_repository(self) -> None:
        root = Path(__file__).resolve().parents[1]
        report = doctor_report(root)
        errors = [check for check in report["checks"] if check["status"] == "error"]

        self.assertEqual([], errors)
        self.assertTrue(any(check["name"] == "opencli" for check in report["checks"]))
        release_check = next(check for check in report["checks"] if check["name"] == "release-readiness-files")
        self.assertIn("published GitHub releases are not checked", release_check["message"])

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
        self.assertIn("Claude Code [primary]", menu)
        self.assertIn("Codex", menu)
        self.assertIn("Codex [primary]", menu)
        self.assertIn("does not install or merge files", menu)
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
        self.assertIn("does not install or merge profile files", output.getvalue())
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


class AdoptionTests(unittest.TestCase):
    def _source_tree(self, root: Path) -> None:
        files = {
            "AGENTS.md": "# ForgeLoop agent rules\n",
            "docs/HOW_TO_USE.md": "# Workflow guide\n",
        }
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def test_adoption_previews_then_adds_missing_files_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "source"
            destination = base / "destination"
            source.mkdir()
            destination.mkdir()
            self._source_tree(source)
            (destination / "AGENTS.md").write_text("# User-owned instructions\n", encoding="utf-8")

            preview = adopt_into_repo(source, destination, "codex")
            self.assertTrue(preview.dry_run)
            self.assertEqual("conflict", preview.entries[0].action)
            self.assertFalse((destination / "docs/HOW_TO_USE.md").exists())

            applied = adopt_into_repo(source, destination, "codex", apply=True)
            self.assertFalse(applied.dry_run)
            self.assertEqual(["docs/HOW_TO_USE.md"], [entry.path for entry in applied.entries if entry.action == "created"])
            self.assertEqual("# User-owned instructions\n", (destination / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertEqual("# Workflow guide\n", (destination / "docs/HOW_TO_USE.md").read_text(encoding="utf-8"))

            repeated = adopt_into_repo(source, destination, "codex", apply=True)
            self.assertEqual(1, sum(entry.action == "unchanged" for entry in repeated.entries))
            self.assertEqual(1, len(repeated.conflicts))

    def test_adoption_rejects_symlinked_destination_components(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "source"
            destination = base / "destination"
            outside = base / "outside"
            source.mkdir()
            destination.mkdir()
            outside.mkdir()
            self._source_tree(source)
            try:
                (destination / "docs").symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlinks unavailable: {exc}")

            with self.assertRaisesRegex(ValueError, "symlink"):
                adopt_into_repo(source, destination, "codex", apply=True)
            self.assertFalse((destination / "AGENTS.md").exists())
            self.assertFalse((outside / "HOW_TO_USE.md").exists())

    def test_failed_adoption_rolls_back_files_and_directories_it_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "source"
            destination = base / "destination"
            source.mkdir()
            destination.mkdir()
            self._source_tree(source)

            from forgeloop import adoption

            create_file = adoption._create_file_exclusive
            calls = 0

            def fail_on_last_file(path: Path, content: bytes) -> bool:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("simulated write failure")
                return create_file(path, content)

            with (
                patch("forgeloop.adoption._create_file_exclusive", side_effect=fail_on_last_file),
                self.assertRaisesRegex(OSError, "simulated write failure"),
            ):
                adopt_into_repo(source, destination, "codex", apply=True)

            self.assertFalse((destination / "AGENTS.md").exists())
            self.assertFalse((destination / "docs/HOW_TO_USE.md").exists())
            self.assertFalse((destination / "docs").exists())

    def test_adoption_cli_defaults_to_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            output = StringIO()

            with (
                patch("forgeloop.cli.adoption_source_root", return_value=Path(__file__).resolve().parents[1]),
                redirect_stdout(output),
            ):
                self.assertEqual(0, main(["adopt", str(destination), "--tool", "codex"]))

            self.assertIn("Preview only", output.getvalue())
            self.assertFalse((destination / "AGENTS.md").exists())

    def test_adoption_rejects_traversal_and_cross_platform_absolute_paths(self) -> None:
        for value in ("../outside.md", "docs/../outside.md", "C:/outside.md", "docs//guide.md", "docs/./guide.md"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                _validated_relative_path(value)

    def test_adoption_refuses_a_destination_inside_the_source_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            destination = source / "nested"
            destination.mkdir()

            with self.assertRaisesRegex(ValueError, "inside the ForgeLoop source"):
                adopt_into_repo(source, destination, "codex")

    def test_adoption_rejects_windows_reparse_points(self) -> None:
        candidate = SimpleNamespace(
            is_symlink=lambda: False,
            is_junction=lambda: False,
            lstat=lambda: SimpleNamespace(st_file_attributes=0x400),
        )

        self.assertTrue(_is_link_like(candidate))


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
