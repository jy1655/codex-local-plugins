---
name: pstack-principle-outcome-oriented-execution
description: Use when the user invokes pstack-principle-outcome-oriented-execution or asks to use pstack to organize changes around the intended and verifiable final state.
---

# Pstack principle-outcome-oriented-execution

Direct entry point for `$pstack principle-outcome-oriented-execution`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-outcome-oriented-execution workflow](../pstack/references/skills/principle-outcome-oriented-execution/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-outcome-oriented-execution` directly. The original `$pstack principle-outcome-oriented-execution`
form remains available.
