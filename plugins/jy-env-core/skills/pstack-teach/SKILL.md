---
name: pstack-teach
description: Use when the user invokes pstack-teach or asks to use pstack to combine how and why investigations into an explanation at the user's pace.
---

# Pstack teach

Direct entry point for `$pstack teach`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the teach workflow](../pstack/references/skills/teach/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `teach` directly. The original `$pstack teach`
form remains available.
