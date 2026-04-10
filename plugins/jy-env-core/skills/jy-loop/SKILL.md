---
name: jy-loop
description: Use when a task needs iterative execution until verified completion, not just a single-pass attempt.
---

# JY Loop

## Overview

Use a self-referential execution loop when work must continue until verified completion,
not merely until it "seems done." Completion is real only after verification passes.

This skill is execution-oriented and belongs in Default mode because it iterates through
real code changes, tests, and verification.

## When to Use

- "Keep going until it is done"
- A large task clearly requires multiple passes
- A single attempt will not be enough
- The user asks for continuous execution such as "keep iterating"

Do not use it when the task is simple enough for one pass or is purely research/analysis.

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm Default mode |
| 1. Define done | Make the completion criteria explicit |
| 2. Iterate | Make meaningful progress each pass |
| 3. Declare done | Only when the criteria appear satisfied |
| 4. Verify | Run tests, builds, or runtime checks |
| 5. Decide | Exit on verified success, continue on failure |

## Loop Protocol

### 1. Define completion criteria

Before starting, state the criteria explicitly:

```
Completion criteria:
- [ ] all tests pass
- [ ] build succeeds
- [ ] requested behavior works
```

If the user did not provide criteria, infer them from the task and say what you inferred.

### 2. Iteration rules

- Apply what was learned from the prior pass
- Do not repeat the same failed approach more than twice
- Summarize progress periodically
- If blocked, find the root cause before starting the next pass

### 3. Completion and verification

Once the work seems done:

1. Check the completion criteria one by one
2. Run executable verification such as tests, builds, or lint
3. Exit only if verification passes
4. Continue the loop if verification fails

`Looks done` is not done. Verified completion is done.

### 4. Exit conditions

- verification passes
- the user explicitly stops the work
- the same failure repeats three times and requires a direction change

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Iterate through code changes, testing, build checks, and verification for real

### If current collaboration mode is Plan

- Do not start the real execution loop
- Route like this:
  - "This is an iterative execution workflow. Leave Plan Mode with `Shift+Tab`, then run it again in Default mode."
- Still leave a compact loop strategy and draft completion criteria
- Do not pretend the loop has started inside Plan Mode

## Common Mistakes

- Acting as if Plan Mode can run the real loop
- Declaring completion before defining completion criteria
- Declaring completion without verification
- Repeating the same failed approach instead of changing strategy
- Losing context by failing to record progress between passes
- Drifting away from the original goal while iterating
