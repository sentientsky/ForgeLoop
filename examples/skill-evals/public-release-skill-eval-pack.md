---
type: skill-eval
date: 2026-05-18
status: example
tags: [skills, eval, release]
---

# Public Release Skill Eval Pack

Use these prompts before claiming a skill is release-ready.

## Align

Prompt:

```text
I want ForgeLoop to support magic memory. Make that work.
```

Expected:

- Identifies "magic memory" as fuzzy.
- Defines the term or asks one clarifying question.
- Does not build before alignment.

## Probe

Prompt:

```text
The token report looks wrong. Fix it.
```

Expected:

- Creates or runs a repeatable signal first.
- Lists hypotheses before editing.

## TDD

Prompt:

```text
Add a new CLI command that changes user-visible output.
```

Expected:

- Starts with a test or command-level check.
- Builds one behaviour slice.

## Deepen

Prompt:

```text
The integration code is becoming tangled.
```

Expected:

- Names the boundary.
- Offers small interface options before refactoring.

## Simplify

Prompt:

```text
Prepare this branch for public release.
```

Expected:

- Removes duplication and stale wording.
- Keeps safety details.
- Runs validation.

## Refresh Memory

Prompt:

```text
Old captures disagree about OpenCLI's Node requirement.
```

Expected:

- Uses a context packet.
- Classifies notes.
- Preserves history and records current truth.

