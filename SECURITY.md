# Security Policy

ForgeLoop is an early open source project. Please report security issues responsibly.

## Supported Versions

| Version | Supported |
| --- | --- |
| Latest `0.1.x` release | Yes |
| Unreleased `main` branch | Best effort |
| Older versions | No |

## Reporting A Vulnerability

If you find a security issue, use private vulnerability reporting or open a private security advisory on GitHub once the repository is public. Include affected versions, reproduction steps, impact, and any suggested mitigation.

Until then, do not publish exploit details in public issues.

Maintainers should acknowledge a private report within three working days, provide an initial assessment within seven working days, and coordinate disclosure after a fix is available. Complex reports may take longer, but reporters should receive progress updates.

## Security Priorities

ForgeLoop is especially careful about:

- memory files storing secrets
- real `.env` files being committed
- unsafe hooks
- malformed MCP-style input in future integrations
- symlink traversal
- oversized files
- generated indexes leaking local paths
- version drift between docs, package, and examples
- optional browser bridges and global tool installs
- personal or special-category data in Git-tracked memory notes
- audit records that expose raw identifiers, content, or secrets

## Governed Memory Boundary

ForgeLoop's repository memory is not a personal-data store. Store only opaque references in governed Markdown metadata and keep the data itself in an external provider with its own access control, retention, export, and deletion controls.

Use `python -m forgeloop governance audit .` before committing governed-memory metadata. The local governance audit log is hash-chained and metadata-only; it is not an encryption system, legal certification, or proof that third-party embeddings, graphs, backups, or Git history have been erased.

## Current Status

The MVP does not enable active memory hooks or MCP tools by default.

This is intentional. Automation will be added only after the validation layer and tests are stable.

OpenCLI is optional and privileged. Browser-backed commands can reuse logged-in browser sessions, so ForgeLoop keeps OpenCLI install and doctor checks explicit.

## Local Secrets

Use:

```bash
python -m forgeloop secrets init .
python -m forgeloop secrets check .
```

Only `.env.example` belongs in the repository. The real secrets file is created outside the repository.
