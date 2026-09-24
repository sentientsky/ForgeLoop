from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import time
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .core import MAX_FILE_BYTES, MEMORY_FOLDERS, parse_frontmatter

AUDIT_SCHEMA_VERSION = "FGA/2"
LEGACY_AUDIT_SCHEMA_VERSION = "FGA/1"
MAX_AUDIT_LOG_BYTES = 5_000_000
MAX_AUDIT_LINE_BYTES = 16_000
ALLOWED_ACTIONS = {"collect", "access", "update", "export", "share", "erase", "retention-review"}
ALLOWED_CLASSIFICATIONS = {"public", "internal", "personal", "special-category"}
ALLOWED_LAWFUL_BASES = {
    "consent",
    "contract",
    "legal-obligation",
    "vital-interests",
    "public-task",
    "legitimate-interests",
}
ALLOWED_PROVENANCE_SOURCES = {"user-provided", "system-observed", "human-review", "derived", "imported"}
OPAQUE_REFERENCE_RE = re.compile(r"^[A-Z][A-Z0-9_-]{2,63}$")
JURISDICTION_RE = re.compile(r"^(?:[A-Z]{2}|EEA|GLOBAL)$")
AUDIT_EVENT_ID_RE = re.compile(r"^AUD-[A-F0-9]{32}$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
PERSONAL_DATA_HINT_RE = re.compile(
    r"(?i)(?:\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|"
    r"\b(?:token|password|secret|api[_ -]?key)\s*[:=])"
)


def audit_governed_memory(root: Path, today: date | None = None) -> dict[str, Any]:
    """Validate governance metadata without exporting or indexing note contents."""
    root = root.resolve()
    current_day = today or datetime.now(timezone.utc).date()
    findings: list[dict[str, str]] = []
    governed_records = 0

    for folder in MEMORY_FOLDERS:
        base = root / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.is_symlink() or path.name.upper() == "README.MD":
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    findings.append(_finding("error", path, "file-too-large", "Governed memory file exceeds the size limit.", root=root))
                    continue
                text = path.read_text(encoding="utf-8")
            except OSError:
                findings.append(_finding("error", path, "file-unreadable", "Governed memory file could not be read.", root=root))
                continue

            frontmatter, _body = parse_frontmatter(text)
            classification = _text(frontmatter.get("data_classification")).lower()
            content_classification = _text(frontmatter.get("governed_content_classification")).lower()
            tags = {str(tag).lower() for tag in frontmatter.get("tags", [])}
            governed = bool(classification) or bool(content_classification) or "personal-data" in tags or "governed-memory" in tags
            if not governed:
                continue

            governed_records += 1
            findings.extend(
                _audit_record(root, path, text, frontmatter, classification, content_classification, current_day)
            )

    errors = [item for item in findings if item["level"] == "error"]
    warnings = [item for item in findings if item["level"] == "warning"]
    return {
        "schema_version": "FGR/1",
        "governed_records": governed_records,
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
        "scope": "Repository-backed Markdown metadata only. External stores and Git history are out of scope.",
    }


def record_audit_event(
    root: Path,
    *,
    action: str,
    actor_ref: str,
    record_ref: str,
    subject_ref: str | None = None,
    evidence_ref: str | None = None,
) -> dict[str, Any]:
    """Append a tamper-evident, metadata-only audit event outside the repository."""
    root = root.resolve()
    clean_action = _validate_action(action)
    clean_actor = _validate_opaque_reference(actor_ref, "actor reference")
    clean_record = _validate_opaque_reference(record_ref, "record reference")
    clean_subject = None if subject_ref is None else _validate_opaque_reference(subject_ref, "subject reference")
    if clean_action == "erase":
        if evidence_ref is None:
            raise ValueError("An erase event requires an opaque reference to provider deletion evidence")
        clean_evidence = _validate_opaque_reference(evidence_ref, "evidence reference")
    elif evidence_ref is not None:
        raise ValueError("An evidence reference is only accepted for an erase event")
    else:
        clean_evidence = None
    log_path = _audit_log_path(root)

    with _audit_lock(log_path):
        events = _read_audit_events(log_path)
        if error := _audit_chain_error(events):
            raise ValueError(f"Refusing to append to an invalid governance audit log: {error}")
        previous_hash = events[-1]["event_hash"] if events else ""
        event = {
            "schema_version": AUDIT_SCHEMA_VERSION,
            "event_id": f"AUD-{uuid.uuid4().hex.upper()}",
            "occurred_at": _utc_now(),
            "action": clean_action,
            "actor_ref_hash": _hash_reference("actor", clean_actor),
            "record_ref_hash": _hash_reference("record", clean_record),
            "subject_ref_hash": _hash_reference("subject", clean_subject) if clean_subject else "",
            "evidence_ref_hash": _hash_reference("evidence", clean_evidence) if clean_evidence else "",
            "previous_event_hash": previous_hash,
        }
        event["event_hash"] = _hash_event(event)
        _append_audit_event(log_path, event)

    return {
        "recorded": True,
        "action": clean_action,
        "event_fingerprint": event["event_hash"][:16],
    }


def verify_audit_log(root: Path) -> dict[str, Any]:
    """Verify the append-only audit chain without returning its stored identifiers."""
    try:
        log_path = _audit_log_path(root.resolve())
        events = _read_audit_events(log_path)
    except (OSError, ValueError) as exc:
        return {"exists": False, "valid": False, "event_count": 0, "reason": str(exc)}

    if error := _audit_chain_error(events):
        return _invalid_audit_status(log_path, len(events), error)

    previous_hash = str(events[-1]["event_hash"]) if events else ""

    return {
        "exists": log_path.exists(),
        "valid": True,
        "event_count": len(events),
        "head_fingerprint": previous_hash[:16] if previous_hash else "",
        "reason": "Audit log is empty." if not events else "Audit hash chain is valid.",
    }


def format_governance_audit(report: dict[str, Any]) -> str:
    lines = [
        "ForgeLoop governance audit:",
        f"- Governed records: {report['governed_records']}",
        f"- Errors: {len(report['errors'])}",
        f"- Warnings: {len(report['warnings'])}",
    ]
    for finding in [*report["errors"], *report["warnings"]]:
        lines.append(f"- {finding['level'].upper()} {finding['code']} ({finding['path']}): {finding['message']}")
    lines.append(f"Overall: {'ok' if report['ok'] else 'needs attention'}")
    return "\n".join(lines)


def format_governance_log_status(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "ForgeLoop governance audit log:",
            f"- Exists: {status['exists']}",
            f"- Events: {status['event_count']}",
            f"- Valid: {status['valid']}",
            f"- Status: {status['reason']}",
        ]
    )


