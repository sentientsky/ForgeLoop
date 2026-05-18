# ForgeLoop Agent Instructions

ForgeLoop is an open source operating system for disciplined AI-assisted engineering.

These instructions are written for Codex and other AI coding agents that read `AGENTS.md`.

For Claude Code, `CLAUDE.md` remains the primary instruction file. Keep both files aligned, but do not copy large blocks between them.

## Core Loop

Use the ForgeLoop stages for non-trivial work:

1. Discover
2. Frame
3. Build
4. Check
5. Capture

Small tasks may compress the stages, but still inspect before editing and validate after editing.

## Token Economy

Before opening broad memory folders, run:

```bash
python -m forgeloop pack "<task query>" . --limit 5
```

Use the FCP/1 output as a pointer index.

Open exact source files only when the packet shows they are likely relevant.

Do not load whole memory folders into context.

## Commands

Use these from the repository root:

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop setup . --list
python -m forgeloop compat .
python -m forgeloop tokens "memory validation" . --limit 5
python -m forgeloop index .
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m forgeloop pack "memory validation" . --limit 5
```

After adding capture, solution, entity, timeline, or palace drawer notes, run:

```bash
python -m forgeloop index .
```

## Editing Rules

- Use UK English in documentation.
- Prefer small, reversible changes.
- Keep the repository dependency-light.
- Keep secrets outside the repository.
- Do not add active hooks unless they are reviewed, tested, and opt-in.
- Do not edit generated memory indexes by hand.
- Use `python -m forgeloop setup .` to select a local tool profile.
- Do not claim token savings without measured packet output.
- Treat token reports as exact only when their `exact` field is true.
- Keep native tool profiles short and point them back to `AGENTS.md`.
- Preserve original implementation and wording.
- Treat OpenCLI as an optional integrated peer plugin, not copied code.
- Do not install, update, or run browser-backed OpenCLI commands without explicit user intent.

## Definition Of Done

Work is done when:

- requested behaviour is complete
- relevant tests or validation have run
- no P1 security issue remains
- docs are updated when behaviour changes
- non-trivial work has a capture note
- memory indexes are refreshed when memory records changed
- optional integration status is checked when integration files changed
- public-release changes have updated guides, benchmarks, or acceptance notes when relevant
