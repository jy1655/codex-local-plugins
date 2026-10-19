---
name: pstack-principle-guard-the-context-window
description: Use when the user invokes pstack-principle-guard-the-context-window or asks to use pstack to scope phases and evidence to fit the available context window.
---

# Pstack principle-guard-the-context-window

Direct entry point for `$pstack principle-guard-the-context-window`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-guard-the-context-window workflow](../pstack/references/skills/principle-guard-the-context-window/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-guard-the-context-window` directly. The original `$pstack principle-guard-the-context-window`
form remains available.
