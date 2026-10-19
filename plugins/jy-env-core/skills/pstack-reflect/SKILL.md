---
name: pstack-reflect
description: Use when the user invokes pstack-reflect or asks to use pstack to extract durable conversation lessons and apply scoped skill improvements.
---

# Pstack reflect

Direct entry point for `$pstack reflect`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the reflect workflow](../pstack/references/skills/reflect/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `reflect` directly. The original `$pstack reflect`
form remains available.
