---
name: pstack-create-verification-skill
description: Use when the user invokes pstack-create-verification-skill or asks to use pstack to create a project verification skill grounded in actual user flows.
---

# Pstack create-verification-skill

Direct entry point for `$pstack create-verification-skill`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the create-verification-skill workflow](../pstack/references/skills/create-verification-skill/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `create-verification-skill` directly. The original `$pstack create-verification-skill`
form remains available.
