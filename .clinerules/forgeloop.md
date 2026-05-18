# ForgeLoop Rule For Cline

Read `AGENTS.md` before starting work.

Use the ForgeLoop loop for non-trivial tasks:

1. Discover the repository state and constraints.
2. Frame the work with scope, files, risks, validation, and rollback.
3. Build in small, reversible steps.
4. Check with security, architecture, testing, and documentation viewpoints.
5. Capture reusable lessons after meaningful work.

Keep context small:

- Use `python -m forgeloop pack "<task query>" . --limit 5` before reading old memory.
- Use `.clineignore` to avoid caches, build output, and dependency folders.
- Use `python -m forgeloop tokens "<task query>" . --tool cline-roo --limit 5` when measuring savings.

Do not commit secrets, local setup files, or real `.env` files.
