---
name: pstack-principle-attack-the-premise
description: Use when the user invokes pstack-principle-attack-the-premise or asks to use pstack to reconsider a shared premise after repeated fixes fail the same check.
---

# Pstack principle-attack-the-premise

Direct entry point for `$pstack principle-attack-the-premise`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-attack-the-premise workflow](../pstack/references/skills/principle-attack-the-premise/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-attack-the-premise` directly. The original `$pstack principle-attack-the-premise`
form remains available.
