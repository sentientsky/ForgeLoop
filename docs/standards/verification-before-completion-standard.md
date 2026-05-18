---
type: standard
date: 2026-05-11
status: current
tags: [completion, validation, quality]
---

# Verification Before Completion Standard

ForgeLoop should not finish work by vibes alone.

Before handoff, the agent must show evidence that the requested outcome is complete.

## Required Proof

- The user request is satisfied.
- Relevant validation has run.
- P1 findings are fixed or clearly blocked.
- User-facing behaviour has docs.
- Non-trivial work has a capture note.
- Residual risks are named.

## Skill

Use `.claude/skills/verify-completion/SKILL.md`.

## Release Rule

Any feature that adds commands, installers, plugin behaviour, security rules, or compatibility targets must include completion evidence in the final check note.

