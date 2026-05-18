# ForgeLoop Project Language

## Core Terms

- ForgeLoop: the open source operating system for disciplined AI-assisted engineering.
- Loop: the five-stage path of Discover, Frame, Build, Check, and Capture.
- Discover: inspect the repo, task, memory, constraints, and risks before planning.
- Frame: turn discovery into scope, affected files, validation, rollback, and capture target.
- Build: implement in small reversible steps.
- Check: review and validate the change before completion.
- Capture: save reusable lessons, decisions, and changed facts.
- Memory palace: ForgeLoop's local-first markdown memory structure.
- Forge Context Packet: a compact pointer-only memory packet, also called FCP.
- Peer plugin: an optional integration kept outside ForgeLoop core and installed only by explicit user action.
- Doctor: the release health check that combines validation, compatibility, secrets, memory, CI, tokenizer, and integration status.

## Review Terms

- P1: must fix before completion.
- P2: should fix soon or record clearly.
- P3: useful improvement, not blocking.
- Reviewer routing: choosing specialist reviewers based on the risk of the change.
- Completion evidence: the short proof that the requested outcome, validation, docs, capture, and residual risk are handled.

## Memory Terms

- Capture note: a time-aware record of a lesson, decision, or changed fact.
- Solution note: a reusable pattern that can be applied again.
- Decision note: a durable trade-off that future maintainers may question.
- Superseded note: historical memory that remains true for the past but is no longer current guidance.

## Terms To Avoid

- AI-only language: avoid opaque compression that humans cannot audit.
- Auto-install: use explicit install because global tools and browser bridges are privileged.
- Token-saving claim: do not use this phrase publicly without command output, date, tool profile, and exactness.

