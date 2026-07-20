---
type: capture
date: 2026-06-21
status: current
task: production release audit
supersedes:
superseded_by:
valid_from: 2026-06-21
valid_to:
tags: [release, security, ci, packaging, governance]
---

# Capture: Production Release Audit

## What Happened

The public-release gate was expanded beyond source-tree tests. ForgeLoop now tests an installed wheel outside the checkout, pins external workflow actions, scans with CodeQL, measures branch coverage, validates workflow safety, verifies release tags, creates build provenance, and defines human approval rules.

## Exact Source Text

Not needed. The implementation and workflow files are the durable evidence.

## Decision Or Lesson

A successful package build is not proof that users can run the package. Production readiness needs an isolated installation test, immutable workflow dependencies, least-privilege permissions, a release gate that runs before publishing, and governance that distinguishes automated evidence from human approval.

## Why It Matters

These controls catch missing package files, source-checkout leakage, supply-chain drift, accidental version tags, and unsafe auto-approval assumptions before they reach users.

## Where It Belongs

- CLAUDE.md: Existing Check and Capture rules remain sufficient.
- Skill: `verify-completion`
- Agent: security and reliability reviewers
- Hook: None
- Standard: Release guide and governance
- Solution: None
- Palace drawer: Release engineering

## Links

- Discovery: Local release audit on 2026-06-21
- Frame: Four-step production audit plan
- Build: CI, release, validation, package smoke, and governance changes
- Check: Full release gate and isolated wheel installation
- Solution: None
- Palace memory: This capture

## Will This Prevent Future Rework?

Yes. The checks are executable and run on every pull request or release rather than relying on a maintainer remembering the audit steps.
