from __future__ import annotations

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

    acceptance_text = _read(root / "docs/compatibility/deployment-evals/2026-05-18-clean-session-acceptance.md")
    claude_blocked = "blocked by API authentication" in acceptance_text or "not evidence" in acceptance_text
    _add(
        checks,
        "stable-claude-acceptance",
        "block" if claude_blocked else "pass",
        "Claude Code clean-session acceptance is still blocked or incomplete."
        if claude_blocked
        else "Claude Code clean-session acceptance has a current passing evidence record.",
    )

    roadmap_text = _read(root / "docs/ROADMAP.md")
    governance_text = _read(root / "GOVERNANCE.md")
    independent_review_blocked = "Add a second trusted maintainer" in roadmap_text or "only one active maintainer" in governance_text
    _add(
        checks,
        "stable-independent-review",
        "block" if independent_review_blocked else "pass",
        "Independent maintainer review is not yet available."
        if independent_review_blocked
        else "Independent maintainer review is available and documented.",
    )

    governance_docs = _read(root / "docs/governance/README.md") + "\n" + _read(
        root / "docs/checks/2026-09-24-production-closure-audit.md"
    )
    external_erasure_blocked = (
        "no external-store connector" in governance_docs
        or "no provider deletion adapter" in governance_docs
        or "cannot verify third-party deletion" in governance_docs
    )
    _add(
        checks,
        "stable-external-erasure-evidence",
        "block" if external_erasure_blocked else "pass",
        "External-store erasure remains operator-attested, not provider-verified."
        if external_erasure_blocked
        else "External-store erasure has provider-specific verification evidence.",
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


def _add(
    checks: list[dict[str, Any]],
    name: str,
    status: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> None:
    checks.append({"name": name, "status": status, "message": message, "details": details or {}})
