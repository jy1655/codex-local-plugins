---
name: jy-framing
description: Use when a user is still shaping a product or feature direction and needs a sharp problem brief before implementation planning.
---

# JY Framing

## Overview

Turn an idea-stage request into a short, execution-ready brief before anyone starts
planning implementation. Narrow the user, pain, scope, and success criteria first, using
the best available context in the current collaboration mode.

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
- evidence or freshness notes when they affect the brief
- recommended next step

## Mode-Aware Behavior

### If current collaboration mode is Default

- Produce the best compact brief supported by the available context.
- Ask one plain-text question only when the answer materially changes the smallest useful wedge.
- Mark unresolved material facts `UNKNOWN` or `NOT-VERIFIED`; do not treat them as blockers when
  a provisional brief is still useful.
- Mention Plan Mode only when its structured input would materially improve an extended interview.

### If current collaboration mode is Plan

- Narrow the remaining open questions for real
- Ask only when needed, using `request_user_input` when it improves a bounded choice
- End with a brief plus an explicit next step: `jy-plan-review`, `jy-writing-plans`, or direct execution

## Workflow

1. Check the current collaboration mode
2. Read the request and relevant repo context
3. Distinguish current evidence from stale, unknown, or unverified inputs when it matters
4. Turn the idea into user, pain, and constraint statements
5. Replace vague wording with measurable wording
6. Summarize the key decisions that must be agreed before implementation
7. Recommend the next step: `jy-plan-review`, `jy-writing-plans`, or execution

## Boundaries

- Do not write code
- Do not assume external research is required
- Do not depend on hidden sidecar state
- Describe outputs as a conversation result or a repo-visible plan artifact

## Common Mistakes

- Acting as if the skill can switch collaboration mode automatically
- Stopping at a mode-switch instruction instead of producing a useful brief
- Choosing a solution before the user and problem are clear
- Expanding to a large system before narrowing scope
- Writing a nice idea summary with no success criteria
- Missing the handoff to `jy-writing-plans` when the brief is approved but implementer breakdown is still needed
- Ending without a clear next step
