---
name: pstack-principle-exhaust-the-design-space
description: Use when the user invokes pstack-principle-exhaust-the-design-space or asks to use pstack to explore alternative designs before committing to a solution.
---

# Pstack principle-exhaust-the-design-space

Direct entry point for `$pstack principle-exhaust-the-design-space`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-exhaust-the-design-space workflow](../pstack/references/skills/principle-exhaust-the-design-space/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-exhaust-the-design-space` directly. The original `$pstack principle-exhaust-the-design-space`
form remains available.
