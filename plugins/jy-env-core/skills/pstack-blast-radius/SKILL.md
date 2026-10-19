---
name: pstack-blast-radius
description: Use when the user invokes pstack-blast-radius or asks to use pstack to find and verify downstream breakage caused by a proposed change.
---

# Pstack blast-radius

Direct entry point for `$pstack blast-radius`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the blast-radius workflow](../pstack/references/skills/blast-radius/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `blast-radius` directly. The original `$pstack blast-radius`
form remains available.
