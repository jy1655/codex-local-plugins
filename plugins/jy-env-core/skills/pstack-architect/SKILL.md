---
name: pstack-architect
description: Use when the user invokes pstack-architect or asks to use pstack to compare architecture proposals and record the design rationale.
---

# Pstack architect

Direct entry point for `$pstack architect`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the architect workflow](../pstack/references/skills/architect/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `architect` directly. The original `$pstack architect`
form remains available.
