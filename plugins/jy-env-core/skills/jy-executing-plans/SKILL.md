---
name: jy-executing-plans
description: Use when a written implementation plan already exists and needs to be executed task by task in the current session.
---

# JY Executing Plans

## Overview

Execute an approved written plan in the current session. This workflow does not auto-spawn subagents.
It uses test-first discipline where behavior changes and closes the work with
one final fresh verification rather than repeating the same gate after every checkbox.

## When to Use

- The user asks to execute an existing plan or checklist.
- Tasks, file paths, and completion signals are already concrete.

Use `jy-plan-review` for unresolved decisions and `jy-writing-plans` when task decomposition
is missing.

## Quick Reference

| Step | Action |
|---|---|
| 1. Read | Reconcile the plan with the current repo state |
| 2. Execute | Follow task order and use `jy-test-driven` for behavior changes |
| 3. Review | Use risk-proportionate review at a meaningful handoff |
| 4. Verify | Run one final fresh verification before completion |

## Execution Rules

- Follow plan order unless repo evidence makes a dependency invalid.
- Keep checkbox state aligned with actual files and test results.
- Use `jy-test-driven` within each behavior-changing task.
- Do not re-run `jy-verification-before-completion` after every small edit; use targeted
  feedback during implementation, then one final fresh verification for the complete
  surface.
- Use `jy-review-work` as a risk-proportionate review for non-trivial batches or final
  handoff, not as a ritual for every task.
- Stop and report when the plan is contradicted by the repo or requires new authority.

## Mode-Aware Behavior

### If current collaboration mode is Default

Execute the plan for real and keep progress tied to repo evidence.

### If current collaboration mode is Plan

Do not edit files. Tell the user to leave Plan mode with `Shift+Tab` and re-run
`jy-executing-plans` in Default mode; include the first task and expected checks as a
preview.

## Workflow

1. Read the plan, repo rules, and current diff.
2. Reconcile already-completed or stale steps.
3. Execute remaining tasks in dependency order.
4. Use RED/GREEN/REFACTOR for behavior changes through `jy-test-driven`.
5. Run `jy-review-work` once when the batch risk warrants it.
6. Run final commands through `jy-verification-before-completion`.
7. Update the plan status and report evidence.

## Common Mistakes

- Re-planning an already decision-complete task
- Treating every checkbox as a full release gate
- Claiming progress from the plan instead of the working tree
- Spawning subagents without explicit permission
