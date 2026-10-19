---
name: pstack-unslop
description: Use when the user invokes pstack-unslop or asks to use pstack to remove formulaic AI prose while preserving meaning and tone.
---

# Pstack unslop

Direct entry point for `$pstack unslop`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the unslop workflow](../pstack/references/skills/unslop/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `unslop` directly. The original `$pstack unslop`
form remains available.
