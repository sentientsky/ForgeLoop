---
type: research
date: 2026-04-17
status: current
tags: [security, ideation, hardening]
---

# Seeded Security Ideation

This note records the seeded thinking used for the next ForgeLoop hardening phase.

## Seed 17: Path Safety

Question: How could note creation write outside the repository?

Risk:

- path traversal through task names
- reserved device names
- symlinked output folders
- accidental overwrite

Response:

- allow only known note kinds
- generate slugs from safe ASCII
- resolve all output paths under the repo root
- refuse symlinked output ancestors
- refuse overwrite unless `--force` is explicit

## Seed 31: Hook Injection

Question: How could future hooks become dangerous?

Risk:

- shell interpolation
- `eval`
- broad delete commands
- transcript paths treated as trusted
- accidental command execution during tests

Response:

- add dry-run hook simulation only
- do not read transcript files in simulation
- return recommendations without executing commands
- keep active hooks disabled by default
- validate hook and settings files for risky patterns

## Seed 53: Deterministic Outputs

Question: How could generated files break CI even when behaviour is unchanged?

Risk:

- generated dates
- absolute paths
- machine-specific data
- random ordering

Response:

- remove current date from generated indexes
- use stable ordering
- keep paths repository-relative
- check generated files in CI

## Seed 79: MCP Boundary

Question: How could a future MCP server fail safely?

Risk:

- malformed arguments
- null payloads
- protocol stdout pollution
- oversized input
- leaking memory contents in logs
- unclear write permissions

Response:

- design MCP as read-only first
- validate every tool argument
- return structured errors
- write human logs to stderr only
- require tests before enabling write tools

