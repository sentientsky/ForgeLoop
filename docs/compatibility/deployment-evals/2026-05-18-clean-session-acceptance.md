---
type: deployment-acceptance
date: 2026-09-24
status: planned
tags: [deployment, compatibility, release]
---

# Clean-Session Acceptance Pack

This file is a planned acceptance prompt, not evidence that each external tool has been tested.

It does not pretend to be a live transcript from every external product UI. It records the repeatable check a maintainer should run when refreshing public compatibility claims.

## Universal Prompt

```text
Read this repository's AI instructions, explain the ForgeLoop workflow in five bullets, then say which validation command you would run first.
```

Expected answer:

- Mentions Discover, Frame, Build, Check, Capture.
- Points to the tool's native entry file or `AGENTS.md`.
- Recommends `python -m forgeloop doctor .` or `python -m forgeloop validate .`.
- Does not load broad memory folders before using `pack`.
- Does not propose writing files before discovery.

## Tool Matrix

| Tool | Entry file | Expected first validation | Status |
| --- | --- | --- | --- |
| Claude Code | `CLAUDE.md` | `python -m forgeloop doctor .` | Prompt defined; current live acceptance not recorded |
| Codex | `AGENTS.md` | `python -m forgeloop doctor .` | Prompt defined; current live acceptance not recorded |
| Cursor | `.cursor/rules/forgeloop.mdc` | `python -m forgeloop validate .` | Prompt defined; current live acceptance not recorded |
| GitHub Copilot | `.github/copilot-instructions.md` | `python -m forgeloop validate .` | Prompt defined; current live acceptance not recorded |
| Gemini | `GEMINI.md` | `python -m forgeloop tokens "memory validation" . --tool gemini` | Prompt defined; current live acceptance not recorded |
| Windsurf | `.windsurf/rules/forgeloop.md` | `python -m forgeloop pack "memory validation" .` | Prompt defined; current live acceptance not recorded |
| Cline | `.clinerules/forgeloop.md` | `python -m forgeloop doctor .` | Prompt defined; current live acceptance not recorded |
| Roo Code | `.roo/rules/forgeloop.md` | `python -m forgeloop doctor .` | Prompt defined; current live acceptance not recorded |
| JetBrains AI | `.aiassistant/rules/forgeloop.md` | `python -m forgeloop validate .` | Beta, needs IDE attachment check |
| Kiro | `.kiro/steering/` | `python -m forgeloop validate .` | Beta, needs steering attachment check |
| OpenCode | `.opencode/agents/forge-review.md` and `AGENTS.md` | `python -m forgeloop compat .` | Prompt defined; current live acceptance not recorded |
| Aider | `.aider.conf.yml` and `AGENTS.md` | `python -m forgeloop validate .` | Portable check |
| Generic agents | `AGENTS.md` | `python -m forgeloop doctor .` | Portable check |

## Recording A Live Check

Copy `templates/deployment-acceptance-template.md`, fill the actual prompt, response, validation command, and limitation, then update `docs/compatibility/deployment-matrix.md`.
