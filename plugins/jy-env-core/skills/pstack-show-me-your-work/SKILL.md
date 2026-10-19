---
name: pstack-show-me-your-work
description: Use when the user invokes pstack-show-me-your-work or asks to use pstack to keep a canonical decision log with concise evidence pointers.
---

# Pstack show-me-your-work

Direct entry point for `$pstack show-me-your-work`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the show-me-your-work workflow](../pstack/references/skills/show-me-your-work/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `show-me-your-work` directly. The original `$pstack show-me-your-work`
form remains available.
