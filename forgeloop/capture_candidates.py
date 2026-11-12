from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import uuid
from datetime import date
from pathlib import Path

from .core import _contains_secret, slugify

MAX_CANDIDATE_BYTES = 20_000
_ID_RE = re.compile(r"^[a-f0-9]{32}$")


def propose_candidate(root: Path, title: str, body: str) -> dict[str, str]:
    root = root.resolve()
    title = " ".join(title.split())
    body = body.strip()
    if not title or len(title) > 160:
        raise ValueError("Candidate title must contain 1 to 160 characters")
    if not body or len(body.encode("utf-8")) > MAX_CANDIDATE_BYTES:
        raise ValueError(f"Candidate body must contain 1 to {MAX_CANDIDATE_BYTES} bytes")
    if _contains_secret(title + "\n" + body):
        raise ValueError("Candidate appears to contain a secret")
    directory = root / ".forgeloop-candidates"
    if _is_link_like(directory):
        raise ValueError("Refusing to use a symlinked candidate directory")
    directory.mkdir(mode=0o700, exist_ok=True)
    if _is_link_like(directory):
        raise ValueError("Refusing to use a symlinked candidate directory")
    if os.name == "posix":
        directory.chmod(0o700)
    candidate_id = uuid.uuid4().hex
    path = directory / f"{candidate_id}.json"
    payload = {"id": candidate_id, "title": title, "body": body, "status": "pending"}
    _write_new(path, json.dumps(payload, ensure_ascii=True, indent=2) + "\n", mode=0o600)
    return {"id": candidate_id, "path": str(path.relative_to(root)), "status": "pending"}


def inspect_candidate(root: Path, candidate_id: str) -> dict[str, str]:
    candidate = _read_candidate(root, candidate_id)
    candidate["fingerprint"] = _fingerprint(candidate)
    return candidate


def approve_candidate(root: Path, candidate_id: str, expected_fingerprint: str) -> dict[str, str]:
    root = root.resolve()
    candidate = _read_candidate(root, candidate_id)
    if candidate["status"] != "pending":
        raise ValueError("Only pending candidates can be approved")
    if not expected_fingerprint or not hmac.compare_digest(
        _fingerprint(candidate), expected_fingerprint
    ):
        raise ValueError("Candidate changed since review; inspect it again before approval")
    content = (
        "---\n"
        "type: capture\n"
        "status: current\n"
        f"valid_from: {date.today().isoformat()}\n"
        "tags: [reviewed-candidate]\n"
        "---\n\n"
        f"# {candidate['title']}\n\n{candidate['body']}\n"
    )
    if _contains_secret(content):
        raise ValueError("Candidate appears to contain a secret")
    output_dir = root / "docs" / "captures"
    if _is_link_like(root / "docs") or _is_link_like(output_dir):
        raise ValueError("Refusing to write into a symlinked capture directory")
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{date.today().isoformat()}-{slugify(candidate['title'])}.md"
    _write_new(output, content)
    candidate_path = root / ".forgeloop-candidates" / f"{candidate_id}.json"
    if _is_link_like(candidate_path):
        raise ValueError("Refusing to update a symlinked candidate")
    candidate["status"] = "approved"
    candidate["saved_to"] = str(output.relative_to(root))
    candidate_path.write_text(json.dumps(candidate, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return {"id": candidate_id, "status": "approved", "saved_to": str(output.relative_to(root))}


def _fingerprint(candidate: dict[str, str]) -> str:
    reviewed = {key: candidate[key] for key in ("id", "title", "body", "status")}
    encoded = json.dumps(reviewed, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _read_candidate(root: Path, candidate_id: str) -> dict[str, str]:
    if not _ID_RE.fullmatch(candidate_id):
        raise ValueError("Candidate ID must be a 32-character lowercase hex ID")
    directory = root.resolve() / ".forgeloop-candidates"
    if _is_link_like(directory):
        raise ValueError("Refusing to read from a symlinked candidate directory")
    path = directory / f"{candidate_id}.json"
    if _is_link_like(path) or not path.is_file():
        raise FileNotFoundError("Capture candidate not found")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("id") != candidate_id or not isinstance(payload.get("title"), str) or not isinstance(payload.get("body"), str):
        raise ValueError("Capture candidate is invalid")
    return payload


def _write_new(path: Path, content: str, mode: int = 0o644) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags, mode)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
    except FileExistsError:
        raise ValueError("Refusing to overwrite an existing file") from None


def _is_link_like(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())
