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

## Adopt A Tool Profile

Run these from a ForgeLoop source checkout. Preview is the default; `--apply` adds missing files without overwriting conflicts.

```bash
python -m forgeloop adopt ../my-project --tool claude-code
python -m forgeloop adopt ../my-project --tool claude-code --apply
python -m forgeloop adopt ../my-project --tool all-supported --apply
```

This adds profile entry files only. It does not install the CLI/runtime into the destination or provide automatic updates/uninstall.

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

## Governance

```bash
python -m forgeloop governance audit .
python -m forgeloop governance log collect . --actor-ref OPERATOR-001 --record-ref STORE-EXTERNAL-001 --subject-ref SUBJ-EXAMPLE-001
python -m forgeloop governance verify .
```

Use only opaque references. The audit log is local, outside the repository, and stores hashes rather than the references or personal data.

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
