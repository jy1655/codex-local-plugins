---
name: pstack-setup-pstack
description: Use when the user invokes pstack-setup-pstack or asks to use pstack to configure optional pstack model roles without changing global settings.
---

# Pstack setup-pstack

Direct entry point for `$pstack setup-pstack`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the setup-pstack workflow](../pstack/references/skills/setup-pstack/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `setup-pstack` directly. The original `$pstack setup-pstack`
form remains available.
