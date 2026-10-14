---
type: check
date: 2026-10-07
status: current
valid_from: 2026-10-07
tags: [release, security, governance, compatibility]
---

# Release Gate Audit

## Decision

ForgeLoop should remain public source alpha until the stable-production blockers are closed. It may move through release-candidate and source-alpha promotion only when `python -m forgeloop release gate .`, local tests, and required GitHub checks pass, and the pull request receives the review required by current governance.

## What Changed

- Added a repeatable local release gate command.
- Added a release checklist that separates source-alpha, release-candidate, and stable-production decisions.
- Added CI coverage for the source-alpha release gate.
- Kept stable promotion blocked while Claude Code acceptance, independent maintainer review, branch-protection review requirements, and external-store erasure evidence remain incomplete.

## Evidence To Record Before Promotion

- Local command output for the source-alpha gate.
- GitHub Actions run URL for CI, CodeQL, fuzzing, and cross-platform tests.
- Pull request review state.
- Current GitHub security alert state.
- Current compatibility acceptance evidence.

## Stable Blockers

- Claude Code clean-session acceptance needs a fresh passing record.
- A trusted second maintainer is needed before independent approval can be required without making the repository unmergeable.
- External-store erasure remains operator-attested until provider-specific deletion adapters and evidence checks exist.
- Public claims must stay measured, narrow, and reversible.

## Release Wording

Use:

- public source alpha
- release candidate
- production-minded
- security-first defaults
- governed-memory metadata checks
- measured packet-size reporting

Avoid:

- stable production
- fully enterprise ready
- guaranteed erasure
- legal certification
- fixed token-saving percentages without dated measurement
