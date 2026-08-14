# Roadmap And Current Status

This page separates what is already built from what still needs repository-owner setup or future product work.

## Current Status

ForgeLoop is locally release-ready for a first public GitHub push.

The repository now includes the five-stage workflow, Claude Code skills, portable Codex guidance, multi-tool compatibility profiles, memory palace structure, Forge Context Packets, measured token reporting, external secrets handling, optional OpenCLI integration, release workflows, CodeQL, Scorecard, governance, issue templates, and an installed-wheel smoke test.

Current local proof commands:

```bash
python -m ruff check forgeloop tests
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m build
python -m twine check dist/*
python tests/package_smoke.py dist .
```

## Owner-Only Launch Tasks

These cannot be completed safely without the final GitHub owner or organisation:

- create the public GitHub repository
- push the `main` branch
- enable branch protection, security features, and required checks
- configure PyPI Trusted Publishing
- create the first signed or reviewed release tag

Follow `docs/GITHUB_SETUP.md` for these steps.

## Near-Term Product Work

These are the next improvements after public launch:

- record live clean-session transcripts for each supported AI coding tool
- add exact token counters where a provider exposes a safe local or official counter
- expand skill evaluation examples into a runnable behaviour test harness
- add a dynamic review router that chooses reviewers from changed files and risk signals
- add a worktree lifecycle command in dry-run mode before any automated writes
- package optional integrations only after install and uninstall behaviour is tested
- publish a small docs site once repository URLs are final

## Contribution Direction

Good first contributions should be small, testable, and tied to a real user workflow.

Prefer:

- one problem per pull request
- clear reproduction steps
- measured token or compatibility evidence for public claims
- docs updates with examples
- tests for CLI, validation, security, or packaging changes

Avoid:

- broad speculative rewrites
- unmeasured performance or token-saving claims
- silent installation of external tools
- long-lived secrets in GitHub settings or repository files

ForgeLoop should keep getting stronger by proving more of its behaviour, not by making louder claims.
