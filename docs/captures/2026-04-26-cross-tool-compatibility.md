---
type: capture
date: 2026-04-26
status: current
valid_from: 2026-04-26
tags: [compatibility, claude-code, codex, cursor]
---

# Capture: Cross-Tool Compatibility

## Decision

ForgeLoop should support multiple AI coding tools through compact, native instruction files.

Claude Code remains primary.

Codex, Cursor, and GitHub Copilot are supported through `AGENTS.md`, `.cursor/rules/forgeloop.mdc`, and `.github/copilot-instructions.md`.

## Why

Different agents load instructions differently.

A single giant prompt file would waste tokens and drift quickly.

Small native entry points keep the workflow portable without giving up Claude Code features.

## Reusable Rule

When adding support for a new tool, create the smallest native entry file that points back to ForgeLoop commands and docs.

Do not duplicate the full operating manual.
