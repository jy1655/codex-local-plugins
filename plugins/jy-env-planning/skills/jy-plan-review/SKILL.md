---
name: jy-plan-review
description: Use when a plan exists and needs to be made decision-complete across product, architecture, UX, and delivery concerns.
---

# JY Plan Review

## Overview

Read an existing plan and close the gaps so an implementer does not need to make new
decisions during execution. Review scope, architecture, UX or operator impact, and
verification in one pass. Reconcile the plan with current repository evidence and keep the
review moving in the current collaboration mode.

## When to Use

- You want to lock the plan before implementation starts
- "Review this plan", "What decisions are missing?", "Can this be implemented as-is?"
- Multiple review angles need to be consolidated into one repo-native workflow

Do not use it when:

- The problem definition itself is still unstable
- The task is really a code diff review

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm Default or Plan |
| 1. Read the plan | Understand the draft and repo rules |
| 2. Find gaps | Identify missing decisions that would block implementation |
| 3. Write findings | Order them by severity |
| 4. Rewrite the plan | Produce a revised decision-complete plan |
| 5. Lock readiness | State acceptance criteria and start conditions |

## Expected Inputs

- a plan doc or planning draft in the user's message
- repo rules and existing structure
- explicit constraints such as timeline, compatibility, and non-functional requirements

## Expected Output

- findings ordered by priority
- missing decisions that must be added
- current, stale, unknown, or unverified assumptions when currency affects implementation
- a revised plan with those decisions filled in
- acceptance criteria before implementation begins
- the next handoff: `jy-writing-plans` or direct execution

## Review Dimensions

- scope and non-goals
- data flow and interfaces
- UX or operator touchpoints
- failure modes and rollback thinking
- test and verification coverage
- migration or compatibility impact

## Mode-Aware Behavior

### If current collaboration mode is Default

- Complete as much of the review and revision as current evidence supports.
- Ask one plain-text focused question only when a missing decision cannot be safely inferred and
  materially changes the plan.
- Mark stale or unverified assumptions instead of treating incomplete context as a reason to stop.
- Mention Plan Mode only as an optional richer interaction surface for substantial bounded choices.
- If the plan is approved but not yet taskized, explicitly hand off to `jy-writing-plans`

### If current collaboration mode is Plan

- Turn missing decisions into explicit questions
- Fill the plan until an implementer can pick it up directly
- End with a `<proposed_plan>` block
- If the result is not yet a taskized implementation plan, explicitly hand off to `jy-writing-plans`

## Workflow

1. Check the current collaboration mode
2. Read the plan, current repo context, and relevant source timestamps or revisions
3. Mark assumptions `CURRENT`, `STALE`, `UNKNOWN`, or `NOT-VERIFIED` when it matters
4. Identify the missing decisions that would block implementation
5. Order the findings by severity
6. Rewrite the plan with the missing decisions filled in
7. State implementation entry conditions and verification criteria
8. If the plan is still not taskized, hand off to `jy-writing-plans`

## Boundaries

- Do not write code
- Do not depend on hidden runtimes, review logs, or telemetry
- The output must be a plan another implementer can continue from directly

## Common Mistakes

- Assuming the skill can enable Plan Mode automatically
- Stopping at a mode-switch instruction when the review can continue with available evidence
- Evaluating the idea without actually locking implementation decisions
- Looking only at architecture and missing UX, migration, or verification criteria
- Listing findings without rewriting the plan
- Forgetting to say when `jy-writing-plans` is still required
- Ending in a state where the implementer still has to ask basic plan questions
