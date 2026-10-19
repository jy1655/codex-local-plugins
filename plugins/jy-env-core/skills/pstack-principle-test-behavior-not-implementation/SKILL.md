---
name: pstack-principle-test-behavior-not-implementation
description: Use when the user invokes pstack-principle-test-behavior-not-implementation or asks to use pstack to test observable behavior instead of private implementation details.
---

# Pstack principle-test-behavior-not-implementation

Direct entry point for `$pstack principle-test-behavior-not-implementation`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-test-behavior-not-implementation workflow](../pstack/references/skills/principle-test-behavior-not-implementation/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-test-behavior-not-implementation` directly. The original `$pstack principle-test-behavior-not-implementation`
form remains available.
