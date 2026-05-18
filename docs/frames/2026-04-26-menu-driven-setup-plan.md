---
type: frame
date: 2026-04-26
status: current
tags: [setup, compatibility, install, ai-coding-tools]
---

# Menu-Driven Setup Plan

## Goal

Make ForgeLoop installation feel guided.

Users should be able to choose their AI coding tool from a menu instead of reading all compatibility docs first.

## Scope

- Add `python -m forgeloop setup .`.
- Add `--tool` for non-interactive setup.
- Add `--dry-run` for demos, docs, and tests.
- Add `--list` to show supported and coming-soon tools.
- Add a local ignored setup file for the user's selected profile.
- Add GitHub Copilot instructions because it is widely used.
- Keep Claude Code and Codex as the main supported paths.

## Non-Goals

- Do not auto-install external tools.
- Do not activate hooks.
- Do not write secrets.
- Do not claim full support for untested tools.

## User Experience

Run:

```bash
python -m forgeloop setup .
```

The user sees:

1. Claude Code
2. Codex
3. Cursor
4. GitHub Copilot
5. All supported tools

Coming-soon tools are listed below the menu.

## Validation

Run:

```bash
python -m forgeloop setup . --list
python -m forgeloop setup . --tool claude-code --dry-run
python -m forgeloop compat .
python -m unittest discover -s tests
```

## Follow-Up

Add native profiles for Gemini CLI, Windsurf, JetBrains AI, Amazon Q, Cline / Roo Code, and OpenCode after their instruction formats are reviewed and tested.
