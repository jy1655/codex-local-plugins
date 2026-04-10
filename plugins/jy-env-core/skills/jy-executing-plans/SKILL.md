---
name: jy-executing-plans
description: Use when a written implementation plan already exists and needs to be executed task by task in the current session.
---

# JY Executing Plans

## Overview

Execute an existing implementation plan step by step in the current session. The point is
not to dump code immediately, but to close each task with the right verification and
handoff discipline.

This skill is a `current session` executor. In this wave it `does not auto-spawn subagents`.

## When to Use

- "Execute this plan", "work from the plan", "follow the checklist"
- A written plan already exists and real implementation work remains
- The plan is approved and needs to be closed out in the current session

Do not use it when:

- There is no written plan yet (`jy-writing-plans`)
- The plan still has major decision gaps (`jy-plan-review`)
- The task is only routing or high-level advice

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm Default or Plan |
| 1. Read the plan | Identify tasks, file paths, and verification steps |
| 2. Execute the current step | Do not skip the order without cause |
| 3. Apply implementation discipline | Use `jy-test-driven` for code-change steps |
| 4. Block premature completion | Use `jy-verification-before-completion` before closing a task or batch |
| 5. Review milestones | Use `jy-review-work` before large handoffs |

## Input Contract

- a written plan or checkbox task list
- repo rules and current branch context
- per-task verification commands

Stop if the plan is still weak:

- if the decision gap is large, go to `jy-plan-review`
- if the task breakdown is missing, go to `jy-writing-plans`

## Execution Rules

- Follow the plan order by default
- Use `jy-test-driven` for code-change steps
- Use `jy-verification-before-completion` before any task, batch, or handoff completion claim
- Use `jy-review-work` before large milestones or final handoff
- If checkbox state and actual repo state disagree, do not overstate progress

## Progress Tracking

Track:

- current task number
- completed checkbox steps
- remaining blockers
- latest verification result

Do not rely on memory alone. Compare the plan artifact with the real working state.

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Read the written plan and execute the current task for real
- If the plan is too weak, say so and route back to `jy-writing-plans` or `jy-plan-review`

### If current collaboration mode is Plan

- Do not start real implementation or edits
- Route like this:
  - "This is an execution-oriented plan workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-executing-plans` again."
- Still leave a compact execution preview:
  - the first task to run
  - required verification commands
  - any visible plan gap

## Workflow

1. Check the current collaboration mode
2. Confirm the plan is a sufficient written artifact
3. Read the current task's file paths, verification steps, and completion signals
4. If it is a code task, start from RED with `jy-test-driven`
5. Before saying a task is done, create fresh evidence with `jy-verification-before-completion`
6. Before a large batch or handoff, run `jy-review-work`
7. Move to the next checkbox step

## Common Mistakes

- Ignoring the written order and jumping around the plan
- Acting like an automatic swarm when this is a `current session` executor
- Assuming the skill `does not auto-spawn subagents` but still making it behave that way
- Implementing code steps without `jy-test-driven`
- Claiming task completion without `jy-verification-before-completion`
- Ignoring plan gaps and implementing anyway
- Closing a large batch without a milestone review
