---
type: capture
date: 2026-04-17
status: current
task: External Secrets Outside Repository
supersedes:
superseded_by:
valid_from: 2026-04-17
valid_to:
tags: []
---

# Capture: External Secrets Outside Repository

## What Happened

ForgeLoop added an external secrets workflow. The repository now commits only `.env.example` with blank values, while the real local secrets file is created outside the repo.

## Exact Source Text

Use this section when the original wording matters.

```text
The codebase should be safe to push to GitHub without exposing credentials.
```

## Decision Or Lesson

Store secret values outside the executable project area. Keep the key shape in `.env.example`, but keep values in the OS-specific ForgeLoop config directory.

## Why It Matters

This reduces the chance of accidentally committing secrets and makes the project safer to open source later.

## Where It Belongs

- CLAUDE.md: secrets validation commands
- Standard: `docs/standards/secrets-management-standard.md`
- Solution: `docs/solutions/external-env-file-outside-repo.md`
- Palace drawer: not needed yet

## Links

- Example: `examples/external-secrets-workflow.md`
- Solution: `docs/solutions/external-env-file-outside-repo.md`

## Will This Prevent Future Rework?

Partly. It prevents common repo-level leaks, but production deployments still need proper secret stores, rotation, and access controls.
