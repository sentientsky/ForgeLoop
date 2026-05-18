---
type: standard
status: current
tags: [tokens, measurement, compatibility, security]
valid_from: 2026-05-02
---

# Token Measurement Standard

ForgeLoop must not make public token-saving claims without measured output.

## Rule

Every token-saving claim needs:

- the exact command that produced the report
- the tool profile used
- the packet size
- the selected source size
- whether the token count was exact or estimated
- the repository state or commit when measured

## Commands

Use byte-level packet measurement:

```bash
python -m forgeloop pack "<task query>" . --limit 5
```

Use tool-specific token measurement:

```bash
python -m forgeloop tokens "<task query>" . --tool codex --limit 5
```

Use all profiles:

```bash
python -m forgeloop tokens "<task query>" . --tool all-supported --limit 5
```

## Exact Counts

Exact counts are only exact when the report says `exact: true`.

Codex can use a local `tiktoken` tokenizer when the optional dependency is installed:

```bash
pip install -e ".[tokenizers]"
```

Other tools can route through several models or require provider token APIs. ForgeLoop does not call provider APIs by default because that can require secrets and network access.

## Security

Token reports must not include secrets.

Do not paste real prompts that contain credentials, private keys, tokens, customer data, or sensitive personal data.

If a token report needs provider APIs later, it must read credentials only from the external ForgeLoop secrets file, never from a committed `.env` file.

## Wording

Allowed:

- "This report estimated a 70.2 percent token saving for the selected source files."
- "This Codex report used an exact local tokenizer."

Not allowed:

- "ForgeLoop saves 90 percent of tokens" without the command and report.
- "Exact token savings" when `exact` is false.
- "Lossless compression" without explaining that ForgeLoop is lossless by reference.
