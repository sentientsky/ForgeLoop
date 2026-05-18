# ForgeLoop Workspace Rule

Use `AGENTS.md` as the shared instruction file.

For non-trivial work, follow Discover, Frame, Build, Check, Capture.

Keep context lean:

- Run `python -m forgeloop pack "<task query>" . --limit 5` before reading broad memory.
- Run `python -m forgeloop tokens "<task query>" . --tool windsurf --limit 5` before making token-saving claims.
- Open exact source files only when the packet points to them.

Safety rules:

- Do not store secrets in memory, logs, captures, or `.env` files inside the repo.
- Do not activate hooks unless they are reviewed, tested, and opt-in.
- Validate after meaningful changes with `python -m forgeloop validate .` and `python -m unittest discover -s tests`.
