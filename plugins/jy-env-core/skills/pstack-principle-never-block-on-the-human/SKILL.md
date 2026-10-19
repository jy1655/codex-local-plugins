---
name: pstack-principle-never-block-on-the-human
description: Use when the user invokes pstack-principle-never-block-on-the-human or asks to use pstack to continue authorized work while keeping decisions and approval boundaries clear.
---

# Pstack principle-never-block-on-the-human

Direct entry point for `$pstack principle-never-block-on-the-human`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-never-block-on-the-human workflow](../pstack/references/skills/principle-never-block-on-the-human/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-never-block-on-the-human` directly. The original `$pstack principle-never-block-on-the-human`
form remains available.
