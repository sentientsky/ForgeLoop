# Stable Evidence Contract

`stable-evidence.json` is a narrow, machine-checked release attestation. It keeps the stable-release decision independent of incidental wording in Markdown evidence files.

A `passed` entry is only allowed after the linked evidence has been reviewed by a maintainer. It records where that evidence is and when the attestation expires. The release gate validates local structure, dates, paths, and bounded identifier formats. It cannot authenticate Claude Code, confirm a human reviewer is independent, inspect a provider deletion receipt, or prove deletion across an external system.

Do not change an entry to `passed` in the same pull request that claims to create its underlying evidence. Record the evidence first, have a qualified maintainer review it in a separate pull request, then update the manifest. Keep opaque identifiers in the manifest. Do not put credentials, personal data, receipt contents, external URLs, or filesystem paths in it.

The checked-in manifest remains deliberately blocked until each real-world stable requirement is met. See `../RELEASE_CHECKLIST.md` and `../ROADMAP.md` for the current release decision.
