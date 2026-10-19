---
name: pstack-principle-migrate-callers-then-delete-legacy-apis
description: Use when the user invokes pstack-principle-migrate-callers-then-delete-legacy-apis or asks to use pstack to migrate callers before removing legacy APIs and obsolete tests.
---

# Pstack principle-migrate-callers-then-delete-legacy-apis

Direct entry point for `$pstack principle-migrate-callers-then-delete-legacy-apis`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-migrate-callers-then-delete-legacy-apis workflow](../pstack/references/skills/principle-migrate-callers-then-delete-legacy-apis/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-migrate-callers-then-delete-legacy-apis` directly. The original `$pstack principle-migrate-callers-then-delete-legacy-apis`
form remains available.
