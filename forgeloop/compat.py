from __future__ import annotations

from pathlib import Path
from typing import Any

COMPATIBILITY_TARGETS = [
    {
        "tool": "Claude Code",
        "priority": "primary",
        "required": [
            "CLAUDE.md",
            ".claude/skills/discover/SKILL.md",
            ".claude/skills/frame/SKILL.md",
            ".claude/skills/build/SKILL.md",
            ".claude/skills/check/SKILL.md",
            ".claude/skills/capture/SKILL.md",
            ".claude/skills/pack-context/SKILL.md",
            ".claude/skills/opencli-integrated/SKILL.md",
            ".claude/skills/verify-completion/SKILL.md",
            ".claude/skills/worktree-lifecycle/SKILL.md",
            ".claude/skills/align/SKILL.md",
            ".claude/skills/probe/SKILL.md",
            ".claude/skills/tdd/SKILL.md",
            ".claude/skills/deepen/SKILL.md",
            ".claude/skills/simplify/SKILL.md",
            ".claude/skills/refresh-memory/SKILL.md",
            ".claude/agents/architecture-reviewer.md",
            ".claude/agents/security-reviewer.md",
            ".claude/agents/test-reviewer.md",
            ".claude/agents/docs-reviewer.md",
            ".claude/agents/correctness-reviewer.md",
            ".claude/agents/reliability-reviewer.md",
            ".claude/agents/api-contract-reviewer.md",
            ".claude/agents/adversarial-reviewer.md",
        ],
        "optional": [
            ".claude/settings.example.json",
            ".claude/hooks/README.md",
        ],
    },
    {
        "tool": "Codex",
        "priority": "primary",
        "required": [
            "AGENTS.md",
            "README.md",
            "pyproject.toml",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
            "docs/WHAT_IT_IS.md",
            "docs/GETTING_STARTED.md",
            "docs/RELEASE_GUIDE.md",
        ],
    },
    {
        "tool": "Cursor",
        "priority": "supported",
        "required": [
            "AGENTS.md",
            ".cursor/rules/forgeloop.mdc",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
        ],
    },
    {
        "tool": "GitHub Copilot",
        "priority": "supported",
        "required": [
            "AGENTS.md",
            ".github/copilot-instructions.md",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
        ],
    },
    {
        "tool": "Gemini CLI / Gemini Code Assist",
        "priority": "supported",
        "required": [
            "GEMINI.md",
            "AGENTS.md",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
            "docs/standards/token-measurement-standard.md",
        ],
    },
    {
        "tool": "Windsurf",
        "priority": "supported",
        "required": [
            "AGENTS.md",
            ".windsurf/rules/forgeloop.md",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
        ],
    },
    {
        "tool": "Cline / Roo Code",
        "priority": "supported",
        "required": [
            "AGENTS.md",
            ".clinerules/forgeloop.md",
            ".clineignore",
            ".roo/rules/forgeloop.md",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
        ],
    },
    {
        "tool": "JetBrains AI",
        "priority": "beta",
        "required": [
            "AGENTS.md",
            ".aiassistant/rules/forgeloop.md",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
        ],
    },
    {
        "tool": "Kiro",
        "priority": "beta",
        "required": [
            "AGENTS.md",
            ".kiro/steering/product.md",
            ".kiro/steering/tech.md",
            ".kiro/steering/structure.md",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
        ],
    },
    {
        "tool": "OpenCode",
        "priority": "supported",
        "required": [
            "AGENTS.md",
            ".opencode/agents/forge-review.md",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
        ],
    },
    {
        "tool": "Aider",
        "priority": "portable",
        "required": [
            "AGENTS.md",
            ".aider.conf.yml",
        ],
        "optional": [
            "docs/compatibility/ai-coding-tools.md",
        ],
    },
    {
        "tool": "OpenCLI integrated plugin",
        "priority": "supported",
        "required": [
            "docs/integrations/opencli.md",
            "integrations/opencli/opencli-plugin.json",
            "integrations/opencli/package.json",
            ".claude/skills/opencli-integrated/SKILL.md",
        ],
        "optional": [
            "docs/research/2026-05-11-opencli-review.md",
        ],
    },
    {
        "tool": "Generic AI coding agents",
        "priority": "portable",
        "required": [
            "AGENTS.md",
            "README.md",
            "docs/HOW_TO_USE.md",
        ],
        "optional": [
            "docs/GITHUB_PAGE.md",
        ],
    },
]


def compatibility_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    targets = []
    for target in COMPATIBILITY_TARGETS:
        required = [_file_status(root, rel_path) for rel_path in target["required"]]
        optional = [_file_status(root, rel_path) for rel_path in target["optional"]]
        targets.append(
            {
                "tool": target["tool"],
                "priority": target["priority"],
                "ready": all(item["exists"] for item in required),
                "required": required,
                "optional": optional,
            }
        )
    return {
        "schema_version": 1,
        "root": str(root),
        "targets": targets,
    }


def format_compatibility_report(report: dict[str, Any]) -> str:
    lines = ["ForgeLoop compatibility report:"]
    for target in report["targets"]:
        ready = "ready" if target["ready"] else "missing files"
        lines.append(f"- {target['tool']} ({target['priority']}): {ready}")
        missing = [item["path"] for item in target["required"] if not item["exists"]]
        if missing:
            lines.append(f"  missing: {', '.join(missing)}")
    return "\n".join(lines)


def _file_status(root: Path, rel_path: str) -> dict[str, Any]:
    path = root / rel_path
    return {
        "path": rel_path,
        "exists": path.is_file(),
        "bytes": path.stat().st_size if path.is_file() else 0,
    }
