---
name: pstack-principle-model-the-domain
description: Use when the user invokes pstack-principle-model-the-domain or asks to use pstack to represent domain constraints in data structures instead of scattered conditions.
---

# Pstack principle-model-the-domain

Direct entry point for `$pstack principle-model-the-domain`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-model-the-domain workflow](../pstack/references/skills/principle-model-the-domain/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-model-the-domain` directly. The original `$pstack principle-model-the-domain`
form remains available.
