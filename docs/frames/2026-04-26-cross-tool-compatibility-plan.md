---
type: frame
date: 2026-04-26
status: current
tags: [compatibility, claude-code, codex, cursor]
---

# Cross-Tool Compatibility Plan

## Goal

Make ForgeLoop usable by Claude Code, Codex, Cursor, and generic AI coding tools while keeping Claude Code as the richest integration.

## Scope

- Add `AGENTS.md` for Codex and generic agents.
- Add `.cursor/rules/forgeloop.mdc` for Cursor Agent.
- Add `.github/copilot-instructions.md` for GitHub Copilot.
- Add `python -m forgeloop compat .` to check entry files.
- Add `python -m forgeloop setup .` for menu-driven onboarding.
- Document tool support and risks.
- Keep all tool instructions compact.

## Non-Goals

- Do not copy large sections into every tool file.
- Do not add active hooks for every tool.
- Do not depend on hosted memory services.
- Do not promise identical behaviour across tools.

## Compatibility Strategy

ForgeLoop has one core loop and multiple tool-native entry points.

Claude Code gets skills and reviewer agents.

Codex gets `AGENTS.md`.

Cursor gets an MDC project rule and `AGENTS.md`.

GitHub Copilot gets repository custom instructions and `AGENTS.md`.

Generic agents get `README.md`, `AGENTS.md`, and `docs/HOW_TO_USE.md`.

## Validation

Run:

```bash
python -m forgeloop compat .
python -m forgeloop validate .
python -m unittest discover -s tests
```

## Risks

- Tools may load instructions differently in future versions.
- Instruction files are soft guidance, not security controls.
- Cursor rules can be ignored in long or overloaded sessions.
- Codex instruction chains can be truncated if files become too large.
- Claude-specific skills do not automatically transfer to other agents.

## Follow-Up

Add a generated compatibility audit to CI after ForgeLoop becomes a Git repository.
