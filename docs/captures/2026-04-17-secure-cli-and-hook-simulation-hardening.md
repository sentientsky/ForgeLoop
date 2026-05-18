---
type: capture
date: 2026-04-17
status: current
task: Secure CLI And Hook Simulation Hardening
supersedes:
superseded_by:
valid_from: 2026-04-17
valid_to:
tags: []
---

# Capture: Secure CLI And Hook Simulation Hardening

## What Happened

ForgeLoop added safe note creation, dry-run hook simulation, deterministic memory indexes, seeded threat ideation, and MCP safety design.

## Exact Source Text

Use this section when the original wording matters.

```text
Security remains the priority. Active hooks and MCP writes stay disabled until they have validation, tests, and clear failure behaviour.
```

## Decision Or Lesson

Prefer safe simulation and deterministic scaffolding before enabling automation that can write files, read transcripts, or run commands.

## Why It Matters

This prevents ForgeLoop from repeating common memory-system mistakes: unsafe shell hooks, path traversal, non-deterministic generated files, unreviewable writes, and unclear MCP boundaries.

## Where It Belongs

- CLAUDE.md: validation commands and dry-run hook guidance
- Skill: future Capture and Check improvements
- Agent: future security reviewer expansion
- Hook: dry-run simulation before activation
- Standard: MCP safety design, memory safety, portability, testing
- Solution: dependency-light memory validation
- Palace drawer: not needed yet

## Links

- Research: `docs/research/seeded-security-ideation-2026-04-17.md`
- Standard: `docs/standards/mcp-safety-design.md`
- Solution: `docs/solutions/dependency-light-memory-validation.md`

## Will This Prevent Future Rework?

Partly. The new CLI checks and simulations reduce risk before GitHub, but live hooks and MCP still need their own tests before release.
