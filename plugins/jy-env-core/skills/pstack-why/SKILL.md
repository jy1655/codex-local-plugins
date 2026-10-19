---
name: pstack-why
description: Use when the user invokes pstack-why or asks to use pstack to investigate the history and motivations behind a code design.
---

# Pstack why

Direct entry point for `$pstack why`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the why workflow](../pstack/references/skills/why/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `why` directly. The original `$pstack why`
form remains available.
