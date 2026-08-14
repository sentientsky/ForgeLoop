---
type: capture
date: 2026-08-14
status: current
valid_from: 2026-08-14
tags: [security, release, secrets, opencli, validation]
---

# Capture: Release Readiness Hardening

## What Happened

A release audit found two safety gaps in optional or local-only paths: a dangling symlink could redirect an external secrets write, and the OpenCLI executor did not run every verification command shown in its install plan.

## Decision Or Lesson

Treat local filesystem boundaries and optional integrations with the same care as the core workflow. Check links directly, not only path existence. Before executing an external install, validate the local source, use fixed argument lists, stop at a failed critical step, and make the real execution match the published plan.

## Reusable Pattern

- Reject both existing and dangling symlinks before sensitive writes.
- Recheck sensitive path ancestors after creating directories.
- Prefer no-follow file opens when the platform provides them.
- Model optional integration readiness explicitly rather than inferring it from folder existence.
- Add regression tests for security boundaries and advertised execution steps.

## Where It Belongs

- `forgeloop/secrets.py`
- `forgeloop/opencli.py`
- `tests/test_forgeloop.py`
- `docs/checks/2026-08-14-release-readiness-audit.md`

## Follow-Up

Repeat a live OpenCLI peer-package smoke test only in an isolated environment with a reliable network connection and lifecycle scripts disabled.
