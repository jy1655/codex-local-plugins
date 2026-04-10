---
name: jy-ship
description: Use when the user wants to "ship", "deploy", "push to main", or create/update a PR/MR for the current branch and the work needs a verified base-branch, push, and docs-sync workflow.
---

# JY Ship

## Overview

This is the repo-native workflow for taking the current branch through a safe push and
PR/MR closeout. The core rule is simple: do not skip
`base branch safety -> review -> fresh verification -> push -> PR/MR -> docs sync`.

This skill does not depend on gstack hidden runtime, telemetry, self-update flows, or
local sidecar state. It uses only the real git surface and first-party skills that exist
in this repo.

## When to Use

- "ship it", "push this branch", "make the PR", "prepare this for merge"
- Implementation is complete and the work needs to be pushed and closed out through a PR/MR
- Review, verification, and docs sync all need to happen before handoff

Do not use it when:

- Implementation or debugging is still incomplete
- The user only wants planning, not actual git work
- The task is only documentation sync (`jy-document-release`)

## Quick Reference

| Step | Action | Stop Condition |
|------|--------|----------------|
| 0. Mode check | Execute in Default, preview only in Plan | If in Plan Mode, route with `Shift+Tab` |
| 1. Detect base branch | Use remote and CLI metadata to find the target branch | Stop if the current branch is the base branch |
| 2. Gather ship surface | Check `git status`, diff, and commit log | Stop if the change surface cannot be explained |
| 3. Review + verify | Use `jy-review-work` and `jy-verification-before-completion` for fresh gates | Stop on review FAIL or verification FAIL |
| 4. Commit + push | Commit the required changes and use normal `git push` | `Never force push` |
| 5. PR/MR | Create or update the PR/MR with `gh`/`glab` when available | Do not claim creation without a URL |
| 6. Docs sync | Use `jy-document-release` when docs are affected | Do not leave docs drift unresolved |

## Base Branch Gate

- Find the current branch and the base branch first
- Detect the base branch in this order:
  - GitHub: `gh pr view` or `gh repo view`
  - GitLab: `glab mr view` or the project default branch lookup
  - Common fallback: `origin/HEAD`
- If the current branch is the base branch, abort the ship workflow
- Even if the user says "ship directly from main", do not do it without a feature branch

## Review And Verification Gate

- Multi-file implementation should close a review gate through `jy-review-work` first
- Completion claims, passing tests, and ship readiness must be backed by fresh verification
  evidence using `jy-verification-before-completion`
- Do not rely on earlier test memory, an `old CI run`, or an agent success report to justify
  push or PR/MR creation
- If review or verification fails, stop the workflow and report that state directly

## Release File Rules

- Only handle release bookkeeping files such as `VERSION`, `CHANGELOG`, or `TODOS.md` if
  they already exist in the repo
- Do not invent `VERSION` or `CHANGELOG` files that the repo does not have
- In repos like this one, a shipping summary plus verification results and PR/MR body is enough

## Push And PR/MR Rules

- If the worktree is dirty, stage and commit only the current ship surface
- Keep the commit message within what can be safely inferred from the diff and user goal
- If you cannot responsibly name the change, ask the user for a commit summary instead of
  inventing one
- Push with normal `git push` or `git push -u origin <branch>`
- `Never force push`
- If `gh` or `glab` exists, update an existing PR/MR or create a new one
- If no CLI exists, leave the branch name, remote, compare URL, or manual PR next step
- If there is no URL, do not claim that the PR was created

## Documentation Sync

- If the shipped changes touch README, instructions, skill docs, or verification assets,
  run `jy-document-release` as the follow-up docs path
- Do not skip the `jy-document-release` decision when the diff clearly affects docs
- If docs state is still unclear, do not report ship complete; leave `Docs: blocked`
- If docs sync creates a new commit, push the same branch again and update the PR/MR body
- If docs changes are not needed, state that explicitly and end there

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode for the skill
- Perform base branch detection, fresh verification, commit, push, PR/MR creation, and docs sync for real

### If current collaboration mode is Plan

- Do not perform real git writes, pushes, or PR/MR creation
- Route like this:
  - "This is an execution-oriented ship workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-ship` again."
- Still leave a compact ship checklist preview:
  - how to confirm the base branch
  - which review and verification commands are required
  - which stop conditions block PR/MR creation
- Do not pretend that a push or PR/MR was already done while still in Plan Mode

## Output Template

- Render the headings and short status phrases in the user's language unless the user explicitly asks for English.
- Keep the structure stable even when the labels are localized.

- `Base Branch:` detected target branch
- `Review Gate:` PASS/FAIL with evidence
- `Verification Gate:` command run plus result
- `Push:` pushed / already up to date / blocked
- `PR/MR:` created / updated / manual action required
- `Docs:` synced / no changes needed / blocked

## Common Mistakes

- Pushing before confirming the base branch
- Claiming ship readiness without review or fresh verification
- Auto-creating `VERSION` or `CHANGELOG` in a repo that does not use them
- Using force push to hide process problems
- Claiming PR/MR creation without a real URL
- Skipping `jy-document-release` when docs are affected
- Acting as if Plan Mode can perform the real ship workflow
