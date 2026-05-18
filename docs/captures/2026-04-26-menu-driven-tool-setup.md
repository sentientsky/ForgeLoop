---
type: capture
date: 2026-04-26
status: current
valid_from: 2026-04-26
tags: [setup, compatibility, cli, ai-coding-tools]
---

# Capture: Menu-Driven Tool Setup

## Decision

ForgeLoop now provides a setup menu.

Users can select Claude Code, Codex, Cursor, GitHub Copilot, or all supported tools.

## Why

Open source users will arrive with different AI coding tools.

A setup menu reduces first-run confusion and gives ForgeLoop a product-like onboarding flow.

## Implementation

Use:

```bash
python -m forgeloop setup .
python -m forgeloop setup . --tool codex --dry-run
python -m forgeloop setup . --list
```

The selected profile is written to `.forgeloop.local.json` unless `--dry-run` is used.

The file is ignored by Git.

## Reusable Lesson

Tool compatibility should be selected explicitly by the user and verified by `python -m forgeloop compat .`.
