---
name: pstack-tdd
description: Use when the user invokes pstack-tdd or asks to use pstack to reproduce a bug with a practical regression test before fixing it.
---

# Pstack tdd

Direct entry point for `$pstack tdd`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the tdd workflow](../pstack/references/skills/tdd/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `tdd` directly. The original `$pstack tdd`
form remains available.
