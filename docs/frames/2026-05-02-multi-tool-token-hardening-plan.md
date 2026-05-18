---
type: frame
date: 2026-05-02
status: current
tags: [compatibility, tokens, security, setup]
valid_from: 2026-05-02
---

# Frame: Multi-Tool Token Hardening

## Goal

Make ForgeLoop safer and more useful across AI coding tools while keeping Claude Code and Codex as the strongest paths.

## Scope

- Initialise Git for local repo state checks.
- Add native profiles for Gemini, Windsurf, Cline, Roo Code, JetBrains AI, Kiro, OpenCode, and Aider.
- Add a token report command with per-tool profiles.
- Harden setup writes and validation.
- Update tests, docs, CI, and memory.

## Non-Goals

- No remote installer.
- No provider API calls for token counting.
- No automatic hook activation.
- No copied skill text or plugin code from external repositories.

## Security Risks

- Tool rule sprawl can hide stale instructions.
- Token reports can accidentally overclaim exactness.
- Symlinks can make validation read or write outside the repository.
- Local setup files can become accidental commits.

## Validation

Run:

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop compat .
python -m forgeloop setup . --tool all-supported --dry-run
python -m forgeloop tokens "memory validation" . --limit 5
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m compileall forgeloop tests
```

## Rollback

Remove the new native profile files, remove the `tokens` command, and restore the previous compatibility target list.
