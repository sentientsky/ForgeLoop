# Release Guide

Use this guide before publishing ForgeLoop to GitHub.

## Release Gate

Run:

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m forgeloop tokens "release readiness" . --limit 5
```

Optional:

```bash
python -m forgeloop opencli status . --fetch-npm
python -m forgeloop opencli plan . --fetch-npm --with-skills --run-doctor
```

## Manual Checks

- No real `.env` files are in the repository.
- No generated cache folders are committed.
- No public token-saving claim lacks command evidence.
- No optional integration installs silently.
- Docs link to current commands.
- New skills have evaluation examples or templates.
- Memory index is current.

## Git Steps

```bash
git status --short
git add .
git status --short
git commit -m "Prepare ForgeLoop public release foundation"
```

Do not push until the remote repository, description, topics, and security settings are ready.

## GitHub Repository Settings

Recommended settings:

- enable secret scanning if available
- enable push protection if available
- require pull request review before merge
- require CI before merge
- add MIT licence
- add topics: `ai`, `claude-code`, `codex`, `agentic-engineering`, `memory`, `developer-tools`

## Public Claims

Use cautious language:

- "measured packet reports"
- "token-aware memory"
- "pointer-first context"
- "exact when tokenizer support is available"

Avoid:

- fixed percentage claims without benchmark evidence
- claims that all tool integrations are deeply verified
- claims that OpenCLI is bundled

## Release Notes Template

```text
ForgeLoop public foundation release

Included:
- five-stage workflow
- Claude Code skills and reviewers
- portable AI tool entry files
- local memory palace
- Forge Context Packets
- doctor and validation commands
- external secrets workflow
- optional OpenCLI peer integration

Known limitations:
- optional exact tokenisers are not installed by default
- OpenCLI must be installed explicitly
- live clean-session verification should be refreshed as tools evolve
```

