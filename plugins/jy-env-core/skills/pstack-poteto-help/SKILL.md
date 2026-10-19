---
name: pstack-poteto-help
description: Use when the user invokes pstack-poteto-help or asks to use pstack to explain the available pstack workflows and invocation examples.
---

# Pstack poteto-help

Direct entry point for `$pstack poteto-help`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the poteto-help workflow](../pstack/references/skills/poteto-help/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `poteto-help` directly. The original `$pstack poteto-help`
form remains available.
