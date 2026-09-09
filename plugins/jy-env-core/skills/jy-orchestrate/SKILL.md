---
name: jy-orchestrate
description: Use when the user explicitly requests jy-orchestrate for Codex and Claude planning or implementation with independent Codex DevBlue and Claude verification.
---

# JY Orchestrate

The invoking session is the orchestrator. Delegate the requested planning or
implementation to Codex and Claude.

Have Codex DevBlue (`gpt-daybreak-blue-latest`) and Claude independently verify the same
result, using sessions separate from the workers. Route necessary fixes to the workers.

Use Agent Bridge when available locally, following the applicable local instructions.
