# ForgeLoop For Gemini

Read `AGENTS.md` first. It is the portable source of truth for this repository.

Use the ForgeLoop loop for non-trivial work:

1. Discover
2. Frame
3. Build
4. Check
5. Capture

Before reading broad memory, run:

```bash
python -m forgeloop pack "<task query>" . --limit 5
python -m forgeloop tokens "<task query>" . --tool gemini --limit 5
```

Treat FCP output as a pointer index. Open only the listed source files that are relevant.

Keep secrets outside the repository. Run `python -m forgeloop secrets check .` before sharing work.

Validate with:

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop compat .
python -m forgeloop index . --check
```
