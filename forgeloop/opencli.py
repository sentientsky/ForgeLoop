from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


OPENCLI_PACKAGE = "@jackwener/opencli"
OPENCLI_PACKAGE_LATEST = f"{OPENCLI_PACKAGE}@latest"
OPENCLI_SKILLS_PACKAGE = "jackwener/opencli"
OPENCLI_MIN_NODE_MAJOR = 21
OPENCLI_PLUGIN_REL = "integrations/opencli"
OPENCLI_SKILLS = [
    "opencli-adapter-author",
    "opencli-autofix",
    "opencli-browser",
    "opencli-usage",
    "smart-search",
]
DEFAULT_INSTALL_TIMEOUT = 300
DEFAULT_STATUS_TIMEOUT = 10


@dataclass(frozen=True)
class CommandRun:
    command: list[str]
    exit_code: int | None
    stdout: str
    stderr: str
    timed_out: bool = False
    skipped: bool = False
    reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "command": self.command,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "timed_out": self.timed_out,
            "skipped": self.skipped,
            "reason": self.reason,
        }


def opencli_status(root: Path, fetch_npm: bool = False) -> dict[str, Any]:
    root = root.resolve()
    node_path = shutil.which("node")
    npm_path = shutil.which("npm")
    npx_path = shutil.which("npx")
    opencli_path = shutil.which("opencli")
    plugin_source = _plugin_source_status(root)

    node_version = _version_from_command(node_path, ["--version"])
    node_major = parse_node_major(node_version)
    opencli_version = _version_from_command(opencli_path, ["--version"])
    registry = fetch_opencli_npm_metadata(timeout=DEFAULT_STATUS_TIMEOUT) if fetch_npm else _empty_registry_metadata()

    warnings: list[str] = []
    if not node_path:
        warnings.append("Node.js was not found on PATH. The standard npm install path cannot run.")
    elif node_major is None:
        warnings.append("Node.js version could not be parsed.")
    elif node_major < OPENCLI_MIN_NODE_MAJOR:
        warnings.append(f"OpenCLI requires Node.js >= {OPENCLI_MIN_NODE_MAJOR}.")
    if not npm_path:
        warnings.append("npm was not found on PATH. OpenCLI cannot be installed with npm.")
    if not opencli_path:
        warnings.append("OpenCLI is not installed on PATH yet.")
    if not plugin_source["ready"]:
        warnings.append(plugin_source["reason"])
    warnings.extend(registry["warnings"])

    return {
        "schema_version": 1,
        "root": str(root),
        "package": OPENCLI_PACKAGE,
        "latest_package_spec": OPENCLI_PACKAGE_LATEST,
        "minimum_node_major": OPENCLI_MIN_NODE_MAJOR,
        "registry": registry,
        "node": {
            "path": node_path or "",
            "version": node_version,
            "major": node_major,
            "ready": bool(node_path and node_major is not None and node_major >= OPENCLI_MIN_NODE_MAJOR),
        },
        "npm": {
            "path": npm_path or "",
            "ready": bool(npm_path),
        },
        "npx": {
            "path": npx_path or "",
            "ready": bool(npx_path),
        },
        "opencli": {
            "path": opencli_path or "",
            "version": opencli_version,
            "installed": bool(opencli_path),
        },
        "plugin_source": {
            **plugin_source,
            "install_command": ["opencli", "plugin", "install", plugin_source["path"]],
        },
        "skills": {
            "package": OPENCLI_SKILLS_PACKAGE,
            "available_skills": OPENCLI_SKILLS,
            "install_command": ["npx", "skills", "add", OPENCLI_SKILLS_PACKAGE],
        },
        "warnings": warnings,
    }


