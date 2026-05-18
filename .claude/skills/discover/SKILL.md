---
name: discover
description: Inspect the repository, task, constraints, and related memory before planning. Use at the start of any non-trivial ForgeLoop task.
---

# Discover

Use this skill before planning or editing.

The goal is to understand the task and the project state well enough to avoid building on assumptions.

## Inputs

- The user's request.
- The current repository state.
- Relevant files, docs, and memory.
- Any known constraints.

## Steps

1. Restate the user goal in plain English.
2. Inspect the repository structure.
3. Read `README.md`, `CLAUDE.md`, and relevant docs.
4. Search for related previous work in:
   - `docs/discoveries/`
   - `docs/frames/`
   - `docs/checks/`
   - `docs/captures/`
   - `docs/solutions/`
   - `docs/palace/`
5. Identify relevant files and folders.
6. List constraints, assumptions, risks, and missing context.
7. Decide whether the task is small enough to continue directly or needs a full Frame stage.

## Output

Create a discovery note in `docs/discoveries/` for non-trivial tasks.

Use `templates/discovery-template.md`.

## Discovery Note Naming

Use this pattern:

```text
docs/discoveries/YYYY-MM-DD-short-task-name.md
```

## Rules

- Do not edit product code during Discover.
- Do not invent requirements.
- Do not ask the user questions unless the task cannot be safely framed without the answer.
- Prefer evidence from the repo over guesses.
- If no related memory exists, say that clearly.

## Done When

- The goal is clear.
- Relevant context has been inspected.
- Risks and assumptions are visible.
- The next Frame stage has enough information to produce a plan.

