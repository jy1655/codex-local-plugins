---
name: pstack-principle-encode-lessons-in-structure
description: Use when the user invokes pstack-principle-encode-lessons-in-structure or asks to use pstack to encode recurring lessons in enforceable structure when possible.
---

# Pstack principle-encode-lessons-in-structure

Direct entry point for `$pstack principle-encode-lessons-in-structure`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-encode-lessons-in-structure workflow](../pstack/references/skills/principle-encode-lessons-in-structure/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-encode-lessons-in-structure` directly. The original `$pstack principle-encode-lessons-in-structure`
form remains available.
