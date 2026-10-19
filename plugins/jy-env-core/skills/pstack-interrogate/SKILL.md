---
name: pstack-interrogate
description: Use when the user invokes pstack-interrogate or asks to use pstack to review a change through independent investigators and evidence-based judgment.
---

# Pstack interrogate

Direct entry point for `$pstack interrogate`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the interrogate workflow](../pstack/references/skills/interrogate/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `interrogate` directly. The original `$pstack interrogate`
form remains available.
