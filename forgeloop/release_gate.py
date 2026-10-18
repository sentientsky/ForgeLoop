from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .doctor import doctor_report

SOURCE_ALPHA_FILES = {
    "CHANGELOG.md": "changelog",
    "GOVERNANCE.md": "project governance",
    "SECURITY.md": "security policy",
    "SUPPORT.md": "support policy",
    "docs/RELEASE_GUIDE.md": "release guide",
    "docs/RELEASE_CHECKLIST.md": "release checklist",
    "docs/PUBLISHING.md": "publishing guide",
    "docs/MAINTAINER_GUIDE.md": "maintainer guide",
    "docs/ROADMAP.md": "roadmap and current status",
    "docs/compatibility/deployment-evals/2026-05-18-clean-session-acceptance.md": "clean-session evidence",
    ".github/workflows/ci.yml": "CI workflow",
    ".github/workflows/codeql.yml": "CodeQL workflow",
    ".github/workflows/fuzz.yml": "fuzz workflow",
    ".github/workflows/release.yml": "release workflow",
    ".github/CODEOWNERS": "code owner routing",
    "docs/release/stable-evidence.json": "stable-evidence manifest",
}

STABLE_EVIDENCE_PATH = "docs/release/stable-evidence.json"
MAX_STABLE_EVIDENCE_BYTES = 64_000
STABLE_EVIDENCE_REQUIREMENTS = {
    "claude_clean_session": ("tool_version", "command_ref", "working_tree"),
    "independent_review": ("reviewer", "review_url", "branch_protection_checked"),
    "external_erasure": ("provider", "evidence_ref", "verification_method"),
}

UNSUPPORTED_CLAIM_PATTERNS = {
    "100% production": "Do not claim absolute production completeness.",
    "bullet proof": "Do not claim impossible security guarantees.",
    "bulletproof": "Do not claim impossible security guarantees.",
    "gdpr compliant": "Do not claim legal compliance without formal legal review.",
    "hipaa compliant": "Do not claim legal compliance without formal legal review.",
    "soc 2": "Do not claim certification or equivalent assurance without evidence.",
    "guaranteed erasure": "Do not claim third-party erasure completion without provider proof.",
    "90 percent token": "Use measured packet reports instead of fixed token-saving claims.",
    "80 percent token": "Use measured packet reports instead of fixed token-saving claims.",
}


def release_gate_report(root: Path, target: str = "source-alpha") -> dict[str, Any]:
    if target not in {"source-alpha", "stable"}:
        raise ValueError("target must be 'source-alpha' or 'stable'")

    root = root.resolve()
    checks: list[dict[str, Any]] = []

    doctor = doctor_report(root)
    _add(
        checks,
        "local-health",
        "pass" if doctor["ok"] else "fail",
        "Doctor found no blocking local health errors."
        if doctor["ok"]
        else "Doctor found blocking local health errors.",
        {"doctor_ok": doctor["ok"]},
    )

    missing = [path for path in SOURCE_ALPHA_FILES if not (root / path).is_file()]
    _add(
        checks,
        "release-files",
        "pass" if not missing else "fail",
        "Release, security, governance, compatibility, and workflow files are present."
        if not missing
        else "Required release-readiness files are missing.",
        {"missing": missing},
    )

    pyproject_text = _read(root / "pyproject.toml")
    alpha_classifier = "Development Status :: 3 - Alpha" in pyproject_text
    _add(
        checks,
        "public-status-label",
        "pass" if alpha_classifier else "fail",
        "Package metadata labels the project as alpha."
        if alpha_classifier
        else "Package metadata must not imply stable production status yet.",
    )

    unsupported_claims = _unsupported_claims(root)
    _add(
        checks,
        "unsupported-public-claims",
        "pass" if not unsupported_claims else "fail",
        "No unsupported absolute production, legal-certification, or fixed token-saving claims were found."
        if not unsupported_claims
        else "Unsupported public claims need removal or stronger evidence.",
        {"matches": unsupported_claims},
    )

    stable_evidence, stable_evidence_error = _load_stable_evidence(root)
    for evidence_name, check_name, passed_message, blocked_message in (
        (
            "claude_clean_session",
            "stable-claude-acceptance",
            "Claude Code clean-session acceptance has a current structured evidence record.",
            "Claude Code clean-session acceptance is still blocked or incomplete.",
        ),
        (
            "independent_review",
            "stable-independent-review",
            "Independent maintainer review has a current structured evidence record.",
            "Independent maintainer review is not yet available.",
        ),
        (
            "external_erasure",
            "stable-external-erasure-evidence",
            "External-store erasure has provider-specific structured verification evidence.",
            "External-store erasure remains operator-attested, not provider-verified.",
        ),
    ):
        passed, reason, details = _stable_evidence_status(
            root, stable_evidence, stable_evidence_error, evidence_name
        )
        _add(
            checks,
            check_name,
            "pass" if passed else "block",
            passed_message if passed else f"{blocked_message} {reason}",
            details,
        )

    failures = [check for check in checks if check["status"] == "fail"]
    blockers = [check for check in checks if check["status"] == "block"]
    source_alpha_ready = not failures
    stable_ready = source_alpha_ready and not blockers
    ok = source_alpha_ready if target == "source-alpha" else stable_ready

    return {
        "schema_version": 1,
        "root": str(root),
        "target": target,
        "ok": ok,
        "source_alpha_ready": source_alpha_ready,
        "stable_ready": stable_ready,
        "decision": _decision(target, source_alpha_ready, stable_ready),
        "checks": checks,
    }


