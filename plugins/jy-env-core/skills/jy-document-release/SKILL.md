---
name: jy-document-release
description: Use when shipped changes in this repo need README, instructions, skill docs, or verification artifacts synced before handoff or release.
---

# JY Document Release

## Overview

Run the final documentation sync so behavior and docs stay aligned after a change ships.

The useful part of upstream `document-release` is post-ship documentation sync. The parts
to reject are hidden runtime state, telemetry, self-update behavior, and inventing docs the
repo does not actually use.

This skill defaults to a full consistency audit, not a one-file patch. Even if the diff
starts in one place, finish by checking whether the existing docs still describe the same
reality.

## When to Use

- "Update the docs", "docs sync", "post-ship docs"
- a skill, manifest, instruction, or install-surface change needs docs to match
- README and verification artifacts must reflect the shipped behavior before handoff

Do not use it when:

- the implementation is still unstable and docs should wait
- the task is only a trivial typo fix

## Quick Reference

| Step | Action |
|------|--------|
| 0. Mode check | mutate in Default, preview in Plan |
| 1. Inspect change surface | understand the diff and changed files |
| 2. Map doc surface | decide which docs are affected |
| 3. Apply the minimum sync | update only what truly changed |
| 4. Verify | run related tests and artifact checks |

## Repo-Local Doc Surface

Review these docs first in this repo:

- `README.md`
- `instructions/AGENTS.md`
- `plugins/jy-env-core/skills/<skill>/SKILL.md`
- `skill-tests/first-party/<skill>/`
- explicit plan or design notes under `docs/` when relevant

Do not invent new top-level docs:

- `CHANGELOG`
- `VERSION`
- `ARCHITECTURE.md`
- `CONTRIBUTING.md`

If the repo does not already contain them, `Do not invent` them just because upstream workflows often do.

## Full Consistency Audit

Doc drift usually happens when only the directly changed file gets updated. This skill uses
the current diff as a starting point, but it closes with a `full consistency audit` across
the existing doc surface.

Minimum audit set:

- `README.md`
- `instructions/AGENTS.md`
- `plugins/jy-env-core/skills/*/SKILL.md`
- `skill-tests/first-party/*/README.md`
- `skill-tests/first-party/*/pressure-scenarios.json`
- explicit design or plan docs under `docs/`

Key questions:

- are the same paths, commands, mode rules, and storage locations described consistently?
- is a rule present in one doc but missing in another?
- does this pass recover older drift that was previously skipped?

## Change-to-Docs Routing Matrix

### 1. Skill behavior change

Required review:

- `plugins/jy-env-core/skills/<skill>/SKILL.md`
- `skill-tests/first-party/<skill>/`
- `instructions/AGENTS.md` when that skill's routing is affected

Rules:

- wording-only edits can stay narrow, but behavior or trigger changes require the scenario pack too
- static verification rule changes require the matching tests

### 2. Install surface or environment rule change

Required review:

- `README.md`
- `instructions/AGENTS.md`
- `plugins/jy-env-core/skills/jy-env-sync-admin/SKILL.md` when relevant

Rules:

- if paths, commands, restart expectations, or storage locations change, sync both README and AGENTS

### 3. Routing or skill selection rule change

Required review:

- `instructions/AGENTS.md`
- the relevant skill docs
- related scenario packs when needed

Rules:

- if repo-level routing changes, do not let the skill docs and AGENTS diverge

### 4. Docs-only cleanup

Required review:

- only the docs actually being touched

Rules:

- keep docs-only changes narrow
- do not force verification artifacts or tests into scope unless the behavior contract changed

## Output Template

- Render headings and short status phrases in the user's language unless the user explicitly asks for English.
- Keep the template structure stable even when the labels are localized.

- `Change Surface:` changed behavior, skill, or install surface
- `Docs Updated:` the docs that were actually synced
- `Docs Skipped:` docs that were unaffected or do not exist
- `Verification:` tests or checks that were run

## Mode-Aware Behavior

### If current collaboration mode is Default

- This is the normal execution mode
- Edit docs and verification artifacts for real
- Run related tests when needed

### If current collaboration mode is Plan

- Do not edit docs for real
- Route like this:
  - "This is an execution-oriented docs sync workflow. Leave Plan Mode with `Shift+Tab`, then run `/jy-document-release` again."
- Still leave a preview:
  - which docs will change
  - which docs must stay untouched
  - which verification will run

## Workflow

1. Collect the change surface with `git diff --name-only` and targeted reads
2. Map the affected docs
3. Then scan the existing repo docs again as a full consistency audit
4. Fix only the statements that no longer match real behavior
5. If a user-facing path, command, storage location, or routing rule changed, update docs to match exactly
6. Review verification artifacts too:
   - scenario pack
   - compliance or bundle tests
7. Recheck the mandatory doc pairs:
   - `skill behavior change -> skill doc + scenario pack`
   - `install surface change -> README + AGENTS`
   - `routing change -> AGENTS + related skill doc`
8. Run tests so the docs and static verification agree

## Scope Rules

- Start from the change surface, but close with an existing-doc audit
- Do not broaden unrelated files just to polish tone
- If a skill changes, inspect its scenario pack and static tests too
- If the install surface changes, inspect both README and AGENTS
- If routing changes, inspect both AGENTS and the related skill docs
- Do not introduce release artifacts the repo does not already use

## Common Mistakes

- Auto-creating `CHANGELOG`, `VERSION`, `ARCHITECTURE.md`, or `CONTRIBUTING.md`
- Updating README and forgetting `instructions/AGENTS.md` or the scenario pack
- Touching only README or only AGENTS after an install-surface change
- Changing routing without syncing AGENTS and the related skill docs together
- Leaving known drift behind because it was not part of today's diff
- Writing generic prose without checking the actual implementation diff
- Failing to reflect the real maintainer-facing paths, commands, and storage locations
- Broadening a docs-only change unnecessarily
- Pretending Plan Mode already edited the files
