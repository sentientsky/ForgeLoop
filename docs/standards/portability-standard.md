---
type: standard
date: 2026-04-17
status: current
tags: [portability, windows, macos, linux]
---

# Portability Standard

ForgeLoop should work on Windows, macOS, and Linux.

## Rules

- Use Python standard library features where practical.
- Use `pathlib` for paths in Python code.
- Avoid shell-only workflows for core behaviour.
- Keep active automation cross-platform.
- Do not assume a Unix home directory.
- Do not assume a specific terminal encoding.
- Keep file names simple and ASCII.
- Test on more than one Python version.

## Command Design

Core commands should work as:

```bash
python -m forgeloop validate .
python -m forgeloop index .
python -m forgeloop status .
python -m forgeloop new frame "Add export button" .
python -m forgeloop hook-simulate PreCompact .
```

Package installs may add the shorter `forgeloop` command, but the module form is the portable baseline.

## Generated Files

Generated files must be deterministic.

That means:

- stable ordering
- no machine-specific absolute paths
- no random IDs
- no local usernames
- no private environment data

## AI Tool Compatibility

ForgeLoop should expose compact entry points for common AI coding tools:

- Claude Code: `CLAUDE.md`, `.claude/skills/`, `.claude/agents/`
- Codex: `AGENTS.md`
- Cursor: `.cursor/rules/*.mdc`
- Generic agents: `AGENTS.md`, `README.md`, `docs/HOW_TO_USE.md`

Run this check after editing compatibility files:

```bash
python -m forgeloop compat .
```
