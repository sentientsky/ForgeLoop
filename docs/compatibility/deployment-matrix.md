---
type: compatibility
date: 2026-09-24
status: current
tags: [deployment, compatibility, ai-tools]
---

# Deployment Matrix

This matrix records the profile files provided by ForgeLoop and the evidence level. A local file-presence check is not a live integration test.

For repeatable clean-session prompts, see `docs/compatibility/deployment-evals/2026-05-18-clean-session-acceptance.md`.

| Tool | Profile level | Entry point | Evidence | Limitation |
| --- | --- | --- | --- | --- |
| Claude Code | Primary profile | `CLAUDE.md`, `.claude/skills/` | Files and metadata validated by CI; live check must be recorded per release | Real skill triggering and tool behaviour are not established by `compat`. |
| Codex | Primary profile | `AGENTS.md` | Files present; live check must be recorded per release | Uses portable instructions rather than Claude skills. |
| Cursor | Profile provided | `.cursor/rules/forgeloop.mdc` | File presence only | Confirm rule activation and behaviour in the current client. |
| GitHub Copilot | Profile provided | `.github/copilot-instructions.md` | File presence only | Workspace behaviour depends on Copilot client support. |
| Gemini | Profile provided | `GEMINI.md` | File presence only | Exact token counts require provider tooling. |
| Windsurf | Profile provided | `.windsurf/rules/forgeloop.md` | File presence only | Confirm rule activation in the current client. |
| Cline / Roo Code | Profile provided | `.clinerules/`, `.roo/rules/` | File presence only | Requires local extension configuration. |
| JetBrains AI | Beta profile | `.aiassistant/rules/forgeloop.md` | File presence only | Native rule behaviour needs IDE testing. |
| Kiro | Beta profile | `.kiro/steering/` | File presence only | Steering support may vary by version. |
| OpenCode | Profile provided | `.opencode/agents/forge-review.md` | File presence only | Agent schema may evolve. |
| Aider | Portable profile | `.aider.conf.yml` | File presence only | Uses shared instructions rather than native stages. |
| OpenCLI | Optional peer plugin | `integrations/opencli/` | Source files validated; live bridge is optional and not required for core ForgeLoop | Browser sessions are privileged and must be tested explicitly. |

Run this before a public release:

```bash
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop validate .
```

The `compat` command reports only required-file presence. Public claims must say whether evidence is file presence, repository validation, or a dated live clean-session transcript.
