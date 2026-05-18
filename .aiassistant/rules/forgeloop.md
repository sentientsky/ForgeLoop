# ForgeLoop Project Rule

Read `AGENTS.md` before planning or editing.

Use the ForgeLoop loop for non-trivial work: Discover, Frame, Build, Check, Capture.

Keep edits small, reversible, and easy to review. Use UK English in documentation.

Use these commands from the repository root:

```bash
python -m forgeloop pack "<task query>" . --limit 5
python -m forgeloop tokens "<task query>" . --tool jetbrains-ai --limit 5
python -m forgeloop validate .
python -m unittest discover -s tests
```

Do not store secrets in the repository. Keep real `.env` files outside the project folder.