def opencli_plan(
    root: Path,
    include_skills: bool = False,
    run_doctor: bool = False,
    fetch_npm: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    plugin_source = _plugin_source_status(root)
    steps: list[dict[str, Any]] = [
        {
            "name": "Install or update OpenCLI",
            "command": ["npm", "install", "-g", OPENCLI_PACKAGE_LATEST],
            "network": True,
            "writes": "global npm package area",
            "safe_default": "manual or explicit --execute only",
        },
        {
            "name": "Install ForgeLoop OpenCLI plugin source",
            "command": ["opencli", "plugin", "install", plugin_source["path"]],
            "network": False,
            "writes": "local OpenCLI plugin registry",
            "safe_default": "manual or explicit --execute only",
        },
        {
            "name": "Verify OpenCLI binary",
            "command": ["opencli", "--version"],
            "network": False,
            "writes": "none",
            "safe_default": "read-only",
        },
        {
            "name": "List OpenCLI commands",
            "command": ["opencli", "list", "-f", "json"],
            "network": False,
            "writes": "none",
            "safe_default": "read-only",
        },
    ]
    if run_doctor:
        steps.append(
            {
                "name": "Run OpenCLI doctor",
                "command": ["opencli", "doctor"],
                "network": False,
                "writes": "may start the local OpenCLI daemon",
                "safe_default": "explicit --run-doctor only",
            }
        )
    if include_skills:
        steps.append(
            {
                "name": "Install OpenCLI AI skills",
                "command": ["npx", "skills", "add", OPENCLI_SKILLS_PACKAGE],
                "network": True,
                "writes": "local AI-agent skills directory",
                "safe_default": "explicit --with-skills only",
            }
        )

    return {
        "schema_version": 1,
        "root": str(root),
        "integration": "OpenCLI integrated peer plugin",
        "status": opencli_status(root, fetch_npm=fetch_npm),
        "steps": steps,
        "safety_notes": [
            "ForgeLoop integrates OpenCLI as an external peer dependency and does not vendor OpenCLI source.",
            "The installer uses @latest only when the user explicitly executes the install command.",
            "Browser-backed OpenCLI commands reuse logged-in Chrome or Chromium sessions, so run them only for trusted tasks.",
            "ForgeLoop does not store OpenCLI credentials, browser cookies, or site tokens.",
            "Use opencli doctor manually when you are ready to test the browser bridge.",
        ],
    }


def run_opencli_install(
    root: Path,
    include_skills: bool = False,
    run_doctor: bool = False,
    execute: bool = False,
    timeout: int = DEFAULT_INSTALL_TIMEOUT,
) -> dict[str, Any]:
    root = root.resolve()
    plan = opencli_plan(root, include_skills=include_skills, run_doctor=run_doctor)
    if not execute:
        return {
            "schema_version": 1,
            "executed": False,
            "status": "dry-run",
            "plan": plan,
            "results": [],
        }

    status = plan["status"]
    results: list[CommandRun] = []
    if not status["node"]["ready"]:
        return _blocked_install(plan, "Node.js >= 21 is required before installing OpenCLI.")
    if not status["npm"]["ready"]:
        return _blocked_install(plan, "npm is required before installing OpenCLI.")
    if not status["plugin_source"]["ready"]:
        return _blocked_install(plan, status["plugin_source"]["reason"])

    npm = status["npm"]["path"]
    results.append(_run_fixed(npm, ["install", "-g", OPENCLI_PACKAGE_LATEST], timeout=timeout))
    if results[-1].exit_code != 0:
        return _install_result(plan, results, "failed")

    opencli = shutil.which("opencli")
    if not opencli:
        results.append(
            CommandRun(
                ["opencli", "--version"],
                None,
                "",
                "",
                skipped=True,
                reason="OpenCLI was not found on PATH after npm install.",
            )
        )
        return _install_result(plan, results, "blocked")

    plugin_source = _plugin_source_status(root)
    if not plugin_source["ready"]:
        return _blocked_install(plan, plugin_source["reason"])
    plugin_path = plugin_source["path"]
    results.append(_run_fixed(opencli, ["plugin", "install", plugin_path], timeout=timeout))
    if results[-1].exit_code != 0 or results[-1].timed_out or results[-1].skipped:
        return _install_result(plan, results, "failed")
    results.append(_run_fixed(opencli, ["--version"], timeout=DEFAULT_STATUS_TIMEOUT))
    if results[-1].exit_code != 0 or results[-1].timed_out or results[-1].skipped:
        return _install_result(plan, results, "failed")
    results.append(_run_fixed(opencli, ["list", "-f", "json"], timeout=DEFAULT_STATUS_TIMEOUT))
    if results[-1].exit_code != 0 or results[-1].timed_out or results[-1].skipped:
        return _install_result(plan, results, "failed")

    if run_doctor:
        results.append(_run_fixed(opencli, ["doctor"], timeout=timeout))

    if include_skills:
        npx = shutil.which("npx")
        if npx:
            results.append(_run_fixed(npx, ["skills", "add", OPENCLI_SKILLS_PACKAGE], timeout=timeout))
        else:
            results.append(
                CommandRun(
                    ["npx", "skills", "add", OPENCLI_SKILLS_PACKAGE],
                    None,
                    "",
                    "",
                    skipped=True,
                    reason="npx was not found on PATH.",
                )
            )

    final_status = "ok" if all(item.exit_code == 0 and not item.timed_out and not item.skipped for item in results) else "failed"
    return _install_result(plan, results, final_status)


def format_opencli_status(status: dict[str, Any]) -> str:
    lines = [
        "ForgeLoop OpenCLI status:",
        f"- Package: {status['latest_package_spec']}",
        f"- Node: {status['node']['version'] or 'not found'}",
        f"- npm: {'ready' if status['npm']['ready'] else 'missing'}",
        f"- OpenCLI: {status['opencli']['version'] or 'not installed'}",
        f"- Plugin source: {'present' if status['plugin_source']['exists'] else 'missing'}",
    ]
    registry = status.get("registry", {})
    if registry.get("checked"):
        lines.append(f"- npm latest: {registry.get('version') or 'unknown'}")
        node_engine = registry.get("engines", {}).get("node", "")
        if node_engine:
            lines.append(f"- npm engine: node {node_engine}")
    if status["warnings"]:
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in status["warnings"])
    return "\n".join(lines)


