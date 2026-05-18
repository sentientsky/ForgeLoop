---
name: capture
description: Store the reusable lesson, decision, fix, pattern, preference, or changed fact after a task so ForgeLoop compounds over time.
---

# Capture

Use this skill after Check.

The goal is to make the next task easier by preserving what this task taught the system.

## Inputs

- User request.
- Discovery, frame, build, and check notes.
- Final change summary.
- Review findings.
- Decisions and trade-offs.

## Steps

1. Summarise what was solved.
2. Preserve exact wording when it matters.
3. Identify the reusable lesson.
4. Decide where the lesson belongs:
   - `docs/captures/`
   - `docs/solutions/`
   - `docs/standards/`
   - `docs/palace/drawers/`
   - `docs/palace/entities/`
   - `docs/palace/timelines/`
   - `CLAUDE.md`
   - a skill
   - a reviewer agent
   - a hook example
5. Mark changed facts with time-aware metadata.
6. Link related notes together.
7. State whether the system would catch this issue next time.

## Output

Create a capture note in `docs/captures/`.

Create a solution note in `docs/solutions/` when the lesson is reusable.

Use:

- `templates/capture-template.md`
- `templates/palace-drawer-template.md`

## Capture Naming

Use these patterns:

```text
docs/captures/YYYY-MM-DD-short-task-name.md
docs/solutions/short-solution-name.md
docs/palace/drawers/YYYY-MM-DD-short-memory-name.md
```

## Rules

- Do not store secrets.
- Do not store private personal data.
- Do not overwrite history when a fact changes.
- Mark old facts as superseded.
- Promote repeated patterns into templates, skills, agents, hooks, or standards.

## Done When

- The task has left reusable memory behind.
- Related memory is linked.
- Any changed fact is time-aware.
- The next similar task should be easier.

