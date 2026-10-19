---
name: pstack-swarm
description: Use when the user invokes pstack-swarm or asks to use pstack to partition or race scoped workers and aggregate their verified results.
---

# Pstack swarm

Direct entry point for `$pstack swarm`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the swarm workflow](../pstack/references/skills/swarm/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `swarm` directly. The original `$pstack swarm`
form remains available.
