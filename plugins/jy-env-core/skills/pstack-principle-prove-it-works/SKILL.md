---
name: pstack-principle-prove-it-works
description: Use when the user invokes pstack-principle-prove-it-works or asks to use pstack to verify the actual task output and distinguish evidence from assumptions.
---

# Pstack principle-prove-it-works

Direct entry point for `$pstack principle-prove-it-works`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-prove-it-works workflow](../pstack/references/skills/principle-prove-it-works/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-prove-it-works` directly. The original `$pstack principle-prove-it-works`
form remains available.
