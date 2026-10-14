---
type: standard
date: 2026-08-23
status: current
tags: [governance, memory, provenance, retention, erasure, security]
---

# Governed Memory Standard

## Purpose

This standard keeps governance metadata useful without turning ForgeLoop into a store of personal data.

It is informed by storage-limitation and accountability practices. It is not legal advice and does not determine whether a deployment is subject to the UK GDPR, EU GDPR, EU AI Act, HIPAA, or another regime.

## Default Rules

- Keep repository Markdown free of personal and special-category data.
- Use a separate governed store for any data that identifies or can reasonably identify a person.
- Reference people only through opaque identifiers such as `SUBJ-EXAMPLE-001`.
- Record provenance, purpose, jurisdiction, lawful basis, retention deadline, and downstream storage reference before relying on governed information.
- Keep audit events metadata-only. Never put raw content, names, emails, credentials, prompts, or outputs in an audit event.
- Review retention before its deadline. Erase or document a valid reason to retain.
- Treat Git history, forks, build artefacts, backups, embeddings, graphs, caches, and vendor copies as separate deletion targets.

## Required Metadata

For a pointer to personal or special-category content stored elsewhere, use this shape:

```yaml
data_classification: internal
governed_content_classification: personal
subject_ref: SUBJ-EXAMPLE-001
jurisdiction: GB
purpose: support
lawful_basis: contract
provenance_source: user-provided
provenance_recorded_at: 2026-08-23
retention_until: 2026-11-21
storage_ref: STORE-EXTERNAL-001
```

Supported `lawful_basis` values are `consent`, `contract`, `legal-obligation`, `vital-interests`, `public-task`, and `legitimate-interests`. A project must select the value that actually applies, or seek specialist advice.

## Audit Events

Use `forgeloop governance log` for the metadata event trail:

```bash
python -m forgeloop governance log access . --actor-ref OPERATOR-001 --record-ref STORE-EXTERNAL-001 --subject-ref SUBJ-EXAMPLE-001
python -m forgeloop governance verify .
```

The external audit log includes when an event occurred, what category of action took place, and hashes of the opaque actor, record, and subject references. It does not contain the personal data or the identifiers themselves.

## Erasure

Before completing an erasure request:

1. Identify every provider, index, embedding store, graph store, cache, backup, export, and replica that holds the data.
2. Obtain deletion or irreversible anonymisation evidence from each provider.
3. Confirm that no Git-tracked file or public history contains the data.
4. Record an `erase` audit event using opaque references.
5. Keep only the minimum metadata needed to evidence the request, subject to the project retention policy.

ForgeLoop cannot perform or prove these third-party deletions on its own. Never describe a deletion as complete based only on the ForgeLoop audit log.

New `erase` events require `--evidence-ref`, an opaque identifier for evidence held outside ForgeLoop. The event stores only a hash of that identifier. This is an operator attestation and does not validate the evidence, contact a provider, or establish that all replicas were erased. Existing `FGA/1` events remain verifiable but are not retroactively evidence-backed.
