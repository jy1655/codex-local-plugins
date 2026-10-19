---
name: pstack-principle-foundational-thinking
description: Use when the user invokes pstack-principle-foundational-thinking or asks to use pstack to choose data structures and preserve options before adding logic.
---

# Pstack principle-foundational-thinking

Direct entry point for `$pstack principle-foundational-thinking`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-foundational-thinking workflow](../pstack/references/skills/principle-foundational-thinking/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-foundational-thinking` directly. The original `$pstack principle-foundational-thinking`
form remains available.
