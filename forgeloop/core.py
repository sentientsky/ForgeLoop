from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from . import __version__
from .secrets import find_repo_env_files


MAX_FILE_BYTES = 1_000_000
REQUIRED_FILES = [
    "README.md",
    "CLAUDE.md",
    "AGENTS.md",
    "GEMINI.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "GOVERNANCE.md",
    ".github/copilot-instructions.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/codeql.yml",
    ".github/workflows/release.yml",
    ".github/workflows/scorecard.yml",
    ".clineignore",
    ".aider.conf.yml",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    ".env.example",
    "pyproject.toml",
    "docs/WHAT_IT_IS.md",
    "docs/GETTING_STARTED.md",
    "docs/HOW_TO_USE.md",
    "docs/RELEASE_GUIDE.md",
    "docs/FAQ.md",
    "docs/INSTALLATION.md",
    "docs/COMMAND_REFERENCE.md",
    "docs/TROUBLESHOOTING.md",
    "docs/PUBLISHING.md",
    "docs/MAINTAINER_GUIDE.md",
    "docs/GITHUB_SETUP.md",
    "docs/integrations/opencli.md",
    "integrations/opencli/opencli-plugin.json",
    "tests/package_smoke.py",
]
REQUIRED_DIRS = [
    ".claude/skills/discover",
    ".claude/skills/frame",
    ".claude/skills/build",
    ".claude/skills/check",
    ".claude/skills/capture",
    ".claude/agents",
    ".claude/skills/opencli-integrated",
    ".claude/skills/verify-completion",
    ".claude/skills/worktree-lifecycle",
    ".claude/skills/align",
    ".claude/skills/probe",
    ".claude/skills/tdd",
    ".claude/skills/deepen",
    ".claude/skills/simplify",
    ".claude/skills/refresh-memory",
    "docs/discoveries",
    "docs/frames",
    "docs/builds",
    "docs/checks",
    "docs/captures",
    "docs/solutions",
    "docs/standards",
    "docs/compatibility",
    "docs/compatibility/deployment-evals",
    "docs/integrations",
    "docs/language",
    "docs/decisions",
    "docs/benchmarks",
    "docs/palace/indexes",
    ".github/ISSUE_TEMPLATE",
    ".cursor/rules",
    ".windsurf/rules",
    ".clinerules",
    ".roo/rules",
    ".aiassistant/rules",
    ".kiro/steering",
    ".opencode/agents",
    "integrations/opencli",
    "memory",
    "templates",
    "examples",
    "examples/skill-evals",
]
MEMORY_FOLDERS = [
    "docs/captures",
    "docs/solutions",
    "docs/palace/drawers",
    "docs/palace/entities",
    "docs/palace/timelines",
    "docs/decisions",
]
SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
    "node_modules",
    ".opencli",
}
ALLOWED_NOTE_KINDS = {
    "discover": ("templates/discovery-template.md", "docs/discoveries", "discovery"),
    "discovery": ("templates/discovery-template.md", "docs/discoveries", "discovery"),
    "frame": ("templates/frame-template.md", "docs/frames", "frame"),
    "build": ("templates/build-template.md", "docs/builds", "build"),
    "check": ("templates/check-template.md", "docs/checks", "check"),
    "capture": ("templates/capture-template.md", "docs/captures", "capture"),
    "handoff": ("templates/handoff-template.md", "docs/captures", "handoff"),
    "drawer": ("templates/palace-drawer-template.md", "docs/palace/drawers", "drawer"),
    "solution": ("templates/solution-template.md", "docs/solutions", "solution"),
    "entity": ("templates/entity-template.md", "docs/palace/entities", "entity"),
    "timeline": ("templates/timeline-template.md", "docs/palace/timelines", "timeline"),
    "decision": ("templates/decision-template.md", "docs/decisions", "decision"),
    "probe": ("templates/probe-template.md", "docs/checks", "probe"),
    "tdd": ("templates/tdd-cycle-template.md", "docs/builds", "tdd-cycle"),
    "memory-refresh": ("templates/memory-refresh-template.md", "docs/checks", "memory-refresh"),
    "language": ("templates/project-language-template.md", "docs/language", "project-language"),
}
ALLOWED_HOOK_EVENTS = {"Stop", "PreCompact", "SessionEnd"}
SAFE_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9_.-]{1,120}$")
PINNED_ACTION_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str
    path: Path | None = None

    def as_dict(self, root: Path) -> dict[str, str]:
        item = {
            "level": self.level,
            "code": self.code,
            "message": self.message,
        }
        if self.path:
            item["path"] = str(self.path.relative_to(root))
        return item


