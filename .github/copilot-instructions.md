# ForgeLoop Copilot Instructions

Follow the shared agent instructions in `AGENTS.md`.

Key rules:

- Use Discover, Frame, Build, Check, Capture for non-trivial work.
- Run `python -m forgeloop pack "<task query>" . --limit 5` before loading broad memory.
- Run `python -m forgeloop validate .` and `python -m forgeloop compat .` after structural changes.
- Keep secrets outside the repository.
- Do not make token-savings claims without measured FCP output.
