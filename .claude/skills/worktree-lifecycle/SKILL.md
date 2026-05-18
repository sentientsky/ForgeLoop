---
name: worktree-lifecycle
description: Use when editing a repository to protect user changes, track local state, and produce a clean handoff.
---

# Worktree Lifecycle

Use this skill before edits, during long changes, and before handoff.

The goal is to protect existing work and make every change reviewable.

## Inputs

- Repository root.
- User request.
- Current worktree state.
- Files changed during the task.

## Steps

1. Check whether the folder is a Git repository.
2. If Git is available, inspect local changes before editing.
3. Treat unknown existing changes as user work.
4. Keep your edits focused on the requested scope.
5. Avoid destructive Git commands.
6. Before handoff, list files you changed and note unrelated dirty files separately.
7. If Git is not available, report that file state was tracked manually.

## Output

Create a worktree handoff when the task is substantial:

```text
Worktree handoff
- Git repository:
- Pre-existing changes:
- Files changed by this task:
- Validation:
- Unrelated dirty files:
- Cleanup needed:
```

## Rules

- Do not reset, checkout, clean, or remove files unless the user clearly asked for it.
- Do not overwrite user changes to solve a merge problem.
- Do not claim a clean tree if Git was unavailable.
- Keep generated cache files out of commits.
- Mention untracked files when they matter for release.

## Done When

- User changes are preserved.
- Task changes are visible.
- Validation is tied to the current file state.

