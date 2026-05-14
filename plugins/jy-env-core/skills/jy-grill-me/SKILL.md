---
name: jy-grill-me
description: Use when the user wants to pressure-test a plan, design, or feature direction through a one-question-at-a-time decision interview before implementation.
---

# JY Grill Me

## Overview

Run a decision interview that makes weak plans stronger before implementation. Challenge
the user's plan one question at a time, answer codebase-checkable facts yourself, and keep
going until there is shared understanding of the decision, tradeoffs, and next step.

Do not modify code. This skill is advisory and planning-oriented.

## When to Use

- The user says "grill me", "pressure-test this", "stress-test this plan", or "ask me hard questions"
- A plan or feature direction exists but important assumptions may still be hidden
- The user wants an interactive challenge session instead of a rewritten plan
- The next useful step is decision clarity, not implementation

Do not use it when:

- the user wants a normal implementation review with findings ordered by severity
- the request is only vague idea shaping with no plan to challenge
- the answer can be completed by direct codebase exploration alone
- implementation should begin now

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm Default or Plan behavior |
| 1. State understanding | Summarize the current plan in one or two sentences |
| 2. Explore facts | Use the codebase for answerable questions before asking the user |
| 3. Ask one question | Ask exactly one focused decision question |
| 4. Recommend | Include a recommended answer when the evidence supports one |
| 5. Continue or close | Repeat until shared understanding exists, then hand off |

## Interview Contract

Each turn should contain:

- current understanding of the plan
- the single next question
- why that question matters
- recommended answer or default path, when there is enough evidence
- what would change depending on the answer

Ask exactly one question at a time. If you need five things, pick the highest-leverage
question first and wait.

## Codebase Grounding

Do not ask the user to answer facts that the repo can answer.

Before asking about existing structure, search the codebase directly. If the search spans
multiple modules or the path is unclear, use `jy-codebase-explore` first, then ask the
next decision question based on what was found.

Examples of questions to answer yourself first:

- where the existing implementation lives
- whether there is already a related abstraction
- what tests or docs define the current behavior
- whether the proposed plan conflicts with repo rules

## Mode-Aware Behavior

### If current collaboration mode is Default

- Run the first pass directly when one or two questions are enough
- If the user wants an extended back-and-forth interview, say:
  - "This belongs in Plan Mode. Press `Shift+Tab`, switch to Plan Mode, then run `/jy-grill-me` again."
- Still leave a useful first question, why it matters, and a recommended answer if possible
- Do not rely on Plan-only question flows while staying in Default mode

### If current collaboration mode is Plan

- Run the interview one question at a time
- Use `request_user_input` only when it genuinely improves a bounded choice
- After each answer, update the shared understanding before asking the next question
- Stop when the remaining uncertainty belongs in `jy-plan-review`, `jy-writing-plans`, or direct execution

## Closing Criteria

End the interview when all are true:

- the goal and non-goals are explicit
- the highest-risk assumptions have been challenged
- the recommended answer is clear or the tradeoff is deliberately accepted
- the user and agent share the same implementation entry criteria

Then state the next handoff:

- `jy-framing` if the problem is still not clear
- `jy-plan-review` if a plan exists but needs decision-complete review
- `jy-writing-plans` if the decisions are approved but not taskized
- direct execution only if the plan is already implementer-ready

## Boundaries

- Do not modify code
- Do not batch multiple unrelated questions
- Do not ask questions before checking facts the codebase can answer
- Do not turn the session into a generic brainstorm
- Do not approve the plan just because it sounds plausible

## Common Mistakes

- asking a long questionnaire instead of one question
- skipping the recommended answer when evidence supports one
- asking the user to describe code that can be inspected
- rewriting the whole plan instead of running the interview
- staying in Default mode for a long interactive loop without mentioning Shift+Tab
- ending without shared understanding or a clear handoff
