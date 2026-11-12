from __future__ import annotations

import re
import unittest
from pathlib import Path


class CiDependencyLockTests(unittest.TestCase):
    def test_windows_keyring_backend_is_explicit_and_hash_locked(self) -> None:
        root = Path(__file__).resolve().parents[1]
        requirements_in = (root / ".github/requirements-ci.in").read_text(encoding="utf-8")
        requirements_lock = (root / ".github/requirements-ci.txt").read_text(encoding="utf-8")

        self.assertRegex(
            requirements_in,
            r"(?m)^pywin32-ctypes>=0\.2\.3;\s*sys_platform == 'win32'$",
        )
        self.assertRegex(
            requirements_lock,
            r"(?m)^pywin32-ctypes==0\.2\.3 ; .*sys_platform == 'win32' \\\s*$",
        )
        locked_entry = requirements_lock.split("pywin32-ctypes==0.2.3", maxsplit=1)[1].split(
            "\nreadme-renderer==", maxsplit=1
        )[0]
        self.assertEqual(2, len(re.findall(r"--hash=sha256:[0-9a-f]{64}", locked_entry)))

    def test_python_310_tomli_dependency_is_explicit_and_hash_locked(self) -> None:
        root = Path(__file__).resolve().parents[1]
        requirements_in = (root / ".github/requirements-ci.in").read_text(encoding="utf-8")
        requirements_lock = (root / ".github/requirements-ci.txt").read_text(encoding="utf-8")

        self.assertRegex(requirements_in, r"(?m)^tomli>=1\.1\.0;\s*python_version < '3\.11'$")
        self.assertRegex(
            requirements_lock,
            r"(?m)^tomli==[^\s;]+ ; .*python_full_version .*\\\s*$",
        )
        lock_lines = requirements_lock.splitlines()
        tomli_index = next(i for i, line in enumerate(lock_lines) if line.startswith("tomli=="))
        tomli_hashes = 0
        for line in lock_lines[tomli_index + 1 :]:
            if not line.startswith("    --hash=sha256:"):
                break
            tomli_hashes += 1
        self.assertGreaterEqual(tomli_hashes, 2)

    def test_codeql_init_and_analyze_use_the_same_pinned_release(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/codeql.yml").read_text(encoding="utf-8")
        actions = re.findall(
            r"(?m)^\s*- uses: github/codeql-action/(init|analyze)@([0-9a-f]{40}) # (v\d+\.\d+\.\d+)$",
            workflow,
        )

        self.assertEqual({"init", "analyze"}, {name for name, _, _ in actions})
        self.assertEqual(1, len({sha for _, sha, _ in actions}))
        self.assertEqual(1, len({version for _, _, version in actions}))


if __name__ == "__main__":
    unittest.main()
