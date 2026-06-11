# Command Reference

Run commands from the repository root.

## Health

```bash
python -m forgeloop doctor .
python -m forgeloop validate .
python -m forgeloop compat .
python -m forgeloop status .
```

## Setup

```bash
python -m forgeloop setup .
python -m forgeloop setup . --list
python -m forgeloop setup . --tool codex --dry-run
```

## Memory

```bash
python -m forgeloop pack "task query" . --limit 5
python -m forgeloop tokens "task query" . --tool codex --limit 5
python -m forgeloop index .
python -m forgeloop index . --check
```

## Notes

```bash
python -m forgeloop new discover "Task title" .
python -m forgeloop new frame "Task title" .
python -m forgeloop new check "Task title" .
python -m forgeloop new capture "Lesson title" .
python -m forgeloop new solution "Pattern title" .
python -m forgeloop new decision "Decision title" .
```

## Secrets

```bash
python -m forgeloop secrets init .
python -m forgeloop secrets path .
python -m forgeloop secrets check .
```

## Hooks

```bash
python -m forgeloop hook-simulate PreCompact .
python -m forgeloop hook-simulate Stop . --interval 15
```

## OpenCLI

```bash
python -m forgeloop opencli status .
python -m forgeloop opencli status . --fetch-npm
python -m forgeloop opencli plan .
python -m forgeloop opencli install . --execute
```

## Intro

```bash
python -m forgeloop intro
python -m forgeloop intro --plain
```

