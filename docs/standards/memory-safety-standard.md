---
type: standard
date: 2026-04-17
status: current
tags: [memory, safety, security]
---

# Memory Safety Standard

ForgeLoop memory should be useful without becoming a liability.

## Rules

- Never store secrets, tokens, private keys, passwords, or confidential customer data.
- Prefer exact wording only when it is safe and useful.
- Redact sensitive values before storing examples.
- Keep memory files small enough to review.
- Skip symlinks in memory folders.
- Reject or warn on unusually large files.
- Treat user-provided files as untrusted input.
- Mark outdated facts as superseded rather than silently replacing them.
- Keep generated indexes deterministic and easy to diff.

## Hook Safety

Hooks must be safe before they are enabled.

Avoid:

- `eval`
- unquoted shell variables
- `curl | sh`
- broad delete commands
- shelling out with unchecked user input
- writing secrets to logs

Prefer:

- dry-run examples first
- explicit allowlists
- timeouts
- structured JSON input validation
- clear failure behaviour
- simulation before activation

Use `python -m forgeloop hook-simulate <event> .` before designing any active hook.

## MCP Safety

Future MCP tools must:

- validate all arguments
- handle null arguments safely
- bound file sizes
- avoid protocol stdout pollution
- return structured errors
- avoid leaking sensitive content in logs
- include tests for malformed input
