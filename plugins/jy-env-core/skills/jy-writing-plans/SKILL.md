---
name: jy-writing-plans
description: Use when approved requirements or a reviewed plan need to become a detailed implementation plan another engineer can execute directly.
---

# JY Writing Plans

## Overview

Turn an approved brief, reviewed plan, or stable requirement set into a
`decision-complete` implementation plan that another implementer can execute directly.

This wave stores repo-visible plans, not repo-visible spec docs. Write implementation plans
under `docs/superpowers/plans/` and do not auto-create separate spec documents.

## When to Use

- "Write the implementation plan", "turn this into a task list", "make it executable for another engineer"
- The brief is approved but task-level breakdown is missing
- A reviewed plan needs exact file paths, verification commands, and acceptance criteria

Do not use it when:

- The problem definition is still unstable (`jy-framing`)
- Major decisions are still missing (`jy-plan-review`)
- A written plan already exists and only execution remains (`jy-executing-plans`)

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm Default or Plan |
| 1. Lock inputs | Gather the brief, reviewed plan, repo rules, and constraints |
| 2. Lock structure | Fix changed files, ownership, and verification flow |
| 3. Break into tasks | Create steps an implementer can follow directly |
| 4. Document the plan | Save under `docs/superpowers/plans/` |
| 5. Handoff | Point to `jy-worktrees` or `jy-executing-plans` |

## Plan Document Contract

- Save plans under `docs/superpowers/plans/YYYY-MM-DD-<topic>.md`
- The result must be `decision-complete`
- Every task must include exact file paths, commands, expected results, and acceptance criteria
- The plan must be trackable via checkbox steps
- This wave does not create repo-visible spec docs

## Required Content

Every plan should include at least:

- Goal
- Architecture summary
- Files to create or modify
- Ordered tasks with checkbox steps
- Verification commands and expected result
- `acceptance criteria`
- Next handoff: `jy-worktrees` or `jy-executing-plans`

A good plan:

- locks the changed files and ownership early
- uses a clear execution order
- avoids vague verification
- leaves little interpretation burden for the implementer

## No Placeholders

These phrases mean the plan is not ready:

- `TBD`
- `TODO`
- "implement later"
- "write tests"
- "add appropriate error handling"
- "handle edge cases"
- "similar to previous task"

If you see them, do not close the plan. Replace them with actual file paths, steps,
commands, and expected outputs.

## Mode-Aware Behavior

### If current collaboration mode is Default

- Write a real plan doc only when the inputs are already stable enough for a one-pass result
- If the input is still moving, route like this:
  - "This should be locked in Plan Mode. Press `Shift+Tab`, switch to Plan Mode, then run `/jy-writing-plans` again."
- Even then, do not leave empty-handed:
  - a compact file map
  - a task skeleton
  - the remaining open questions

### If current collaboration mode is Plan

- Turn missing decisions into explicit questions
- Produce an implementation plan at `<proposed_plan>` quality
- Do not pretend the file has already been written in Plan Mode

## Workflow

1. Check the current collaboration mode
2. Decide whether the inputs are stable enough
3. Read the repo structure and existing patterns
4. Lock changed files and ownership boundaries first
5. Break the work into checkbox tasks
6. Attach verification commands and expected results to each task
7. End with acceptance criteria
8. Leave the next step as `jy-worktrees` or `jy-executing-plans`

## Common Mistakes

- Writing a task plan before the brief is stable
- Calling a vague outline a `decision-complete` implementation plan
- Saving the plan outside `docs/superpowers/plans/`
- Ending with a checklist but no acceptance criteria
- Leaving placeholders such as `TBD`
- Saying "add tests" without an actual verification command
- Auto-creating spec docs in this wave
