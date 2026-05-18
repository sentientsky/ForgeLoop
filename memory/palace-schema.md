# Palace Schema

ForgeLoop uses a simple local-first memory palace.

The palace is not a database in the MVP. It is a clear folder and metadata structure that can later become an indexed store or MCP-backed memory system.

## Structure

```text
docs/palace/
+-- wings/
+-- rooms/
+-- drawers/
+-- entities/
+-- timelines/
+-- indexes/
```

## Wings

Wings are broad domains.

Examples:

- product
- engineering
- design
- operations
- research
- personal-preferences

## Rooms

Rooms are focused containers inside a wing.

Examples:

- a project
- a workstream
- a session
- a topic
- a feature area

## Drawers

Drawers are the actual memory units.

They may store:

- decisions
- plans
- reviews
- fixes
- reusable lessons
- user preferences
- assumptions
- bug explanations

## Entities

Entities are named things ForgeLoop may need to track over time.

Examples:

- a tool
- a dependency
- a module
- a person
- a policy
- a product area

## Timelines

Timelines record changing truth.

They should answer:

- what was true
- when it became true
- when it stopped being true
- what replaced it

## Indexes

Indexes help future sessions find memory quickly.

Indexes may group memory by:

- tag
- wing
- entity
- task type
- repeated mistake
- reusable solution
