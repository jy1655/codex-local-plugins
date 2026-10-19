---
name: pstack-figure-it-out
description: Use when the user invokes pstack-figure-it-out or asks to use pstack to design a verifiable workflow for a task without a matching playbook.
---

# Pstack figure-it-out

Direct entry point for `$pstack figure-it-out`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the figure-it-out workflow](../pstack/references/skills/figure-it-out/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `figure-it-out` directly. The original `$pstack figure-it-out`
form remains available.
