from __future__ import annotations

import importlib.util
import platform
from pathlib import Path
from typing import Any

from .compat import compatibility_report
from .core import build_memory_index, repo_status, validate_repo
from .governance import audit_governed_memory, verify_audit_log
from .opencli import opencli_status
from .secrets import check_secrets
from .setup import LOCAL_SETUP_FILE


def doctor_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    checks: list[dict[str, Any]] = []

    _add(
        checks,
        "python",
        "ok",
        f"Python {platform.python_version()} on {platform.system() or 'unknown system'}",
    )

    findings = validate_repo(root)
    errors = [item for item in findings if item.level == "error"]
    warnings = [item for item in findings if item.level == "warning"]
    _add(
        checks,
        "structure",
        "error" if errors else "ok",
        f"{len(errors)} errors, {len(warnings)} warnings from validate_repo.",
        {"errors": [item.as_dict(root) for item in errors[:10]], "warning_count": len(warnings)},
    )

    compat = compatibility_report(root)
    missing_targets = [target["tool"] for target in compat["targets"] if not target["profile_files_present"]]
    _add(
        checks,
        "compatibility",
        "error" if missing_targets else "ok",
        "All expected AI tool profile files are present; external tool behaviour is not tested here."
        if not missing_targets
        else "Some tool profile files are missing.",
        {"missing_targets": missing_targets},
    )

    secrets = check_secrets(root)
    if secrets.repo_env_files:
        _add(
            checks,
            "secrets",
            "error",
            "Real .env-style files were found inside the repository.",
            {"repo_env_files": [str(path.relative_to(root)) for path in secrets.repo_env_files]},
        )
    elif secrets.exists and not secrets.warnings:
        _add(checks, "secrets", "ok", "External secrets file exists and no repo .env files were found.")
    elif secrets.exists:
        _add(checks, "secrets", "warn", "External secrets file exists but needs local attention.", {"warnings": secrets.warnings})
    else:
        _add(
            checks,
            "secrets",
            "warn",
            "External secrets file has not been initialised yet or is unsafe.",
            {"warnings": secrets.warnings},
        )

    index = build_memory_index(root, check=True)
    _add(
        checks,
        "memory-index",
        "error" if index.changed else "ok",
        "Memory index is current." if not index.changed else "Memory index is out of date.",
        {
            "record_count": index.record_count,
            "json_path": str(index.json_path.relative_to(root)),
            "markdown_path": str(index.markdown_path.relative_to(root)),
        },
    )

    governance = audit_governed_memory(root)
    _add(
        checks,
        "governed-memory",
        "error" if governance["errors"] else "warn" if governance["warnings"] else "ok",
        "Governed-memory metadata is valid."
        if governance["ok"]
        else "Governed-memory metadata needs attention.",
        {
            "governed_records": governance["governed_records"],
            "errors": len(governance["errors"]),
            "warnings": len(governance["warnings"]),
        },
    )
    audit_log = verify_audit_log(root)
    _add(
        checks,
        "governance-audit-log",
        "ok" if audit_log["valid"] else "error",
        audit_log["reason"],
        {"exists": audit_log["exists"], "event_count": audit_log["event_count"]},
    )

    status = repo_status(root)
    _add(
        checks,
        "memory-status",
        "ok",
        f"{status['memory_records']} memory records, {status['skills']} skills, {status['agents']} agents.",
        status,
    )

    local_setup = root / LOCAL_SETUP_FILE
    _add(
        checks,
        "local-setup",
        "ok",
        "Local setup profile exists."
        if local_setup.is_file()
        else "No local setup profile selected yet. This is normal for a clean clone.",
        {"path": LOCAL_SETUP_FILE},
    )

    ci_path = root / ".github/workflows/ci.yml"
    ci_text = ci_path.read_text(encoding="utf-8", errors="replace") if ci_path.is_file() else ""
    ci_markers = [
        "python -m coverage run -m unittest discover -s tests",
        "python -m coverage report",
        "python -m ruff check forgeloop tests",
        "python -m forgeloop validate .",
        "python tests/package_smoke.py dist .",
    ]
    ci_ok = ci_path.is_file() and all(marker in ci_text for marker in ci_markers)
    _add(
        checks,
        "ci",
        "ok" if ci_ok else "warn",
        "CI runs Python tests on Ubuntu, Windows, and macOS, plus lint, validation, and an isolated wheel smoke test."
        if ci_ok
        else "CI workflow is missing or incomplete.",
        {"path": ".github/workflows/ci.yml"},
    )

    release_files = {
        "CHANGELOG.md": "changelog",
        "CODE_OF_CONDUCT.md": "code of conduct",
        "GOVERNANCE.md": "project governance",
        "SUPPORT.md": "support policy",
        "docs/INSTALLATION.md": "installation guide",
        "docs/COMMAND_REFERENCE.md": "command reference",
        "docs/TROUBLESHOOTING.md": "troubleshooting guide",
        "docs/ROADMAP.md": "roadmap and current status",
        "docs/PUBLISHING.md": "publishing guide",
        "docs/MAINTAINER_GUIDE.md": "maintainer guide",
        "docs/GITHUB_SETUP.md": "GitHub setup guide",
        ".github/CODEOWNERS": "code owner routing",
        ".github/PULL_REQUEST_TEMPLATE.md": "pull request template",
        ".github/ISSUE_TEMPLATE/bug_report.yml": "bug issue form",
        ".github/ISSUE_TEMPLATE/feature_request.yml": "feature issue form",
        ".github/ISSUE_TEMPLATE/documentation.yml": "documentation issue form",
        ".github/dependabot.yml": "Dependabot config",
        ".github/workflows/release.yml": "release workflow",
        ".github/workflows/scorecard.yml": "Scorecard workflow",
        ".github/workflows/codeql.yml": "CodeQL workflow",
        "tests/package_smoke.py": "isolated wheel smoke test",
    }
    missing_release = [path for path in release_files if not (root / path).is_file()]
    _add(
        checks,
        "release-readiness-files",
        "error" if missing_release else "ok",
        "Local release-readiness files are present; published GitHub releases are not checked."
        if not missing_release
        else "Some local release-readiness files are missing.",
        {"missing": missing_release},
    )

    tokenizer_ready = importlib.util.find_spec("tiktoken") is not None
    _add(
        checks,
        "tokenizer",
        "ok",
        "Optional tiktoken tokenizer is installed."
        if tokenizer_ready
        else "Optional tiktoken tokenizer is not installed; estimated token counts remain available.",
    )

    opencli = opencli_status(root)
    opencli_level = "ok"
    if not opencli["plugin_source"]["ready"]:
        opencli_level = "error"
    if opencli_level == "error":
        opencli_message = "OpenCLI integration source is incomplete."
    elif opencli["opencli"]["installed"] and opencli["node"]["ready"]:
        opencli_message = "OpenCLI is installed and the ForgeLoop plugin source is present."
    else:
        opencli_message = "ForgeLoop OpenCLI plugin source is present. OpenCLI itself is optional and not required for core health."
    _add(
        checks,
        "opencli",
        opencli_level,
        opencli_message,
        {
            "installed": opencli["opencli"]["installed"],
            "node_ready": opencli["node"]["ready"],
            "plugin_source": opencli["plugin_source"],
            "warnings": opencli["warnings"],
        },
    )

    return {
        "schema_version": 1,
        "root": str(root),
        "ok": not any(item["status"] == "error" for item in checks),
        "checks": checks,
    }


def format_doctor_report(report: dict[str, Any]) -> str:
    lines = ["ForgeLoop doctor:"]
    for check in report["checks"]:
        lines.append(f"- {check['status'].upper()} {check['name']}: {check['message']}")
    lines.append("")
    lines.append(f"Overall: {'ok' if report['ok'] else 'needs attention'}")
    return "\n".join(lines)


def _add(
    checks: list[dict[str, Any]],
    name: str,
    status: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> None:
    checks.append(
        {
            "name": name,
            "status": status,
            "message": message,
            "details": details or {},
        }
    )
