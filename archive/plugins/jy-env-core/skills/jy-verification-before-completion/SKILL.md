---
name: jy-verification-before-completion
description: Use when about to claim work is complete, fixed, or passing and you need fresh verification evidence first.
---

# JY Verification Before Completion

## Overview

Do not make a completion claim, fix claim, or passing claim without fresh verification
evidence. Without evidence, the status is unverified, not successful.

This skill is execution-oriented. In Default mode it runs the relevant verification
command. In Plan Mode it only leaves a checklist and required commands.

## When to Use

- Right before saying "done", "fixed", "passes", or "ready"
- Right before a commit, push, handoff, or PR summary
- When another agent or tool reported success
- When only part of the test surface ran but an overall status is needed

## Quick Reference

| Claim | Required Evidence | Not Enough |
|-------|-------------------|------------|
| Tests pass | fresh test command output | memory of an earlier run |
| Bug is fixed | rerun of the original symptom | the fact that code changed |
| Build is good | fresh build output | lint output only |
| Work is complete | requirement check plus verification result | "it should work" |

## Verification Gate

1. Identify the exact completion claim
2. Select the most direct command that proves it
3. Run the command fresh
4. Read the exit code, failures, warnings, and meaningful output
5. Report the status with evidence

If the command was not run, explicitly say `not run` or unverified instead of implying success.

## Reporting Rules

- If verification passed, say which command ran and what passed
- If verification failed, report the real state directly
- If verification did not run, do not make a completion claim
- Another agent's success report is input, not evidence

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Run the needed verification commands and report the result with fresh evidence

### If current collaboration mode is Plan

- Do not run tests, builds, or live verification
- Route like this:
  - "This is an execution-oriented verification workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-verification-before-completion` again."
- Still leave a checklist showing which command proves which completion claim
- Do not pretend fresh verification evidence exists in Plan Mode

## Common Mistakes

- Treating old test output as fresh evidence
- Running only a subset of tests and claiming the full surface passes
- Trusting a sub-agent report as if it were evidence
- Claiming success from lint output without a build or run
- Hinting at success with "should", "probably", or "looks good" when no evidence exists
- Failing to say `not run` when verification did not actually happen
