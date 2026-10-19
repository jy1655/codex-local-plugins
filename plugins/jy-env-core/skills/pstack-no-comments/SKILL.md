---
name: pstack-no-comments
description: Use when the user invokes pstack-no-comments or asks to use pstack to review and edit comments through the Comment Sicko workflow.
---

# Pstack no-comments

Direct entry point for `$pstack no-comments`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the no-comments workflow](../pstack/references/skills/no-comments/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `no-comments` directly. The original `$pstack no-comments`
form remains available.
