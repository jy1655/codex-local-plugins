---
name: pstack-correct
description: Use when the user invokes pstack-correct or asks to use pstack to prevent recurring agent mistakes through architecture, types, and checks.
---

# Pstack correct

Direct entry point for `$pstack correct`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the correct workflow](../pstack/references/skills/correct/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `correct` directly. The original `$pstack correct`
form remains available.
