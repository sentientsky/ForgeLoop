# GitHub Setup

This guide covers the one-time steps that require the repository owner's GitHub account.

Target repository: `https://github.com/sentientsky/ForgeLoop`

## 1. Prepare The Local Repository

Run the release gate in `RELEASE_GUIDE.md`. Confirm the primary branch is `main`:

```bash
git branch --show-current
git branch -m main
```

The second command is needed only when the branch has another name.

## 2. Create And Push The Repository

### Create It In The Browser

On the GitHub page shown in the launch screenshot, use:

- Owner: `sentientsky`
- Repository name: `ForgeLoop`
- Description: `An open source operating system for disciplined AI-assisted engineering.`
- Visibility: `Public`
- Add README: `Off`
- Add .gitignore: `No .gitignore`
- Add licence: leave the existing local `MIT Licence` unchanged by selecting `No licence` here

Click **Create repository**. Do not initialise the remote with a README, `.gitignore`, or licence because ForgeLoop already has them.

### Connect And Push The Existing Local Repository

After GitHub shows the empty repository page, run these commands from the ForgeLoop folder:

```bash
git remote add origin https://github.com/sentientsky/ForgeLoop.git
git remote -v
git push -u origin main
```

If GitHub asks you to sign in, complete the browser prompt. Use Git Credential Manager or GitHub CLI authentication. Do not paste a personal access token into the repository, a command transcript, or any ForgeLoop file.

### Alternative: GitHub CLI

```bash
gh auth login
gh repo create ForgeLoop --public --source . --remote origin --push
```

## 3. Replace Repository-Specific Values

The local launch configuration is already prepared with the `sentientsky/ForgeLoop` URLs:

- `pyproject.toml` has the homepage, documentation, issues, and source URLs.
- `.github/ISSUE_TEMPLATE/config.yml` has the private security-advisory link.
- `.github/CODEOWNERS` routes repository review requests to `@sentientsky`.

After the first push, verify the security link opens this repository's advisory form:

```yaml
contact_links:
  - name: Security issue
    url: https://github.com/sentientsky/ForgeLoop/security/advisories/new
    about: Follow SECURITY.md. Do not publish exploit details in public issues.
```

The public package metadata deliberately keeps the author as `ForgeLoop contributors`. An email address is not required for GitHub, PyPI, or project ownership. Configure your Git email locally only if you want future commits attributed to that address.

## 4. Protect `main`

Create a branch ruleset for `main`:

- require a pull request before merging
- require at least one approval
- dismiss stale approvals after new commits
- require all conversations to be resolved
- require the CI and CodeQL checks that appear after the first workflow run
- block force pushes and branch deletion
- allow bypass only for an emergency maintainer role

Do not enable automatic approval. Auto-merge is acceptable only after every required check and human approval has completed.

## 5. Enable Security Features

In repository settings, enable every feature available to the account:

- Dependabot alerts and security updates
- secret scanning and push protection
- private vulnerability reporting
- CodeQL code scanning
- dependency graph

Review the first Scorecard and CodeQL runs rather than treating a green workflow icon as proof that no risk exists.

## 6. Configure PyPI Trusted Publishing

Create a protected GitHub environment named `pypi`. Add a required reviewer when the account plan supports it.

In PyPI, add a Trusted Publisher with:

- GitHub owner `sentientsky`
- repository `ForgeLoop`
- workflow `release.yml`
- environment `pypi`

Do not add a long-lived PyPI token to GitHub secrets.

## 7. First Public Release

Update `CHANGELOG.md`, set the package version, and run the complete release gate. Then create and push the matching tag:

```bash
git tag -s v0.1.0 -m "ForgeLoop 0.1.0"
git push origin v0.1.0
```

Use an unsigned annotated tag only when signed tags are not yet configured. The release workflow rejects a tag that does not match `pyproject.toml`, tests the built wheel in isolation, creates build provenance, and publishes through the protected `pypi` environment.

## 8. Finish The Repository Page

- Add the description from `GITHUB_PAGE.md`.
- Add the recommended topics from `RELEASE_GUIDE.md`.
- Create labels such as `good first issue`, `security`, `documentation`, and `integration`.
- Pin a roadmap or first-release discussion.
- Verify every link while signed out of GitHub.
