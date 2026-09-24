# Troubleshooting

## Doctor Shows Optional Items

`doctor` may mention optional features such as tokenisers or OpenCLI.

These are not required for the core workflow.

Use:

```bash
python -m forgeloop opencli status .
```

for OpenCLI detail.

## Token Counts Are Estimates

Install optional tokenizer support:

```bash
python -m pip install -e ".[tokenizers]"
```

Then run:

```bash
python -m forgeloop tokens "memory validation" . --tool codex --limit 5
```

The report tells you whether counts are exact.

## Memory Index Is Out Of Date

Run:

```bash
python -m forgeloop index .
python -m forgeloop index . --check
```

This happens after adding captures, solutions, decisions, entities, timelines, or palace drawers.

## A Real .env File Was Found

Move real secrets outside the repository.

Then run:

```bash
python -m forgeloop secrets init .
python -m forgeloop secrets check .
python -m forgeloop validate .
```

Only `.env.example` belongs in the repo.

## OpenCLI Is Not Installed

This is normal unless you want OpenCLI.

Preview:

```bash
python -m forgeloop opencli plan .
```

Install:

```bash
python -m forgeloop opencli install . --execute
```

Browser-backed commands are privileged, so do not run them casually.

## GitHub Source Release Fails

Check:

- the tag starts with `v`
- the pushed tag matches the version in `pyproject.toml`
- all release-gate checks pass
- the GitHub token has the workflow's `contents: write` permission
- package metadata is valid
- no local-only files were committed; inspect the archive safety-check output

Build locally:

```bash
python -m pip install --require-hashes -r .github/requirements-ci.txt
python -m pip install --no-deps --no-build-isolation -e .
python -m build
python -m twine check dist/*
```
