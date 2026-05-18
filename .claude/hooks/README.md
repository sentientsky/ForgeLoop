# Hooks

This folder is for hook guidance and future hook scripts.

ForgeLoop does not enable active hooks by default in the MVP. That is intentional. Hooks can run commands automatically, so the first version keeps them as examples until a project maintainer chooses which ones are safe.

## Useful Future Hooks

- `InstructionsLoaded`: remind Claude to follow the ForgeLoop loop.
- `TaskCompleted`: prompt for Capture when a non-trivial task ends.
- `PreCompact`: save current state before context is compacted.
- `FileChanged`: run project-specific validation after important files change.

## Rule

Only add active hooks when the command is deterministic, safe, and useful across the project.

Prefer hook examples first, then promote them to active settings after they have been tested.

