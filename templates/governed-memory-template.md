---
type: palace-drawer
date: YYYY-MM-DD
status: current
data_classification: internal
governed_content_classification: personal
subject_ref: SUBJ-EXAMPLE-001
jurisdiction: GB
purpose: support
lawful_basis: contract
provenance_source: user-provided
provenance_recorded_at: YYYY-MM-DD
retention_until: YYYY-MM-DD
storage_ref: STORE-EXTERNAL-001
tags: [governed-memory]
---

# Governed Memory Pointer: Short Name

## External Storage Pointer

Store no personal data in this file. `storage_ref` must point to a separately governed external store that can report deletion, access, and retention outcomes.

## Provenance

- Source type:
- Source date:
- Collection purpose:
- Human reviewer, if any:

## Retention And Erasure

- Jurisdiction:
- Retention review date:
- Erasure route:
- Downstream stores:

## Audit Events

Use opaque references only. Record metadata-only events with:

```bash
python -m forgeloop governance log collect . --actor-ref OPERATOR-001 --record-ref STORE-EXTERNAL-001 --subject-ref SUBJ-EXAMPLE-001
```
