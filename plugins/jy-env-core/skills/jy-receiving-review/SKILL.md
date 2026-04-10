---
name: jy-receiving-review
description: Use when review feedback, PR comments, or requested fixes need verification against the codebase before code changes are made.
---

# JY Receiving Review

## Overview

Review comments are inputs to verify against the real codebase, not instructions to obey
blindly. The core principle is technical evaluation, not social performance.

In particular, ban `performative agreement`. Apply correct feedback after verification, and
respond to incorrect feedback with `technical pushback`.

## When to Use

- "Apply this review", "handle these PR comments", "check whether this feedback is right"
- A reviewer left multiple requested changes
- An external suggestion might conflict with the current implementation

Do not use it when:

- The task is really a new implementation request
- The fix list is already verified and only needs mechanical application

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm Default or Plan |
| 1. Triage | Classify feedback as clear / unclear / disputed |
| 2. Verify | Compare each item against the real codebase |
| 3. Clarify or push back | Ask about unclear items, challenge wrong items |
| 4. Implement | Apply only the verified items |
| 5. Verify again | Confirm the result with fresh evidence |

## Feedback Triage

- clear: the requested change and location are obvious
- unclear: the request is `unclear` or depends on other items
- disputed: the request conflicts with the current codebase, requirement, or compatibility rule

Do not implement unclear or disputed items immediately.

## Verification Rules

- Compare each item with the actual codebase
- Check whether the review comment is accurate, already resolved, or in conflict with other constraints
- If one item in a multi-item review is `unclear`, split it out and ask about it directly
- Never assume an external review comment is correct by default

## Response Rules

Forbidden:

- `performative agreement`
- unverified acceptance such as "You're right, I'll fix it immediately"
- implementing only the easy items while an `unclear` item still blocks the review set

Allowed:

- direct fixes after verification
- clarification requests
- `technical pushback` grounded in tests, code, and requirements

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Perform triage, codebase verification, clarification, edits, and final verification for real

### If current collaboration mode is Plan

- Do not make real code changes
- Route like this:
  - "This is an execution-oriented review-response workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-receiving-review` again."
- Still leave the triage result and the missing clarification list

## Workflow

1. Check the current collaboration mode
2. Classify the feedback as clear / unclear / disputed
3. Compare each item against the codebase
4. Turn each unclear item into a focused question and each disputed item into grounded technical pushback
5. Implement only the verified items
6. Close with fresh verification

## Common Mistakes

- Using `performative agreement` and accepting the review without verification
- Trusting the reviewer description without looking at the real codebase
- Implementing only part of the set while an `unclear` item is still unresolved
- Following wrong feedback without technical pushback
- Claiming "review feedback applied" without verification
- Acting as if Plan Mode already performed the edits
