# Maintainer Guide

This guide is for people preparing ForgeLoop for public use.

## Routine Checks

```bash
python -m pip install --require-hashes -r .github/requirements-ci.txt
python -m pip install --no-deps --no-build-isolation -e .
python -m ruff check forgeloop tests
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m forgeloop governance audit .
python -m forgeloop governance verify .
python -m build --no-isolation
python -m twine check dist/*
python tests/package_smoke.py dist .
```

## Locked CI Dependencies

GitHub workflows install development and build tools from hash-locked files. To update the locks after changing `.github/requirements-ci.in` or `.github/requirements-fuzz.in`, install a reviewed `uv` release and run:

```bash
uv pip compile --generate-hashes --universal --python-version 3.10 --output-file .github/requirements-ci.txt .github/requirements-ci.in
uv pip compile --generate-hashes --python-version 3.14 --python-platform x86_64-unknown-linux-gnu --output-file .github/requirements-fuzz.txt .github/requirements-fuzz.in
```

Review the complete diff, including versions, markers, and hashes. Do not remove `--require-hashes` from workflow install commands. CI itself checks Python 3.10 through 3.14.

The `Fuzz` workflow runs a bounded, seeded Atheris session against the frontmatter parser. Reproduce it locally on Linux or macOS after installing the exact fuzzer lock:

```bash
python -m pip install --require-hashes -r .github/requirements-fuzz.txt
python fuzz/fuzz_frontmatter.py fuzz/corpus/frontmatter -atheris_runs=20000 -seed=20260924 -max_len=65536
```

## Review Priorities

1. Security and secrets.
2. Correctness of commands and docs.
3. Compatibility with Claude Code and Codex.
4. Token measurement honesty.
5. Beginner clarity.
6. Governed-memory boundaries and evidence.

## Issue Triage

- Bugs need reproduction steps and doctor output.
- Feature requests need a clear user workflow.
- Tool integrations need a compatibility file and acceptance prompt.
- Security issues should move to private handling.

## Maintenance Rhythm

- Review security and dependency alerts weekly.
- Triage new issues and pull requests at least weekly.
- Review compatibility notes and AI tool instructions monthly.
- Review governed-memory retention deadlines and external-store deletion evidence before making a public compliance claim.
- Refresh clean-session compatibility evidence before each minor release.
- Remove stale memory only through a superseding capture or decision record.

Approval authority, sole-maintainer safeguards, and high-risk review rules live in `../GOVERNANCE.md`.

For first-time repository publication and settings, follow `GITHUB_SETUP.md`.

## Release Notes

Keep `CHANGELOG.md` concise.

Mention:

- new commands
- changed workflow rules
- compatibility changes
- security hardening
- known limitations

## Package Metadata

The final project URLs are prepared locally for the first push:

```toml
[project.urls]
Homepage = "https://github.com/sentientsky/ForgeLoop"
Documentation = "https://github.com/sentientsky/ForgeLoop/tree/main/docs"
Issues = "https://github.com/sentientsky/ForgeLoop/issues"
Source = "https://github.com/sentientsky/ForgeLoop"
```
