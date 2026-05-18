---
type: standard
date: 2026-05-18
status: current
tags: [debugging, testing, probe]
---

# Debugging Feedback Loop Standard

ForgeLoop fixes bugs by creating a signal before changing code.

## Rules

- Reproduce before fixing when possible.
- If reproduction is impossible, state the limitation.
- Test one hypothesis at a time.
- Remove debug instrumentation before completion.
- Capture the prevention pattern when the bug teaches something reusable.

## Skill

Use `.claude/skills/probe/SKILL.md`.

