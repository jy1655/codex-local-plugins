---
name: pstack
description: Use when the user invokes pstack or poteto-mode, or asks to use a named pstack workflow for investigation, implementation, verification, or review.
---

# Pstack for local Codex

This is the experimental pstack port inside the jy-env-core plugin. Keep this entry point,
its references, tools, license, and provenance together. It preserves the upstream
explicit invocation of poteto-mode; installation alone does not activate the mode.

## Start

1. Read [the Codex runtime adapter](references/codex-runtime.md). It defines the
   host-specific execution contract for every bundled workflow and takes precedence
   over retained upstream tool notation, including coexistence with other active skills.
   User and host instructions remain higher priority.
2. For `$pstack <task>` or `$pstack poteto-mode <task>`, read
   [poteto-mode](references/skills/poteto-mode/WORKFLOW.md), choose its matching
   playbook, and execute it within the user's scope.
3. For `$pstack <workflow> <task>`, read the named
   `references/skills/<workflow>/WORKFLOW.md`. For example, `how`, `why`, `architect`,
   `arena`, `swarm`, `interrogate`, `tdd`, `unslop`, `recall`, or `reflect`.
   Read poteto-mode's principles and delegation sections when that workflow calls for them.
4. `$pstack setup-pstack` configures optional model roles;
   `$pstack poteto-help` reads [the workflow index](references/workflows.md).

Bundled workflow names and slash examples refer to these local files, not to
separately installed skills. Resolve relative links from the document being read.
In poteto-mode, `playbooks/`, `scripts/`, and `references/` are relative to
`references/skills/poteto-mode/`. Use only the relevant references, not the whole bundle.
Only this SKILL.md is registered with Codex; internal WORKFLOW.md files are resources.

Keep the mode for the current task and its follow-ups. Leave it when the user opts
out or changes to an unrelated task. Do not edit global instructions to make it sticky.

For each child, supply this file's absolute path, the runtime adapter's absolute
path, the applicable workflow/prompt paths, the task scope, and verification criteria.
Only delegate when the host permits it. An unavailable delegate is an evidence gap,
not a completed review; perform feasible work directly and label the limitation.

See [NOTICE.md](NOTICE.md) for provenance, port changes, usage, and removal.