def _audit_record(
    root: Path,
    path: Path,
    text: str,
    frontmatter: dict[str, Any],
    classification: str,
    content_classification: str,
    current_day: date,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if classification not in ALLOWED_CLASSIFICATIONS:
        return [_finding("error", path, "classification", "Governed memory needs a supported data_classification.", root=root)]

    if classification in {"personal", "special-category"}:
        findings.append(
            _finding(
                "error",
                path,
                "personal-data-in-repository",
                "Do not place personal data in repository-backed Markdown. Keep only an opaque external-store pointer.",
                root=root,
            )
        )

    if content_classification and content_classification not in ALLOWED_CLASSIFICATIONS:
        findings.append(
            _finding(
                "error",
                path,
                "governed-content-classification",
                "governed_content_classification needs a supported value.",
                root=root,
            )
        )

    if content_classification in {"personal", "special-category"}:
        for key in (
            "subject_ref",
            "jurisdiction",
            "purpose",
            "lawful_basis",
            "provenance_source",
            "provenance_recorded_at",
            "retention_until",
            "storage_ref",
        ):
            if not _text(frontmatter.get(key)):
                findings.append(
                    _finding(
                        "error",
                        path,
                        "missing-governance-field",
                        f"Missing {key} for personal-data metadata.",
                        root=root,
                    )
                )

        subject_ref = _text(frontmatter.get("subject_ref"))
        if subject_ref and not OPAQUE_REFERENCE_RE.fullmatch(subject_ref):
            findings.append(
                _finding(
                    "error",
                    path,
                    "subject-reference",
                    "subject_ref must be an opaque upper-case identifier.",
                    root=root,
                )
            )
        storage_ref = _text(frontmatter.get("storage_ref"))
        if storage_ref and not OPAQUE_REFERENCE_RE.fullmatch(storage_ref):
            findings.append(
                _finding(
                    "error",
                    path,
                    "storage-reference",
                    "storage_ref must be an opaque upper-case identifier, not a provider URL or file path.",
                    root=root,
                )
            )
        jurisdiction = _text(frontmatter.get("jurisdiction"))
        if jurisdiction and not JURISDICTION_RE.fullmatch(jurisdiction):
            findings.append(
                _finding(
                    "error",
                    path,
                    "jurisdiction",
                    "jurisdiction must be an ISO country code, EEA, or GLOBAL.",
                    root=root,
                )
            )
        lawful_basis = _text(frontmatter.get("lawful_basis")).lower()
        if lawful_basis and lawful_basis not in ALLOWED_LAWFUL_BASES:
            findings.append(
                _finding(
                    "error",
                    path,
                    "lawful-basis",
                    "lawful_basis is not one of the supported values.",
                    root=root,
                )
            )
        provenance_source = _text(frontmatter.get("provenance_source")).lower()
        if provenance_source and provenance_source not in ALLOWED_PROVENANCE_SOURCES:
            findings.append(
                _finding(
                    "error",
                    path,
                    "provenance-source",
                    "provenance_source is not one of the supported values.",
                    root=root,
                )
            )
        provenance_date = _check_iso_date(
            findings,
            root,
            path,
            "provenance_recorded_at",
            _text(frontmatter.get("provenance_recorded_at")),
        )
        if provenance_date and provenance_date > current_day:
            findings.append(
                _finding(
                    "error",
                    path,
                    "provenance-in-future",
                    "provenance_recorded_at cannot be in the future.",
                    root=root,
                )
            )
        retention = _check_iso_date(findings, root, path, "retention_until", _text(frontmatter.get("retention_until")))
        if retention and retention < current_day:
            findings.append(
                _finding(
                    "error",
                    path,
                    "retention-expired",
                    "retention_until has passed; erase or review the external record.",
                    root=root,
                )
            )

    if PERSONAL_DATA_HINT_RE.search(text):
        findings.append(
            _finding(
                "warning",
                path,
                "possible-sensitive-content",
                "Possible personal or secret-like content found. Review and redact before committing.",
                root=root,
            )
        )
    return findings


def _check_iso_date(
    findings: list[dict[str, str]], root: Path, path: Path, key: str, value: str
) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        findings.append(_finding("error", path, "date-format", f"{key} must use YYYY-MM-DD.", root=root))
        return None


def _finding(level: str, path: Path, code: str, message: str, *, root: Path) -> dict[str, str]:
    return {"level": level, "path": path.relative_to(root).as_posix(), "code": code, "message": message}


def _text(value: Any) -> str:
    return str(value or "").strip()


def _audit_log_path(root: Path) -> Path:
    root_hash = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:16]
    path = _governance_home() / "audit" / f"{root_hash}.jsonl"
    resolved_path = path.resolve()
    if resolved_path == root or root in resolved_path.parents:
        raise ValueError("Governance audit storage must remain outside the repository")
    return path


