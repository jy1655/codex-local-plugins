---
name: jy-checkpoint
description: Use when the user wants to save, list, or resume repo-local working-state checkpoints across sessions, context switches, or branch handoffs.
---

# JY Checkpoint

## Overview

Create repo-local checkpoint notes that make it easy to resume work in a later session or
from another branch.

Two rules matter most:

- checkpoints live in `.codex/checkpoints/`, not hidden home-directory state
- checkpoints are append-only Markdown files and must never silently overwrite an older note

## When to Use

- "Save this state", "let's continue later", "leave a checkpoint"
- "What was I working on?", "restore the last state", "resume"
- You want to preserve decisions and remaining work before switching branches or ending the session
- Another person needs a compact handoff they can resume immediately

Do not use it when:

- a one-line chat summary is enough
- an official long-lived document should be committed instead

## Quick Reference

| Action | Required Behavior | Default |
|--------|-------------------|---------|
| Save | store branch, modified files, decisions, and remaining work | new Markdown file |
| List | show recent checkpoints for the current branch | newest first |
| Resume | read a specific or latest checkpoint and summarize how to continue | latest checkpoint |

## Storage Contract

- location: `.codex/checkpoints/`
- commit policy: gitignored, repo-local only
- format: Markdown plus YAML frontmatter
- write policy: append-only
- filename: `YYYYMMDD-HHMMSS-title-slug.md`

Required frontmatter:

```yaml
status: in_progress
branch: feature/foo
timestamp: 2026-04-10T16:00:00+09:00
files_modified:
  - plugins/jy-env-core/skills/jy-checkpoint/SKILL.md
```

Required body sections:

- `Summary`
- `Decisions Made`
- `Remaining Work`
- `Notes`

## Output Template

- Render headings and short status phrases in the user's language unless the user explicitly asks for English.
- Keep the template structure stable even when the labels are localized.

### Save

- `Checkpoint:` created file path
- `Status:` current status
- `Branch:` recorded branch
- `Next:` first action to take when resuming

### List

- recent checkpoints for the current branch
- each entry's date, title, and status
- separate branch mismatch items when needed

### Resume

- `Checkpoint:` selected file
- `What You Were Doing:` one short paragraph
- `Remaining Work:` the immediate next work
- `Warnings:` branch mismatch or stale-state warnings

## Mode-Aware Behavior

### If current collaboration mode is Default

- `Save`, `List`, and `Resume` all run for real
- `Save` creates a new file under `.codex/checkpoints/`
- `List` and `Resume` read repo-local checkpoint state and produce a compact summary

### If current collaboration mode is Plan

- `List` and `Resume` can continue because they are read-only
- `Save` must not pretend to write the file
- Route like this:
  - "Checkpoint save needs Default mode. Leave Plan Mode with `Shift+Tab`, then run `/jy-checkpoint save` again."
- Still leave a compact checkpoint draft in the conversation

## Workflow

1. Classify the user's intent as `Save`, `List`, or `Resume`
2. Gather repo context:
   - `git branch --show-current`
   - `git status --short`
   - recent checkpoint list if needed
3. For `Save`, infer the title, status, and modified files from the current context
4. Create a new append-only Markdown file in `.codex/checkpoints/`
5. For `List`, show current-branch items first in newest-first order
6. For `Resume`, use the user-specified item or default to the latest relevant checkpoint
7. Warn on branch mismatch, but do not block resume
8. Keep the result focused on prior work, remaining work, and warnings

## Resume Matching Rules

- Explicit user selection wins:
  - partial filename
  - partial title
  - date
- If the user does not specify anything, prefer the latest checkpoint on the current branch
- If the current branch has no checkpoint, use the latest checkpoint overall and add a branch mismatch warning

## Boundaries

- Do not depend on `~/.codex/...` or any other hidden home-directory state
- Do not add telemetry, update checks, or session analytics
- Do not silently edit or overwrite existing checkpoints
- Do not block resume only because the branch differs
- Do not assume built-in session persistence is enough and skip checkpoint creation

## Common Mistakes

- Leaving only a chat summary and no durable checkpoint file
- Introducing hidden home-directory state instead of `.codex/checkpoints/`
- Overwriting an older checkpoint and breaking the time sequence
- Ignoring the current branch when auto-selecting a checkpoint to resume
- Missing the warning for a branch mismatch
- Pretending a file was written in Plan Mode
- Using a checkpoint as a substitute for a real committed document
