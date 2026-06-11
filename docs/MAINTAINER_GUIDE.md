# Maintainer Guide

This guide is for people preparing ForgeLoop for public use.

## Routine Checks

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop index . --check
python -m forgeloop secrets check .
```

## Review Priorities

1. Security and secrets.
2. Correctness of commands and docs.
3. Compatibility with Claude Code and Codex.
4. Token measurement honesty.
5. Beginner clarity.

## Issue Triage

- Bugs need reproduction steps and doctor output.
- Feature requests need a clear user workflow.
- Tool integrations need a compatibility file and acceptance prompt.
- Security issues should move to private handling.

## Release Notes

Keep `CHANGELOG.md` concise.

Mention:

- new commands
- changed workflow rules
- compatibility changes
- security hardening
- known limitations

## Package Metadata

Do not add project URLs until the public GitHub repository path is final.

After the repository exists, add:

```toml
[project.urls]
Homepage = "https://github.com/<owner>/<repo>"
Documentation = "https://github.com/<owner>/<repo>/tree/main/docs"
Issues = "https://github.com/<owner>/<repo>/issues"
Source = "https://github.com/<owner>/<repo>"
```