def _governance_home() -> Path:
    override = os.environ.get("FORGELOOP_GOVERNANCE_HOME") or os.environ.get("FORGELOOP_CONFIG_HOME")
    if override:
        return Path(override).expanduser().resolve() / "governance"
    if os.name == "nt":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "ForgeLoop" / "governance"
        return Path.home() / "AppData" / "Roaming" / "ForgeLoop" / "governance"
    xdg_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_home:
        return Path(xdg_home).expanduser() / "forgeloop" / "governance"
    if os.uname().sysname == "Darwin":
        return Path.home() / "Library" / "Application Support" / "ForgeLoop" / "governance"
    return Path.home() / ".config" / "forgeloop" / "governance"


class _AuditLock:
    def __init__(self, lock_path: Path) -> None:
        self.lock_path = lock_path
        self.acquired = False

    def __enter__(self) -> None:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        _reject_symlink_ancestors(self.lock_path.parent)
        for _ in range(20):
            if self.lock_path.is_symlink():
                raise ValueError("Refusing to use a symlinked governance audit lock")
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            try:
                fd = os.open(self.lock_path, flags, 0o600)
            except FileExistsError:
                time.sleep(0.05)
                continue
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(str(os.getpid()))
            self.acquired = True
            return
        raise OSError("Governance audit log is busy; retry the command")

    def __exit__(self, _exc_type: object, _exc: object, _traceback: object) -> None:
        if self.acquired:
            try:
                self.lock_path.unlink(missing_ok=True)
            except OSError:
                pass


def _audit_lock(log_path: Path) -> _AuditLock:
    return _AuditLock(log_path.with_suffix(".lock"))


