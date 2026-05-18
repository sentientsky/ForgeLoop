---
name: refresh-memory
description: Use when old captures, solutions, decisions, or indexes may be stale, duplicated, superseded, or too vague.
---

# Refresh Memory

Use this skill during release polish, after major design changes, or when memory gives conflicting guidance.

## Inputs

- Current task.
- Relevant context packet.
- Memory index.
- Candidate memory files.

## Steps

1. Build a context packet for the topic.
2. Open only the likely relevant memory files.
3. Classify each note as keep, update, consolidate, supersede, stale, or delete candidate.
4. Prefer superseding or annotating history over deleting it.
5. Update indexes after any memory change.
6. Capture the refresh decision if it affects future work.

## Output

Use `templates/memory-refresh-template.md`.

## Rules

- Never delete memory automatically.
- Do not rewrite historical facts to make the present look cleaner.
- Do not store secrets or private data.
- Keep refreshed notes small and searchable.

## Done When

- The memory set is less contradictory.
- Indexes are current.
- Future agents know which note to trust.

