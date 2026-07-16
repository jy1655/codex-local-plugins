---
name: jy-autoplan
description: Use when the user wants the Codex planning pack to decide the next planning step automatically and return one consolidated result.
---

# JY Autoplan

## Overview

Classify planning maturity once, select the matching first-party skill, and return one
useful result. This skill routes work; it cannot change collaboration mode by itself.

Do not use it when the user named a specific planning skill or the request is already
straightforward implementation work.

## Quick Reference

| Maturity | Route |
|---|---|
| Idea-stage | `jy-framing` |
| Decision-interview-stage | `jy-grill-me` |
| Plan-stage | `jy-plan-review` |
| Task-plan-stage | `jy-writing-plans` |
| Execution-stage | `jy-executing-plans` |
| Execution-ready | planning pack not applicable |

## Routing Matrix

### Idea-stage

The user, problem, outcome, or constraints are still unclear. Route to `jy-framing`.

### Decision-interview-stage

A direction exists and the user wants one-question-at-a-time pressure testing. Route to
`jy-grill-me`.

### Plan-stage

A proposal or plan exists, but important decisions are unresolved. Route to
`jy-plan-review`.

### Task-plan-stage

Requirements are approved, but an implementer-ready task breakdown is missing. Route to
`jy-writing-plans`.

### Execution-stage

A written plan exists and the user wants it executed. Route to `jy-executing-plans` in
Default mode.

### Execution-ready

The user wants direct implementation, debugging, or review. Return `planning pack not
applicable` and name the relevant execution path without forcing another planning pass.

## Routing Rules

- Respect a skill the user explicitly selected.
- Prefer the earliest unresolved planning dependency.
- Do not send a written plan back to framing.
- Do not send implementation-ready work into planning.
- If two stages seem plausible, use the user's final requested verb.

## Mode-Aware Behavior

### If current collaboration mode is Default

- For Idea-stage, Decision-interview-stage, Plan-stage, or Task-plan-stage, provide a
  compact useful draft and tell the user to press `Shift+Tab` before re-running the chosen
  planning skill.
- For Execution-stage, keep the user in Default mode and route to `jy-executing-plans`.
- For Execution-ready, mark the planning pack not applicable and proceed through the
  appropriate execution workflow.

### If current collaboration mode is Plan

- Continue with the selected planning skill for the first four stages.
- For Execution-stage or Execution-ready, tell the user to leave Plan mode with
  `Shift+Tab` and re-run the execution request in Default mode.

## Output

Return:

1. maturity classification;
2. one-sentence evidence;
3. selected route or `planning pack not applicable`;
4. one compact useful result;
5. one next action.

## Common Mistakes

- Treating routing as an automatic mode switch
- Returning only a classification
- Overriding the user's explicit skill choice
- Sending execution-ready work through another planning cycle
