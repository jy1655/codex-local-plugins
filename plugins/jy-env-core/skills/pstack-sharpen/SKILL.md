---
name: pstack-sharpen
description: Use when the user invokes pstack-sharpen or asks to use pstack to clarify the real goal and improve the approach before executing the task.
---

# Pstack sharpen

Direct entry point for `$pstack sharpen`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the sharpen workflow](../pstack/references/skills/sharpen/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `sharpen` directly. The original `$pstack sharpen`
form remains available.
