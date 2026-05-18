# Temporal Rules

Facts change. ForgeLoop should remember change without pretending history never happened.

## Required Fields For Time-Aware Notes

Use these fields when a memory may change:

```yaml
valid_from: YYYY-MM-DD
valid_to:
supersedes:
superseded_by:
status: current | superseded | archived
```

## Current Facts

A current fact has:

```yaml
status: current
valid_to:
superseded_by:
```

## Superseded Facts

When a fact changes:

1. Keep the old note.
2. Change `status` to `superseded`.
3. Set `valid_to`.
4. Link `superseded_by` to the newer note.
5. Link the newer note back with `supersedes`.

## Historical Facts

Historical facts are useful when they explain why a decision was made.

Do not delete them unless they contain unsafe information.

## Unsafe Memory

Remove or redact:

- passwords
- tokens
- private keys
- sensitive personal data
- confidential customer data

