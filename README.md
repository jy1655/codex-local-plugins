# Portable Codex Environment Sync

[![Language: English](https://img.shields.io/badge/Language-English-111827?style=for-the-badge)](./README.md)
[![Language: Korean](https://img.shields.io/badge/Language-Korean-0A66C2?style=for-the-badge)](./README.ko.md)

This repo defines a portable Codex working environment.

It is not trying to reproduce an entire machine. It only syncs the parts that make
Codex behave the same way everywhere:

- first-party local plugin bundles
- plugin marketplace entries
- generated global instruction artifacts
- first-party Codex skills authored directly inside the installed plugin bundle

The install surface is intentionally small:

- plugins are installed into `~/plugins`
- skill discovery links are installed into `~/.agents/skills/`
- marketplace is written to `~/.agents/plugins/marketplace.json`
- instructions are installed into `~/.codex/...`
- Codex runtime cache under `~/.codex/plugins/cache` is left alone

Local `apply` uses symlinks on macOS and Linux so an intentionally dirty development
checkout is reflected immediately. Windows keeps copy mode via platform override. GitHub
bootstrap installs always use copy snapshots, so later edits or pulls in the managed clone
cannot silently change an installed environment.

Repo-local working state that should not be committed can live under `.codex/`.
The first such path is `.codex/checkpoints/`, used by the first-party `jy-checkpoint`
skill for session handoff notes.

First-party skill authoring happens in `plugins/jy-env-core/skills/`. That directory is
the source of truth for both local development and the installed Codex skill surface.
The current first-party workflow pack covers planning, decision interviews, plan
authoring, isolated worktree setup, debugging, test-first implementation,
change-scope guardrails, plan execution, whole-project audits, review feedback handling,
waterfall-style project records, shipping, and verification disciplines.

## First-Party Skill Catalog

Skill command names stay short as `jy-*`. Role grouping lives here in the README so day-to-day
invocation stays compact while the intended use stays explicit.

### Planning

- `jy-autoplan` chooses the right planning path for the current request and routes to `jy-framing`, `jy-grill-me`, `jy-plan-review`, `jy-writing-plans`, or `jy-executing-plans` without making the user decide first.
- `jy-framing` turns a vague feature or product idea into a sharper problem brief, constraints list, and next planning step.
- `jy-grill-me` pressure-tests a plan or feature direction through a one-question-at-a-time decision interview before implementation.
- `jy-plan-review` takes an existing plan or outline and closes decision gaps before implementation starts.
- `jy-writing-plans` turns approved requirements into a decision-complete implementation plan saved under `docs/superpowers/plans/`.
- `jy-worktrees` starts isolated feature work in `.worktrees/` after verifying that the directory is safe to use.
- `jy-waterfall` creates approval-gated project records for work expected to last 2-3 hours or more, with timestamped orders, plans, results, feedback, and troubleshooting notes.

### Execution

- `jy-executing-plans` runs a written plan task-by-task in the current session, uses TDD inside behavior changes, and closes with proportional review plus one final verification.
- `jy-debugging` forces reproduction, hypothesis testing, and root-cause verification before patching a bug.
- `jy-change-guardrails` keeps non-trivial code changes honest by surfacing assumptions, forcing the smallest valid change, and blocking unrelated cleanup.
- `jy-test-driven` enforces a failing test first and keeps implementation inside a red-green-refactor loop.
- `jy-verification-before-completion` blocks success claims until fresh verification commands and results exist.
- `jy-review-work` runs a structured multi-angle review pass on completed implementation before handoff or merge.
- `jy-receiving-review` triages review feedback, verifies it against the actual codebase, and supports technical pushback when comments are wrong.
- `jy-slop-remover` cleans obvious AI-generated code smells without turning into broad stylistic refactoring.

### Audit

- `jy-review-all` audits an existing project across architecture, module depth, testability, documentation gaps, maintainability, and navigation before choosing focused follow-up work.

### Research

- `jy-codebase-explore` performs multi-angle repository exploration when the structure is unfamiliar or spread across modules.
- `jy-library-research` gathers evidence-backed answers about external libraries, packages, APIs, and usage patterns.
- `jy-consult` stays in advisory mode for architecture, reliability, performance, and repeated-failure decisions that need deeper judgment.

### Maintenance

- `jy-checkpoint` stores repo-local checkpoint notes under `.codex/checkpoints/` for pause, resume, and branch handoff workflows.
- `jy-document-release` synchronizes only the documentation and manual pressure scenarios affected by a change.
- `jy-ship` closes the final branch workflow with base-branch checks, pre-verification docs sync, proportional review, one final verification, push, and PR/MR creation.
- `jy-env-sync-admin` validates this environment repo and reapplies the repo-owned install surface into the home Codex environment.

### Authoring

- `jy-writing-skills` is the first-party skill authoring guide, with risk-scoped static checks, manual pressure scenarios, and deployment checks.

## Secret handling

Secret values should not be committed to this repo.

The current `jy-env-core` plugin bundle does not install MCP servers. Keep any future API
keys or account tokens in machine-local configuration outside this repo.

## First run

macOS / Linux:

```bash
./scripts/bootstrap.sh <git-url>
```

Windows PowerShell:

```powershell
.\scripts\bootstrap.ps1 -GitUrl <git-url>
```

Both bootstrap scripts clone once and install a stable copy snapshot.

## Local development

Inspect the environment defined by this repo:

```bash
python -m codex_env_sync.cli inspect --repo-root .
```

Apply the local checkout into your home directory:

```bash
python -m codex_env_sync.cli apply --repo-root .
```

On macOS and Linux, that creates symlinks for the repo-managed plugin bundle, skill
discovery surface, and instructions. A later `git pull` in the same checkout updates the
installed Codex surface immediately.

To install a detached copy from any existing checkout, use:

```bash
python -m codex_env_sync.cli apply --repo-root . --snapshot
```

## Layout

```text
codex-env.toml                 # Minimal manifest: plugins + instructions + platform overrides
codex_env_sync/                # Apply engine and CLI
plugins/                       # First-party plugin bundles that get installed into ~/plugins
plugins/jy-env-core/skills/    # First-party Codex skills, authoring source and install source
instructions/                  # Generated instruction artifacts
.codex/checkpoints/            # Repo-local ignored checkpoint notes created by jy-checkpoint
.agents/plugins/               # Repo-local marketplace metadata for local plugin discovery
.agents/skills/                # Home install target for Codex native skill discovery
scripts/bootstrap.sh           # First-run shell bootstrap for macOS/Linux
scripts/bootstrap.ps1          # First-run shell bootstrap for Windows
tests/                         # Unit + integration tests
skill-tests/                   # Manual first-party pressure scenarios; CI validates schema only
```

## Design boundaries

- Upstream open source or company skills are seed material only.
- Raw seed sources normally stay local and are not committed here.
- First-party Codex skills are authored directly in `plugins/jy-env-core/skills/`.
- This repo does not keep vendored upstream runtimes as part of the maintained execution surface.
- Repo-local checkpoint notes belong under `.codex/checkpoints/` and stay gitignored.
- What gets committed here is the first-party result after customization.
- Re-running apply should be fast and mostly quiet when nothing changed.

## Tests

Run locally:

```bash
python3 -m unittest discover -s tests -v
```

For first-party manual pressure inputs and their schema checks, see
`skill-tests/first-party/` and run:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```
