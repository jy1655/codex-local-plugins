---
name: jy-slop-remover
description: Use when reviewing a file for AI-generated code smells like obvious comments, over-defensive code, or deep nesting.
---

# JY Slop Remover

## Overview

Detect and remove AI-generated code smells at the single-file level while preserving
behavior. If the change is risky, skip it.

Input is exactly one file. If multiple files need cleanup, run this skill once per file.

This skill is execution-oriented because it edits real files and therefore belongs in
Default mode.

## When to Use

- Cleaning AI-generated code
- A review flags obviously AI-shaped patterns
- The user asks for slop removal, cleanup, or AI-smell cleanup

## Quick Reference

| Detect | Remove | Keep |
|--------|--------|------|
| obvious comments | `x += 1  # increment x` | WHY comments and issue links |
| over-defensive code | null checks for impossible values | system-boundary validation |
| deep nesting | 3+ levels of avoidable conditionals | domain-required branching |
| dead code | commented-out code, `removed` leftovers | intentional feature-flagged code |
| over-abstraction | one-off helper functions | abstractions with clear reuse |
| backward-compat leftovers | `_old = new` aliases with no users | aliases with real external dependents |

## Detection Rules

### 1. Obvious comments

Remove:

- comments that simply restate the code
- obvious docstrings on trivial methods
- section dividers with no information value
- vague TODOs with no concrete plan

Keep:

- business-logic WHY comments
- regex explanations
- comments that match the existing project style

### 2. Over-defensive code

Remove:

- null checks for values that cannot be null
- impossible catch-all exception handlers
- `isinstance()` checks that static typing already guarantees
- default empty values for required parameters

Keep:

- I/O error handling
- nullable database field checks
- assertions in tests

### 3. Deep nesting

Prefer early returns and guard clauses when they preserve the behavior.

## Process

1. Read the entire file and list slop candidates with line numbers
2. Evaluate each candidate:
   - does behavior change?
   - could tests break?
   - is the code needed in context?
   - does readability actually improve?
3. If any answer is risky, skip the change
4. Apply one logical cleanup at a time
5. Report what was removed and what was skipped

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Read the file, identify slop, and edit it for real

### If current collaboration mode is Plan

- Do not edit the file
- Route like this:
  - "This is a file-editing workflow. Leave Plan Mode with `Shift+Tab`, then run it again in Default mode."
- Still leave a compact preview of detected slop and the planned removals
- Do not pretend the file is being edited in Plan Mode

## Iron Rule

If it is doubtful, do not change it. A false negative is better than broken code.

## Common Mistakes

- Trying to process multiple files in one call
- Deleting WHY comments as if they were obvious comments
- Removing system-boundary validation as if it were over-defensive code
- Ignoring project conventions in favor of a generic cleanup style
- Making one large risky edit instead of several logical changes
