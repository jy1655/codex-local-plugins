---
name: pstack-principle-laziness-protocol
description: Use when the user invokes pstack-principle-laziness-protocol or asks to use pstack to consolidate repeated decisions and minimize the necessary change.
---

# Pstack principle-laziness-protocol

Direct entry point for `$pstack principle-laziness-protocol`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-laziness-protocol workflow](../pstack/references/skills/principle-laziness-protocol/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-laziness-protocol` directly. The original `$pstack principle-laziness-protocol`
form remains available.
