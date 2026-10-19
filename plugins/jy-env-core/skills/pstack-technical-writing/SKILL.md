---
name: pstack-technical-writing
description: Use when the user invokes pstack-technical-writing or asks to use pstack to write technical prose that engineers can understand on the first read.
---

# Pstack technical-writing

Direct entry point for `$pstack technical-writing`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the technical-writing workflow](../pstack/references/skills/technical-writing/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `technical-writing` directly. The original `$pstack technical-writing`
form remains available.