def _read_audit_events(log_path: Path) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []
    if log_path.is_symlink() or not log_path.is_file():
        raise ValueError("Governance audit log must be a regular file")
    if log_path.stat().st_size > MAX_AUDIT_LOG_BYTES:
        raise ValueError("Governance audit log exceeds the size limit")
    events: list[dict[str, Any]] = []
    with log_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if len(line.encode("utf-8")) > MAX_AUDIT_LINE_BYTES:
                raise ValueError(f"Governance audit event {line_number} exceeds the size limit")
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Governance audit event {line_number} is invalid JSON") from exc
            if not isinstance(event, dict):
                raise TypeError(f"Governance audit event {line_number} is not an object")
            events.append(event)
    return events


def _append_audit_event(log_path: Path, event: dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    _reject_symlink_ancestors(log_path.parent)
    if log_path.is_symlink():
        raise ValueError("Refusing to write through a symlinked governance audit log")
    if log_path.exists() and not log_path.is_file():
        raise ValueError("Governance audit log must be a regular file")
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    payload = json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
    fd = os.open(log_path, flags, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    _restrict_file_permissions(log_path)


def _reject_symlink_ancestors(path: Path) -> None:
    current = path
    while current != current.parent:
        if current.is_symlink():
            raise ValueError("Refusing a governance audit path with a symlinked parent")
        current = current.parent


def _validate_action(action: str) -> str:
    clean = _text(action).lower()
    if clean not in ALLOWED_ACTIONS:
        raise ValueError("Unsupported governance action")
    return clean


def _validate_opaque_reference(value: str, label: str) -> str:
    clean = _text(value)
    if not OPAQUE_REFERENCE_RE.fullmatch(clean):
        raise ValueError(f"{label.capitalize()} must be an opaque upper-case identifier, not personal data")
    return clean


def _hash_reference(namespace: str, value: str) -> str:
    return hashlib.sha256(f"{namespace}:{value}".encode()).hexdigest()


def _hash_event(event: dict[str, Any]) -> str:
    body = {key: value for key, value in event.items() if key != "event_hash"}
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _audit_chain_error(events: list[dict[str, Any]]) -> str:
    previous_hash = ""
    legacy_keys = {
        "schema_version",
        "event_id",
        "occurred_at",
        "action",
        "actor_ref_hash",
        "record_ref_hash",
        "subject_ref_hash",
        "previous_event_hash",
        "event_hash",
    }
    for index, event in enumerate(events, start=1):
        schema_version = event.get("schema_version")
        if schema_version == LEGACY_AUDIT_SCHEMA_VERSION:
            required_keys = legacy_keys
        elif schema_version == AUDIT_SCHEMA_VERSION:
            required_keys = legacy_keys | {"evidence_ref_hash"}
        else:
            return f"Audit event {index} has an unsupported schema version."
        if set(event) != required_keys:
            return f"Audit event {index} has an unsupported schema."
        if not isinstance(event.get("event_id"), str) or not AUDIT_EVENT_ID_RE.fullmatch(event["event_id"]):
            return f"Audit event {index} has an invalid event identifier."
        action = event.get("action")
        if not isinstance(action, str) or action not in ALLOWED_ACTIONS:
            return f"Audit event {index} has an unsupported action."
        if not _is_timestamp(event.get("occurred_at")):
            return f"Audit event {index} has an invalid timestamp."
        for key in ("actor_ref_hash", "record_ref_hash", "event_hash"):
            if not isinstance(event.get(key), str) or not SHA256_RE.fullmatch(event[key]):
                return f"Audit event {index} has an invalid {key}."
        for key in ("subject_ref_hash", "previous_event_hash"):
            value = event.get(key)
            if not isinstance(value, str) or (value and not SHA256_RE.fullmatch(value)):
                return f"Audit event {index} has an invalid {key}."
        if schema_version == AUDIT_SCHEMA_VERSION:
            evidence_hash = event["evidence_ref_hash"]
            if not isinstance(evidence_hash, str) or (evidence_hash and not SHA256_RE.fullmatch(evidence_hash)):
                return f"Audit event {index} has an invalid evidence_ref_hash."
            if (event["action"] == "erase") != bool(evidence_hash):
                return f"Audit event {index} has an inconsistent erasure evidence reference."
        if event["previous_event_hash"] != previous_hash:
            return f"Audit event {index} breaks the event chain."
        if event["event_hash"] != _hash_event(event):
            return f"Audit event {index} hash does not match its contents."
        previous_hash = event["event_hash"]
    return ""


def _is_timestamp(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return value.endswith("Z")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _restrict_file_permissions(path: Path) -> None:
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def _invalid_audit_status(log_path: Path, index: int, reason: str) -> dict[str, Any]:
    return {
        "exists": log_path.exists(),
        "valid": False,
        "event_count": index,
        "head_fingerprint": "",
        "reason": reason,
    }
