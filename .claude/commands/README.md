# Commands

ForgeLoop uses Claude Code skills as the primary command layer.

The five project skills create these slash-style workflows:

- `/discover`
- `/frame`
- `/build`
- `/check`
- `/capture`

Claude Code still supports command files in `.claude/commands/`, but skills are preferred here because they can hold richer instructions and supporting files.

Add command files only when you need a small alias that should not become a full skill.

