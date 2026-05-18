---
type: standard
date: 2026-05-11
status: current
tags: [review, agents, quality, routing]
---

# Review Routing Standard

ForgeLoop review should match the risk of the change.

The default reviewers are architecture, security, testing, and documentation. Use extra reviewers when the change touches their area.

## Reviewer Map

- Architecture: structure, boundaries, dependency direction.
- Security: secrets, injection, permissions, unsafe execution.
- Testing: coverage, missing cases, validation quality.
- Documentation: user-facing clarity and drift.
- Correctness: behaviour and edge cases.
- Maintainability: simplicity, naming, future cost.
- Performance: token load, runtime cost, unbounded scans.
- Reliability: timeouts, failure handling, portability.
- API contract: CLI, JSON, templates, plugin manifests.
- Data: memory quality, indexes, retention risk.
- Adversarial: abuse paths, hidden side effects, false claims.

## Routing Rule

For low-risk documentation edits, use the default reviewers lightly.

For command, installer, plugin, network, browser, secrets, or release changes, include security, correctness, reliability, API contract, and adversarial review.