def format_opencli_plan(plan: dict[str, Any]) -> str:
    lines = [
        "ForgeLoop OpenCLI integration plan:",
        "",
        "Status:",
        f"- Node: {plan['status']['node']['version'] or 'not found'}",
        f"- OpenCLI: {plan['status']['opencli']['version'] or 'not installed'}",
        f"- Plugin source: {'present' if plan['status']['plugin_source']['exists'] else 'missing'}",
    ]
    registry = plan["status"].get("registry", {})
    if registry.get("checked"):
        lines.append(f"- npm latest: {registry.get('version') or 'unknown'}")
        node_engine = registry.get("engines", {}).get("node", "")
        if node_engine:
            lines.append(f"- npm engine: node {node_engine}")
    lines.extend(
        [
            "",
            "Steps:",
        ]
    )
    for index, step in enumerate(plan["steps"], start=1):
        lines.append(f"{index}. {step['name']}")
        lines.append(f"   command: {_display_command(step['command'])}")
        lines.append(f"   writes: {step['writes']}")
    lines.append("")
    lines.append("Safety notes:")
    lines.extend(f"- {note}" for note in plan["safety_notes"])
    return "\n".join(lines)


def format_opencli_install_result(result: dict[str, Any]) -> str:
    if not result["executed"]:
        return format_opencli_plan(result["plan"])
    lines = [
        f"ForgeLoop OpenCLI install: {result['status']}",
        "",
        "Results:",
    ]
    for item in result["results"]:
        command = _display_command(item["command"])
        if item["skipped"]:
            lines.append(f"- skipped: {command} ({item['reason']})")
        elif item["timed_out"]:
            lines.append(f"- timed out: {command}")
        else:
            lines.append(f"- exit {item['exit_code']}: {command}")
    return "\n".join(lines)


def parse_node_major(version: str) -> int | None:
    match = re.search(r"v?(\d+)(?:\.\d+)?(?:\.\d+)?", version.strip())
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def parse_node_engine_major(engine: str) -> int | None:
    match = re.search(r">=\s*(\d+)(?:\.\d+)?(?:\.\d+)?", engine.strip())
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def fetch_opencli_npm_metadata(timeout: int = DEFAULT_STATUS_TIMEOUT) -> dict[str, Any]:
    npm = shutil.which("npm")
    metadata = _empty_registry_metadata()
    metadata["checked"] = True
    if not npm:
        metadata["warnings"].append("npm metadata could not be fetched because npm is not on PATH.")
        return metadata

    result = _run_fixed(
        npm,
        ["view", OPENCLI_PACKAGE, "version", "dist-tags", "engines", "license", "--json"],
        timeout=timeout,
    )
    if result.exit_code != 0 or result.timed_out:
        metadata["warnings"].append("npm metadata fetch failed.")
        metadata["result"] = result.as_dict()
        return metadata

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        metadata["warnings"].append("npm metadata was not valid JSON.")
        metadata["result"] = result.as_dict()
        return metadata

    if not isinstance(payload, dict):
        metadata["warnings"].append("npm metadata did not return an object.")
        return metadata

    engines = payload.get("engines") if isinstance(payload.get("engines"), dict) else {}
    node_engine = str(engines.get("node", "")) if engines else ""
    engine_major = parse_node_engine_major(node_engine)
    metadata.update(
        {
            "version": str(payload.get("version", "")),
            "dist_tags": payload.get("dist-tags") if isinstance(payload.get("dist-tags"), dict) else {},
            "engines": engines,
            "node_engine_major": engine_major,
            "license": str(payload.get("license", "")),
        }
    )
    if engine_major is not None and engine_major < OPENCLI_MIN_NODE_MAJOR:
        metadata["warnings"].append(
            "npm engine metadata is less strict than OpenCLI installation docs; ForgeLoop keeps the stricter docs baseline."
        )
    return metadata


