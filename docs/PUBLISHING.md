# Publishing ForgeLoop

ForgeLoop currently ships through its public GitHub repository and source-template flow. It does **not** publish a Python distribution to PyPI.

## Why There Is No PyPI Release

The normalized PyPI project name `forgeloop` is already used by an unrelated package ([project page](https://pypi.org/project/forgeloop/)). The Python import namespace also overlaps. ForgeLoop must not publish to, or tell users to install from, that project. The current wheel contains the CLI only, not the skills, rules, templates, and docs that make up the complete ForgeLoop system.

Do not run `pip install forgeloop` from the public package index. Use the GitHub template instead. Reconsider PyPI only after choosing and verifying a distinct distribution **and** import namespace, packaging the complete product assets, and testing installation and upgrades in clean environments.

## GitHub Source Release

The tag-triggered workflow verifies the release, builds a source archive from tracked files, checks for local-only secret files, creates a SHA-256 checksum, attests the archive, and creates a GitHub Release. A retry compares existing release assets byte-for-byte and fails closed if an asset differs. The Python wheel is built and smoke-tested internally but is not attached or published. An active repository ruleset prevents `v*` tags from being updated or deleted, so never reuse a published version tag; release corrections require a new version.

Before tagging:

1. Merge the release changes through a reviewed pull request and confirm the latest CI, CodeQL, and fuzz checks pass on `main`.
2. Review dependency update pull requests and open security alerts.
3. Update `CHANGELOG.md` and confirm the version in `pyproject.toml` is intended for a source alpha.
4. Check `git status --short` is clean and run the gate in `docs/RELEASE_GUIDE.md`.
5. Create and push the matching tag:

```bash
git tag -a v0.1.0 -m "ForgeLoop 0.1.0 source alpha"
git push origin v0.1.0
```

The workflow must pass before promoting the release. Verify the downloaded archive against its `.sha256` file and, where GitHub CLI is installed, verify its provenance:

```bash
sha256sum --check ForgeLoop-v0.1.0-source.zip.sha256
gh attestation verify ForgeLoop-v0.1.0-source.zip --repo sentientsky/ForgeLoop
```

The release contains the full repository source, not a standalone installed toolkit for an existing project.

## Future Package-Index Release Gate

A PyPI release is a separate product decision, not a checkbox. Before enabling it:

- reserve a unique normalized PyPI name and import namespace under the maintainer's account;
- include all advertised skills, profiles, templates, and documentation in the installable artifact;
- test clean installation, upgrade, uninstall, and conflict handling on Windows, macOS, and Linux;
- configure PyPI Trusted Publishing for the exact GitHub owner, repository, workflow, and protected environment;
- test the publisher on TestPyPI and verify provenance before publishing a stable release.

PyPI recommends OIDC Trusted Publishing with an optional GitHub `pypi` environment, not long-lived upload tokens. See [PyPI's Trusted Publisher guide](https://docs.pypi.org/trusted-publishers/using-a-publisher/).
