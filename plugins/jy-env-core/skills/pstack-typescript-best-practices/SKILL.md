---
name: pstack-typescript-best-practices
description: Use when the user invokes pstack-typescript-best-practices or asks to use pstack to apply TypeScript patterns that model domain constraints and reject invalid states.
---

# Pstack typescript-best-practices

Direct entry point for `$pstack typescript-best-practices`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the typescript-best-practices workflow](../pstack/references/skills/typescript-best-practices/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `typescript-best-practices` directly. The original `$pstack typescript-best-practices`
form remains available.
