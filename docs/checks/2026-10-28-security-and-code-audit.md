---
type: check
date: 2026-10-28
status: current
task: security and code audit
tags: [security, audit, dependencies, tests, release]
---

# Check: Security and Code Audit

## Summary

The repository audit found and fixed a local setup-file symlink overwrite, an affected CI trust-store dependency, and an assert-based release-evidence guard. Local tests, lint, coverage, self-validation, dependency audit, and package smoke checks passed. This is a point-in-time engineering audit, not a guarantee that the project is defect-free.

## Findings And Fixes

- Setup previously resolved `.forgeloop.local.json` before checking whether that path was a symlink. A link to another file inside the repository could therefore cause setup to replace that target. Setup now checks the link itself before resolution, rejects non-regular destinations, and has a regression test that confirms the target remains unchanged.
- The CI lock contained `certifi==2026.7.22`, which is affected by `PYSEC-2026-4320`. The input now requires `certifi>=2026.10.19`; the hash lock resolves to `2026.10.23` and changes no other package versions.
- Stable release evidence validation used `assert manifest is not None`. This is now an explicit fail-closed return and remains active with optimized Python.

## Validation

- `python -m unittest discover -s tests`: 76 tests passed.
- `python -m ruff check forgeloop tests`: passed.
- Branch coverage: 75%, above the configured 70% minimum.
- `uvx --from pip-audit pip-audit --requirement .github/requirements-ci.txt`: no known vulnerabilities found.
- `uvx --from bandit bandit -q -r forgeloop`: no medium or high findings. The low findings were reviewed: the token-estimate label is not a credential, and OpenCLI invokes argument arrays with `shell=False` and fixed timeouts.
- ForgeLoop repository validation, setup dry run, compatibility, doctor, release gate, OpenCLI plan, context/token report, secret check, governance checks, and memory-index check passed.
- Source and wheel builds, Twine metadata checks, and the installed-wheel smoke test passed.
- `git diff --check` passed.

## Remaining Limits

- Claude Code clean-session acceptance still requires valid user authentication and a real interactive session.
- Independent maintainer review requires a separate human reviewer.
- External-store erasure guarantees require provider-specific evidence. ForgeLoop does not claim these gates have passed.
- GitHub hosted CI must run on the updated commit before this change is considered merged or released.

## External References

- [OSV: PYSEC-2026-4320](https://osv.dev/vulnerability/PYSEC-2026-4320).
- [Certifi security advisory GHSA-6q48-6c7w-9gw2](https://github.com/certifi/python-certifi/security/advisories/GHSA-6q48-6c7w-9gw2).
- [Certifi on PyPI](https://pypi.org/project/certifi/).