def _empty_registry_metadata() -> dict[str, Any]:
    return {
        "checked": False,
        "version": "",
        "dist_tags": {},
        "engines": {},
        "node_engine_major": None,
        "license": "",
        "warnings": [],
    }


def _plugin_source_status(root: Path) -> dict[str, Any]:
    """Describe the local plugin source without following repository symlinks."""
    path = root / OPENCLI_PLUGIN_REL
    manifest = path / "opencli-plugin.json"
    base = {
        "path": str(path),
        "relative_path": OPENCLI_PLUGIN_REL,
        "exists": path.is_dir(),
        "manifest_exists": manifest.is_file() and not manifest.is_symlink(),
    }
    if _has_symlink_ancestor(path, root):
        return {**base, "ready": False, "reason": "ForgeLoop OpenCLI plugin source must not use symlinks."}
    try:
        resolved = path.resolve()
    except (OSError, RuntimeError):
        return {
            **base,
            "ready": False,
            "reason": "ForgeLoop OpenCLI plugin source could not be resolved safely.",
        }
    if resolved != root and root not in resolved.parents:
        return {**base, "ready": False, "reason": "ForgeLoop OpenCLI plugin source resolves outside the repository."}
    if not path.is_dir():
        return {
            **base,
            "ready": False,
            "reason": f"ForgeLoop OpenCLI plugin source is missing: {OPENCLI_PLUGIN_REL}.",
        }
    if manifest.is_symlink() or not manifest.is_file():
        return {
            **base,
            "ready": False,
            "reason": "ForgeLoop OpenCLI plugin manifest is missing or unsafe.",
        }
    return {**base, "ready": True, "reason": ""}


def _has_symlink_ancestor(path: Path, root: Path) -> bool:
    current = path
    while current != root:
        if current.is_symlink():
            return True
        current = current.parent
    return False


def _version_from_command(executable: str | None, args: list[str]) -> str:
    if not executable:
        return ""
    result = _run_fixed(executable, args, timeout=DEFAULT_STATUS_TIMEOUT)
    if result.exit_code != 0 or result.timed_out:
        return ""
    return (result.stdout or result.stderr).strip().splitlines()[0] if (result.stdout or result.stderr).strip() else ""


def _run_fixed(executable: str, args: list[str], timeout: int) -> CommandRun:
    command = [executable, *args]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        return CommandRun(
            command,
            None,
            _truncate(exc.stdout or ""),
            _truncate(exc.stderr or ""),
            timed_out=True,
        )
    except OSError as exc:
        return CommandRun(command, None, "", _truncate(str(exc)), skipped=True, reason="command could not start")
    return CommandRun(
        command,
        completed.returncode,
        _truncate(completed.stdout),
        _truncate(completed.stderr),
    )


def _blocked_install(plan: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "executed": True,
        "status": "blocked",
        "plan": plan,
        "results": [
            CommandRun([], None, "", "", skipped=True, reason=reason).as_dict(),
        ],
    }


def _install_result(plan: dict[str, Any], results: list[CommandRun], status: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "executed": True,
        "status": status,
        "plan": plan,
        "results": [item.as_dict() for item in results],
    }


def _truncate(text: str, limit: int = 4000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n[truncated]"


def _display_command(command: list[str]) -> str:
    parts = []
    for part in command:
        if not part:
            continue
        if re.search(r"\s", part):
            parts.append(f'"{part}"')
        else:
            parts.append(part)
    return " ".join(parts)
