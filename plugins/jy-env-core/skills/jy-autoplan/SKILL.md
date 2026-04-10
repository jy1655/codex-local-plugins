---
name: jy-autoplan
description: Use when the user wants the Codex planning pack to decide the next planning step automatically and return one consolidated result.
---

# JY Autoplan

## Overview

Act as the planning-pack orchestrator. Decide whether the current request belongs to brief
framing, plan review, taskized implementation planning, or written-plan execution, then
choose the right `jy-*` path automatically.

This skill can select the right planning route, but it cannot switch Codex into Plan Mode
by itself. If a mode change is needed, tell the user to use `Shift+Tab`.

## When to Use

- "autoplan", "run the whole planning flow", "pick the right planning step for me"
- The user did not explicitly separate framing, plan review, and implementation planning
- One consolidated planning result is needed

Do not use it when:

- The user already named a specific planning skill
- The request is already clearly an implementation-only request

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Detect Default or Plan |
| 1. Judge maturity | Decide idea / plan / task-plan / execution stage |
| 2. Pick route | Choose `jy-framing`, `jy-plan-review`, `jy-writing-plans`, or `jy-executing-plans` |
| 3. Consolidate result | Return one brief, review result, task-plan preview, or execution handoff |
| 4. Leave next step | Make the next action obvious |

## Routing Matrix

### 1. Idea-stage

Signals:

- "Is this worth building?", "Where should I start?", "Is this the right direction?"
- the target user, problem, or success criteria are still blurry
- the task needs problem definition before implementation planning

Route:

- `jy-framing`

Output:

- compact brief draft or a Plan Mode framing handoff

### 2. Plan-stage

Signals:

- a plan, proposal, outline, design doc, or TODO draft already exists
- "Fill in the missing decisions", "Can this be implemented as-is?", "Lock this before implementation"
- the bottleneck is decision completeness rather than task decomposition

Route:

- `jy-plan-review`

Output:

- compact review summary or a Plan Mode plan-review handoff

### 3. Task-plan-stage

Signals:

- an approved brief or reviewed plan exists, but implementer-ready task breakdown is missing
- "Write the implementation plan", "turn this into a task list", "make it executable"
- execution units are the bottleneck, not the high-level decisions

Route:

- `jy-writing-plans`

Output:

- compact task-plan preview or a Plan Mode writing-plans handoff

### 4. Execution-stage

Signals:

- a written plan already exists and real work should now follow it
- "Execute this plan", "work from the plan", "follow the checkbox list"
- the request is execution-ready because the plan artifact already exists

Route:

- `jy-executing-plans`

Output:

- compact execution handoff or the Default mode next step

### 5. Execution-ready

Signals:

- "Implement this", "fix this now", "change the code", "run the tests", "review my implementation"
- implementation is already done and an execution-oriented review or QA pass is needed
- planning is no longer the bottleneck

Route:

- do not force a planning-pack route
- send it to direct implementation or an execution skill such as `jy-review-work`

Output:

- `planning pack not applicable` plus the right next step

## Routing Rules

- If the user explicitly named `jy-framing`, `jy-plan-review`, `jy-writing-plans`, or `jy-executing-plans`, do not override it
- idea-stage -> `jy-framing`
- plan-stage -> `jy-plan-review`
- task-plan-stage -> `jy-writing-plans`
- execution-stage -> `jy-executing-plans`
- if idea and plan signals are mixed but the main uncertainty is problem definition, choose `jy-framing`
- if the plan was reviewed but is not implementer-ready, choose `jy-writing-plans`
- if a written plan already exists, do not send it back to earlier planning stages
- if the request is execution-ready, do not send it through the planning pack
- if the request is ambiguous between "lock decisions" and "execute now", prioritize the user's final verb

Examples:

- "review the plan" -> plan-stage
- "write the implementation plan" -> task-plan-stage
- "execute this plan" -> execution-stage
- "review my implementation" -> execution-ready

## Expected Output

- the maturity classification
- a one-line reason for that classification
- the selected skill route or `planning pack not applicable`
- one consolidated planning result
- exactly one next step

## Mode-Aware Behavior

### If current collaboration mode is Default

- Do not stop at classification alone
- If the request is idea-stage or plan-stage:
  - choose the route
  - then say:
    - "This belongs in Plan Mode. Press `Shift+Tab`, switch to Plan Mode, then run `/{skill-name}` again."
- Still leave the smallest useful result:
  - compact brief draft for idea-stage
  - compact review summary for plan-stage
- If the request is task-plan-stage:
  - route to Plan Mode for `/jy-writing-plans`
  - still leave a compact task breakdown draft
- If the request is execution-stage:
  - do not recommend Plan Mode
  - say that the written plan should be executed in Default mode with `/jy-executing-plans`
- If the request is execution-ready:
  - do not recommend Plan Mode
  - say that implementation or an execution skill should happen next
  - explicitly mark `planning pack not applicable`

### If current collaboration mode is Plan

- For idea-stage, continue with the `jy-framing` behavior
- For plan-stage, continue with the `jy-plan-review` behavior
- For task-plan-stage, continue with the `jy-writing-plans` behavior
- Use `<proposed_plan>` when the downstream skill would do so
- For execution-stage, route back to Default mode:
  - "This is an execution-oriented plan workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-executing-plans` again."
- For execution-ready, route back to Default mode:
  - "This is execution work, not planning. Leave Plan Mode with `Shift+Tab`, then run it again in Default mode."
- Always consolidate the result into one planning outcome

## Workflow

1. Check the current collaboration mode
2. Check whether the user already named a specific planning skill
3. Classify the request as `idea-stage / plan-stage / task-plan-stage / execution-stage / execution-ready`
4. Write a one-line reason
5. Choose the route or mark `planning pack not applicable`
6. Produce the mode-appropriate result
7. Consolidate it into one response
8. Leave one clear next step

## Boundaries

- Do not assume any external orchestration runtime
- Do not assume a third-party review pack
- Prefer a single-response result
- Do not force execution-ready work into a planning workflow

## Common Mistakes

- Confusing routing with mode switching
- Recommending a planning skill without handling the mode mismatch
- Telling the user only to switch to Plan Mode and giving no useful draft result
- Sending task-plan work to plan review or execution
- Sending a written plan back to brief or review stages
- Forcing execution-ready requests through the planning pack
- Overriding a planning skill the user explicitly named
- Giving planning advice without actually routing
- Sending idea-stage work straight to plan review
- Sending an existing plan back to problem definition
- Leaving no consolidated outcome
