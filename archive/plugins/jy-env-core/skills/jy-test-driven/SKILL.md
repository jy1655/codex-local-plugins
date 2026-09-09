---
name: jy-test-driven
description: Use when starting a feature, bugfix, or behavior change and you need a failing test first before implementation.
---

# JY Test-Driven

## Overview

Start feature work and bug fixes with the failing test first. If you have not seen the
test fail first, you still do not know what the test protects.

This skill is execution-oriented. In Default mode it performs test writing, RED, minimal
implementation, GREEN, and REFACTOR. In Plan Mode it only leaves the test strategy.

## When to Use

- new feature implementation
- bug fixes
- refactors with behavior changes
- tasks where test design clarifies the requirement

Do not use it when:

- the change is documentation-only
- the work is pure planning
- the edit changes metadata or comments only

## Quick Reference

| Phase | Required Action | Check |
|-------|-----------------|-------|
| RED | write the smallest failing test first | does it fail for the expected reason? |
| GREEN | add the minimum implementation | do the new test and directly related tests pass? |
| REFACTOR | clean structure only | is behavior unchanged? |
| Repeat | restart from RED for the next behavior | one behavior at a time |

## Red-Green-Refactor

### 1. RED

- Choose the smallest user-visible behavior
- Add a test that exposes only that behavior
- Name the test after the behavior
- Run it and confirm it fails for the expected reason

### 2. GREEN

- Add only the minimum implementation needed to pass the new failing test
- Do not expand the design for future requirements
- Rerun the new test and the directly related tests

### 3. REFACTOR

- Remove duplication, improve naming, and make small structural cleanups
- Do not add new behavior during REFACTOR
- Rerun the tests after the cleanup

## Guardrails

- Do not write production code before the test
- Adding tests after implementation is retrofitted testing, not TDD
- Even if the user pressures you to "test later," find the smallest failing test first
- If the test already passes, you have not yet protected the new behavior; narrow the test or
  change the input until it really fails

## If Code Already Exists

- Do not pretend already-written production code was TDD
- If possible, stop and restart from failing test first based on the desired behavior
- If a restart is impractical, say clearly that this is no longer TDD and that the work is
  now a follow-up testing pass

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Write tests, confirm RED, implement, confirm GREEN, and REFACTOR for real

### If current collaboration mode is Plan

- Do not start real test writing or production code changes
- Route like this:
  - "This is an execution-oriented TDD workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-test-driven` again."
- Still leave a compact candidate for the smallest failing test first, the expected
  verification command, and the likely implementation order
- Do not pretend TDD has already started in Plan Mode

## Common Mistakes

- Writing production code before the test
- Implementing before observing the RED failure
- Packing multiple behaviors into one test
- Verifying only mocks instead of real behavior
- Adding tests after implementation and calling it TDD
- Stopping after GREEN without REFACTOR
- Talking as if real implementation is happening while still in Plan Mode
