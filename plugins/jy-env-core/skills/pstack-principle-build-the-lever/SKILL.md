---
name: pstack-principle-build-the-lever
description: Use when the user invokes pstack-principle-build-the-lever or asks to use pstack to build a reusable tool that performs or verifies the requested work.
---

# Pstack principle-build-the-lever

Direct entry point for `$pstack principle-build-the-lever`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the principle-build-the-lever workflow](../pstack/references/skills/principle-build-the-lever/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `principle-build-the-lever` directly. The original `$pstack principle-build-the-lever`
form remains available.
