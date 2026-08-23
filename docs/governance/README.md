# Governance-First Memory

ForgeLoop keeps its public repository memory free of personal data. This folder documents the governance controls that apply when a project needs to reference externally stored governed data.

## What Is Implemented

- metadata checks for provenance, purpose, lawful basis, jurisdiction, retention, and opaque subject references
- a local audit log outside the repository with a SHA-256 hash chain
- audit events for collection, access, update, export, sharing, erasure, and retention review
- a validation rule that rejects personal or special-category data in repository-backed Markdown

Run:

```bash
python -m forgeloop governance audit .
python -m forgeloop governance log collect . --actor-ref OPERATOR-001 --record-ref STORE-EXTERNAL-001 --subject-ref SUBJ-EXAMPLE-001
python -m forgeloop governance verify .
```

Audit events use opaque references and write only hashed identifiers. The log is local to the operating-system user profile, outside the repository. `FORGELOOP_GOVERNANCE_HOME` can set a different local location.

## What Is Not Claimed

ForgeLoop is not a legal-compliance certification, a hosted privacy service, or an erasure engine for third-party embeddings, graphs, backups, Git history, or vendor APIs.

The hash chain is tamper-evident, not tamper-proof. A project must still secure its operating-system account, govern every downstream store, set its own retention periods, and obtain legal advice for its use case.

## Using Governed Metadata

Start from `templates/governed-memory-template.md`. The Markdown file is an internal pointer, never the personal data itself.

For personal or special-category data, supply:

- `subject_ref`: an opaque identifier such as `SUBJ-EXAMPLE-001`, never a name or email address
- `jurisdiction`: an ISO country code, `EEA`, or `GLOBAL`
- `purpose`, `lawful_basis`, `provenance_source`, and `provenance_recorded_at`
- `retention_until`: an explicit review or erasure deadline
- `storage_ref`: the external store that must participate in an erasure request

The governance audit checks metadata only. It does not read, index, transmit, or delete external data.

## Right-To-Erasure Boundary

Do not put personal data in Git-tracked files. Removing a file from a working tree does not erase prior Git commits, forks, clones, build artefacts, or third-party stores.

An external memory provider must implement and evidence deletion across every copy it controls before a project can describe a request as complete. Record the resulting `erase` event only after the provider has returned its own deletion evidence.

Read `../standards/governed-memory-standard.md` before enabling a governed memory provider.
