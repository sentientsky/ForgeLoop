---
type: capture
date: 2026-10-28
status: current
task: security audit fixes
supersedes:
superseded_by:
valid_from: 2026-10-28
valid_to:
tags: [security, audit, setup, dependencies, release]
---

# Capture: Security Audit Fixes

## What Happened

A full local audit reproduced a setup path issue: resolving a configuration symlink before checking it could redirect an atomic replacement onto another file in the repository. The audit also found an affected `certifi` version in the CI dependency lock and an assert-based guard in stable-evidence validation.

All three issues were addressed with path checks, a regression test, an updated hash-locked dependency, and explicit fail-closed validation.

## Decision Or Lesson

For filesystem writes, inspect the original path for symlinks before resolving it. A later containment check does not protect sibling files inside the allowed root. Keep security-relevant validation as explicit runtime branches, not Python `assert` statements.

For dependencies, audit the exact committed lock rather than only declared top-level inputs, and preserve hashes when updating a vulnerable transitive package.

## Why It Matters

These practices reduce accidental file replacement, keep security decisions active in optimized builds, and make dependency remediation reproducible in CI.

## Where It Belongs

- Standard: secure path handling and fail-closed release validation.
- Tests: setup symlink regression coverage.
- Dependency policy: `.github/requirements-ci.in` and its generated hash lock.
- Palace drawer: `docs/checks/` and this capture.

## Links

- Check: [security and code audit](../checks/2026-10-28-security-and-code-audit.md).
- Vulnerability: [OSV PYSEC-2026-4320](https://osv.dev/vulnerability/PYSEC-2026-4320).

## Will This Prevent Future Rework?

Yes. The regression test protects the observed setup path, the lock input retains the patched certificate package floor, and runtime validation no longer depends on debug assertions.
