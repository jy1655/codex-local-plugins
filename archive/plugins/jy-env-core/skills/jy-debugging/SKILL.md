---
name: jy-debugging
description: Use when debugging a bug, failing test, or unexpected behavior and you need verified root-cause analysis before patching.
---

# JY Debugging

## Overview

Prioritize reproduce-and-verify over guess-and-patch. Fix the proven root cause, not just
the nearby symptom.

This skill is execution-oriented. In Default mode it can reproduce, inspect logs, run
tests, and apply the smallest verified fix. In Plan Mode it only leaves a debug strategy.

## When to Use

- A test is failing
- A runtime error or broken behavior is reproducible
- Multiple guess patches have already failed
- The user pressures you toward a shotgun fix such as "just add more null checks"
- A flaky-looking issue must be separated from a real product bug

## Quick Reference

| Step | Required Action | Forbidden Shortcut |
|------|-----------------|--------------------|
| Reproduce | make the failure happen again | patch before reproduce |
| Narrow scope | reduce when and where it breaks | shotgun edits everywhere |
| Hypothesis | list 1-3 plausible causes | unsupported certainty |
| Verify | prove or disprove each hypothesis | fixing multiple causes at once |
| Minimal fix | change only the verified cause | broad edits around the symptom |
| Verify again | rerun the failure and regressions | "probably fixed" |

## Debug Loop

### 1. Reproduce

- Capture the failing test, input, log, or environment first
- If no reproduction command exists, build the smallest one
- If it is not reproduced yet, say so directly

### 2. Narrow scope

- Reduce when it breaks, which input triggers it, and which module is involved
- Observe one new signal at a time through logs, output, or state
- Do not touch unrelated files

### 3. Write hypotheses

- Base each hypothesis on observed facts
- Each hypothesis should include what would disprove it
- Order them by likelihood, but do not present them as proven

### 4. Verify

- Define a command, log point, or test for each hypothesis
- Record whether the result supports or disproves it
- Do not patch until the root cause is verified

### 5. Apply the minimal fix

- Change only the verified cause
- Keep the fix as small as possible
- Treat shotgun tactics such as broad null checks, retries, and sleeps as forbidden by default

### 6. Close the loop

- Rerun the original reproduction
- Add a regression test when practical, or lock the symptom into an existing test
- Rerun related tests or builds to confirm nothing else broke

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Reproduce, inspect, test, apply the minimal fix, and re-verify for real

### If current collaboration mode is Plan

- Do not start real debugging execution or file edits
- Route like this:
  - "This is an execution-oriented debugging workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-debugging` again."
- Still leave a compact reproduction path, hypothesis list, and verification order
- Do not pretend a patch is already being applied in Plan Mode

## Common Mistakes

- Editing code before you reproduce the issue
- Spraying null checks or retries as a shotgun patch
- Adding logs without a hypothesis
- Mixing multiple fixes and verifications so the winning change is unclear
- Hand-waving the problem away as a flake without root-cause verification
- Stopping after the fix without a regression test or rerun
- Acting as if Plan Mode can do real debugging execution
