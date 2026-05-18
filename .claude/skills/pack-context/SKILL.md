---
name: pack-context
description: Build a compact Forge Context Packet before reading ForgeLoop memory for a task.
---

# Pack Context Skill

Use this skill when a task needs project memory, previous decisions, reusable solutions, or review history.

The goal is to reduce token use by loading a small pointer packet first, then opening full source files only when needed.

## Rules

- Run `python -m forgeloop pack "<task query>" .` before reading broad memory folders.
- Run `python -m forgeloop tokens "<task query>" . --tool claude-code` before making token-saving claims.
- Treat the packet as an index, not as evidence.
- Read only the listed source files that are needed for the current task.
- If exact wording matters, open the source file before deciding.
- Do not paste secrets into the query.
- Do not copy full memory folders into context.
- If the packet has no match, use normal discovery search and then capture the missing pattern later.

## Output

Return:

- the compact packet result
- the exact files opened from the packet
- the memory facts used
- any missing memory that should be captured after the task
- the token report command used, when savings are discussed
