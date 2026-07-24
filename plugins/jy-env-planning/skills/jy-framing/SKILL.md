---
name: jy-framing
description: Use when a user is still shaping a product or feature direction and needs a sharp problem brief before implementation planning.
---

# JY Framing

## Overview

Turn an idea-stage request into a short, execution-ready brief before anyone starts
planning implementation. Narrow the user, pain, scope, and success criteria first.

This skill must be mode-aware. It can recommend Plan Mode, but it cannot switch Codex
collaboration mode by itself.

## When to Use

- New product ideas, feature direction changes, or scope-shaping requests
- "Is this direction right?", "Is this worth building?", "How should I scope this?"
- The user, problem, or success criteria need to be defined before implementation planning

Do not use it when:

- The implementation plan is already decision-complete
- Only code changes remain

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm whether the session is Default or Plan |
| 1. Read context | Review the request and relevant repo docs |
| 2. Fix the problem | Clarify user, pain, and current workaround |
| 3. Narrow scope | Define the smallest useful wedge and non-goals |
| 4. Write the brief | Include success criteria and open questions |
| 5. Handoff | Point to `jy-plan-review`, `jy-writing-plans`, or execution |

## Expected Inputs

- the current user request
- relevant repo docs such as `README.md`, `instructions/AGENTS.md`, and existing plans
- explicit constraints, timeline, and target users if the user provided them

## Expected Output

A compact brief containing:

- target user
- concrete problem
- current workaround or status quo
- smallest useful wedge
- success criteria
- non-goals
- open questions
- recommended next step

## Mode-Aware Behavior

### If current collaboration mode is Default

- First decide whether back-and-forth planning is truly needed
- If it is, route like this:
  - "This belongs in Plan Mode. Press `Shift+Tab`, switch to Plan Mode, and run `/jy-framing` again."
- Do not stop there when a compact draft brief is still possible
- Do not rely on Plan-only flows such as `request_user_input` while staying in Default mode

### If current collaboration mode is Plan

- Narrow the remaining open questions for real
- Ask only when needed
- End with a brief plus an explicit next step: `jy-plan-review`, `jy-writing-plans`, or direct execution

## Workflow

1. Check the current collaboration mode
2. Read the request and relevant repo context
3. Turn the idea into user, pain, and constraint statements
4. Replace vague wording with measurable wording
5. Summarize the key decisions that must be agreed before implementation
6. Recommend the next step: `jy-plan-review`, `jy-writing-plans`, or execution

## Boundaries

- Do not write code
- Do not assume external research is required
- Do not depend on hidden sidecar state
- Describe outputs as a conversation result or a repo-visible plan artifact

## Common Mistakes

- Acting as if the skill can switch collaboration mode automatically
- Starting a Plan-only question flow while still in Default mode
- Choosing a solution before the user and problem are clear
- Expanding to a large system before narrowing scope
- Writing a nice idea summary with no success criteria
- Missing the handoff to `jy-writing-plans` when the brief is approved but implementer breakdown is still needed
- Ending without a clear next step
