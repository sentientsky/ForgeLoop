from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LOCAL_SETUP_FILE = ".forgeloop.local.json"
ALL_SUPPORTED_ID = "all-supported"


SUPPORTED_TOOLS = [
    {
        "id": "claude-code",
        "label": "Claude Code",
        "support": "primary",
        "usage": "State of Code 2025: 57%; SonarSource 2026: Claude / Claude Code 48%",
        "entry_files": [
            "CLAUDE.md",
            ".claude/skills/pack-context/SKILL.md",
            ".claude/agents/architecture-reviewer.md",
            ".claude/agents/security-reviewer.md",
            ".claude/agents/test-reviewer.md",
            ".claude/agents/docs-reviewer.md",
        ],
        "next_steps": [
            "Open the repository in Claude Code.",
            "Ask Claude to read CLAUDE.md.",
            "Run python -m forgeloop pack \"your task\" . --limit 5 before loading memory.",
        ],
    },
    {
        "id": "codex",
        "label": "Codex",
        "support": "primary",
        "usage": "State of Code 2025: 23%; SonarSource 2026: OpenAI Codex 17%",
        "entry_files": [
            "AGENTS.md",
            "README.md",
            "docs/HOW_TO_USE.md",
        ],
        "next_steps": [
            "Start Codex from the repository root.",
            "Ask Codex to summarise active instructions.",
            "Use python -m forgeloop compat . to confirm entry files.",
        ],
    },
    {
        "id": "cursor",
        "label": "Cursor",
        "support": "supported",
        "usage": "State of Code 2025: 43%; SonarSource 2026: Cursor 21%",
        "entry_files": [
            "AGENTS.md",
            ".cursor/rules/forgeloop.mdc",
        ],
        "next_steps": [
            "Open the repository in Cursor.",
            "Check that .cursor/rules/forgeloop.mdc is active.",
            "Ask Cursor to run python -m forgeloop compat .",
        ],
    },
    {
        "id": "github-copilot",
        "label": "GitHub Copilot",
        "support": "supported",
        "usage": "SonarSource 2026: GitHub Copilot 75%; State of Code 2025: 30%",
        "entry_files": [
            "AGENTS.md",
            ".github/copilot-instructions.md",
        ],
        "next_steps": [
            "Use Copilot in a workspace containing this repository.",
            "Check that .github/copilot-instructions.md appears in Copilot references.",
            "Ask Copilot to follow AGENTS.md for validation commands.",
        ],
    },
    {
        "id": "gemini",
        "label": "Gemini CLI / Gemini Code Assist",
        "support": "supported",
        "usage": "SonarSource 2026: Gemini / Duet AI 31%",
        "entry_files": [
            "GEMINI.md",
            "AGENTS.md",
        ],
        "next_steps": [
            "Open Gemini CLI from the repository root.",
            "Ask Gemini to refresh or show project memory if needed.",
            "Run python -m forgeloop tokens \"your task\" . --tool gemini before broad memory reads.",
        ],
    },
    {
        "id": "windsurf",
        "label": "Windsurf",
        "support": "supported",
        "usage": "State of Code 2025: Windsurf 5%",
        "entry_files": [
            "AGENTS.md",
            ".windsurf/rules/forgeloop.md",
        ],
        "next_steps": [
            "Open the repository in Windsurf.",
            "Check that .windsurf/rules/forgeloop.md is active as a workspace rule.",
            "Use AGENTS.md as the portable fallback instruction file.",
        ],
    },
    {
        "id": "cline-roo",
        "label": "Cline / Roo Code",
        "support": "supported",
        "usage": "State of Code 2025: Cline 11%",
        "entry_files": [
            "AGENTS.md",
            ".clinerules/forgeloop.md",
            ".clineignore",
            ".roo/rules/forgeloop.md",
        ],
        "next_steps": [
            "Open the repository in VS Code with Cline or Roo Code.",
            "Check that workspace rules are active.",
            "Use .clineignore and FCP packets to keep startup context lean.",
        ],
    },
    {
        "id": "jetbrains-ai",
        "label": "JetBrains AI",
        "support": "beta",
        "usage": "SonarSource 2026: JetBrains AI 12%",
        "entry_files": [
            "AGENTS.md",
            ".aiassistant/rules/forgeloop.md",
        ],
        "next_steps": [
            "Open the repository in a JetBrains IDE with AI Assistant enabled.",
            "Confirm .aiassistant/rules/forgeloop.md is attached as a project rule.",
            "Keep tool-specific guidance short and defer details to AGENTS.md.",
        ],
    },
    {
        "id": "kiro",
        "label": "Kiro",
        "support": "beta",
        "usage": "State of Code 2025: Kiro 7%",
        "entry_files": [
            "AGENTS.md",
            ".kiro/steering/product.md",
            ".kiro/steering/tech.md",
            ".kiro/steering/structure.md",
        ],
        "next_steps": [
            "Open the repository in Kiro.",
            "Ask Kiro to review steering before planning.",
            "Keep steering concise and update it when the system changes.",
        ],
    },
    {
        "id": "opencode",
        "label": "OpenCode",
        "support": "supported",
        "usage": "Common open source agentic coding workflow",
        "entry_files": [
            "AGENTS.md",
            ".opencode/agents/forge-review.md",
        ],
        "next_steps": [
            "Start OpenCode from the repository root.",
            "Use AGENTS.md for standing instructions.",
            "Invoke the forge-review subagent for read-only review passes.",
        ],
    },
    {
        "id": "aider",
        "label": "Aider",
        "support": "portable",
        "usage": "Common open source agentic coding workflow",
        "entry_files": [
            "AGENTS.md",
            ".aider.conf.yml",
        ],
        "next_steps": [
            "Start Aider from the repository root.",
            "Let .aider.conf.yml load AGENTS.md as the shared instruction file.",
            "Run ForgeLoop validation before and after edits.",
        ],
    },
]


