# Entity Model

An entity is a named thing ForgeLoop should remember over time.

Examples include tools, modules, projects, policies, people, preferences, and workflows.

## Entity File

Store entity notes in `docs/palace/entities/`.

Use this shape:

```yaml
type: entity
name: entity-name
entity_type: tool | module | project | person | policy | preference | workflow | other
status: current
valid_from: YYYY-MM-DD
valid_to:
superseded_by:
tags: []
```

## Required Sections

Each entity should include:

- what it is
- why it matters
- current state
- historical notes
- related drawers
- related timelines

## Rules

- Do not create an entity for every passing mention.
- Create one when the thing will likely matter again.
- Mark changed facts as superseded instead of deleting history.
- Do not store secrets or sensitive personal data.

