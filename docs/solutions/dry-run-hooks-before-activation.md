---
type: solution
date: 2026-04-17
status: current
tags: []
---

# Solution: Dry Run Hooks Before Activation

## Problem

Automation hooks are useful, but unsafe hooks can run commands at the wrong time, trust hostile input, or block the agent in confusing loops.

## Solution

Build a simulator first.

The simulator should:

- accept structured input
- validate event names
- sanitise identifiers
- refuse to read transcript files
- never execute commands
- return a clear recommendation
- have tests before any active hook exists

## Why It Works

It lets maintainers test the policy before adding execution. The dangerous part of hooks is not the idea of capture, it is the boundary where untrusted runtime data meets shell commands or file writes.

## Use When

- designing lifecycle hooks
- deciding save intervals
- checking PreCompact or SessionEnd behaviour
- reviewing whether automation is safe enough to enable

## Do Not Use When

- a hook must perform real work in production
- the required behaviour is not yet covered by tests
- the hook needs to read sensitive transcript content

## Validation

- `python -m forgeloop hook-simulate PreCompact .`
- `python -m unittest discover -s tests`

## Related Notes

- Capture: `docs/captures/2026-04-17-secure-cli-and-hook-simulation-hardening.md`
- Standard: `docs/standards/mcp-safety-design.md`
