# Interface Options

When deepening a design, consider:

- Keep the existing interface and simplify internals.
- Add a small adapter around an external dependency.
- Move validation closer to input.
- Split read-only reporting from write actions.
- Make risky behaviour explicit through flags.

Reject options that:

- hide errors
- increase always-loaded context
- spread one concept across many files
- require broad rewrites before value appears

