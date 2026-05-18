---
name: opencli-integrated
description: Use when a task could benefit from ForgeLoop's OpenCLI integrated peer plugin for website, browser, Electron, or local CLI automation.
---

# OpenCLI Integrated

Use this skill when the user asks ForgeLoop to use OpenCLI, browser-backed automation, website-to-CLI workflows, Electron app control, or deterministic external CLI access.

ForgeLoop integrates OpenCLI as a peer tool. It does not copy OpenCLI source, skills, adapters, or branding.

## Inputs

- User task.
- Repository root.
- OpenCLI status from ForgeLoop.
- Browser or site safety constraints.

## Steps

1. Run `python -m forgeloop opencli status .`.
2. If OpenCLI is missing, show `python -m forgeloop opencli plan .`.
3. Do not install, update, or run browser-backed commands unless the user explicitly asks.
4. Prefer read-only OpenCLI commands before write commands.
5. Use explicit sessions for browser work.
6. Avoid collecting secrets, cookies, tokens, or sensitive page data into ForgeLoop memory.
7. After any OpenCLI-assisted task, verify the result with ForgeLoop Check and Capture.

## Output

Create a short integration note:

```text
OpenCLI integrated run
- Status:
- Command class:
- Session:
- Data handled:
- Verification:
- Capture:
```

## Rules

- Treat OpenCLI as an external dependency.
- Do not vendor OpenCLI files into ForgeLoop.
- Use `@latest` only through the explicit ForgeLoop install command.
- Browser-backed commands reuse the user's logged-in browser, so treat them as privileged.
- Do not store live browser output in memory unless it is safe and necessary.
- Stop and ask if the task requires posting, deleting, buying, messaging, or changing account state.

## Done When

- OpenCLI status is known.
- The command path is explicit.
- Sensitive data was not captured.
- The result was verified or the limitation was stated.

