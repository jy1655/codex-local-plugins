---
name: pstack-principle-type-system-discipline
description: Use when the user invokes pstack-principle-type-system-discipline or asks to use pstack to use types to reject invalid states, mismatched values, and missing variants.
---

# Pstack principle-type-system-discipline

Direct entry point for `$pstack principle-type-system-discipline`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-type-system-discipline workflow](../pstack/references/skills/principle-type-system-discipline/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-type-system-discipline` directly. The original `$pstack principle-type-system-discipline`
form remains available.
