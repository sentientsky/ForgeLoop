---
type: solution
status: current
tags: [setup, compatibility, onboarding, cli]
---

# Menu-Driven Agent Tool Selection

## Problem

AI coding tools use different instruction files.

New users should not need to understand every tool-specific convention before trying ForgeLoop.

## Solution

Provide a setup menu.

The menu should:

- list supported tools first
- show adoption context where useful
- show coming-soon tools honestly
- support non-interactive setup for CI and documentation
- write only a local ignored profile file

## Command

```bash
python -m forgeloop setup .
```

Non-interactive:

```bash
python -m forgeloop setup . --tool claude-code
python -m forgeloop setup . --tool all-supported
```

Preview:

```bash
python -m forgeloop setup . --tool cursor --dry-run
```

## Rule

Setup should never install tools, activate hooks, or write secrets.

It should only select a profile and tell the user what to do next.
