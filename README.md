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

The current manifest uses symlinks on macOS and Linux so a later `git pull` updates the
installed plugin bundle and global instructions without re-copying. Windows keeps copy mode
via platform override.

Repo-local working state that should not be committed can live under `.codex/`.
The first such path is `.codex/checkpoints/`, used by the first-party `jy-checkpoint`
skill for session handoff notes.

Authoring references that support local skill development can live in `references/`.
They are part of this repo for maintenance work, not part of the installed Codex surface.

First-party skill authoring happens in `plugins/jy-env-core/skills/`. That directory is
the source of truth for both local development and the installed Codex skill surface.
The current first-party workflow pack covers planning, plan authoring, isolated worktree
setup, debugging, test-first implementation, plan execution, review feedback handling,
shipping, and verification disciplines.

## First-Party Skill Catalog

Skill command names stay short as `jy-*`. Role grouping lives here in the README so day-to-day
invocation stays compact while the intended use stays explicit.

### Planning

- `jy-autoplan` chooses the right planning path for the current request and routes to `jy-framing`, `jy-plan-review`, `jy-writing-plans`, or `jy-executing-plans` without making the user decide first.
- `jy-framing` turns a vague feature or product idea into a sharper problem brief, constraints list, and next planning step.
- `jy-plan-review` takes an existing plan or outline and closes decision gaps before implementation starts.
- `jy-writing-plans` turns approved requirements into a decision-complete implementation plan saved under `docs/superpowers/plans/`.
- `jy-worktrees` starts isolated feature work in `.worktrees/` after verifying that the directory is safe to use.

### Execution

- `jy-executing-plans` runs a written plan task-by-task in the current session and keeps execution tied to TDD, verification, and review gates.
- `jy-debugging` forces reproduction, hypothesis testing, and root-cause verification before patching a bug.
- `jy-test-driven` enforces a failing test first and keeps implementation inside a red-green-refactor loop.
- `jy-verification-before-completion` blocks success claims until fresh verification commands and results exist.
- `jy-review-work` runs a structured multi-angle review pass on completed implementation before handoff or merge.
- `jy-receiving-review` triages review feedback, verifies it against the actual codebase, and supports technical pushback when comments are wrong.
- `jy-loop` keeps working a task iteratively until the stated completion criteria are actually verified.
- `jy-slop-remover` cleans obvious AI-generated code smells without turning into broad stylistic refactoring.

### Routing

- `jy-intent-gate` classifies ambiguous requests before choosing a planning, execution, or research path.

### Research

- `jy-codebase-explore` performs multi-angle repository exploration when the structure is unfamiliar or spread across modules.
- `jy-korean-law-search` routes Korean law, ordinance, precedent, annex, amendment, and procedure queries through the current `korean-law` MCP toolset.
- `jy-library-research` gathers evidence-backed answers about external libraries, packages, APIs, and usage patterns.
- `jy-consult` stays in advisory mode for architecture, reliability, performance, and repeated-failure decisions that need deeper judgment.

### Maintenance

- `jy-checkpoint` stores repo-local checkpoint notes under `.codex/checkpoints/` for pause, resume, and branch handoff workflows.
- `jy-document-release` syncs README, AGENTS instructions, skill docs, and verification packs after shipped changes.
- `jy-ship` closes the final branch workflow with base-branch checks, fresh verification, push, PR/MR creation, and docs sync.
- `jy-env-sync-admin` validates this environment repo and reapplies the repo-owned install surface into the home Codex environment.

### Authoring

- `jy-writing-skills` is the first-party skill authoring guide, including TDD-style scenario validation and deployment checks for skill changes.

## Secret handling

MCP server definitions can live in committed plugin bundles.

Secret values should not.

If an MCP server needs API keys or account tokens, keep those in local machine config or
another local-only secret layer. This repo should only commit the portable server
definition.

For plugin-managed MCP secrets, use a local-only overlay file:

- `~/.codex-env-sync/local/plugins/jy-env-core.mcp.json`

If you are migrating from the previous plugin id, `apply` also reads
`~/.codex-env-sync/local/plugins/codex-env-core.mcp.json` only when the new file does not
exist yet.

Example:

```json
{
  "mcpServers": {
    "korean-law": {
      "env": {
        "LAW_OC": "your-token-here"
      }
    }
  }
}
```

`apply` and `bootstrap` merge that file into the installed plugin bundle at `~/plugins/...`.
The repo copy stays secret-free.

## First run

macOS / Linux:

```bash
./scripts/bootstrap.sh <git-url>
```

Windows PowerShell:

```powershell
.\scripts\bootstrap.ps1 -GitUrl <git-url>
```

## Local development

Inspect the environment defined by this repo:

```bash
python3 -m codex_env_sync.cli inspect --repo-root .
```

Apply the local checkout into your home directory:

```bash
python3 -m codex_env_sync.cli apply --repo-root .
```

On macOS and Linux, that creates symlinks for the repo-managed plugin bundle, skill
discovery surface, and instructions. A later `git pull` in the same checkout updates the
installed Codex surface immediately.

## Layout

```text
codex-env.toml                 # Minimal manifest: plugins + instructions + platform overrides
codex_env_sync/                # Apply engine and CLI
plugins/                       # First-party plugin bundles that get installed into ~/plugins
plugins/jy-env-core/skills/ # First-party Codex skills, authoring source and install source
instructions/                  # Generated instruction artifacts
references/                    # Local authoring references used while building first-party skills
.codex/checkpoints/            # Repo-local ignored checkpoint notes created by jy-checkpoint
.agents/plugins/               # Repo-local marketplace metadata for local plugin discovery
.agents/skills/                # Home install target for Codex native skill discovery
scripts/bootstrap.sh           # First-run shell bootstrap for macOS/Linux
scripts/bootstrap.ps1          # First-run shell bootstrap for Windows
tests/                         # Unit + integration tests
skill-tests/                   # First-party skill verification packs (baseline + pressure scenarios)
```

## Design boundaries

- Upstream open source or company skills are seed material only.
- Raw seed sources normally stay local and are not committed here.
- Curated authoring references that we actively use to build first-party skills may be vendored under `references/`.
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

For first-party skill verification assets and static coverage, see `skill-tests/first-party/`
and run:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```
