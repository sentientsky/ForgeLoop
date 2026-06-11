# Installation

ForgeLoop is a local-first Python package.

## Requirements

- Python 3.10 or newer
- Git
- A terminal

Optional:

- Node.js and npm for OpenCLI integration
- `tiktoken` for exact local Codex-style token counts

## Install For Local Development

From the repository root:

```bash
python -m pip install -e .
```

With optional tokeniser support:

```bash
python -m pip install -e ".[tokenizers]"
```

With release tooling:

```bash
python -m pip install -e ".[dev]"
```

## Verify Installation

```bash
python -m forgeloop doctor .
python -m forgeloop validate .
forgeloop intro --plain
```

## Select Your AI Tool

```bash
python -m forgeloop setup .
```

The setup profile is local-only and ignored by Git.

## Optional OpenCLI

Preview first:

```bash
python -m forgeloop opencli plan .
```

Install only when explicitly wanted:

```bash
python -m forgeloop opencli install . --execute
```

