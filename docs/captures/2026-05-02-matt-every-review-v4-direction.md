---
type: capture
date: 2026-05-02
status: current
task: matt every review v4 direction
valid_from: 2026-05-02
tags: [research, skills, review, memory, v4]
---

# Capture: Matt And Every Review For ForgeLoop V4

Date: 2026-05-02

## What Was Reviewed

ForgeLoop was compared against:

- Matt Pocock's public skills repository at commit `b843cb5ea74b1fe5e58a0fc23cddef9e66076fb8`.
- Every's Compound Engineering plugin at commit `d685f0794863a73ae3ca3620d2ae747510e9eaa0`.
- The Matt Pocock transcript supplied by the user.

## Reusable Lesson

ForgeLoop should not become a bigger prompt. It should become a better ladder.

The strongest next version combines:

- Matt-style small composable thinking loops.
- A human-readable shared language file.
- Tiny decision records.
- Feedback-loop-first debugging.
- Tracer bullet testing.
- Architecture deepening.
- Every-style strategy anchors, dynamic review routing, health checks, memory refresh, and safe installer ideas.

## Decision

ForgeLoop V4 should add advanced skills around the existing five-stage loop instead of replacing the loop.

The five stages remain the beginner-safe path. Advanced skills are loaded only when needed.

## Next Action

Implement `docs/language`, `docs/decisions`, and the `align` skill first. This gives the highest leverage with the lowest risk.

## Update 2026-05-18

This action is complete.

ForgeLoop now includes `docs/language/`, `docs/decisions/`, `align`, `probe`, `tdd`, `deepen`, `simplify`, and `refresh-memory` skills.
