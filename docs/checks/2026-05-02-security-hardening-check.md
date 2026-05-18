---
type: check
date: 2026-05-02
status: current
tags: [security, validation, compatibility]
valid_from: 2026-05-02
---

# Check: Security Hardening

## Review Points

- Native tool profiles are short and point back to `AGENTS.md`.
- Setup writes refuse symlinked paths.
- Validation now rejects symlinked repository files.
- Token reports label exactness explicitly.
- Provider token APIs are not called by default.
- Aider auto-commits are disabled.
- OpenCode review agent denies edits.
- Cline ignores cache, build, and local-only files.

## Residual Risks

- AI tools can ignore or truncate rules.
- Exact token counting still depends on model-specific tokenizers or provider APIs.
- JetBrains AI and Kiro profiles should be checked in the actual IDEs.
- Future hooks still need opt-in review before activation.

## Decision

No P1 issue is known in this pass.

The next hardening pass should add a dedicated `forgeloop audit` command that runs validation, compatibility, token smoke tests, and secrets checks in one command.
