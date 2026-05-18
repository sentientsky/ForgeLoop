---
type: compatibility
date: 2026-05-11
status: current
tags: [deployment, compatibility, ai-tools]
---

# Deployment Matrix

This matrix records the current ForgeLoop support claim for each tool family.

For repeatable clean-session prompts, see `docs/compatibility/deployment-evals/2026-05-18-clean-session-acceptance.md`.

| Tool | Level | Entry Point | Last Verified | Limitation |
| --- | --- | --- | --- | --- |
| Claude Code | Full | `CLAUDE.md`, `.claude/skills/` | 2026-05-11 | Real user sessions still need periodic skill trigger evals. |
| Codex | Full | `AGENTS.md` | 2026-05-11 | Uses portable instructions rather than Claude skills. |
| Cursor | Supported | `.cursor/rules/forgeloop.mdc` | 2026-05-11 | Model routing can change token counts. |
| GitHub Copilot | Supported | `.github/copilot-instructions.md` | 2026-05-11 | Workspace behaviour depends on Copilot client support. |
| Gemini | Supported | `GEMINI.md` | 2026-05-11 | Exact token counts require provider tooling. |
| Windsurf | Supported | `.windsurf/rules/forgeloop.md` | 2026-05-11 | Keep rule file concise. |
| Cline / Roo Code | Supported | `.clinerules/`, `.roo/rules/` | 2026-05-11 | Requires local extension configuration. |
| JetBrains AI | Beta | `.aiassistant/rules/forgeloop.md` | 2026-05-11 | Native rule behaviour needs more user testing. |
| Kiro | Beta | `.kiro/steering/` | 2026-05-11 | Steering support may vary by version. |
| OpenCode | Supported | `.opencode/agents/forge-review.md` | 2026-05-11 | Agent schema may evolve. |
| Aider | Portable | `.aider.conf.yml` | 2026-05-11 | Uses shared instructions rather than native stages. |
| OpenCLI | Supported integration | `integrations/opencli/` | 2026-05-11 | Optional peer dependency, not required for core ForgeLoop. |

Run this before a public release:

```bash
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop validate .
```

Public compatibility claims should say whether the evidence is file-readiness, local CLI validation, or a live clean-session transcript.
