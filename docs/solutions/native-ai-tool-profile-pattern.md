---
type: solution
status: current
tags: [compatibility, setup, tooling]
valid_from: 2026-05-02
---

# Native AI Tool Profile Pattern

Use this pattern when adding a new AI coding tool to ForgeLoop.

## Steps

1. Find the tool's native instruction location from official docs.
2. Add the smallest useful rule file for that tool.
3. Point the tool back to `AGENTS.md` for shared workflow.
4. Add the entry file to `forgeloop.compat`.
5. Add the tool profile to `forgeloop.setup`.
6. Add validation for the tool-specific safety anchor.
7. Add a setup dry-run test.
8. Update `docs/compatibility/ai-coding-tools.md`.

## Rule File Shape

Keep native files short:

```text
Read AGENTS.md.
Follow Discover, Frame, Build, Check, Capture.
Use forgeloop pack before broad memory.
Use forgeloop tokens before public savings claims.
Do not commit secrets.
Run validation.
```

## Anti-Pattern

Do not paste the full README, CLAUDE.md, or every skill into each tool profile.

That creates token waste and makes rules drift apart.
