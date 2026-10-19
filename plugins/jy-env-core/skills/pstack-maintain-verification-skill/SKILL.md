---
name: pstack-maintain-verification-skill
description: Use when the user invokes pstack-maintain-verification-skill or asks to use pstack to repair a project's verification skill against the current product.
---

# Pstack maintain-verification-skill

Direct entry point for `$pstack maintain-verification-skill`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the maintain-verification-skill workflow](../pstack/references/skills/maintain-verification-skill/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `maintain-verification-skill` directly. The original `$pstack maintain-verification-skill`
form remains available.
