---
type: solution
date: 2026-05-02
status: current
tags: [skills, language, memory, tokens, workflow]
---

# Skill Ladder And Language-Led AI Engineering

## Problem

AI coding tools move quickly, but they often repeat the same mistakes:

- They misunderstand the user's intent.
- They explain the same concepts in long prose every session.
- They guess at bugs before reproducing them.
- They add code before the test surface is clear.
- They forget why decisions were made.
- They capture lessons but never refresh them.

## Solution

Use a skill ladder with a shared language layer.

Core skills run for almost every task:

- Discover
- Frame
- Build
- Check
- Capture

Advanced skills run only when useful:

- Align for fuzzy goals and terminology.
- Probe for bugs and regressions.
- TDD for risky behaviour changes.
- Deepen for architecture friction.
- Simplify for recently changed code.
- Refresh-memory for stale lessons.

The project language file gives humans and agents a common vocabulary. It compresses repeated explanations without hiding meaning from humans.

## Why This Works

The system saves tokens because it lets the agent refer to precise project terms instead of reloading broad context. It improves quality because each advanced skill is a focused thinking loop, not a giant universal prompt.

The ladder also keeps the beginner experience calm. Most users see the five simple stages first. The deeper tools appear only when the task needs them.

## When To Apply

Use this pattern when building an AI-assisted engineering repository, especially one that needs:

- Long-term memory.
- Cross-tool compatibility.
- Review discipline.
- Token control.
- Open source maintainability.
- Strong security defaults.

## Guardrails

- Keep shared language human-readable.
- Do not invent opaque AI-only codes.
- Keep skills short.
- Put detailed references behind optional reads.
- Measure packet size before making token-saving claims.
- Never copy another repo's prompt text or implementation.

## ForgeLoop Application

ForgeLoop should use this pattern in V4 by adding:

- `docs/language/PROJECT_LANGUAGE.md`
- `docs/decisions/`
- `align`, `probe`, `tdd`, `deepen`, `simplify`, and `refresh-memory` skills
- dynamic review routing
- a `doctor` command
- measured token benchmark examples
