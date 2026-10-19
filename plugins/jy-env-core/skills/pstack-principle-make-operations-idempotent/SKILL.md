---
name: pstack-principle-make-operations-idempotent
description: Use when the user invokes pstack-principle-make-operations-idempotent or asks to use pstack to make state changes converge safely after retries or interruptions.
---

# Pstack principle-make-operations-idempotent

Direct entry point for `$pstack principle-make-operations-idempotent`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-make-operations-idempotent workflow](../pstack/references/skills/principle-make-operations-idempotent/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-make-operations-idempotent` directly. The original `$pstack principle-make-operations-idempotent`
form remains available.
