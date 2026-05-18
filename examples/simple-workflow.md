# Example Workflow

This example shows how a beginner might use ForgeLoop with Claude Code.

## User Request

```text
Add a CSV export button to my habit tracker.
```

## 1. Discover

Claude inspects the repo, reads the existing habit list code, checks whether export already exists, and searches previous captures for export patterns.

Expected output:

```text
docs/discoveries/2026-04-17-csv-export.md
```

## 2. Frame

Claude creates a small plan.

Example frame:

- Add one export button near the habit list.
- Generate CSV from the current habits in the browser.
- Do not add a backend.
- Validate by exporting sample habits and opening the file.

Expected output:

```text
docs/frames/2026-04-17-csv-export.md
```

## 3. Build

Claude implements the button and CSV generation in small steps.

Expected output:

```text
docs/builds/2026-04-17-csv-export.md
```

## 4. Check

Claude reviews the change using the architecture, security, testing, and documentation reviewers.

Example findings:

- P1: None.
- P2: Add a test for escaping commas in habit names.
- P3: Add a short README note for export behaviour.

Expected output:

```text
docs/checks/2026-04-17-csv-export.md
```

## 5. Capture

Claude stores the reusable lesson:

```text
When adding browser-only exports, handle commas, quotes, and new lines before creating the download.
```

Expected outputs:

```text
docs/captures/2026-04-17-csv-export.md
docs/solutions/browser-csv-export.md
docs/palace/drawers/2026-04-17-browser-csv-export.md
```

## Why This Helps

The next time the user asks for an export feature, Claude can reuse the stored solution instead of rediscovering the same edge cases.

