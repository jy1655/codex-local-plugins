---
name: pstack-principle-boundary-discipline
description: Use when the user invokes pstack-principle-boundary-discipline or asks to use pstack to place validation at boundaries and keep business logic in pure functions.
---

# Pstack principle-boundary-discipline

Direct entry point for `$pstack principle-boundary-discipline`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-boundary-discipline workflow](../pstack/references/skills/principle-boundary-discipline/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-boundary-discipline` directly. The original `$pstack principle-boundary-discipline`
form remains available.
