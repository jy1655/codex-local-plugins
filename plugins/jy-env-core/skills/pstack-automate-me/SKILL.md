---
name: pstack-automate-me
description: Use when the user invokes pstack-automate-me or asks to use pstack to turn recurring working conventions into a personal mode skill.
---

# Pstack automate-me

Direct entry point for `$pstack automate-me`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the automate-me workflow](../pstack/references/skills/automate-me/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `automate-me` directly. The original `$pstack automate-me`
form remains available.
