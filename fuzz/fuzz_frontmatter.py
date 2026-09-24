from __future__ import annotations

import sys
from pathlib import Path

import atheris

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

with atheris.instrument_imports():
    from forgeloop.core import parse_frontmatter


def test_one_input(data: bytes) -> None:
    text = data[:65536].decode("utf-8", errors="replace")
    metadata, body = parse_frontmatter(text)
    if not isinstance(metadata, dict) or not isinstance(body, str):
        raise TypeError("frontmatter parser returned an invalid result")
    lines = text.splitlines()
    if (not lines or lines[0].strip() != "---") and (metadata or body != text):
        raise AssertionError("text without an opening delimiter must remain unchanged")


atheris.Setup(sys.argv, test_one_input)
atheris.Fuzz()
