---
name: pstack-poteto-mode
description: Use when the user invokes pstack-poteto-mode or asks to use pstack to select and execute the matching poteto-mode playbook.
---

# Pstack poteto-mode

Direct entry point for `$pstack poteto-mode`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the poteto-mode workflow](../pstack/references/skills/poteto-mode/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `poteto-mode` directly. The original `$pstack poteto-mode`
form remains available.
