# Security Policy

ForgeLoop is an early open source project. Please report security issues responsibly.

## Supported Versions

The current development version is supported until the first public release process is defined.

## Reporting A Vulnerability

If you find a security issue, open a private security advisory on GitHub once the repository is public.

Until then, do not publish exploit details in public issues.

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
