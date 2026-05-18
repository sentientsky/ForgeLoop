---
type: standard
date: 2026-05-11
status: current
tags: [git, worktree, safety, handoff]
---

# Worktree Lifecycle Standard

ForgeLoop must protect user work.

AI agents may be working inside a dirty tree, a fresh folder, or a partial repository. They should adapt without destructive commands.

## Rules

- Inspect local state before editing when Git is available.
- Treat unknown existing changes as user work.
- Never use destructive reset, checkout, clean, delete, or move commands unless the user clearly asked for them.
- Keep generated caches out of release.
- Report Git unavailability instead of pretending the tree was clean.

## Skill

Use `.claude/skills/worktree-lifecycle/SKILL.md`.

## Handoff

Use `templates/worktree-handoff-template.md` for substantial changes.

