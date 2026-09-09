---
name: jy-document-release
description: Use when shipped changes in this repo need README, instructions, skill docs, or verification artifacts synced before handoff or release.
---

# JY Document Release

## Overview

Synchronize documentation that is materially affected by a change. Start from evidence in
the diff and stop at the affected documentation surface; this is not a standing invitation
to audit or rewrite every document.

## When to Use

- Install paths, commands, routing, or skill behavior changed.
- README, instructions, skill docs, or pressure scenarios no longer match reality.
- A ship workflow needs its documentation decision closed before final verification.

Skip this skill for a typo isolated to one already-known document.

## Quick Reference

| Step | Action |
|---|---|
| 1. Inspect | Read the diff and changed behavior |
| 2. Route | Map the change to existing docs |
| 3. Sync | Edit only affected statements and assets |
| 4. Verify | Run targeted static or behavioral checks |

## Existing Documentation Surface

- `README.md` and `README.ko.md`
- `instructions/AGENTS.md`
- `plugins/jy-env-*/skills/<skill>/SKILL.md`
- `skill-tests/first-party/<skill>/pressure-scenarios.json`
- an existing plan or design note under `docs/` when the change invalidates it

Do not invent `CHANGELOG`, `VERSION`, `ARCHITECTURE.md`, or `CONTRIBUTING.md` when the
repository does not already use them.

## Change-to-Docs Routing Matrix

- `skill behavior change -> skill doc + scenario pack`
- `install surface change -> README + AGENTS`
- `routing change -> AGENTS + related skill doc`
- wording-only doc change -> the touched document only
- stale plan/design claim -> update or remove that specific existing record

Pressure scenarios are manual evaluation inputs. Update them when a trigger, safety rule,
or expected behavior changes; do not claim they passed unless they were actually run.

## Risk-Scoped Consistency Check

Check only the directly affected documentation surface and its mandatory pair from the
matrix. Broaden the scan only when inspected evidence shows the same changed contract is
repeated elsewhere.

Examples:

- a command change warrants searching for that command;
- a renamed skill warrants searching for that skill name;
- a local prose correction does not warrant scanning all skills.

## Mode-Aware Behavior

### If current collaboration mode is Default

Edit the affected docs and run proportional checks.

### If current collaboration mode is Plan

Do not edit files. Explain that this is execution work, tell the user to leave Plan mode
with `Shift+Tab`, and preview the affected files and checks.

## Workflow

1. Inspect `git diff --name-only`, the relevant diff, and the real implementation.
2. Select the matching row in the routing matrix.
3. Update only existing documentation and required scenario assets.
4. Search for exact changed names, paths, or commands to catch evidenced duplicates.
5. Run the smallest checks that prove the synchronized contract.

## Output Template

Render labels in the user's language unless English was requested.

- `Change Surface:` behavior that changed
- `Docs Updated:` files synchronized
- `Docs Skipped:` relevant files intentionally unaffected
- `Verification:` commands and results, or not run

## Common Mistakes

- Inventing release files the repository does not use
- Updating README but missing the paired AGENTS rule
- Treating a manual scenario asset as an executed evaluation
- Expanding a narrow documentation fix into unrelated cleanup
