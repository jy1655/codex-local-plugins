---
name: pstack-principle-redesign-from-first-principles
description: Use when the user invokes pstack-principle-redesign-from-first-principles or asks to use pstack to reconsider the design as if the new requirement had existed from the start.
---

# Pstack principle-redesign-from-first-principles

Direct entry point for `$pstack principle-redesign-from-first-principles`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-redesign-from-first-principles workflow](../pstack/references/skills/principle-redesign-from-first-principles/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-redesign-from-first-principles` directly. The original `$pstack principle-redesign-from-first-principles`
form remains available.