@dataclass(frozen=True)
class IndexResult:
    record_count: int
    json_path: Path
    markdown_path: Path
    changed: bool = False


@dataclass(frozen=True)
class NewNoteResult:
    path: Path
    created: bool


@dataclass(frozen=True)
class HookSimulation:
    event: str
    action: str
    reason: str
    details: dict[str, Any]


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse the small frontmatter subset ForgeLoop uses.

    This intentionally avoids a YAML dependency. It supports simple key/value
    pairs and bracket lists such as `tags: [memory, safety]`.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, text

    data: dict[str, Any] = {}
    for raw in lines[1:end]:
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [part.strip().strip("\"'") for part in inner.split(",") if part.strip()]
        elif value in {"true", "false"}:
            data[key] = value == "true"
        else:
            data[key] = value.strip("\"'")
    return data, "\n".join(lines[end + 1 :])


def validate_repo(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    root = root.resolve()

    for rel_path in REQUIRED_FILES:
        path = root / rel_path
        if not path.is_file():
            findings.append(Finding("error", "missing-file", f"Missing required file: {rel_path}", path))

    for rel_path in REQUIRED_DIRS:
        path = root / rel_path
        if not path.is_dir():
            findings.append(Finding("error", "missing-dir", f"Missing required folder: {rel_path}", path))
        elif path.is_symlink():
            findings.append(Finding("error", "symlink-dir", f"Required folder must not be a symlink: {rel_path}", path))

    findings.extend(_validate_versions(root))
    findings.extend(_validate_skills(root))
    findings.extend(_validate_agents(root))
    findings.extend(_validate_templates(root))
    findings.extend(_validate_json_files(root))
    findings.extend(_validate_directory_safety(root))
    findings.extend(_validate_file_safety(root))
    findings.extend(_validate_github_workflows(root))
    findings.extend(_validate_cursor_rules(root))
    findings.extend(_validate_native_tool_profiles(root))
    findings.extend(_validate_opencli_integration(root))
    findings.extend(_validate_repo_env_files(root))
    findings.extend(_validate_memory_notes(root))
    return sorted(findings, key=lambda item: (item.level != "error", item.code, str(item.path or "")))


def format_findings(findings: list[Finding], root: Path) -> str:
    if not findings:
        return "ForgeLoop validation passed."

    lines = ["ForgeLoop validation findings:"]
    for finding in findings:
        location = ""
        if finding.path:
            try:
                location = f" ({finding.path.relative_to(root)})"
            except ValueError:
                location = f" ({finding.path})"
        lines.append(f"- {finding.level.upper()} {finding.code}{location}: {finding.message}")
    return "\n".join(lines)


def build_memory_index(root: Path, check: bool = False) -> IndexResult:
    root = root.resolve()
    records = collect_memory_records(root)
    json_path = root / "docs/palace/indexes/memory-index.json"
    markdown_path = root / "docs/palace/indexes/memory-index.md"
    json_text = json.dumps(
        {
            "schema_version": 1,
            "generated_by": f"forgeloop {__version__}",
            "record_count": len(records),
            "records": records,
        },
        indent=2,
    ) + "\n"
    markdown_text = _render_memory_index_markdown(records)

    changed = _file_text(json_path) != json_text or _file_text(markdown_path) != markdown_text
    if not check:
        _atomic_write(json_path, json_text)
        _atomic_write(markdown_path, markdown_text)
    return IndexResult(len(records), json_path, markdown_path, changed)


def create_note(
    root: Path,
    kind: str,
    title: str,
    note_date: date | None = None,
    force: bool = False,
) -> NewNoteResult:
    root = root.resolve()
    kind_key = kind.strip().lower()
    if kind_key not in ALLOWED_NOTE_KINDS:
        allowed = ", ".join(sorted(ALLOWED_NOTE_KINDS))
        raise ValueError(f"Unsupported note kind '{kind}'. Allowed kinds: {allowed}")

    clean_title = _clean_title(title)
    slug = slugify(clean_title)
    current_date = note_date or date.today()
    template_rel, output_rel, _type_name = ALLOWED_NOTE_KINDS[kind_key]
    template_path = _safe_join(root, template_rel)
    output_dir = _safe_join(root, output_rel)

    if not template_path.is_file():
        raise FileNotFoundError(f"Template not found: {template_rel}")
    if _has_symlink_ancestor(output_dir, root):
        raise ValueError(f"Output folder uses a symlink: {output_rel}")

    output_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{current_date.isoformat()}-{slug}.md"
    if kind_key in {"solution", "entity"}:
        file_name = f"{slug}.md"
    output_path = _safe_join(output_dir, file_name)

    if _has_symlink_ancestor(output_path.parent, root):
        raise ValueError("Refusing to write inside a symlinked folder")
    if output_path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file: {output_path.relative_to(root)}")

    template = template_path.read_text(encoding="utf-8")
    content = _fill_template(template, clean_title, current_date)
    if _contains_secret(content):
        raise ValueError("Generated note appears to contain a secret")

    if force:
        _atomic_write(output_path, content)
    else:
        _exclusive_write(output_path, content)
    return NewNoteResult(output_path, True)


def simulate_hook_event(
    root: Path,
    event: str,
    payload: dict[str, Any] | None = None,
    interval: int = 15,
) -> HookSimulation:
    root = root.resolve()
    if event not in ALLOWED_HOOK_EVENTS:
        allowed = ", ".join(sorted(ALLOWED_HOOK_EVENTS))
        raise ValueError(f"Unsupported hook event '{event}'. Allowed events: {allowed}")
    if interval < 1 or interval > 100:
        raise ValueError("Interval must be between 1 and 100")
    if payload is None:
        payload = {}
    if not isinstance(payload, dict):
        raise ValueError("Hook payload must be a JSON object")

    session_id = _safe_session_id(payload.get("session_id", "unknown"))
    stop_hook_active = bool(payload.get("stop_hook_active", False))
    message_count = _safe_int(payload.get("message_count"), default=0, minimum=0, maximum=100_000)

    details = {
        "session_id": session_id,
        "message_count": message_count,
        "interval": interval,
        "dry_run": True,
        "executes_commands": False,
    }

    transcript_path = payload.get("transcript_path")
    if transcript_path:
        details["transcript_path_accepted"] = False
        details["transcript_path_reason"] = "Dry-run simulation does not read transcript files."

    if event == "PreCompact":
        return HookSimulation(
            event,
            "remind-capture",
            "PreCompact is a high-value capture point. Dry run recommends saving current task state.",
            details,
        )

    if event == "SessionEnd":
        return HookSimulation(
            event,
            "remind-capture",
            "SessionEnd should prompt a capture check for non-trivial work.",
            details,
        )

    if stop_hook_active:
        return HookSimulation(
            event,
            "allow-stop",
            "A capture reminder is already active, so the next stop should be allowed.",
            details,
        )

    if message_count >= interval:
        return HookSimulation(
            event,
            "remind-capture",
            "Message count reached the dry-run interval.",
            details,
        )

    return HookSimulation(
        event,
        "allow-stop",
        "Message count has not reached the dry-run interval.",
        details,
    )


def collect_memory_records(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for folder in MEMORY_FOLDERS:
        base = root / folder
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.is_symlink() or path.name.upper() == "README.MD":
                continue
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            text = path.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(text)
            title = _first_heading(body) or path.stem.replace("-", " ").title()
            records.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "title": title,
                    "type": frontmatter.get("type", _type_from_path(path)),
                    "status": frontmatter.get("status", ""),
                    "tags": frontmatter.get("tags", []),
                    "valid_from": frontmatter.get("valid_from", ""),
                    "valid_to": frontmatter.get("valid_to", ""),
                    "supersedes": frontmatter.get("supersedes", ""),
                    "superseded_by": frontmatter.get("superseded_by", ""),
                }
            )
    return records


