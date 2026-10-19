---
name: pstack-how
description: Use when the user invokes pstack-how or asks to use pstack to investigate how code works and explain its execution paths.
---

# Pstack how

Direct entry point for `$pstack how`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the how workflow](../pstack/references/skills/how/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `how` directly. The original `$pstack how`
form remains available.
