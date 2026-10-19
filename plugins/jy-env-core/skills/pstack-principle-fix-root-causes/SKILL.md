---
name: pstack-principle-fix-root-causes
description: Use when the user invokes pstack-principle-fix-root-causes or asks to use pstack to trace a symptom to the first incorrect state and fix its cause.
---

# Pstack principle-fix-root-causes

Direct entry point for `$pstack principle-fix-root-causes`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-fix-root-causes workflow](../pstack/references/skills/principle-fix-root-causes/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-fix-root-causes` directly. The original `$pstack principle-fix-root-causes`
form remains available.
