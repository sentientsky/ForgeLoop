---
type: capture
date: 2026-07-26
status: current
task: public status clarity
supersedes:
superseded_by:
valid_from: 2026-07-26
valid_to:
tags: [release, docs, roadmap, public-status]
---

# Capture: Public Status Clarity

## What Happened

Older research and audit notes still contained "not yet" language from before the production release hardening work. Those notes were historically useful, but public readers could mistake them for the current state.

## Decision Or Lesson

Keep historical notes intact, but mark them clearly when they are superseded. Add one current roadmap/status page that separates finished local work from owner-only GitHub launch tasks and future product improvements.

## Why It Matters

Open source users need to know whether a gap is still real, already fixed, or blocked on repository-owner setup. This reduces confusion without deleting the reasoning trail that led to the current product shape.

## Where It Belongs

- Public docs: `docs/ROADMAP.md`
- Research folder: `docs/research/README.md`
- Release gate: `python -m forgeloop doctor .`

## Will This Prevent Future Rework?

Yes. Future audits can update the roadmap and supersede old notes instead of leaving contradictory status claims scattered through the repository.