COMING_SOON_TOOLS = [
    {
        "id": "chatgpt",
        "label": "ChatGPT coding workspace",
        "usage": "SonarSource 2026: ChatGPT 74%",
        "reason": "Needs a tested repo attachment and instruction workflow.",
    },
    {
        "id": "amazon-q",
        "label": "Amazon Q Developer",
        "usage": "State of Code 2025: 9%; SonarSource 2026: Amazon Q 8%",
        "reason": "Needs AWS-focused setup and security notes.",
    },
    {
        "id": "zed",
        "label": "Zed",
        "usage": "State of Code 2025: 9%",
        "reason": "Needs Zed AI workflow testing.",
    },
    {
        "id": "replit",
        "label": "Replit",
        "usage": "State of Code 2025: 7%",
        "reason": "Needs hosted workspace safety guidance.",
    },
    {
        "id": "qwen-droid-pi",
        "label": "Qwen Code / Factory Droid / Pi",
        "usage": "Emerging Claude-compatible plugin and coding-agent workflows",
        "reason": "Needs native install verification on each tool.",
    },
]


INTEGRATION_ADD_ONS = [
    {
        "id": "opencli",
        "label": "OpenCLI integrated browser and desktop bridge",
        "usage": "Optional peer plugin for deterministic website, browser, Electron, and local CLI automation.",
        "command": "python -m forgeloop opencli plan .",
    },
]


@dataclass(frozen=True)
class SetupResult:
    selected_tool: str
    selected_label: str
    support: str
    config_path: Path
    wrote_config: bool
    dry_run: bool
    entry_files: list[str]
    missing_files: list[str]
    next_steps: list[str]

    def as_dict(self, root: Path) -> dict[str, Any]:
        return {
            "selected_tool": self.selected_tool,
            "selected_label": self.selected_label,
            "support": self.support,
            "config_path": str(self.config_path.relative_to(root)),
            "wrote_config": self.wrote_config,
            "dry_run": self.dry_run,
            "entry_files": self.entry_files,
            "missing_files": self.missing_files,
            "next_steps": self.next_steps,
        }


def setup_menu_text() -> str:
    lines = [
        "ForgeLoop setup",
        "",
        "Choose a tool profile already included in this template.",
        "This selection does not install or merge files into another repository.",
        "",
        "Select your primary AI coding tool:",
    ]
    for index, tool in enumerate(SUPPORTED_TOOLS, start=1):
        lines.append(f"{index}. {tool['label']} [{tool['support']}] - {tool['usage']}")
    lines.append(f"{len(SUPPORTED_TOOLS) + 1}. All supported tools [recommended for teams]")
    lines.append("")
    lines.append("Coming soon:")
    for tool in COMING_SOON_TOOLS:
        lines.append(f"- {tool['label']} - {tool['usage']}")
    lines.append("")
    lines.append("Optional integrations:")
    for add_on in INTEGRATION_ADD_ONS:
        lines.append(f"- {add_on['label']} - {add_on['command']}")
    return "\n".join(lines)


