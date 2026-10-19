---
name: pstack-bro
description: Use when the user invokes pstack-bro or asks to use pstack to restate the previous answer in plain, concise language.
---

# Pstack bro

Direct entry point for `$pstack bro`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the bro workflow](../pstack/references/skills/bro/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `bro` directly. The original `$pstack bro`
form remains available.
