---
type: deployment-acceptance
date: 2026-05-18
status: current
tags: [deployment, compatibility, release]
---

# Clean-Session Acceptance Pack

This file defines the public-release acceptance prompt for each supported tool.

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
| Claude Code | `CLAUDE.md` | `python -m forgeloop doctor .` | Ready for live session check |
| Codex | `AGENTS.md` | `python -m forgeloop doctor .` | Ready for live session check |
| Cursor | `.cursor/rules/forgeloop.mdc` | `python -m forgeloop validate .` | Ready for live session check |
| GitHub Copilot | `.github/copilot-instructions.md` | `python -m forgeloop validate .` | Ready for live session check |
| Gemini | `GEMINI.md` | `python -m forgeloop tokens "memory validation" . --tool gemini` | Ready for live session check |
| Windsurf | `.windsurf/rules/forgeloop.md` | `python -m forgeloop pack "memory validation" .` | Ready for live session check |
| Cline | `.clinerules/forgeloop.md` | `python -m forgeloop doctor .` | Ready for live session check |
| Roo Code | `.roo/rules/forgeloop.md` | `python -m forgeloop doctor .` | Ready for live session check |
| JetBrains AI | `.aiassistant/rules/forgeloop.md` | `python -m forgeloop validate .` | Beta, needs IDE attachment check |
| Kiro | `.kiro/steering/` | `python -m forgeloop validate .` | Beta, needs steering attachment check |
| OpenCode | `.opencode/agents/forge-review.md` and `AGENTS.md` | `python -m forgeloop compat .` | Ready for live session check |
| Aider | `.aider.conf.yml` and `AGENTS.md` | `python -m forgeloop validate .` | Portable check |
| Generic agents | `AGENTS.md` | `python -m forgeloop doctor .` | Portable check |

## Recording A Live Check

Copy `templates/deployment-acceptance-template.md`, fill the actual prompt, response, validation command, and limitation, then update `docs/compatibility/deployment-matrix.md`.

