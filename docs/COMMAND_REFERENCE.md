# Command Reference

Run commands from the repository root.

## Health

```bash
python -m forgeloop doctor .
python -m forgeloop validate .
python -m forgeloop compat .
python -m forgeloop status .
```

## Release

```bash
python -m forgeloop release gate .
python -m forgeloop release gate . --target stable
python -m forgeloop release gate . --json
```

The default gate checks whether the repository is safe to promote as a source alpha or release candidate after review. The stable target intentionally fails until the documented human-review, Claude acceptance, branch-protection, and external-erasure evidence gates are closed.

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

## Reviewed Capture Candidates

Candidate text is read from stdin so it is not included in shell history. Keep candidates concise, and do not stage transcripts, secrets, or personal data. The staging directory is local and Git-ignored, not encrypted.

```bash
python -m forgeloop capture-candidate propose "Lesson title" --root .
# Type or paste a short candidate, then send EOF (Ctrl+Z then Enter in PowerShell).
python -m forgeloop capture-candidate show CANDIDATE_ID --root .
python -m forgeloop capture-candidate approve CANDIDATE_ID REVIEW_FINGERPRINT --root .
```

Approval writes a new file only; it refuses overwrites. The fingerprint ties approval to the exact title and body shown during review. Inspect candidate content for privacy and correctness before approving.

## Beads (Optional)

ForgeLoop does not install or initialise Beads. When `bd` is already installed and configured for this project, this command reads a bounded ready-work list:

```bash
python -m forgeloop beads ready . --limit 20
```

It invokes `bd ready --json --brief --limit N` with `shell=False` and a 10-second timeout. It never claims work, creates a second task graph, syncs, or writes Beads data. The official [Beads CLI reference](https://github.com/gastownhall/beads/blob/main/docs/CLI_REFERENCE.md) documents `bd ready` and its separate `--claim` flag; check the installed Beads version before relying on this integration.

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
python -m forgeloop governance log erase . --actor-ref OPERATOR-001 --record-ref STORE-EXTERNAL-001 --subject-ref SUBJ-EXAMPLE-001 --evidence-ref EVIDENCE-PACKET-001
python -m forgeloop governance verify .
```

Use only opaque references. New `erase` events require `--evidence-ref`; the audit log hashes that reference and cannot verify provider evidence. The log is local, outside the repository, and stores no raw references or personal data.

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
