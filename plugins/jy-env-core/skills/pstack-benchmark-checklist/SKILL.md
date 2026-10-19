---
name: pstack-benchmark-checklist
description: Use when the user invokes pstack-benchmark-checklist or asks to use pstack to verify performance measurements, variance, and the limiting resource.
---

# Pstack benchmark-checklist

Direct entry point for `$pstack benchmark-checklist`. This skill ships with the shared
`pstack` module in the same plugin; keep them installed together.

1. Read [the shared entry point](../pstack/SKILL.md) and
   [the Codex runtime adapter](../pstack/references/codex-runtime.md).
2. Read [the benchmark-checklist workflow](../pstack/references/skills/benchmark-checklist/WORKFLOW.md)
   and apply it to the user's task. Load other workflows only when this one calls for them.
3. Resolve workflow-relative links from the workflow's directory. Preserve the
   shared module's scope, model-role, and delegation rules, including its child briefs.

This invocation selects `benchmark-checklist` directly. The original `$pstack benchmark-checklist`
form remains available.
