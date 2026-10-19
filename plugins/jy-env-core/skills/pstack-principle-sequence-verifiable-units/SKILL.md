---
name: pstack-principle-sequence-verifiable-units
description: Use when the user invokes pstack-principle-sequence-verifiable-units or asks to use pstack to sequence work into small units with a check at each boundary.
---

# Pstack principle-sequence-verifiable-units

Direct entry point for `$pstack principle-sequence-verifiable-units`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-sequence-verifiable-units workflow](../pstack/references/skills/principle-sequence-verifiable-units/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-sequence-verifiable-units` directly. The original `$pstack principle-sequence-verifiable-units`
form remains available.
