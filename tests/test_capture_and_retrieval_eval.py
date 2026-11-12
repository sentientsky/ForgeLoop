from __future__ import annotations

import os
import stat
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from forgeloop.beads import beads_ready
from forgeloop.capture_candidates import (
    approve_candidate,
    inspect_candidate,
    propose_candidate,
)
from forgeloop.cli import main
from forgeloop.context import build_context_pack


class CaptureCandidateTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "posix", "POSIX permission bits are not portable to Windows ACLs")
    def test_candidate_storage_is_owner_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            candidate = propose_candidate(root, "Private draft", "Short reusable lesson.")
            directory_mode = stat.S_IMODE((root / ".forgeloop-candidates").stat().st_mode)
            file_mode = stat.S_IMODE((root / candidate["path"]).stat().st_mode)
        self.assertEqual(0o700, directory_mode)
        self.assertEqual(0o600, file_mode)

    def test_candidate_requires_explicit_approval_before_memory_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            candidate = propose_candidate(root, "Retry guidance", "Retry transient errors with bounded backoff.")
            self.assertEqual("pending", candidate["status"])
            self.assertFalse((root / "docs/captures").exists())
            reviewed = inspect_candidate(root, candidate["id"])
            self.assertEqual("pending", reviewed["status"])

            result = approve_candidate(root, candidate["id"], reviewed["fingerprint"])

            self.assertEqual("approved", result["status"])
            saved = root / result["saved_to"]
            self.assertIn("bounded backoff", saved.read_text(encoding="utf-8"))
            self.assertEqual("approved", inspect_candidate(root, candidate["id"])["status"])
            with self.assertRaises(ValueError):
                approve_candidate(root, candidate["id"], reviewed["fingerprint"])

    def test_candidate_rejects_secret_patterns_and_invalid_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ValueError, "secret"):
                propose_candidate(root, "Credential", "token=ghp_" + "a" * 30)
            with self.assertRaisesRegex(ValueError, "ID"):
                inspect_candidate(root, "../outside")

    def test_review_fingerprint_rejects_changed_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            candidate = propose_candidate(root, "Retry guidance", "Use bounded retry.")
            reviewed = inspect_candidate(root, candidate["id"])
            path = root / candidate["path"]
            path.write_text(path.read_text(encoding="utf-8").replace("bounded", "unbounded"), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "changed since review"):
                approve_candidate(root, candidate["id"], reviewed["fingerprint"])
            self.assertFalse((root / "docs/captures").exists())

    def test_cli_reads_candidate_body_from_stdin(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "capture.json"
            with patch("sys.stdin") as stdin, patch("builtins.print", side_effect=lambda value: output.write_text(value)):
                stdin.read.return_value = "A useful, reviewed lesson."
                status = main(["capture-candidate", "propose", "A lesson", "--root", temp])
            self.assertEqual(0, status)
            self.assertEqual("pending", __import__("json").loads(output.read_text())["status"])

    def test_candidate_refuses_symlinked_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            candidate = propose_candidate(root, "Safe note", "A reviewed, reusable lesson.")
            outside = root / "outside"
            outside.mkdir()
            captures = root / "docs/captures"
            captures.parent.mkdir()
            try:
                captures.symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Directory symlinks are unavailable")
            with self.assertRaisesRegex(ValueError, "symlink"):
                reviewed = inspect_candidate(root, candidate["id"])
                approve_candidate(root, candidate["id"], reviewed["fingerprint"])
            self.assertEqual([], list(outside.iterdir()))


class RetrievalEvaluationBaselineTests(unittest.TestCase):
    """Hand-labelled miniature relevance set guarding the existing ranker."""

    def test_known_queries_retrieve_the_labelled_relevant_note_first(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            captures = root / "docs/captures"
            captures.mkdir(parents=True)
            notes = {
                "retry-policy.md": ("Retry policy", "[retries, resilience]", "Use bounded backoff for transient network errors."),
                "memory-index.md": ("Memory index", "[memory, retrieval]", "Build a compact index of project notes."),
                "release-review.md": ("Release review", "[release, review]", "Verify tests and package artifacts before release."),
            }
            for filename, (title, tags, body) in notes.items():
                (captures / filename).write_text(
                    f"---\ntype: capture\nstatus: current\ntags: {tags}\n---\n# {title}\n\n{body}\n",
                    encoding="utf-8",
                )

            labelled_cases = [
                ("transient network retries backoff", "docs/captures/retry-policy.md"),
                ("memory note retrieval index", "docs/captures/memory-index.md"),
                ("release package tests review", "docs/captures/release-review.md"),
            ]
            reciprocal_ranks = []
            for query, relevant_path in labelled_cases:
                results = build_context_pack(root, query, limit=3)["records"]
                ranks = [index for index, record in enumerate(results, 1) if record["path"] == relevant_path]
                reciprocal_ranks.append(1 / ranks[0] if ranks else 0)

            self.assertGreaterEqual(sum(reciprocal_ranks) / len(reciprocal_ranks), 1.0)


class BeadsReadOnlyBridgeTests(unittest.TestCase):
    def test_ready_uses_bounded_json_read_without_claim_or_shell(self) -> None:
        completed = SimpleNamespace(returncode=0, stdout='[{"id":"bd-1","title":"Test"}]', stderr="")
        with patch("forgeloop.beads.shutil.which", return_value="C:/tools/bd.exe"), patch(
            "forgeloop.beads.subprocess.run", return_value=completed
        ) as run:
            result = beads_ready(Path.cwd(), limit=7)

        self.assertEqual("read-only", result["mode"])
        self.assertEqual("bd-1", result["items"][0]["id"])
        command = run.call_args.args[0]
        self.assertEqual(["C:/tools/bd.exe", "ready", "--json", "--brief", "--limit", "7"], command)
        self.assertNotIn("--claim", command)
        self.assertFalse(run.call_args.kwargs["shell"])
        self.assertEqual(10, run.call_args.kwargs["timeout"])

    def test_ready_rejects_invalid_limits_json_and_missing_cli(self) -> None:
        with self.assertRaises(ValueError):
            beads_ready(Path.cwd(), 0)
        with patch("forgeloop.beads.shutil.which", return_value=None), self.assertRaisesRegex(
            FileNotFoundError, "will not install"
        ):
            beads_ready(Path.cwd())
        with patch("forgeloop.beads.shutil.which", return_value="bd"), patch(
            "forgeloop.beads.subprocess.run",
            return_value=SimpleNamespace(returncode=0, stdout="not-json", stderr=""),
        ), self.assertRaisesRegex(ValueError, "invalid JSON"):
            beads_ready(Path.cwd())


if __name__ == "__main__":
    unittest.main()
