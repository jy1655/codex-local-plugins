---
name: pstack-principle-minimize-reader-load
description: Use when the user invokes pstack-principle-minimize-reader-load or asks to use pstack to reduce the layers and mutable context a reader must track.
---

# Pstack principle-minimize-reader-load

Direct entry point for `$pstack principle-minimize-reader-load`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-minimize-reader-load workflow](../pstack/references/skills/principle-minimize-reader-load/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-minimize-reader-load` directly. The original `$pstack principle-minimize-reader-load`
form remains available.
