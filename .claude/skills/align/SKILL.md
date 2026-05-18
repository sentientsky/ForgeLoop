---
name: align
description: Use when the goal, vocabulary, constraints, or decision surface is fuzzy and the agent needs shared language before planning.
---

# Align

Use this skill before Frame when a task contains unclear terms, competing goals, or decisions that could shape future work.

## Inputs

- User request.
- Existing project language.
- Relevant decisions.
- Current repo context.

## Steps

1. Identify fuzzy terms, contradictions, missing decisions, and hidden assumptions.
2. Propose short human-readable definitions for important terms.
3. Ask only for information that genuinely changes the path.
4. Record a decision only if it is surprising, costly to reverse, or easy to forget.
5. Update project language when a term will be reused.

## Output

Use one of these:

- A short alignment note in the conversation for simple tasks.
- `docs/language/PROJECT_LANGUAGE.md` for reusable terms.
- `docs/decisions/NNNN-short-title.md` for durable decisions.

## Rules

- Keep language human-readable.
- Do not invent opaque AI-only codes.
- Use one sentence per term.
- Prefer a small decision note over a long essay.
- Do not turn every preference into a decision record.

## Done When

- Key terms are clear.
- The next frame can be written without guessing.
- Any durable decision has a home.