def format_release_gate_report(report: dict[str, Any]) -> str:
    lines = ["ForgeLoop release gate:"]
    for check in report["checks"]:
        lines.append(f"- {check['status'].upper()} {check['name']}: {check['message']}")
    lines.append("")
    lines.append(f"Source alpha ready: {'yes' if report['source_alpha_ready'] else 'no'}")
    lines.append(f"Stable production ready: {'yes' if report['stable_ready'] else 'no'}")
    lines.append(f"Decision: {report['decision']}")
    return "\n".join(lines)


def _unsupported_claims(root: Path) -> list[dict[str, str]]:
    matches: list[dict[str, str]] = []
    public_files = [
        root / "README.md",
        root / "docs/WHAT_IT_IS.md",
        root / "docs/GITHUB_PAGE.md",
        root / "docs/HOW_TO_USE.md",
        root / "docs/INSTALLATION.md",
        root / "docs/RELEASE_GUIDE.md",
        root / "docs/PUBLISHING.md",
        root / "docs/ROADMAP.md",
    ]
    for path in public_files:
        text = _read(path)
        lowered = text.casefold()
        for pattern, reason in UNSUPPORTED_CLAIM_PATTERNS.items():
            if pattern in lowered:
                matches.append({"path": str(path.relative_to(root)), "pattern": pattern, "reason": reason})
    return matches


def _decision(target: str, source_alpha_ready: bool, stable_ready: bool) -> str:
    if target == "stable":
        if stable_ready:
            return "Stable production promotion may proceed after the normal reviewed release process."
        return "Do not promote to stable production. Resolve the blocking gates first."
    if source_alpha_ready:
        return "Source alpha or release-candidate promotion may proceed after PR review and required GitHub checks."
    return "Do not promote. Fix failing release-readiness checks first."


def _read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _load_stable_evidence(root: Path) -> tuple[dict[str, Any] | None, str | None]:
    path = root / STABLE_EVIDENCE_PATH
    try:
        if path.stat().st_size > MAX_STABLE_EVIDENCE_BYTES:
            return None, "The stable-evidence manifest exceeds the size limit."
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, "The stable-evidence manifest is missing."
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None, "The stable-evidence manifest is unreadable or invalid JSON."

    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        return None, "The stable-evidence manifest has an unsupported schema."
    return payload, None


def _stable_evidence_status(
    root: Path,
    manifest: dict[str, Any] | None,
    manifest_error: str | None,
    evidence_name: str,
) -> tuple[bool, str, dict[str, str]]:
    if manifest_error:
        return False, manifest_error, {}
    assert manifest is not None

    entry = manifest.get(evidence_name)
    if not isinstance(entry, dict):
        return False, "The required evidence entry is missing.", {}
    if entry.get("status") != "passed":
        return False, "The evidence entry is deliberately marked blocked.", {}

    evidence_path = entry.get("evidence_path")
    if not _is_safe_evidence_path(root, evidence_path):
        return False, "The evidence path is missing, unsafe, or unavailable.", {}
    if not _is_iso_date(entry.get("updated_on")):
        return False, "The evidence date is missing, malformed, or in the future.", {}

    for field in STABLE_EVIDENCE_REQUIREMENTS[evidence_name]:
        value = entry.get(field)
        if evidence_name == "independent_review" and field == "branch_protection_checked":
            if value is not True:
                return False, "The branch-protection check is not recorded as passed.", {}
            continue
        if not _is_short_text(value):
            return False, "The evidence entry is missing required structured details.", {}

    return True, "", {"evidence_path": str(evidence_path), "updated_on": str(entry["updated_on"])}


def _is_safe_evidence_path(root: Path, value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("docs/") or "\\" in value:
        return False
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return candidate.is_file()


def _is_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value) <= datetime.now(timezone.utc).date()
    except ValueError:
        return False


def _is_short_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 240 and "\n" not in value and "\r" not in value


def _add(
    checks: list[dict[str, Any]],
    name: str,
    status: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> None:
    checks.append({"name": name, "status": status, "message": message, "details": details or {}})
