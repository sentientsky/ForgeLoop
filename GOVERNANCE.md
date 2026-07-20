# Governance

ForgeLoop is maintained in public. This document explains how changes are reviewed and who may approve them.

## Roles

- Contributors report issues, improve documentation, propose designs, and open pull requests.
- Reviewers examine changes but cannot merge unless they are also maintainers.
- Maintainers triage issues, protect releases, approve pull requests, and manage repository settings.

Maintainer access is earned through a sustained record of careful contributions, constructive reviews, security awareness, and respect for the Code of Conduct. Existing maintainers decide access in a public governance issue, excluding private security details.

## Pull Request Decisions

Pull requests are never auto-approved. Passing automation is evidence, not approval.

A normal pull request needs:

- a clear purpose and focused diff
- all required CI checks passing
- at least one maintainer approval
- resolved review conversations
- documentation and capture notes when behaviour or durable knowledge changed

The author may not count their own review as an independent approval. While ForgeLoop has only one active maintainer, that maintainer may merge their own low-risk change after all checks pass and the pull request has been open for at least 48 hours. The waiting period may be skipped for an actively exploited vulnerability, a broken release, or an obviously reversible documentation correction, with the reason recorded in the pull request.

Security controls, release workflows, secret handling, governance, and breaking changes need two maintainer approvals when two active maintainers are available. Before then, seek one independent reviewer with relevant experience and record any residual risk.

Auto-merge may be enabled only after required reviews and checks are satisfied. Dependabot pull requests follow the same review rules as human contributions.

## Releases

Only maintainers may create release tags or approve the protected `pypi` environment. A release must follow `docs/RELEASE_GUIDE.md`, use a tag matching the package version, and pass the release workflow.

## Decisions And Disagreements

Prefer evidence from tests, benchmarks, user workflows, and security analysis. If maintainers cannot reach consensus, keep the current behaviour and open a decision record in `docs/decisions/`.

Conduct concerns follow `CODE_OF_CONDUCT.md`. Vulnerabilities follow `SECURITY.md` and must not be debated in public issues before coordinated disclosure.

## Changes To Governance

Governance changes use the same pull request process and should remain open for at least seven days for public comment unless they close an urgent security gap.
