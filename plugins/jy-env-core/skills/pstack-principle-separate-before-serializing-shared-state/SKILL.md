---
name: pstack-principle-separate-before-serializing-shared-state
description: Use when the user invokes pstack-principle-separate-before-serializing-shared-state or asks to use pstack to separate independent state before serializing truly shared writes.
---

# Pstack principle-separate-before-serializing-shared-state

Direct entry point for `$pstack principle-separate-before-serializing-shared-state`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-separate-before-serializing-shared-state workflow](../pstack/references/skills/principle-separate-before-serializing-shared-state/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-separate-before-serializing-shared-state` directly. The original `$pstack principle-separate-before-serializing-shared-state`
form remains available.
