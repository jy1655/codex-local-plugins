---
name: pstack-ketchup
description: Use when the user invokes pstack-ketchup or asks to use pstack to summarize what changed since the user's previous message.
---

# Pstack ketchup

Direct entry point for `$pstack ketchup`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the ketchup workflow](../pstack/references/skills/ketchup/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `ketchup` directly. The original `$pstack ketchup`
form remains available.
