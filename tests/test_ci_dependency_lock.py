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


if __name__ == "__main__":
    unittest.main()
