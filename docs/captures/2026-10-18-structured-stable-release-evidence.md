---
type: capture
date: 2026-10-18
status: current
task: Structured stable release evidence
supersedes:
superseded_by:
valid_from: 2026-10-18
valid_to:
tags: [release, governance, security, evidence]
---

# Capture: Structured stable release evidence

## What Happened

ForgeLoop's stable release gate now validates `docs/release/stable-evidence.json` instead of inferring critical evidence from text in unrelated Markdown documents. The checked-in manifest is deliberately blocked until real evidence exists.

## Exact Source Text

Use this section when the original wording matters.

```text
The release gate validates this manifest's shape, dates, paths, and constrained attestation fields; it does not contact external providers, authenticate a tool session, or replace human review.
```

## Decision Or Lesson

Treat release readiness as structured evidence with fail-closed defaults, explicit expiry dates, and bounded field formats. Prose is useful for explanation, but it is too easy for an editorial change to alter an automated release decision accidentally, and an unexpired record should not stay valid forever. A machine-validated attestation still cannot prove a provider action or a human review.

## Why It Matters

The gate now makes every future stable-promotion input explicit: which evidence record was reviewed, when it was current, and which role-specific details were supplied. It also retains a hard boundary between validating evidence metadata and proving an external provider's behaviour.

## Where It Belongs

- CLAUDE.md: Existing release-evidence rules apply; no change required.
- Skill: `check` and `capture`.
- Agent: Release reviewer and security reviewer.
- Hook: None.
- Standard: `docs/standards/verification-before-completion-standard.md`.
- Solution: `docs/release/stable-evidence.json`.
- Palace drawer: `docs/checks/` and `docs/captures/`.

## Links

- Discovery: [production closure audit](../checks/2026-09-24-production-closure-audit.md).
- Frame: [release gate audit](../checks/2026-10-07-release-gate-audit.md).
- Build: `forgeloop/release_gate.py`.
- Check: [structured stable release evidence check](../checks/2026-10-18-structured-stable-release-evidence.md).
- Solution: [stable evidence manifest](../release/stable-evidence.json).
- Palace memory: refresh the memory index after this capture.

## Will This Prevent Future Rework?

Yes. It prevents documentation wording changes from silently turning a stable gate from blocked to passed, while preserving the requirement for independent and provider-side evidence.
