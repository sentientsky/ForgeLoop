# GitHub Setup And Release Operations

ForgeLoop's public repository is [sentientsky/ForgeLoop](https://github.com/sentientsky/ForgeLoop). It is already public; do not repeat the original create-and-push steps.

## Current Repository Controls

- `main` requires a pull request and passing Python 3.10-3.14 CI, package-quality, CodeQL, and fuzz checks.
- Branch protection is enforced for administrators; force-push and branch deletion are disabled; review conversations must be resolved.
- Required independent approvals remain at zero while there is one active maintainer. This is a disclosed solo-maintainer compromise, not equivalent to independent review. Add a second maintainer and raise the requirement to one approval before treating the process as team-reviewed.
- Dependabot alerts/security updates, secret scanning, push protection, and private vulnerability reporting are enabled.
- Scorecard notices about project age, review history, and the OpenSSF Best Practices badge are maturity signals, not confirmed source vulnerabilities.

Verify live settings in GitHub before each public release; repository settings can change independently of this document.

## Use The Repository As A Template

ForgeLoop's supported alpha distribution is the GitHub template. From the repository page, choose **Use this template** and create a new repository under the intended owner. GitHub creates a separate repository with the tracked files; repository rules, secrets, environments, and other settings must be configured separately. See [GitHub's template repository guide](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository).

The template is for starting a new project. It does not safely merge ForgeLoop files into an existing codebase. See `docs/INSTALLATION.md` for that limitation and the current manual-adoption boundary.

## Source Release

Follow `docs/PUBLISHING.md` and `docs/RELEASE_GUIDE.md`. A matching `v<version>` tag triggers verification, creation and attestation of a full source archive, a SHA-256 checksum, and a GitHub Release. The workflow does not publish to PyPI.

Do not configure a PyPI publisher or upload token for this repository. The PyPI name `forgeloop` and Python import namespace are used by another project; see `docs/PUBLISHING.md`.

## Human Release Checklist

- Review the full diff and latest test/security workflow results.
- Confirm no real `.env`, generated local setup files, or credentials are tracked.
- Confirm repository URLs, release notes, and compatibility evidence are current.
- Review dependency update pull requests; automation is not approval.
- Do not make GDPR, EU AI Act, HIPAA, SOC 2, or completed erasure claims without appropriate evidence and review.
