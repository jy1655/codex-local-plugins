---
name: jy-worktrees
description: Use when starting isolated feature work on a new branch or worktree before implementation begins.
---

# JY Worktrees

## Overview

Start feature work in an isolated worktree instead of the current workspace. The key is
not just creating a worktree, but first verifying which directory policy applies and
whether that directory is safe.

## When to Use

- "Split this into a new branch", "make a worktree", "I need an isolated workspace"
- Branch isolation is needed before implementation begins
- Parallel work must start without touching the current workspace

Do not use it when:

- You are already inside the correct feature branch or worktree
- The task is read-only

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | Confirm Default or Plan |
| 1. Choose location | `.worktrees/` first, then `worktrees/`, else create `.worktrees/` |
| 2. Verify safety | Confirm the chosen directory is `gitignored` |
| 3. Create worktree | Make the new branch and path |
| 4. Run baseline check | Run a light setup or test command if an obvious one exists |
| 5. Report result | Return the full path and baseline status |

## Directory Policy

- If `.worktrees/` already exists, use it
- If `.worktrees/` does not exist and `worktrees/` does, use `worktrees/`
- If neither exists, standardize on `.worktrees/`

The chosen directory must be `gitignored`.

Verification examples:

```bash
git check-ignore -q .worktrees
git check-ignore -q worktrees
```

If the chosen directory is not `gitignored`, fix the ignore rule before creating the worktree.

## Baseline Validation

- If `package.json` exists, inspect scripts for an obvious validation command
- If `pyproject.toml` or `requirements.txt` exists, look for an obvious Python baseline command
- Treat `Cargo.toml`, `go.mod`, and `Makefile` the same way
- If no obvious command exists, say so instead of guessing

Always report:

- whether a baseline command was found
- whether it was actually run
- if nothing obvious was found

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Enforce the directory policy, verify ignore rules, create the worktree, and run baseline validation for real

### If current collaboration mode is Plan

- Do not create the real worktree
- Route like this:
  - "This is an execution-oriented workspace workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-worktrees` again."
- Still leave a compact preview:
  - the directory that would be used
  - the required `git check-ignore` command
  - candidate baseline commands

## Workflow

1. Check the current collaboration mode
2. Inspect whether `.worktrees/` or `worktrees/` already exists
3. Verify the selected directory is `gitignored` with `git check-ignore`
4. Fix the ignore rule first if needed
5. Decide the branch name and worktree path
6. Create the worktree
7. Run an obvious baseline command if one exists, or explicitly report that none was found

## Common Mistakes

- Creating a worktree in an arbitrary directory
- Ignoring the `.worktrees/` and `worktrees/` precedence
- Failing to verify that the chosen directory is `gitignored`
- Assuming safety without `git check-ignore`
- Pretending tests passed when no obvious baseline command exists
- Acting as if Plan Mode already created the worktree
