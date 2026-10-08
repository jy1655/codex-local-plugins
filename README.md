# Portable Codex Environment Sync

[![Language: English](https://img.shields.io/badge/Language-English-111827?style=for-the-badge)](./README.md)
[![Language: Korean](https://img.shields.io/badge/Language-Korean-0A66C2?style=for-the-badge)](./README.ko.md)

This repository defines a portable, first-party Codex environment. It stages local plugin
bundles, maintains a personal marketplace, and installs compact global instructions without
editing Codex's runtime cache directly.

User-visible plugin and skill labels, descriptions, and suggested prompts are Korean.
Skill labels include the exact invocation name first, for example
`domain-modeling · 도메인 용어와 결정 기록`, so it remains visible in skill lists.
Model-facing skill instructions and trigger descriptions stay English. Shared language,
authorization, privacy, and workspace-preservation rules remain in global `AGENTS.md`
regardless of workflow installation. Machine-specific instructions live in a separate,
user-maintained `LOCAL.md`.

## Pack model

The GPT-6 Astra baseline keeps `max` reasoning with one default core-lite guardrail,
an explicitly invoked orchestration skill, the selected architecture/interview pack,
and an optional iOS memory-analysis pack. `apply` stages the three active bundles under
`~/plugins`, then installs
`INSTALLED_BY_DEFAULT` entries through the Codex CLI.

| Pack | Policy | Skills |
|---|---|---|
| `jy-env-core` — core-lite | `INSTALLED_BY_DEFAULT` | `jy-change-guardrails`, `jy-orchestrate` (explicit only) |
| `jy-env-design` | `INSTALLED_BY_DEFAULT` | `improve-codebase-architecture`, `grill-me`, `grill-with-docs` (explicit only); `grilling`, `codebase-design`, `domain-modeling` |
| `jy-env-ios` | `AVAILABLE` | `ios-memgraph-leaks` — physical-device memory graph analysis |

Invoke `$jy-orchestrate` for the current session to directly coordinate Codex and Claude
planning or implementation, followed by independent Codex DevBlue and Claude verification
of the same candidate. Workers receive bounded assignments and return concise results;
supported findings go back to workers for fixes and review of the affected changes.
There is no separate manager session or manager-replacement count. Independent work can
run concurrently within the runtime's capabilities, while overlapping edits are isolated
or sequenced. It prefers Agent Bridge locally and has `allow_implicit_invocation: false`.
Native context compression is the default; a compact record serves actual handoff or
recovery needs. The invoking session remains responsible for durable Wiki updates under
global/local policy, verifies they were saved, and closes task-owned sessions after results
and follow-ups are complete. No machine-specific Wiki path is embedded in the skill.

The other 23 workflow skills, including `jy-env-planning`, `jy-env-delivery`, and
`jy-env-audit`, are preserved under [archive/](archive/README.md). They are absent from the
manifest and marketplace, are not staged or installed, and are not implicitly invoked.
The archive also preserves the original versions of the ten skills retained in the
2026-09-08 migration. On 2026-10-06, the active iOS pack was reduced to memory leak
analysis for physical-device development; the other eight iOS skills were deleted
from the active pack. Existing historical archives and evaluation inputs remain reference data.

`AVAILABLE` does not uninstall an existing plugin. To migrate an existing installation,
remove the three old workflow packs before applying the reduced marketplace:

```bash
codex plugin remove jy-env-planning@personal-codex
codex plugin remove jy-env-delivery@personal-codex
codex plugin remove jy-env-audit@personal-codex
python3 -m codex_env_sync.cli apply --repo-root .
codex plugin add jy-env-ios@personal-codex
```

Run the remove commands only for installed entries. Update changed active plugins through
`plugin-creator`'s cachebuster flow before `apply`; re-add iOS after staging because it is
optional. `apply` refreshes the default core and design packs. It does not uninstall Codex plugins.
Start a fresh Codex session after changing installed packs. No second
`~/.agents/skills/<pack>` discovery link is created.

## Architecture improvement and grilling

On 2026-10-07, the user chose these workflows after using Matt Pocock's originals in
Claude Code and explicitly requested preservation without simplification. This choice
supersedes the core-lite adoption filter for this pack. Other upstream workflows remain
outside scope until the user tries and selects them.

The separate `jy-env-design` pack preserves version 1.2.3 at `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`:

- `$improve-codebase-architecture`: exploration, visual HTML candidates, user selection,
  then grilling and domain records; full HTML and parallel alternative-design references.
- `$grill-me`: the complete decision-tree interview, question rounds with recommendations,
  fact-finding delegation, and confirmation before acting.
- `$grill-with-docs`: the same interview with inline `CONTEXT.md` and selective ADR recording.

The three entry points are explicit-only. Their reusable `grilling`, `codebase-design`,
and `domain-modeling` skills keep automatic discovery and can also be read through bundled
relative links. Runtime adaptations cover Codex invocation, Korean UI, local delegation,
and configured Wiki/report storage; they do not shorten the original workflows.
See [port boundaries and attribution](plugins/jy-env-design/NOTICE.md).

## iOS memory analysis on physical devices

`jy-env-ios` contains only `ios-memgraph-leaks` and its memory graph summary script.
Capture a `.memgraph` from the connected iPhone or iPad through Xcode's Debug Memory
Graph and File > Export Memory Graph, then analyze the exported file on macOS with
`leaks` and the bundled helper. An existing capture can be used directly.

The skill focuses on object lifetimes, retaining paths, and comparable before/after
evidence. It does not install simulator tooling or register an MCP server. General
builds, debugging, and UI work use the app repository's existing tools and instructions.
See the [skill](plugins/jy-env-ios/skills/ios-memgraph-leaks/SKILL.md) for the workflow.

## Archived research guidance

The Context7 route in `jy-library-research` is archived with the other workflow skills.
It is not an active routing requirement. Its original public-query-only and
`CONTEXT7_API_KEY` handling guidance remains in the archive for an explicit reactivation.

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
core-lite and the design pack.

## Update an existing machine

From that machine's clone of this repository, pull the published changes and apply them:

```bash
git pull --ff-only
python3 -m codex_env_sync.cli apply --repo-root .
codex plugin list --marketplace personal-codex --json
```

Use the machine's configured Python 3.11+ interpreter (`python` on Windows if needed).
`apply` updates the default core and design plugins; confirm each installed version
matches its `plugins/<pack>/.codex-plugin/plugin.json`, then start a fresh Codex session. Machine-local `LOCAL.md` remains separately managed.

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
codex-env.toml                    # Three active plugin sources and their installation policies
codex_env_sync/                   # Inspect/apply/bootstrap engine
archive/                         # Inactive originals, checksums, and restoration notes
plugins/jy-env-core/              # Default core-lite bundle
plugins/jy-env-design/            # Selected Matt Pocock architecture/interview port
plugins/jy-env-ios/               # Optional physical-device memory-analysis pack
instructions/AGENTS.md            # Compact global rules; no eager optional-skill routing
.agents/plugins/marketplace.json  # Local personal marketplace catalog
skill-tests/first-party/          # Skill utility pressure scenarios
skill-tests/UTILITY-EVAL.md       # Three-arm skill utility and reporting contract
tests/                            # Unit and integration tests
```

Active first-party skill sources live under `plugins/jy-env-*/skills/`; inactive originals
live under `archive/` and are excluded from deployment. Upstream or company-shared skills
are local-only seed material; this repo stores only the customized first-party result and
does not vendor third-party runtimes. The user-selected `jy-env-design` port is a deliberate
exception to seed-only rewriting: it preserves the selected original skills and references
with a pinned provenance record and their MIT license. Maintain retained skills here as first-party plugin
assets rather than live dependencies on upstream seeds. Do not install, discover, or follow
instructions under `archive/` unless the user requests a reference or reactivation.

## Tests

Use Python 3.11 to match CI and run the full suite before pushing:

```bash
python3 -X warn_default_encoding -W error::EncodingWarning -m unittest discover -s tests -q
git diff --check
```

The test command treats omitted text encodings as errors on every OS, catching locale
dependencies locally before they fail on Windows. Keep explicit UTF-8 file I/O and the
`.gitattributes` archive byte-preservation and plugin LF rules intact.

Validate pressure-scenario assets:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```

## Skill utility gate

The design pack is retained by the user's direct-use decision. Its explicit-only workflows
are not blocked by implicit-activation gates or a new adoption benchmark. Scenario assets
support behavioral regression checks; they do not establish comparative Codex utility.

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

Evaluation is opt-in when a concrete deficiency needs a comparison. The evaluator discovers
only active sources under `plugins/`; archived sources and historical reports remain
reference material. The current policy tests `gpt-6-astra` at `max` with the default service
tier; the separate judge model keeps its existing role. GPT-5.6 results do not establish
Astra utility. This migration does not run a full model benchmark. See
[skill-tests/UTILITY-EVAL.md](skill-tests/UTILITY-EVAL.md) for evidence limits and
[archive/README.md](archive/README.md) for restoring one candidate.
