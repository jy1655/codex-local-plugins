---
name: jy-ship
description: Use when the user wants to "ship", "deploy", "push to main", or create/update a PR/MR for the current branch and the work needs a verified base-branch, push, and docs-sync workflow.
---

# JY Ship

## Overview

Close a ready branch in this order:

`base safety -> change surface -> docs sync -> risk-proportionate review -> final fresh verification -> commit/push -> PR/MR`

Documentation is part of the candidate that gets verified and pushed, not a post-push
follow-up.

## When to Use

- The user asks to ship, push, deploy, or create/update a PR/MR.
- Implementation is complete enough for a release candidate.

Do not use it for unfinished debugging or planning-only requests.

## Quick Reference

| Step | Action | Stop condition |
|---|---|---|
| 1. Base | Detect current and target base branches | current branch is base |
| 2. Surface | Explain status, diff, and commits | scope is unclear |
| 3. Docs | Run the `jy-document-release` decision | doc drift remains |
| 4. Review | Review in proportion to risk | actionable failure |
| 5. Verify | Run fresh checks on the final candidate | any required check fails |
| 6. Publish | Commit, normal push, create/update PR/MR | no authority or remote |

## Base Branch And Scope Gate

- Detect the base from an existing PR/MR, repository metadata, or `origin/HEAD`.
- Stop if the current branch is the base branch.
- Inspect `git status`, the full diff, and relevant commit history.
- Preserve unrelated dirty changes and stage only the user-authorized ship surface.

## Documentation Sync

- Decide whether the diff affects README, AGENTS, skill docs, commands, or manual pressure
  scenarios before review and verification.
- Do not skip the `jy-document-release` decision when those contracts changed.
- Apply required docs first so the final checks cover the exact commit candidate.
- Do not invent `VERSION` or `CHANGELOG` unless those files already exist and are part of
  the repository's release process.

## Final Review And Verification Gate

- Use `jy-review-work` as the review gate for non-trivial implementation changes.
- Skip a full review for docs-only, config-only, or already-reviewed low-risk changes unless
  new evidence raises the risk.
- Do not use `jy-review-all` as a ship gate; it is a whole-project audit.
- Run `jy-verification-before-completion` once after docs and review fixes are settled.
- Reject test memory, a stale CI result, or an earlier agent report as evidence for the
  final candidate.
- Stop on unresolved review findings or failed required checks.

## Commit, Push, And PR/MR

- Commit only the explained change surface with an evidence-based message.
- Push with normal `git push` or `git push -u origin <branch>`.
- `Never force push`.
- Create or update the PR/MR with the available repository tool.
- Do not claim a PR/MR exists without a real URL.
- If publication is unavailable, provide the branch and exact manual action.

## Mode-Aware Behavior

### If current collaboration mode is Default

Perform the authorized ship workflow for real.

### If current collaboration mode is Plan

Do not commit, push, or create a PR/MR. Tell the user to leave Plan mode with `Shift+Tab`
and re-run `jy-ship` in Default mode; provide only a checklist preview.

## Output Template

Render labels in the user's language unless English was requested.

- `Base Branch:` detected target
- `Docs:` synced / not affected / blocked
- `Review Gate:` PASS / FAIL / proportionally skipped
- `Verification Gate:` fresh command and result
- `Push:` pushed / unchanged / blocked
- `PR/MR:` URL / updated / manual action

## Common Mistakes

- Pushing documentation changes after the supposedly final verification
- Running duplicate review and verification gates after every small step
- Using force push to bypass branch state
- Claiming publication without a real remote result
