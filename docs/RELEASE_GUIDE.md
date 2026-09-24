# Source Alpha Release Guide

ForgeLoop is released as a GitHub source archive. It is not currently a PyPI-installable toolkit.

## Release Gate

Use a clean virtual environment and run from the repository root:

```bash
python -m pip install --require-hashes -r .github/requirements-ci.txt
python -m pip install --no-deps --no-build-isolation -e .
python -m ruff check forgeloop tests
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop setup . --tool all-supported --dry-run
python -m forgeloop opencli plan .
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m forgeloop governance audit .
python -m forgeloop governance verify .
python -m build --no-isolation
python -m twine check dist/*
python tests/package_smoke.py dist .
```

Optional live OpenCLI checks must be explicit and run only in an approved test account/session.

## Manual Checks

- No real `.env` files, credentials, or local setup files are tracked.
- No generated caches or unrelated build artefacts enter the source archive.
- Token claims are backed by reproducible command output.
- Compatibility claims distinguish profile-file presence from an actual clean-session tool check.
- The memory index is current and governed-memory metadata is valid.
- Open security findings and Dependabot PRs are reviewed; a green workflow alone is not approval.
- Release tag matches `pyproject.toml` version.
- The source archive contains the full tracked project and passes the archive safety check.
- The release includes a matching SHA-256 checksum; the archive attestation verifies against the expected repository.
- Legal, certification, and third-party erasure claims have appropriate evidence and review.

## Publish A GitHub Source Release

1. Merge a reviewed release change to `main` and confirm all required CI, CodeQL, and fuzz checks pass.
2. Update `CHANGELOG.md` and the version in `pyproject.toml`.
3. Create a matching annotated tag, for example:

```bash
git tag -a v0.1.0 -m "ForgeLoop 0.1.0 source alpha"
git push origin v0.1.0
```

4. Wait for the tag-triggered Release workflow. It runs the release gate, builds and attests the complete source archive, checks it for local-only files, generates a SHA-256 checksum, and creates the GitHub Release.
5. Verify the release page and attached assets. Check the checksum and provenance using the commands in `docs/PUBLISHING.md` before promoting it.

The CLI wheel is built and tested internally but is not published or attached. Do not run `pip install forgeloop` from PyPI; that name is used by an unrelated project. Read `docs/PUBLISHING.md` before considering any future package-index distribution.

## Public Claims

Use cautious language:

- measured packet-size reports
- token-aware, pointer-first memory lookup
- profile files are included for named tools
- live compatibility is confirmed only when a dated clean-session acceptance record exists

Avoid fixed token-saving percentages without benchmark evidence, claims that all integrations are deeply verified, claims that OpenCLI is bundled, and unsupported legal/compliance claims.
