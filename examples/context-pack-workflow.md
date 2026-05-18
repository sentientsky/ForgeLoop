# Context Pack Workflow

Use this when a task may depend on older ForgeLoop decisions.

## Prompt

```text
Before planning, run a ForgeLoop context pack for "security memory validation".
Open only the listed files that matter.
Then continue with Discover and Frame.
```

## Command

```bash
python -m forgeloop pack "security memory validation" . --limit 5
```

## Expected Behaviour

Claude reads the FCP/1 packet, chooses the most relevant paths, opens those source files, and avoids loading the whole memory folder.

The packet reports measured byte savings. Use those numbers when discussing token reduction.
