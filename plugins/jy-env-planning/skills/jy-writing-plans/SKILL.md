---
name: jy-writing-plans
description: Use when approved requirements or a reviewed plan need to become a detailed implementation plan another engineer can execute directly.
---

# JY Writing Plans

## Overview

Turn an approved brief, reviewed plan, or stable requirement set into a
`decision-complete` implementation plan that another implementer can execute directly.

Return the plan in conversation by default. Persist a repo-visible plan only when the user
explicitly requests a file or a concrete cross-session, cross-person, audit, or handoff boundary
requires durable state.

## When to Use

- "Write the implementation plan", "turn this into a task list", "make it executable for another engineer"
- The brief is approved but task-level breakdown is missing
- A reviewed plan needs exact file paths, verification commands, and acceptance criteria

Do not use it when:

- The problem definition is still unstable (`jy-framing`)
- Major decisions are still missing (`jy-plan-review`)
- A written plan already exists and only execution remains (`jy-executing-plans` when the delivery pack is installed)

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm Default or Plan |
| 1. Lock inputs | Gather the brief, reviewed plan, repo rules, and constraints |
| 2. Lock structure | Fix changed files, ownership, and verification flow |
| 3. Break into tasks | Create steps an implementer can follow directly |
| 4. Decide persistence | Keep it in conversation unless a durable boundary justifies a file |
| 5. Handoff | Point to direct execution or the installed delivery pack |

## Persistence Contract

- Conversation output is the default; do not create checkpoints, registries, or a planning
  hierarchy merely because they might be useful later
- Persist only on an explicit file request or a concrete boundary that native session state and
  context handling cannot reliably cross
- When persistence is justified, prefer the repository's existing plan location; if none exists,
  use `docs/superpowers/plans/YYYY-MM-DD-<topic>.md`
- The result must be `decision-complete`
- Every task must include exact file paths, commands, expected results, and acceptance criteria
- The plan must be trackable via checkbox steps
- Do not auto-create separate spec documents

## Required Content

Every plan should include at least:

- Goal
- Architecture summary
- Files to create or modify
- Ordered tasks with checkbox steps
- Verification commands and expected result
- `acceptance criteria`
- Next handoff: `jy-worktrees` or `jy-executing-plans` when the delivery pack is installed;
  otherwise direct execution

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

For a provisional plan, `UNKNOWN` or `NOT-VERIFIED` is allowed only when paired with the exact
decision or evidence needed. Do not call that plan decision-complete.

## Mode-Aware Behavior

### If current collaboration mode is Default

- Produce the best complete or provisional plan supported by current evidence.
- Mark material stale, unknown, or unverified inputs instead of stopping for a mode switch.
- Ask one plain-text focused question only when it prevents a safe decision-complete plan.
- Write a plan file only when the Persistence Contract justifies the side effect.
- Mention Plan Mode only as an optional richer interaction surface for substantial bounded choices.

### If current collaboration mode is Plan

- Turn missing decisions into explicit questions
- Produce an implementation plan at `<proposed_plan>` quality
- Do not pretend the file has already been written in Plan Mode

## Workflow

1. Check the current collaboration mode
2. Decide whether the inputs are stable enough
3. Read the repo structure and existing patterns, and mark stale or unverified inputs
4. Lock changed files and ownership boundaries first
5. Break the work into checkbox tasks
6. Attach verification commands and expected results to each task
7. End with acceptance criteria
8. Decide whether a durable file is justified; otherwise keep the plan in conversation
9. Leave the next step as direct execution, or `jy-worktrees` / `jy-executing-plans`
   when the delivery pack is installed

## Common Mistakes

- Writing a task plan before the brief is stable
- Calling a vague outline a `decision-complete` implementation plan
- Creating a repo-visible plan, checkpoint, or tracking hierarchy without a concrete persistence boundary
- Ignoring an existing repo plan location and inventing a parallel one
- Ending with a checklist but no acceptance criteria
- Leaving placeholders such as `TBD`
- Saying "add tests" without an actual verification command
- Auto-creating spec docs in this wave
- Treating collaboration mode as a prerequisite for producing a useful plan
