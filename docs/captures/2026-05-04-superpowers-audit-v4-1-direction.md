---
type: capture
date: 2026-05-04
status: superseded
task: superpowers auditor review v4.1 direction
valid_from: 2026-05-04
valid_to: 2026-06-21
superseded_by: 2026-06-21-production-release-audit
tags: [audit, superpowers, deployment, skills, v4.1]
---

# Capture: Superpowers Audit And ForgeLoop V4.1 Direction

Status note, 2026-07-26: this capture remains useful for product history, but the production-release hardening work resolved several gaps listed here. Current status lives in `docs/ROADMAP.md` and `docs/captures/2026-06-21-production-release-audit.md`.

## What Happened

ForgeLoop was audited against Matt Pocock's skills, Every's Compound Engineering plugin, and Obra's Superpowers repository.

Superpowers added a missing perspective: skills should be tested as behaviour-shaping code, not only written as good-looking documentation.

## Reusable Lesson

The next ForgeLoop quality leap is not another broad feature. It is proof.

ForgeLoop should prove:

- the right skills trigger
- the workflow starts before coding
- completion claims have evidence
- tool integrations work in clean sessions
- memory packets save tokens in measured reports
- public deployment paths are safe

## Decision

ForgeLoop V4.1 should prioritise:

1. Skill eval harness.
2. Deployment acceptance matrix.
3. Doctor command.
4. Verification-before-completion.
5. Worktree lifecycle.
6. Dynamic review routing.

## Comparison Verdict

ForgeLoop is stronger than the reviewed projects in memory-first design, token accountability, and secret-safety posture.

ForgeLoop is not yet stronger in deployment maturity. Superpowers and Every have stronger plugin packaging and behaviour testing.

## Next Action

Implement the V4.1 hardening plan before adding more broad features.
