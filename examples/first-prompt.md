# First Prompt

Paste this into Claude Code when starting inside a project that uses ForgeLoop:

```text
Read README.md and CLAUDE.md, then use the ForgeLoop workflow.

Start with /discover for this task:

[describe the task here]

Keep explanations simple, use UK English, and do not edit product code until the work has been framed.
```

After the discovery is done, continue with:

```text
/frame Use the latest discovery and create a practical plan.
```

Then:

```text
/build Implement the approved frame in small, reversible steps.
```

Then:

```text
/check Review the result using ForgeLoop reviewers.
```

Finally:

```text
/capture Store the reusable lesson and update palace memory if useful.
```

