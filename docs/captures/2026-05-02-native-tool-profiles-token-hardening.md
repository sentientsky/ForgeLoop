---
type: capture
date: 2026-05-02
status: current
tags: [compatibility, tokens, setup, security]
valid_from: 2026-05-02
---

# Native Tool Profiles And Token Hardening

ForgeLoop now uses a compatibility pattern:

```text
shared workflow, native entry files, short rules
```

Native profiles were added for Gemini, Windsurf, Cline, Roo Code, JetBrains AI, Kiro, OpenCode, and Aider.

The setup menu can select these tools and write only a local ignored profile file.

Token reporting now has a separate command:

```bash
python -m forgeloop tokens "<task query>" . --tool <tool> --limit 5
```

The important rule is that token counts are exact only when the report says `exact: true`.

This keeps ForgeLoop honest while still proving packet savings.

## Reusable Lesson

Do not duplicate long instructions into every tool file.

Keep tool-native files short, point them back to `AGENTS.md`, and use validation to make sure the expected anchors stay present.
