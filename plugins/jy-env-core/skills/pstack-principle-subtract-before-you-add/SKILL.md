---
name: pstack-principle-subtract-before-you-add
description: Use when the user invokes pstack-principle-subtract-before-you-add or asks to use pstack to remove unnecessary complexity before adding new mechanisms.
---

# Pstack principle-subtract-before-you-add

Direct entry point for `$pstack principle-subtract-before-you-add`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-subtract-before-you-add workflow](../pstack/references/skills/principle-subtract-before-you-add/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-subtract-before-you-add` directly. The original `$pstack principle-subtract-before-you-add`
form remains available.
