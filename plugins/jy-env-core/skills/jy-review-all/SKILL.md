---
name: jy-review-all
description: Use when the user wants a whole-project audit for architecture, module depth, testability, documentation gaps, and maintainability before choosing focused follow-up work.
---

# JY Review All

## Overview

Run a whole-project audit of an existing repository. The goal is to find evidence-backed
improvement candidates across architecture, module depth, testability, documentation gaps,
maintainability, and codebase navigation before choosing focused follow-up work.

Do not modify code. This skill produces a prioritized audit report, not an automatic
refactor.

## When to Use

- "Review this whole project", "audit this codebase", or "check the whole repo"
- The user wants architecture or maintainability risks across the existing project
- The user wants refactoring candidates before picking one focused task
- The request is broader than one completed diff or one review comment set

Do not use it when:

- the user wants review of a specific completed diff (`jy-review-work`)
- the user wants push, PR/MR, or release closeout (`jy-ship`)
- the user only needs to find where something is implemented (`jy-codebase-explore`)
- the user has already picked a concrete refactor to implement (`jy-change-guardrails`)

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Full audit in Default, preview in Plan |
| 1. Map surfaces | Read README, docs, tests, entrypoints, and top-level modules |
| 2. Sample flows | Trace representative user, data, and build/test paths |
| 3. Score health | Check architecture, module depth, testability, docs, and maintainability |
| 4. Ground findings | Attach file paths, line references, commands, or observed structure |
| 5. Prioritize | Return ranked candidates with risk, value, and next skill handoff |

## Audit Lenses

Use these lenses together instead of doing a generic code review:

- architecture boundaries and cross-module coupling
- module depth: whether interfaces hide useful complexity or merely forward calls
- testability and test locality
- documentation gaps around setup, architecture, and operational behavior
- maintainability risks such as large files, scattered concepts, or unclear ownership
- navigation: whether a new maintainer can find the important entrypoints quickly

## Evidence Rules

Every finding must cite evidence. Use at least one of:

- file path and line reference
- command output or test/build result
- observed module structure
- missing expected artifact, such as absent docs or tests

Do not report architecture folklore without repository evidence. If the repo is too large
for full coverage, say what was sampled and why.

## Output Shape

Return a compact audit report:

```markdown
## Whole-Project Audit

| Priority | Area | Finding | Evidence | Candidate | Next |
|----------|------|---------|----------|-----------|------|
| P1 | Architecture | ... | path:line | ... | jy-grill-me |

## Keep
- patterns that should not be disturbed

## Not Covered
- surfaces skipped and why
```

Recommended next handoffs:

- `jy-codebase-explore` for deeper tracing before judging a candidate
- `jy-grill-me` to pressure-test one candidate before planning
- `jy-plan-review` when a remediation plan exists and needs decision closure
- `jy-writing-plans` when the user approves a candidate and wants an execution plan
- `jy-change-guardrails` when implementing a focused refactor
- `jy-review-work` only after a concrete implementation diff exists

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal mode for a real whole-project audit
- Run read-only exploration, gather evidence, and produce the prioritized report
- Do not edit files, create branches, or start refactors

### If current collaboration mode is Plan

- Do not perform a long repository scan as if it already happened
- Route like this:
  - "This whole-project audit needs Default mode for real repository exploration. Leave Plan Mode with `Shift+Tab`, then run `/jy-review-all` again."
- Still leave a compact audit plan:
  - likely surfaces to inspect
  - expected commands
  - risk lenses
  - follow-up decision points

## Boundaries

- Do not modify code
- Do not create `CONTEXT.md`, ADRs, docs, tickets, branches, or refactor plans unless the user explicitly asks
- Do not treat `jy-review-all` as a ship gate; `jy-ship` owns push and PR/MR closeout
- Do not use `jy-review-all` for one diff; use `jy-review-work`
- Do not promise exhaustive coverage when only a sample was inspected

## Common Mistakes

- giving generic best practices with no evidence
- turning the audit into an automatic refactor
- reviewing only the current diff and calling it a whole-project audit
- creating docs or ADRs just because they are missing
- listing every nit instead of prioritized candidates
- missing good existing patterns that should be preserved
- acting as if Plan Mode completed the real repository scan
