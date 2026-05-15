---
name: jy-change-guardrails
description: Use when implementing or reviewing a non-trivial code change that risks hidden assumptions, overengineering, or unrelated edits.
---

# JY Change Guardrails

## Overview

Apply lightweight execution guardrails before and during a non-trivial code change.
Surface risky assumptions, choose the smallest valid change, keep edits inside a declared
boundary, and tie the work to direct verification.

This skill is execution-oriented. In Default mode it can clarify, implement, and verify.
In Plan Mode it only leaves the guarded execution approach.

## When to Use

- A coding request has multiple plausible interpretations
- The change risks overengineering or speculative abstraction
- The work must stay tightly scoped with no drive-by cleanup
- A review or implementation request is clear enough to proceed but still needs guardrails

Do not use it when:

- The task is trivial and unambiguous
- The task is pure planning and belongs in `jy-autoplan` or `jy-framing`
- The main job is bug investigation and belongs in `jy-debugging`
- The work already follows a written implementation plan and belongs in `jy-executing-plans`
- The main input is review feedback that belongs in `jy-receiving-review`

## Quick Reference

| Guardrail | Required Action | Failure Signal |
|-----------|-----------------|----------------|
| assumptions | separate explicit requirements from inferred ones | silent guessing |
| interpretations | name competing readings when they matter | choosing one without saying so |
| smallest valid change | prefer the simplest code that fits the request | one-off abstraction or speculative flexibility |
| edit boundary | declare what is in and out of scope | drive-by cleanup |
| verification | pick the most direct proving command | "should work" with no evidence |

## Guardrail Protocol

### 1. Surface assumptions

- List the requirements that are explicit in the request
- List inferred assumptions that affect behavior, data shape, or interfaces
- If an assumption is blocking and cannot be resolved from the codebase, ask before editing

### 2. Name competing interpretations

- If two or more reasonable interpretations exist, state them briefly
- Pick the safest interpretation only when the request or codebase clearly supports it
- Otherwise ask instead of guessing

### 3. Choose the smallest valid change

- Reuse the current project pattern before inventing a new abstraction
- Treat future-proofing, configurability, and fallback code as out of scope unless requested
- Use `jy-test-driven` when the change adds or changes behavior

### 4. Declare the edit boundary

- State which files, modules, or surfaces are in scope
- Do not refactor adjacent code, comments, or formatting unless your change makes them wrong
- If you notice unrelated issues, mention them without fixing them

### 5. Anchor verification

- Select the smallest command that proves the change
- For reproducible bugs, start with `jy-debugging`
- Before claiming success, finish with `jy-verification-before-completion`

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Apply the guardrails, implement the smallest justified change, and verify it for real

### If current collaboration mode is Plan

- Do not edit files or claim implementation progress
- Route like this:
  - "This is an execution-oriented guarded change workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-change-guardrails` again."
- Still leave the assumptions list, interpretations, edit boundary, and verification plan
- Do not pretend the guarded change is already happening in Plan Mode

## Common Mistakes

- Silently guessing across ambiguous requirements
- Building a generic framework for a one-off change
- Expanding the diff into adjacent refactors or comment cleanup
- Adding speculative error handling for scenarios nobody asked about
- Claiming success without a direct proving command
- Acting as if Plan Mode can perform the real change
