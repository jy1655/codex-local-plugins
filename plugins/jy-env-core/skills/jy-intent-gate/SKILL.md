---
name: jy-intent-gate
description: Use when a user request is ambiguous and needs intent classification before choosing an action strategy.
---

# JY Intent Gate

## Overview

Classify the real intent behind an ambiguous request, then route to the right strategy.
The key is not the literal wording, but what the user is actually trying to achieve.

This skill must also account for the current collaboration mode. It cannot switch modes by
itself, and it must not fake execution while still in Plan Mode.

## When to Use

- A request could mean multiple things
- The user says something vague like "do this"
- It is unclear whether the task is research, implementation, or debugging
- The request mixes multiple intents such as investigate + fix + verify

Do not use it when the intent is already obvious, such as "rename this function" or "run the tests."

## Quick Reference

| Intent Type | Signal | Strategy |
|-------------|--------|----------|
| Research | "How does this work?", "What is best?" | Read -> analyze -> explain. No edits |
| Implementation | "Build this", "add this" | plan -> implement -> verify |
| Investigation | "Why is it broken?", "what is causing this?" | collect symptoms -> hypotheses -> evidence |
| Fix | "Fix this", "resolve this error" | reproduce -> root cause -> minimal fix -> verify |
| Evaluation | "Is this okay?", "review this", "compare these" | set criteria -> analyze -> judge |
| Refactoring | "Clean this up", "refactor this" | preserve behavior -> change gradually -> verify |

## Mode-Aware Behavior

### If current collaboration mode is Default

- Classify intent first
- If the result is planning-heavy:
  - choose the right planning skill
  - route like this:
    - "This belongs in Plan Mode. Press `Shift+Tab`, switch modes, then run `/{skill-name}` again."
  - still leave the smallest useful brief or plan summary
- If the result is execution-heavy, continue in Default mode

### If current collaboration mode is Plan

- Continue in Plan Mode for planning-heavy intents
- If the classification is execution-heavy, call out the mode mismatch
  - for example: implementation, fix, or live review execution
- Route like this:
  - "This fits Default mode better than Plan Mode. Leave Plan Mode with `Shift+Tab`, then run it again."
- Do not promise file edits or test runs while still in Plan Mode

## Classification Process

### Step 1: Separate wording from intent

```
Literal request: exactly what the user said
Actual intent: what the user is trying to accomplish
```

Examples:

- "Explain this code" -> Research
- "Look at this code" -> Evaluation or Fix
- "Do this" plus a stack trace -> Fix

### Step 2: Split mixed intent

If one request contains multiple intents, separate them:

```
"Find why this API is slow and fix it"
-> Investigation -> Fix
-> First find the cause, then patch it
```

### Step 3: State the strategy

Explicitly say the classification and the chosen strategy.
If the classification is still uncertain, ask for confirmation.

### Step 4: Check mode compatibility

- planning strategy in Default mode -> route to Plan Mode
- execution strategy in Plan Mode -> route back to Default mode
- matching mode and strategy -> proceed

## Common Mistakes

- Assuming the skill can switch collaboration mode automatically
- Starting implementation, fix, or review execution while still in Plan Mode
- Forcing execution in Default mode when the task really needs planning
- Skipping classification and jumping straight to code
- Treating the literal wording as the real intent every time
- Modifying code for a research request
- Collapsing a mixed request into one intent and skipping the first necessary phase
- Adding classification overhead to a request whose intent is already clear
