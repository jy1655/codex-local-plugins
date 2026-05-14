---
name: jy-review-work
description: Use when implementation is complete and needs multi-angle review before merging or handing off.
---

# JY Review Work

## Overview

Run a multi-angle review workflow with five review lenses after implementation is complete.
The goal is to cover blind spots a single reviewer would miss. All five must pass for the
overall review to pass.

Do not auto-spawn subagents. Use local review plus real tool execution by default. Only use
subagents when the user explicitly asks for sub-agents, delegation, or parallel agent work.

This skill is execution-oriented. Actual review execution, testing, and QA normally belong
in Default mode, and the skill cannot switch Plan Mode by itself.

## When to Use

- Implementation is complete and approaching merge or handoff
- The user asks for review, verification, or QA
- The change is large enough to justify multi-angle review

Do not use it when the change is tiny, config-only, or docs-only.

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm Default or Plan |
| 1. Gather context | Diff, changed files, goal, constraints, execution commands |
| 2. Run 5 review lenses | Cover all five lenses before deciding |
| 3. Collect results | Record all lens results |
| 4. Decide | If any reviewer fails, the whole review fails |

## Five Review Lenses

| # | Lens | Focus | Mode |
|---|------|-------|------|
| 1 | Goal Verifier | original request and constraint coverage | read-only analysis |
| 2 | QA Executor | real execution and tests | tool use allowed |
| 3 | Code Reviewer | code quality and pattern consistency | read-only analysis |
| 4 | Security Auditor | OWASP, injection, secret exposure | read-only analysis |
| 5 | Context Miner | git history, related issues, missing context | tool use allowed |

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Gather context, cover the five review lenses, run real checks where needed, and aggregate the results

### If current collaboration mode is Plan

- Do not start the real execution review
- Route like this:
  - "This is an execution-oriented review workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-review-work` again."
- If the user only wants the review strategy, leave a compact checklist instead
- Do not pretend the five review lenses have already run in Plan Mode

## Phase 0: Context Gathering

Collect before review:

```bash
git diff --name-only HEAD~1
git diff HEAD~1
```

Also extract the original goal, constraints, and background from the conversation. If a key
point is unclear, ask one focused question.

If the session is in Plan Mode, stop here and provide only the preview.

## Phase 1: Review Execution

Cover all five review lenses before deciding. Run tool-based checks in parallel when the
commands are independent, but do not auto-spawn subagents.

If the user explicitly authorizes subagents or parallel agent work, delegated review lenses may
be used. Otherwise, perform the review locally and keep the same PASS/FAIL standard.

Each review lens should include:

- the original goal and constraints
- the list of changed files
- PASS/FAIL criteria for that lens

## Phase 2-3: Collection and Decision

Summarize the results in a table:

```markdown
| # | Lens | Verdict | Key Finding |
|---|------|---------|-------------|
| 1 | Goal Verifier | PASS/FAIL | ... |
| 2 | QA Executor | PASS/FAIL | ... |
| 3 | Code Reviewer | PASS/FAIL | ... |
| 4 | Security Auditor | PASS/FAIL | ... |
| 5 | Context Miner | PASS/FAIL | ... |
```

If any single reviewer fails, the overall result is FAIL. List the concrete follow-up fixes.

## Common Mistakes

- Acting as if Plan Mode can run the real review execution
- Starting the workflow without first routing out of Plan Mode
- Treating one code-review pass as enough when QA, security, goal, and context checks are still missing
- Failing to include enough file context for read-only lenses
- Overusing the workflow for tiny changes
- Treating "mostly passed" as success when one reviewer failed
- Skipping context gathering before review execution
- Auto-spawning subagents when the user did not explicitly ask for delegated agent work
