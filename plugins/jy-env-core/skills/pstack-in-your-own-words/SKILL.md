---
name: pstack-in-your-own-words
description: Use when the user invokes pstack-in-your-own-words or asks to use pstack to restate the user's goals and the problem they are trying to solve.
---

# Pstack in-your-own-words

Direct entry point for `$pstack in-your-own-words`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the in-your-own-words workflow](../pstack/references/skills/in-your-own-words/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `in-your-own-words` directly. The original `$pstack in-your-own-words`
form remains available.