def repo_status(root: Path) -> dict[str, Any]:
    root = root.resolve()
    markdown_files = [path for path in _iter_files(root) if path.suffix.lower() == ".md"]
    skills = list((root / ".claude/skills").glob("*/SKILL.md"))
    agents = list((root / ".claude/agents").glob("*.md"))
    return {
        "markdown_files": len(markdown_files),
        "skills": len(skills),
        "agents": len(agents),
        "memory_records": len(collect_memory_records(root)),
        "index_exists": (root / "docs/palace/indexes/memory-index.json").is_file(),
    }


def _validate_github_workflows(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    workflow_dir = root / ".github/workflows"
    if not workflow_dir.is_dir():
        return findings

    workflow_paths = sorted([*workflow_dir.glob("*.yml"), *workflow_dir.glob("*.yaml")])
    for path in workflow_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^\s*pull_request_target\s*:", text, re.MULTILINE):
            findings.append(
                Finding(
                    "error",
                    "risky-workflow-trigger",
                    "pull_request_target is forbidden because it can expose privileged workflow context",
                    path,
                )
            )
        if not re.search(r"^\s*permissions\s*:", text, re.MULTILINE):
            findings.append(
                Finding(
                    "error",
                    "workflow-permissions",
                    "Workflow must declare explicit least-privilege permissions",
                    path,
                )
            )
        if re.search(r"^\s*permissions\s*:\s*write-all\s*$", text, re.MULTILINE):
            findings.append(
                Finding(
                    "error",
                    "workflow-write-all",
                    "Workflow must not grant write-all permissions",
                    path,
                )
            )

        for line_number, line in enumerate(text.splitlines(), start=1):
            match = re.search(r"\buses:\s*([^\s#]+)", line)
            if not match:
                continue
            action = match.group(1).strip("\"'")
            if action.startswith(("./", "docker://")):
                continue
            _name, separator, reference = action.rpartition("@")
            if not separator or not PINNED_ACTION_RE.fullmatch(reference):
                findings.append(
                    Finding(
                        "error",
                        "unpinned-action",
                        f"External action on line {line_number} must be pinned to a full commit SHA: {action}",
                        path,
                    )
                )
    return findings


def _validate_versions(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject.read_text(encoding="utf-8"), re.M)
        if match and match.group(1) != __version__:
            findings.append(
                Finding(
                    "error",
                    "version-mismatch",
                    f"pyproject version {match.group(1)} does not match package version {__version__}",
                    pyproject,
                )
            )
    return findings


def _validate_skills(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skills_dir = root / ".claude/skills"
    if not skills_dir.is_dir():
        return findings
    for skill_path in sorted(skills_dir.glob("*/SKILL.md")):
        frontmatter, body = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
        expected_name = skill_path.parent.name
        if frontmatter.get("name") != expected_name:
            findings.append(
                Finding("error", "skill-name", f"Skill name should be '{expected_name}'", skill_path)
            )
        if not frontmatter.get("description"):
            findings.append(Finding("error", "skill-description", "Skill needs a description", skill_path))
        if "## Rules" not in body:
            findings.append(Finding("warning", "skill-rules", "Skill should include a Rules section", skill_path))
        if "## Output" not in body:
            findings.append(Finding("warning", "skill-output", "Skill should include an Output section", skill_path))
    return findings


def _validate_agents(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    agents_dir = root / ".claude/agents"
    if not agents_dir.is_dir():
        return findings
    for agent_path in sorted(agents_dir.glob("*.md")):
        frontmatter, _body = parse_frontmatter(agent_path.read_text(encoding="utf-8"))
        expected_name = agent_path.stem
        if frontmatter.get("name") != expected_name:
            findings.append(
                Finding("error", "agent-name", f"Agent name should be '{expected_name}'", agent_path)
            )
        if not frontmatter.get("description"):
            findings.append(Finding("error", "agent-description", "Agent needs a description", agent_path))
        tools = str(frontmatter.get("tools", ""))
        if expected_name.endswith("reviewer") and re.search(r"\b(Write|Edit)\b", tools):
            findings.append(
                Finding("error", "reviewer-write-access", "Reviewer agents should not edit files", agent_path)
            )
    return findings


def _validate_templates(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    templates_dir = root / "templates"
    if not templates_dir.is_dir():
        return findings
    for path in sorted(templates_dir.glob("*.md")):
        frontmatter, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not frontmatter.get("type"):
            findings.append(Finding("warning", "template-type", "Template should define a type", path))
    return findings


def _validate_json_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_files(root):
        if path.suffix.lower() != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(Finding("error", "json-invalid", f"Invalid JSON: {exc}", path))
    return findings


def _validate_directory_safety(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for current_root, dirs, _files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        for dir_name in list(dirs):
            path = Path(current_root) / dir_name
            if path.is_symlink():
                findings.append(Finding("error", "symlink-dir", "Repository folders must not be symlinks", path))
                dirs.remove(dir_name)
    return findings


def _validate_file_safety(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_files(root):
        if path.is_symlink():
            findings.append(Finding("error", "symlink-file", "Repository files must not be symlinks", path))
            continue
        try:
            stat = path.stat()
        except OSError as exc:
            findings.append(Finding("error", "file-stat", f"Cannot inspect file: {exc}", path))
            continue
        if stat.st_size > MAX_FILE_BYTES:
            findings.append(
                Finding("warning", "large-file", f"File is larger than {MAX_FILE_BYTES} bytes", path)
            )
        if path.suffix.lower() not in {
            ".md",
            ".mdc",
            ".py",
            ".json",
            ".js",
            ".ts",
            ".toml",
            ".yml",
            ".yaml",
            ".txt",
            ".sh",
            ".ps1",
        }:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            findings.append(Finding("error", "file-read", f"Cannot read file safely: {exc}", path))
            continue
        if _contains_secret(text):
            findings.append(Finding("error", "possible-secret", "Possible secret or token found", path))
        is_claude_settings = ".claude" in path.parts and path.name.startswith("settings")
        if path.suffix.lower() in {".sh", ".ps1"} or ".claude/hooks" in path.as_posix() or is_claude_settings:
            if _contains_risky_command(text):
                findings.append(Finding("error", "risky-hook", "Risky hook command pattern found", path))
    return findings


def _validate_cursor_rules(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    rules_dir = root / ".cursor/rules"
    if not rules_dir.is_dir():
        return findings
    for path in sorted(rules_dir.glob("*.mdc")):
        frontmatter, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not frontmatter:
            findings.append(Finding("error", "cursor-frontmatter", "Cursor rule needs MDC frontmatter", path))
            continue
        if not frontmatter.get("description"):
            findings.append(Finding("error", "cursor-description", "Cursor rule needs a description", path))
        if "alwaysApply" not in frontmatter:
            findings.append(Finding("warning", "cursor-always-apply", "Cursor rule should set alwaysApply", path))
        if not body.strip():
            findings.append(Finding("warning", "cursor-empty-rule", "Cursor rule should include instructions", path))
    return findings


def _validate_native_tool_profiles(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    checks = [
        ("GEMINI.md", "GEMINI.md should point Gemini to AGENTS.md and ForgeLoop token commands", ["AGENTS.md", "forgeloop tokens"]),
        (
            ".windsurf/rules/forgeloop.md",
            "Windsurf rule should stay concise and point to AGENTS.md",
            ["AGENTS.md", "forgeloop pack"],
        ),
        (
            ".clinerules/forgeloop.md",
            "Cline rule should point to AGENTS.md and avoid broad memory loading",
            ["AGENTS.md", "forgeloop pack"],
        ),
        (
            ".roo/rules/forgeloop.md",
            "Roo rule should point to AGENTS.md and avoid broad memory loading",
            ["AGENTS.md", "forgeloop pack"],
        ),
        (
            ".aiassistant/rules/forgeloop.md",
            "JetBrains AI rule should point to AGENTS.md",
            ["AGENTS.md"],
        ),
        (
            ".opencode/agents/forge-review.md",
            "OpenCode review agent should be read-only",
            ["mode: subagent", "edit: deny"],
        ),
        (
            ".aider.conf.yml",
            "Aider config should load AGENTS.md",
            ["AGENTS.md"],
        ),
    ]
    for rel_path, message, needles in checks:
        path = root / rel_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in needles:
            if needle not in text:
                findings.append(Finding("warning", "tool-profile-guidance", message, path))
                break

    windsurf = root / ".windsurf/rules/forgeloop.md"
    if windsurf.is_file() and windsurf.stat().st_size > 12_000:
        findings.append(
            Finding("warning", "windsurf-rule-size", "Windsurf workspace rules should stay under 12,000 characters", windsurf)
        )

    clineignore = root / ".clineignore"
    if clineignore.is_file():
        text = clineignore.read_text(encoding="utf-8", errors="replace")
        for needle in ["__pycache__/", ".git/", ".venv/"]:
            if needle not in text:
                findings.append(Finding("warning", "clineignore-gap", f".clineignore should include {needle}", clineignore))

    for rel_path in [".kiro/steering/product.md", ".kiro/steering/tech.md", ".kiro/steering/structure.md"]:
        path = root / rel_path
        if path.is_file() and path.stat().st_size > 8_000:
            findings.append(Finding("warning", "kiro-steering-size", "Kiro steering files should stay concise", path))
    return findings


def _validate_opencli_integration(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    manifest = root / "integrations/opencli/opencli-plugin.json"
    docs = root / "docs/integrations/opencli.md"
    if manifest.is_file():
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return findings
        if payload.get("name") != "forgeloop":
            findings.append(Finding("error", "opencli-plugin-name", "OpenCLI plugin name should be forgeloop", manifest))
        if not payload.get("opencli"):
            findings.append(Finding("error", "opencli-plugin-range", "OpenCLI plugin should declare an opencli range", manifest))
        if not payload.get("description"):
            findings.append(Finding("error", "opencli-plugin-description", "OpenCLI plugin needs a description", manifest))
    if docs.is_file():
        text = docs.read_text(encoding="utf-8", errors="replace").lower()
        if "integrated" not in text or "not copied" not in text:
            findings.append(
                Finding(
                    "warning",
                    "opencli-originality-note",
                    "OpenCLI integration docs should state that OpenCLI is integrated, not copied",
                    docs,
                )
            )
    return findings


def _validate_repo_env_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in find_repo_env_files(root):
        findings.append(
            Finding(
                "error",
                "env-file-in-repo",
                "Real .env-style files must live outside the repository. Keep only .env.example here.",
                path,
            )
        )
    env_example = root / ".env.example"
    if env_example.is_file() and _contains_secret(env_example.read_text(encoding="utf-8", errors="replace")):
        findings.append(
            Finding(
                "error",
                "env-example-secret",
                ".env.example must contain blank or placeholder values only.",
                env_example,
            )
        )
    return findings


def _validate_memory_notes(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for folder in MEMORY_FOLDERS:
        base = root / folder
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name.upper() == "README.MD":
                continue
            frontmatter, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
            if not frontmatter:
                findings.append(Finding("warning", "memory-frontmatter", "Memory note needs frontmatter", path))
                continue
            if "status" not in frontmatter:
                findings.append(Finding("warning", "memory-status", "Memory note should include status", path))
            if "valid_from" not in frontmatter and frontmatter.get("type") in {"capture", "palace-drawer"}:
                findings.append(
                    Finding("warning", "memory-valid-from", "Time-aware memory should include valid_from", path)
                )
    return findings


def _iter_files(root: Path):
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        for file_name in files:
            yield Path(current_root) / file_name


def _contains_secret(text: str) -> bool:
    patterns = [
        r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----",
        r"\bsk-ant-[A-Za-z0-9_-]{20,}",
        r"\bsk-proj-[A-Za-z0-9_-]{20,}",
        r"\bghp_[A-Za-z0-9]{20,}",
        r"\bgithub_pat_[A-Za-z0-9_]{20,}",
        r"\bAKIA[0-9A-Z]{16}\b",
        r"(?i)\b(api[_-]?key|token|secret|password)\s*=\s*['\"]?(?!your|example|changeme|redacted|none)[A-Za-z0-9_\-]{12,}",
    ]
    return any(re.search(pattern, text) for pattern in patterns)


def _contains_risky_command(text: str) -> bool:
    patterns = [
        r"\beval\s+",
        r"\brm\s+-rf\s+[/~$]",
        r"curl\b.*\|\s*(sh|bash)",
        r"Invoke-Expression",
        r"chmod\s+777",
        r"shell\s*=\s*True",
    ]
    return any(re.search(pattern, text, flags=re.I | re.S) for pattern in patterns)


def _first_heading(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _type_from_path(path: Path) -> str:
    parts = set(path.parts)
    if "solutions" in parts:
        return "solution"
    if "captures" in parts:
        return "capture"
    if "entities" in parts:
        return "entity"
    if "timelines" in parts:
        return "timeline"
    if "decisions" in parts:
        return "decision"
    return "memory-record"


def _render_memory_index_markdown(records: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        "type: memory-index",
        "date: generated",
        "status: generated",
        "tags: [memory, index]",
        "---",
        "",
        "# Memory Index",
        "",
        "This file is generated by `python -m forgeloop index .`.",
        "",
        f"Record count: {len(records)}",
        "",
    ]
    by_type: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_type.setdefault(str(record["type"]), []).append(record)
    for record_type in sorted(by_type):
        lines.append(f"## {record_type}")
        lines.append("")
        for record in by_type[record_type]:
            path = record["path"]
            title = record["title"]
            status = record.get("status") or "unknown"
            lines.append(f"- [{title}](../../../{path}) - {status}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _file_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def _exclusive_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _safe_join(root: Path, relative_path: str | Path) -> Path:
    candidate = (root / relative_path).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"Path escapes repository root: {relative_path}")
    return candidate


def _has_symlink_ancestor(path: Path, root: Path) -> bool:
    root = root.resolve()
    current = path.resolve()
    while current != root:
        if current.is_symlink():
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent
    return False


def _clean_title(title: str) -> str:
    clean = " ".join(title.strip().split())
    if not clean:
        raise ValueError("Title cannot be empty")
    if len(clean) > 120:
        raise ValueError("Title must be 120 characters or fewer")
    if _contains_secret(clean):
        raise ValueError("Title appears to contain a secret")
    return clean


def slugify(value: str) -> str:
    ascii_value = value.encode("ascii", "ignore").decode("ascii").lower()
    ascii_value = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    ascii_value = re.sub(r"-{2,}", "-", ascii_value)
    if not ascii_value:
        raise ValueError("Title must contain at least one ASCII letter or number")
    if ascii_value in {".", "..", "con", "prn", "aux", "nul"}:
        raise ValueError("Title produces a reserved file name")
    return ascii_value[:80].strip("-")


def _fill_template(template: str, title: str, note_date: date) -> str:
    return (
        template.replace("YYYY-MM-DD", note_date.isoformat())
        .replace("short task name", title)
        .replace("Short Task Name", title)
        .replace("Short Memory Name", title)
    )


def _safe_session_id(raw: Any) -> str:
    value = str(raw or "unknown")[:120]
    value = re.sub(r"[^A-Za-z0-9_.-]", "_", value)
    if not value or not SAFE_IDENTIFIER_RE.fullmatch(value):
        return "unknown"
    return value


def _safe_int(raw: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, value))