def run_setup(
    root: Path,
    tool_id: str | None = None,
    dry_run: bool = False,
    input_func: Callable[[str], str] | None = None,
) -> SetupResult:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Repository root does not exist: {root}")
    selected = _select_tool(tool_id, input_func)
    profile = _combined_profile() if selected == ALL_SUPPORTED_ID else _profile_by_id(selected)
    missing = [path for path in profile["entry_files"] if not (root / path).is_file()]
    config_path = _local_setup_path(root)
    wrote_config = False

    if not dry_run:
        payload = {
            "schema_version": 1,
            "selected_tool": profile["id"],
            "selected_label": profile["label"],
            "support": profile["support"],
            "entry_files": profile["entry_files"],
            "next_steps": profile["next_steps"],
        }
        _atomic_write_json(config_path, payload)
        wrote_config = True

    return SetupResult(
        selected_tool=profile["id"],
        selected_label=profile["label"],
        support=profile["support"],
        config_path=config_path,
        wrote_config=wrote_config,
        dry_run=dry_run,
        entry_files=list(profile["entry_files"]),
        missing_files=missing,
        next_steps=list(profile["next_steps"]),
    )


def format_setup_result(result: SetupResult, root: Path) -> str:
    lines = [
        f"Selected: {result.selected_label} ({result.support})",
        f"Local setup file: {result.config_path.relative_to(root)}",
        f"Written: {result.wrote_config}",
        "This records a local preference only; it does not install or merge profile files.",
    ]
    if result.missing_files:
        lines.append("Missing entry files:")
        lines.extend(f"- {path}" for path in result.missing_files)
    else:
        lines.append("All entry files are present.")
    lines.append("Next steps:")
    lines.extend(f"- {step}" for step in result.next_steps)
    return "\n".join(lines)


def supported_tool_ids() -> list[str]:
    return [str(tool["id"]) for tool in SUPPORTED_TOOLS] + [ALL_SUPPORTED_ID]


def _select_tool(tool_id: str | None, input_func: Callable[[str], str] | None) -> str:
    if tool_id:
        selected = tool_id.strip().lower()
        if selected not in supported_tool_ids():
            allowed = ", ".join(supported_tool_ids())
            raise ValueError(f"Unsupported tool '{tool_id}'. Allowed tools: {allowed}")
        return selected

    print(setup_menu_text())
    prompt = f"Enter 1-{len(SUPPORTED_TOOLS) + 1}: "
    answer = (input_func or input)(prompt).strip()
    try:
        choice = int(answer)
    except ValueError:
        raise ValueError("Menu choice must be a number") from None
    if choice < 1 or choice > len(SUPPORTED_TOOLS) + 1:
        raise ValueError("Menu choice is out of range")
    if choice == len(SUPPORTED_TOOLS) + 1:
        return ALL_SUPPORTED_ID
    return str(SUPPORTED_TOOLS[choice - 1]["id"])


def _profile_by_id(tool_id: str) -> dict[str, Any]:
    for tool in SUPPORTED_TOOLS:
        if tool["id"] == tool_id:
            return tool
    raise ValueError(f"Unknown tool profile: {tool_id}")


def _combined_profile() -> dict[str, Any]:
    entry_files: list[str] = []
    next_steps: list[str] = []
    for tool in SUPPORTED_TOOLS:
        entry_files.extend(path for path in tool["entry_files"] if path not in entry_files)
        next_steps.append(f"{tool['label']}: {tool['next_steps'][0]}")
    return {
        "id": ALL_SUPPORTED_ID,
        "label": "All supported tools",
        "support": "team",
        "usage": "Recommended when a team uses more than one AI coding tool",
        "entry_files": entry_files,
        "next_steps": [
            "Run python -m forgeloop compat .",
            "Use the tool-native entry file for each agent.",
            "Keep deep workflow details in docs instead of duplicating prompts.",
            *next_steps,
        ],
    }


def _local_setup_path(root: Path) -> Path:
    path = (root / LOCAL_SETUP_FILE).resolve()
    if path != root and root not in path.parents:
        raise ValueError("Local setup path escapes repository root")
    if _has_symlink_ancestor(path.parent, root):
        raise ValueError("Refusing to write setup inside a symlinked folder")
    if path.exists() and path.is_symlink():
        raise ValueError("Refusing to write setup through a symlink")
    return path


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def _has_symlink_ancestor(path: Path, root: Path) -> bool:
    root = root.resolve()
    current = path
    while current != root:
        if current.exists() and current.is_symlink():
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent
    return False
