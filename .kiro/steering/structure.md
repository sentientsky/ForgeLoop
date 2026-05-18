# ForgeLoop Structure Steering

Key files:

- `README.md`: human overview.
- `CLAUDE.md`: Claude Code rules.
- `AGENTS.md`: portable coding-agent rules.
- `GEMINI.md`: Gemini entry point.
- `forgeloop/`: CLI package.
- `tests/`: unit tests.
- `docs/`: workflow notes, standards, compatibility, research, and memory.
- `templates/`: note templates.
- `.claude/`: Claude skills, agents, hooks, and commands.

Memory folders:

- `docs/captures/`
- `docs/solutions/`
- `docs/palace/`

After changing memory records, run:

```bash
python -m forgeloop index .
python -m forgeloop index . --check
```
