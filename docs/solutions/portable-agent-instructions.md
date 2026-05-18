---
type: solution
status: current
tags: [compatibility, agents, codex, cursor, claude-code]
---

# Portable Agent Instructions

## Problem

AI coding tools do not share one instruction format.

Claude Code uses `CLAUDE.md`, skills, agents, and hooks.

Codex uses `AGENTS.md`.

Cursor uses project rules in `.cursor/rules/` and can also use `AGENTS.md`.

GitHub Copilot uses `.github/copilot-instructions.md` and can use agent instructions.

## Solution

Keep the workflow portable and the entry files small.

Use:

- `CLAUDE.md` for Claude Code
- `AGENTS.md` for Codex and generic agents
- `.cursor/rules/forgeloop.mdc` for Cursor
- `.github/copilot-instructions.md` for GitHub Copilot
- `docs/HOW_TO_USE.md` for human-readable usage
- `python -m forgeloop compat .` to check required files

## Rule

Do not duplicate the full system across every tool.

Each tool file should explain:

- the five-stage loop
- the packet-first memory command
- validation commands
- safety rules
- where to find deeper docs

## Benefit

ForgeLoop stays compatible without becoming prompt spaghetti.
