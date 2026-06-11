# Publishing

ForgeLoop should use PyPI Trusted Publishing rather than long-lived API tokens.

## Local Build Check

```bash
python -m pip install -e ".[dev]"
python -m build
python -m twine check dist/*
```

Do not commit `dist/`.

## Release Flow

1. Run the release gate in `docs/RELEASE_GUIDE.md`.
2. Update `CHANGELOG.md`.
3. Commit the release changes.
4. Create a signed or reviewed tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

5. Let the GitHub release workflow publish the package.

## Trusted Publishing Setup

In PyPI, configure a trusted publisher for:

- repository owner
- repository name
- workflow file: `release.yml`
- environment: `pypi`

ForgeLoop's workflow does not store a PyPI token.

## Before First Publish

Set real project URLs in `pyproject.toml` after the GitHub repository URL is final.

Do not publish with placeholder URLs.

