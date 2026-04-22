---
name: jy-waterfall
description: Use when a project task needs a durable waterfall-style project record across orders, plans, execution reports, feedback, and troubleshooting notes.
---

# JY Waterfall

## Overview

Create and maintain a repo-visible project record for work that is too large to rely on
chat memory alone. This skill is for tasks expected to take 2-3 hours or more, or any task
that needs a durable order, plan, execution report, review trail, or troubleshooting log.

The useful pattern is a lightweight waterfall ledger:

- decide whether the work is large enough to track
- choose a public or private record surface before writing details
- create timestamped project notes with `YYYYMMDDTHHMM`
- connect local records to plans, execution, verification, and review
- optionally connect GitHub issues, milestones, and branches only after explicit approval

This skill coordinates existing skills. It does not replace `jy-writing-plans`,
`jy-executing-plans`, `jy-verification-before-completion`, `jy-review-work`, or `jy-ship`.

## When to Use

- work is expected to last 2-3 hours or more
- a task spans multiple sessions, branches, issues, or review passes
- the user asks for `mydocs/`, project records, task orders, work reports, or a waterfall log
- decisions, verification results, and feedback need to remain readable after the chat ends
- GitHub issue, milestone, or branch linkage is useful but should be approval-gated

Do not use it when:

- a one-line `jy-checkpoint` handoff is enough
- the task is a tiny edit with no durable decision trail
- the user only wants an implementation plan (`jy-writing-plans`)
- the user only wants to execute an existing plan (`jy-executing-plans`)

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Mutate in Default, preview in Plan |
| 1. Size gate | Use this for 2-3 hours or larger work |
| 2. Security gate | Decide public, private repo, or gitignored record storage |
| 3. GitHub gate | Ask before issue, milestone, or branch creation |
| 4. Record | Create timestamped notes using `YYYYMMDDTHHMM` |
| 5. Route | Hand off plan, execution, verification, and review to existing skills |

## Record Surface

Default public record root:

```text
mydocs/
  orders/
  plans/
  working/
  feedback/
  tech/
  troubleshootings/
```

Default private local record root:

```text
.codex/waterfall/
  orders/
  plans/
  working/
  feedback/
  tech/
  troubleshootings/
```

Use `mydocs/` for committed project knowledge only when the contents are safe to commit.
Use `.codex/waterfall/` or another gitignored path when details include secrets, credentials,
private customer data, unpublished business context, internal URLs, or anything the user does
not want committed.

## Timestamp Contract

Every new record file must include local time down to minutes:

```text
YYYYMMDDTHHMM-<kind>-<slug>.md
```

Examples:

```text
mydocs/orders/20260422T1530-order-plugin-waterfall.md
mydocs/plans/20260422T1545-plan-plugin-waterfall.md
mydocs/working/20260422T1810-result-plugin-waterfall.md
```

Do not use date-only names for new waterfall records. If two records are created in the
same minute, add a short suffix such as `-a` or a task id.

## Security Gate

Before creating or updating `mydocs/`, ask whether records may include sensitive material.
Treat the answer as risky unless the user clearly says the records are public-safe.

If secrets or sensitive details may appear:

- check whether the repo is a private repo before recommending committed `mydocs/`
- use a gitignored path such as `.codex/waterfall/` for raw notes
- keep a sanitized public summary separate from private raw notes
- add or verify a `.gitignore` entry before writing private records
- do not paste API keys, tokens, credentials, private customer data, or internal URLs into
  committed notes

The skill must not treat a non-sensitive project as permanently safe. A single API key,
token, credential, or private URL inside `mydocs/` is enough to switch to private or
gitignored storage.

## GitHub Gate

Detecting `gh`, a GitHub remote, existing issues, or milestones is read-only context. It is
not approval.

Before making GitHub changes, ask the user which option they want:

- local records only
- link to an existing issue
- create a new issue
- link to an existing milestone
- create or assign a milestone
- create a branch

Until the user gives explicit approval, the operator:

- must not create GitHub issues
- must not create milestones
- must not create branches
- must not run `gh issue create`
- must not run `gh api` to create milestones
- must not run `git switch -c` or `git checkout -b` for this workflow

When approval is granted, show the intended target repository and operation before running
the command. If the target repo is ambiguous, stop and ask instead of guessing from `origin`.

## Workflow

1. Check the current collaboration mode.
2. Estimate whether the work is 2-3 hours or more, multi-session, review-heavy, or issue-linked.
3. If waterfall tracking is warranted, run the security gate before writing records.
4. Choose `mydocs/` for public-safe records or a gitignored private root for sensitive records.
5. Gather read-only repo context:
   - current branch
   - `git status --short`
   - remote names and URLs when GitHub linkage is relevant
   - existing project record roots
6. Ask for explicit approval before any GitHub issue, milestone, or branch mutation.
7. Create the first timestamped order note with:
   - goal
   - task id or GitHub issue link if approved
   - chosen record root
   - sensitivity decision
   - next skill handoff
8. Route implementation planning to `jy-writing-plans` when a decision-complete plan is missing.
9. Route execution to `jy-executing-plans` when a plan exists.
10. Route completion claims to `jy-verification-before-completion`.
11. Route review or handoff milestones to `jy-review-work` and final branch closure to `jy-ship`.

## Record Templates

### Order

```markdown
# Waterfall Order

- Timestamp:
- Task:
- Record root:
- Sensitivity decision:
- GitHub linkage:
- Expected duration:
- Next skill:

## Goal

## Scope

## Decisions Needed

## Handoff
```

### Execution Result

```markdown
# Waterfall Execution Result

- Timestamp:
- Task:
- Plan:
- Verification:
- Review:

## Completed

## Evidence

## Remaining Work

## Follow-up Records
```

## Mode-Aware Behavior

### If current collaboration mode is Default

- Create or update record files for real after the security gate
- Run only read-only GitHub discovery before explicit approval
- Mutate GitHub issues, milestones, or branches only after explicit approval
- If a private record root is chosen, verify it is gitignored before writing sensitive notes

### If current collaboration mode is Plan

- Do not write files or mutate GitHub
- Route like this:
  - "This is an execution-oriented waterfall record workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-waterfall` again."
- Still leave a compact preview:
  - proposed record root
  - proposed timestamped filenames
  - security decision still needed
  - GitHub linkage options that require approval

## Output Template

- Render headings and short status phrases in the user's language unless the user explicitly asks for English.
- Keep literal paths, commands, timestamps, and skill names exact.

- `Waterfall:` enabled, previewed, or skipped
- `Record Root:` chosen public or private path
- `Timestamp:` `YYYYMMDDTHHMM`
- `Security:` public-safe, private repo, or gitignored
- `GitHub:` local-only, linked, or pending explicit approval
- `Next:` next skill or command

## Common Mistakes

- Creating `mydocs/` before checking whether secrets may appear
- Treating private repo status as a reason to store raw API keys in committed notes
- Using date-only filenames instead of `YYYYMMDDTHHMM`
- Automatically creating GitHub issues because `gh` is installed
- Automatically creating milestones because a remote exists
- Automatically creating branches because the task has a clear name
- Guessing the GitHub target repo from an ambiguous remote
- Using waterfall records instead of `jy-writing-plans` for implementation detail
- Claiming the workflow is done without `jy-verification-before-completion`
