---
type: check
date: 2026-11-12
status: current
tags: [governance, release, erasure, independent-review, evidence]
---

# Co-Founder-Style Governance And Evidence Audit

## Authority And Scope

This is an AI-generated, adversarial co-founder-style audit prepared at the repository owner's request. It is not a human co-founder, GitHub collaborator, independent maintainer review, legal opinion, or provider attestation. It must not be entered as evidence that either stable-release blocker has passed.

The audit covers GitHub issue [#40](https://github.com/sentientsky/ForgeLoop/issues/40), GitHub issue [#41](https://github.com/sentientsky/ForgeLoop/issues/41), current branch protection, repository governance, and Qdrant as a possible first external vector-store target.

## Executive Decision

- Issue #40 remains **blocked**. CI and automated security checks are strong evidence of process execution, not an independent human review. GitHub currently lists only `sentientsky` as a collaborator; `main` requires zero approvals and does not require CODEOWNERS review.
- Issue #41 remains **blocked**. Qdrant is selected as the first candidate for a narrowly scoped self-hosted adapter, but no adapter was executed against a real Qdrant service in this audit. No deletion occurred and no `erase` audit event was recorded.
- ForgeLoop is not ready for a stable-production promotion. The existing release gate remains authoritative and must not be weakened to convert these gaps into passes.

## Issue #40: Independent Review

### Evidence checked

- GitHub collaborator list: only `sentientsky` is active.
- `main` branch protection: nine required status contexts; administrator enforcement enabled; required approvals `0`; CODEOWNERS review disabled.
- The latest PR, [#62](https://github.com/sentientsky/ForgeLoop/pull/62), passed CI, CodeQL, fuzz, and cross-platform jobs. Those checks do not establish independent review.
- [Repository governance](../../GOVERNANCE.md) says an author cannot count their own review as independent and requires a 48-hour open period for a solo-maintainer low-risk self-merge (with listed exceptions).
- PR #62 was merged shortly after its checks passed. It includes CLI behaviour, so it is not obviously within the documented documentation-only exception to the 48-hour period. This audit records a process deviation; that merge must not be treated as a precedent for bypassing governance.

### Simulated reviewer conclusion

The current automation is a useful technical control, but the governance control is absent by design while the project has one maintainer. A second GitHub identity controlled by the same person, an AI agent, or a self-authored approval would not resolve this gap. Requiring one approval before another trusted reviewer exists would make ordinary changes unmergeable, so the current zero-approval setting is a disclosed temporary compromise, not a production-quality review process. The owner should also reconcile the standing immediate-merge instruction with the repository's 48-hour solo-maintainer policy before future merges.

### Required closure evidence

1. Owner identifies and invites a trusted, distinct person with relevant engineering/security experience.
2. That person accepts the project governance and completes a genuine review on a non-trivial pull request.
3. Owner adds the reviewer to the appropriate GitHub team/collaborator list and `.github/CODEOWNERS` where appropriate.
4. Owner changes branch protection to require one approval and CODEOWNERS review, then verifies the setting through the GitHub API.
5. Release evidence cites the human review and verified protection state. Do not count this report or an AI review as that evidence.

**Verdict: not passed; issue remains open.**

## Issue #41: Provider Erasure Evidence

### Candidate selected

Qdrant self-hosted is the first candidate for a narrowly scoped provider adapter. This is a design selection only; it does not mean Qdrant support has shipped or that any data has been erased.

### Provider behaviour and limitations

- Qdrant's point-delete API accepts point IDs or a filter and supports `wait=true`. That can establish completion of the operation in the live database, followed by a read-back check that the points are no longer visible through the Qdrant API. See [Qdrant point management](https://qdrant.tech/documentation/manage-data/points/) and the [delete-points API reference](https://api.qdrant.tech/master/api-reference/points/delete-points).
- Qdrant describes point deletion as a soft delete. Deleted points are excluded from API operations, while physical cleanup is performed later by the vacuum optimizer. An API read-back therefore does not prove immediate physical-media sanitisation. See [Qdrant FAQ: deletion and vacuum](https://qdrant.tech/documentation/faq/).
- Backup/snapshot retention is deployment-specific. Qdrant Private Cloud documentation says scheduled snapshots with retention are removed when retention expires, while snapshots without retention can remain indefinitely. This is not evidence about a particular operator's storage, object-versioning, replication, or backup account. See [Qdrant Private Cloud backup retention](https://qdrant.tech/documentation/private-cloud/backups/).
- Restoring a snapshot can restore deleted content. The deployment owner must inventory and expire or destroy every backup, replica, export, cache, and downstream embedding copy separately.

### Evidence available in this audit

- Current Qdrant API and backup behaviour was reviewed from official documentation on 2026-11-12.
- The local environment has no Docker CLI, Qdrant endpoint, or dedicated provider test account available for a real integration run.
- No external data was submitted or deleted. No Qdrant credentials were requested or inspected. No ForgeLoop erase event or provider receipt was created.

### Required implementation and verification before closure

1. Pin and document the supported Qdrant deployment/version and the required payload contract, using a pseudonymous subject reference rather than raw identity data.
2. Implement an explicit, opt-in delete adapter using a synchronous deletion request and a post-delete API query. Never log request payloads, API keys, raw content, or unredacted provider errors.
3. Run repeatable tests against a disposable, version-pinned Qdrant service with synthetic records; prove API invisibility after deletion and that unrelated subjects remain present.
4. Document the vacuum/physical-cleanup boundary and deployer's snapshot, backup, replica, and object-version retention controls. Capture evidence from the actual target deployment, not just this test service.
5. Only record an `erase` audit event after all in-scope copies are accounted for and provider/deployment evidence has been reviewed. Keep the receipt outside Git and store only an opaque evidence reference in ForgeLoop's log.
6. Keep public claims scoped to what the adapter actually verifies. Do not say physical or backup erasure is proven solely from the point-delete API response.

**Verdict: not passed; issue remains open.** The candidate is selected and the provider-specific evidence boundary is documented, but the adapter, live integration test, and deployment backup proof are absent.

## Remaining Owner Actions

- Recruit a real second maintainer for issue #40.
- Provide a disposable Qdrant test environment and decide which backup/retention deployment ForgeLoop will support for issue #41.
- Rerun the stable release gate only after the evidence above exists. An owner instruction can authorise the work, but it cannot make absent review history or provider deletion records exist.
