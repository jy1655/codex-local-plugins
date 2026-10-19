---
name: pstack-make-bot-ui
description: Use when the user invokes pstack-make-bot-ui or asks to use pstack to build a UI for an existing authorized webhook bot backend.
---

# Pstack make-bot-ui

Direct entry point for `$pstack make-bot-ui`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the make-bot-ui workflow](../pstack/references/skills/make-bot-ui/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `make-bot-ui` directly. The original `$pstack make-bot-ui`
form remains available.
