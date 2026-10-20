# Release Checklist

Use this checklist before promoting ForgeLoop, opening a public release announcement, or merging a release-critical pull request.

ForgeLoop currently ships as a GitHub source alpha. Treat "production level" as a set of evidence gates, not as a slogan.

## Decision Levels

| Level | Meaning | Current policy |
| --- | --- | --- |
| Source alpha | The repository is usable as a source template with clear limits. | Allowed after local checks, GitHub checks, and review pass. |
| Release candidate | The next alpha release is ready for maintainer review. | Allowed when the source-alpha gate passes and the release notes are accurate. |
| Stable production | The project can be promoted as broadly production ready. | Not allowed until the stable blockers below are closed. |

## Source Alpha Gate

Run from a clean checkout and a clean virtual environment:

```bash
python -m pip install --require-hashes -r .github/requirements-ci.txt
python -m pip install --no-deps --no-build-isolation -e .
python -m ruff check forgeloop tests
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop release gate .
python -m forgeloop compat .
python -m forgeloop setup . --tool all-supported --dry-run
python -m forgeloop opencli plan .
python -m forgeloop tokens "release readiness security compatibility" . --limit 5
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m forgeloop governance audit .
python -m forgeloop governance verify .
python -m build --no-isolation
python -m twine check dist/*
python tests/package_smoke.py dist .
```

The source-alpha gate may pass while the stable gate is still blocked. That is expected.

## Stable Production Gate

Run:

```bash
python -m forgeloop release gate . --target stable
```

Do not promote ForgeLoop as stable production until this command passes and the following are true:

- `docs/release/stable-evidence.json` is updated from `blocked` to `passed` only after a maintainer has reviewed the linked evidence, and each record has a current `valid_until` date. The release gate validates this manifest's shape, dates, and paths; it does not contact external providers or replace human review.
- Claude Code has a fresh clean-session acceptance record with the exact command, result, date, tool version, and unchanged working tree.
- At least one trusted independent maintainer can review and approve changes.
- Branch protection requires passing checks, conversation resolution, one independent approval, and code-owner review.
- External-store erasure claims are backed by provider-specific deletion evidence and repeatable tests.
- Open security, dependency, and Scorecard maturity findings have been reviewed honestly.
- Public docs avoid fixed token-saving percentages unless the claim links to reproducible measurement.
- Public docs avoid legal-certification claims unless formal evidence exists.

## Pull Request Release Gate

Before merging a release-critical pull request:

- The diff is focused and understandable.
- Every required GitHub check passes on the latest commit.
- `python -m forgeloop release gate .` passes locally.
- `CHANGELOG.md`, `docs/ROADMAP.md`, and compatibility evidence are updated if the public status changed.
- New commands, governance behaviour, installers, or integrations include tests.
- Any security-sensitive change has a security review note in the pull request.
- No generated cache, local secret, or private credential file is committed.

## Tag Gate

Before pushing a version tag:

- The release change has been merged into `main`.
- The tag version matches `pyproject.toml`.
- The tag has not been used before.
- The release workflow is expected to build from `main`, not from a local working tree.
- The generated source archive is checked for local-only secret paths.
- The release notes repeat known limitations plainly.

## No-Claim List

Do not claim:

- guaranteed security
- guaranteed third-party erasure
- GDPR, HIPAA, SOC 2, or equivalent certification
- universal compatibility with every AI coding tool
- fixed 80 percent or 90 percent token savings without a dated measurement
- full-runtime install, update, or uninstall for existing projects
- PyPI availability under the `forgeloop` name

## Owner Actions After Merge

After a release-critical merge, the repository owner should:

- check the GitHub Security tab for secret scanning, Dependabot, CodeQL, and Scorecard alerts;
- confirm branch protection is still enabled for `main`;
- confirm release tags are protected from update and deletion;
- refresh the clean-session acceptance notes before public promotion;
- keep the README and roadmap aligned with the real status.
