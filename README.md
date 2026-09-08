# Portable Codex Environment Sync

[![Language: English](https://img.shields.io/badge/Language-English-111827?style=for-the-badge)](./README.md)
[![Language: Korean](https://img.shields.io/badge/Language-Korean-0A66C2?style=for-the-badge)](./README.ko.md)

This repository defines a portable, first-party Codex environment. It stages local plugin
bundles, maintains a personal marketplace, and installs compact global instructions without
editing Codex's runtime cache directly.

## Pack model

The default environment is intentionally small. `apply` stages all five bundles under
`~/plugins`, then explicitly installs each `INSTALLED_BY_DEFAULT` plugin through the Codex
CLI. Marketplace policy selects the default install set; it is not an installation action
by itself.

| Pack | Policy | Skills |
|---|---|---|
| `jy-env-core` — core-lite | `INSTALLED_BY_DEFAULT` | `jy-change-guardrails`, `jy-debugging`, `jy-test-driven`, `jy-verification-before-completion`, `jy-codebase-explore`, `jy-library-research`, `jy-consult` |
| `jy-env-planning` | `AVAILABLE` | `jy-framing`, `jy-grill-me`, `jy-plan-review`, `jy-writing-plans` |
| `jy-env-delivery` | `AVAILABLE` | `jy-executing-plans`, `jy-worktrees`, `jy-checkpoint`, `jy-document-release`, `jy-ship`, `jy-waterfall`, `jy-env-sync-admin`, `jy-writing-skills` |
| `jy-env-audit` | `AVAILABLE` | `jy-explain-change` (explicit invocation only), `jy-review-all`, `jy-review-work`, `jy-receiving-review`, `jy-slop-remover` |
| `jy-env-ios` | `AVAILABLE` | iOS Simulator debugging, performance, memory, App Intents, and SwiftUI workflows |

Staging and activation are deliberately separate:

- `~/plugins/<pack>` is the local marketplace source.
- `INSTALLED_BY_DEFAULT` makes `apply` and bootstrap run
  `codex plugin add jy-env-core@personal-codex`.
- `AVAILABLE` packs stay inactive until installed from the Plugins Directory or CLI.
- This repo no longer creates a second `~/.agents/skills/<pack>` discovery link, avoiding
  duplicate skill metadata from plugin cache and native discovery.

Install only the optional packs you need:

```bash
codex plugin add jy-env-planning@personal-codex
codex plugin add jy-env-delivery@personal-codex
codex plugin add jy-env-audit@personal-codex
codex plugin add jy-env-ios@personal-codex
```

Start a fresh Codex thread after changing installed packs.

## Pinned XcodeBuildMCP

`jy-env-ios` replaces the upstream `build-ios-apps` plugin on this machine. It runs
`xcodebuildmcp@2.7.0` through `npx` and enables only the `simulator`, `ui-automation`,
and `debugging` workflows. The bundled debugger skill uses the current session-default,
runtime-log, and `elementRef` UI contracts.

Do not enable `build-ios-apps@openai-curated` and `jy-env-ios@personal-codex` together;
both register the `xcodebuildmcp` server name.

## Lazy Context7 research

Context7 is not installed as an MCP server or a separate `jy-context7` skill. The core-lite
`jy-library-research` skill treats it as an optional read-only provider:

1. use an existing `ctx7` command when available;
2. otherwise, when Node.js 18+ and `npx` are available, invoke the pinned
   `ctx7@0.5.5` package only for that research request;
3. fall back to official documentation, source, changelogs, and issue trackers on any CLI,
   network, sandbox, rate-limit, or index failure.

Most public documentation queries work without authentication. If higher limits are needed,
keep the key outside this repo in `CONTEXT7_API_KEY`. The skill never passes a key in command
arguments and never sends private source or credentials to Context7.

## Install surface

- plugin sources: `~/plugins`
- personal marketplace: `~/.agents/plugins/marketplace.json`
- global instructions: `~/.codex/AGENTS.md`
- machine-local instructions (user-maintained, not synced): `~/.codex/LOCAL.md`
- managed state: `~/.codex-env-sync/state.json`
- Codex-owned plugin cache, changed only through `codex plugin`: `~/.codex/plugins/cache`

Local `apply` symlinks plugin sources and instructions on macOS and Linux. Windows uses copy
mode. Bootstrap and `--snapshot` always copy a stable snapshot. After staging, the commands
install or refresh default plugins with `codex plugin add`; optional packs remain explicit
installs. A dirty checkout is not a second live skill-discovery surface.

### Machine-local instructions

Keep machine-specific paths, local tools, and workspace rules in `LOCAL.md` alongside the
installed global `AGENTS.md`: `~/.codex/LOCAL.md` on macOS/Linux or
`%USERPROFILE%\.codex\LOCAL.md` on Windows. If Codex uses a custom `CODEX_HOME`, put
`LOCAL.md` there. When `AGENTS.md` is a symlink, use the installed directory rather than
the repository's `instructions/` directory.

The shared `AGENTS.md` instructs Codex to read this optional file before work; `LOCAL.md`
is not a built-in automatically discovered instruction filename. If it is absent, Codex
continues with the shared rules. `apply`, bootstrap, and snapshot installs leave this file
unmanaged: they do not create, copy, overwrite, or delete it. Keep it outside the repository
and out of `codex-env.toml`. Start a fresh Codex session after changing instructions.

## First run

macOS / Linux:

```bash
./scripts/bootstrap.sh <git-url>
```

Windows PowerShell:

```powershell
.\scripts\bootstrap.ps1 -GitUrl <git-url>
```

Both commands require the `codex` CLI, clone once, install a stable snapshot, and activate
core-lite.

## Local development

Inspect the resolved sources, install modes, and marketplace policies:

```bash
python3 -m codex_env_sync.cli inspect --repo-root .
```

Apply the live checkout:

```bash
python3 -m codex_env_sync.cli apply --repo-root .
```

Install a detached snapshot:

```bash
python3 -m codex_env_sync.cli apply --repo-root . --snapshot
```

After changing an already installed plugin, use the `plugin-creator` cachebuster/reinstall
workflow and start a new thread. Do not edit `~/.codex/plugins/cache` directly.

## Layout

```text
codex-env.toml                    # Five plugin sources and their installation policies
codex_env_sync/                   # Inspect/apply/bootstrap engine
plugins/jy-env-core/              # Default core-lite bundle
plugins/jy-env-planning/          # Optional planning pack
plugins/jy-env-delivery/          # Optional delivery pack
plugins/jy-env-audit/             # Optional audit pack
plugins/jy-env-ios/               # Optional pinned iOS/XcodeBuildMCP pack
instructions/AGENTS.md            # Compact global rules; no eager optional-skill routing
.agents/plugins/marketplace.json  # Local personal marketplace catalog
skill-tests/first-party/          # Skill utility pressure scenarios
skill-tests/UTILITY-EVAL.md       # Three-arm skill utility and reporting contract
tests/                            # Unit and integration tests
```

First-party skill sources live only under `plugins/jy-env-*/skills/`. Upstream or
company-shared skills are local-only seed material; this repo stores only the customized
first-party result and does not vendor third-party runtimes. Maintain retained skills here
as first-party plugin assets rather than live dependencies on upstream seeds. Treat any
material under `archive/` as inactive: do not install, discover, or follow its instructions
unless the user requests a reference or reactivation.

Repo-local working state that should not be committed can live under `.codex/`.
`jy-checkpoint`, when the delivery pack is installed, uses `.codex/checkpoints/`.

## Tests

Run the full suite:

```bash
python3 -m unittest discover -s tests -v
```

Validate pressure-scenario assets:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```

## Skill utility gate

Do not keep a skill merely because its instructions sound reasonable. The utility evaluator
compares the same task on the same model and effort as `baseline` (skill absent), `implicit`
(discoverable), and `explicit` (forced), while holding same-plugin peers constant. It then
blind-scores the responses and applies quality,
token, latency, and implicit-activation gates while recording tool calls and observed skill
reads.

Preview model-call scope first:

```bash
python3 -m codex_env_sync.skill_eval plan \
  --repo-root . --skill jy-change-guardrails
```

Run one skill and inspect freshness or the latest report:

```bash
python3 -m codex_env_sync.skill_eval run \
  --repo-root . --skill jy-change-guardrails

python3 -m codex_env_sync.skill_eval status --repo-root .
python3 -m codex_env_sync.skill_eval report --repo-root .
```

Use `run --candidate --skill <name>` before adopting a new source,
`run --changed-from <ref>` for skill changes, `run --stale` for invalidated evidence, and
`run --all --model <new-model>` for a new model baseline. Reports and raw JSONL are ignored
under `.codex/skill-evals/`; no verdict automatically installs or deletes a skill. See
[skill-tests/UTILITY-EVAL.md](skill-tests/UTILITY-EVAL.md) for thresholds and evidence limits.
